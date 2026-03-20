<p align="center">
  <img src="claude-code-skeleton-icon.png" alt="Claude Code Skeleton — macro workspace" width="120">
</p>

<h1 align="center">Claude Code Skeleton</h1>

<p align="center">
  <strong>Upstream Claude Code + a human-readable skeleton + an auditable matcher that keeps them in sync.</strong>
</p>

<p align="center">
  Clone, run one command, get a <code>MATCHING.md</code> report you can diff in CI — no guesswork about what macro docs map to which upstream files.
</p>

---

## Why this repo

| You get | How |
|--------|-----|
| **Traceability** | Every `claude-code-skeleton/**/MACRO.md` declares `matching.paths` in YAML; the matcher validates coverage and flags gaps. |
| **Fresh upstream** | Optional `git pull` / shallow clone of [anthropics/claude-code](https://github.com/anthropics/claude-code) before regenerating the report. |
| **Review-friendly output** | `MATCHING.md` is generated — brief summary + tables (covered paths, uncovered, validation issues). |

Useful if you maintain plugins, hooks, or macro docs and want a **repeatable, readable audit trail** instead of tribal knowledge.

> **Open vs closed in `claude-code/`** — The upstream GitHub repo exposes ~180 readable files: plugin manifests, skill prompts, hook scripts, slash commands, example settings, and workflow YAML. These define *what the extensions do*. The **agent loop** (tool selection, reasoning, context compression, permission enforcement) lives in the minified `@anthropic-ai/claude-code` npm bundle and is not human-readable. This skeleton documents the open file topology; hook event names like `PreToolUse` and `Stop` are the surface where you plug in — the engine behind them is closed. See **[`GLOSSARY.md`](GLOSSARY.md)** for a full open/closed breakdown.

## Quick start

```bash
python3 -m pip install -r matching/requirements.txt
python3 matching/generate_matching.py
```

### Example output

The matcher prints **upstream git** context for `claude-code/` and a **matching summary** (counts mirror the top of `MATCHING.md`):

```text
────────────────────────────────────────────────────
  claude-code/ (upstream git)
────────────────────────────────────────────────────
  version:   v2.1.80
  commit:    1653669 (16536693ecc04f50f04696e109fe2a1a5f0d09fd)
  branch:    main
  summary:   chore: Update CHANGELOG.md
  date:      2026-03-19 22:08:02 +0000
  origin:    https://github.com/anthropics/claude-code.git

────────────────────────────────────────────────────
  matching summary
────────────────────────────────────────────────────
  PASS   →  MATCHING.md

  upstream files:   183   uncovered: 7
  MACRO.md files:   28   paths declared: 176

  errors: none
────────────────────────────────────────────────────
```

*(Exact revision and counts depend on your clone and skeleton state.)*

Prefer a fixed `claude-code/` checkout? Use `--no-fetch` and manage the tree yourself. More flags: `--remote`, `--branch`, `--seed` (rebuild path lists — review the diff). See **[`PLAN.md`](PLAN.md)**, **[`GLOSSARY.md`](GLOSSARY.md)**, and the docstring in **`matching/generate_matching.py`**.

## Workspace layout

```text
./
├── README.md                      # This file
├── PLAN.md                        # Conventions and workflows
├── GLOSSARY.md                    # Terms (plugins, hooks, skills, …)
├── LICENSE                        # License for this workspace
├── MACRO.md                       # Optional root narrative (not read by the matcher)
├── MATCHING.md                    # GENERATED — read-only; do not edit by hand
├── claude-code-skeleton-icon.png  # Logo for README / sharing
├── matching/
│   ├── generate_matching.py       # Fetch upstream (default) + writes MATCHING.md
│   └── requirements.txt           # PyYAML
├── claude-code/                   # Official Anthropic repo (clone or your fork)
└── claude-code-skeleton/          # Human-readable macro layer: MACRO.md files only
    ├── .claude/
    ├── .claude-plugin/
    ├── .devcontainer/
    ├── .github/
    ├── Script/                    # e.g. PowerShell helper (mirrors upstream)
    ├── examples/
    ├── plugins/
    └── scripts/                   # MACRO.md covers upstream scripts/; matcher stays in ./matching/
```

The matcher only ingests YAML from **`claude-code-skeleton/**/MACRO.md`**. A **`MACRO.md`** at the workspace root is for humans only unless you relocate that content into the skeleton.

## What the matcher does

1. **`git pull --ff-only`** inside `claude-code/` if it is already a repo, or **`git clone --depth 1`** from **`https://github.com/anthropics/claude-code.git`** if the folder is missing or empty.
2. Reads **`matching.paths`** YAML on every **`claude-code-skeleton/**/MACRO.md`**.
3. Overwrites **`MATCHING.md`** (full file) with a short **summary** and **tables** for covered paths, uncovered upstream files, and validation issues; and prints a **terminal summary** (git identity + counts).

## Refining `claude-code-skeleton/` with your agentic workflow

You can use **any** agentic coding setup—**Claude Code**, **Cursor**, **GitHub Copilot** (agent / chat in-editor), or similar—as long as the model can read project files and apply patches. Treat **[`PLAN.md`](PLAN.md)** as the **rules of engagement**: what the skeleton is for, mandatory YAML on every skeleton **`MACRO.md`**, and how **`MATCHING.md`** is produced.

**Scope to edit:** only under **`claude-code-skeleton/`** (plus optional narrative in root **`MACRO.md`**). Do **not** hand-edit **`MATCHING.md`**. Treat **`claude-code/`** as **read-only truth** for "what upstream looks like" unless you intentionally maintain a fork.

**Suggested loop**

1. Refresh upstream (or pin it): run **`python3 matching/generate_matching.py`** with or without **`--no-fetch`**, per `PLAN.md`.
2. Give your agent **`PLAN.md`**, **`GLOSSARY.md`** (shared vocabulary), and the specific upstream paths you care about.
3. Ask it to **align the skeleton with upstream**: update prose in the relevant **`MACRO.md`** files and adjust **`matching.paths`** to reflect any new or removed upstream files.
4. Run **`python3 matching/generate_matching.py --no-fetch`** and fix anything flagged until you get **PASS**.

**Prompt pattern (tool-agnostic)**
*"Follow [`PLAN.md`](PLAN.md). Compare `claude-code/<path>…` with `claude-code-skeleton/<path>…`. Update only the `MACRO.md` files: frontmatter `matching.paths` and the human-readable body. Do not copy implementation files into the skeleton. When done, list which `MACRO.md` files changed and why."*

Product-specific habits: use your environment's **folder / file context** (e.g. adding `PLAN.md` and a target subtree to the chat) so the model does not guess the matching rules from memory.

## Where to read next

- **[`MACRO.md`](MACRO.md)** — workspace-level macro map and neighbors.
- **[`claude-code-skeleton/plugins/MACRO.md`](claude-code-skeleton/plugins/MACRO.md)** — plugin atlas; other subtrees (`examples/`, `.claude/`, etc.) each have their own **`MACRO.md`**.

## License

**[`LICENSE`](LICENSE)** applies to this workspace. Upstream **`claude-code/`** remains under its own license.
