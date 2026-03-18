# Global Cline/Roo Rules

**Centralized rule repository for all projects across all machines**

This repo contains rules that apply globally to all projects in the workspace, eliminating duplication and ensuring consistency.

---

## Repository Structure

```
cline-global-rules/
  README.md                          ← you are here
  .gitignore
  global/                            ← rules that apply to ALL projects
    10-anti-loop.md
    20-plink-ssh.md
    30-context-eviction.md
    40-git-sync.md
    50-api-budget.md
    60-documentation-rules.md
  workspace/                         ← rules specific to the Projects workspace
    10-workspace-index.md
    20-backtest-multiprocessing.md
  src/                               ← shared utilities and tools
    llm/                             ← LLM API gateways
      anthropic_gateway.py           ← Weighted concurrency control for Anthropic API
      README.md                      ← Usage guide
      SETUP.md                       ← Setup instructions
```

---

## How It Works

### At Session Start

Roo/Cline automatically reads these rules via **Custom Instructions** (set in VS Code settings):

1. Read all files in `global/` (10–60 in order)
2. Read `workspace/10-workspace-index.md` to identify projects
3. Read the relevant project's `.clinerules/` files

### Project-Level Rules

Each project has a **thin stub** in its `.clinerules/10-project-rules.md` that:
- Points to this global rules repo
- Contains only project-specific rules (env check, startup sequence, file priority)

---

## Setup on a New Machine

### 1. Clone This Repo

```bash
cd c:/Users/LENOVO/Projects  # or your Projects directory
git clone git@github.com:osokk/cline-global-rules.git
```

### 2. Set Environment Variable: `PLINK_PATH`

The `20-plink-ssh.md` rule requires `%PLINK_PATH%` to be set.

**Windows (PowerShell as Admin):**
```powershell
[System.Environment]::SetEnvironmentVariable('PLINK_PATH', 'C:\path\to\plink.exe', 'User')
```

**Windows (cmd.exe as Admin):**
```cmd
setx PLINK_PATH "C:\path\to\plink.exe"
```

Then restart your terminal/IDE.

### 3. Update VS Code Custom Instructions

Open VS Code Settings (`Ctrl+,`) → search for `roo` → find **Roo: Custom Instructions**

Or edit `settings.json` directly:

```json
"roo-cline.customInstructions": "At the start of EVERY new task, before anything else: read ALL files in c:/Users/LENOVO/Projects/cline-global-rules/global/ (files 10–60 in order), then read workspace/10-workspace-index.md, then read the relevant project .clinerules/. Do NOT skip this."
```

**Important:** Update the path if your Projects directory is in a different location on this machine.

---

## Updating Rules

### To Update a Global Rule

1. Edit the file in `global/` or `workspace/`
2. Commit and push:
   ```bash
   git add -A
   git commit -m "Update [rule name]: [reason]"
   git push
   ```
3. On other machines: `git pull` to get the update

### To Add a New Global Rule

1. Create a new file in `global/` with the next number (e.g., `70-new-rule.md`)
2. Update this README to document it
3. Commit and push

---

## Shared Utilities

### Anthropic API Gateway

The [`src/llm/anthropic_gateway.py`](src/llm/anthropic_gateway.py) module provides a thread-safe gateway for Anthropic API calls with weighted concurrency control.

**Key Features:**
- **Weighted semaphore**: Heavy calls (2 slots) vs Light calls (1 slot)
- **Max 3 concurrent slots**: Prevents token burst limits and 429 errors
- **Global pacing**: 0.8s minimum gap between request starts
- **Smart backoff**: Only retries on actual limit hits (429, overloaded, etc.)
- **2-3x faster than serial**: While maintaining safety

**Quick Start:**
```python
from cline_global_rules.src.llm.anthropic_gateway import gateway

# Heavy call (long context, research, synthesis)
response = gateway.create_message(
    size="heavy",
    model="claude-sonnet-4-20250514",
    messages=messages,
    max_tokens=1400,
)

# Light call (formatting, extraction, small tasks)
response = gateway.create_message(
    size="light",
    model="claude-sonnet-4-20250514",
    messages=messages,
    max_tokens=500,
)
```

**Documentation:**
- [Full Usage Guide](src/llm/README.md) - Detailed examples, tuning, best practices
- [Setup Instructions](src/llm/SETUP.md) - Installation and rollout guide

---

## Why This Exists

**Problem:** Rules were duplicated across 4+ `.clinerules/` locations. When a rule changed (e.g., the plink.exe incident on 2026-03-18), it had to be updated in multiple places, causing drift and confusion.

**Solution:** Centralize global rules in one git-tracked repo that syncs across machines. Project-level `.clinerules/` become thin stubs that reference the global rules.

**Benefits:**
- ✅ Single source of truth for global rules
- ✅ Update once, applies everywhere
- ✅ Git-tracked for cross-machine sync
- ✅ Auto-loaded at session start via Custom Instructions
- ✅ No more "read rules first" prompts needed

---

## Git Remote

- **Remote:** `git@github.com:osokk/cline-global-rules.git`
- **Branch:** `main`

---

## Maintenance

- Review rules quarterly to remove obsolete ones
- Keep rule files focused and single-purpose
- Document the "why" behind each rule (root cause, date added)
- Use clear numbering (10, 20, 30...) to allow insertion of new rules between existing ones

---

## Questions?

If a rule is unclear or seems wrong, check the git history to see when/why it was added, then update it with a commit explaining the change.
