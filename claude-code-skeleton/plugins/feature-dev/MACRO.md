---
matching:
  paths:
  - plugins/feature-dev/README.md
---

# Plugin: `feature-dev`

**Role:** End-to-end **feature development workflow** (`/feature-dev`) with three cooperating **agents**: explore the codebase, propose architecture, and review quality.

**Audience:** Engineers building non-trivial features with Claude Code.

**Surfaces:** One command + three agent prompts + manifest.

**Neighbors:** [`.claude-plugin/MACRO.md`](.claude-plugin/MACRO.md). Per-artifact macros: [`commands/`](commands/), [`agents/`](agents/) (`*.macro.md` pairs with upstream `*.md`).

**Stability:** The **phase structure** of the command is user-visible contract.
