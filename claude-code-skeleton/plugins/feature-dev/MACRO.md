---
matching:
  paths:
  - plugins/feature-dev/.claude-plugin/plugin.json
  - plugins/feature-dev/README.md
  - plugins/feature-dev/agents/code-explorer.md
  - plugins/feature-dev/agents/code-architect.md
  - plugins/feature-dev/agents/code-reviewer.md
  - plugins/feature-dev/commands/feature-dev.md
---

# Plugin: `feature-dev`

**Role:** End-to-end **feature development workflow** (`/feature-dev`) with three cooperating **agents**: explore the codebase, propose architecture, and review quality. The `plugin.json` declares the plugin for Claude Code loader / marketplace.

**Audience:** Engineers building non-trivial features with Claude Code.

**Surfaces:** One slash command (`/feature-dev`) that orchestrates three agents — `code-explorer` surveys the codebase, `code-architect` proposes a plan, and `code-reviewer` validates the result. The `plugin.json` registers the plugin for the marketplace.

**Stability:** The phase structure of the command is user-visible contract.
