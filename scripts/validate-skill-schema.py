#!/usr/bin/env python3
"""
validate-skill-schema.py — Schema validation for 1ai-skills.

Validates SKILL.md YAML frontmatter against schemas/skill.schema.json.
Applies defaults for missing fields, handles legacy domain→category mapping.

Usage:
    python3 scripts/validate-skill-schema.py                # Validate all skills
    python3 scripts/validate-skill-schema.py --skill NAME   # Single skill
    python3 scripts/validate-skill-schema.py --json         # Machine-readable output
    python3 scripts/validate-skill-schema.py --verbose      # Show all details, including clean
    python3 scripts/validate-skill-schema.py --summary      # Just summary, no per-skill detail
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required — pip install PyYAML", file=sys.stderr)
    sys.exit(2)

try:
    import jsonschema
    from jsonschema import ValidationError, validate
except ImportError:
    print("ERROR: jsonschema required — pip install jsonschema", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parent.parent

SKILL_DIRS = [
    "agents", "automation", "content", "core", "cybersecurity", "data",
    "development", "devops", "finance", "financial", "integrations",
    "marketing", "mcp", "meta", "mindset", "operations", "productivity",
    "research", "sales", "trading",
]

SCHEMA_PATH = ROOT / "schemas" / "skill.schema.json"

# Default values for fields not present in existing skills
DEFAULTS = {
    "schema_version": "1.0.0",
    "version": "0.1.0",
    "status": "active",
    "risk_level": "info",
    "human_approval": False,
    "author": "",
    "license": "MIT",
    "domain": None,
}

# Fields allowed in frontmatter that are NOT part of the schema schema.
ALLOWED_EXTRA = {"persona", "scripts", "language", "type"}


def load_schema() -> dict:
    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema not found at {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(2)
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def find_skills(filter_name: str | None = None) -> list[dict]:
    skills = []
    for d in SKILL_DIRS:
        dir_path = ROOT / d
        if not dir_path.is_dir():
            continue
        for md in sorted(dir_path.rglob("SKILL.md")):
            name = md.parent.name
            if filter_name and name != filter_name:
                continue
            skills.append({
                "name": name,
                "category": d,
                "path": md,
                "rel": str(md.parent.relative_to(ROOT)),
            })
    return skills


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm = text[4:end]
    body = text[end + 4:]
    return fm, body


def normalize_metadata(meta: dict) -> dict:
    # domain <-> category bridge
    if "category" not in meta and "domain" in meta:
        meta["category"] = meta["domain"]
    elif "domain" not in meta and "category" in meta:
        meta["domain"] = meta["category"]

    for field, default in DEFAULTS.items():
        if field not in meta or meta[field] is None or meta[field] == "":
            if default is not None:
                meta[field] = default

    return meta


def validate_skill(skill_info: dict, schema: dict) -> list[dict]:
    issues = []

    try:
        text = skill_info["path"].read_text(encoding="utf-8")
    except Exception as e:
        issues.append({"level": "error", "code": "read-error",
                       "message": f"Cannot read file: {e}"})
        return issues

    fm_raw, body = split_frontmatter(text)
    if fm_raw is None:
        issues.append({"level": "error", "code": "no-frontmatter",
                       "message": "No YAML frontmatter found (file must start with ---)"})
        return issues

    try:
        meta = yaml.load(fm_raw, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader)) or {}
    except Exception as e:
        issues.append({"level": "error", "code": "yaml-parse-error",
                       "message": f"YAML parse failed: {e}"})
        return issues

    if not isinstance(meta, dict):
        issues.append({"level": "error", "code": "not-a-dict",
                       "message": "Frontmatter did not parse as a YAML mapping"})
        return issues

    # Warn about extra non-schema fields
    schema_props = set(schema.get("properties", {}).keys())
    known = schema_props | ALLOWED_EXTRA
    for f in sorted(meta):
        if f not in known and not f.startswith("_"):
            issues.append({"level": "info", "code": "extra-field",
                           "message": f"Unknown frontmatter field: '{f}'"})

    meta = normalize_metadata(meta)

    # Frontmatter name vs directory
    dir_name = skill_info["path"].parent.name
    fm_name = meta.get("name", "")
    if fm_name and fm_name != dir_name:
        issues.append({"level": "warning", "code": "name-mismatch",
                       "message": f"Frontmatter name '{fm_name}' != directory '{dir_name}'"})

    # JSON Schema validation
    try:
        validate(instance=meta, schema=schema)
    except ValidationError as e:
        path_str = ".".join(str(p) for p in e.absolute_path)
        issues.append({"level": "error", "code": "schema-violation",
                       "message": f"{path_str}: {e.message}"})

    # Manual checks beyond schema expressiveness

    # Description quality
    desc = meta.get("description", "")
    if len(desc) < 30:
        issues.append({"level": "warning", "code": "desc-too-short",
                       "message": f"Description is {len(desc)} chars (min 30)"})
    if len(desc) > 500:
        issues.append({"level": "warning", "code": "desc-too-long",
                       "message": f"Description is {len(desc)} chars (max 500)"})
    if not re.search(r"\buse when\b", desc.lower()):
        issues.append({"level": "warning", "code": "no-trigger-phrase",
                       "message": "Description lacks 'Use when' trigger phrase"})

    # Tags
    tags = meta.get("tags", [])
    if not tags:
        issues.append({"level": "warning", "code": "missing-tags",
                       "message": "No tags in frontmatter"})

    # Category matches directory
    cat = skill_info["category"]
    fm_cat = meta.get("category", "")
    finance_group = {"finance", "financial"}
    if fm_cat and fm_cat != cat and {fm_cat, cat} != finance_group:
        issues.append({"level": "warning", "code": "category-mismatch",
                       "message": f"Frontmatter category '{fm_cat}' != directory '{cat}'"})

    # Version sanity check (schema checks semver, this catches values like "0.01")
    version = meta.get("version", "")
    if version and not re.match(r"^\d+\.\d+(\.\d+)?$", str(version)):
        issues.append({"level": "warning", "code": "bad-version",
                       "message": f"Invalid version format: '{version}' (expect semver)"})

    # Risk/human-approval consistency
    risk = meta.get("risk_level", "info")
    ha = meta.get("human_approval", False)
    if risk in ("high", "critical") and ha is not True:
        issues.append({"level": "error", "code": "risk-no-approval",
                       "message": f"Risk level '{risk}' requires human_approval: true"})

    return issues


def print_report(results: list[dict], args):
    total = len(results)
    errors = [r for r in results if any(i["level"] == "error" for i in r["issues"])]
    warnings = [r for r in results if not any(i["level"] == "error" for i in r["issues"])
                and any(i["level"] == "warning" for i in r["issues"])]
    clean = [r for r in results if not r["issues"]]

    if args.json:
        report = {
            "total": total,
            "clean": len(clean),
            "warnings": len(warnings),
            "errors": len(errors),
            "results": results,
        }
        print(json.dumps(report, indent=2))
        return

    if not args.summary:
        for r in results:
            if not r["issues"]:
                if args.verbose:
                    print(f"  V {r['skill']} ({r['category']})")
                continue
            else:
                level = "X" if any(i["level"] == "error" for i in r["issues"]) else "!"
                print(f"  {level} {r['skill']} ({r['category']})")
                for issue in r["issues"]:
                    icon = {"error": "  E", "warning": "  W", "info": "  I"}
                    print(f"     {icon.get(issue['level'], '  ?')} [{issue['code']}] {issue['message']}")

    print()
    passed = total - len(errors)
    print(f"Schema Validation: {passed}/{total} passed ({len(errors)} errors, {len(warnings)} warnings)")
    if args.summary:
        print(f"  Clean: {len(clean)}, Warnings only: {len(warnings)}, Errors: {len(errors)}")


def main():
    parser = argparse.ArgumentParser(description="Validate 1ai-skills against schema")
    parser.add_argument("--skill", help="Validate only one skill by name")
    parser.add_argument("--json", action="store_true",
                        help="Machine-readable JSON output")
    parser.add_argument("--verbose", action="store_true",
                        help="Show all details including clean skills")
    parser.add_argument("--summary", action="store_true",
                        help="Summary only, no per-skill detail")
    args = parser.parse_args()

    schema = load_schema()
    skills = find_skills(args.skill)

    if not skills:
        print(f"No skills found{' matching ' + args.skill if args.skill else ''}")
        sys.exit(1)

    if not args.json:
        print(f"Validating {len(skills)} skills against {SCHEMA_PATH.name}...\n")

    results = []
    for s in skills:
        issues = validate_skill(s, schema)
        results.append({
            "skill": s["name"],
            "category": s["category"],
            "path": s["rel"],
            "issues": issues,
        })

    print_report(results, args)

    has_errors = any(
        any(i["level"] == "error" for i in r["issues"])
        for r in results
    )
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
