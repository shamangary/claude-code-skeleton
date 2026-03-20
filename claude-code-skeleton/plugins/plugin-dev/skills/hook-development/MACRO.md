---
matching:
  paths:
  - plugins/plugin-dev/skills/hook-development/SKILL.md
  - plugins/plugin-dev/skills/hook-development/examples/load-context.sh
  - plugins/plugin-dev/skills/hook-development/examples/validate-bash.sh
  - plugins/plugin-dev/skills/hook-development/examples/validate-write.sh
  - plugins/plugin-dev/skills/hook-development/references/advanced.md
  - plugins/plugin-dev/skills/hook-development/references/migration.md
  - plugins/plugin-dev/skills/hook-development/references/patterns.md
  - plugins/plugin-dev/skills/hook-development/scripts/README.md
  - plugins/plugin-dev/skills/hook-development/scripts/hook-linter.sh
  - plugins/plugin-dev/skills/hook-development/scripts/test-hook.sh
  - plugins/plugin-dev/skills/hook-development/scripts/validate-hook-schema.sh
---

# Skill: `hook-development`

**Role:** Teaches **event-driven hooks** in Claude Code: when to use `PreToolUse`, schema expectations, bash vs Python, migration from older hook styles, and validation tooling.

**Contents:** `SKILL.md` is the entry point covering triggers and essential patterns. `references/` provides deep documentation on hook patterns, migrations, and advanced topics. `examples/` contains copy-paste hook shells demonstrating validation, context loading, and guard patterns. `scripts/` provides maintainer-facing bash utilities to lint, validate JSON schema, and exercise hooks locally (`hook-linter.sh`, `validate-hook-schema.sh`, `test-hook.sh`).
