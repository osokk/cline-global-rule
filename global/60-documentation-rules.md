# GLOBAL RULE — Documentation Discipline

**MANDATORY — applies to ALL projects**

---

## STARTING A NEW TASK — Read MD Files First

**RULE: NEVER read source code to understand the project. Read MD files first.**

Before reading ANY source code, read the relevant MD files for the task:

1. Read the startup/state MD files (QUICK_STATE.md, STATUS.md, ARCHITECTURE.md, etc.)
2. Identify which MD files are relevant to the specific task
3. Only read source files you need to **modify** — not to understand

**Do NOT read MD files unrelated to the task at hand.** If fixing a bug in the Discord bot, read bot-related docs only — not strategy docs, not pipeline docs.

**Do NOT scan the entire codebase.** Use PROJECT_INDEX.md or AGENT_MAP.md to navigate to the specific file needed.

---

## AFTER EVERY TASK — Document Work in MD Files

After completing any task, you MUST update the relevant MD files:

- **STATUS.md** — what was done, what changed, current state, next steps, any blockers
- **WORKLOG.md** — append a dated entry summarizing the work done
- **TASKS.md** — mark completed tasks, add any new tasks discovered
- **ARCHITECTURE.md** — update if any structural changes were made

**Which MD files to update depends on the task:**

| Task Type | Files to Update |
|-----------|----------------|
| Bug fix | STATUS.md + WORKLOG.md |
| New feature | STATUS.md + WORKLOG.md + ARCHITECTURE.md (if structure changed) |
| Config change | STATUS.md + WORKLOG.md |
| Research/analysis | STRATEGY_RESEARCH_LOG.md or relevant research doc |

**If the relevant MD file doesn't exist, CREATE it.**

---

## Documentation Standards

All decisions, parameters, and design choices must be documented with reasoning. **No undocumented arbitrary values.**

Every project MUST have these files, always up to date:

- **ARCHITECTURE.md** — system structure, data flow, components, dependencies
- **STATUS.md** — current state, what's working, what's broken, last session summary

---

## Why This Matters

- **Continuity across sessions** — next session (or next AI agent) can pick up where you left off
- **Cross-machine sync** — documentation travels with git, code context doesn't
- **Debugging** — when something breaks, STATUS.md shows what changed recently
- **Onboarding** — new collaborators (human or AI) can understand the project quickly

---

## Anti-Pattern: Reading Source to Understand

**DON'T:**
```
1. Read main.py to understand what the app does
2. Read config.py to see what settings exist
3. Read database.py to understand the schema
```

**DO:**
```
1. Read ARCHITECTURE.md to understand what the app does
2. Read STATUS.md to see current state and recent changes
3. Read the specific source file you need to MODIFY
```

---

## Documentation Before Code

If documentation is missing or outdated:

1. **Ask the user** if they can provide context
2. **Infer from code** only as a last resort
3. **Document your findings** in the appropriate MD file
4. **Proceed with the task** using the documented understanding

Never assume — always document assumptions and ask for confirmation if critical.
