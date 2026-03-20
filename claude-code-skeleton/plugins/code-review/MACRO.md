---
matching:
  paths:
  - plugins/code-review/.claude-plugin/plugin.json
  - plugins/code-review/README.md
  - plugins/code-review/commands/code-review.md
---

# Plugin: `code-review`

**Role:** **Automated pull-request review** that orchestrates **multiple subagents** (Haiku gates, Sonnet reviewers, Opus bug finders), **validates** suspected issues to cut false positives, and optionally posts **inline GitHub comments** via MCP. The `plugin.json` declares the plugin for Claude Code loader / marketplace.

**Audience:** Maintainers and reviewers wanting a high-signal PR pass.

**Surfaces:** Primarily the `/code-review` command (agents are embedded in the command flow as instructions, not separate `.md` agent files).

**Flow (macro):** (1) Skip closed/draft/no-review PRs and duplicate Claude comments. (2) Collect relevant `CLAUDE.md` paths. (3) Summarize PR. (4) Parallel review passes (CLAUDE compliance + bug hunts). (5) Validate each flagged issue. (6) Summarize; optionally comment.

**Stability:** Behavior depends on `gh`, `CLAUDE.md` conventions, and optional MCP inline-comment tool availability.
