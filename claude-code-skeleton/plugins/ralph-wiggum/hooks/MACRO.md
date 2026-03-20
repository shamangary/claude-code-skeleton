---
matching:
  paths:
  - plugins/ralph-wiggum/hooks/hooks.json
  - plugins/ralph-wiggum/hooks/stop-hook.sh
---

# Hooks: `ralph-wiggum`

**Role:** `hooks.json` wires the **Stop** event to `stop-hook.sh` so the session can **continue** instead of ending when the loop mode is active.

| Upstream file | Macro meaning |
|---------------|----------------|
| `hooks.json` | Declares Stop → `${CLAUDE_PLUGIN_ROOT}/hooks/stop-hook.sh`. |
| `stop-hook.sh` | Implements continuation / loop policy at stop time. |

**Neighbors:** [Plugin overview](../MACRO.md); [`../commands/`](../commands/) (`*.macro.md`).
