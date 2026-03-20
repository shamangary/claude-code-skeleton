---
matching:
  paths:
  - plugins/learning-output-style/.claude-plugin/plugin.json
  - plugins/learning-output-style/README.md
  - plugins/learning-output-style/hooks/hooks.json
  - plugins/learning-output-style/hooks-handlers/session-start.sh
---

# Plugin: `learning-output-style`

**Role:** **Interactive learning** mode: at decision points, nudges the **human** to write meaningful small chunks of code while the model teaches—mirrors an unshipped product "Learning" style. The `plugin.json` declares the plugin for Claude Code loader / marketplace.

**Audience:** Learners; workshops.

**Surfaces:** A **SessionStart** hook (`hooks/hooks.json`) registers `SessionStart` → `hooks-handlers/session-start.sh`, which injects learning-mode instructions that set up participatory learning behavior. Structurally identical to `explanatory-output-style`.

**Stability:** Hook contract (`SessionStart`) is stable; learning instruction wording can evolve.
