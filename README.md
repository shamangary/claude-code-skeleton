# Claude Code — macro workspace

This repository brings together **upstream Claude Code**, a **natural-language skeleton** of that tree, and a **matcher** that keeps an auditable map between them.

## Layout

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

## Matching (recommended workflow)

**Running the matcher updates `claude-code/` to the latest default remote and rebuilds `MATCHING.md`.**

```bash
python3 -m pip install -r matching/requirements.txt
python3 matching/generate_matching.py
```

What it does:

1. **`git pull --ff-only`** inside `claude-code/` if it is already a repo, or **`git clone --depth 1`** from **`https://github.com/anthropics/claude-code.git`** if the folder is missing/empty.
2. Reads **`matching.paths`** YAML on every **`claude-code-skeleton/**/MACRO.md`**.
3. Writes **`MATCHING.md`** with:
   - **Report summary** (counts, PASS/FAIL),
   - **Ignored paths** policy (.git, .vscode, implicit command/agent prompts),
   - **1:1** and **1:many** tables,
   - **Validation issues** (duplicate paths, missing upstream files, bad YAML),
   - **Uncovered upstream files** (informational — not necessarily errors).

Use **`python3 matching/generate_matching.py --no-fetch`** if you manage `claude-code/` yourself (fork, pin, or air‑gapped).

Other flags: **`--remote URL`**, **`--branch BRANCH`**, **`--seed`** (rebuild YAML path lists — review git diff). Details in **[`PLAN.md`](PLAN.md)** and the docstring in **`matching/generate_matching.py`**.

## Skeleton-only docs

See **[`claude-code-skeleton/README.md`](claude-code-skeleton/README.md)** for the macro layer README (atlas of plugins, hooks, examples, etc.).

## License

Skeleton content: see **`claude-code-skeleton/LICENSE`**. Upstream **`claude-code/`** remains under its own license.
