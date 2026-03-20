---
matching:
  paths:
  - plugins/README.md
---

# Official plugins (agentic surface)

**Role:** Bundled **plugins** that extend Claude Code with **commands** (user-invoked workflows), **agents** (specialized subagents), **skills** (model-invoked guidance with triggers), and **hooks** (event-driven guards and injections).

**Audience:** Plugin authors, power users, and anyone reasoning about **what the agent is allowed to do** and **when**.

**Composition:** Each subdirectory is one plugin with a `.claude-plugin/plugin.json` manifest (except `plugin-dev` in this checkout, which still ships commands/agents/skills as a toolkit). Together they demonstrate **multi-agent orchestration**, **PR review**, **git workflows**, **session personality**, and **safety hooks**.

**How to read this mirror:** Open a plugin’s **`MACRO.md`**, then drill into `commands/`, `agents/`, `skills/`, or `hooks/` for folder-level stories. Dense reference corpora are summarized in one **`MACRO.md` per folder**, not one file per upstream markdown.

**Official docs:** [Claude Code plugins](https://docs.claude.com/en/docs/claude-code/plugins).

**Plugin index (short):**

| Plugin | Agentic focus |
|--------|----------------|
| `agent-sdk-dev` | Bootstrap + validate **Agent SDK** apps |
| `claude-opus-4-5-migration` | **Skill** for model / header / prompt migration |
| `code-review` | **Multi-phase PR review** with validation and inline comments |
| `commit-commands` | **Git** slash commands (commit / push / PR hygiene) |
| `explanatory-output-style` | **SessionStart** → explanatory tone |
| `feature-dev` | **Feature workflow** + explorer / architect / reviewer agents |
| `frontend-design` | **Skill** for distinctive UI implementation |
| `hookify` | Author **user rules** → dynamic **Pre/PostToolUse**, Stop, UserPromptSubmit hooks |
| `learning-output-style` | **SessionStart** → learning / hands-on mode |
| `plugin-dev` | **Meta** toolkit: create plugins, hooks, MCP, skills, agents |
| `pr-review-toolkit` | **Specialist agents** for PR quality facets |
| `ralph-wiggum` | **Stop** hook + commands for **iterative “loop until done”** |
| `security-guidance` | **PreToolUse** security nudges on edits |
