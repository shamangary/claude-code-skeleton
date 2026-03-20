---
matching:
  paths:
  - plugins/ralph-wiggum/.claude-plugin/plugin.json
  - plugins/ralph-wiggum/README.md
  - plugins/ralph-wiggum/hooks/hooks.json
  - plugins/ralph-wiggum/hooks/stop-hook.sh
  - plugins/ralph-wiggum/scripts/setup-ralph-loop.sh
  - plugins/ralph-wiggum/commands/ralph-loop.md
  - plugins/ralph-wiggum/commands/cancel-ralph.md
  - plugins/ralph-wiggum/commands/help.md
---

# Plugin: `ralph-wiggum`

**Role:** Enables **self-referential iteration**: keep Claude working on the **same task** in a loop until an exit condition is met—"Ralph Wiggum technique." Combines **Stop hook** interception with slash commands to start/cancel/help. The `plugin.json` declares the plugin for Claude Code loader / marketplace.

**Audience:** Agentsmiths debugging long-horizon tasks or enforcing completion.

**Surfaces:** `hooks/hooks.json` wires the `Stop` event to `hooks/stop-hook.sh`, which decides whether to loop or exit. `scripts/setup-ralph-loop.sh` is a one-shot bootstrap helper. Three slash commands — `ralph-loop`, `cancel-ralph`, and `help` — let users start, stop, and understand the loop.

**Stability:** Hook on `Stop` is central—changing behavior affects session exit semantics.
