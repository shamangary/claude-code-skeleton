---
matching:
  paths:
  - .claude-plugin/marketplace.json
---

# Root manifest: `.claude-plugin/marketplace.json`

**Role:** Declares **`claude-code-plugins`**: the **bundled marketplace catalog** for this repo—lists every official plugin with `source` path, category, metadata, and schema version.

**Audience:** Claude Code when resolving **local / dev** marketplace installs; authors comparing plugin inventory to `plugins/`.

**Upstream:** [`../../claude-code/.claude-plugin/marketplace.json`](../../claude-code/.claude-plugin/marketplace.json)

**Neighbors:** [`../plugins/MACRO.md`](../plugins/MACRO.md).

**Stability:** Adding a plugin upstream should update this file and the [`plugins/`](../plugins/) tree together.
