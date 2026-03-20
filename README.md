<p align="center">
  <img src="claude-code-skeleton-icon.png" alt="Claude Code Skeleton — macro workspace" width="240">
</p>

<h1 align="center">Claude Code Skeleton</h1>

<p align="center">
  <strong>Understand the Claude Code extension layer — then build your own agentic loop on top of it.</strong>
</p>

<p align="center">
  A human-readable skeleton of the upstream Anthropic repo + an auditable matcher that keeps them in sync.
</p>

---

## What this repo is for

Claude Code exposes an **extension layer** of ~180 readable files: plugin manifests, skill prompts, hook scripts, slash commands, and example settings. The actual **agent loop engine** (tool selection, stop conditions, context compression) lives in a closed npm bundle you cannot read.

This skeleton helps you:

1. **Map what's open** — every file in the upstream repo is documented in a `MACRO.md` with a human-readable explanation
2. **Understand the hook surface** — `PreToolUse`, `PostToolUse`, `Stop`, `UserPromptSubmit` are where you plug in
3. **Build your own agentic loop** — from a single hook all the way to a full multi-agent pipeline

> See [`GLOSSARY.md`](GLOSSARY.md) for the full open/closed breakdown and [`PLAN.md`](PLAN.md) for workspace conventions.

---

## How the agentic loop works

Before building extensions, understand what you're extending. Claude Code's loop has three phases that repeat until the task is done:

```
Your prompt
     │
     ▼
┌──────────────────┐
│  Gather context  │  ← read files, search, run tests, web fetch
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Take action    │  ← edit files, run commands, call agents
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Verify results  │  ← run tests, check output, re-read files
└────────┬─────────┘
         │
         ▼ (loop until done, or you interrupt)
```

Claude Code is the **agentic harness** around the model — it provides tools, context management, and execution environment. The model reasons; the tools act.

### Built-in tool categories

| Category | What Claude can do |
|----------|-------------------|
| **File operations** | Read, edit, create, rename files |
| **Search** | Find files by pattern, search content with regex |
| **Execution** | Run shell commands, start servers, run tests, use git |
| **Web** | Search the web, fetch documentation |
| **Code intelligence** | See type errors after edits, jump to definitions, find references |

### Safety mechanisms

| Mechanism | How it works |
|-----------|-------------|
| **Checkpoints** | Every file edit is snapshotted before change — press Esc×2 to rewind |
| **Permission modes** | Shift+Tab cycles: Default → Auto-accept edits → Plan mode (read-only) |
| **CLAUDE.md** | Persistent rules loaded every session — put invariants here, not in conversation |

### What you can hook into

Extensions plug into the loop at defined boundary points:

| Extension type | When it runs | Can it block Claude? |
|----------------|-------------|----------------------|
| `SessionStart` hook | Once at session open | No — inject context only |
| `PreToolUse` hook | Before every tool call | Yes — return `{"decision":"block"}` |
| `PostToolUse` hook | After every tool call | No — observe/log only |
| `Stop` hook | When Claude is about to stop | Yes — return `{"decision":"block"}` to re-loop |
| `UserPromptSubmit` hook | When user sends a message | Yes — can modify or block |
| Slash command | User-invoked | n/a — drives the loop |
| Skill | Model-invoked on trigger | n/a — injects guidance |
| Subagent | Spawned by orchestrator | n/a — fresh isolated context |

---

## Build your own agentic loop

Stack these six levels progressively. Each builds on the previous.

### Primitive reference

| Primitive | File type | Role in the loop |
|-----------|-----------|-----------------|
| **CLAUDE.md** | Markdown | Persistent context loaded every session; survives compaction |
| **Hook** | `hooks.json` + script | React at lifecycle boundaries |
| **Slash command** | `commands/*.md` | User-invoked workflow prompt |
| **Agent** | `agents/*.md` | Specialist sub-prompt with its own tool allow-list |
| **Skill** | `SKILL.md` | Model-invoked guidance loaded on trigger |
| **Plugin** | `plugin.json` + any of the above | Installable package |

---

### Level 0 — CLAUDE.md (persistent context)

**Start here before anything else.** CLAUDE.md is loaded at the start of every session and survives context compaction. It is Claude's long-term memory for your project.

**What to put in CLAUDE.md:**

```markdown
# Project conventions

## Stack
- Python 3.12, FastAPI, PostgreSQL 16
- Tests: pytest, always run with `pytest -x`
- Never use `print()` — use `logger = logging.getLogger(__name__)`

## Commit rules
- Imperative mood, ≤72 chars subject
- Always run `pytest -x` before committing
- Never amend published commits

## Compact Instructions
When compacting, preserve: current task, open files, failing tests.
```

