---
matching:
  paths:
  - .github/ISSUE_TEMPLATE/bug_report.yml
  - .github/ISSUE_TEMPLATE/config.yml
  - .github/ISSUE_TEMPLATE/documentation.yml
  - .github/ISSUE_TEMPLATE/feature_request.yml
  - .github/ISSUE_TEMPLATE/model_behavior.yml
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

# `.github/` (GitHub automation)

**Role:** **GitHub Actions** workflows and **issue templates** for the public Claude Code repository.

**Issue templates** (`ISSUE_TEMPLATE/`): YAML forms for bug reports, feature requests, documentation, model behavior, and a template chooser config—standardize triage fields for the public issue tracker.

**Workflows** (`workflows/`): GitHub Actions for issue/PR automation and scheduled jobs—issue opened dispatch, lifecycle comments, auto-close duplicates, backfill, lock closed issues, remove autoclose label, sweep, non-write user checks, event logging, and Claude-invoking flows for triage and dedupe.

**Note on workflow-macros/:** This skeleton stores workflow MACRO content here (not inside `workflows/`) so a normal GitHub PAT can push without the `workflow` scope. The `matching.paths` above still point at upstream `.yml` files in `.github/workflows/`.

**Audience:** Maintainers, security reviewers of third-party Actions, and issue filers.

**Upstream:** [`../../claude-code/.github/`](../../claude-code/.github/)

**Neighbors:** [`../scripts/MACRO.md`](../scripts/MACRO.md).
