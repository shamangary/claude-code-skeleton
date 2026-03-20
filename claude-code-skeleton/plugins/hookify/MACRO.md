---
matching:
  paths:
  - plugins/hookify/.claude-plugin/plugin.json
  - plugins/hookify/.gitignore
  - plugins/hookify/README.md
  - plugins/hookify/core/__init__.py
  - plugins/hookify/core/config_loader.py
  - plugins/hookify/core/rule_engine.py
  - plugins/hookify/examples/console-log-warning.local.md
  - plugins/hookify/examples/dangerous-rm.local.md
  - plugins/hookify/examples/require-tests-stop.local.md
  - plugins/hookify/examples/sensitive-files-warning.local.md
  - plugins/hookify/hooks/__init__.py
  - plugins/hookify/hooks/hooks.json
  - plugins/hookify/hooks/posttooluse.py
  - plugins/hookify/hooks/pretooluse.py
  - plugins/hookify/hooks/stop.py
  - plugins/hookify/hooks/userpromptsubmit.py
  - plugins/hookify/matchers/__init__.py
  - plugins/hookify/skills/writing-rules/SKILL.md
  - plugins/hookify/utils/__init__.py
  - plugins/hookify/agents/conversation-analyzer.md
  - plugins/hookify/commands/hookify.md
  - plugins/hookify/commands/list.md
  - plugins/hookify/commands/configure.md
  - plugins/hookify/commands/help.md
---

# Plugin: `hookify`

**Role:** Lets users author **declarative guardrail rules** (in `.local.md`-style files) that compile into runtime behavior across **PreToolUse**, **PostToolUse**, **Stop**, and **UserPromptSubmit**—with slash commands to **create, list, configure, and get help**. The `plugin.json` declares the plugin for Claude Code loader / marketplace.

**Audience:** Power users and orgs standardizing "never do X" policies without writing raw hook JSON by hand.

**Architecture:** Python **hook entrypoints** (`hooks/`) register four events and delegate to a **rule engine** (`core/`) that loads config via `config_loader.py` and evaluates rules against hook payloads. **Matchers** (`matchers/`) classify tool/prompt events so rules can target specific situations (e.g. destructive commands, sensitive paths). **Utils** (`utils/`) provides shared Python helpers imported by the hook scripts.

**Examples** (`examples/`): Sample `*.local.md` rule files serving as a cookbook—warn on `console.log`, block dangerous `rm`, require tests before stopping, guard sensitive files.

**Skill (`skills/writing-rules/`):** Teaches authors how to write Hookify-compatible rule documents and think in terms of matchers + outcomes. A conversation-analyzer agent also helps distill rules from chat history.

**Stability:** Hook event names and timeout fields are contract-sensitive; rule file format evolves with the engine.
