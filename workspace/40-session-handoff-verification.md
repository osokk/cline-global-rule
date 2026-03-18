# Rule 40 — Session Handoff Verification

## Purpose
Prevent work loss between sessions by verifying all created/modified files exist on disk before writing the session handoff document.

## When This Rule Applies
- At the end of every session, before writing a SESSION_HANDOFF document
- After any bulk file operations (merges, copies, git operations)

## Required Steps Before Session Handoff

### 1. File Verification
Before writing the handoff document, run a verification check:
```bash
# List all files you created or modified this session
# Verify each one exists on disk with non-zero size
dir /b <filepath>   # Windows
ls -la <filepath>   # Linux
```

Do NOT rely on the VSCode file explorer or environment_details file listing — these can be truncated or stale. Always verify with a direct filesystem command.

### 2. Git Verification
If changes were committed:
```bash
git status              # Should show clean working tree
git log --oneline -3    # Verify your commit is at HEAD
git diff --stat HEAD~1  # Verify expected files are in the commit
```

If changes were pushed:
```bash
git log --oneline origin/main..HEAD  # Should be empty (all pushed)
```

### 3. Handoff Document Requirements
The SESSION_HANDOFF document must include:
- **File verification section** — explicit confirmation that all referenced files were verified on disk
- **Git state** — current branch, HEAD commit hash, push status
- **Data artifacts** — list of any output files (optimization results, logs, etc.) with sizes

### 4. Stuck Operations Check
Before ending a session, verify no operations are stuck:
```bash
git status          # No rebase/merge in progress
git stash list      # Document any stashes
```

## Anti-Pattern: Truncated File Listings
The VSCode workspace file listing in environment_details is often truncated for large projects. NEVER assume a file doesn't exist just because it's not in the truncated listing. Always verify with `dir` or `ls` commands.
