# WORKSPACE INDEX — Multi-Project Workspace

**Location:** `c:/Users/LENOVO/Projects`

This workspace contains multiple projects. Before reading ANY project files or running ANY commands:

1. **Identify which project the task is for**
2. **Read that project's `.clinerules/` directory FIRST**

---

## Projects in This Workspace

| Project | Description | Clinerules Path | Status |
|---------|-------------|----------------|--------|
| **crew_v33** | Quant strategy research pipeline, AI agent orchestration, live trading bot management | `crew_v33/.clinerules/10-project-rules.md` | ✅ **CANONICAL** — git remote: osokk/crew_v33, branch: main |
| **crew_v33_git** | (STALE SNAPSHOT — older partial copy) | `crew_v33_git/.clinerules/10-project-rules.md` | ⚠️ **DO NOT USE** — stale copy, use crew_v33 instead |
| **quant-data-pipeline** | Binance Futures data ingestion (funding rates + 1m OHLCV) → Backblaze B2 | `quant-data-pipeline/.clinerules/10-project-rules.md` | ✅ Active |

---

## Project Details

### crew_v33 (local working copy)

- **Purpose:** Quant strategy research pipeline, AI agent orchestration, live trading bot management
- **Key docs:** `crew_v33/docs/README_FIRST.md`, `crew_v33/CLINE_WORKFLOW_RULES.md`
- **Live server:** exec-01 (45.32.46.76) — **HIGH RISK, live trading**
- **Git remote:** osokk/crew_v33

### crew_v33_git (git-tracked canonical copy)

- **Purpose:** Same as crew_v33 — this WAS the canonical version with more workspace files
- **Status:** ⚠️ **STALE SNAPSHOT** — older partial copy, do not use for new work
- **Key docs:** `crew_v33_git/docs/README_FIRST.md`, `crew_v33_git/CLINE_WORKFLOW_RULES.md`
- **Action:** If asked to work on crew_v33, use `crew_v33/` NOT `crew_v33_git/`

### quant-data-pipeline

- **Purpose:** Binance Futures data ingestion (funding rates + 1m OHLCV) → Backblaze B2
- **Key docs:** `quant-data-pipeline/ARCHITECTURE.md`, `quant-data-pipeline/STATUS.md`
- **VPS:** quant-ingestion (188.166.255.248) — **MEDIUM RISK, data server**
- **Git remote:** (check project for remote URL)

---

## STEP 0 — Read Global Rules First (NON-NEGOTIABLE)

Before working on ANY project in this workspace:

1. **Read ALL files in `c:/Users/LENOVO/Projects/cline-global-rules/global/`** (files 10–60 in order)
2. **Read this file** (`workspace/10-workspace-index.md`) — you are reading it now
3. **Identify the project** for the current task
4. **Read that project's `.clinerules/` files**

**NEVER work on a project without reading its `.clinerules/` first.**

---

## Cross-Project Rules

### SSH / VPS Access

- **NEVER use `ssh` on Windows** — it hangs indefinitely
- **ALWAYS use `plink.exe`:** Use `%PLINK_PATH%` environment variable
- Full credentials in each project's `VPS_SSH_NOTES.md` (read before any SSH work)

### Anti-Loop Safeguard

- Same command or file check more than 2 times with no change → STOP immediately
- Report: "Stuck in polling loop checking [X]. Stopping."

### Context Eviction Hard Stop

- If `read_file` returns `[NOTE] This file read has been removed to save space` → DO NOT re-read
- Work with what is in memory or call `attempt_completion` to end the session

### API Budget

- Default task budget: $10 USD
- At $10 estimated spend: STOP and ask user to approve another $10

### Git Discipline

- `git pull` before starting any work on any project
- Session end: `git add -A` → commit → push
- Never commit `.env` files
