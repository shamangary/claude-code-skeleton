---
matching:
  paths:
  - plugins/plugin-dev/README.md
---

# Plugin: `plugin-dev`

**Role:** **Meta-plugin** for building other plugins: an 8-phase **`/plugin-dev:create-plugin`** workflow, three **agents** (creator, validator, skill reviewer), and **seven skills** covering hooks, MCP, structure, settings, commands, agents, and skills.

**Audience:** Internal and external **plugin authors**.

**Note:** This checkout has **no** `.claude-plugin/plugin.json` folder; the toolkit is still consumed as plugin content by Claude Code when packaged—treat **commands/agents/skills** as the source of truth.

**Neighbors:** [`commands/`](commands/), [`agents/`](agents/) (`*.macro.md` per upstream command/agent); [`skills/MACRO.md`](skills/MACRO.md).

**Stability:** High—many downstream plugins copy these patterns verbatim.
