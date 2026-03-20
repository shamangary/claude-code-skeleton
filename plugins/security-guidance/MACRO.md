---
matching:
  paths: []
---

# Plugin: `security-guidance`

**Role:** **PreToolUse** guardrail: when the model attempts **Edit / Write / MultiEdit**, a Python hook scans for **common unsafe patterns** (injection, XSS, `eval`, dangerous HTML, unsafe deserialization, `os.system`, etc.) and **warns or blocks** accordingly.

**Audience:** Security-conscious users; default-deny-leaning orgs.

**Surfaces:** `hooks.json` + `security_reminder_hook.py` only (no commands/agents).

**Neighbors:** [`.claude-plugin/MACRO.md`](.claude-plugin/MACRO.md); [`hooks/MACRO.md`](hooks/MACRO.md).

**Stability:** Matcher list is security-critical; changes should be reviewed like production security policy.
