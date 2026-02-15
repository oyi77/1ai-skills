#!/usr/bin/env python3
"""Lint SKILL.md files with actionable, grep-friendly output."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
REQUIRED_HEADINGS = [
    "## Overview",
    "## When to Use",
    "## When NOT to Use",
    "## Quick Reference",
    "## Common Mistakes",
]
WORKFLOW_VERBS = ["write", "run", "dispatch", "review", "commit", "execute"]
BANNED_PHRASES = ["ask your human", "manual review required", "have a human"]

WORD_COUNT_WARN = 500
WORD_COUNT_FAIL = 1200

FREQUENTLY_LOADED_SKILLS = {
    "using-superpowers",
    "writing-plans",
    "executing-plans",
    "verification-before-completion",
    "test-driven-development",
    "systematic-debugging",
    "dispatching-parallel-agents",
    "subagent-driven-development",
    "writing-skills",
}

WORD_COUNT_THRESHOLDS: dict[str, tuple[int, int]] = {
    "FREQUENTLY_LOADED": (300, 900),
    "OTHER": (WORD_COUNT_WARN, WORD_COUNT_FAIL),
}


@dataclass(frozen=True)
class LintIssue:
    path: str
    rule_id: str
    message: str
    is_error: bool = True


def discover_skill_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("SKILL.md") if path.is_file())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, int]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0

    closing = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            closing = idx
            break
    if closing is None:
        return None, 0

    raw = lines[1:closing]
    data: dict[str, str] = {}
    i = 0
    key_re = re.compile(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$")

    while i < len(raw):
        line = raw[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue

        match = key_re.match(line)
        if not match:
            i += 1
            continue

        key = match.group(1)
        value = match.group(2).strip()

        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            i += 1
            block_lines: list[str] = []
            while i < len(raw):
                next_line = raw[i]
                if key_re.match(next_line) and not next_line.startswith((" ", "\t")):
                    break
                block_lines.append(next_line.strip())
                i += 1
            collapsed = " ".join(part for part in block_lines if part)
            data[key] = collapsed
            continue

        data[key] = _strip_quotes(value)
        i += 1

    return data, closing + 1


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def word_count_category(path: Path, root: Path) -> str:
    rel_parts = path.relative_to(root).parts
    top_level_dir = rel_parts[0] if rel_parts else ""
    if top_level_dir in FREQUENTLY_LOADED_SKILLS:
        return "FREQUENTLY_LOADED"
    return "OTHER"


def lint_skill(path: Path, root: Path) -> list[LintIssue]:
    rel = path.relative_to(root).as_posix()
    text = read_text(path)
    issues: list[LintIssue] = []

    fm, _ = parse_frontmatter(text)
    if fm is None:
        issues.append(
            LintIssue(
                rel,
                "FRONTMATTER_MISSING",
                "Missing YAML frontmatter fence at file start",
            )
        )
    else:
        keys = set(fm.keys())
        extra = sorted(keys - ALLOWED_FRONTMATTER_KEYS)
        missing = sorted(ALLOWED_FRONTMATTER_KEYS - keys)

        if extra:
            issues.append(
                LintIssue(
                    rel,
                    "FRONTMATTER_EXTRA_KEYS",
                    f"Unsupported frontmatter keys: {', '.join(extra)}",
                )
            )
        if missing:
            issues.append(
                LintIssue(
                    rel,
                    "FRONTMATTER_MISSING_KEYS",
                    f"Missing frontmatter keys: {', '.join(missing)}",
                )
            )

        description = fm.get("description", "")
        if description and not description.startswith("Use when"):
            issues.append(
                LintIssue(
                    rel, "DESCRIPTION_PREFIX", "description must start with 'Use when'"
                )
            )

        if description:
            lowered = description.lower()
            for verb in WORKFLOW_VERBS:
                if re.search(rf"\b{re.escape(verb)}\b", lowered):
                    issues.append(
                        LintIssue(
                            rel,
                            "DESCRIPTION_WORKFLOW_VERB",
                            f"description appears workflow-oriented (contains '{verb}')",
                        )
                    )

    lines = text.splitlines()
    line_set = set(lines)
    for heading in REQUIRED_HEADINGS:
        if heading not in line_set:
            issues.append(
                LintIssue(
                    rel, "HEADING_MISSING", f"Missing required heading: {heading}"
                )
            )

    lowered_text = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lowered_text:
            issues.append(
                LintIssue(
                    rel,
                    "BANNED_HUMAN_VERIFICATION",
                    f"Contains banned phrase: '{phrase}'",
                )
            )

    category = word_count_category(path, root)
    warn_limit, fail_limit = WORD_COUNT_THRESHOLDS[category]
    total_words = word_count(text)
    if total_words > fail_limit:
        issues.append(
            LintIssue(
                rel,
                "WORD_COUNT_FAIL",
                f"word count {total_words} exceeds fail limit {fail_limit} (category={category})",
            )
        )
    elif total_words > warn_limit:
        issues.append(
            LintIssue(
                rel,
                "WORD_COUNT_WARN",
                f"word count {total_words} exceeds warn limit {warn_limit} (category={category})",
                is_error=False,
            )
        )

    return issues


def print_issues(issues: list[LintIssue]) -> None:
    for issue in issues:
        print(f"{issue.path}: {issue.rule_id}: {issue.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint SKILL.md files")
    parser.add_argument(
        "--list", action="store_true", help="List discovered SKILL.md files"
    )
    parser.add_argument(
        "--check", action="store_true", help="Run lint checks and report violations"
    )
    args = parser.parse_args()

    if not args.list and not args.check:
        parser.error("Specify at least one mode: --list and/or --check")

    skill_files = discover_skill_files(ROOT)

    if args.list:
        for path in skill_files:
            print(path.relative_to(ROOT).as_posix())

    if not args.check:
        return 0

    all_issues: list[LintIssue] = []
    for path in skill_files:
        all_issues.extend(lint_skill(path, ROOT))

    all_issues.sort(key=lambda i: (i.path, i.rule_id, i.message))
    print_issues(all_issues)
    has_errors = any(issue.is_error for issue in all_issues)
    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
