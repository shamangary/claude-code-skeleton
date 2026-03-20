# MATCHING: skeleton ↔ upstream `claude-code`

Maps each **skeleton** doc to **upstream** files in [`../claude-code/`](../claude-code/).

> **Generated** by `python3 claude-code-skeleton/scripts/generate_matching.py`  
> (from the parent folder of both `claude-code-skeleton/` and `claude-code/`).  
> Source of truth: YAML `matching.paths` in each **`MACRO.md`** frontmatter.  
> Dependencies: `python3 -m pip install -r claude-code-skeleton/scripts/requirements-matching.txt`  

## Rules

1. **`MACRO.md`** — YAML frontmatter (skill-style `---` block) with **`matching.paths`**: list of upstream files (repo-root-relative). **`commands/`** / **`agents/`** prompt `*.md` must appear only in **§1:1**.
2. **`*.macro.md`** — **1:1** with upstream **`*.md`** at the same path (basename without `.macro`).
3. **No duplicate** upstream paths across `MACRO.md` files (enforced by the generator).
4. Paths are relative to repo roots: `claude-code-skeleton/` vs `claude-code/`.
5. **Skeleton-only** files (`MATCHING.md`, `generate_matching.py`, …) are **not** listed.

## 1:1 — `*.macro.md` → upstream `*.md`

| Skeleton | Upstream |
|----------|----------|
| `.claude/commands/commit-push-pr.macro.md` | `.claude/commands/commit-push-pr.md` ✓ |
| `.claude/commands/dedupe.macro.md` | `.claude/commands/dedupe.md` ✓ |
| `.claude/commands/triage-issue.macro.md` | `.claude/commands/triage-issue.md` ✓ |
| `plugins/agent-sdk-dev/agents/agent-sdk-verifier-py.macro.md` | `plugins/agent-sdk-dev/agents/agent-sdk-verifier-py.md` ✓ |
| `plugins/agent-sdk-dev/agents/agent-sdk-verifier-ts.macro.md` | `plugins/agent-sdk-dev/agents/agent-sdk-verifier-ts.md` ✓ |
| `plugins/agent-sdk-dev/commands/new-sdk-app.macro.md` | `plugins/agent-sdk-dev/commands/new-sdk-app.md` ✓ |
| `plugins/code-review/commands/code-review.macro.md` | `plugins/code-review/commands/code-review.md` ✓ |
| `plugins/commit-commands/commands/clean_gone.macro.md` | `plugins/commit-commands/commands/clean_gone.md` ✓ |
| `plugins/commit-commands/commands/commit-push-pr.macro.md` | `plugins/commit-commands/commands/commit-push-pr.md` ✓ |
| `plugins/commit-commands/commands/commit.macro.md` | `plugins/commit-commands/commands/commit.md` ✓ |
| `plugins/feature-dev/agents/code-architect.macro.md` | `plugins/feature-dev/agents/code-architect.md` ✓ |
| `plugins/feature-dev/agents/code-explorer.macro.md` | `plugins/feature-dev/agents/code-explorer.md` ✓ |
| `plugins/feature-dev/agents/code-reviewer.macro.md` | `plugins/feature-dev/agents/code-reviewer.md` ✓ |
| `plugins/feature-dev/commands/feature-dev.macro.md` | `plugins/feature-dev/commands/feature-dev.md` ✓ |
| `plugins/hookify/agents/conversation-analyzer.macro.md` | `plugins/hookify/agents/conversation-analyzer.md` ✓ |
| `plugins/hookify/commands/configure.macro.md` | `plugins/hookify/commands/configure.md` ✓ |
| `plugins/hookify/commands/help.macro.md` | `plugins/hookify/commands/help.md` ✓ |
| `plugins/hookify/commands/hookify.macro.md` | `plugins/hookify/commands/hookify.md` ✓ |
| `plugins/hookify/commands/list.macro.md` | `plugins/hookify/commands/list.md` ✓ |
| `plugins/plugin-dev/agents/agent-creator.macro.md` | `plugins/plugin-dev/agents/agent-creator.md` ✓ |
| `plugins/plugin-dev/agents/plugin-validator.macro.md` | `plugins/plugin-dev/agents/plugin-validator.md` ✓ |
| `plugins/plugin-dev/agents/skill-reviewer.macro.md` | `plugins/plugin-dev/agents/skill-reviewer.md` ✓ |
| `plugins/plugin-dev/commands/create-plugin.macro.md` | `plugins/plugin-dev/commands/create-plugin.md` ✓ |
| `plugins/pr-review-toolkit/agents/code-reviewer.macro.md` | `plugins/pr-review-toolkit/agents/code-reviewer.md` ✓ |
| `plugins/pr-review-toolkit/agents/code-simplifier.macro.md` | `plugins/pr-review-toolkit/agents/code-simplifier.md` ✓ |
| `plugins/pr-review-toolkit/agents/comment-analyzer.macro.md` | `plugins/pr-review-toolkit/agents/comment-analyzer.md` ✓ |
| `plugins/pr-review-toolkit/agents/pr-test-analyzer.macro.md` | `plugins/pr-review-toolkit/agents/pr-test-analyzer.md` ✓ |
| `plugins/pr-review-toolkit/agents/silent-failure-hunter.macro.md` | `plugins/pr-review-toolkit/agents/silent-failure-hunter.md` ✓ |
| `plugins/pr-review-toolkit/agents/type-design-analyzer.macro.md` | `plugins/pr-review-toolkit/agents/type-design-analyzer.md` ✓ |
| `plugins/pr-review-toolkit/commands/review-pr.macro.md` | `plugins/pr-review-toolkit/commands/review-pr.md` ✓ |
| `plugins/ralph-wiggum/commands/cancel-ralph.macro.md` | `plugins/ralph-wiggum/commands/cancel-ralph.md` ✓ |
| `plugins/ralph-wiggum/commands/help.macro.md` | `plugins/ralph-wiggum/commands/help.md` ✓ |
| `plugins/ralph-wiggum/commands/ralph-loop.macro.md` | `plugins/ralph-wiggum/commands/ralph-loop.md` ✓ |

