---
matching:
  paths:
  - examples/settings/README.md
  - examples/settings/settings-bash-sandbox.json
  - examples/settings/settings-lax.json
  - examples/settings/settings-strict.json
---

# `examples/settings/`

**Role:** **Example JSON settings** for org-wide or strict deployments: lax vs strict permission posture, bash sandboxing, marketplace restrictions (see upstream README table).

| Upstream file | Macro meaning |
|---------------|----------------|
| `README.md` | Explains the matrix of guarantees across the three JSON files and links to official settings docs. |
| `settings-lax.json` | Stricter than default in some enterprise dimensions (e.g. marketplaces); compare table in README. |
| `settings-strict.json` | Heavier lockdown: hooks, web tools, bash approval, etc. |
| `settings-bash-sandbox.json` | Emphasizes **Bash sandbox** requirements. |

**Audience:** Security/platform teams drafting `managed-settings` style policies.

**Upstream:** [`../../../claude-code/examples/settings/`](../../../claude-code/examples/settings/). Official reference: [Settings](https://code.claude.com/docs/en/settings).

**Neighbors:** [Examples root](../MACRO.md).
