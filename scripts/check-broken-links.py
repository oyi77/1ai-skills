#!/usr/bin/env python3
"""
check-broken-links.py — Scan SKILL.md files for broken internal /skills/ references.

Checks that markdown links of the form [text](/skills/name) or [text](../skills/name)
point to existing skill names in SKILLS.json. Also checks skill://name links
(already validated by lint-skills.py, but rechecked here for completeness).

Usage:
  python3 scripts/check-broken-links.py              # Report broken links
  python3 scripts/check-broken-links.py --json        # Machine-readable JSON output
  python3 scripts/check-broken-links.py --exit-zero   # Always exit 0 (for non-blocking CI)
  python3 scripts/check-broken-links.py --verbose     # Show all scanned files
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_JSON = ROOT / "SKILLS.json"
SKILL_DIRS = [
    ROOT / p
    for p in [
        "agents", "automation", "commands", "content", "core", "cybersecurity",
        "data", "development", "devops", "docs", "finance", "financial",
        "hooks", "integrations", "launch", "marketing", "mcp", "meta",
        "mindset", "operations", "productivity", "references", "research",
        "rules", "sales", "trading", "writing",
    ]
]
SKILL_LINK_RE = re.compile(r"skill://([a-z0-9-]+)")
PATH_LINK_RE = re.compile(r"\[([^\]]*)\]\(/skills/([a-z0-9-]+)\)")
RELATIVE_LINK_RE = re.compile(r"\[([^\]]*)\]\(\.\.\/skills/([a-z0-9-]+)\)")


def load_skill_names() -> set[str]:
    """Load all registered skill names from SKILLS.json."""
    data = json.loads(SKILLS_JSON.read_text())
    return {s["name"] for s in data.get("skills", [])}


def find_all_md_files() -> list[Path]:
    """Find all markdown files in the repo (SKILL.md, CHANGELOG, README, docs, etc.)"""
    files = []
    for ext in ("*.md", "*.mdx"):
        files.extend(ROOT.rglob(ext))
    # Filter .gitignore'd dirs
    ignored_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", ".git"}
    return sorted(f for f in files if not any(p.name in ignored_dirs for p in f.parents))


def scan_file(path: Path, all_names: set[str]) -> list[dict]:
    """Scan a single file for broken internal skill references."""
    issues: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [{"file": str(path), "line": 0, "type": "read_error", "target": str(e)}]

    lines = text.split("\n")

    for line_no, line in enumerate(lines, 1):
        # Check skill://name links
        for m in SKILL_LINK_RE.finditer(line):
            target = m.group(1)
            if target not in all_names:
                issues.append({
                    "file": str(path),
                    "line": line_no,
                    "type": "skill_link",
                    "target": f"skill://{target}",
                    "content": line.strip()[:120],
                })

        # Check /skills/name links
        for m in PATH_LINK_RE.finditer(line):
            target = m.group(2)
            if target not in all_names:
                issues.append({
                    "file": str(path),
                    "line": line_no,
                    "type": "path_link",
                    "target": f"/skills/{target}",
                    "content": line.strip()[:120],
                })

        # Check ../skills/name links
        for m in RELATIVE_LINK_RE.finditer(line):
            target = m.group(2)
            if target not in all_names:
                issues.append({
                    "file": str(path),
                    "line": line_no,
                    "type": "relative_link",
                    "target": f"../skills/{target}",
                    "content": line.strip()[:120],
                })

    return issues


def main():
    parser = argparse.ArgumentParser(description="Check for broken internal skill references")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    parser.add_argument("--verbose", action="store_true", help="Show all scanned files")
    parser.add_argument("--exit-zero", action="store_true",
                        help="Always exit 0 (useful for non-blocking CI)")
    args = parser.parse_args()

    all_names = load_skill_names()
    if not all_names:
        print("ERROR: No skill names loaded from SKILLS.json")
        sys.exit(2)

    if not args.json:
        print(f"Loaded {len(all_names)} skill names from SKILLS.json")
        print(f"Scanning markdown files for broken internal references...\n")

    files = find_all_md_files()

    all_issues: list[dict] = []
    scanned = 0
    for f in files:
        if args.verbose:
            print(f"  {f.relative_to(ROOT)}")
        issues = scan_file(f, all_names)
        all_issues.extend(issues)
        scanned += 1

    if not args.json:
        print(f"\nScanned {scanned} files.")
        print(f"Found {len(all_issues)} broken internal reference(s)\n")

        if all_issues:
            # Group by type
            by_type: dict[str, list[dict]] = {}
            for issue in all_issues:
                by_type.setdefault(issue["type"], []).append(issue)

            for t, items in sorted(by_type.items()):
                print(f"  [{t}] ({len(items)}):")
                for item in sorted(items, key=lambda x: (x["file"], x["line"])):
                    rel = Path(item["file"]).relative_to(ROOT)
                    print(f"    {rel}:{item['line']}  {item['target']}")
                    if args.verbose:
                        print(f"        {item['content']}")
                print()

            print(f"Total: {len(all_issues)} broken reference(s)")
        else:
            print("  All internal references resolve correctly!")

    # JSON output
    if args.json:
        report = {
            "scanned": scanned,
            "skills_in_registry": len(all_names),
            "broken_count": len(all_issues),
            "broken": sorted(all_issues, key=lambda x: (x["file"], x["line"])),
        }
        print(json.dumps(report, indent=2))

    if args.exit_zero:
        sys.exit(0)
    sys.exit(1 if all_issues else 0)


if __name__ == "__main__":
    main()
