<p align="center">
  <img src="claude-code-skeleton-icon.png" alt="Claude Code Skeleton — macro workspace" width="120">
</p>

<h1 align="center">Claude Code Skeleton</h1>

<p align="center">
  <strong>Upstream Claude Code + a natural-language skeleton + an auditable matcher that keeps them in sync.</strong>
</p>

<p align="center">
  Clone, run one command, get a <code>MATCHING.md</code> report you can diff in CI — no guesswork about what macro docs map to which upstream files.
</p>

---

## Why this repo

| You get | How |
|--------|-----|
| **Traceability** | Every `claude-code-skeleton/**/MACRO.md` declares `matching.paths` in YAML; the matcher validates 1:1 and 1:many links. |
| **Fresh upstream** | Optional `git pull` / shallow clone of [anthropics/claude-code](https://github.com/anthropics/claude-code) before regenerating the report. |
| **Review-friendly output** | `MATCHING.md` is generated — summary, tables, ignored-path policy, validation issues, and uncovered upstream paths. |

Useful if you maintain plugins, hooks, or macro docs and want a **repeatable, readable audit trail** instead of tribal knowledge.

## Quick start

```bash
python3 -m pip install -r matching/requirements.txt
python3 matching/generate_matching.py
```

Prefer a fixed `claude-code/` checkout? Use `--no-fetch` and manage the tree yourself. More flags: `--remote`, `--branch`, `--seed` (rebuild path lists — review the diff). See **[`PLAN.md`](PLAN.md)** and the docstring in **`matching/generate_matching.py`**.

## Repository layout

```text
./
├── README.md                 # This file
├── PLAN.md                   # Conventions and workflows
├── MATCHING.md               # GENERATED — read-only; do not edit by hand
├── matching/
│   ├── generate_matching.py # Fetches upstream (default) + writes MATCHING.md
│   └── requirements.txt     # PyYAML
├── claude-code/              # Official Anthropic repo (clone or your fork)
└── claude-code-skeleton/     # MACRO.md / *.macro.md mirror (no implementation copy)
```

## What the matcher does

1. **`git pull --ff-only`** inside `claude-code/` if it is already a repo, or **`git clone --depth 1`** from **`https://github.com/anthropics/claude-code.git`** if the folder is missing or empty.
2. Reads **`matching.paths`** YAML on every **`claude-code-skeleton/**/MACRO.md`**.
3. Writes **`MATCHING.md`** with:
   - Report summary (counts, PASS/FAIL)
   - Ignored paths policy (`.git`, `.vscode`, implicit command/agent prompts)
   - 1:1 and 1:many tables
   - Validation issues (duplicate paths, missing upstream files, bad YAML)
   - Uncovered upstream files (informational — not necessarily errors)

## Skeleton docs

See **[`claude-code-skeleton/README.md`](claude-code-skeleton/README.md)** for the macro layer README (atlas of plugins, hooks, examples, and more).

## License

Skeleton content: **`claude-code-skeleton/LICENSE`**. Upstream **`claude-code/`** stays under its own license.
