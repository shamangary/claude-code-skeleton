---
matching:
  paths:
  - examples/hooks/bash_command_validator_example.py
---

# `examples/hooks/`

**Role:** **Runnable hook samples** showing how to implement `PreToolUse` (and similar) logic in Python.

| Upstream file | Macro meaning |
|---------------|----------------|
| `bash_command_validator_example.py` | **PreToolUse** on `Bash`: validates/transforms shell before execution (example: steering `grep` toward `rg`). Docstring includes a **copy-paste `hooks.json` fragment**. |

**Audience:** Anyone authoring custom hooks without starting from zero.

**Upstream:** [`../../../claude-code/examples/hooks/`](../../../claude-code/examples/hooks/). Docs: [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks).

**Neighbors:** [Examples root](../MACRO.md).
