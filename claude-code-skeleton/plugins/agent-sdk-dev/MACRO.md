---
matching:
  paths:
  - plugins/agent-sdk-dev/.claude-plugin/plugin.json
  - plugins/agent-sdk-dev/README.md
  - plugins/agent-sdk-dev/agents/agent-sdk-verifier-py.md
  - plugins/agent-sdk-dev/agents/agent-sdk-verifier-ts.md
  - plugins/agent-sdk-dev/commands/new-sdk-app.md
---

# Plugin: `agent-sdk-dev`

**Role:** Help developers **scaffold** and **verify** applications built with the **Claude Agent SDK** (TypeScript and Python). Declares plugin identity (`plugin.json`) for Claude Code loader / marketplace discovery.

**Audience:** SDK authors; teams standardizing agent app layout.

**Surfaces:** One slash command (`/agent-sdk-dev:new-sdk-app`) to scaffold a new SDK project, plus two verifier agents — one for TypeScript and one for Python — that validate structure, dependencies, and patterns after scaffolding.

**Stability:** User-facing; command/agent names should stay stable within a major plugin version. The `plugin.json` is the contract surface for installation and discovery.
