#!/usr/bin/env python3
"""
Generate ../MATCHING.md from YAML frontmatter in claude-code-skeleton/**/MACRO.md

Layout (workspace root = parent of this matching/ directory):

  workspace/
    claude-code/              # upstream (default: clone/pull from GitHub)
    claude-code-skeleton/
    matching/
      generate_matching.py
    MATCHING.md               # written here

Usage:

  python3 -m pip install -r matching/requirements.txt
  python3 matching/generate_matching.py              # fetch upstream + regenerate
  python3 matching/generate_matching.py --no-fetch   # use existing claude-code/
  python3 matching/generate_matching.py --seed       # refresh matching.paths (then run without --seed)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

UPSTREAM_DEFAULT_REMOTE = "https://github.com/anthropics/claude-code.git"

SKIP_TOP = {".git", ".vscode"}
SKIP_ANYWHERE = {".git"}  # exclude nested .git (shouldn't exist in tree files)

FRONTMATTER_PATTERN = re.compile(
    r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL
)


def workspace_roots(script_path: Path) -> tuple[Path, Path, Path, Path]:
    """Return (workspace, claude-code, skeleton, matching_dir)."""
    matching_dir = script_path.resolve().parent
    workspace = matching_dir.parent
    return workspace, workspace / "claude-code", workspace / "claude-code-skeleton", matching_dir


def skip_path(parts: tuple[str, ...]) -> bool:
    if not parts:
        return False
    if parts[0] in SKIP_TOP:
        return True
    return any(p in SKIP_ANYWHERE for p in parts)


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
        raise RuntimeError(
            "Install PyYAML: python3 -m pip install -r matching/requirements.txt"
        )
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


def fetch_upstream(up: Path, remote: str, branch: str | None) -> list[str]:
    """Clone or pull. Returns log lines for the report."""
    log: list[str] = []
    if (up / ".git").is_dir():
        log.append(f"git repo exists: {up}")
        r = subprocess.run(
            ["git", "-C", str(up), "fetch", "origin"],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            log.append(f"git fetch warning: {r.stderr.strip() or r.stdout.strip()}")
        r2 = subprocess.run(
            ["git", "-C", str(up), "pull", "--ff-only"],
            capture_output=True,
            text=True,
        )
        if r2.returncode != 0:
            log.append(
                f"git pull --ff-only failed (resolve conflicts or use --no-fetch): "
                f"{r2.stderr.strip() or r2.stdout.strip()}"
            )
        else:
            log.append("git pull --ff-only: ok")
    else:
        if up.exists() and any(up.iterdir()):
            log.append(
                f"ERROR: `{up}` exists and is not empty but has no `.git` — "
                "remove it or clone manually, then re-run."
            )
            return log
        up.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["git", "clone", "--depth", "1"]
        if branch:
            cmd.extend(["--branch", branch])
        cmd.extend([remote, str(up)])
        log.append(f"clone: {' '.join(cmd)}")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            log.append(f"git clone failed: {r.stderr.strip() or r.stdout.strip()}")
        else:
            log.append("git clone: ok")
    return log


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
        sys.exit("Install PyYAML: python3 -m pip install -r matching/requirements.txt")

    assignments = default_assignments(skel, up)
    macro_files = sorted(
        p
        for p in skel.rglob("MACRO.md")
        if not any(part == ".git" for part in p.relative_to(skel).parts)
    )

    for mpath in macro_files:
        rel_dir = mpath.parent.relative_to(skel)
        key = rel_dir.as_posix() if str(rel_dir) != "." else "."
        paths = assignments.get(key, [])

        text = mpath.read_text(encoding="utf-8")
        meta, body = split_frontmatter(text)
        if meta is None:
            body = text.lstrip("\ufeff")

        new_meta = {"matching": {"paths": paths}}
        header = yaml.safe_dump(
            new_meta, default_flow_style=False, sort_keys=False, allow_unicode=True
        ).strip()
        new_text = f"---\n{header}\n---\n\n{body.lstrip()}"

        mpath.write_text(new_text, encoding="utf-8")
        print(f"seed {mpath.relative_to(skel)}  ({len(paths)} paths)")


@dataclass
class ValidationResult:
    macro_paths: dict[str, list[str]] = field(default_factory=dict)
    duplicate_claims: list[str] = field(default_factory=list)
    missing_upstream: list[str] = field(default_factory=list)
    yaml_errors: list[str] = field(default_factory=list)

    @property
    def fatal(self) -> bool:
        return bool(self.duplicate_claims or self.missing_upstream or self.yaml_errors)


def collect_macro_paths(skel: Path, up: Path) -> ValidationResult:
    vr = ValidationResult()
    claimed: dict[str, str] = {}

    macro_files = sorted(
        p
        for p in skel.rglob("MACRO.md")
        if not any(part == ".git" for part in p.relative_to(skel).parts)
    )
    for mpath in macro_files:
        skel_key = mpath.relative_to(skel).as_posix()
        text = mpath.read_text(encoding="utf-8")
        try:
            if yaml is None:
                vr.yaml_errors.append(f"{skel_key}: PyYAML not installed")
                continue
            meta, _ = split_frontmatter(text)
            if meta is None:
                vr.yaml_errors.append(
                    f"{skel_key}: missing YAML frontmatter (run: python3 matching/generate_matching.py --seed)"
                )
                continue
            m = ensure_matching_block(meta)
            paths = list(m["paths"])
            vr.macro_paths[skel_key] = paths

            for p in paths:
                norm = p.replace("\\", "/").lstrip("/")
                if norm in claimed and claimed[norm] != skel_key:
                    vr.duplicate_claims.append(
                        f"`{norm}` claimed by `{claimed[norm]}` and `{skel_key}`"
                    )
                elif norm in claimed:
                    pass
                else:
                    claimed[norm] = skel_key
                    if not (up / norm).is_file():
                        vr.missing_upstream.append(f"`{norm}` from `{skel_key}` — file missing in claude-code")
        except (ValueError, RuntimeError) as e:
            vr.yaml_errors.append(f"{skel_key}: {e}")

    return vr


def build_matching(
    skel: Path,
    up: Path,
    out: Path,
    fetch_log: list[str],
    vr: ValidationResult,
) -> tuple[list[str], list[str], dict[str, int]]:
    """Returns (paired_ok, paired_fail, stats)."""
    skel = skel.resolve()
    up = up.resolve()
    macro_md = sorted(
        p
        for p in skel.rglob("*.macro.md")
        if not any(part == ".git" for part in p.relative_to(skel).parts)
    )
    paired_ok: list[str] = []
    paired_fail: list[str] = []

    all_upstream: list[Path] = []
    for p in up.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(up)
        if skip_path(rel.parts):
            continue
        all_upstream.append(rel)

    claimed_from_yaml = set()
    for paths in vr.macro_paths.values():
        for p in paths:
            claimed_from_yaml.add(p.replace("\\", "/").lstrip("/"))

    claimed_1_1 = set()
    for p in macro_md:
        rel = p.relative_to(skel)
        stem = p.name.removesuffix(".macro.md") + ".md"
        upstream_rel = rel.with_name(stem)
        u = upstream_rel.as_posix()
        claimed_1_1.add(u)
        if (up / upstream_rel).is_file():
            paired_ok.append(f"| `{rel.as_posix()}` | `{u}` ✓ |")
        else:
            paired_fail.append(f"| `{rel.as_posix()}` | `{u}` ✗ |")

    implicit_covered = set()
    for rel in all_upstream:
        if is_paired_prompt(rel):
            implicit_covered.add(rel.as_posix())

    all_pos = {rel.as_posix() for rel in all_upstream}
    fully_claimed = claimed_from_yaml | claimed_1_1 | implicit_covered
    uncovered = sorted(all_pos - fully_claimed)

    lines: list[str] = []
    lines.append("# MATCHING: skeleton ↔ `claude-code/`\n\n")
    lines.append(
        "Maps **`claude-code-skeleton/`** to **`claude-code/`** (paths relative to each repo root).\n\n"
    )
    lines.append("> **Generated** by `python3 matching/generate_matching.py`  \n")
    lines.append("> Source of truth: YAML `matching.paths` on each **`MACRO.md`**.  \n")
    lines.append(
        "> Dependencies: `python3 -m pip install -r matching/requirements.txt`  \n\n"
    )

    # --- Summary stats (first-class) ---
    n_yaml_paths = sum(len(v) for v in vr.macro_paths.values())
    stats = {
        "upstream_files_indexed": len(all_pos),
        "macro_1_many_paths": n_yaml_paths,
        "macro_1_1_pairs_total": len(macro_md),
        "macro_1_1_ok": len(paired_ok),
        "macro_1_1_missing_upstream": len(paired_fail),
        "uncovered_upstream_files": len(uncovered),
        "duplicate_claim_errors": len(vr.duplicate_claims),
        "yaml_or_schema_errors": len(vr.yaml_errors),
        "missing_declared_upstream": len(vr.missing_upstream),
    }
    lines.append("## Report summary\n\n")
    lines.append("| Metric | Count |\n|--------|-------:|\n")
    for k, v in stats.items():
        lines.append(f"| {k.replace('_', ' ').title()} | {v} |\n")
    lines.append("\n")

    ok_report = (
        stats["duplicate_claim_errors"]
        + stats["missing_declared_upstream"]
        + stats["yaml_or_schema_errors"]
        + stats["macro_1_1_missing_upstream"]
        == 0
    )
    lines.append(
        f"**Overall:** `{'PASS' if ok_report else 'FAIL'}`"
        " — non-zero issue counts below mean the report is still written, but you should fix YAML or upstream sync.\n\n"
    )

    if fetch_log:
        lines.append("## Upstream sync log\n\n")
        for row in fetch_log:
            lines.append(f"- {row}\n")
        lines.append("\n")

    lines.append("## Ignored when indexing upstream\n\n")
    lines.append(
        "These path rules exclude files from **uncovered** / **indexed** counts (mirroring skeleton policy):\n\n"
    )
    lines.append(f"- Top-level only skipped: `{sorted(SKIP_TOP)}`\n")
    lines.append(f"- Any path segment skipped: `{sorted(SKIP_ANYWHERE)}`\n")
    lines.append(
        "- **`*.md` in `**/commands/` and `**/agents/`** are covered implicitly by the **1:1** table, not by `matching.paths`.\n\n"
    )

    if vr.duplicate_claims or vr.missing_upstream or vr.yaml_errors:
        lines.append("## Validation issues\n\n")
        if vr.yaml_errors:
            lines.append("### YAML / frontmatter\n\n")
            for e in vr.yaml_errors:
                lines.append(f"- {e}\n")
            lines.append("\n")
        if vr.duplicate_claims:
            lines.append("### Duplicate `matching.paths`\n\n")
            for e in vr.duplicate_claims:
                lines.append(f"- {e}\n")
            lines.append("\n")
        if vr.missing_upstream:
            lines.append("### Missing upstream (declared in MACRO but absent on disk)\n\n")
            for e in vr.missing_upstream:
                lines.append(f"- {e}\n")
            lines.append("\n")

    lines.append("## Rules\n\n")
    lines.append(
        "1. **`MACRO.md`** — YAML `matching.paths` (no `**/commands/*.md` / `**/agents/*.md` here).\n"
    )
    lines.append(
        "2. **`*.macro.md`** — 1:1 with upstream `*.md` (same relative path; strip `.macro`).\n"
    )
    lines.append("3. Paths in this doc are relative to each repo root.\n\n")

    lines.append("## 1:1 — `*.macro.md` → upstream `*.md`\n\n")
    lines.append("| Skeleton | Upstream |\n|----------|----------|\n")
    for row in sorted(paired_ok) + sorted(paired_fail):
        lines.append(row + "\n")
    lines.append("\n")

    lines.append("## 1:many — `MACRO.md` → `matching.paths`\n\n")
    for skel_macro in sorted(vr.macro_paths.keys(), key=lambda s: (s != "MACRO.md", s)):
        paths = vr.macro_paths[skel_macro]
        lines.append(f"### `{skel_macro}`\n\n")
        lines.append(f"**Files ({len(paths)}):**\n\n")
        for f in paths:
            lines.append(f"- `{f}`\n")
        lines.append("\n")

    if uncovered:
        lines.append("## Uncovered upstream files (informational)\n\n")
        lines.append(
            "Files under `claude-code/` not assigned to any `matching.paths`, "
            "not a 1:1 prompt pair, and not ignored by policy — you may add them to a `MACRO.md` or extend ignore rules.\n\n"
        )
        for f in uncovered[:500]:
            lines.append(f"- `{f}`\n")
        if len(uncovered) > 500:
            lines.append(f"\n… *{len(uncovered) - 500} more*\n")
        lines.append("\n")

    out.write_text("".join(lines), encoding="utf-8")
    return paired_ok, paired_fail, stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate MATCHING.md for skeleton ↔ claude-code")
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Do not git clone/pull claude-code/ (use existing tree)",
    )
    parser.add_argument(
        "--remote",
        default=UPSTREAM_DEFAULT_REMOTE,
        help="Git remote for upstream (default: Anthropic claude-code)",
    )
    parser.add_argument(
        "--branch",
        default=None,
        help="Branch for shallow clone (default: remote default branch)",
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Rewrite matching.paths in all MACRO.md using directory heuristic",
    )
    args = parser.parse_args()

    # Order from workspace_roots: (workspace, claude-code, claude-code-skeleton, matching/)
    _, up, skel, _md = workspace_roots(Path(__file__))
    skel = skel.resolve()
    up = up.resolve()
    out = skel.parent / "MATCHING.md"

    if not skel.is_dir():
        sys.exit(f"Missing skeleton: {skel}")
    if yaml is None and not args.seed:
        sys.exit("Install PyYAML: python3 -m pip install -r matching/requirements.txt")

    fetch_log: list[str] = []
    if not args.no_fetch:
        fetch_log = fetch_upstream(up, args.remote, args.branch)
        if any(line.startswith("ERROR:") for line in fetch_log):
            print("\n".join(fetch_log))
            sys.exit(1)
        clone_failed = any("git clone failed" in line for line in fetch_log)
        if clone_failed and not (up / ".git").is_dir():
            print("\n".join(fetch_log))
            sys.exit(1)

    if not up.is_dir() or not ((up / "README.md").exists() or (up / "plugins").exists()):
        print("\n".join(fetch_log))
        sys.exit(
            f"Upstream tree missing or unusable at {up}. Fix git sync or use --no-fetch with a valid tree."
        )

    if args.seed:
        if yaml is None:
            sys.exit("Install PyYAML for --seed")
        seed_frontmatter(skel, up)

    vr = collect_macro_paths(skel, up)
    paired_ok, paired_fail, _stats = build_matching(skel, up, out, fetch_log, vr)

    print(f"Wrote {out}")
    print(
        f"1:1 pairs ok/miss: {len(paired_ok)}/{len(paired_fail)} | "
        f"issues: dup={len(vr.duplicate_claims)} missing={len(vr.missing_upstream)} "
        f"yaml={len(vr.yaml_errors)}"
    )

    if vr.fatal or paired_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
