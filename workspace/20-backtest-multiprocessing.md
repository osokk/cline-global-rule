# RULE — Backtest Optimization: Multiprocessing (Local Only)

> Use multicore parallelization for backtest grid search on the **local dev machine** only.
> **NEVER** enable it on the VPS (exec-01).

---

## Context

The bottleneck in backtest optimization is the single-threaded pure-Python settlement loop in `backtest_engine.py` — `iterrows()` + sequential config iteration inside `run_batch()`. Grid search over many parameter combos is embarrassingly parallel and benefits hugely from `multiprocessing.Pool`.

## Rule

When modifying or running backtest optimization code (`run_optimization.py`, `backtest_engine.py`, `optimizer.py`):

### ✅ Local Machine (Windows, this dev machine)
- Use `multiprocessing.Pool` (or `ProcessPoolExecutor`) to parallelize `run_batch()` calls across CPU cores
- This dramatically speeds up grid search on the multi-core local machine

### ❌ VPS (exec-01, 45.32.46.76)
- Do **NOT** apply multicore parallelization on the VPS
- The VPS has limited CPU/memory and runs the **live trading bot** — parallelized backtests could starve the bot process and cause missed trades or crashes

## Suggested Implementation

Detect the environment and only enable multiprocessing on local:

```python
import os

def _use_parallel():
    """Enable multiprocessing only on local dev machine, never on VPS."""
    # Explicit opt-in via env var (highest priority)
    env_flag = os.environ.get("CREW33_PARALLEL")
    if env_flag is not None:
        return env_flag == "1"
    # Auto-detect: Windows == local dev machine
    return os.name == "nt"
```

- **`CREW33_PARALLEL=1`** — force-enable (local)
- **`CREW33_PARALLEL=0`** — force-disable (VPS, or local if you want single-threaded)
- **No env var set** — auto-detect via `os.name == 'nt'` (Windows = local, Linux = VPS)

## Files Affected

| File | Role |
|------|------|
| `workspace/run_optimization.py` | Entry point — orchestrates grid search |
| `backtest_engine.py` | Core settlement loop (`run_batch()`) |
| `optimizer.py` | Parameter grid generation + dispatch |
