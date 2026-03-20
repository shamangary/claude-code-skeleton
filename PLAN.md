# PLAN: Macro natural language map of Claude Code

## Purpose

Build a **parallel documentation layer** for the [`../claude-code/`](../claude-code/) tree:

- **`MACRO.md`** — skill-style **YAML frontmatter** + prose (see § [Frontmatter & matching](#frontmatter--matching-mandatory)).
- **`*.macro.md`** — paired with upstream **`*.md`** under **`commands/`** and **`agents/`** (same basename; no rollup `MACRO.md` in those folders).
- **`MATCHING.md`** — **generated only** by [`scripts/generate_matching.py`](scripts/generate_matching.py); do not hand-edit except by changing source `MACRO.md` files and re-running the script.

**This repo (`claude-code-skeleton`)** holds the macro layer and this plan, **not** a fork of implementation source.

---

## Frontmatter & matching (mandatory)

Every **`MACRO.md`** must begin with a YAML block (same fenced style as Agent **Skills**):

```yaml
---
matching:
  paths:
    - README.md
    - plugins/foo/bar.py
---
```

Rules enforced by **`generate_matching.py`**:

| Rule | Detail |
|------|--------|
| `matching.paths` | **Required.** List of paths **relative to `claude-code/`** root. Use `[]` if this macro owns no files in §1:many (e.g. index-only folders). |
| No prompt overlap | Do **not** list `**/commands/*.md` or `**/agents/*.md`; those are **1:1** via **`*.macro.md`** only. |
| Uniqueness | The same upstream path must **not** appear in two `MACRO.md` files (generator errors on collision). |
| Existence | Every listed path must **exist** in the upstream repo (or the generator fails). |

**Bootstrap path lists** (first time or large upstream moves):

```bash
python3 -m pip install -r claude-code-skeleton/scripts/requirements-matching.txt
python3 claude-code-skeleton/scripts/generate_matching.py --seed   # writes/overwrites matching.paths from a directory heuristic
python3 claude-code-skeleton/scripts/generate_matching.py          # writes MATCHING.md from YAML
```

After `--seed`, **review and edit** `matching.paths` by hand where the heuristic is wrong, then run without `--seed`.

---

## Main codebase (source of truth)

| Location | What it is |
|----------|------------|
| **[`../claude-code/`](../claude-code/)** | Anthropic’s **claude-code** repo: plugins, `examples/`, marketplace, repo `.claude` commands, GitHub automation, etc. |
| **CLI binary** | Ships separately; not documented file-by-file here. |
| **Other workspace projects** | Out of scope unless merged intentionally. |

---

## Scope

### In scope

- **`../claude-code/plugins/**`**, **`examples/`**, **`.claude/commands/`**, root **`.claude-plugin/`**, **`Script/`**, **`scripts/`**, **`.github/`**, **`.devcontainer/`** — see mirrored tree in skeleton.
- **[`GLOSSARY.md`](GLOSSARY.md)**.

### Ignored for mirroring

- **`.vscode/`**, **`.git/`**, lockfiles, `node_modules`, binary media you choose to omit from `matching.paths`.

Macro-only descriptions (no upstream file copies): **`.github`**, **`.devcontainer`**, etc.—paths still listed in YAML when upstream files exist.

---

## Deliverable structure

```text
claude-code-skeleton/
├── README.md
├── PLAN.md
├── MATCHING.md              # GENERATED — edit MACRO.md files instead
├── GLOSSARY.md
├── MACRO.md                 # YAML + prose
├── .claude-plugin/MACRO.md
├── .claude/
│   ├── MACRO.md
│   └── commands/*.macro.md
├── examples/
├── .github/
├── .devcontainer/
├── Script/
├── scripts/
│   ├── MACRO.md
│   ├── generate_matching.py
│   └── requirements-matching.txt
└── plugins/
    └── <plugin>/...
```

### Naming

- **`commands/`**, **`agents/`** — only **`*.macro.md`** (pair with upstream **`*.md`**).
- **Other dirs** — **`MACRO.md`** with **`matching.paths`**.

---

## Phases

### Phase 0 — Conventions ✅

- [x] `MACRO.md` frontmatter with **`matching.paths`**
- [x] Generator + **`MATCHING.md`**
- [x] [`GLOSSARY.md`](GLOSSARY.md)

### Phase 1 — Inventory ✅

- [x] Plugins and supporting dirs enumerated; parity with upstream tree

### Phase 2–3 — Content ✅

- [x] Macro prose and `*.macro.md` pairs

### Phase 4 — When upstream changes

1. Add/move upstream files; mirror dirs in skeleton as needed.
2. Update **`matching.paths`** in the relevant **`MACRO.md`** (or run **`--seed`** then fix).
3. Add **`*.macro.md`** for new commands/agents.
4. Run: `python3 claude-code-skeleton/scripts/generate_matching.py`

### Phase 5 — Quality

- **Faithful** summaries; **navigable** links; **terse** prose.
- **`MATCHING.md`** always reflects YAML after edits (regenerate).

---

## Open decisions

| Topic | Resolution |
|-------|------------|
| Layout | Mirror `claude-code/` under skeleton (no `nl/` nesting). |
| `MATCHING.md` | Generated; source of truth is **`MACRO.md` YAML**. |

---

## Immediate next action

After any structural or path change: **`python3 claude-code-skeleton/scripts/generate_matching.py`** (with optional **`--seed`** when rebuilding path lists).
