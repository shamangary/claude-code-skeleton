---
matching:
  paths:
  - plugins/commit-commands/.claude-plugin/plugin.json
  - plugins/commit-commands/README.md
  - plugins/commit-commands/commands/commit.md
  - plugins/commit-commands/commands/commit-push-pr.md
  - plugins/commit-commands/commands/clean_gone.md
---

# Plugin: `commit-commands`

**Role:** Shortens **git** workflows via slash commands: commit, push + PR, and **cleanup** helpers. The `plugin.json` declares the plugin for Claude Code loader / marketplace.

**Audience:** Daily developers using Claude Code as a git companion.

**Surfaces:** Three slash commands — `commit` (stage and write a commit message), `commit-push-pr` (commit, push, and open a PR in one flow), and `clean_gone` (delete local branches whose remotes are gone). No agents or skills.

**Stability:** User-facing; renames would break muscle memory—expect additive changes only.
