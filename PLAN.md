# PLAN: Macro workspace (`claude-code` + `claude-code-skeleton`)

## Purpose

This **workspace** holds:

| Folder | Role |
|--------|------|
| **`claude-code/`** | Upstream **Anthropic** repo — default: **auto-updated** via `git pull` / shallow **clone** when you run [`matching/generate_matching.py`](matching/generate_matching.py). |
| **`claude-code-skeleton/`** | **Macro layer only** — mirrors structure with **`MACRO.md`** (YAML `matching.paths`) and **`*.macro.md`** next to commands/agents. |
| **`matching/`** | **Tooling** — generator + `requirements.txt` (does **not** mirror upstream; avoids confusion with `claude-code/scripts/`). |
| **`MATCHING.md`** (root) | **Generated** report — skeleton ↔ upstream map, **summary stats**, ignored-path policy, **validation failures**, optional **uncovered** upstream files. |

Do **not** hand-edit **`MATCHING.md`**; change **`MACRO.md`** YAML or `*.macro.md`, then regenerate.

---

## Frontmatter (mandatory on every `MACRO.md`)

```yaml
---
matching:
  paths:
    - README.md
    - plugins/foo/bar.py
---
```

| Rule | Detail |
|------|--------|
| `matching.paths` | Paths **relative to `claude-code/`**. Use `[]` for index-only macros. |
| No prompt overlap | Do **not** list `**/commands/*.md` or `**/agents/*.md` — only **`*.macro.md`** (1:1). |
| Uniqueness | Same path must not appear in two `MACRO.md` files. |

**Bootstrap `paths` after large upstream moves:**

```bash
python3 -m pip install -r matching/requirements.txt
python3 matching/generate_matching.py --seed --no-fetch
python3 matching/generate_matching.py --no-fetch
```

(`--no-fetch` if you are not cloning/updating yet.)

---

## Regenerate `MATCHING.md` (typical)

From **this workspace root** (folder that contains `claude-code/`, `claude-code-skeleton/`, `matching/`):

```bash
python3 -m pip install -r matching/requirements.txt
python3 matching/generate_matching.py
```

By **default** this will **`git fetch` / `git pull --ff-only`** inside **`claude-code/`** (or **shallow clone** if the directory is missing). Use **`--no-fetch`** to skip network/git.

Options: `--remote URL`, `--branch NAME`, `--seed` (rewrites all `matching.paths` heuristically — review diff).

---

## `claude-code-skeleton/` layout (no generator under `scripts/`)

`skeleton/scripts/MACRO.md` documents **only** upstream **`claude-code/scripts/`** (GitHub automation). The matcher lives at **`matching/generate_matching.py`**.

---

## Phases

- **Phase 4 — upstream change:** edit skeleton; run `python3 matching/generate_matching.py`.
- **Quality:** Regenerate after every macro or upstream path change.

---

## Immediate next action

```bash
python3 matching/generate_matching.py
```

Inspect **`MATCHING.md` → Report summary** and **Validation issues**.
