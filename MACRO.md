---
matching:
  paths:
  - .gitattributes
  - .gitignore
  - CHANGELOG.md
  - LICENSE.md
  - README.md
  - SECURITY.md
---

# Claude Code — macro view (agentic layer)

**Role:** Orient readers to how this repository extends **Claude Code** as an **agentic system**: slash commands, subagents, skills, and lifecycle hooks that shape tool use and session behavior.

**Scope:** Mirrors the inner [`claude-code`](../claude-code/) repo at macro granularity: [`plugins/`](plugins/), [`examples/`](examples/), [`.claude/`](.claude/) (repo slash commands + `*.macro.md` pairs), [`.claude-plugin/`](.claude-plugin/), [`Script/`](Script/), [`scripts/`](scripts/), [`.github/`](.github/) (workflows + templates), [`.devcontainer/`](.devcontainer/). **Skipped:** `.vscode`, `.git`, root demo assets, CLI binary source.

**Audience:** Engineers who want a **system map** before reading prompts, JSON manifests, or hook scripts.

**Layout:** Under [`plugins/`](plugins/), most dirs use **`MACRO.md`**; **`plugins/.../commands/`** and **`plugins/.../agents/`** use **`foo.macro.md`** next to each upstream `foo.md`. The **repo’s own** [`.claude/commands/`](.claude/commands/) uses the same **`*.macro.md`** pattern for Anthropic’s maintainer slash flows.

**Neighbors:** **[`MATCHING.md`](MATCHING.md)** (skeleton ↔ upstream index); [`plugins/MACRO.md`](plugins/MACRO.md); [`examples/MACRO.md`](examples/MACRO.md); [`.claude/MACRO.md`](.claude/MACRO.md); [`.claude-plugin/MACRO.md`](.claude-plugin/MACRO.md); [`scripts/MACRO.md`](scripts/MACRO.md); [`.github/MACRO.md`](.github/MACRO.md); [`.devcontainer/MACRO.md`](.devcontainer/MACRO.md); [`Script/MACRO.md`](Script/MACRO.md).

**Stability:** Descriptions follow the upstream repo at the time of writing; they are **not** a semver API contract—plugin manifests and hooks are the real contracts.
