---
matching:
  paths:
  - README.md
  - CHANGELOG.md
  - LICENSE.md
  - SECURITY.md
---

# Claude Code — top-level docs

These four files are the entry point for anyone landing on the upstream repository.

**README.md** is the primary user-facing guide: installation, quick start, feature overview, and links to deeper docs. If something is user-visible it starts here.

**CHANGELOG.md** tracks every release with breaking changes, new features, and fixes. Check this first when upgrading or debugging unexpected behaviour after a version bump.

**LICENSE.md** defines the terms under which Claude Code is distributed. The skeleton and any plugins you build are covered by your own `LICENSE` at the workspace root — these are separate.

**SECURITY.md** explains the responsible disclosure policy for vulnerabilities. Not relevant to day-to-day development but important if you find a bug with security implications.
