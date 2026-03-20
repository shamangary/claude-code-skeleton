---
matching:
  paths:
  - .devcontainer/Dockerfile
  - .devcontainer/devcontainer.json
  - .devcontainer/init-firewall.sh
---

# `.devcontainer/` (containerized dev)

**Role:** **VS Code / Dev Container** definition so contributors can develop in a **reproducible Linux environment** with Dockerfile + `devcontainer.json`, plus an **init firewall** helper script.

| Upstream file (cluster) | Macro meaning |
|---------------------------|----------------|
| `devcontainer.json` | Dev container metadata (features, mounts, lifecycle). |
| `Dockerfile` | Image build for the dev environment. |
| `init-firewall.sh` | Setup script referenced by container initialization. |

**Audience:** Contributors using “Reopen in Container” (and **`Script/run_devcontainer_claude_code.ps1`** on Windows—see [`../Script/MACRO.md`](../Script/MACRO.md)).

**Upstream:** [`../../claude-code/.devcontainer/`](../../claude-code/.devcontainer/)

**Neighbors:** [`../Script/MACRO.md`](../Script/MACRO.md).
