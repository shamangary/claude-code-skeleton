---
matching:
  paths:
  - plugins/explanatory-output-style/.claude-plugin/plugin.json
  - plugins/explanatory-output-style/README.md
  - plugins/explanatory-output-style/hooks/hooks.json
  - plugins/explanatory-output-style/hooks-handlers/session-start.sh
---

# Plugin: `explanatory-output-style`

**Role:** Shifts session behavior toward **educational explanations**—why choices fit the codebase—similar to a deprecated product "Explanatory" style. The `plugin.json` declares the plugin for Claude Code loader / marketplace.

**Audience:** Learners and teams that want narrated reasoning, not just diffs.

**Surfaces:** A **SessionStart** hook (`hooks/hooks.json`) wires the event to a shell handler (`hooks-handlers/session-start.sh`) that **injects instructions** into the session.

**Stability:** Hook contract (`SessionStart`) is stable; wording of the injected instructions can evolve.
