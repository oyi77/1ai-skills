#!/usr/bin/env python3
"""
lint-skills.py — Quality linter for 1ai-skills.

Checks beyond basic validation:
  - Duplicate / near-duplicate skill names
  - Description quality (too short, generic, missing trigger phrases)
  - Missing tags
  - Cross-reference validation (skill:// links that point to nonexistent skills)
  - Structural completeness (required sections present)

Also generates an enriched SKILLS.json with per-skill metadata for fast
agent discovery.

Usage:
    python3 scripts/lint-skills.py              # lint only
    python3 scripts/lint-skills.py --write       # lint + update SKILLS.json
    python3 scripts/lint-skills.py --json        # machine-readable output
    python3 scripts/lint-skills.py --fix-report  # print fixable issues
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required — pip install PyYAML", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent

SKILL_DIRS = [
    "agents", "automation", "content", "core", "cybersecurity", "data",
    "development", "devops", "financial", "integrations", "marketing",
    "mcp", "meta", "mindset", "operations", "productivity", "research",
    "sales", "trading",
]

# ── Thresholds ──────────────────────────────────────────────────────────
MIN_DESC_LENGTH = 30          # characters
MAX_DESC_LENGTH = 500         # characters
SIMILARITY_THRESHOLD = 0.99   # for near-duplicate detection
REQUIRED_SECTIONS = {"## When to Use"}
RECOMMENDED_SECTIONS = {"## Overview", "## Process", "## Verification"}

GENERIC_DESCS = {
    "ai agent skill", "skill for agents", "automation skill",
    "use this skill when", "agent skill",
}


# ── Helpers ─────────────────────────────────────────────────────────────
def find_skills() -> list[Path]:
    found = []
    for d in SKILL_DIRS:
        p = ROOT / d
        if p.is_dir():
            found.extend(p.rglob("SKILL.md"))
    return sorted(found)


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---"):
        return None, text
    # find closing ---
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm = text[4:end]
    body = text[end + 4:]
    return fm, body


def extract_metadata(path: Path) -> dict | None:
    """Extract frontmatter metadata from a SKILL.md file."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    fm, body = split_frontmatter(text)
    if fm is None:
        return None
    try:
        meta = yaml.safe_load(fm) or {}
    except Exception:
        return None
    if not isinstance(meta, dict):
        return None
    meta["_path"] = str(path.relative_to(ROOT))
    meta["_body"] = body
    meta["_text"] = text
    return meta


def skill_rel_path(path: Path) -> str:
    """Return relative path like 'category/skill-name'."""
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"
    return str(rel)


