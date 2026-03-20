---
matching:
  paths:
  - plugins/plugin-dev/skills/plugin-settings/SKILL.md
  - plugins/plugin-dev/skills/plugin-settings/examples/create-settings-command.md
  - plugins/plugin-dev/skills/plugin-settings/examples/example-settings.md
  - plugins/plugin-dev/skills/plugin-settings/examples/read-settings-hook.sh
  - plugins/plugin-dev/skills/plugin-settings/references/parsing-techniques.md
  - plugins/plugin-dev/skills/plugin-settings/references/real-world-examples.md
  - plugins/plugin-dev/skills/plugin-settings/scripts/parse-frontmatter.sh
  - plugins/plugin-dev/skills/plugin-settings/scripts/validate-settings.sh
---

# Skill: `plugin-settings`

**Role:** Patterns for **per-plugin settings** via `.claude/plugin-name.local.md` (frontmatter + body), parsing approaches, and validation scripts.

**Contents:** `SKILL.md` is the entry point covering when to use local markdown settings vs env vars. `references/` provides detailed notes on parsing markdown settings safely and real-world production examples. `examples/` contains sample settings files and command snippets that load them. `scripts/` provides bash helpers to parse frontmatter (`parse-frontmatter.sh`) and validate settings documents (`validate-settings.sh`).
