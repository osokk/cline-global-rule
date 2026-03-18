# GLOBAL RULE — API Budget Management

**MANDATORY — applies to ALL projects**

---

## Default Task Budget

**$10 USD per task**

---

## The Rule

When estimated API spend reaches **$10**:

1. **STOP immediately**
2. Report to user:
   ```
   "API budget limit reached ($10). Current spend: $X.XX.
   
   Progress so far: [brief summary]
   
   To continue, please approve another $10 budget increment."
   ```
3. **Wait for explicit user approval** before continuing

---

## Why This Matters

- Prevents runaway costs from infinite loops (context eviction, anti-loop violations)
- Forces periodic check-ins on complex tasks
- Gives user visibility into cost vs. progress

---

## Exceptions

User may specify a different budget at task start:
- "Budget: $20 for this task"
- "No budget limit for this session"

If no budget is specified, default to $10.

---

## Tracking Spend

Roo/Cline displays current cost in the environment details. Check it periodically during long tasks.

If cost is approaching $10, proactively report:
```
"Approaching budget limit. Current spend: $8.50 / $10.00. 
Estimated $1.50 more to complete [remaining work]."
```

---

## Cost-Saving Strategies

When approaching budget limit:

1. **Stop reading large files** — work with what's in memory
2. **Summarize instead of re-reading** — use memory from earlier in session
3. **Complete current subtask** — reach a clean stopping point
4. **Update documentation** — ensure progress is saved before stopping
5. **Call `attempt_completion`** — present results and await next steps
