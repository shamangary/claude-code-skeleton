---
matching:
  paths:
  - scripts/auto-close-duplicates.ts
  - scripts/backfill-duplicate-comments.ts
  - scripts/comment-on-duplicates.sh
  - scripts/edit-issue-labels.sh
  - scripts/gh.sh
  - scripts/issue-lifecycle.ts
  - scripts/lifecycle-comment.ts
  - scripts/sweep.ts
---

# `scripts/` (upstream GitHub automation)

**Role:** TypeScript and shell utilities under **`claude-code/scripts/`** for **maintaining the Claude Code GitHub repo** (issues, labels, duplicates, sweeps). **Not** the agentic plugin runtime — and **not** where the matcher script lives.

**Audience:** Upstream maintainers.

**File-level map:** **[`../../MATCHING.md`](../../MATCHING.md)** → section `scripts/MACRO.md` (1:many).

**Upstream tree:** [`../../claude-code/scripts/`](../../claude-code/scripts/).

**Matcher tooling** (this workspace only): [`../../matching/generate_matching.py`](../../matching/generate_matching.py) at workspace root — **not** under this folder.
