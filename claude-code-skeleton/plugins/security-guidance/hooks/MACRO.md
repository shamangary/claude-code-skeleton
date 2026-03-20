---
matching:
  paths:
  - plugins/security-guidance/hooks/hooks.json
  - plugins/security-guidance/hooks/security_reminder_hook.py
---

# Hooks: `security-guidance`

**Role:** Declares **PreToolUse** hooks for edit-like tools; runs `python3 .../security_reminder_hook.py`.

| Upstream file | Macro meaning |
|---------------|----------------|
| `hooks.json` | Limits matcher to `Edit|Write|MultiEdit`; delegates to Python. |
| `security_reminder_hook.py` | Implements pattern scans and user-visible security reminders. |

**Neighbors:** [Plugin overview](../MACRO.md).
