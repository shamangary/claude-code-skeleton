---
matching:
  paths:
  - plugins/plugin-dev/README.md
  - plugins/plugin-dev/agents/agent-creator.md
  - plugins/plugin-dev/agents/plugin-validator.md
  - plugins/plugin-dev/agents/skill-reviewer.md
  - plugins/plugin-dev/commands/create-plugin.md
---

# Plugin: `plugin-dev`

**Role:** **Meta-plugin** for building other plugins: an 8-phase **`/plugin-dev:create-plugin`** workflow, three **agents** (creator, validator, skill reviewer), and **seven skills** covering hooks, MCP, structure, settings, commands, agents, and skills.

**Audience:** Internal and external **plugin authors**.

**Note:** This checkout has no `.claude-plugin/plugin.json` folder; the toolkit is consumed as plugin content by Claude Code when packaged—treat `commands/`, `agents/`, and `skills/` as the source of truth.

**Skills catalog** (`skills/`): Seven sub-skills activate during plugin development questions—each follows **progressive disclosure** with a lean `SKILL.md`, deeper `references/`, optional `examples/` and `scripts/`. See individual skill MACRO.md files for path details.

| Skill | Focus |
|-------|-------|
| `hook-development` | Hooks API, lifecycle events, validation scripts, bash/Python patterns |
| `mcp-integration` | MCP server types, auth, `stdio`/`sse`/`http` examples |
| `plugin-structure` | Directories, `plugin.json`, marketplace readiness, advanced layouts |
| `plugin-settings` | `.claude/plugin-name.local.md` settings patterns and parsing |
| `command-development` | Slash commands, frontmatter, arguments, testing |
| `agent-development` | Authoring agents, prompts, tool policies, validation scripts |
| `skill-development` | Authoring skills, triggers, reference splitting |

**Stability:** High—many downstream plugins copy these patterns verbatim.
