---
matching:
  paths:
  - plugins/claude-opus-4-5-migration/.claude-plugin/plugin.json
  - plugins/claude-opus-4-5-migration/README.md
  - plugins/claude-opus-4-5-migration/skills/claude-opus-4-5-migration/SKILL.md
  - plugins/claude-opus-4-5-migration/skills/claude-opus-4-5-migration/references/effort.md
  - plugins/claude-opus-4-5-migration/skills/claude-opus-4-5-migration/references/prompt-snippets.md
---

# Plugin: `claude-opus-4-5-migration`

**Role:** Automates **migration** of model identifiers, beta headers, and prompt tweaks when moving from **Sonnet 4.x / Opus 4.1** style configurations to **Opus 4.5**. Contains a single skill that activates when migration work matches its triggers.

**Skill (`skills/claude-opus-4-5-migration/`):** Entry point `SKILL.md` describes when to activate and what to change; `references/` provides supplemental migration tables, edge cases, and version notes for progressive disclosure (effort levels, prompt-snippet examples).

**Audience:** Teams upgrading model usage across code and prompts; model + user pair during upgrade discussions.

**Stability:** Tied to Anthropic model lifecycle; update when model names or migration steps change.
