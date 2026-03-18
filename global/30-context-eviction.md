# GLOBAL RULE — Context Eviction Hard Stop

**ABSOLUTE HARD STOP — applies to ALL projects**

**INTERNALIZE THIS RULE IMMEDIATELY. It overrides ALL other rules.**

---

## The Rule

If a `read_file` tool call returns this message:

```
[NOTE] This file read has been removed to save space in the context window
```

**DO NOT re-read that file. Not once. Not ever in this session.**

---

## Why This Matters

This message means the system evicted the file content to free context space. Re-reading will succeed momentarily, then get evicted again immediately — creating an infinite loop that costs $100+ per session. This happened on 2026-03-17 and burned over $100 in a single session.

---

## What to Do Instead

1. **STOP all file reads immediately**
2. Work with what you already have in memory from earlier in the session
3. If you cannot proceed without the evicted file, call `attempt_completion` with:
   ```
   "Context window too full to continue. File [X] was evicted. Please start a new task."
   ```
4. **NEVER call `read_file` on any file that returned the eviction message in this session**

---

## Detection — Before Calling `read_file`

Ask yourself:
- "Did this file return the eviction message earlier in this session?"
- If YES → **DO NOT READ IT. Use memory or stop.**

---

## This Rule Applies to ALL Files

Including:
- TASKS.md
- AGENT_STATE.md
- PROJECT_INDEX.md
- QUICK_STATE.md
- Source files
- Config files
- Any file that was evicted

---

## Root Cause (2026-03-17)

Cline repeatedly re-read large documentation files after they were evicted, creating a loop:
1. Read file → evicted to save space
2. Re-read file → evicted again
3. Re-read file → evicted again
4. ... (repeat 50+ times)

This burned $100+ in API costs with zero progress.
