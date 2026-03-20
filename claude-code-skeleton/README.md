<div align="center">

<img src="claude-code-skeleton-icon.png" alt="Claude Code Skeleton — pixel-art three-headed skeleton mascot" width="128" />

# Claude Code Skeleton

**Natural-language macro layer** for [Claude Code](https://github.com/anthropics/claude-code): skill-style **`MACRO.md`** maps, paired **`*.macro.md`** next to commands/agents, and a workspace-level **[`../MATCHING.md`](../MATCHING.md)** (generated from YAML — lives **next to** this folder, not inside `scripts/`).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<br/>

</div>

This folder is a **parallel, skimmable atlas** of plugins, examples, hooks, marketplace manifest, maintainer slash commands, and GitHub automation — **without** duplicating implementation source.

**Parent workspace:** see **[`../README.md`](../README.md)** (clone/pull upstream + run **`matching/generate_matching.py`**) and **[`../PLAN.md`](../PLAN.md)** (conventions).

---

## Why this exists

| You want… | This folder gives you… |
|-----------|------------------------|
| **Orientation** | YAML frontmatter + prose on folders via **`MACRO.md`** |
| **A concrete map** | **[`../MATCHING.md`](../MATCHING.md)** — auto-generated from `matching.paths` |
| **Command/agent context** | **`foo.macro.md`** beside each upstream **`foo.md`** in **`commands/`** and **`agents/`** |
| **Vocabulary** | **[`GLOSSARY.md`](GLOSSARY.md)** |

Most directories use **`MACRO.md`**; **`commands/`** and **`agents/`** use **`*.macro.md`** only (no rollup `MACRO.md` there).

---

## Layout (mirrors upstream `claude-code/`)

**Mirrored:** `plugins/`, `examples/`, `.claude/commands/`, `.claude-plugin/`, `Script/`, **`scripts/MACRO.md`** (documents upstream `claude-code/scripts/` only), `.github/`, `.devcontainer/`.

**Omitted:** `.vscode/`, `.git/`, bulky assets — see ignore rules in **[`../MATCHING.md`](../MATCHING.md)**.

**Not here:** the generator lives in **`../matching/generate_matching.py`** so this tree is not confused with **`claude-code/scripts/`**.

---

## Documentation inside this folder

| Doc | Purpose |
|-----|---------|
| **[`MACRO.md`](MACRO.md)** | Root macro index |
| **[`plugins/MACRO.md`](plugins/MACRO.md)** | Plugins roll-up |
| **[`../MATCHING.md`](../MATCHING.md)** | Skeleton ↔ upstream (**generated** at workspace root) |
| **[`../PLAN.md`](../PLAN.md)** | Conventions, frontmatter, matcher workflow |
| **[`GLOSSARY.md`](GLOSSARY.md)** | Shared vocabulary |

### Regenerate `MATCHING.md`

From the **workspace root** (parent of this directory):

```bash
python3 -m pip install -r matching/requirements.txt
python3 matching/generate_matching.py
```

See **[`../README.md`](../README.md)** — by default this **updates `claude-code/` from GitHub** then rewrites **`MATCHING.md`**.

---

## License

[MIT](LICENSE) © Tsun-Yi Yang