## 1:many — `MACRO.md` → upstream files (from YAML)

Prompt markdown under `**/commands/` and `**/agents/**` is **omitted**; see **§1:1**.

### `MACRO.md`

**Files (6):**

- `.gitattributes`
- `.gitignore`
- `CHANGELOG.md`
- `LICENSE.md`
- `README.md`
- `SECURITY.md`

### `.claude-plugin/MACRO.md`

**Files (1):**

- `.claude-plugin/marketplace.json`

### `.claude/MACRO.md`

**Files (0):**


### `.devcontainer/MACRO.md`

**Files (3):**

- `.devcontainer/Dockerfile`
- `.devcontainer/devcontainer.json`
- `.devcontainer/init-firewall.sh`

### `.github/ISSUE_TEMPLATE/MACRO.md`

**Files (5):**

- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/ISSUE_TEMPLATE/documentation.yml`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/ISSUE_TEMPLATE/model_behavior.yml`

### `.github/MACRO.md`

**Files (0):**


### `.github/workflow-macros/MACRO.md`

**Files (12):**

- `.github/workflows/auto-close-duplicates.yml`
- `.github/workflows/backfill-duplicate-comments.yml`
- `.github/workflows/claude-dedupe-issues.yml`
- `.github/workflows/claude-issue-triage.yml`
- `.github/workflows/claude.yml`
- `.github/workflows/issue-lifecycle-comment.yml`
- `.github/workflows/issue-opened-dispatch.yml`
- `.github/workflows/lock-closed-issues.yml`
- `.github/workflows/log-issue-events.yml`
- `.github/workflows/non-write-users-check.yml`
- `.github/workflows/remove-autoclose-label.yml`
- `.github/workflows/sweep.yml`

### `Script/MACRO.md`

**Files (1):**

- `Script/run_devcontainer_claude_code.ps1`

### `examples/MACRO.md`

**Files (0):**


### `examples/hooks/MACRO.md`

**Files (1):**

- `examples/hooks/bash_command_validator_example.py`

### `examples/settings/MACRO.md`

**Files (4):**

- `examples/settings/README.md`
- `examples/settings/settings-bash-sandbox.json`
- `examples/settings/settings-lax.json`
- `examples/settings/settings-strict.json`

### `plugins/MACRO.md`

**Files (1):**

- `plugins/README.md`

### `plugins/agent-sdk-dev/.claude-plugin/MACRO.md`

**Files (1):**

- `plugins/agent-sdk-dev/.claude-plugin/plugin.json`

### `plugins/agent-sdk-dev/MACRO.md`

**Files (1):**

- `plugins/agent-sdk-dev/README.md`

### `plugins/claude-opus-4-5-migration/.claude-plugin/MACRO.md`

**Files (1):**

- `plugins/claude-opus-4-5-migration/.claude-plugin/plugin.json`

### `plugins/claude-opus-4-5-migration/MACRO.md`

**Files (1):**

- `plugins/claude-opus-4-5-migration/README.md`

