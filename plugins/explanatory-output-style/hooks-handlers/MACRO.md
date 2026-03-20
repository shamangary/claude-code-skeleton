---
matching:
  paths:
  - plugins/explanatory-output-style/hooks-handlers/session-start.sh
---

# Hook handlers: `explanatory-output-style`

**Role:** Executable **session bootstrap** that adds “explanatory mode” guidance to the model context.

| Upstream file | Macro meaning |
|---------------|----------------|
| `session-start.sh` | Runs on SessionStart; emits or loads the explanatory instructions payload for the session. |

**Neighbors:** [`../hooks/MACRO.md`](../hooks/MACRO.md).
