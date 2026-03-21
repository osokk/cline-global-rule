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
| **crew_v33_git** | ~~(STALE SNAPSHOT — older partial copy)~~ | `crew_v33_git/.clinerules/10-project-rules.md` | 🚫 **FULLY DEPRECATED** — verified 2026-03-20. crew_v33/workspace/ is a strict superset. Do not read, do not modify, do not reference. See `crew_v33_git/DEPRECATED.md`. |
| **quant-data-pipeline** | Binance Futures data ingestion (funding rates + 1m OHLCV) → Backblaze B2 | `quant-data-pipeline/.clinerules/10-project-rules.md` | ✅ Active |

---

## Project Details

### crew_v33 (local working copy)

- **Purpose:** Quant strategy research pipeline, AI agent orchestration, live trading bot management
- **Key docs:** `crew_v33/docs/README_FIRST.md`, `crew_v33/CLINE_WORKFLOW_RULES.md`
- **Live server:** exec-01 (45.32.46.76) — **HIGH RISK, live trading**
- **Git remote:** osokk/crew_v33

### crew_v33_git — 🚫 FULLY DEPRECATED (2026-03-20)

- **Status:** **FULLY DEPRECATED** — verified and closed out during MVP-0 (2026-03-20)
- **Reason:** `crew_v33/workspace/` is a strict superset of `crew_v33_git/workspace/`. All shared files are identical in content. `crew_v33/workspace/` has 16 additional newer files (dated Mar 18–20, 2026) not present in `crew_v33_git/`.
- **Action:** Do NOT read, modify, or reference any files in `crew_v33_git/`. Use `crew_v33/` for all work.
- **See:** `crew_v33_git/DEPRECATED.md` for full deprecation record.

### quant-data-pipeline

- **Purpose:** Binance/Bybit Futures data ingestion (funding rates + 1m OHLCV + OI) → Backblaze B2
- **Key docs:** `quant-data-pipeline/ARCHITECTURE.md`, `quant-data-pipeline/STATUS.md`
- **VPS:** Hetzner (`46.4.188.166`) — **MEDIUM RISK, data server**
  - ⚠️ Migrated from DO `188.166.255.248` (decommissioned 2026-03-20) → Hetzner (2026-03-20)
  - **Pipeline runs on Hetzner ONLY — do NOT run pipeline scripts locally**
  - SSH: use `plink.exe` with hostkey `SHA256:eiTqlFJisIFazlv1kh/vXpJQ2cFrfNADlBJqDBl/t/A`
  - Full SSH notes: `quant-data-pipeline/VPS_SSH_NOTES.md` and `crew_v33/VPS_SSH_NOTES.md`
- **Git remote:** `git@github.com:osokk/quant-data-pipeline.git` (SSH — no PAT needed on VPS)

---

## STEP 0 — Read Global Rules First (NON-NEGOTIABLE)

Before working on ANY project in this workspace:

1. **Read ALL files in `c:/Users/LENOVO/Projects/cline-global-rules/global/`** (files 10–70 in order)
2. **Read this file** (`workspace/10-workspace-index.md`) — you are reading it now
3. **Identify the project** for the current task
4. **Read that project's `.clinerules/` files**

**NEVER work on a project without reading its `.clinerules/` first.**

---

## Cross-Project Rules

### exec-01 Server — READ-ONLY by Default

- **exec-01 (`45.32.46.76`) is READ-ONLY** — no writes, modifications, deletions, or executions unless the user explicitly grants write permission in the current conversation turn
- **NOT subject to auto-approvals** — always pause and ask before any write operation on exec-01
- Override applies only to the single explicitly approved action; reverts to read-only immediately after
- Full rule: `cline-global-rules/global/70-exec01-readonly.md`

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
