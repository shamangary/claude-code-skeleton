# Glossary (agentic Claude Code)

| Term | Meaning here |
|------|----------------|
| **Plugin** | Bundled extension: manifest + optional commands, agents, skills, hooks, MCP. |
| **Command** | User-invoked slash workflow (`commands/*.md`). |
| **Agent** | Specialist prompt template run as a **subagent** with its own tool policy. |
| **Skill** | Model-invoked guidance (`SKILL.md`) with **triggers** and optional `references/`. |
| **Hook** | Event handler (`hooks.json` + executable): reacts at lifecycle points. |
| **`SessionStart`** | Hook event: new session bootstrap (personality injection). |
| **`PreToolUse`** | Hook event: before a tool runs; can block or warn. |
| **`PostToolUse`** | Hook event: after a tool completes. |
| **`Stop`** | Hook event: session stopping; can loop or confirm (see Ralph). |
| **`UserPromptSubmit`** | Hook event: user message submitted. |
| **`CLAUDE_PLUGIN_ROOT`** | Filesystem root of the active plugin (used in hook commands). |
| **MCP** | Model Context Protocol: external tools/servers wired into Claude Code. |
