---
matching:
  paths:
  - plugins/explanatory-output-style/README.md
---

# Plugin: `explanatory-output-style`

**Role:** Shifts session behavior toward **educational explanations**—why choices fit the codebase—similar to a deprecated product “Explanatory” style.

**Audience:** Learners and teams that want narrated reasoning, not just diffs.

**Surfaces:** **SessionStart** hook runs a shell handler that **injects instructions** into the session.

**Neighbors:** [`.claude-plugin/MACRO.md`](.claude-plugin/MACRO.md); [`hooks/MACRO.md`](hooks/MACRO.md); [`hooks-handlers/MACRO.md`](hooks-handlers/MACRO.md).

**Stability:** Hook contract (`SessionStart`) is stable; wording can evolve.
