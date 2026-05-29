#!/usr/bin/env python3
"""
test_quality.py — Quality test suite for all SKILL.md files.

Validates structural integrity, content quality, and consistency
across all 1284+ skill definitions.

Usage:
    python3 scripts/test_quality.py          # human-readable output
    python3 scripts/test_quality.py --json   # JSON report to stdout

Exit code 0 = all pass, 1 = failures found.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

SKILL_DIRS = [
    "agents", "automation", "content", "core", "cybersecurity", "data",
    "development", "devops", "financial", "integrations", "marketing",
    "mcp", "meta", "operations", "productivity", "research", "sales",
    "trading",
]

# Sections that count toward the "at least 3 of these" requirement
QUALITY_SECTIONS = {
    "When to Use", "Red Flags", "Verification", "How to Use",
    "Common Rationalizations",
}

MIN_LINES = 50
MIN_DESC_LEN = 20

# Pattern for cross-references like `category/skill-name`
CROSS_REF_RE = re.compile(r"`([a-z][a-z0-9-]*/[a-z][a-z0-9-]*(?:/[a-z][a-z0-9-]*)*)`")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_all_skill_paths() -> list[Path]:
    """Walk SKILL_DIRS and collect every SKILL.md path."""
    paths: list[Path] = []
    for d in SKILL_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for p in base.rglob("SKILL.md"):
            paths.append(p)
    return sorted(paths)


def parse_frontmatter(text: str) -> tuple[dict | None, str | None, str]:
    """Return (metadata_dict_or_None, error_string, body).

    Handles both valid and invalid frontmatter gracefully.
    """
    if not text.startswith("---"):
        return None, "missing leading ---", text

    # Find closing ---
    lines = text.split("\n")
    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            close_idx = i
            break

    if close_idx is None:
        return None, "missing closing ---", text

    fm_text = "\n".join(lines[1:close_idx])
    body = "\n".join(lines[close_idx + 1:])

    # Simple YAML parser (no PyYAML dependency) — handles flat key: value
    meta: dict[str, str] = {}
    current_key = None
    current_value_lines: list[str] = []

    for line in fm_text.split("\n"):
        # Detect top-level key: value
        m = re.match(r"^([a-zA-Z_][\w-]*):\s*(.*)", line)
        if m and not line.startswith(("  ", "\t")):
            # Save previous key
            if current_key is not None:
                meta[current_key] = "\n".join(current_value_lines).strip()
            current_key = m.group(1)
            val = m.group(2).strip()
            # Strip surrounding quotes
            if len(val) >= 2 and val[0] in ('"', "'") and val[-1] == val[0]:
                val = val[1:-1]
            current_value_lines = [val] if val else []
        elif current_key is not None:
            # Continuation line (list item, multi-line value)
            current_value_lines.append(line)

    if current_key is not None:
        meta[current_key] = "\n".join(current_value_lines).strip()

    return meta, None, body


def count_lines(text: str) -> int:
    """Count non-empty lines."""
    return sum(1 for line in text.split("\n") if line.strip())


def find_sections(body: str) -> list[str]:
    """Extract all ## section headers from body."""
    sections = []
    for m in re.finditer(r"^##\s+(.+?)\s*$", body, re.MULTILINE):
        sections.append(m.group(1).strip())
    return sections


def find_empty_sections(body: str) -> list[str]:
    """Find section headers immediately followed by another header (empty section)."""
    empty = []
    lines = body.split("\n")
    for i, line in enumerate(lines):
        hdr = re.match(r"^##\s+(.+?)\s*$", line)
        if not hdr:
            continue
        # Look at next non-empty line
        for j in range(i + 1, len(lines)):
            if lines[j].strip():
                if re.match(r"^#{1,6}\s+", lines[j]):
                    empty.append(hdr.group(1).strip())
                break
    return empty


def find_cross_refs(body: str) -> list[str]:
    """Extract cross-references like `category/skill-name`."""
    return CROSS_REF_RE.findall(body)


# ---------------------------------------------------------------------------
# Validation (runs per-file, designed for parallelism)
# ---------------------------------------------------------------------------

