---
matching:
  paths:
  - plugins/explanatory-output-style/hooks/hooks.json
---

# Hooks config: `explanatory-output-style`

**Role:** `hooks.json` wires **SessionStart** → shell command under `${CLAUDE_PLUGIN_ROOT}/hooks-handlers/`.

**Events:** `SessionStart` only.

**Audience:** Claude Code hook runtime.

**Neighbors:** [Handlers folder](../hooks-handlers/MACRO.md); [plugin overview](../MACRO.md).
