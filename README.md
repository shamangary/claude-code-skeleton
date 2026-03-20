<div align="center">

<img src="claude-code-skeleton-icon.png" alt="Claude Code Skeleton — pixel-art three-headed skeleton mascot" width="128" />

# Claude Code Skeleton

**Natural-language macro layer** for the [Claude Code](https://github.com/anthropics/claude-code) repo: human-oriented **`MACRO.md`** maps, generated **[`MATCHING.md`](MATCHING.md)**, and paired **`*.macro.md`** files next to upstream commands and agents.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<br/>

</div>

Think of this repo as a **parallel, skimmable atlas** of plugins, examples, hooks, marketplace manifest, maintainer slash commands, and GitHub automation—without duplicating implementation source.

---

## Why this exists

| You want… | This repo gives you… |
|-----------|----------------------|
| **Orientation** | Skill-style frontmatter + prose on folders via **`MACRO.md`** |
| **A concrete map** | **`MATCHING.md`** linking macros ↔ upstream paths (generator-driven) |
| **Command/agent context** | **`foo.macro.md`** beside each upstream **`foo.md`** in **`commands/`** and **`agents/`** |
| **Conventions** | **[`PLAN.md`](PLAN.md)**, **[`GLOSSARY.md`](GLOSSARY.md)** |

Most directories use **`MACRO.md`**; **`commands/`** and **`agents/`** use **`*.macro.md`** pairs only (no rollup `MACRO.md` there).

---

## Layout (mirrors upstream)

The skeleton mirrors **`claude-code/`** structure: **`plugins/`**, **`examples/`**, **`.claude/commands/`**, **`.claude-plugin/`**, **`Script/`**, **`scripts/MACRO.md`** (GitHub automation), plus **`.github/`** and **`.devcontainer/`** as macro-only summaries.

**Omitted on purpose:** **`.vscode/`**, assets, **`.git/**` — editor noise and binaries stay out of the mirror.

---

## Documentation

| Doc | Purpose |
|-----|---------|
| **[`MACRO.md`](MACRO.md)** | Root macro index — start here |
| **[`plugins/MACRO.md`](plugins/MACRO.md)** | Plugins roll-up |
| **[`MATCHING.md`](MATCHING.md)** | Skeleton ↔ upstream file map (**generated** — do not hand-edit) |
| **[`PLAN.md`](PLAN.md)** | Conventions, scope, maintenance |
| **[`GLOSSARY.md`](GLOSSARY.md)** | Shared vocabulary (plugins, hooks, skills, MCP, …) |

### Regenerate `MATCHING.md`

From **this repo’s root** (typical GitHub clone):

```bash
python3 -m pip install -r scripts/requirements-matching.txt
python3 scripts/generate_matching.py
```

If this folder lives inside a parent workspace as `claude-code-skeleton/`, prefix those paths accordingly (e.g. `claude-code-skeleton/scripts/...`).

`matching.paths` in each **`MACRO.md`** drives the map. Optional bootstrap: `python3 scripts/generate_matching.py --seed` (then review YAML and re-run without `--seed`). Details in **[`PLAN.md`](PLAN.md)**.

---

## License

[MIT](LICENSE) © Tsun-Yi Yang
