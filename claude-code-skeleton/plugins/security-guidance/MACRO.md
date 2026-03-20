---
matching:
  paths:
  - plugins/security-guidance/.claude-plugin/plugin.json
  - plugins/security-guidance/hooks/hooks.json
  - plugins/security-guidance/hooks/security_reminder_hook.py
---

# Plugin: `security-guidance`

**Role:** **PreToolUse** guardrail: when the model attempts **Edit / Write / MultiEdit**, a Python hook scans for **common unsafe patterns** (injection, XSS, `eval`, dangerous HTML, unsafe deserialization, `os.system`, etc.) and **warns or blocks** accordingly. The `plugin.json` declares the plugin for Claude Code loader / marketplace.

**Audience:** Security-conscious users; default-deny-leaning orgs.

**Surfaces:** `hooks/hooks.json` limits the matcher to `Edit|Write|MultiEdit` and delegates to `hooks/security_reminder_hook.py`, which implements pattern scans and user-visible security reminders. No commands or agents.

**Stability:** Matcher list is security-critical; changes should be reviewed like production security policy.
