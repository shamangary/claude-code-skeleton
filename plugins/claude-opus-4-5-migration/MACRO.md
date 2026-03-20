---
matching:
  paths:
  - plugins/claude-opus-4-5-migration/README.md
---

# Plugin: `claude-opus-4-5-migration`

**Role:** Automates **migration** of model identifiers, beta headers, and prompt tweaks when moving from **Sonnet 4.x / Opus 4.1** style configurations to **Opus 4.5**.

**Audience:** Teams upgrading model usage across code and prompts.

**Surfaces:** A single **skill** (invoked when migration work matches its triggers).

**Neighbors:** Manifest [`.claude-plugin/MACRO.md`](.claude-plugin/MACRO.md); skills index [`skills/MACRO.md`](skills/MACRO.md); bundle [`skills/claude-opus-4-5-migration/MACRO.md`](skills/claude-opus-4-5-migration/MACRO.md).

**Stability:** Tied to Anthropic model lifecycle; update when model names or migration steps change.
