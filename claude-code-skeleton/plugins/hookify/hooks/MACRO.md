---
matching:
  paths:
  - plugins/hookify/hooks/__init__.py
  - plugins/hookify/hooks/hooks.json
  - plugins/hookify/hooks/posttooluse.py
  - plugins/hookify/hooks/pretooluse.py
  - plugins/hookify/hooks/stop.py
  - plugins/hookify/hooks/userpromptsubmit.py
---

# Hooks: `hookify`

**Role:** `hooks.json` registers **four hook events**, each backed by a **Python** command with bounded timeouts.

| Event | Upstream module | Macro meaning |
|-------|-----------------|---------------|
| `PreToolUse` | `pretooluse.py` | Inspect / block / warn **before** tool execution. |
| `PostToolUse` | `posttooluse.py` | React **after** tools run (logging, remediation prompts). |
| `Stop` | `stop.py` | Intercept session stop / exit attempts (e.g. “are you sure?” flows). |
| `UserPromptSubmit` | `userpromptsubmit.py` | Observe or reshape user prompts on submit. |

**Config:**Matcher behavior and rule sources are driven by Hookify’s engine + user rule files (see [`../core/MACRO.md`](../core/MACRO.md)).

**Neighbors:** [Plugin overview](../MACRO.md).
