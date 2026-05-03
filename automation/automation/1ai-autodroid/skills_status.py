#!/usr/bin/env python3
"""
Skills Status Dashboard — Autodroid Skills Health Check

Checks all autodroid skills and generates a markdown status report.

Run:
    python3 skills_status.py
    python3 skills_status.py --out /tmp/status.md
    python3 skills_status.py --json

Checks per skill:
    - SKILL.md present?
    - Tests exist?
    - Config exists?
    - AI Interceptor integrated?
    - Syntax errors in Python files?
    - Line count
    - Main script exists?
"""

import ast
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ─── Config ──────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent

ALL_SKILLS = [
    "autodroid-kling-agent",
    "autodroid-grok-agent",
    "autodroid-flow-agent",
    "autodroid-pixverse-agent",
    "autodroid-instagram-agent",
    "autodroid-tiktok-agent",
    "autodroid-youtube-agent",
    "autodroid-whatsapp-agent",
    "ai-interceptor",
    "autodroid-device-agent",
    "autodroid-dashboard",
    "autodroid-playstore-agent",
    "autodroid-shopee-agent",
]

AI_INTERCEPTOR_MARKERS = [
    "ADBInterceptor",
    "AI_INTERCEPT_ENABLED",
    "ai-interceptor",
    "adb_interceptor",
    "from adb_interceptor",
    "import adb_interceptor",
]

# ─── Checks ──────────────────────────────────────────────────────────────────

def check_skill(skill_name: str) -> dict:
    """Run all checks for a skill. Returns status dict."""
    skill_path = BASE_DIR / skill_name
    result = {
        "skill": skill_name,
        "exists": skill_path.exists(),
        "skill_md": False,
        "tests_exist": False,
        "config_exists": False,
        "ai_interceptor": False,
        "syntax_errors": [],
        "line_count": 0,
        "main_script": None,
        "python_files": 0,
        "status": "missing",
    }

    if not skill_path.exists():
        return result

    # SKILL.md
    result["skill_md"] = (skill_path / "SKILL.md").exists()

    # Tests
    test_patterns = [
        "tests/test_*.py",
        "tests/*_test.py",
        "test_*.py",
        "scripts/test_*.py",
    ]
    test_files = []
    for pat in test_patterns:
        test_files.extend(skill_path.glob(pat))
    result["tests_exist"] = len(test_files) > 0

    # Config
    config_patterns = [
        "config/*.json",
        "config/*.yaml",
        "config/*.yml",
        "*.json",
    ]
    config_files = []
    for pat in config_patterns:
        config_files.extend(skill_path.glob(pat))
    result["config_exists"] = len(config_files) > 0

    # Find main Python scripts
    python_files = list(skill_path.glob("scripts/*.py")) + list(skill_path.glob("*.py"))
    # Filter out __init__, test files
    main_scripts = [
        f for f in python_files
        if not f.name.startswith("test_") and not f.name.startswith("__")
    ]
    result["python_files"] = len(python_files)

    if main_scripts:
        # Sort by size (largest = likely main)
        main_scripts.sort(key=lambda f: f.stat().st_size, reverse=True)
        result["main_script"] = str(main_scripts[0].relative_to(BASE_DIR))

    # Line count (all Python files)
    total_lines = 0
    syntax_errors = []

    for py_file in python_files:
        try:
            content = py_file.read_text(encoding="utf-8", errors="replace")
            total_lines += content.count("\n") + 1

            # Syntax check
            try:
                ast.parse(content)
            except SyntaxError as e:
                syntax_errors.append(f"{py_file.name}:{e.lineno}: {e.msg}")

            # AI Interceptor integration check
            if any(marker in content for marker in AI_INTERCEPTOR_MARKERS):
                result["ai_interceptor"] = True

        except Exception as e:
            syntax_errors.append(f"{py_file.name}: read error: {e}")

    result["line_count"] = total_lines
    result["syntax_errors"] = syntax_errors

    # Overall status
    if syntax_errors:
        result["status"] = "error"
    elif result["skill_md"] and result["tests_exist"] and result["ai_interceptor"]:
        result["status"] = "complete"
    elif result["skill_md"] or result["python_files"] > 0:
        result["status"] = "partial"
    else:
        result["status"] = "empty"

    return result


# ─── Report ───────────────────────────────────────────────────────────────────

def icon(val: bool) -> str:
    return "✅" if val else "❌"


