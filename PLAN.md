# PLAN: Macro workspace (`claude-code` + `claude-code-skeleton`)

## Purpose

Reverse-engineer the **observable** surface of Claude Code (the extension layer) and maintain a traceable, human-readable map of it. The workspace holds:

| Path | Role |
|------|------|
| **`claude-code/`** | Upstream **Anthropic** tree — auto-updated via `git pull --ff-only` or shallow clone when you run the matcher. Treat as **read-only truth**. |
| **`claude-code-skeleton/`** | **Human-readable macro layer** — same relative layout as upstream, MACRO.md files only. Each MACRO.md declares which upstream files it covers (YAML frontmatter) and explains what those files do at a high level (prose body). |
| **`matching/`** | **Tooling** — `generate_matching.py` + `requirements.txt`. Validates coverage; kept outside `claude-code/scripts/` and skeleton `scripts/`. |
| **`MATCHING.md`** | **Generated** — short summary (PASS/FAIL, git tip, counts) + tables (covered paths, uncovered, validation issues). Overwritten every run; do **not** hand-edit. |
| **`README.md`**, **`PLAN.md`**, **`GLOSSARY.md`** | Human docs for the workspace. |
| **`MACRO.md`** *(workspace root)* | Narrative atlas — **not** read by the matcher (see below). Do **not** put `matching.paths` values here that you intend the matcher to see; they will be silently ignored. Only skeleton-tree MACRO.md files count. |

**Matcher input scope:** `collect_macro_paths` reads only **`claude-code-skeleton/**/MACRO.md`**. The workspace-root `MACRO.md` is for humans, even if it carries a `matching:` block — those paths are ignored by the matcher.

After a successful run, the script prints a **terminal summary** (upstream git revision + matching counts) that mirrors the top of **`MATCHING.md`**.

---

## The agentic loop — reference model

Claude Code's loop runs three phases that repeat until the task is done or you interrupt:

```
gather context  →  take action  →  verify results  →  (repeat)
```

Claude Code is the **agentic harness** around the model: it provides tools, context management, and execution environment. The model reasons; the tools act.

