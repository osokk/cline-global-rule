# GLOBAL RULE — Git Sync Discipline

**MANDATORY — applies to ALL projects**

---

## START of Every Session

**Before any work:**

```bash
git pull
```

This ensures you have the latest changes from other machines or collaborators.

---

## END of Every Session

**After completing work:**

1. Update relevant documentation (STATUS.md, WORKLOG.md, etc.)
2. Stage all changes:
   ```bash
   git add -A
   ```
3. Commit with a descriptive message:
   ```bash
   git commit -m "Descriptive message of what was done"
   ```
4. Push to remote:
   ```bash
   git push
   ```

**Never leave untracked work files uncommitted.**

---

## What NOT to Commit

- `.env` files (contain secrets)
- `__pycache__/` directories
- `.pyc` files
- Large binary files (unless necessary)
- Temporary files

Ensure `.gitignore` is properly configured for each project.

---

## Multi-Machine Workflow

If working across multiple machines (e.g., local dev + VPS):

1. **Local machine:** `git pull` → work → `git add -A` → `git commit` → `git push`
2. **VPS:** `git pull` to get the changes
3. **VPS:** work → `git add -A` → `git commit` → `git push`
4. **Local machine:** `git pull` to get VPS changes

Always pull before starting work on any machine.

---

## Conflict Resolution

If `git pull` reports conflicts:

1. **DO NOT force push** (`git push -f`) unless explicitly instructed
2. Review conflicts with `git status`
3. Resolve conflicts manually in the affected files
4. Stage resolved files: `git add <file>`
5. Complete the merge: `git commit`
6. Push: `git push`

If unsure, report the conflict to the user and await instruction.
