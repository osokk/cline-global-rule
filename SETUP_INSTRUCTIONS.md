# Setup Instructions — Manual Steps Required

**Status:** Implementation is 95% complete. The following manual steps are needed to finish.

---

## ✅ What's Already Done

- [x] Created `cline-global-rules/` directory with all global rules
- [x] Created `global/` rules (10–60): anti-loop, plink-ssh, context-eviction, git-sync, api-budget, documentation-rules
- [x] Created `workspace/` rules: workspace-index, backtest-multiprocessing
- [x] Created README.md and .gitignore
- [x] Replaced workspace-level `.clinerules/` with stubs
- [x] Replaced project-level `.clinerules/` with stubs (crew_v33, crew_v33_git, quant-data-pipeline)
- [x] `git init` + initial commit in `cline-global-rules/`
- [x] Set git remote to `https://github.com/osokk/cline-global-rules.git`

---

## ⏳ Manual Steps Needed

### 1. Create GitHub Repository

**Action:** Create a new GitHub repository named `cline-global-rules` under the `osokk` account.

**Steps:**
1. Go to https://github.com/new
2. Repository name: `cline-global-rules`
3. Description: "Centralized Cline/Roo rules for all projects"
4. Visibility: Private (recommended) or Public
5. **Do NOT initialize with README, .gitignore, or license** (we already have these)
6. Click "Create repository"

### 2. Push Local Repo to GitHub

**Action:** Push the local `cline-global-rules` repo to the new GitHub remote.

**Commands:**
```bash
cd c:/Users/LENOVO/Projects/cline-global-rules
git push -u origin main
```

If you get authentication errors, you may need to:
- Set up a GitHub Personal Access Token (PAT) for HTTPS
- Or switch to SSH: `git remote set-url origin git@github.com:osokk/cline-global-rules.git`

### 3. Commit Stub Changes in Project Repos

**Action:** Commit the updated `.clinerules/` stubs in each project repo.

**crew_v33_git:**
```bash
cd c:/Users/LENOVO/Projects/crew_v33_git
git add .clinerules/10-project-rules.md
git commit -m "clinerules: replace with stub pointing to cline-global-rules"
git push
```

**quant-data-pipeline:**
```bash
cd c:/Users/LENOVO/Projects/quant-data-pipeline
git add .clinerules/10-project-rules.md
git commit -m "clinerules: replace with stub pointing to cline-global-rules"
git push
```

**crew_v33:** (if it's a git repo)
```bash
cd c:/Users/LENOVO/Projects/crew_v33
git add .clinerules/10-project-rules.md
git commit -m "clinerules: replace with stub pointing to cline-global-rules"
git push
```

### 4. Set Environment Variable: `PLINK_PATH`

**Action:** Set the `PLINK_PATH` environment variable on this machine.

**Windows (PowerShell as Admin):**
```powershell
[System.Environment]::SetEnvironmentVariable('PLINK_PATH', 'C:\Users\LENOVO\Downloads\plink.exe', 'User')
```

**Windows (cmd.exe as Admin):**
```cmd
setx PLINK_PATH "C:\Users\LENOVO\Downloads\plink.exe"
```

Then **restart VS Code** for the change to take effect.

### 5. Add Roo Custom Instructions to VS Code

**Action:** Configure Roo to auto-read global rules at every session start.

**Steps:**
1. Open VS Code Settings (`Ctrl+,`)
2. Search for: `roo`
3. Find: **Roo: Custom Instructions**
4. Add this text:

```
At the start of EVERY new task, before anything else: read ALL files in c:/Users/LENOVO/Projects/cline-global-rules/global/ (files 10–60 in order), then read workspace/10-workspace-index.md, then read the relevant project .clinerules/. Do NOT skip this.
```

**Or edit `settings.json` directly:**

Open Command Palette (`Ctrl+Shift+P`) → "Preferences: Open User Settings (JSON)" → add:

```json
"roo-cline.customInstructions": "At the start of EVERY new task, before anything else: read ALL files in c:/Users/LENOVO/Projects/cline-global-rules/global/ (files 10–60 in order), then read workspace/10-workspace-index.md, then read the relevant project .clinerules/. Do NOT skip this."
```

---

## ✅ Verification

After completing the manual steps, verify the setup:

1. **Test GitHub sync:**
   ```bash
   cd c:/Users/LENOVO/Projects/cline-global-rules
   echo "test" >> README.md
   git add README.md
   git commit -m "test commit"
   git push
   ```
   Then undo: `git reset --hard HEAD~1 && git push -f`

2. **Test Roo Custom Instructions:**
   - Start a new Roo task
   - Check if it automatically reads the global rules without you typing "read rules first"

3. **Test on another machine:**
   - Clone `cline-global-rules` on the other machine
   - Set `PLINK_PATH` env var
   - Update Roo Custom Instructions with the correct path
   - Verify rules are auto-loaded

---

## 🎯 What This Achieves

- ✅ **Single source of truth** for global rules
- ✅ **No more duplication** across 4+ locations
- ✅ **Auto-loaded at session start** via Custom Instructions
- ✅ **Git-tracked** for cross-machine sync
- ✅ **Easy to update** — change once, applies everywhere

---

## 📝 Future Maintenance

- To update a global rule: edit in `cline-global-rules/global/`, commit, push
- To add a new global rule: create `70-new-rule.md`, update README, commit, push
- On other machines: `cd cline-global-rules && git pull` to get updates
- Review rules quarterly to remove obsolete ones

---

## ❓ Questions?

See [`README.md`](README.md) for full documentation.

If a rule is unclear, check git history: `git log --oneline -- global/XX-rule-name.md`