**Five built-in tool categories** (official names from [docs](https://code.claude.com/docs/en/how-claude-code-works)):

| Category | What Claude can do |
|----------|-------------------|
| File operations | Read, edit, create, rename |
| Search | Glob patterns, regex content search |
| Execution | Shell commands, tests, git |
| Web | Search, fetch docs |
| Code intelligence | Type errors after edits, definitions, references |

**Context management** — relevant when writing MACRO.md prose and when designing long-horizon loops:

- `CLAUDE.md` is loaded every session and survives compaction — put invariants here
- Skills load on demand; only descriptions are in context until triggered (`disable-model-invocation: true` keeps them out entirely)
- Subagents get fresh isolated context — their work does not bloat the main session
- `/compact focus on X` guides what the compressor preserves; `/context` shows what's consuming budget

**Session model** — relevant for parallel or long-running agentic work:

- `claude --continue` resumes the same session (conversation history restored, not session-scoped permissions)
- `claude --continue --fork-session` branches from the current state with a new session ID
- Git worktrees give each branch its own directory and therefore its own independent Claude session

---

## Open vs. closed — reverse-engineering boundary

The upstream repo exposes the **extension layer** (~180 files): plugin manifests, skill prompts, slash commands, hook scripts, example settings, workflow YAML. This is what the skeleton maps.

**What the skeleton can capture:**

- Plugin/command/agent/skill/hook structure and prompts
- Hook event names and their declared trigger points (`PreToolUse`, `Stop`, etc.)
- Permission allow/deny syntax in `settings.json`
- MCP server integration patterns

**What the skeleton cannot capture** (closed, obfuscated npm bundle or server-side):

- Agent loop internals — phase transitions, tool selection heuristics, stop conditions
- Context compression implementation — when it triggers, what the summariser preserves
- Permission enforcement implementation — how allow/deny rules are evaluated at runtime
- Tool dispatch and sandboxing
- Model inference and token sampling

Hook events (`PreToolUse`, `Stop`, …) are **surface hooks into the closed agent loop** — you observe and influence boundaries; you do not see the interior. Use `GLOSSARY.md` for the full open/closed term breakdown.

**Implication for MACRO.md prose:** document what the files *declare* (prompts, manifests, hook scripts). Inferences about runtime behavior should be explicitly flagged as inferences, not stated as fact.

---

## Redundancy map — where docs intentionally overlap (and where they don't)

| Topic | Canonical home | Also mentioned in | Resolution |
|-------|---------------|-------------------|------------|
| Quick start commands | `README.md` | PLAN.md (removed) | Follow README.md for running the matcher |
| Workspace layout | `README.md` | PLAN.md (table above, abbreviated) | PLAN.md table is authoritative for *roles*; README.md layout block is for orientation |
| Term definitions | `GLOSSARY.md` | README.md "Open vs closed" callout | GLOSSARY.md is canonical; README.md only summarises |
| Open/closed boundary | `GLOSSARY.md` | PLAN.md (section above) | PLAN.md adds *reverse-engineering implications*; GLOSSARY.md stays as pure reference |
| Matcher flags | `generate_matching.py` docstring | README.md, PLAN.md | Script docstring is canonical; prose docs summarise |

Avoid adding workflow narrative to GLOSSARY.md or term definitions to PLAN.md — keep each file's focus clean.

---

## `claude-code-skeleton/` top-level (mirrors upstream)

```text
claude-code-skeleton/
├── .claude/              # repo-level slash commands (MACRO.md covers all commands)
├── .claude-plugin/
├── .devcontainer/
├── .github/              # workflows, ISSUE_TEMPLATE, workflow-macros
├── Script/               # upstream PowerShell helper (see Script/MACRO.md)
├── examples/
├── plugins/
└── scripts/              # upstream automation; MACRO.md documents claude-code/scripts/
```

The matcher lives only under **`matching/`**, not under **`claude-code-skeleton/scripts/`**.

---

## Frontmatter (mandatory on every `MACRO.md` under the skeleton)

```yaml
---
matching:
  paths:
    - README.md
    - plugins/foo/bar.py
    - plugins/foo/commands/do-thing.md
---
```

| Rule | Detail |
|------|--------|
| `matching.paths` | Paths **relative to `claude-code/`**. Use `[]` for index-only macros. Includes commands and agents — list them here explicitly. |
| Uniqueness | Same path must not appear in two `MACRO.md` files. |

**MACRO.md body — write for humans, not the matcher:**

The YAML frontmatter is the machine-readable part. The body below the `---` is for people. Write it at a high enough level that someone unfamiliar with the plugin can understand what it does, why it exists, and how its pieces fit together. If a section of upstream is already self-explanatory, a one-paragraph summary is enough — don't duplicate content, just orient the reader.

**Granularity — fewer MACRO.md files is better:**

Prefer one MACRO.md per plugin root and one per skill, not one per subdirectory.

| Preferred | Avoid |
|-----------|-------|
| Plugin root MACRO.md lists: `README.md`, `plugin.json`, `hooks.json`, hook scripts, commands, agents | Separate MACRO.md for `.claude-plugin/`, `hooks/`, `commands/`, `agents/` within one plugin |
| Skill MACRO.md lists: `SKILL.md` + `references/*.md` + `examples/*.md` as a group | Separate MACRO.md for `references/`, `examples/`, `scripts/` per skill |

Rule of thumb: only create a sub-folder MACRO.md if that folder has **5 or more files** that benefit from independent description.

**Bootstrap `paths` after large upstream moves:**

```bash
python3 -m pip install -r matching/requirements.txt
python3 matching/generate_matching.py --seed --no-fetch
python3 matching/generate_matching.py --no-fetch
```

(`--no-fetch` if you are not cloning/updating yet.)

---

## Workflow

**Typical cycle** (see `README.md` for full command reference):

1. Edit `claude-code-skeleton/**/MACRO.md` — update `matching.paths` and prose.
2. Run `python3 matching/generate_matching.py --no-fetch` to validate locally.
3. Inspect `MATCHING.md` (summary + tables) and fix any flagged issues until you reach PASS.
4. Run without `--no-fetch` to pull latest upstream before committing.

**After large upstream moves** — use `--seed` to auto-populate `matching.paths`, then review the diff before committing.
