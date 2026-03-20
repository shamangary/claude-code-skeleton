---
matching:
  paths:
  - plugins/plugin-dev/skills/plugin-settings/SKILL.md
---

# Skill: `plugin-settings`

**Role:** Patterns for **per-plugin settings** via `.claude/plugin-name.local.md` (frontmatter + body), parsing approaches, and validation scripts.

**Contents:**

| Subfolder | Macro meaning |
|-----------|----------------|
| `SKILL.md` | Entry + when to use local markdown settings vs env vars. |
| `references/` | Parsing techniques and real-world examples (**cluster**). |
| `examples/` | Sample settings files + command docs showing reads. |
| `scripts/` | `parse-frontmatter.sh`, `validate-settings.sh` helpers. |

**Neighbors:** [Skills catalog](../MACRO.md).
