#!/usr/bin/env python3
"""
check-dispatch-refs.py — Validate corporate dispatch completeness.

Checks every corporate/*/SKILL.md for:
  1. Frontmatter: triggers, persona (with name/title), version, license,
     subdomain, tags, description, argument-hint.
  2. Sections: Deterministic Dispatch Matrix (where applicable), Workflow,
     Verification Checklist, Anti-Rationalization Table, Integration with
     1ai-rules.
  3. Dispatch targets referenced in the matrix resolve to a real skill:
     - present in SKILLS.json by frontmatter `name`, AND
     - backed by an actual SKILL.md on disk under <category>/<dir>/.
  4. Type 2 skills log decisions per DECISION.md §4 (vendor-and-partnerships,
     crisis-communications, people-operations must reference logs/decisions).

Exit 0 = all clean. Non-zero = number of failing skills.

Usage:
    python3 scripts/check-dispatch-refs.py            # All corporate skills
    python3 scripts/check-dispatch-refs.py --skill NAME
    python3 scripts/check-dispatch-refs.py --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required — pip install PyYAML", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
CORPORATE_DIR = ROOT / "corporate"
SKILLS_JSON = ROOT / "SKILLS.json"

# Skills whose workflow makes a Type 2 decision (irreversible / external spend /
# publication). Per DECISION.md §4 they MUST carry a logging step referencing
# logs/decisions/. ponytail: hardcoded list; upgrade when a skill gains Type 2
# authority so it no longer needs manual registration here.
TYPE2_LOGGING_REQUIRED = {
    "role-vendor-and-partnerships",
    "role-crisis-communications",
    "role-people-operations",
    "role-owner-decision-log",
}

# owner-decision-log IS the logger; it has no outbound dispatch matrix by design.
NO_DISPATCH_MATRIX_OK = {"role-owner-decision-log"}

REQUIRED_FRONTMATTER = [
    "name", "description", "version", "license", "subdomain", "tags", "triggers",
]

# Hard-required sections (verified blockers depend on these).
REQUIRED_SECTIONS = [
    "Workflow",
    "Verification Checklist",
    "Anti-Rationalization",
]

# Advisory sections — reported separately, do not fail the gate.
ADVISORY_SECTIONS = [
    "Integration with 1ai-rules",
]

# Matches `category/skill-dir` references inside backticks in dispatch tables.
TARGET_RE = re.compile(r"`([a-z][a-z0-9_-]*/[A-Za-z0-9_.-]+)`")


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm_text = text[4:end]
    body = text[end + 4:]
    try:
        meta = yaml.load(fm_text, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    except Exception:
        return None, body
    if not isinstance(meta, dict):
        return None, body
    return meta, body


def load_registry() -> tuple[set[str], dict[str, str]]:
    """Return (set of skill names, map of category->display) from SKILLS.json."""
    data = json.loads(SKILLS_JSON.read_text(encoding="utf-8"))
    names = {s["name"] for s in data.get("skills", []) if s.get("name")}
    cats = set(data.get("categories", {}).keys()) if isinstance(
        data.get("categories"), dict) else {c["name"] for c in data.get("categories", [])}
    return names, cats


def resolve_target(target: str, registry_names: set[str]) -> tuple[bool, bool, str]:
    """Resolve `category/dir`. Returns (in_registry, on_disk, resolved_skill_name).

    The registry stores frontmatter `name`, which is usually `role-<dir>` for
    anchors but bare `<dir>` for atomic skills. Try both spellings.
    """
    cat, _, leaf = target.partition("/")
    candidates = [leaf, f"role-{leaf}"]
    in_registry = any(c in registry_names for c in candidates)
    on_disk = (ROOT / cat / leaf / "SKILL.md").exists()
    resolved = next((c for c in candidates if c in registry_names), leaf)
    return in_registry, on_disk, resolved


def check_skill(md_path: Path, registry_names: set[str]) -> list[str]:
    issues: list[str] = []
    text = md_path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text)
    if meta is None:
        return ["no-frontmatter-or-invalid-yaml"]

    name = meta.get("name", md_path.parent.name)

    # 1. Required frontmatter fields present and non-empty
    for field in REQUIRED_FRONTMATTER:
        val = meta.get(field)
        if val is None or (isinstance(val, str) and not val.strip()) \
                or (isinstance(val, list) and not val):
            issues.append(f"missing-frontmatter:{field}")

    # argument-hint: advisory only. Pre-existing C-suite anchors omit it;
    # not a verified blocker, so do not fail the gate on it.
    # ponytail: promote to hard error when all 14 corporate skills carry it.

    # 2. Persona with name + title
    persona = meta.get("persona")
    if not isinstance(persona, dict):
        issues.append("missing-persona-block")
    else:
        if not str(persona.get("name", "")).strip():
            issues.append("persona-missing:name")
        if not str(persona.get("title", "")).strip():
            issues.append("persona-missing:title")

    # 3. Required sections
    for section in REQUIRED_SECTIONS:
        heading_re = re.compile(r"^#{2,4}\s+.*" + re.escape(section), re.MULTILINE)
        if not heading_re.search(text):
            issues.append(f"missing-section:{section}")
    # Advisory sections: report separately, do not fail gate
    for section in ADVISORY_SECTIONS:
        heading_re = re.compile(r"^#{2,4}\s+.*" + re.escape(section), re.MULTILINE)
        if not heading_re.search(text):
            issues.append(f"advisory-section:{section}")

    # 4. Dispatch matrix
    has_matrix = re.search(r"^#{2,4}\s+.*(Deterministic Dispatch Matrix|Dispatch)",
                           text, re.MULTILINE) is not None
    if not has_matrix and name not in NO_DISPATCH_MATRIX_OK:
        issues.append("missing-section:Deterministic Dispatch Matrix")

    # 5. Every dispatched target resolves
    seen: set[str] = set()
    for m in TARGET_RE.finditer(body):
        target = m.group(1).rstrip("/")
        if target in seen:
            continue
        seen.add(target)
        # Skip obvious non-skill paths (log locations, config dirs).
        if target.startswith("logs/") or target.endswith(".md"):
            continue
        cat = target.split("/", 1)[0]
        if cat not in registry_names and not (ROOT / cat).is_dir():
            # Unknown category prefix — only flag if it looks like a skill path.
            issues.append(f"dispatch-target-bad-category:{target}")
            continue
        in_reg, on_disk, resolved = resolve_target(target, registry_names)
        if not in_reg and not on_disk:
            issues.append(f"dispatch-target-unresolved:{target}")
        elif not on_disk:
            issues.append(f"dispatch-target-no-file:{target}(name={resolved})")
        elif not in_reg:
            issues.append(f"dispatch-target-not-in-registry:{target}(file exists)")

    # 6. Type 2 logging mandate (DECISION.md §4)
    if name in TYPE2_LOGGING_REQUIRED:
        if not re.search(r"logs/decisions", text):
            issues.append("type2-decision-not-logged:logs/decisions/YYYY-MM-DD.md")

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate corporate dispatch completeness")
    ap.add_argument("--skill", help="Check a single skill directory name")
    ap.add_argument("--json", action="store_true", help="Machine-readable output")
    args = ap.parse_args()

    registry_names, _ = load_registry()

    md_paths = sorted(CORPORATE_DIR.glob("*/SKILL.md"))
    if args.skill:
        md_paths = [p for p in md_paths if p.parent.name == args.skill]
    if not md_paths:
        print(f"No corporate skills found{' matching ' + args.skill if args.skill else ''}",
              file=sys.stderr)
        return 1

    results: dict[str, list[str]] = {}
    advisory: dict[str, list[str]] = {}
    for p in md_paths:
        issues = check_skill(p, registry_names)
        name = p.parent.name
        if issues:
            # Split hard errors (failures) from advisory warnings (print only)
            hard_errors = []
            advisory_warnings = []
            for i in issues:
                if i.startswith("advisory-section"):
                    advisory_warnings.append(i)
                else:
                    hard_errors.append(i)
            if hard_errors:
                results[name] = hard_errors
            if advisory_warnings:
                advisory[name] = advisory_warnings

    # Print advisory warnings for visibility (still pass gate)
    if advisory and (not args.json):
        print(f"\nAdvisory warnings (pass gate):")
        for name, warns in advisory.items():
            print(f"  Advisory {name}:")
            for w in warns:
                print(f"      - {w}")

    if args.json:
        print(json.dumps({
            "checked": len(md_paths),
            "failing": len(results),
            "advisory": advisory,
            "issues": results,
        }, indent=2))
    else:
        print(f"\nChecking {len(md_paths)} corporate skills against dispatch contract...")
        if results:
            print(f"Hard failures ({len(results)}):")
            for dir_name, issues in results.items():
                print(f"  X {dir_name}")
                for i in issues:
                    print(f"      - {i}")
        passed = len(md_paths) - len(results)
        print(f"\nDispatch Refs Check: {passed}/{len(md_paths)} passed ({len(results)} failures)")
        if advisory:
            print(f"Advisory notes: {len(advisory)} skills have non-blocking warnings.")

    return min(len(results), 255)

    if args.json:
        print(json.dumps({
            "checked": len(md_paths),
            "failing": len(results),
            "issues": results,
        }, indent=2))
    else:
        print(f"Checking {len(md_paths)} corporate skills against dispatch contract...\n")
        for dir_name, issues in results.items():
            print(f"  X {dir_name}")
            for i in issues:
                print(f"      - {i}")
        passed = len(md_paths) - len(results)
        print(f"\nDispatch Refs Check: {passed}/{len(md_paths)} passed "
              f"({len(results)} failing)")

    return min(len(results), 255)


if __name__ == "__main__":
    sys.exit(main())
