# Anthropic Gateway Setup Guide

Quick setup instructions for using the Anthropic API Gateway across all your machines.

## 🚀 One-Time Setup Per Machine

### 1. Install Dependencies

```bash
pip install anthropic
```

### 2. Set API Key

**Option A: Environment Variable (Recommended)**
```bash
# Linux/Mac
export ANTHROPIC_API_KEY="your_key_here"

# Windows CMD
set ANTHROPIC_API_KEY=your_key_here

# Windows PowerShell
$env:ANTHROPIC_API_KEY="your_key_here"
```

**Option B: In Code**
```python
from cline_global_rules.src.llm.anthropic_gateway import AnthropicGateway

gateway = AnthropicGateway(api_key="your_key_here")
```

### 3. Ensure Python Path

The `cline-global-rules` directory should be in your Python path. If not:

**Option A: Add to PYTHONPATH**
```bash
# Linux/Mac
export PYTHONPATH="${PYTHONPATH}:/path/to/cline-global-rules"

# Windows
set PYTHONPATH=%PYTHONPATH%;C:\path\to\cline-global-rules
```

**Option B: Add in code**
```python
import sys
sys.path.insert(0, '/path/to/cline-global-rules')
```

**Option C: Install as editable package**
```bash
cd /path/to/cline-global-rules
pip install -e .
```

## 📝 Quick Test

Create a test file to verify setup:

```python
# test_gateway.py
from cline_global_rules.src.llm.anthropic_gateway import gateway

response = gateway.create_message(
    size="light",
    model="claude-sonnet-4-20250514",
    messages=[
        {"role": "user", "content": "Say 'Gateway working!' and nothing else."}
    ],
    max_tokens=50,
)

print(response.content[0].text)
```

Run it:
```bash
python test_gateway.py
```

Expected output: `Gateway working!`

## 🔄 Rollout to Existing Project

### Step 1: Find All Anthropic Calls

```bash
# Search for direct Anthropic usage
grep -r "from anthropic import" .
grep -r "Anthropic(" .
grep -r "messages.create" .
```

### Step 2: Replace One File at a Time

**Before:**
```python
from anthropic import Anthropic

client = Anthropic()
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
    size="heavy",  # or "light" - classify appropriately
    model="claude-sonnet-4-20250514",
    messages=messages,
    max_tokens=2000,
)
```

### Step 3: Classify Each Call

For each replacement, decide if it's "heavy" or "light":

- **Heavy**: Long prompts, research, synthesis, large outputs (>800 tokens)
- **Light**: Formatting, extraction, small tasks, outputs (<500 tokens)

### Step 4: Test Incrementally

1. Replace calls in one module
2. Run tests for that module
3. Verify no errors
4. Move to next module

### Step 5: Monitor Performance

After rollout, check:
- Are you still getting 429 errors? → Reduce `max_inflight_weight`
- Is it too slow? → Verify `size` classification is correct
- Timeouts? → Increase `default_timeout_seconds`

## 🎯 Project-Specific Wrapper (Optional)

Create a project-specific wrapper for convenience:

```python
# my_project/llm/client.py
from cline_global_rules.src.llm.anthropic_gateway import gateway

def research_call(messages, max_tokens=1500):
    """Heavy call for research/synthesis."""
    return gateway.create_message(
        size="heavy",
        model="claude-sonnet-4-20250514",
        messages=messages,
        max_tokens=max_tokens,
    )

def helper_call(messages, max_tokens=500):
    """Light call for small tasks."""
    return gateway.create_message(
        size="light",
        model="claude-sonnet-4-20250514",
        messages=messages,
        max_tokens=max_tokens,
    )
```

Then use throughout your project:
```python
from my_project.llm.client import research_call, helper_call

# Easy to use
response = research_call(messages)
response = helper_call(messages)
```

## 🔧 Configuration Per Project

If different projects need different settings:

```python
# my_project/llm/client.py
from cline_global_rules.src.llm.anthropic_gateway import AnthropicGateway

# Custom gateway for this project
gateway = AnthropicGateway(
    max_inflight_weight=2,          # More conservative
    min_start_gap_seconds=1.0,      # Slower pacing
)

def create_message(**kwargs):
    return gateway.create_message(**kwargs)
```

## 📊 Monitoring & Debugging

### Enable Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("anthropic_gateway")
```

### Track Metrics

```python
import time
from cline_global_rules.src.llm.anthropic_gateway import gateway

start = time.time()
response = gateway.create_message(...)
elapsed = time.time() - start

print(f"Call took {elapsed:.2f}s")
print(f"Tokens used: {response.usage.input_tokens + response.usage.output_tokens}")
```

### Common Issues

**Import Error:**
```
ModuleNotFoundError: No module named 'cline_global_rules'
```
→ Fix: Add to PYTHONPATH or install as editable package

**API Key Error:**
```
AuthenticationError: Invalid API key
```
→ Fix: Set ANTHROPIC_API_KEY environment variable

**Still Getting 429s:**
```
RateLimitError: 429 Too Many Requests
```
→ Fix: Reduce `max_inflight_weight` to 2 or increase `min_start_gap_seconds`

## 🌐 Multi-Machine Sync

Since this is in `cline-global-rules`, sync across machines:

```bash
# On machine 1 (after making changes)
cd cline-global-rules
git add src/llm/
git commit -m "Add Anthropic gateway"
git push

# On machine 2
cd cline-global-rules
git pull
```

All machines will now have the same gateway implementation.

## ✅ Verification Checklist

- [ ] `pip install anthropic` completed
- [ ] `ANTHROPIC_API_KEY` environment variable set
- [ ] `cline-global-rules` in Python path
- [ ] Test script runs successfully
- [ ] Existing code identified for migration
- [ ] First module migrated and tested
- [ ] Performance monitored after rollout

## 🆘 Need Help?

Check the main [README.md](./README.md) for:
- Detailed usage examples
- Performance tuning guide
- Troubleshooting section
- Best practices

## 📈 Recommended Rollout Order

1. **Test environment**: Migrate and test one small script
2. **Development**: Migrate dev/test code
3. **Staging**: Migrate staging environment
4. **Production**: Migrate production (monitor closely)

Start conservative (2 slots, 1.0s gap), then optimize based on actual performance.
