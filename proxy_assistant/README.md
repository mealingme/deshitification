# Deshitification Proxy Assistant — local setup

This folder is the planned home for a local Windows browser-automation assistant for Google Flow and Microsoft Clipchamp.

## Current status

No local proxy agent was previously installed according to the project history. The existing Deshitification scheduled workflows are separate ChatGPT tasks and do not control the local Windows browser.

## First step: inventory the existing PC setup

From PowerShell, run:

```powershell
cd C:\Deshitification
git pull
powershell -NoProfile -ExecutionPolicy Bypass -File .\proxy_assistant\inventory_local_agents.ps1
```

Paste the complete output into the Deshitification chat. The script is read-only. It lists relevant source/configuration filenames and checks Python and Playwright availability. It deliberately does not read credentials, browser profiles, environment files, or file contents.

## Intended architecture

- A local Python coordinator running on Windows.
- Playwright for browser automation in a dedicated persistent browser profile.
- A task queue and audit log, with a strict allowlist of permitted sites and actions.
- Explicit approval gates before publishing, uploading, deleting, sending, spending, or changing account settings.
- No passwords, cookies, session tokens, API keys, or personal browser profiles committed to GitHub.
- No public inbound port. Any future ChatGPT-to-PC bridge must use an authenticated, outbound-only design and be reviewed before activation.

## Google Flow and Clipchamp scope

The first useful workflows will be:
1. Open the approved project and locate the supplied script/assets.
2. Prepare prompts, storyboard text, narration text and production assets.
3. Assist with browser-based generation/editing and wait for user-facing confirmation where required.
4. Download and organise generated outputs.
5. Prepare an export checklist and report what succeeded or needs attention.

Browser automation cannot guarantee that Google Flow or Clipchamp controls remain unchanged; selectors and workflows must be tested and maintained. The assistant must stop for MFA, CAPTCHA, unexpected dialogs, permission prompts, or any action outside its allowlist.

## Important limitation

A local Python process does not automatically connect this ChatGPT conversation to the PC. The secure bridge is a separate design and must be implemented only after the local environment has been inventoried.