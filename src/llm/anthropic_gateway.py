"""
Anthropic API Gateway with Weighted Concurrency Control

This module provides a thread-safe gateway for Anthropic API calls with:
- Weighted semaphore (3 max slots: heavy=2, light=1)
- Global pacing between request starts (0.8s default)
- Aggressive backoff only on actual limit hits (429, overloaded, etc.)
- Jitter and per-call timeouts
- Hard cap on max_tokens

Best practical setup:
- Max in-flight calls: 3
- Heavy calls: cost 2 slots (never allow 2 heavy calls at once)
- Light calls: cost 1 slot
- Global minimum gap between request starts: 0.6-1.0s
- Backoff: only on 429 / overloaded / transient server errors

Why this is the best efficiency/safety balance:
- Much faster than serial
- Prevents the worst token spikes
- Still lets small/helper calls overlap
- Keeps one big research call from colliding with another big one
"""

import os
import time
import random
import threading
from contextlib import contextmanager
from anthropic import Anthropic


class WeightedSemaphore:
    """
    Thread-safe semaphore that supports weighted acquire/release.
    
    Allows different operations to consume different amounts of capacity.
    For example, with capacity=3:
    - 3 light operations (weight=1 each) can run concurrently
    - 1 heavy (weight=2) + 1 light (weight=1) can run concurrently
    - 2 heavy operations cannot run together (would need 4 slots)
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.available = capacity
        self.cond = threading.Condition()

    def acquire(self, weight: int):
        """Block until weight slots are available, then acquire them."""
        with self.cond:
            while self.available < weight:
                self.cond.wait()
            self.available -= weight

    def release(self, weight: int):
        """Release weight slots back to the pool."""
        with self.cond:
            self.available += weight
            if self.available > self.capacity:
                self.available = self.capacity
            self.cond.notify_all()


class AnthropicGateway:
    """
    Thread-safe gateway for Anthropic API calls with weighted concurrency control.
    
    Features:
    - Weighted semaphore prevents token spikes (heavy=2 slots, light=1 slot)
    - Global pacing ensures minimum gap between request starts
    - Automatic retry with exponential backoff on transient errors
    - Per-call timeouts and max_tokens defaults
    
    Usage:
        from cline_global_rules.src.llm.anthropic_gateway import gateway
        
        # Heavy call (long context, large output)
        resp = gateway.create_message(
            size="heavy",
            model="claude-sonnet-4-6",
            messages=messages,
            max_tokens=1400,
        )
        
        # Light call (small helper, extraction, formatting)
        resp = gateway.create_message(
            size="light",
            model="claude-sonnet-4-6",
            messages=messages,
            max_tokens=500,
        )
    """
    
    def __init__(
        self,
        api_key: str | None = None,
        max_inflight_weight: int = 3,
        min_start_gap_seconds: float = 0.8,
        max_retries: int = 5,
        base_backoff_seconds: float = 1.5,
        default_timeout_seconds: float = 120.0,
        default_max_tokens: int = 1200,
    ):
        """
        Initialize the Anthropic gateway.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            max_inflight_weight: Maximum total weight of concurrent calls (default: 3)
            min_start_gap_seconds: Minimum time between request starts (default: 0.8s)
            max_retries: Maximum retry attempts on transient errors (default: 5)
            base_backoff_seconds: Base backoff time for exponential retry (default: 1.5s)
            default_timeout_seconds: Default timeout per call (default: 120s)
            default_max_tokens: Default max_tokens if not specified (default: 1200)
        """
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.slots = WeightedSemaphore(max_inflight_weight)
        self.min_start_gap_seconds = min_start_gap_seconds
        self.max_retries = max_retries
        self.base_backoff_seconds = base_backoff_seconds
        self.default_timeout_seconds = default_timeout_seconds
        self.default_max_tokens = default_max_tokens

        self._start_lock = threading.Lock()
        self._last_start_ts = 0.0

    def _pace_start(self):
        """Enforce minimum gap between request starts."""
        with self._start_lock:
            now = time.time()
            elapsed = now - self._last_start_ts
            wait_s = self.min_start_gap_seconds - elapsed
            if wait_s > 0:
                time.sleep(wait_s)
            self._last_start_ts = time.time()

    def _is_retryable(self, exc: Exception) -> bool:
        """
        Check if an exception is retryable.
        
        Retries on:
        - 429 rate limit errors
        - Overloaded errors
        - Timeout errors
        - Connection errors
        - Internal server errors
        """
        msg = str(exc).lower()
        retry_terms = [
            "429",
            "rate limit",
            "rate_limit",
            "overloaded",
            "timeout",
            "timed out",
            "temporarily unavailable",
            "connection reset",
            "internal server error",
            "server error",
            "api_error",
        ]
        return any(term in msg for term in retry_terms)

    def _backoff_sleep(self, attempt: int):
        """
        Sleep with exponential backoff and jitter.
        
        Formula: base * (2 ^ attempt) + random(0, 0.75)
        """
        sleep_s = self.base_backoff_seconds * (2 ** attempt) + random.uniform(0, 0.75)
        time.sleep(sleep_s)

    @contextmanager
    def _acquire_weight(self, weight: int):
        """Context manager for acquiring and releasing weighted slots."""
        self.slots.acquire(weight)
        try:
            yield
        finally:
            self.slots.release(weight)

    def create_message(
        self,
        *,
        size: str = "light",   # "light" or "heavy"
        **kwargs,
    ):
        """
        Create a message via Anthropic API with weighted concurrency control.
        
        Args:
            size: "light" (1 slot) or "heavy" (2 slots)
                  Use "heavy" for:
                  - Long-context research prompts
                  - Synthesis prompts
                  - Anything with large artifacts/history
                  - Outputs above ~800 tokens
                  
                  Use "light" for:
                  - Formatting
                  - Extraction
                  - Small critiques
                  - Summaries of already-small inputs
            
            **kwargs: All standard Anthropic messages.create() parameters
                     (model, messages, max_tokens, temperature, etc.)
        
        Returns:
            Anthropic Message response object
        
        Raises:
            RuntimeError: If all retries are exhausted
            Exception: If a non-retryable error occurs
        """
        weight = 2 if size == "heavy" else 1

        # Apply defaults if not specified
        if "max_tokens" not in kwargs:
            kwargs["max_tokens"] = self.default_max_tokens
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.default_timeout_seconds

        last_exc = None
        for attempt in range(self.max_retries):
            with self._acquire_weight(weight):
                try:
                    self._pace_start()
                    return self.client.messages.create(**kwargs)
                except Exception as exc:
                    last_exc = exc
                    # If not retryable, raise immediately
                    if not self._is_retryable(exc):
                        raise

            # Backoff before retry (outside the weight lock)
            self._backoff_sleep(attempt)

        raise RuntimeError(f"Anthropic call failed after {self.max_retries} retries: {last_exc}")


# Global singleton instance with recommended defaults
gateway = AnthropicGateway(
    max_inflight_weight=3,
    min_start_gap_seconds=0.8,
    max_retries=5,
    base_backoff_seconds=1.5,
    default_timeout_seconds=120.0,
    default_max_tokens=1200,
)