**How to scaffold it:**

```bash
# Inside a Claude Code session
/init
```

`/init` walks you through creating a CLAUDE.md for your project interactively.

**Plan mode** (read-only explore before acting) is the companion to CLAUDE.md. Use it to build the CLAUDE.md itself:

```text
[Shift+Tab twice to enter Plan mode]

Read the src/ directory and propose a CLAUDE.md with:
- tech stack summary
- test command
- code conventions you observe
- commit rules
```

Review the plan, then let Claude write the file.

---

### Level 1 — Single hook (simplest extension)

**What it does:** intercept one lifecycle event and run a shell script.

**When to use:** you want Claude to never do something (block), always log something, or inject context at session start.

**Files needed:**

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── hooks/
    ├── hooks.json
    └── guard.sh
```

**`hooks/hooks.json`:**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/guard.sh"
      }
    ]
  }
}
```

**`hooks/guard.sh`** — read the tool payload from stdin, decide allow or block:

```bash
#!/usr/bin/env bash
# Claude passes the tool call as JSON on stdin
input=$(cat)
tool=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))")

if [[ "$tool" == "Bash" ]]; then
  cmd=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))")
  if echo "$cmd" | grep -qE 'rm\s+-rf\s+/'; then
    echo '{"decision":"block","reason":"Refusing destructive rm -rf /"}'
    exit 0
  fi
fi

echo '{"decision":"allow"}'
```

**`plugin.json` minimum:**

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Guards against destructive commands",
  "hooks": "hooks/hooks.json"
}
```

> **Context note:** `PreToolUse` fires during the "take action" phase. Blocking here keeps the loop in "gather context" until Claude finds a safe path.

---

### Level 2 — Slash command

**What it does:** give Claude a reusable, user-invocable workflow written in plain English.

**When to use:** you have a multi-step task you run repeatedly (commit, deploy, review a PR, scaffold a component).

**Files needed:**

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── commands/
    └── my-workflow.md
```

**`commands/my-workflow.md`:**

```markdown
---
description: Stage, summarise, and commit all changes
allowed-tools:
  - Bash
  - Read
---

You are a careful Git committer. Work through all three loop phases:

**Gather context**
1. Run `git diff` and `git status` to understand what changed.
2. Read any files that look unclear from the diff.

**Take action**
3. Write a commit message: imperative mood, ≤72 chars subject, blank line, brief body.
4. Run `git add -A && git commit -m "<your message>"`.

**Verify**
5. Run `git log --oneline -1` to confirm the commit landed.
6. Print the hash and subject.

Never amend, force-push, or skip hooks.
```

**Key frontmatter fields:**

```markdown
---
description: shown in /help
allowed-tools: [Bash, Read, Edit, Write, Glob, Grep]
argument-hint: "<what the user passes>"
---
```

---

### Level 3 — Hook + command (guarded workflow)

**What it does:** a command drives the loop; a hook enforces invariants at the boundary of every tool call.

**Example:** `/deploy` command that deploys, but a `PreToolUse` hook blocks any `kubectl delete` unless `DEPLOY_CONFIRMED=1` is set.

**Directory layout:**

```
my-plugin/
├── .claude-plugin/plugin.json
├── hooks/
│   ├── hooks.json
│   └── require-confirm.sh
└── commands/
    └── deploy.md
```

**`hooks/require-confirm.sh`:**

```bash
#!/usr/bin/env bash
input=$(cat)
cmd=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))")

if echo "$cmd" | grep -q 'kubectl delete'; then
  if [[ -z "$DEPLOY_CONFIRMED" ]]; then
    echo '{"decision":"block","reason":"Set DEPLOY_CONFIRMED=1 before destructive kubectl commands."}'
    exit 0
  fi
fi

echo '{"decision":"allow"}'
```

**`commands/deploy.md`:**

```markdown
---
description: Build, test, and deploy to the current Kubernetes context
allowed-tools: [Bash]
---

Work through gather → act → verify:

**Gather:** Run `make build` (fail fast). Run `make test` — stop if any test fails.

**Act:** Run `docker build -t myapp:latest . && docker push myapp:latest`.
Then `kubectl apply -f k8s/`.

**Verify:** Run `kubectl rollout status deployment/myapp` and report the result.

If any step fails, stop and report the error — do not skip steps or continue past failure.
```

---

### Level 4 — Plugin with specialist agents