def similarity(a: str, b: str) -> float:
    """Sequence-based similarity ratio."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def levenshtein_ratio(s1: str, s2: str) -> float:
    """Fast Levenshtein similarity (0-1)."""
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    if len(s2) == 0:
        return 0.0
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            cost = 0 if c1 == c2 else 1
            curr.append(min(
                curr[j] + 1,          # insert
                prev[j + 1] + 1,      # delete
                prev[j] + cost,        # replace
            ))
        prev = curr
    dist = prev[-1]
    max_len = max(len(s1), len(s2))
    return 1.0 - (dist / max_len)


# ── Lint Checks ─────────────────────────────────────────────────────────
class LintResult:
    def __init__(self):
        self.errors: list[dict] = []       # must fix
        self.warnings: list[dict] = []     # should fix
        self.info: list[dict] = []         # nice to fix
        self.stats: dict = {}

    def add(self, level: str, skill: str, code: str, message: str):
        entry = {"skill": skill, "code": code, "message": message}
        getattr(self, level if level in ("errors", "warnings", "info") else "info").append(entry)

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def summary(self) -> str:
        lines = []
        lines.append(f"Lint: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.info)} info")
        if self.stats:
            for k, v in self.stats.items():
                lines.append(f"  {k}: {v}")
        return "\n".join(lines)


def check_description_quality(meta: dict, result: LintResult):
    """Check description length and quality."""
    skill = meta.get("name", meta["_path"])
    desc = meta.get("description", "")

    if not desc:
        return

    if len(desc) < MIN_DESC_LENGTH:
        result.add("warnings", skill, "desc-too-short",
                    f"Description only {len(desc)} chars (min {MIN_DESC_LENGTH})")

    if len(desc) > MAX_DESC_LENGTH:
        result.add("warnings", skill, "desc-too-long",
                    f"Description is {len(desc)} chars (max {MAX_DESC_LENGTH})")

    desc_lower = desc.lower()
    for generic in GENERIC_DESCS:
        if desc_lower.startswith(generic) or desc_lower == generic:
            result.add("warnings", skill, "desc-generic",
                        f"Description is generic: '{desc[:60]}...'")
            break

    # Check for trigger phrases ("Use when", "Use for", etc.)
    trigger_patterns = [
        r"\buse when\b", r"\buse for\b", r"\btriggers? on\b",
        r"\bcovers?\b", r"\bautomate[ds]?\b", r"\bgenerat[es]+\b",
    ]
    has_trigger = any(re.search(p, desc_lower) for p in trigger_patterns)
    if not has_trigger:
        result.add("info", skill, "desc-no-trigger",
                    "Description lacks trigger phrase (e.g., 'Use when...')")


def check_tags(meta: dict, result: LintResult):
    """Check for missing or empty tags."""
    skill = meta.get("name", meta["_path"])
    tags = meta.get("tags")

    if tags is None:
        result.add("info", skill, "missing-tags", "No tags in frontmatter")
    elif isinstance(tags, list) and len(tags) == 0:
        result.add("info", skill, "empty-tags", "Tags list is empty")


def check_sections(body: str, skill: str, result: LintResult):
    """Check for required and recommended sections."""
    if not body:
        return

    # Extract H2 headers
    headers = set()
    for line in body.splitlines():
        if line.startswith("## "):
            headers.add(line.strip())

    for section in REQUIRED_SECTIONS:
        if section not in headers:
            result.add("warnings", skill, "missing-section",
                        f"Missing required section: {section}")

    for section in RECOMMENDED_SECTIONS:
        if section not in headers:
            result.add("info", skill, "missing-recommended-section",
                        f"Missing recommended section: {section}")


def check_duplicates(skills_meta: list[dict], result: LintResult):
    """Detect duplicate and near-duplicate skill names."""
    names = [(m.get("name", ""), m["_path"]) for m in skills_meta]

    # Exact duplicates
    seen = {}
    for name, path in names:
        if name in seen:
            result.add("errors", name, "duplicate-name",
                        f"Duplicate skill name: also in {seen[name]}")
        seen[name] = path

    # Near-duplicates (only check within same category for relevance)
    by_category: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for name, path in names:
        parts = Path(path).parts
        cat = parts[0] if parts else "unknown"
        by_category[cat].append((name, path))

    for cat, cat_skills in by_category.items():
        for i, (name1, path1) in enumerate(cat_skills):
            for name2, path2 in cat_skills[i + 1:]:
                # Fast length-based pre-check for performance
                if 2.0 * min(len(name1), len(name2)) < SIMILARITY_THRESHOLD * (len(name1) + len(name2)):
                    continue
                sim = similarity(name1, name2)
                if sim >= SIMILARITY_THRESHOLD and name1 != name2:
                    result.add("warnings", name1, "near-duplicate",
                                f"Near-duplicate of {name2} (similarity={sim:.2f})")


def check_cross_references(skills_meta: list[dict], result: LintResult):
    """Check that skill:// links in body text point to real skills."""
    all_names = {m.get("name") for m in skills_meta if m.get("name")}

    skill_link_re = re.compile(r"skill://([a-z0-9-]+)")

    for meta in skills_meta:
        body = meta.get("_body", "")
        if not body:
            continue

        skill = meta.get("name", meta["_path"])
        for match in skill_link_re.finditer(body):
            target = match.group(1)
            if target not in all_names:
                result.add("warnings", skill, "broken-skill-ref",
                            f"References nonexistent skill: skill://{target}")


def check_stub_descriptions(skills_meta: list[dict], result: LintResult):
    """Flag descriptions that look like auto-generated stubs."""
    stub_patterns = [
        r"^ai.?agent",
        r"^skill for",
        r"^use this skill",
        r"^todo[:\s]",
        r"^placeholder",
        r"^tbd",
        r"^lorem",
    ]
    for meta in skills_meta:
        desc = (meta.get("description") or "").strip().lower()
        skill = meta.get("name", meta["_path"])
        for pat in stub_patterns:
            if re.match(pat, desc):
                result.add("warnings", skill, "stub-description",
                            f"Stub description: '{desc[:60]}'")
                break


