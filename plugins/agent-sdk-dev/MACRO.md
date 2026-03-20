---
matching:
  paths:
  - plugins/agent-sdk-dev/README.md
---

# Plugin: `agent-sdk-dev`

**Role:** Help developers **scaffold** and **verify** applications built with the **Claude Agent SDK** (TypeScript and Python).

**Audience:** SDK authors; teams standardizing agent app layout.

**Surfaces:** One slash command plus two verifier agents (language-specific).

**Neighbors:** Manifest in [`.claude-plugin/MACRO.md`](.claude-plugin/MACRO.md). Each upstream `*.md` under [`commands/`](commands/) and [`agents/`](agents/) has a matching **`*.macro.md`** (same basename).

**Stability:** User-facing; command/agent names should stay stable within a major plugin version.