**What it does:** break a complex workflow into **sequential specialist agents**, each with a focused role and a limited tool set. This is the core pattern in `feature-dev`, `code-review`, and `pr-review-toolkit`.

Each agent gets its **own fresh context** — subagents don't bloat your main conversation. They return a summary when done.

**Architecture:**

```
my-plugin/
├── .claude-plugin/plugin.json
├── agents/
│   ├── explorer.md      # gather phase: reads codebase, produces report
│   ├── planner.md       # context → plan: proposes design
│   └── implementer.md   # act phase: writes code
└── commands/
    └── build-feature.md # orchestrates the three agents in sequence
```

**`commands/build-feature.md`** — orchestrator (note: each agent runs in its own fresh context):

```markdown
---
description: Explore → plan → implement a feature end to end
allowed-tools: [Agent]
---

Run these three agents in sequence. Pass outputs forward.

**Step 1 — Explore (gather context)**
Launch the `explorer` agent with the user's feature description.
Collect its structured report: affected files, patterns, risks.

**Step 2 — Plan (act on context)**
Launch the `planner` agent with: feature description + explorer report.
Collect: proposed design (file list, change summary, open questions).

**Step 3 — Implement (act + verify)**
Launch the `implementer` agent with: feature description + planner design.
It writes all code and runs tests.

After Step 3, print: files changed, test result, open questions from the planner.
```

**`agents/explorer.md`** — read-only gather phase:

```markdown
---
description: Survey the codebase and produce a structured report
allowed-tools: [Read, Glob, Grep]
---

You are a codebase surveyor. Given a feature description:

1. Find relevant files with Glob and Grep.
2. Read the most important ones (max 10).
3. Identify: existing patterns, likely touch points, risks.

Output:
- Relevant files (path + one-line reason)
- Patterns observed
- Risks or blockers
- Suggested approach (2–3 sentences)

Do not write any code. Read only.
```

**`agents/implementer.md`** — act + verify phase:

```markdown
---
description: Implement a feature given a plan
allowed-tools: [Read, Edit, Write, Bash]
---

You are a careful implementer. You receive a feature description and a design plan.

Rules:
- Follow the plan. Do not invent scope.
- Make the minimal change that implements the feature.
- Run tests after every file change: `pytest -x` (or the project's test command from CLAUDE.md).
- If a test fails, fix it before moving on.
- Do not refactor surrounding code unless the plan says to.

When done: list every file changed and the final test result.
```

---

### Level 5 — Loop until done (Stop hook)

**What it does:** intercept the `Stop` event and re-launch Claude with a continuation prompt until an exit condition is met. This is the `ralph-wiggum` pattern.

The `Stop` hook turns a single-pass workflow into a **persistent agentic loop** — Claude keeps cycling through gather → act → verify until *your* condition is satisfied.

**Use cases:** run until all tests pass, run until no linting errors, background poller.

**`hooks/hooks.json`:**

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "command",
        "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/stop-hook.sh"
      }
    ]
  }
}
```

**`hooks/stop-hook.sh`:**

```bash
#!/usr/bin/env bash
# Called when Claude is about to stop.
# Return {"decision":"allow"} to let it stop.
# Return {"decision":"block","reason":"..."} to re-loop with a new prompt.

# Limit iterations to avoid infinite loops
ITER_FILE="/tmp/claude_loop_count_$$"
count=$(cat "$ITER_FILE" 2>/dev/null || echo 0)
count=$((count + 1))
echo "$count" > "$ITER_FILE"

if [[ "$count" -ge 10 ]]; then
  rm -f "$ITER_FILE"
  echo '{"decision":"allow"}'
  exit 0
fi

# Check exit condition: all tests pass
if npm test --silent 2>/dev/null; then
  rm -f "$ITER_FILE"
  echo '{"decision":"allow"}'
else
  echo '{"decision":"block","reason":"Tests are still failing. Fix the failures and then stop."}'