# ── Search Index Generation ─────────────────────────────────────────────
def build_search_index(skills_meta: list[dict]) -> dict:
    """Build enriched SKILLS.json with per-skill metadata."""
    categories: dict[str, list] = defaultdict(list)
    all_skills = []

    for meta in skills_meta:
        name = meta.get("name", "")
        if not name:
            continue

        parts = Path(meta["_path"]).parts
        category = parts[0] if parts else "unknown"

        entry = {
            "name": name,
            "category": category,
            "description": meta.get("description", ""),
            "domain": meta.get("domain", category),
            "tags": meta.get("tags", []),
        }

        # Add persona if present
        persona = meta.get("persona")
        if isinstance(persona, dict):
            entry["persona"] = persona.get("name", "")

        all_skills.append(entry)
        categories[category].append(entry)

    # Sort for deterministic output
    all_skills.sort(key=lambda s: (s["category"], s["name"]))
    for cat in categories:
        categories[cat].sort(key=lambda s: s["name"])

    # Build final structure
    return {
        "total_skills": len(all_skills),
        "category_count": len(categories),
        "categories": {cat: len(skills) for cat, skills in sorted(categories.items())},
        "skills": all_skills,
        "tooling_dirs": ["docs", "hooks", "manifests", "references", "scripts"],
    }


# ── Main ────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description="Quality linter for 1ai-skills")
    ap.add_argument("--write", action="store_true",
                    help="Write enriched SKILLS.json")
    ap.add_argument("--json", action="store_true",
                    help="Machine-readable JSON output")
    ap.add_argument("--fix-report", action="store_true",
                    help="Print fixable issues only")
    ap.add_argument("--category", type=str, default=None,
                    help="Lint only one category (e.g., 'content')")
    args = ap.parse_args()

    skills = find_skills()
    if args.category:
        skills = [s for s in skills if s.relative_to(ROOT).parts[0] == args.category]

    print(f"Linting {len(skills)} skills...")

    # Extract metadata for all skills
    skills_meta: list[dict] = []
    for path in skills:
        meta = extract_metadata(path)
        if meta:
            skills_meta.append(meta)

    result = LintResult()

    # Individual checks
    for meta in skills_meta:
        skill = meta.get("name", meta["_path"])
        check_description_quality(meta, result)
        check_tags(meta, result)
        check_sections(meta.get("_body", ""), skill, result)

    # Cross-skill checks
    check_duplicates(skills_meta, result)
    check_cross_references(skills_meta, result)
    check_stub_descriptions(skills_meta, result)

    # Stats
    result.stats["total_skills"] = len(skills_meta)
    result.stats["with_tags"] = sum(1 for m in skills_meta if m.get("tags"))
    result.stats["avg_desc_length"] = (
        int(sum(len(m.get("description") or "") for m in skills_meta) / max(len(skills_meta), 1))
    )

    # Output
    if args.json:
        output = {
            "errors": result.errors,
            "warnings": result.warnings,
            "info": result.info,
            "stats": result.stats,
        }
        print(json.dumps(output, indent=2))
    elif args.fix_report:
        for entry in result.errors + result.warnings:
            print(f"[{entry['code']}] {entry['skill']}: {entry['message']}")
    else:
        # Human-readable
        if result.errors:
            print(f"\n=== ERRORS ({len(result.errors)}) ===")
            for e in result.errors:
                print(f"  ❌ [{e['code']}] {e['skill']}: {e['message']}")

        if result.warnings:
            print(f"\n=== WARNINGS ({len(result.warnings)}) ===")
            for w in result.warnings:
                print(f"  ⚠️  [{w['code']}] {w['skill']}: {w['message']}")

        if result.info:
            print(f"\n=== INFO ({len(result.info)}) ===")
            for i in result.info:
                print(f"  ℹ️  [{i['code']}] {i['skill']}: {i['message']}")

        print(f"\n{result.summary()}")

    # Write enriched SKILLS.json
    if args.write:
        index = build_search_index(skills_meta)
        out = ROOT / "SKILLS.json"
        out.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        print(f"\nWrote {out} ({index['total_skills']} skills, {len(index['skills'])} indexed)")

    return 1 if result.has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
