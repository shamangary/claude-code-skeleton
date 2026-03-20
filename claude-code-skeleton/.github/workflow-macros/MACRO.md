---
matching:
  paths:
  - .github/workflows/auto-close-duplicates.yml
  - .github/workflows/backfill-duplicate-comments.yml
  - .github/workflows/claude-dedupe-issues.yml
  - .github/workflows/claude-issue-triage.yml
  - .github/workflows/claude.yml
  - .github/workflows/issue-lifecycle-comment.yml
  - .github/workflows/issue-opened-dispatch.yml
  - .github/workflows/lock-closed-issues.yml
  - .github/workflows/log-issue-events.yml
  - .github/workflows/non-write-users-check.yml
  - .github/workflows/remove-autoclose-label.yml
  - .github/workflows/sweep.yml
---

# `.github/workflows/`

**Skeleton note:** This file lives in **`.github/workflow-macros/`** instead of inside **`.github/workflows/`** so a normal GitHub PAT can push without the **`workflow`** scope (GitHub blocks updates under **`workflows/`**). The **`matching.paths`** above still point at upstream **`.yml`** in **`.github/workflows/`**.

**Role:** **GitHub Actions** for issue/PR automation and scheduled jobs. Typical themes: **issue opened → dispatch**, **lifecycle comments**, **auto-close duplicates**, **backfill**, **lock closed issues**, **remove autoclose label**, **sweep**, **non-write user checks**, **event logging**, and **Claude**-invoking flows for **triage** and **dedupe**.

**Audience:** Repo maintainers; security reviewers of third-party Actions.

**Upstream:** [`../../../claude-code/.github/workflows/`](../../../claude-code/.github/workflows/)

**Neighbors:** [`.github overview`](../MACRO.md); [`../../scripts/MACRO.md`](../../scripts/MACRO.md).
