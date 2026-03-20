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

# `scripts/` (dual meaning in this repo)

## Upstream — `../claude-code/scripts/`

**Role:** TypeScript and shell utilities for **maintaining the Claude Code GitHub repo** (issues, labels, duplicates, sweeps). **Not** the agentic plugin runtime.

**Audience:** Upstream maintainers only.

**File-level mapping:** See **[`../MATCHING.md`](../MATCHING.md)** (look for `scripts/MACRO.md` in §1:many).

**Upstream tree:** [`../../claude-code/scripts/`](../../claude-code/scripts/).

---

## Skeleton-only — `generate_matching.py`

**Role:** Reads **`matching:`** YAML in every **`MACRO.md`**, validates paths, and writes **[`../MATCHING.md`](../MATCHING.md)** (do not edit **`MATCHING.md`** by hand).

**Dependencies:**

```bash
python3 -m pip install -r claude-code-skeleton/scripts/requirements-matching.txt
```

**Run** (parent folder must contain **both** `claude-code-skeleton/` and `claude-code/`):

```bash
python3 claude-code-skeleton/scripts/generate_matching.py
```

**Refresh `matching.paths` heuristically** (overwrites YAML lists; keep a git diff to review):

```bash
python3 claude-code-skeleton/scripts/generate_matching.py --seed
python3 claude-code-skeleton/scripts/generate_matching.py
```
