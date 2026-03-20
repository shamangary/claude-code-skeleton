#!/usr/bin/env python3
"""
Generate ../MATCHING.md from YAML frontmatter in claude-code-skeleton/**/MACRO.md

Layout (workspace root = parent of this matching/ directory):

  workspace/
    claude-code/              # upstream (default: clone/pull from GitHub)
    claude-code-skeleton/
    matching/
      generate_matching.py
    MATCHING.md               # written here (summary + tables; full overwrite)

Usage:

  python3 -m pip install -r matching/requirements.txt
  python3 matching/generate_matching.py              # fetch upstream + regenerate
  python3 matching/generate_matching.py --no-fetch   # use existing claude-code/
  python3 matching/generate_matching.py --seed       # refresh matching.paths (then run without --seed)

MACRO.md granularity guidance
------------------------------
Prefer fewer, higher-level MACRO.md files rather than one per subdirectory:
  - One per plugin root  (covers README, plugin.json, hooks, scripts)
  - One per skill        (covers SKILL.md + references/ + examples/ as a group)
  - Only create a sub-folder MACRO.md when it has 5+ files worth of independent description.

The --seed flag assigns upstream files to the *nearest existing* MACRO.md, so if you
consolidate MACRO.md files first, --seed will naturally produce broader path lists per file.

Open vs closed in upstream
---------------------------
claude-code/ contains ~180 readable files (prompts, manifests, hook scripts, settings).
The agent loop, context compression, permission enforcement, and tool dispatch live in the
minified @anthropic-ai/claude-code npm bundle and are not readable here. This matcher
only indexes the open file topology — see GLOSSARY.md for a full open/closed breakdown.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
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


def upstream_git_snapshot(up: Path) -> dict[str, str] | None:
    """Best-effort git identity for claude-code/. Empty strings omit that field."""
    up = up.resolve()
    if not (up / ".git").is_dir():
        return None

    def run_git(args: list[str]) -> str:
        r = subprocess.run(
            ["git", "-C", str(up)] + args,
            capture_output=True,
            text=True,
        )
        return (r.stdout or "").strip() if r.returncode == 0 else ""

    commit = run_git(["rev-parse", "HEAD"])
    short = run_git(["rev-parse", "--short", "HEAD"]) if commit else ""
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    if branch == "HEAD":
        branch = "(detached)"
    subject = run_git(["log", "-1", "--format=%s"])
    when = run_git(["log", "-1", "--format=%ci"])
    describe = run_git(["describe", "--tags", "--always", "--dirty"])
    origin = run_git(["remote", "get-url", "origin"])

    out: dict[str, str] = {}
    if commit:
        out["commit"] = commit
    if short:
        out["short"] = short
    if branch:
        out["branch"] = branch
    if subject:
        out["subject"] = subject
    if when:
        out["date"] = when
    if describe:
        out["describe"] = describe
    if origin:
        out["origin"] = origin
    return out or None


def print_terminal_summary(
    up: Path,
    out: Path,
    stats: dict[str, int],
    vr: ValidationResult,
) -> None:
    ok_report = (
        stats["duplicate_claim_errors"]
        + stats["missing_declared_upstream"]
        + stats["yaml_or_schema_errors"]
        == 0
    )
    sep = "─" * 52
    print()
    print(sep)
    print("  claude-code/ (upstream git)")
    print(sep)
    snap = upstream_git_snapshot(up)
    if snap is None:
        print("  (not a git repository — unexpected for a normal clone)")
    else:
        if snap.get("describe"):
            print(f"  version:   {snap['describe']}")
        if snap.get("short") and snap.get("commit"):
            print(f"  commit:    {snap['short']} ({snap['commit']})")
        elif snap.get("commit"):
            print(f"  commit:    {snap['commit']}")
        if snap.get("branch"):
            print(f"  branch:    {snap['branch']}")
        if snap.get("subject"):
            print(f"  summary:   {snap['subject']}")
        if snap.get("date"):
            print(f"  date:      {snap['date']}")
        if snap.get("origin"):
            print(f"  origin:    {snap['origin']}")
    print()
    print(sep)
    print("  matching summary")
    print(sep)
    status = "PASS" if ok_report else "FAIL"
    try:
        out_display = str(out.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        out_display = str(out)
    n_errors = (
        stats["duplicate_claim_errors"]
        + stats["yaml_or_schema_errors"]
        + stats["missing_declared_upstream"]
    )
    print(f"  {status}   →  {out_display}")
    print()
    print(f"  upstream files:   {stats['upstream_files_indexed']}   "
          f"uncovered: {stats['uncovered_upstream_files']}")
    print(f"  MACRO.md files:   {stats['macro_md_files']}   "
          f"paths declared: {stats['paths_declared']}")
    print()
    if n_errors == 0:
        print("  errors: none")
    else:
        print(f"  errors: dup {stats['duplicate_claim_errors']}  "
              f"yaml {stats['yaml_or_schema_errors']}  "
              f"missing-decl {stats['missing_declared_upstream']}")
    print(sep)
    print()


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


def _md_cell_inline(text: str) -> str:
    """Single inline code span; avoid breaking markdown tables."""
    t = text.replace("`", "´")
    return f"`{t}`"


def build_matching(
    skel: Path,
    up: Path,
    out: Path,
    vr: ValidationResult,
) -> dict[str, int]:
    """Write MATCHING.md (summary + tables only). Returns stats dict."""
    skel = skel.resolve()
    up = up.resolve()

    all_upstream: list[Path] = []
    for p in up.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(up)
        if skip_path(rel.parts):
            continue
        all_upstream.append(rel)

    claimed = set()
    for paths in vr.macro_paths.values():
        for p in paths:
            claimed.add(p.replace("\\", "/").lstrip("/"))

    all_pos = {rel.as_posix() for rel in all_upstream}
    uncovered = sorted(all_pos - claimed)

    n_yaml_paths = sum(len(v) for v in vr.macro_paths.values())
    stats = {
        "upstream_files_indexed": len(all_pos),
        "macro_md_files": len(vr.macro_paths),
        "paths_declared": n_yaml_paths,
        "uncovered_upstream_files": len(uncovered),
        "duplicate_claim_errors": len(vr.duplicate_claims),
        "yaml_or_schema_errors": len(vr.yaml_errors),
        "missing_declared_upstream": len(vr.missing_upstream),
    }
    ok_report = (
        stats["duplicate_claim_errors"]
        + stats["missing_declared_upstream"]
        + stats["yaml_or_schema_errors"]
        == 0
    )

    gen_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    snap = upstream_git_snapshot(up)

    lines: list[str] = []
    lines.append("# MATCHING\n\n")
    lines.append(
        f"Generated {gen_ts} — `python3 matching/generate_matching.py` "
        "(this file is overwritten each run; edit `claude-code-skeleton/**/MACRO.md`, not here.)\n\n"
    )
    lines.append(f"**Overall:** `{'PASS' if ok_report else 'FAIL'}`\n\n")
    if snap:
        bits = []
        if snap.get("describe"):
            bits.append(snap["describe"])
        if snap.get("short"):
            bits.append(f"@{snap['short']}")
        if snap.get("branch"):
            bits.append(f"({snap['branch']})")
        line = " ".join(bits) if bits else ""
        if snap.get("subject"):
            line = (line + " — " if line else "") + snap["subject"]
        if line:
            lines.append(f"- **claude-code/** {line}\n")
    else:
        lines.append("- **claude-code/** *(not a git checkout or no `.git`)*\n")
    lines.append(
        f"- **Counts:** {stats['upstream_files_indexed']} upstream files; "
        f"{stats['macro_md_files']} MACRO.md files; "
        f"{stats['paths_declared']} paths declared; "
        f"{stats['uncovered_upstream_files']} uncovered; "
        f"errors dup/yaml/missing {stats['duplicate_claim_errors']}/"
        f"{stats['yaml_or_schema_errors']}/{stats['missing_declared_upstream']}\n\n"
    )

    lines.append("---\n\n")
    lines.append("## MACRO.md → `matching.paths`\n\n")
    lines.append("| MACRO.md | Path |\n|----------|------|\n")
    many_rows: list[tuple[str, str]] = []
    for skel_macro in sorted(vr.macro_paths.keys(), key=lambda s: (s != "MACRO.md", s)):
        paths = vr.macro_paths[skel_macro]
        if paths:
            for f in paths:
                many_rows.append((skel_macro, f.replace("\\", "/").lstrip("/")))
        else:
            many_rows.append((skel_macro, ""))
    if many_rows:
        for macro_key, path in many_rows:
            path_cell = _md_cell_inline(path) if path else "*(empty)*"
            lines.append(
                f"| {_md_cell_inline(macro_key)} | {path_cell} |\n"
            )
    else:
        lines.append("| — | *(no MACRO.md parsed)* |\n")
    lines.append("\n")

    lines.append("## Uncovered upstream files\n\n")
    lines.append("| Path |\n|------|\n")
    if uncovered:
        for f in uncovered:
            lines.append(f"| {_md_cell_inline(f)} |\n")
    else:
        lines.append("| *(none)* |\n")
    lines.append("\n")

    lines.append("## Validation issues\n\n")
    lines.append("| Kind | Detail |\n|------|--------|\n")
    issue_rows: list[tuple[str, str]] = []
    for e in vr.yaml_errors:
        issue_rows.append(("yaml", e))
    for e in vr.duplicate_claims:
        issue_rows.append(("duplicate_paths", e))
    for e in vr.missing_upstream:
        issue_rows.append(("missing_upstream", e))
    if issue_rows:
        for kind, detail in issue_rows:
            d = detail.replace("\n", " ").replace("|", "\\|")
            lines.append(f"| `{kind}` | {d} |\n")
    else:
        lines.append("| — | *(none)* |\n")
    lines.append("\n")

    out.write_text("".join(lines), encoding="utf-8")
    return stats


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
    stats = build_matching(skel, up, out, vr)

    print_terminal_summary(up, out, stats, vr)

    if vr.fatal:
        sys.exit(1)


if __name__ == "__main__":
    main()
