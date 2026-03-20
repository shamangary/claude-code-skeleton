---
matching:
  paths:
  - plugins/pr-review-toolkit/.claude-plugin/plugin.json
  - plugins/pr-review-toolkit/README.md
  - plugins/pr-review-toolkit/agents/comment-analyzer.md
  - plugins/pr-review-toolkit/agents/pr-test-analyzer.md
  - plugins/pr-review-toolkit/agents/silent-failure-hunter.md
  - plugins/pr-review-toolkit/agents/type-design-analyzer.md
  - plugins/pr-review-toolkit/agents/code-reviewer.md
  - plugins/pr-review-toolkit/agents/code-simplifier.md
  - plugins/pr-review-toolkit/commands/review-pr.md
---

# Plugin: `pr-review-toolkit`

**Role:** **Composable PR review** via `/pr-review-toolkit:review-pr` with **specialist agents** (comments, tests, silent failures, types, general code review, simplification)—run **all** or a **subset** of "aspects." The `plugin.json` declares the plugin for Claude Code loader / marketplace.

**Audience:** Reviewers who want parallel deep dives without a single monolithic prompt.

**Surfaces:** One slash command (`/pr-review-toolkit:review-pr`) that fans out to six specialist agents — comment analysis, test coverage, silent failure detection, type design, general code review, and simplification. Run all aspects or pick a subset.

**Stability:** Aspect flags and agent names are user-visible.