def status_icon(status: str) -> str:
    return {
        "complete": "🟢",
        "partial": "🟡",
        "empty": "⚪",
        "error": "🔴",
        "missing": "⬛",
    }.get(status, "❓")


def generate_markdown_report(results: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Autodroid Skills Status Dashboard",
        "",
        f"**Generated:** {now}  ",
        f"**Base Dir:** {BASE_DIR}  ",
        "",
        "## Legend",
        "",
        "| Icon | Meaning |",
        "|------|---------|",
        "| 🟢 | Complete (SKILL.md + Tests + AI Interceptor) |",
        "| 🟡 | Partial (exists but missing some checks) |",
        "| ⚪ | Empty (directory exists but nothing inside) |",
        "| 🔴 | Error (syntax errors detected) |",
        "| ⬛ | Missing (directory not found) |",
        "",
        "## Skills Status",
        "",
        "| Status | Skill | SKILL.md | Tests | Config | AI Interceptor | Syntax | Lines | Main Script |",
        "|--------|-------|----------|-------|--------|----------------|--------|-------|-------------|",
    ]

    for r in results:
        skill_name = r["skill"]
        st = status_icon(r["status"])
        skill_md = icon(r["skill_md"])
        tests = icon(r["tests_exist"])
        config = icon(r["config_exists"])
        ai_int = icon(r["ai_interceptor"])
        syntax = f"✅ OK" if not r["syntax_errors"] else f"❌ {len(r['syntax_errors'])} error(s)"
        lines_count = f"{r['line_count']:,}" if r["line_count"] > 0 else "-"
        main_script = Path(r["main_script"]).name if r["main_script"] else "-"

        lines.append(
            f"| {st} | `{skill_name}` | {skill_md} | {tests} | {config} | {ai_int} | {syntax} | {lines_count} | `{main_script}` |"
        )

    lines.append("")

    # Summary stats
    complete = sum(1 for r in results if r["status"] == "complete")
    partial = sum(1 for r in results if r["status"] == "partial")
    missing = sum(1 for r in results if r["status"] == "missing")
    errors = sum(1 for r in results if r["status"] == "error")
    total_lines = sum(r["line_count"] for r in results)

    lines += [
        "## Summary",
        "",
        f"- **Total skills checked:** {len(results)}",
        f"- **Complete:** {complete}",
        f"- **Partial:** {partial}",
        f"- **Missing:** {missing}",
        f"- **Errors:** {errors}",
        f"- **Total lines of code:** {total_lines:,}",
        "",
    ]

    # Syntax errors detail
    all_errors = [(r["skill"], e) for r in results for e in r["syntax_errors"]]
    if all_errors:
        lines.append("## ❌ Syntax Errors")
        lines.append("")
        for skill, err in all_errors:
            lines.append(f"- **{skill}:** `{err}`")
        lines.append("")

    # Skills without tests
    no_tests = [r["skill"] for r in results if not r["tests_exist"] and r["exists"]]
    if no_tests:
        lines.append("## 📭 Skills Without Tests")
        lines.append("")
        for skill in no_tests:
            lines.append(f"- `{skill}`")
        lines.append("")

    # Skills without AI Interceptor
    no_interceptor = [r["skill"] for r in results if not r["ai_interceptor"] and r["exists"] and r["python_files"] > 0]
    if no_interceptor:
        lines.append("## ⚠️ Skills Without AI Interceptor")
        lines.append("")
        for skill in no_interceptor:
            lines.append(f"- `{skill}`")
        lines.append("")

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Skills Status Dashboard — check health of all autodroid skills"
    )
    parser.add_argument("--out", "-o", default=None, help="Save report to markdown file")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--skill", "-s", default=None, help="Check specific skill only")
    args = parser.parse_args()

    skills_to_check = ALL_SKILLS
    if args.skill:
        skills_to_check = [s for s in ALL_SKILLS if args.skill.lower() in s.lower()]
        if not skills_to_check:
            print(f"No skill matching '{args.skill}'")
            sys.exit(1)

    print(f"🔍 Checking {len(skills_to_check)} skills...", file=sys.stderr)

    results = []
    for skill_name in skills_to_check:
        result = check_skill(skill_name)
        results.append(result)
        st = status_icon(result["status"])
        print(f"  {st} {skill_name} ({result['line_count']:,} lines)", file=sys.stderr)

    print(file=sys.stderr)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    report = generate_markdown_report(results)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report)
        print(f"📄 Report saved: {args.out}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
