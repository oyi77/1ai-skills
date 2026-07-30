#!/usr/bin/env python3
"""
run-evals.py — Evaluation runner for 1ai-skills.

Loads eval cases from evals/cases/ and runs checks against each skill's
SKILL.md. Reports pass/fail per check with summary statistics.

Usage:
    python3 scripts/run-evals.py                 # Run all evals
    python3 scripts/run-evals.py --list           # List available cases
    python3 scripts/run-evals.py --skill NAME     # Single skill
    python3 scripts/run-evals.py --category CAT   # Single category
    python3 scripts/run-evals.py --json           # Machine-readable output
    python3 scripts/run-evals.py --verbose        # Show passing checks
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = ROOT / "evals" / "cases"

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required — pip install PyYAML", file=sys.stderr)
    sys.exit(2)


# ── Check implementations ──

def _check_contains(text: str, _fm: dict, params: dict) -> tuple[bool, str]:
    pattern = params.get("pattern", "")
    if not pattern:
        return False, "no-pattern-specified"
    flags = re.DOTALL if params.get("multiline") else 0
    if re.search(pattern, text, flags):
        return True, f"found pattern /{pattern}/"
    return False, f"pattern /{pattern}/ not found"


def _check_not_contains(text: str, _fm: dict, params: dict) -> tuple[bool, str]:
    pattern = params.get("pattern", "")
    if not pattern:
        return False, "no-pattern-specified"
    if re.search(pattern, text):
        return False, f"pattern /{pattern}/ found (should be absent)"
    return True, f"pattern /{pattern}/ absent (as expected)"


def _check_section_exists(text: str, _fm: dict, params: dict) -> tuple[bool, str]:
    """Check for markdown heading (## or ###) matching pattern."""
    pattern = params.get("pattern", "")
    if not pattern:
        return False, "no-pattern-specified"
    # Match markdown headings containing the pattern
    heading_re = re.compile(r"^#{2,4}\s+.*" + pattern + r".*$", re.MULTILINE)
    if heading_re.search(text):
        return True, f"section /{pattern}/ exists"
    return False, f"section /{pattern}/ not found"


def _check_frontmatter_field(_text: str, fm: dict, params: dict) -> tuple[bool, str]:
    field = params.get("field", "")
    if not field:
        return False, "no-field-specified"
    if field not in fm:
        return False, f"frontmatter missing field '{field}'"
    value = params.get("value")
    if value is not None:
        actual = str(fm.get(field, ""))
        if actual != value:
            return False, f"field '{field}' value '{actual}' != expected '{value}'"
    return True, f"frontmatter field '{field}' present"


def _check_frontmatter_field_exists(_text: str, fm: dict, params: dict) -> tuple[bool, str]:
    field = params.get("field", "")
    if not field:
        return False, "no-field-specified"
    if field in fm and fm[field] is not None and str(fm[field]).strip():
        return True, f"frontmatter field '{field}' exists"
    return False, f"frontmatter field '{field}' missing or empty"


def _check_anti_rat_table(text: str, _fm: dict, _params: dict) -> tuple[bool, str]:
    """Check for an anti-rationalization table (| Trap | Reality | or similar)."""
    # Look for a markdown table preceded by "Anti-Rationalization"
    if re.search(r"Anti-Rationalization", text) and re.search(r"\|.*\|.*\|", text):
        # Verify there's actually a table row after the heading
        lines = text.split("\n")
        found_heading = False
        for i, line in enumerate(lines):
            if "Anti-Rationalization" in line:
                found_heading = True
                # Check next few lines for table rows
                for j in range(i + 1, min(i + 10, len(lines))):
                    if lines[j].strip().startswith("|") and lines[j].strip().endswith("|"):
                        return True, "anti-rationalization table found"
        if found_heading:
            return False, "anti-rationalization heading found but no table rows"
    return False, "anti-rationalization table not found"


def _check_code_block_count(text: str, _fm: dict, params: dict) -> tuple[bool, str]:
    min_count = params.get("min", 0)
    max_count = params.get("max")
    blocks = re.findall(r"```", text)
    count = len(blocks) // 2  # each block has opening and closing ```
    if count < min_count:
        return False, f"code block count {count} < min {min_count}"
    if max_count is not None and count > max_count:
        return False, f"code block count {count} > max {max_count}"
    return True, f"code block count {count} in range [{min_count}, {max_count or 'inf'})"


def _check_has_workflow_section(text: str, _fm: dict, _params: dict) -> tuple[bool, str]:
    patterns = [
        r"## Workflow",
        r"## Process",
        r"## Steps",
        r"## Daily Practice",
        r"## Core Principles",
        r"## How to Use",
        r"## Core Features",
        r"## Architecture",
    ]
    for pat in patterns:
        if re.search(rf"^{pat}$", text, re.MULTILINE):
            return True, f"workflow section found: {pat.strip('^$')}"
    return False, "no workflow/process section found"


def _check_trigger_phrase(_text: str, fm: dict, _params: dict) -> tuple[bool, str]:
    desc = str(fm.get("description", ""))
    if desc.lower().startswith("use when"):
        return True, "description starts with 'Use when'"
    return False, f"description does not start with 'Use when' (starts: {desc[:40]!r})"


def _check_skill_depth(text: str, _fm: dict, params: dict) -> tuple[bool, str]:
    min_lines = params.get("min_lines", 0)
    lines = text.strip().count("\n") + 1
    if lines >= min_lines:
        return True, f"skill depth {lines} >= {min_lines}"
    return False, f"skill depth {lines} < {min_lines}"


def _check_has_code_example(text: str, _fm: dict, params: dict) -> tuple[bool, str]:
    language = params.get("language", None)
    if language:
        # Look for fenced block with specific language
        pat = rf"```{language}\n"
        if re.search(pat, text):
            return True, f"code example in {language} found"
        return False, f"code example in {language} not found"
    # Any fenced code block
    if re.search(r"```", text):
        return True, "code example found"
    return False, "no code example found"


def _check_domain_match(_text: str, fm: dict, params: dict) -> tuple[bool, str]:
    """Check that frontmatter domain matches the expected value."""
    expected = params.get("domain", "")
    if not expected:
        return True, "no domain specified for check"
    actual = str(fm.get("domain", ""))
    if actual == expected:
        return True, f"domain matches: {actual}"
    return False, f"domain '{actual}' != expected '{expected}'"


# ── Check registry ──

CHECK_REGISTRY = {
    "contains": _check_contains,
    "not_contains": _check_not_contains,
    "section_exists": _check_section_exists,
    "frontmatter_field": _check_frontmatter_field,
    "frontmatter_field_exists": _check_frontmatter_field_exists,
    "anti_rat_table": _check_anti_rat_table,
    "code_block_count": _check_code_block_count,
    "has_workflow_section": _check_has_workflow_section,
    "trigger_phrase": _check_trigger_phrase,
    "skill_depth": _check_skill_depth,
    "has_code_example": _check_has_code_example,
    "domain_match": _check_domain_match,
}


# ── Eval case loading ──

def discover_cases(filter_skill: str | None = None,
                   filter_category: str | None = None) -> list[dict]:
    """Discover eval case JSON files in evals/cases/."""
    cases = []
    if not CASES_DIR.exists():
        print(f"ERROR: Cases directory not found at {CASES_DIR}", file=sys.stderr)
        sys.exit(2)
    for pattern in ["*.json", "**/*.json"]:
        for case_file in sorted(CASES_DIR.glob(pattern)):
            try:
                case = json.loads(case_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as e:
                print(f"WARNING: Skipping {case_file}: {e}", file=sys.stderr)
                continue
            # Validate required fields
            skill = case.get("skill", "")
            category = case.get("category", "")
            checks = case.get("checks", [])
            if not skill or not category or not checks:
                print(f"WARNING: {case_file} missing skill/category/checks",
                      file=sys.stderr)
                continue
            if filter_skill and skill != filter_skill:
                continue
            if filter_category and category != filter_category:
                continue
            case["_file"] = str(case_file.relative_to(ROOT))
            cases.append(case)
    return cases


# ── Loading SKILL.md ──

def load_skill_text(skill_name: str, category: str) -> str | None:
    """Load SKILL.md text for a skill. Search across all categories if needed."""
    cats = [category] if category else [
        d for d in os.listdir(ROOT)
        if (ROOT / d).is_dir() and not d.startswith(".")
    ]
    for cat in cats:
        skill_dir = ROOT / cat / skill_name
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            return skill_file.read_text(encoding="utf-8")
    # Recursive search in all category subdirs
    for cat in cats:
        for md in (ROOT / cat).rglob("SKILL.md"):
            if md.parent.name == skill_name:
                return md.read_text(encoding="utf-8")
    return None


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract frontmatter dict and body text from SKILL.md."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[4:end]
    body = text[end + 4:]
    try:
        fm = yaml.load(fm_text, Loader=getattr(yaml, 'CSafeLoader', yaml.SafeLoader))
        if not isinstance(fm, dict):
            fm = {}
    except yaml.YAMLError:
        fm = {}
    return fm, body


# ── Running checks ──

def run_eval_case(case: dict, verbose: bool = False) -> dict:
    """Run all checks for a single eval case against its target skill."""
    skill_name = case["skill"]
    category = case.get("category", "")
    result = {
        "skill": skill_name,
        "category": category,
        "name": case.get("name", ""),
        "description": case.get("description", ""),
        "checks": [],
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "total": len(case.get("checks", [])),
    }

    text = load_skill_text(skill_name, category)
    if text is None:
        result["failed"] = result["total"]
        result["error"] = f"SKILL.md not found for '{skill_name}' in '{category}'"
        result["checks"].append({
            "type": "_error",
            "passed": False,
            "message": result["error"],
        })
        return result

    fm, body = parse_frontmatter(text)

    for i, check in enumerate(case.get("checks", [])):
        check_type = check.get("type", "")
        check_name = check.get("name", f"check-{i}")
        handler = CHECK_REGISTRY.get(check_type)

        if handler is None:
            result["skipped"] += 1
            result["checks"].append({
                "type": check_type,
                "name": check_name,
                "passed": False,
                "skipped": True,
                "message": f"unknown check type: {check_type}",
            })
            continue

        try:
            passed, message = handler(text, fm, check)
        except Exception as e:
            passed = False
            message = f"check error: {e}"

        check_result = {
            "type": check_type,
            "name": check_name,
            "passed": passed,
            "message": message,
        }
        result["checks"].append(check_result)
        if passed:
            result["passed"] += 1
        else:
            result["failed"] += 1

    return result


# ── Reporting ──

def print_human_report(results: list[dict], verbose: bool = False):
    """Print human-readable eval report."""
    total_checks = sum(r["total"] for r in results)
    total_passed = sum(r["passed"] for r in results)
    total_failed = sum(r["failed"] for r in results)
    total_skipped = sum(r["skipped"] for r in results)

    print(f"\n{'=' * 70}")
    print(f"  1ai-skills Evaluation Report")
    print(f"{'=' * 70}\n")

    if not results:
        print("  No eval cases found.")
        return

    for r in results:
        status = "✅" if r["failed"] == 0 else "❌"
        print(f"  {status} {r['skill']} ({r['category']})")
        print(f"     {r['name']}")
        if verbose:
            print(f"     Passed: {r['passed']}/{r['total']}  "
                  f"Failed: {r['failed']}  Skipped: {r['skipped']}")
            for c in r["checks"]:
                icon = "✅" if c["passed"] else "❌"
                skip_mark = " ⏭" if c.get("skipped") else ""
                print(f"       {icon}{skip_mark} {c['type']}: {c['message']}")

    print(f"\n  Summary: {total_passed}/{total_checks} passed, "
          f"{total_failed} failed, {total_skipped} skipped "
          f"across {len(results)} case(s)\n")


def print_json_report(results: list[dict]):
    """Print machine-readable JSON report."""
    report = {
        "generated": "1ai-skills eval report",
        "total_cases": len(results),
        "total_checks": sum(r["total"] for r in results),
        "total_passed": sum(r["passed"] for r in results),
        "total_failed": sum(r["failed"] for r in results),
        "total_skipped": sum(r["skipped"] for r in results),
        "cases": results,
    }
    print(json.dumps(report, indent=2))


# ── Main ──

def parse_args():
    parser = argparse.ArgumentParser(
        description="1ai-skills Evaluation Runner",
    )
    parser.add_argument("--list", action="store_true",
                        help="List available eval cases")
    parser.add_argument("--all", action="store_true",
                        help="Run evals for all available cases")
    parser.add_argument("--skill", type=str, default=None,
                        help="Run evals for a specific skill")
    parser.add_argument("--category", type=str, default=None,
                        help="Run evals for a specific category")
    parser.add_argument("--json", action="store_true",
                        help="JSON output (machine-readable)")
    parser.add_argument("--verbose", action="store_true",
                        help="Show passing checks too")
    args = parser.parse_args()
    mode_flags = sum([args.all, args.skill is not None, args.category is not None])
    if not args.list and mode_flags == 0:
        parser.error("specify --all, --skill, or --category (or --list)")
    if not args.list and mode_flags > 1:
        parser.error("use only one of --all, --skill, --category")
    return args


def main():
    args = parse_args()
    cases = discover_cases(
        filter_skill=args.skill,
        filter_category=args.category,
    )

    if args.list:
        print(f"\nAvailable eval cases ({len(cases)}):\n")
        for c in cases:
            cat = c.get("category", "?")
            skill = c.get("skill", "?")
            name = c.get("name", "")
            print(f"  [{cat}] {skill}: {name}")
        print()
        return

    if not cases:
        print(f"No eval cases found"
              f"{' for skill: '+args.skill if args.skill else ''}"
              f"{' for category: '+args.category if args.category else ''}")
        sys.exit(0)

    results = [run_eval_case(c, verbose=args.verbose) for c in cases]

    if args.json:
        print_json_report(results)
    else:
        print_human_report(results, verbose=args.verbose)

    # Exit code: 0 if all passed, 1 if any failed
    any_failures = any(r["failed"] > 0 for r in results)
    sys.exit(1 if any_failures else 0)


if __name__ == "__main__":
    main()
