---
matching:
  paths:
    - .claude/commands/dedupe.md
    - .claude/commands/commit-push-pr.md
    - .claude/commands/triage-issue.md
---

# `.claude/` (repo root)

**Role:** **Project-scoped** Claude Code configuration for the **claude-code** repository itself—not shipped as a plugin. Currently holds **slash command** definitions used by maintainers.

**Contents:**

| Path | Macro meaning |
|------|----------------|
| `commands/*.md` | Maintainer workflows: `triage-issue` (label + prioritise), `dedupe` (find and close duplicate issues), `commit-push-pr` (commit, push, open PR). |

**Audience:** Anthropic maintainers and contributors working *in* this repo.

**Upstream:** [`../../claude-code/.claude/`](../../claude-code/.claude/)

**Neighbors:** [`../scripts/MACRO.md`](../scripts/MACRO.md); [`../plugins/MACRO.md`](../plugins/MACRO.md).
