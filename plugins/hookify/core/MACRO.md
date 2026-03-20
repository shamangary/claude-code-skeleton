---
matching:
  paths:
  - plugins/hookify/core/__init__.py
  - plugins/hookify/core/config_loader.py
  - plugins/hookify/core/rule_engine.py
---

# Package: `hookify/core`

**Role:** **Python library code** for Hookify—loads configuration, parses rule documents, and runs the **rule engine** that decides hook outcomes.

| Upstream file (cluster) | Macro meaning |
|-------------------------|----------------|
| `config_loader.py` | Finds and loads user/org rule configuration. |
| `rule_engine.py` | Evaluates rules against hook payloads. |
| `__init__.py` | Package surface. |

**Audience:** Maintainers extending Hookify semantics.

**Neighbors:** [`../hooks/MACRO.md`](../hooks/MACRO.md); [`../matchers/MACRO.md`](../matchers/MACRO.md).
