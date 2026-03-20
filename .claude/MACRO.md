---
matching:
  paths: []
---

# `.claude/` (repo root)

**Role:** **Project-scoped** Claude Code configuration for the **claude-code** repository itself—not shipped as a plugin. Currently holds **slash command** definitions used by maintainers.

**Contents:**

| Path | Macro meaning |
|------|----------------|
| `commands/*.md` | Maintainer workflows (issue triage, dedupe, commit/push/PR). Each has a paired **`*.macro.md`** in this skeleton under [`commands/`](commands/). |

**Audience:** Anthropic maintainers and contributors working *in* this repo.

**Upstream:** [`../../claude-code/.claude/`](../../claude-code/.claude/)

**Neighbors:** [`../scripts/MACRO.md`](../scripts/MACRO.md); [`../plugins/MACRO.md`](../plugins/MACRO.md).
