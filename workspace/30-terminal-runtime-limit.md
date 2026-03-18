# RULE — Terminal Process Runtime Limit (30 Minutes Maximum)

> Terminal processes launched by Cline (backtests, optimizations, data pipelines) must be designed to complete within **30 minutes maximum**.

---

## Context

Long-running terminal processes block the Cline session, consume system resources, and risk timeout or loss of intermediate results. All compute-intensive tasks launched by Cline must be structured to finish within a predictable time window.

## Rule

### ⏱️ 30-Minute Hard Limit

- Any terminal process (backtest, optimization, data pipeline) launched by Cline **must complete within 30 minutes**
- If a task is expected to exceed 30 minutes, **warn the user before launching** and offer to break it into smaller chunks

### 🔄 Chunking with Checkpoint/Resume

If a task will take longer than 30 minutes, it **must** be broken into smaller chunks with checkpoint/resume capability:

#### Optimization Runs
- Break the parameter grid into batches (e.g., **1000 configs per batch**)
- Save intermediate results to disk after each batch completes
- Support resuming from the last checkpoint so no work is lost
- Example: a 5000-config grid → 5 batches of 1000, each completing in ~10–15 minutes

#### Data Pipelines
- Use **incremental processing** with batch size limits
- Process data in date ranges or symbol batches rather than all-at-once
- Write partial results after each batch

### 📊 Progress Logging

- Long-running processes **must log progress every 30–60 seconds**
- Logs should include: current progress (e.g., `1100/3600 backtests`), elapsed time, and estimated time remaining
- This allows the user to estimate completion time and decide whether to continue or abort

### ⚠️ Pre-Launch Warning

Before launching any process that might exceed 30 minutes:

1. **Estimate the runtime** based on grid size, data volume, or historical benchmarks
2. **Warn the user** with the estimate: _"This optimization has 5000 configs and is estimated to take ~45 minutes. Want me to break it into 5 batches of 1000?"_
3. **Offer to break it up** into smaller chunks that each fit within the 30-minute window

## Files Commonly Affected

| File | Role |
|------|------|
| `workspace/run_optimization.py` | Backtest optimization entry point |
| `workspace/optimizer.py` | Parameter grid generation + dispatch |
| `workspace/backtest_engine.py` | Core backtest settlement loop |
| `src/ingest_ohlcv_1m.py` | OHLCV data ingestion pipeline |
| `src/ingest_funding_rates.py` | Funding rate ingestion pipeline |
