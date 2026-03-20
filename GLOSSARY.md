# Glossary (agentic Claude Code)

## Extension layer — open in `claude-code/` GitHub repo

| Term | Meaning here |
|------|----------------|
| **Plugin** | Bundled extension: manifest + optional commands, agents, skills, hooks, MCP. |
| **Command** | User-invoked slash workflow (`commands/*.md`). |
| **Agent** | Specialist prompt template run as a **subagent** with its own tool policy and fresh context. |
| **Skill** | Model-invoked guidance (`SKILL.md`) with **triggers** and optional `references/`. Loads on demand — only the description is in context until triggered. |
| **Hook** | Event handler (`hooks.json` + executable): reacts at lifecycle points. |
| **`SessionStart`** | Hook event: new session bootstrap (personality injection). Cannot block. |
| **`PreToolUse`** | Hook event: before a tool runs; can block or warn. |
| **`PostToolUse`** | Hook event: after a tool completes. Cannot block. |
| **`Stop`** | Hook event: session stopping; can block to re-loop (ralph-wiggum pattern). |
| **`UserPromptSubmit`** | Hook event: user message submitted; can modify or block. |
| **`CLAUDE_PLUGIN_ROOT`** | Filesystem root of the active plugin (used in hook commands). |
| **MCP** | Model Context Protocol: external tools/servers wired into Claude Code. Each MCP server adds tool definitions to every request — check cost with `/mcp`. |
| **CLAUDE.md** | Markdown file loaded every session. Survives context compaction. Canonical place for project invariants, conventions, and compact instructions. |

## Core runtime — closed (obfuscated npm bundle or server-side)

> Official reference: [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)

| Term | What it does | Where |
|------|--------------|-------|
| **Agent loop** | Three-phase cycle: gather context → take action → verify results. Repeats until done or interrupted. | Minified `@anthropic-ai/claude-code` npm bundle. |
| **Context compression** | Clears older tool outputs first, then summarises if needed. Preserves recent requests and key code; early detailed instructions may be lost. | npm bundle. |
| **Permission enforcement** | Evaluates `settings.json` allow/deny rules at tool invocation time. Three modes: Default, Auto-accept edits, Plan mode (read-only). | npm bundle. |
| **Checkpoints** | Snapshots file contents before every edit. Press Esc×2 to rewind. Local to session; does not cover remote side effects. | npm bundle. |
| **Tool dispatch** | Routes tool calls, sandboxes execution, collects results. | npm bundle. |
| **Model inference** | Token generation, sampling, tool-call parsing. | Server-side (Anthropic API). |

> Hook events (`PreToolUse`, `Stop`, …) are **surface hooks into the closed agent loop** — you control the boundary logic (allow/block/warn) but not the loop internals. Prompts, manifests, and hook scripts in `claude-code/` are readable; the engine that runs them is not.
