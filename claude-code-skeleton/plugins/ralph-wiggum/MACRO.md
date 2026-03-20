---
matching:
  paths:
  - plugins/ralph-wiggum/README.md
---

# Plugin: `ralph-wiggum`

**Role:** Enables **self-referential iteration**: keep Claude working on the **same task** in a loop until an exit condition is met—“Ralph Wiggum technique.” Combines **Stop hook** interception with slash commands to start/cancel/help.

**Audience:** Agentsmiths debugging long-horizon tasks or enforcing completion.

**Surfaces:** `Stop` hook (`stop-hook.sh`), helper setup script, and commands (`ralph-loop`, `cancel-ralph`, `help`).

**Neighbors:** [`.claude-plugin/MACRO.md`](.claude-plugin/MACRO.md); [`hooks/MACRO.md`](hooks/MACRO.md); [`commands/`](commands/) (`*.macro.md`); [`scripts/MACRO.md`](scripts/MACRO.md).

**Stability:** Hook on `Stop` is central—changing behavior affects session exit semantics.