### `plugins/claude-opus-4-5-migration/skills/MACRO.md`

**Files (0):**


### `plugins/claude-opus-4-5-migration/skills/claude-opus-4-5-migration/MACRO.md`

**Files (1):**

- `plugins/claude-opus-4-5-migration/skills/claude-opus-4-5-migration/SKILL.md`

### `plugins/claude-opus-4-5-migration/skills/claude-opus-4-5-migration/references/MACRO.md`

**Files (2):**

- `plugins/claude-opus-4-5-migration/skills/claude-opus-4-5-migration/references/effort.md`
- `plugins/claude-opus-4-5-migration/skills/claude-opus-4-5-migration/references/prompt-snippets.md`

### `plugins/code-review/.claude-plugin/MACRO.md`

**Files (1):**

- `plugins/code-review/.claude-plugin/plugin.json`

### `plugins/code-review/MACRO.md`

**Files (1):**

- `plugins/code-review/README.md`

### `plugins/commit-commands/.claude-plugin/MACRO.md`

**Files (1):**

- `plugins/commit-commands/.claude-plugin/plugin.json`

### `plugins/commit-commands/MACRO.md`

**Files (1):**

- `plugins/commit-commands/README.md`

### `plugins/explanatory-output-style/.claude-plugin/MACRO.md`

**Files (1):**

- `plugins/explanatory-output-style/.claude-plugin/plugin.json`

### `plugins/explanatory-output-style/MACRO.md`

**Files (1):**

- `plugins/explanatory-output-style/README.md`

### `plugins/explanatory-output-style/hooks-handlers/MACRO.md`

**Files (1):**

- `plugins/explanatory-output-style/hooks-handlers/session-start.sh`

### `plugins/explanatory-output-style/hooks/MACRO.md`

**Files (1):**

- `plugins/explanatory-output-style/hooks/hooks.json`

### `plugins/feature-dev/.claude-plugin/MACRO.md`

**Files (1):**

- `plugins/feature-dev/.claude-plugin/plugin.json`

### `plugins/feature-dev/MACRO.md`

**Files (1):**

- `plugins/feature-dev/README.md`

### `plugins/frontend-design/.claude-plugin/MACRO.md`

**Files (1):**

- `plugins/frontend-design/.claude-plugin/plugin.json`

### `plugins/frontend-design/MACRO.md`

**Files (1):**

- `plugins/frontend-design/README.md`

### `plugins/frontend-design/skills/MACRO.md`

**Files (0):**


### `plugins/frontend-design/skills/frontend-design/MACRO.md`

**Files (1):**

- `plugins/frontend-design/skills/frontend-design/SKILL.md`

### `plugins/hookify/.claude-plugin/MACRO.md`

**Files (1):**

- `plugins/hookify/.claude-plugin/plugin.json`

### `plugins/hookify/MACRO.md`

**Files (2):**

- `plugins/hookify/.gitignore`
- `plugins/hookify/README.md`

### `plugins/hookify/core/MACRO.md`

**Files (3):**

- `plugins/hookify/core/__init__.py`
- `plugins/hookify/core/config_loader.py`
- `plugins/hookify/core/rule_engine.py`

### `plugins/hookify/examples/MACRO.md`

**Files (4):**

- `plugins/hookify/examples/console-log-warning.local.md`
- `plugins/hookify/examples/dangerous-rm.local.md`
- `plugins/hookify/examples/require-tests-stop.local.md`
- `plugins/hookify/examples/sensitive-files-warning.local.md`

### `plugins/hookify/hooks/MACRO.md`

**Files (6):**

- `plugins/hookify/hooks/__init__.py`
- `plugins/hookify/hooks/hooks.json`
- `plugins/hookify/hooks/posttooluse.py`
- `plugins/hookify/hooks/pretooluse.py`
- `plugins/hookify/hooks/stop.py`
- `plugins/hookify/hooks/userpromptsubmit.py`

### `plugins/hookify/matchers/MACRO.md`

**Files (1):**

- `plugins/hookify/matchers/__init__.py`

### `plugins/hookify/skills/MACRO.md`

**Files (0):**


### `plugins/hookify/skills/writing-rules/MACRO.md`

**Files (1):**

- `plugins/hookify/skills/writing-rules/SKILL.md`

### `plugins/hookify/utils/MACRO.md`

**Files (1):**

- `plugins/hookify/utils/__init__.py`

### `plugins/learning-output-style/.claude-plugin/MACRO.md`

**Files (1):**

- `plugins/learning-output-style/.claude-plugin/plugin.json`

### `plugins/learning-output-style/MACRO.md`

**Files (1):**

