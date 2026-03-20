---
matching:
  paths:
  - plugins/pr-review-toolkit/README.md
---

# Plugin: `pr-review-toolkit`

**Role:** **Composable PR review** via `/pr-review-toolkit:review-pr` with **specialist agents** (comments, tests, silent failures, types, general code review, simplification)—run **all** or a **subset** of “aspects.”

**Audience:** Reviewers who want parallel deep dives without a single monolithic prompt.

**Surfaces:** One command + six agent prompts.

**Neighbors:** [`.claude-plugin/MACRO.md`](.claude-plugin/MACRO.md); [`commands/`](commands/), [`agents/`](agents/) (`*.macro.md`).

**Stability:** Aspect flags and agent names are user-visible.