def validate_skill(path: str) -> dict:
    """Validate a single SKILL.md. Returns result dict."""
    p = Path(path)
    rel = str(p.relative_to(ROOT))
    errors: list[str] = []
    warnings: list[str] = []

    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"path": rel, "status": "fail", "errors": [f"unreadable: {e}"], "warnings": []}

    # --- Structural checks ---
    meta, fm_err, body = parse_frontmatter(text)

    if fm_err:
        errors.append(f"frontmatter: {fm_err}")
        return {"path": rel, "status": "fail", "errors": errors, "warnings": warnings}

    if meta is None:
        errors.append("frontmatter: could not parse")
        return {"path": rel, "status": "fail", "errors": errors, "warnings": warnings}

    # Required fields
    name = meta.get("name", "")
    desc = meta.get("description", "")

    if not name or not isinstance(name, str) or not name.strip():
        errors.append("missing 'name' field in frontmatter")
    else:
        # Name must match directory name
        dir_name = p.parent.name
        if name.strip() != dir_name:
            errors.append(f"name mismatch: frontmatter='{name.strip()}' vs dir='{dir_name}'")

    if not desc or not isinstance(desc, str) or not desc.strip():
        errors.append("missing 'description' field in frontmatter")
    elif len(desc.strip()) <= MIN_DESC_LEN:
        errors.append(f"description too short ({len(desc.strip())} chars, need >{MIN_DESC_LEN})")

    # Minimum line count
    line_count = count_lines(text)
    if line_count < MIN_LINES:
        errors.append(f"too few lines ({line_count}, need >={MIN_LINES})")

    # Section checks
    sections = find_sections(body)
    matched_quality = [s for s in sections if s in QUALITY_SECTIONS]
    if len(matched_quality) < 3:
        # Also accept close variants (with trailing colon, exclamation, etc.)
        normalized = {s.rstrip(":!").strip() for s in sections}
        for qs in QUALITY_SECTIONS:
            if qs in normalized and qs not in matched_quality:
                matched_quality.append(qs)
        if len(matched_quality) < 3:
            errors.append(
                f"need >=3 quality sections (have {len(matched_quality)}): "
                f"found {[s for s in matched_quality]}; "
                f"need from: {sorted(QUALITY_SECTIONS)}"
            )

    # --- Content quality checks ---
    # Ignore [TODO] when inside checklist items (e.g., "- [ ] No [TODO] or placeholder")
    todo_lines = [line for line in text.splitlines() if "[TODO]" in line and not re.match(r'^\s*-\s*\[', line)]
    if todo_lines:
        errors.append(f"contains {len(todo_lines)} [TODO] marker(s)")

    empty = find_empty_sections(body)
    if empty:
        errors.append(f"empty sections (header-only): {empty[:5]}")

    # --- Consistency: collect cross-refs for later validation ---
    cross_refs = find_cross_refs(body)

    if errors:
        return {"path": rel, "status": "fail", "errors": errors, "warnings": warnings, "cross_refs": cross_refs}

    return {"path": rel, "status": "pass", "errors": [], "warnings": warnings, "cross_refs": cross_refs}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Quality test suite for SKILL.md files")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    parser.add_argument("--workers", type=int, default=None, help="Parallel workers (default: cpu count)")
    args = parser.parse_args()

    t0 = time.monotonic()

    # Discover all skills
    skill_paths = find_all_skill_paths()
    total = len(skill_paths)

    if total == 0:
        print("ERROR: No SKILL.md files found!", file=sys.stderr)
        return 1

    # Validate in parallel
    path_strs = [str(p) for p in skill_paths]
    results: list[dict] = []
    max_workers = args.workers or min(os.cpu_count() or 4, 8)

    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(validate_skill, ps): ps for ps in path_strs}
        for future in as_completed(futures):
            results.append(future.result())

    # Build directory of all existing skills for cross-ref validation
    existing_skills: set[str] = set()
    for p in skill_paths:
        rel = str(p.relative_to(ROOT))
        # e.g. "financial/earnings-viewer/SKILL.md" -> "financial/earnings-viewer"
        existing_skills.add(rel.replace("/SKILL.md", ""))

    # Cross-reference validation (second pass)
    cross_ref_errors: dict[str, list[str]] = {}
    for r in results:
        refs = r.get("cross_refs", [])
        if not refs:
            continue
        bad_refs = []
        for ref in refs:
            if ref not in existing_skills:
                bad_refs.append(ref)
        if bad_refs:
            cross_ref_errors[r["path"]] = [f"broken cross-refs: {bad_refs}"]
            if r["status"] == "pass":
                r["status"] = "fail"
            r["errors"].extend([f"broken cross-ref: `{ref}`" for ref in bad_refs])

    # Sort results by path for deterministic output
    results.sort(key=lambda r: r["path"])

    passed = sum(1 for r in results if r["status"] == "pass")
    failed = sum(1 for r in results if r["status"] == "fail")
    elapsed = time.monotonic() - t0

    # Collect error type stats
    error_counts: Counter[str] = Counter()
    for r in results:
        for e in r["errors"]:
            # Normalize error message to category
            cat = e.split(":")[0].split("(")[0].strip()
            error_counts[cat] += 1

    if args.json:
        report = {
            "total": total,
            "passed": passed,
            "failed": failed,
            "elapsed_seconds": round(elapsed, 2),
            "error_summary": dict(error_counts.most_common()),
            "failures": [
                {"path": r["path"], "errors": r["errors"]}
                for r in results if r["status"] == "fail"
            ],
        }
        print(json.dumps(report, indent=2))
    else:
        # Human-readable output
        print(f"\n{'='*60}")
        print(f"  1ai-skills Quality Test Suite")
        print(f"{'='*60}")
        print(f"  Total:  {total}")
        print(f"  Passed: {passed}")
        print(f"  Failed: {failed}")
        print(f"  Time:   {elapsed:.1f}s")
        print(f"{'='*60}")

        if failed > 0:
            print(f"\n{'-'*60}")
            print(f"  Error Summary")
            print(f"{'-'*60}")
            for cat, cnt in error_counts.most_common():
                print(f"  {cnt:>5}  {cat}")

            print(f"\n{'-'*60}")
            print(f"  Failures (showing all {failed})")
            print(f"{'-'*60}")
            for r in results:
                if r["status"] == "fail":
                    print(f"\n  {r['path']}")
                    for e in r["errors"]:
                        print(f"    - {e}")

        print()

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