fi
```

> **Critical:** always include a hard exit condition (max iterations, a sentinel file, a timeout). A Stop hook that always blocks loops forever.

---

### Level 6 — Composed system (full agentic loop)

**What it does:** combine multiple plugins to cover the full development lifecycle. Hook events from all plugins merge and fire in registration order.

**Example composition:**

```
~/.claude/settings.json   ← install all plugins
│
├── hookify               ← declarative guardrails (block rm -rf, require tests before stop)
├── security-guidance     ← PreToolUse scan for injection/XSS in every Edit/Write
├── feature-dev           ← /feature-dev: explorer → architect → reviewer agents
├── commit-commands       ← /commit, /commit-push-pr for Git workflow
└── ralph-wiggum          ← Stop hook: loop until the user's definition of "done"
```

**Install plugins in `settings.json`:**

```json
{
  "plugins": [
    "hookify",
    "security-guidance",
    "feature-dev",
    "commit-commands",
    "ralph-wiggum"
  ]
}
```

**Add a domain-knowledge Skill** — injects guidance when a trigger phrase appears, without bloating context (skills load on demand):

```markdown
<!-- skills/migrations/SKILL.md -->
---
triggers:
  - "write a migration"
  - "add a database column"
disable-model-invocation: false
---

# Database migration rules

Always use Alembic. Files go in `alembic/versions/`.
Column names are snake_case. Never add NOT NULL without a DEFAULT on existing tables.
Run `alembic upgrade head` after writing, verify with `alembic current`.
```

**Context management at this scale:**

- Skills load on demand — only the description is in context until triggered
- Subagents (Level 4 pattern) get fresh isolated context — use them for large subtasks
- Put invariants in `CLAUDE.md` so they survive compaction
- Run `/compact focus on the current PR changes` to guide what's preserved
- Run `/context` to see what's consuming context budget (MCP servers add tool definitions to every request)

**Parallel work with session forking:**

```bash
# Start a feature session
claude --model claude-opus-4-6

# Fork it to try a different approach without affecting the original
claude --continue --fork-session
```

Or use git worktrees for fully parallel Claude sessions on separate branches:

```bash
git worktree add ../feature-b feature-b
cd ../feature-b && claude   # completely separate session
```

---

## Reference: anatomy of a minimal plugin

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # name, version, description, entrypoints
├── hooks/
│   ├── hooks.json           # event → script mapping
│   └── pretooluse.sh        # or .py
├── commands/
│   └── my-command.md        # slash command prompt
├── agents/
│   └── my-agent.md          # specialist agent prompt
└── skills/
    └── my-skill/
        └── SKILL.md         # trigger-based injected guidance
```

**`plugin.json` minimum:**

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "hooks": "hooks/hooks.json"
}
```

---

## Auditing this skeleton (matcher)

The matcher validates that every upstream file is documented in the skeleton.

```bash
python3 -m pip install -r matching/requirements.txt
python3 matching/generate_matching.py            # fetch upstream + regenerate MATCHING.md
python3 matching/generate_matching.py --no-fetch # skip network, use existing claude-code/
```

More flags: `--remote URL`, `--branch NAME`, `--seed` (rebuild path lists — review the diff).

## Workspace layout

```text
./
├── README.md                      # This file
├── PLAN.md                        # Conventions, open/closed boundary, redundancy map
├── GLOSSARY.md                    # Terms (plugins, hooks, skills, agents, …)
├── LICENSE
├── MACRO.md                       # Narrative atlas (not read by the matcher)
├── MATCHING.md                    # GENERATED — do not hand-edit
├── matching/
│   ├── generate_matching.py
│   └── requirements.txt
├── claude-code/                   # Upstream Anthropic repo (read-only truth)
└── claude-code-skeleton/          # MACRO.md files only — one per upstream subtree
    ├── .claude/
    ├── .claude-plugin/
    ├── .devcontainer/
    ├── .github/
    ├── Script/
    ├── examples/
    ├── plugins/
    └── scripts/
```

## Where to read next

- [`PLAN.md`](PLAN.md) — conventions, the open/closed boundary, and which doc is canonical for what
- [`GLOSSARY.md`](GLOSSARY.md) — every term defined (Plugin, Hook, Agent, Skill, MCP, …)
- [Claude Code official docs: How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) — official reference for the agentic loop, tools, sessions, and permissions
- [`claude-code-skeleton/plugins/MACRO.md`](claude-code-skeleton/plugins/MACRO.md) — plugin atlas
- [`claude-code-skeleton/plugins/hookify/MACRO.md`](claude-code-skeleton/plugins/hookify/MACRO.md) — best reference for hook authoring
- [`claude-code-skeleton/plugins/feature-dev/MACRO.md`](claude-code-skeleton/plugins/feature-dev/MACRO.md) — best reference for multi-agent commands
- [`claude-code-skeleton/plugins/ralph-wiggum/MACRO.md`](claude-code-skeleton/plugins/ralph-wiggum/MACRO.md) — Stop hook / loop-until-done pattern

## License

[`LICENSE`](LICENSE) applies to this workspace. Upstream `claude-code/` remains under its own license.
