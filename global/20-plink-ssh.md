# GLOBAL RULE — SSH / plink.exe (Windows)

**ABSOLUTE HARD STOP — applies to ALL projects**

**INTERNALIZE THIS RULE IMMEDIATELY.**

---

## The Problem

On Windows, the built-in `ssh` command requires interactive password entry. It will **hang indefinitely** waiting for a password that can never be provided non-interactively. This caused 8 terminals to hang simultaneously in a single session (2026-03-18), blocking all progress.

---

## The Rule

**NEVER use `ssh` to connect to any VPS.** Always use `plink.exe`.

---

## Detection — Before ANY Remote Command

> "Am I about to run `ssh ...`? If YES — STOP. Use plink.exe instead."

---

## plink.exe Path

Use the environment variable `%PLINK_PATH%` which should be set on each machine.

**Example for quant-ingestion VPS (188.166.255.248):**

```cmd
"%PLINK_PATH%" -ssh -pw d41b0c2c975a62a405f3c68715 -hostkey "ssh-ed25519 255 SHA256:gOejGPcxgH+KwtA4EA49YwZmVOnom3Xuk6rGcz9Bs+U" root@188.166.255.248 "COMMAND HERE" 2>&1
```

**If `%PLINK_PATH%` is not set:** Report to user: "Environment variable PLINK_PATH is not set. Please set it to the full path of plink.exe on this machine."

Full credentials and templates for all VPS servers are in each project's **VPS_SSH_NOTES.md** — read it before any SSH work.

---

## If a Terminal Hangs (No Output, No Exit Code)

1. **Do NOT open another terminal to retry the same `ssh` command** — it will also hang
2. **Do NOT run more than 1 retry** — if the first plink.exe attempt hangs, stop and report
3. Report to user: "Terminal [N] is hanging. Likely used `ssh` instead of `plink.exe`. Please kill the terminal manually."
4. Switch to plink.exe for all subsequent attempts

---

## Counting Rule

- If you have **2 or more terminals actively hanging** on SSH commands → **HARD STOP**
- Do not open any more terminals
- Report the situation to the user and await instruction

---

## Setup on New Machine

Set the `PLINK_PATH` environment variable:

**Windows (PowerShell as Admin):**
```powershell
[System.Environment]::SetEnvironmentVariable('PLINK_PATH', 'C:\path\to\plink.exe', 'User')
```

**Windows (cmd.exe as Admin):**
```cmd
setx PLINK_PATH "C:\path\to\plink.exe"
```

Then restart your terminal/IDE for the change to take effect.
