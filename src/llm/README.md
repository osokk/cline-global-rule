# Anthropic API Gateway - Weighted Concurrency Control

A thread-safe gateway for Anthropic API calls with optimal efficiency/safety balance.

## 🎯 Why This Exists

Anthropic's API has burst limits that can cause 429 errors when making multiple concurrent calls. This gateway solves that problem while maintaining high throughput.

## ⚡ Key Features

- **Weighted Semaphore**: Heavy calls (2 slots) vs Light calls (1 slot)
- **Max 3 concurrent slots**: Prevents token spikes
- **Global pacing**: 0.8s minimum gap between request starts
- **Smart backoff**: Only retries on actual limit hits (429, overloaded, etc.)
- **Jitter**: Randomized backoff to prevent thundering herd
- **Per-call timeouts**: Prevents hanging requests
- **Hard max_tokens cap**: Defaults to 1200 if not specified

## 🚀 Quick Start

### Installation

1. Ensure the `cline-global-rules` directory is in your Python path
2. Install the Anthropic SDK: `pip install anthropic`
3. Set your API key: `export ANTHROPIC_API_KEY=your_key_here`

### Basic Usage

```python
from cline_global_rules.src.llm.anthropic_gateway import gateway

# Heavy call (long context, large output, research)
response = gateway.create_message(
    size="heavy",
    model="claude-sonnet-4-20250514",
    messages=[
        {"role": "user", "content": "Analyze this large dataset..."}
    ],
    max_tokens=1400,
)

# Light call (formatting, extraction, small tasks)
response = gateway.create_message(
    size="light",
    model="claude-sonnet-4-20250514",
    messages=[
        {"role": "user", "content": "Extract the key points from: ..."}
    ],
    max_tokens=500,
)
```

## 📊 Concurrency Rules

The gateway enforces these rules automatically:

| Scenario | Allowed? | Reason |
|----------|----------|--------|
| 3 light calls | ✅ Yes | 3 slots available |
| 1 heavy + 1 light | ✅ Yes | 2 + 1 = 3 slots |
| 2 heavy calls | ❌ No | Would need 4 slots |
| 1 heavy + 2 light | ❌ No | Would need 4 slots |

## 🏷️ When to Use "heavy" vs "light"

### Use `size="heavy"` for:

- Long-context research prompts (>4000 tokens input)
- Synthesis prompts that combine multiple sources
- Anything with large artifacts or conversation history
- Expected outputs above ~800 tokens
- Code generation with large context
- Document analysis or summarization of long texts

### Use `size="light"` for:

- Formatting or reformatting text
- Data extraction from small inputs
- Small critiques or reviews
- Summaries of already-small inputs
- Classification tasks
- Simple Q&A with minimal context
- Expected outputs below ~500 tokens

## 🔧 Advanced Configuration

### Custom Gateway Instance

```python
from cline_global_rules.src.llm.anthropic_gateway import AnthropicGateway

# Create a custom gateway with different settings
custom_gateway = AnthropicGateway(
    api_key="your_key_here",           # Or use env var
    max_inflight_weight=3,              # Total concurrent slots
    min_start_gap_seconds=0.8,          # Pacing between starts
    max_retries=5,                      # Retry attempts
    base_backoff_seconds=1.5,           # Base backoff time
    default_timeout_seconds=120.0,      # Per-call timeout
    default_max_tokens=1200,            # Default max_tokens
)

response = custom_gateway.create_message(
    size="heavy",
    model="claude-sonnet-4-20250514",
    messages=messages,
)
```

### All Anthropic Parameters Supported

The gateway passes through all standard Anthropic API parameters:

```python
response = gateway.create_message(
    size="heavy",
    model="claude-sonnet-4-20250514",
    messages=messages,
    max_tokens=2000,
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    stop_sequences=["END"],
    system="You are a helpful assistant",
    metadata={"user_id": "123"},
)
```

## 🔄 Retry Behavior

The gateway automatically retries on these errors:

- `429` - Rate limit exceeded
- `overloaded` - API overloaded
- `timeout` - Request timed out
- `connection reset` - Network error
- `internal server error` - Server error
- `temporarily unavailable` - Transient error

**Non-retryable errors** (raised immediately):
- Invalid API key
- Invalid parameters
- Content policy violations
- Any other client errors

### Backoff Formula

```
sleep_time = base_backoff * (2 ^ attempt) + random(0, 0.75)
```

Example with `base_backoff=1.5`:
- Attempt 0: 1.5-2.25s
- Attempt 1: 3.0-3.75s
- Attempt 2: 6.0-6.75s
- Attempt 3: 12.0-12.75s
- Attempt 4: 24.0-24.75s

## 📈 Performance Characteristics

### Throughput Comparison

| Setup | Calls/min | Risk Level | Use Case |
|-------|-----------|------------|----------|
| Serial (1 at a time) | ~40 | Very Low | Legacy/safe |
| This Gateway (3 slots) | ~100-120 | Low | **Recommended** |
| Naive parallel (10+) | ~150+ | High | ⚠️ Causes 429s |

