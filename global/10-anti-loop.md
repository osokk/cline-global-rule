# GLOBAL RULE — Anti-Loop Safeguard

**NON-NEGOTIABLE — applies to ALL projects**

---

## The Rule

If you find yourself running the **same command** or checking the **same file/directory** more than **2 times in a row** with no change in output:

1. **STOP immediately** — do not run it a third time
2. Report to the user: "I'm stuck in a polling loop checking [X]. Output unchanged after 2 checks. Stopping."
3. Suggest alternatives (check a different path, read a log file, report what you know)
4. **NEVER poll for background process completion more than 2 times** — if still running after 2 checks, report status and ask the user what to do

**This applies to:** `dir`, `ls`, file existence checks, retrying failed commands, any repeated identical tool call.

---

## Self-Check Before Any Repeated Command

> "Have I run this exact command before and gotten the same result? If yes — STOP and report."

---

## Root Cause (2026-03-16)

Cline ran `dir strategies\funding_rate\data\` 20+ times waiting for a file that was writing to a different path. The file existed in `data/` (project root) while Cline was checking `strategies/funding_rate/data/`. This wasted significant context and confused the user.

---

## Why This Matters

- Wastes context window tokens
- Confuses the user
- Indicates a logic error (wrong path, wrong assumption)
- Can burn through API budget with no progress
