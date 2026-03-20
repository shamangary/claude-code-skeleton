# Glossary (agentic Claude Code)

## Extension layer — open in `claude-code/` GitHub repo

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

## Core runtime — closed (obfuscated npm bundle or server-side)

| Term | What it does | Where |
|------|--------------|-------|
| **Agent loop** | Decides which tool to call next, manages reasoning and stop conditions. | Minified `@anthropic-ai/claude-code` npm bundle. |
| **Context compression** | Summarises conversation history when approaching context limits. | npm bundle. |
| **Permission enforcement** | Evaluates `settings.json` allow/deny rules at tool invocation time. | npm bundle. |
| **Tool dispatch** | Routes tool calls, sandboxes execution, collects results. | npm bundle. |
| **Model inference** | Token generation, sampling, tool-call parsing. | Server-side (Anthropic API). |

> Hook events (`PreToolUse`, `Stop`, …) are **surface hooks into the closed agent loop** — you control the boundary logic (allow/block/warn) but not the loop internals. Prompts, manifests, and hook scripts in `claude-code/` are readable; the engine that runs them is not.
