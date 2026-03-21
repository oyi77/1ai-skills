#!/usr/bin/env python3
"""
Master test runner for all autodroid skills.

Run:
    python3 run_all_tests.py                    # Run all skills
    python3 run_all_tests.py --skill kling      # Run only kling tests
    python3 run_all_tests.py --verbose          # Verbose output
    python3 run_all_tests.py --report /tmp/r.md # Save markdown report
    python3 run_all_tests.py --fail-fast        # Stop on first failure

Exit code: 0 if all pass, 1 if any fail, 2 if no tests found.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ─── Skill Directories ────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent

SKILL_DIRS = [
    "autodroid-kling-agent",
    "autodroid-grok-agent",
    "autodroid-flow-agent",
    "autodroid-pixverse-agent",
    "autodroid-instagram-agent",
    "autodroid-tiktok-agent",
    "autodroid-youtube-agent",
    "autodroid-whatsapp-agent",
    "ai-interceptor",
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def find_test_files(skill_dir: Path) -> list[Path]:
    """Find all test files in a skill directory."""
    test_files = []
    # Standard test locations
    for pattern in ["tests/test_*.py", "tests/*_test.py", "test_*.py"]:
        test_files.extend(skill_dir.glob(pattern))
    # Also check scripts/ for test files
    for pattern in ["scripts/test_*.py"]:
        test_files.extend(skill_dir.glob(pattern))
    return sorted(set(test_files))


def run_tests(skill_dir_name: str, verbose: bool = False) -> dict:
    """
    Run tests for a skill directory.

    Returns dict with keys:
        skill: str - skill name
        passed: int
        failed: int
        errors: int
        skipped: int
        test_files: list[str]
        output: str - combined stdout/stderr
        duration_ms: int
        status: "pass" | "fail" | "error" | "skip" | "no_tests"
    """
    skill_path = BASE_DIR / skill_dir_name
    result = {
        "skill": skill_dir_name,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "skipped": 0,
        "test_files": [],
        "output": "",
        "duration_ms": 0,
        "status": "no_tests",
    }

    if not skill_path.exists():
        result["status"] = "skip"
        result["output"] = f"Directory not found: {skill_path}"
        return result

    test_files = find_test_files(skill_path)
    if not test_files:
        result["status"] = "no_tests"
        result["output"] = "No test files found"
        return result

    result["test_files"] = [str(f.relative_to(BASE_DIR)) for f in test_files]

    all_output = []
    total_passed = 0
    total_failed = 0
    total_errors = 0
    total_skipped = 0
    any_fail = False

    start = time.time()

    for test_file in test_files:
        cmd = [
            sys.executable, "-m", "pytest",
            str(test_file),
            "--tb=short",
            "-q",
        ]
        if verbose:
            cmd.append("-v")

        # Add the skill's scripts dir to PYTHONPATH
        env = os.environ.copy()
        scripts_dir = skill_path / "scripts"
        if scripts_dir.exists():
            existing = env.get("PYTHONPATH", "")
            env["PYTHONPATH"] = f"{scripts_dir}{os.pathsep}{existing}" if existing else str(scripts_dir)

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                env=env,
                cwd=str(skill_path),
            )
            output = proc.stdout + proc.stderr
            all_output.append(f"=== {test_file.name} ===\n{output}")

            # Parse pytest summary line: "X passed, Y failed, Z error"
            for line in output.splitlines():
                line_lower = line.lower()
                if "passed" in line_lower or "failed" in line_lower or "error" in line_lower:
                    import re
                    for match in re.finditer(r"(\d+)\s+(passed|failed|error|skipped)", line_lower):
                        count, kind = int(match.group(1)), match.group(2)
                        if kind == "passed":
                            total_passed += count
                        elif kind == "failed":
                            total_failed += count
                            any_fail = True
                        elif kind == "error":
                            total_errors += count
                            any_fail = True
                        elif kind == "skipped":
                            total_skipped += count

            if proc.returncode != 0:
                any_fail = True

        except subprocess.TimeoutExpired:
            all_output.append(f"=== {test_file.name} ===\nTIMEOUT after 120s")
            total_errors += 1
            any_fail = True
        except FileNotFoundError:
            # pytest not installed — try running directly
            try:
                proc = subprocess.run(
                    [sys.executable, str(test_file)],
                    capture_output=True,
                    text=True,
                    timeout=120,
                    env=env,
                    cwd=str(skill_path),
                )
                output = proc.stdout + proc.stderr
                all_output.append(f"=== {test_file.name} (direct) ===\n{output}")
                if proc.returncode != 0:
                    any_fail = True
                    total_errors += 1
                else:
                    total_passed += 1
            except Exception as e:
                all_output.append(f"=== {test_file.name} ===\nERROR: {e}")
                total_errors += 1
                any_fail = True
        except Exception as e:
            all_output.append(f"=== {test_file.name} ===\nERROR: {e}")
            total_errors += 1
            any_fail = True

    result["duration_ms"] = int((time.time() - start) * 1000)
    result["passed"] = total_passed
    result["failed"] = total_failed
    result["errors"] = total_errors
    result["skipped"] = total_skipped
    result["output"] = "\n".join(all_output)

    if any_fail:
        result["status"] = "fail"
    else:
        result["status"] = "pass"

    return result


# ─── Report Generation ────────────────────────────────────────────────────────

def generate_report(results: list[dict]) -> str:
    """Generate markdown test report from results list."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# Autodroid Skills Test Report",
        f"",
        f"**Generated:** {now}  ",
        f"**Runner:** {sys.executable}  ",
        f"",
        "## Summary",
        "",
    ]

    total_pass = sum(1 for r in results if r["status"] == "pass")
    total_fail = sum(1 for r in results if r["status"] == "fail")
    total_no_tests = sum(1 for r in results if r["status"] == "no_tests")
    total_skip = sum(1 for r in results if r["status"] == "skip")
    total_tests_passed = sum(r["passed"] for r in results)
    total_tests_failed = sum(r["failed"] for r in results)
    total_tests_errors = sum(r["errors"] for r in results)

    overall = "✅ ALL PASS" if total_fail == 0 and total_tests_failed == 0 else "❌ FAILURES DETECTED"
    lines.append(f"**Overall:** {overall}  ")
    lines.append(f"**Skills:** {total_pass} pass / {total_fail} fail / {total_no_tests} no-tests / {total_skip} skip  ")
    lines.append(f"**Test Cases:** {total_tests_passed} passed / {total_tests_failed} failed / {total_tests_errors} errors  ")
    lines.append("")

    # Table
    lines.append("## Results Table")
    lines.append("")
    lines.append("| Skill | Status | Passed | Failed | Errors | Duration | Test Files |")
    lines.append("|-------|--------|--------|--------|--------|----------|------------|")

    for r in results:
        status_icon = {
            "pass": "✅ PASS",
            "fail": "❌ FAIL",
            "error": "💥 ERROR",
            "skip": "⚠️ SKIP",
            "no_tests": "📭 NO TESTS",
        }.get(r["status"], r["status"])

        files_str = ", ".join(Path(f).name for f in r.get("test_files", [])) or "-"
        lines.append(
            f"| {r['skill']} | {status_icon} | {r['passed']} | {r['failed']} | {r['errors']} | {r['duration_ms']}ms | {files_str} |"
        )

    lines.append("")

    # Detail sections for failures
    failures = [r for r in results if r["status"] in ("fail", "error")]
    if failures:
        lines.append("## Failure Details")
        lines.append("")
        for r in failures:
            lines.append(f"### ❌ {r['skill']}")
            lines.append("")
            lines.append("```")
            lines.append(r["output"][:3000])  # Truncate long outputs
            if len(r["output"]) > 3000:
                lines.append("... [truncated]")
            lines.append("```")
            lines.append("")

    # Skills with no tests
    no_test_skills = [r for r in results if r["status"] == "no_tests"]
    if no_test_skills:
        lines.append("## Skills Without Tests")
        lines.append("")
        for r in no_test_skills:
            lines.append(f"- `{r['skill']}` — {r['output']}")
        lines.append("")

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Master test runner for all autodroid skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 run_all_tests.py
  python3 run_all_tests.py --skill kling
  python3 run_all_tests.py --verbose
  python3 run_all_tests.py --report /tmp/test_report.md
  python3 run_all_tests.py --fail-fast
        """
    )
    parser.add_argument(
        "--skill", "-s",
        default=None,
        help="Run tests for a specific skill only (partial name match)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose test output"
    )
    parser.add_argument(
        "--report", "-r",
        default=None,
        help="Save markdown report to path"
    )
    parser.add_argument(
        "--fail-fast", "-x",
        action="store_true",
        help="Stop on first skill failure"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of human-readable"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all skill directories and exit"
    )
    args = parser.parse_args()

    # List mode
    if args.list:
        print("Configured skill directories:")
        for skill in SKILL_DIRS:
            path = BASE_DIR / skill
            exists = "✅" if path.exists() else "❌"
            print(f"  {exists} {skill}")
        return

    # Filter skills
    skills_to_run = SKILL_DIRS
    if args.skill:
        skills_to_run = [s for s in SKILL_DIRS if args.skill.lower() in s.lower()]
        if not skills_to_run:
            print(f"❌ No skill matching '{args.skill}' in configured list.")
            print(f"Available: {', '.join(SKILL_DIRS)}")
            sys.exit(2)

    print(f"🧪 Running tests for {len(skills_to_run)} skill(s)...")
    print(f"   Base dir: {BASE_DIR}")
    print()

    results = []
    any_failure = False

    for skill_name in skills_to_run:
        print(f"  ▶ {skill_name}...", end=" ", flush=True)
        result = run_tests(skill_name, verbose=args.verbose)
        results.append(result)

        status_line = {
            "pass": f"✅ PASS ({result['passed']} tests, {result['duration_ms']}ms)",
            "fail": f"❌ FAIL ({result['failed']} failed, {result['errors']} errors)",
            "skip": f"⚠️  SKIP (directory not found)",
            "no_tests": f"📭 NO TESTS",
            "error": f"💥 ERROR",
        }.get(result["status"], result["status"])

        print(status_line)

        if result["status"] in ("fail", "error"):
            any_failure = True
            if args.verbose and result["output"]:
                indent = "     "
                for line in result["output"].split("\n")[:50]:
                    print(f"{indent}{line}")
            if args.fail_fast:
                print(f"\n⛔ Stopping due to --fail-fast")
                break

    print()

    # Generate report
    report_md = generate_report(results)

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_md)
        print(f"📄 Report saved: {args.report}")

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        # Print summary
        total_pass = sum(1 for r in results if r["status"] == "pass")
        total_fail = sum(1 for r in results if r["status"] == "fail")
        total_tests_passed = sum(r["passed"] for r in results)
        total_tests_failed = sum(r["failed"] for r in results)
        total_tests_errors = sum(r["errors"] for r in results)

        print("=" * 50)
        print(f"SKILLS: {total_pass}/{len(results)} passed")
        print(f"TESTS:  {total_tests_passed} passed, {total_tests_failed} failed, {total_tests_errors} errors")
        if any_failure:
            print("STATUS: ❌ FAILURE")
        else:
            print("STATUS: ✅ ALL PASS")
        print("=" * 50)

    sys.exit(1 if any_failure else 0)


if __name__ == "__main__":
    main()
