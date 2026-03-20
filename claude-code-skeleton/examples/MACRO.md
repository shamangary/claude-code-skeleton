---
matching:
  paths:
  - examples/hooks/bash_command_validator_example.py
  - examples/settings/README.md
  - examples/settings/settings-bash-sandbox.json
  - examples/settings/settings-lax.json
  - examples/settings/settings-strict.json
---

# `examples/` (upstream)

**Role:** **Reference materials** for Claude Code operators: sample **hook** implementations and **managed settings** JSON presets—not loaded as plugins.

**Hook examples** (`hooks/`): Runnable Python samples showing how to implement `PreToolUse` (and similar) logic—e.g. `bash_command_validator_example.py` validates/transforms shell commands before execution and includes a copy-paste `hooks.json` fragment.

**Settings examples** (`settings/`): Example JSON settings for org-wide deployments covering lax vs strict permission postures and bash sandboxing. The README explains the matrix of guarantees across the three JSON files.

**Audience:** Admins and advanced users copying hook patterns into their own `hooks/` config, and security/platform teams drafting `managed-settings` style policies.

**Upstream:** [`../../claude-code/examples/`](../../claude-code/examples/)

**Stability:** Examples only; paths in snippets (e.g. `/path/to/...`) must be edited before use.
