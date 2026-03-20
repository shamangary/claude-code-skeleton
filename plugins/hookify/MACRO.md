---
matching:
  paths:
  - plugins/hookify/.gitignore
  - plugins/hookify/README.md
---

# Plugin: `hookify`

**Role:** Lets users author **declarative guardrail rules** (in `.local.md`-style files) that compile into runtime behavior across **PreToolUse**, **PostToolUse**, **Stop**, and **UserPromptSubmit**—with slash commands to **create, list, configure, and get help**.

**Audience:** Power users and orgs standardizing “never do X” policies without writing raw hook JSON by hand.

**Architecture (macro):** Python **hook entrypoints** delegate to a **rule engine** (`core/`) that loads config; **matchers** classify tool/prompt events; **utils** shared helpers. A **conversation-analyzer** agent helps distill rules from chat. A **writing-rules** skill teaches syntax.

**Neighbors:** [`.claude-plugin/MACRO.md`](.claude-plugin/MACRO.md); [`hooks/MACRO.md`](hooks/MACRO.md); [`commands/`](commands/), [`agents/`](agents/) (`*.macro.md`); [`skills/writing-rules/MACRO.md`](skills/writing-rules/MACRO.md); [`examples/MACRO.md`](examples/MACRO.md).

**Stability:** Hook event names and timeout fields are contract-sensitive; rule file format evolves with the engine.
