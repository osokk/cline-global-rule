# Anthropic Gateway - Quick Reference Card

## 🚀 Import

```python
from cline_global_rules.src.llm.anthropic_gateway import gateway
```

## 📞 Basic Usage

```python
# Heavy call (long context, research, >800 tokens output)
response = gateway.create_message(
    size="heavy",
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "..."}],
    max_tokens=1400,
)

# Light call (formatting, extraction, <500 tokens output)
response = gateway.create_message(
    size="light",
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "..."}],
    max_tokens=500,
)
```

## 🏷️ Size Classification

| Use `size="heavy"` | Use `size="light"` |
|-------------------|-------------------|
| Long context (>4K tokens) | Short context (<2K tokens) |
| Research/synthesis | Formatting/extraction |
| Large artifacts | Small tasks |
| Output >800 tokens | Output <500 tokens |
| Code generation | Classification |
| Document analysis | Simple Q&A |

## ⚙️ Concurrency Rules

| Scenario | Allowed? |
|----------|----------|
| 3 light calls | ✅ Yes (3 slots) |
| 1 heavy + 1 light | ✅ Yes (3 slots) |
| 2 heavy calls | ❌ No (needs 4 slots) |
| 1 heavy + 2 light | ❌ No (needs 4 slots) |

## 🔧 Default Settings

```python
max_inflight_weight = 3        # Total concurrent slots
min_start_gap_seconds = 0.8    # Gap between starts
max_retries = 5                # Retry attempts
base_backoff_seconds = 1.5     # Base backoff time
default_timeout_seconds = 120  # Per-call timeout
default_max_tokens = 1200      # Default max_tokens
```

## 🔄 Retry Behavior

**Retries on:**
- 429 (rate limit)
- Overloaded
- Timeout
- Connection errors
- Server errors

**Does NOT retry:**
- Invalid API key
- Invalid parameters
- Content policy violations

## 📊 Performance

- **Serial**: ~40 calls/min
- **This gateway**: ~100-120 calls/min (2-3x faster)
- **Naive parallel**: ~150+ calls/min (causes 429s ⚠️)

## 🛠️ All Parameters

```python
response = gateway.create_message(
    size="heavy",                    # Required: "heavy" or "light"
    model="claude-sonnet-4-20250514", # Required
    messages=[...],                  # Required
    max_tokens=1400,                 # Optional (default: 1200)
    temperature=0.7,                 # Optional
    top_p=0.9,                       # Optional
    top_k=40,                        # Optional
    stop_sequences=["END"],          # Optional
    system="You are...",             # Optional
    metadata={"user_id": "123"},     # Optional
    timeout=120.0,                   # Optional (default: 120)
)
```

## 🧵 Thread-Safe Usage

```python
from concurrent.futures import ThreadPoolExecutor

def process(item):
    return gateway.create_message(size="light", ...)

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(process, items))
# Gateway automatically limits to 3 concurrent calls
```

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Add `cline-global-rules` to PYTHONPATH |
| `AuthenticationError` | Set `ANTHROPIC_API_KEY` env var |
| Still getting 429s | Reduce `max_inflight_weight` to 2 |
| Too slow | Check `size` classification |
| Timeouts | Increase `default_timeout_seconds` |

## 📚 Full Documentation

- [README.md](./README.md) - Complete usage guide
- [SETUP.md](./SETUP.md) - Installation instructions
- [CHANGELOG.md](./CHANGELOG.md) - Version history

## 💡 Pro Tips

1. **Centralize**: Use one gateway instance across your project
2. **Classify correctly**: Wrong `size` defeats the purpose
3. **Set max_tokens**: Don't use unnecessarily large limits
4. **Trim context**: Don't resend giant histories
5. **Stagger batches**: Add small delays between batch launches

## 🎯 Migration Pattern

```python
# Before
from anthropic import Anthropic
client = Anthropic()
response = client.messages.create(...)

# After
from cline_global_rules.src.llm.anthropic_gateway import gateway
response = gateway.create_message(size="heavy", ...)
```

---

**Version**: 1.0.0 | **Date**: 2026-03-18 | **Part of**: cline-global-rules