### Why 3 Slots is Optimal

- **Speed**: 2-3x faster than serial
- **Safety**: Prevents token burst limits
- **Flexibility**: Allows small calls to overlap
- **Protection**: Never allows 2 heavy calls simultaneously

## 🛠️ Integration Examples

### Replace Existing Code

**Before:**
```python
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=messages,
    max_tokens=2000,
)
```

**After:**
```python
from cline_global_rules.src.llm.anthropic_gateway import gateway

response = gateway.create_message(
    size="heavy",  # Classify based on your use case
    model="claude-sonnet-4-20250514",
    messages=messages,
    max_tokens=2000,
)
```

### Multi-threaded Usage

The gateway is fully thread-safe:

```python
import concurrent.futures
from cline_global_rules.src.llm.anthropic_gateway import gateway

def process_item(item):
    return gateway.create_message(
        size="light",
        model="claude-sonnet-4-20250514",
        messages=[{"role": "user", "content": f"Process: {item}"}],
        max_tokens=500,
    )

# Process 100 items with automatic concurrency control
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(process_item, items))
```

The gateway will automatically limit to 3 concurrent calls regardless of thread pool size.

### Async/Await Pattern

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from cline_global_rules.src.llm.anthropic_gateway import gateway

async def async_call(messages, size="light"):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(
            pool,
            lambda: gateway.create_message(
                size=size,
                model="claude-sonnet-4-20250514",
                messages=messages,
                max_tokens=800,
            )
        )

# Use in async context
async def main():
    tasks = [
        async_call(msg1, "heavy"),
        async_call(msg2, "light"),
        async_call(msg3, "light"),
    ]
    results = await asyncio.gather(*tasks)
```

## 🎛️ Tuning Guide

### Conservative (Lower Risk)

```python
gateway = AnthropicGateway(
    max_inflight_weight=2,          # Only 2 slots
    min_start_gap_seconds=1.0,      # Slower pacing
    max_retries=3,                  # Fewer retries
)
```

### Aggressive (Higher Throughput)

```python
gateway = AnthropicGateway(
    max_inflight_weight=4,          # 4 slots (risky!)
    min_start_gap_seconds=0.6,      # Faster pacing
    max_retries=7,                  # More retries
)
```

**⚠️ Warning**: Going above 3 slots increases 429 risk significantly.

## 📋 Best Practices

### 1. Centralize All Calls

Create a single gateway instance and import it everywhere:

```python
# my_project/llm/client.py
from cline_global_rules.src.llm.anthropic_gateway import gateway

# Export for project-wide use
__all__ = ["gateway"]
```

### 2. Classify Calls Correctly

```python
# ✅ Good
gateway.create_message(size="heavy", ...)  # Long research prompt
gateway.create_message(size="light", ...)  # Small extraction

# ❌ Bad
gateway.create_message(size="light", ...)  # Actually a huge prompt!
```

### 3. Set Appropriate max_tokens

```python
# ✅ Good - specific limits
gateway.create_message(size="light", max_tokens=300, ...)
gateway.create_message(size="heavy", max_tokens=1500, ...)

# ❌ Bad - unnecessarily large
gateway.create_message(size="light", max_tokens=4000, ...)
```

### 4. Trim Context

```python
# ✅ Good - only send what's needed
messages = trim_old_messages(full_history, max_messages=10)
gateway.create_message(size="heavy", messages=messages, ...)

# ❌ Bad - sending entire history every time
gateway.create_message(size="heavy", messages=full_history, ...)
```

### 5. Stagger Batch Launches

```python
import time

for batch in batches:
    process_batch(batch)
    time.sleep(0.5)  # Small gap between batches
```

## 🐛 Troubleshooting

### Still Getting 429 Errors

1. Check if you're using multiple gateway instances (use singleton)
2. Verify `size` classification is correct
3. Reduce `max_inflight_weight` to 2
4. Increase `min_start_gap_seconds` to 1.0
5. Check for other processes using the same API key

### Slow Performance

1. Ensure you're using `size="light"` for small tasks
2. Check if `min_start_gap_seconds` is too high
3. Verify network latency isn't the bottleneck
4. Consider if serial processing is actually faster for your use case

### Timeout Errors

1. Increase `default_timeout_seconds`
2. Reduce `max_tokens` for the call
3. Simplify the prompt or reduce context
4. Check Anthropic API status

## 📚 Additional Resources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Rate Limits Guide](https://docs.anthropic.com/en/api/rate-limits)
- [Best Practices](https://docs.anthropic.com/en/api/best-practices)

## 🤝 Contributing

This is part of the `cline-global-rules` shared utilities. To modify:

1. Edit files in `cline-global-rules/src/llm/`
2. Test thoroughly with your use case
3. Update this README with any changes
4. Sync to other machines via git

## 📄 License

Part of the Cline Global Rules project. Use freely across all your Roo/Cline projects.