- `plugins/learning-output-style/README.md`

### `plugins/learning-output-style/hooks-handlers/MACRO.md`

**Files (1):**

- `plugins/learning-output-style/hooks-handlers/session-start.sh`

### `plugins/learning-output-style/hooks/MACRO.md`

**Files (1):**

- `plugins/learning-output-style/hooks/hooks.json`

### `plugins/plugin-dev/MACRO.md`

**Files (1):**

- `plugins/plugin-dev/README.md`

### `plugins/plugin-dev/skills/MACRO.md`

**Files (0):**


### `plugins/plugin-dev/skills/agent-development/MACRO.md`

**Files (1):**

- `plugins/plugin-dev/skills/agent-development/SKILL.md`

### `plugins/plugin-dev/skills/agent-development/examples/MACRO.md`

**Files (2):**

- `plugins/plugin-dev/skills/agent-development/examples/agent-creation-prompt.md`
- `plugins/plugin-dev/skills/agent-development/examples/complete-agent-examples.md`

### `plugins/plugin-dev/skills/agent-development/references/MACRO.md`

**Files (3):**

- `plugins/plugin-dev/skills/agent-development/references/agent-creation-system-prompt.md`
- `plugins/plugin-dev/skills/agent-development/references/system-prompt-design.md`
- `plugins/plugin-dev/skills/agent-development/references/triggering-examples.md`

### `plugins/plugin-dev/skills/agent-development/scripts/MACRO.md`

**Files (1):**

- `plugins/plugin-dev/skills/agent-development/scripts/validate-agent.sh`

### `plugins/plugin-dev/skills/command-development/MACRO.md`

**Files (2):**

- `plugins/plugin-dev/skills/command-development/README.md`
- `plugins/plugin-dev/skills/command-development/SKILL.md`

### `plugins/plugin-dev/skills/command-development/examples/MACRO.md`

**Files (2):**

- `plugins/plugin-dev/skills/command-development/examples/plugin-commands.md`
- `plugins/plugin-dev/skills/command-development/examples/simple-commands.md`

### `plugins/plugin-dev/skills/command-development/references/MACRO.md`

**Files (7):**

- `plugins/plugin-dev/skills/command-development/references/advanced-workflows.md`
- `plugins/plugin-dev/skills/command-development/references/documentation-patterns.md`
- `plugins/plugin-dev/skills/command-development/references/frontmatter-reference.md`
- `plugins/plugin-dev/skills/command-development/references/interactive-commands.md`
- `plugins/plugin-dev/skills/command-development/references/marketplace-considerations.md`
- `plugins/plugin-dev/skills/command-development/references/plugin-features-reference.md`
- `plugins/plugin-dev/skills/command-development/references/testing-strategies.md`

### `plugins/plugin-dev/skills/hook-development/MACRO.md`

**Files (1):**

- `plugins/plugin-dev/skills/hook-development/SKILL.md`

### `plugins/plugin-dev/skills/hook-development/examples/MACRO.md`

**Files (3):**

- `plugins/plugin-dev/skills/hook-development/examples/load-context.sh`
- `plugins/plugin-dev/skills/hook-development/examples/validate-bash.sh`
- `plugins/plugin-dev/skills/hook-development/examples/validate-write.sh`

### `plugins/plugin-dev/skills/hook-development/references/MACRO.md`

**Files (3):**

- `plugins/plugin-dev/skills/hook-development/references/advanced.md`
- `plugins/plugin-dev/skills/hook-development/references/migration.md`
- `plugins/plugin-dev/skills/hook-development/references/patterns.md`

### `plugins/plugin-dev/skills/hook-development/scripts/MACRO.md`

**Files (4):**

- `plugins/plugin-dev/skills/hook-development/scripts/README.md`
- `plugins/plugin-dev/skills/hook-development/scripts/hook-linter.sh`
- `plugins/plugin-dev/skills/hook-development/scripts/test-hook.sh`
- `plugins/plugin-dev/skills/hook-development/scripts/validate-hook-schema.sh`

### `plugins/plugin-dev/skills/mcp-integration/MACRO.md`

**Files (1):**

- `plugins/plugin-dev/skills/mcp-integration/SKILL.md`

### `plugins/plugin-dev/skills/mcp-integration/examples/MACRO.md`

**Files (3):**

- `plugins/plugin-dev/skills/mcp-integration/examples/http-server.json`
- `plugins/plugin-dev/skills/mcp-integration/examples/sse-server.json`
- `plugins/plugin-dev/skills/mcp-integration/examples/stdio-server.json`

