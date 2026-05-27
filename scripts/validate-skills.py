#!/usr/bin/env python3
"""
validate-skills.py — Hard validator for every SKILL.md in the repo.

Checks:
  1. File starts with `---` on line 1.
  2. Frontmatter terminates with `---` on a later line.
  3. Frontmatter is parseable YAML.
  4. Required fields present: name, description.
  5. `name` matches the parent directory basename (catches rename drift).
  6. `description` non-empty.

Exit code 0 = clean. Non-zero = number of failing files.

Usage:
    python3 scripts/validate-skills.py [--fix] [--report PATH]

--fix   Attempt to auto-repair missing closing `---`, missing name, and
        backfill description from H1 heading. Will NOT overwrite existing
        good content.
--report PATH  Write JSON report of all issues.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIRS = [
    "agents", "automation", "content", "core", "cybersecurity", "data",
    "development", "devops", "financial", "integrations", "marketing",
    "mcp", "meta", "operations", "productivity", "research", "sales",
    "trading",
]


def find_skills() -> list[Path]:
    found = []
    for d in SKILL_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for p in base.rglob("SKILL.md"):
            found.append(p)
    return sorted(found)


def split_frontmatter(text: str) -> tuple[str | None, str, int | None]:
    """Return (frontmatter_yaml, body, closing_line_index) or (None, text, None)."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip() != "---":
        return None, text, None
    for i, line in enumerate(lines[1:], start=1):
        if line.rstrip() == "---":
            fm = "".join(lines[1:i])
            body = "".join(lines[i + 1:])
            return fm, body, i
    return None, text, None  # no closing


def first_h1(body: str) -> str | None:
    for line in body.splitlines():
        m = re.match(r"^#\s+(.+)$", line.strip())
        if m:
            return m.group(1).strip()
    return None


def validate_one(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        return [f"unreadable: {exc}"]

    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        errors.append("missing-leading----")
        return errors  # everything else depends on this

    fm, _body, _close = split_frontmatter(text)
    if fm is None:
        errors.append("missing-closing-frontmatter-delimiter")
        return errors

    try:
        meta = yaml.safe_load(fm) or {}
    except Exception as exc:
        errors.append(f"invalid-yaml: {exc.__class__.__name__}")
        return errors

    if not isinstance(meta, dict):
        errors.append("frontmatter-not-mapping")
        return errors

    name = meta.get("name")
    desc = meta.get("description")

    if not name or not isinstance(name, str):
        errors.append("missing-name")
    else:
        # name should match parent dir basename (catches rename drift)
        expected = path.parent.name
        if name.strip() != expected:
            errors.append(f"name-mismatch[name='{name}', dir='{expected}']")

    if not desc or not isinstance(desc, str) or not desc.strip():
        errors.append("missing-description")

    return errors


def fix_one(path: Path) -> list[str]:
    """Attempt repair. Returns list of fixes applied."""
    fixes: list[str] = []
    text = path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        return ["cannot-fix:no-leading-delimiter"]

    fm, body, _close = split_frontmatter(text)
    expected_name = path.parent.name

    # Case A: missing closing --- entirely.
    if fm is None:
        # Heuristic: frontmatter ends at first blank line followed by markdown
        # heading, or first line that doesn't look like YAML.
        lines = text.splitlines(keepends=True)
        cut = None
        for i in range(1, len(lines)):
            ln = lines[i]
            stripped = ln.rstrip()
            if stripped.startswith("#") and not stripped.startswith("#!"):
                cut = i
                break
            # YAML-ish keys: `key:` or `  - item` or quoted strings or blank
            if stripped and not re.match(r"^[\s\-]*[\w'\"\[\{]", stripped):
                cut = i
                break
        if cut is None:
            cut = min(20, len(lines))
        fm_raw = "".join(lines[1:cut]).rstrip() + "\n"
        body = "".join(lines[cut:])
        fixes.append("added-closing-delimiter")
        try:
            meta = yaml.safe_load(fm_raw) or {}
        except Exception:
            meta = {}
    else:
        try:
            meta = yaml.safe_load(fm) or {}
        except Exception:
            meta = {}

    if not isinstance(meta, dict):
        meta = {}

    # Case B: missing name.
    if not meta.get("name"):
        meta["name"] = expected_name
        fixes.append("backfilled-name")

    # Case C: missing description. Use H1 if available, else generic.
    if not meta.get("description") or not str(meta.get("description")).strip():
        h1 = first_h1(body)
        if h1:
            meta["description"] = f"{h1}. Use when relevant to this domain."
        else:
            meta["description"] = (
                f"Skill: {expected_name}. See SKILL.md body for details. "
                "Use when this domain is relevant."
            )
        fixes.append("backfilled-description")

    if not fixes:
        return []

    # Reorder so name and description come first.
    ordered: dict = {}
    for key in ("name", "description"):
        if key in meta:
            ordered[key] = meta.pop(key)
    ordered.update(meta)

    new_fm = yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True, width=120).rstrip()
    new_text = f"---\n{new_fm}\n---\n{body}" if not body.startswith("\n") else f"---\n{new_fm}\n---{body}"
    path.write_text(new_text, encoding="utf-8")
    return fixes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true", help="Attempt auto-repair")
    ap.add_argument("--report", type=Path, help="Write JSON report to this path")
    args = ap.parse_args()

    skills = find_skills()
    print(f"Validating {len(skills)} SKILL.md files...", file=sys.stderr)

    issues: dict[str, list[str]] = {}
    fix_log: dict[str, list[str]] = {}

    for s in skills:
        errs = validate_one(s)
        if errs:
            rel = s.relative_to(ROOT).as_posix()
            issues[rel] = errs
            if args.fix:
                applied = fix_one(s)
                if applied:
                    fix_log[rel] = applied
                    # Re-validate after fix
                    new_errs = validate_one(s)
                    if new_errs:
                        issues[rel] = ["AFTER-FIX:"] + new_errs
                    else:
                        del issues[rel]

    report = {
        "total_skills": len(skills),
        "issues_count": len(issues),
        "fixes_applied": len(fix_log),
        "issues": issues,
        "fixes": fix_log,
    }

    if args.report:
        args.report.write_text(json.dumps(report, indent=2))
        print(f"Report written: {args.report}", file=sys.stderr)

    if issues:
        print(f"\nFAIL: {len(issues)} skill(s) with issues:", file=sys.stderr)
        for path, errs in list(issues.items())[:25]:
            print(f"  {path}", file=sys.stderr)
            for e in errs:
                print(f"    - {e}", file=sys.stderr)
        if len(issues) > 25:
            print(f"  ... and {len(issues) - 25} more (use --report for full)", file=sys.stderr)
        return min(len(issues), 255)

    print(f"\nOK: All {len(skills)} skills valid.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
