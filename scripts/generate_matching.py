#!/usr/bin/env python3
"""
Regenerate ../MATCHING.md from YAML frontmatter in MACRO.md files.

Usage (from directory that contains both claude-code-skeleton/ and claude-code/):

  pip install -r claude-code-skeleton/scripts/requirements-matching.txt
  python3 claude-code-skeleton/scripts/generate_matching.py

First-time / refresh path lists from directory ownership heuristic:

  python3 claude-code-skeleton/scripts/generate_matching.py --seed

Frontmatter on every MACRO.md (after --seed or hand-written):

---
matching:
  paths:
    - plugins/foo/README.md   # upstream paths relative to claude-code/
---

Prompt *.md under **/commands/ and **/agents/ must NOT appear here; they are 1:1 via *.macro.md only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

SKIP_TOP = {".git", ".vscode"}

FRONTMATTER_PATTERN = re.compile(
    r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL
)


def workspace_roots() -> tuple[Path, Path, Path]:
    workspace = Path(__file__).resolve().parent.parent.parent
    skel = workspace / "claude-code-skeleton"
    up = workspace / "claude-code"
    return workspace, skel, up


def skip_path(parts: tuple[str, ...]) -> bool:
    return bool(parts) and parts[0] in SKIP_TOP


def is_paired_prompt(rel: Path) -> bool:
    if rel.suffix != ".md":
        return False
    p = rel.parts
    return len(p) >= 2 and p[-2] in ("commands", "agents")


def owner_macro_for(skel: Path, rel_file: Path) -> Path | None:
    parent_parts = rel_file.parent.parts
    for depth in range(len(parent_parts), -1, -1):
        prefix = Path(*parent_parts[:depth]) if depth else Path(".")
        if (skel / prefix / "MACRO.md").is_file():
            return prefix
    return None


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    m = FRONTMATTER_PATTERN.match(text)
    if not m:
        return None, text
    raw, body = m.group(1), m.group(2)
    if yaml is None:
        raise RuntimeError("Install PyYAML: pip install -r claude-code-skeleton/scripts/requirements-matching.txt")
    meta = yaml.safe_load(raw) or {}
    if not isinstance(meta, dict):
        raise ValueError("YAML frontmatter must map to an object at root")
    return meta, body


def ensure_matching_block(meta: dict) -> dict:
    m = meta.get("matching")
    if m is None:
        raise ValueError("MACRO.md must include a `matching:` key in YAML frontmatter")
    if not isinstance(m, dict):
        raise ValueError("`matching` must be a mapping")
    paths = m.get("paths")
    if paths is None:
        raise ValueError("`matching.paths` is required (use [] if no upstream files)")
    if not isinstance(paths, list) or not all(isinstance(x, str) for x in paths):
        raise ValueError("`matching.paths` must be a list of strings")
    return m


def default_assignments(skel: Path, up: Path) -> dict[str, list[str]]:
    all_files: list[Path] = []
    for p in sorted(up.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(up)
        if skip_path(rel.parts):
            continue
        all_files.append(rel)

    assignments: dict[str, list[str]] = {}
    for rel in all_files:
        if is_paired_prompt(rel):
            continue
        own = owner_macro_for(skel, rel)
        if own is None:
            continue
        key = own.as_posix() if str(own) != "." else "."
        assignments.setdefault(key, []).append(rel.as_posix())
    for k in assignments:
        assignments[k].sort()
    return assignments


def seed_frontmatter(skel: Path, up: Path) -> None:
    if yaml is None:
        sys.exit("Install PyYAML first: pip install -r claude-code-skeleton/scripts/requirements-matching.txt")

    assignments = default_assignments(skel, up)
    macro_files = sorted(p for p in skel.rglob("MACRO.md") if ".git" not in p.relative_to(skel).parts)

    for mpath in macro_files:
        rel_dir = mpath.parent.relative_to(skel)
        key = rel_dir.as_posix() if str(rel_dir) != "." else "."
        paths = assignments.get(key, [])

        text = mpath.read_text(encoding="utf-8")
        meta, body = split_frontmatter(text)
        if meta is None:
            body = text.lstrip("\ufeff")

        new_meta = {"matching": {"paths": paths}}
        header = yaml.safe_dump(new_meta, default_flow_style=False, sort_keys=False, allow_unicode=True).strip()
        new_text = f"---\n{header}\n---\n\n{body.lstrip()}"

        mpath.write_text(new_text, encoding="utf-8")
        print(f"seed {mpath.relative_to(skel)}  ({len(paths)} paths)")


def collect_macro_paths(skel: Path, up: Path) -> dict[str, list[str]]:
    macro_files = sorted(p for p in skel.rglob("MACRO.md") if ".git" not in p.relative_to(skel).parts)
    out: dict[str, list[str]] = {}
    claimed: dict[str, str] = {}  # upstream path -> skeleton macro path

    for mpath in macro_files:
        skel_key = mpath.relative_to(skel).as_posix()
        text = mpath.read_text(encoding="utf-8")
        try:
            meta, _ = split_frontmatter(text)
        except RuntimeError as e:
            sys.exit(str(e))
        if meta is None:
            sys.exit(
                f"Missing YAML frontmatter in {skel_key}. "
                f"Run: python3 claude-code-skeleton/scripts/generate_matching.py --seed"
            )
        m = ensure_matching_block(meta)
        paths = list(m["paths"])
        out[skel_key] = paths

        for p in paths:
            norm = p.replace("\\", "/").lstrip("/")
            if norm in claimed and claimed[norm] != skel_key:
                sys.exit(
                    f"Duplicate upstream path `{norm}` claimed by\n"
                    f"  - {claimed[norm]}\n"
                    f"  - {skel_key}"
                )
            claimed[norm] = skel_key
            if not (up / norm).is_file():
                sys.exit(f"Upstream file missing for `{norm}` referenced from `{skel_key}`")

    return out


def build_matching(skel: Path, up: Path) -> None:
    macro_paths = collect_macro_paths(skel, up)

    macro_md = sorted(
        p for p in skel.rglob("*.macro.md") if ".git" not in p.relative_to(skel).parts
    )

    lines: list[str] = []
    lines.append("# MATCHING: skeleton ↔ upstream `claude-code`\n\n")
    lines.append(
        "Maps each **skeleton** doc to **upstream** files in "
        "[`../claude-code/`](../claude-code/).\n\n"
    )
    lines.append(
        "> **Generated** by "
        "`python3 claude-code-skeleton/scripts/generate_matching.py`  \n"
        "> (from the parent folder of both `claude-code-skeleton/` and `claude-code/`).  \n"
        "> Source of truth: YAML `matching.paths` in each **`MACRO.md`** frontmatter.  \n"
        "> Dependencies: `python3 -m pip install -r claude-code-skeleton/scripts/requirements-matching.txt`  \n\n"
    )
    lines.append("## Rules\n\n")
    lines.append(
        "1. **`MACRO.md`** — YAML frontmatter (skill-style `---` block) with **`matching.paths`**: "
        "list of upstream files (repo-root-relative). **`commands/`** / **`agents/`** prompt `*.md` "
        "must appear only in **§1:1**.\n"
    )
    lines.append(
        "2. **`*.macro.md`** — **1:1** with upstream **`*.md`** at the same path "
        "(basename without `.macro`).\n"
    )
    lines.append(
        "3. **No duplicate** upstream paths across `MACRO.md` files (enforced by the generator).\n"
    )
    lines.append(
        "4. Paths are relative to repo roots: `claude-code-skeleton/` vs `claude-code/`.\n"
    )
    lines.append(
        "5. **Skeleton-only** files (`MATCHING.md`, `generate_matching.py`, …) are **not** listed.\n"
    )

    lines.append("\n## 1:1 — `*.macro.md` → upstream `*.md`\n\n")
    lines.append("| Skeleton | Upstream |\n|----------|----------|\n")
    for p in macro_md:
        rel = p.relative_to(skel)
        stem = p.name.removesuffix(".macro.md") + ".md"
        upstream_rel = rel.with_name(stem)
        ok = "✓" if (up / upstream_rel).is_file() else "✗"
        lines.append(f"| `{rel.as_posix()}` | `{upstream_rel.as_posix()}` {ok} |\n")

    lines.append("\n## 1:many — `MACRO.md` → upstream files (from YAML)\n\n")
    lines.append("Prompt markdown under `**/commands/` and `**/agents/**` is **omitted**; see **§1:1**.\n\n")

    for skel_macro in sorted(macro_paths.keys(), key=lambda s: (s != "MACRO.md", s)):
        paths = macro_paths[skel_macro]
        lines.append(f"### `{skel_macro}`\n\n")
        lines.append(f"**Files ({len(paths)}):**\n\n")
        for f in paths:
            lines.append(f"- `{f}`\n")
        lines.append("\n")

    (skel / "MATCHING.md").write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {skel / 'MATCHING.md'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate MATCHING.md from MACRO.md YAML frontmatter")
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Inject / refresh matching.paths in all MACRO.md (from directory ownership heuristic)",
    )
    args = parser.parse_args()

    _, skel, up = workspace_roots()
    if not skel.is_dir() or not up.is_dir():
        sys.exit(f"Expected {skel} and {up} to exist")

    if args.seed:
        seed_frontmatter(skel, up)
    build_matching(skel, up)


if __name__ == "__main__":
    main()