### `plugins/plugin-dev/skills/mcp-integration/references/MACRO.md`

**Files (3):**

- `plugins/plugin-dev/skills/mcp-integration/references/authentication.md`
- `plugins/plugin-dev/skills/mcp-integration/references/server-types.md`
- `plugins/plugin-dev/skills/mcp-integration/references/tool-usage.md`

### `plugins/plugin-dev/skills/plugin-settings/MACRO.md`

**Files (1):**

- `plugins/plugin-dev/skills/plugin-settings/SKILL.md`

### `plugins/plugin-dev/skills/plugin-settings/examples/MACRO.md`

**Files (3):**

- `plugins/plugin-dev/skills/plugin-settings/examples/create-settings-command.md`
- `plugins/plugin-dev/skills/plugin-settings/examples/example-settings.md`
- `plugins/plugin-dev/skills/plugin-settings/examples/read-settings-hook.sh`

### `plugins/plugin-dev/skills/plugin-settings/references/MACRO.md`

**Files (2):**

- `plugins/plugin-dev/skills/plugin-settings/references/parsing-techniques.md`
- `plugins/plugin-dev/skills/plugin-settings/references/real-world-examples.md`

### `plugins/plugin-dev/skills/plugin-settings/scripts/MACRO.md`

**Files (2):**

- `plugins/plugin-dev/skills/plugin-settings/scripts/parse-frontmatter.sh`
- `plugins/plugin-dev/skills/plugin-settings/scripts/validate-settings.sh`

### `plugins/plugin-dev/skills/plugin-structure/MACRO.md`

**Files (2):**

- `plugins/plugin-dev/skills/plugin-structure/README.md`
- `plugins/plugin-dev/skills/plugin-structure/SKILL.md`

### `plugins/plugin-dev/skills/plugin-structure/examples/MACRO.md`

**Files (3):**

- `plugins/plugin-dev/skills/plugin-structure/examples/advanced-plugin.md`
- `plugins/plugin-dev/skills/plugin-structure/examples/minimal-plugin.md`
- `plugins/plugin-dev/skills/plugin-structure/examples/standard-plugin.md`

### `plugins/plugin-dev/skills/plugin-structure/references/MACRO.md`

**Files (2):**

- `plugins/plugin-dev/skills/plugin-structure/references/component-patterns.md`
- `plugins/plugin-dev/skills/plugin-structure/references/manifest-reference.md`

### `plugins/plugin-dev/skills/skill-development/MACRO.md`

**Files (1):**

- `plugins/plugin-dev/skills/skill-development/SKILL.md`

### `plugins/plugin-dev/skills/skill-development/references/MACRO.md`

**Files (1):**

- `plugins/plugin-dev/skills/skill-development/references/skill-creator-original.md`

### `plugins/pr-review-toolkit/.claude-plugin/MACRO.md`

**Files (1):**

- `plugins/pr-review-toolkit/.claude-plugin/plugin.json`

### `plugins/pr-review-toolkit/MACRO.md`

**Files (1):**

- `plugins/pr-review-toolkit/README.md`

### `plugins/ralph-wiggum/.claude-plugin/MACRO.md`

**Files (1):**

- `plugins/ralph-wiggum/.claude-plugin/plugin.json`

### `plugins/ralph-wiggum/MACRO.md`

**Files (1):**

- `plugins/ralph-wiggum/README.md`

### `plugins/ralph-wiggum/hooks/MACRO.md`

**Files (2):**

- `plugins/ralph-wiggum/hooks/hooks.json`
- `plugins/ralph-wiggum/hooks/stop-hook.sh`

### `plugins/ralph-wiggum/scripts/MACRO.md`

**Files (1):**

- `plugins/ralph-wiggum/scripts/setup-ralph-loop.sh`

### `plugins/security-guidance/.claude-plugin/MACRO.md`

**Files (1):**

- `plugins/security-guidance/.claude-plugin/plugin.json`

### `plugins/security-guidance/MACRO.md`

**Files (0):**


### `plugins/security-guidance/hooks/MACRO.md`

**Files (2):**

- `plugins/security-guidance/hooks/hooks.json`
- `plugins/security-guidance/hooks/security_reminder_hook.py`

### `scripts/MACRO.md`

**Files (8):**

- `scripts/auto-close-duplicates.ts`
- `scripts/backfill-duplicate-comments.ts`
- `scripts/comment-on-duplicates.sh`
- `scripts/edit-issue-labels.sh`
- `scripts/gh.sh`
- `scripts/issue-lifecycle.ts`
- `scripts/lifecycle-comment.ts`
- `scripts/sweep.ts`

