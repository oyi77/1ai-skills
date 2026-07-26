#!/usr/bin/env python3
"""
audit-skills.py — Deep quality audit for 1ai-skills.

Per-skill metrics: frontmatter quality, body structure, content depth,
cross-reference health, code quality, stub detection, security red flags.

Output: JSON report + terminal summary with prioritized fix list.

Usage:
    python3 scripts/audit-skills.py                         # summary table
    python3 scripts/audit-skills.py --json                  # full JSON report
    python3 scripts/audit-skills.py --json -o report.json   # write to file
    python3 scripts/audit-skills.py --fix-report            # actionable fix list
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import ast
import io
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required — pip install PyYAML", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent

SKILL_DIRS = [
    "agents", "automation", "content", "core", "cybersecurity", "data",
    "development", "devops", "finance", "financial", "integrations",
    "marketing", "mcp", "meta", "mindset", "operations", "productivity",
    "research", "sales", "trading",
]

# ── Scoring weights ──────────────────────────────────────────────────────
WEIGHTS = {
    "frontmatter_complete": 15,
    "trigger_phrase": 8,
    "tags_present": 5,
    "version_present": 3,
    "category_matches_dir": 5,
    "domain_matches_dir": 3,
    "req_sections_present": 15,
    "recomm_sections_present": 5,
    "content_depth": 12,
    "code_blocks": 10,
    "anti_rat_rows": 5,
    "cross_refs_valid": 5,
    "no_stub": 5,
    "no_security_redflags": 4,
}

MAX_SCORE = sum(WEIGHTS.values())  # 100

# ── Required/recommended sections ────────────────────────────────────────
REQUIRED_SECTIONS = {"## When to Use", "## Anti-Rationalization Table"}
RECOMMENDED_SECTIONS = {"## Overview", "## Process", "## Verification Checklist"}

TRIGGER_PHRASES = {
    "use when", "triggers on", "covers", "activates for",
    "use for", "automated", "generates",
}

SECURITY_PATTERNS = re.compile(
    r"(?:sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|"
    r"rm\s+-rf\s+/\s*$|DROP\s+TABLE|"
    r"(?:subprocess|os\.system)\s*\(|"
    r"(?:exec|eval)\s*\()",
    re.IGNORECASE,
)

SKILL_LINK_RE = re.compile(r"skill://([\w-]+)")


# ── Helpers ──────────────────────────────────────────────────────────────
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
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm = text[4:end]
    body = text[end + 4:]
    return fm, body


def parse_meta(text: str) -> dict | None:
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError:
        return None

def count_code_blocks(body: str) -> dict:
    fences = re.findall(r"```(\w*)\n(.*?)```", body, re.DOTALL)
    total_lines = 0
    by_lang: dict[str, int] = {}
    for lang, code in fences:
        lang = lang or "text"
        lines = code.count("\n") + 1
        total_lines += lines
        by_lang[lang] = by_lang.get(lang, 0) + lines
    return {
        "count": len(fences),
        "total_lines": total_lines,
        "by_language": by_lang,
    }


def count_anti_rat_rows(body: str) -> int:
    """Count filled rows in anti-rationalization tables."""
    if "## Anti-Rationalization Table" not in body:
        return 0
    # Find the table after the header
    m = re.search(r"## Anti-Rationalization Table\n(.+?)(?=\n## |\n---|\Z)", body, re.DOTALL)
    if not m:
        return 0
    section = m.group(1)
    rows = 0
    for line in section.split("\n"):
        line = line.strip()
        # Count data rows: | text | text |
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            # Skip header/separator rows
            if any(c and c != "---" and "Rationalization" not in c for c in cells):
                rows += 1
    return rows


def count_words(text: str) -> int:
    return len(text.split())


def extract_sections(body: str) -> dict[str, int]:
    """Return {section_name: line_number} for all ## headings."""
    sections = {}
    for i, line in enumerate(body.split("\n")):
        m = re.match(r"^## (.+)", line.strip())
        if m:
            sections[m.group(1).strip()] = i + 1
    return sections


def check_skill_links(body: str, skill_names: set[str]) -> list[dict]:
    issues = []
    for m in SKILL_LINK_RE.finditer(body):
        target = m.group(1)
        if target not in skill_names:
            issues.append({
                "type": "broken_skill_link",
                "target": target,
                "match": m.group(0),
            })
    return issues


def python_syntax_check(code: str) -> bool:
    """Check if Python code parses without SyntaxError."""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def audit_skill(path: Path, skill_names: set[str], all_skills: list[dict]) -> dict:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    rel = path.relative_to(ROOT)

    # Determine expected category/domain from directory path
    parts = rel.parts[:-1]  # Exclude SKILL.md
    expected_category = parts[0] if parts else ""
    expected_domain = parts[0] if parts else ""

    meta = parse_meta(raw_fm) if raw_fm else {}
    if meta is None:
        meta = {}

    sections = extract_sections(body)
    word_count = count_words(body)
    code_info = count_code_blocks(body)
    anti_rat_rows = count_anti_rat_rows(body)
    skill_links = check_skill_links(body, skill_names)

    issues: list[dict] = []
    score = 0

    # ── Frontmatter completeness ──
    fm_missing = []
    for field in ["name", "description", "category", "domain"]:
        if field not in meta or not meta.get(field):
            fm_missing.append(field)
    if fm_missing:
        issues.append({
            "severity": "HIGH",
            "rule": "frontmatter_required",
            "detail": f"Missing required fields: {', '.join(fm_missing)}",
        })
    else:
        score += WEIGHTS["frontmatter_complete"]

    # ── Trigger phrase ──
    desc = meta.get("description", "")
    if not any(p in desc.lower()[:60] for p in TRIGGER_PHRASES):
        issues.append({
            "severity": "MEDIUM",
            "rule": "trigger_phrase",
            "detail": f"Description lacks trigger phrase (starts with: {desc[:50]!r})",
        })
    else:
        score += WEIGHTS["trigger_phrase"]

    # ── Tags ──
    tags = meta.get("tags", [])
    if not tags:
        issues.append({
            "severity": "MEDIUM",
            "rule": "tags_missing",
            "detail": "No tags in frontmatter",
        })
    else:
        score += WEIGHTS["tags_present"]

    # ── Version ──
    version = meta.get("version", "")
    if not version:
        issues.append({
            "severity": "LOW",
            "rule": "version_missing",
            "detail": "No version in frontmatter",
        })
    else:
        score += WEIGHTS["version_present"]

    # ── Category matches directory ──
    cat = meta.get("category", "")
    if cat and cat != expected_category:
        issues.append({
            "severity": "MEDIUM",
            "rule": "category_mismatch",
            "detail": f"Category {cat!r} != directory {expected_category!r}",
        })
    else:
        score += WEIGHTS["category_matches_dir"]

    # ── Domain matches directory ──
    domain = meta.get("domain", "")
    if domain and domain != expected_domain:
        issues.append({
            "severity": "LOW",
            "rule": "domain_mismatch",
            "detail": f"Domain {domain!r} != directory {expected_domain!r}",
        })
    else:
        score += WEIGHTS["domain_matches_dir"]

    # ── Required sections ──
    missing_req = [s for s in REQUIRED_SECTIONS if s not in sections]
    if missing_req:
        issues.append({
            "severity": "HIGH",
            "rule": "required_section_missing",
            "detail": f"Missing required sections: {missing_req}",
        })
    else:
        score += WEIGHTS["req_sections_present"]

    # ── Recommended sections ──
    missing_rec = [s for s in RECOMMENDED_SECTIONS if s not in sections]
    if not missing_rec:
        score += WEIGHTS["recomm_sections_present"]

    # ── Content depth ──
    depth_score = 0
    if word_count >= 200:
        depth_score += 4
    elif word_count >= 100:
        depth_score += 2
    if word_count >= 500:
        depth_score += 4
    elif word_count >= 300:
        depth_score += 2
    if len(sections) >= 3:
        depth_score += 4
    elif len(sections) >= 2:
        depth_score += 2
    score += min(depth_score, WEIGHTS["content_depth"])

    # ── Code blocks ──
    code_block_score = 0
    if code_info["count"] >= 3:
        code_block_score += 5
    elif code_info["count"] >= 1:
        code_block_score += 3
    if code_info["total_lines"] >= 30:
        code_block_score += 5
    elif code_info["total_lines"] >= 10:
        code_block_score += 3
    score += min(code_block_score, WEIGHTS["code_blocks"])

    # ── Anti-rationalization rows ──
    if anti_rat_rows >= 2:
        score += WEIGHTS["anti_rat_rows"]
    elif anti_rat_rows == 1:
        score += 2

    # ── Stub detection ──
    desc_stub = any(
        kw in desc.lower()
        for kw in ["stub", "placeholder", "todo: implement", "merged into"]
    ) if desc else False
    is_stub = word_count < 100 and code_info["count"] == 0 and desc_stub
    thin = word_count < 150 and code_info["count"] == 0
    if is_stub:
        issues.append({
            "severity": "HIGH",
            "rule": "stub_skill",
            "detail": f"Stub skill: {word_count} words, 0 code blocks, '{desc[:60]}'",
        })
    elif thin:
        issues.append({
            "severity": "MEDIUM",
            "rule": "thin_skill",
            "detail": f"Thin skill: {word_count} words, 0 code blocks",
        })
    else:
        score += WEIGHTS["no_stub"]

    # ── Cross-reference health ──
    if skill_links:
        for sl in skill_links:
            issues.append({
                "severity": "MEDIUM",
                "rule": "broken_skill_link",
                "detail": f"Broken skill://{sl['target']} link",
            })
    # Score check: if any cross-refs exist and all are valid, award points
    all_links = SKILL_LINK_RE.findall(body)
    if all_links and not skill_links:
        score += WEIGHTS["cross_refs_valid"]

    # ── Security red flags ──
    sec_matches = SECURITY_PATTERNS.findall(body)
    if sec_matches:
        issues.append({
            "severity": "CRITICAL",
            "rule": "security_redflag",
            "detail": f"Security-sensitive patterns: {sec_matches[:3]}",
        })
    else:
        score += WEIGHTS["no_security_redflags"]

    # ── Python syntax check ──
    py_errors = []
    for lang, code in re.findall(r"```(python|py)\n(.*?)```", body, re.DOTALL):
        if not python_syntax_check(code.strip()):
            py_errors.append(code.strip()[:80])
    if py_errors:
        issues.append({
            "severity": "HIGH",
            "rule": "python_syntax_error",
            "detail": f"Python syntax errors in {len(py_errors)} code block(s)",
        })


    return {
        "path": str(rel),
        "name": meta.get("name", path.stem),
        "score": score,
        "max_score": MAX_SCORE,
        "pct": round(score / MAX_SCORE * 100, 1),
        "word_count": word_count,
        "code_blocks": code_info["count"],
        "code_lines": code_info["total_lines"],
        "sections": len(sections),
        "anti_rat_rows": anti_rat_rows,
        "issues": issues,
        "meta": {
            "description": meta.get("description", "")[:80],
            "category": cat,
            "domain": domain,
            "tags": tags,
            "version": version,
        },
    }


def severity_sort_key(s: str) -> int:
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    return order.get(s, 99)


def print_summary(results: list[dict]):
    total = len(results)
    scored = [r for r in results if r["pct"] >= 0]
    avg_pct = sum(r["pct"] for r in scored) / len(scored) if scored else 0

    print(f"\n{'='*72}")
    print(f"  1ai-skills Audit Summary: {total} skills")
    print(f"{'='*72}")
    print(f"  Average quality score: {avg_pct:.1f}%")

    # Distribution
    buckets = {"A (90-100)": 0, "B (80-89)": 0, "C (70-79)": 0,
               "D (60-69)": 0, "F (<60)": 0}
    for r in results:
        pct = r["pct"]
        if pct >= 90:
            buckets["A (90-100)"] += 1
        elif pct >= 80:
            buckets["B (80-89)"] += 1
        elif pct >= 70:
            buckets["C (70-79)"] += 1
        elif pct >= 60:
            buckets["D (60-69)"] += 1
        else:
            buckets["F (<60)"] += 1

    print(f"\n  Grade Distribution:")
    for grade, count in buckets.items():
        bar = "█" * (count * 80 // max(buckets.values())) if max(buckets.values()) else ""
        print(f"    {grade:15s}: {count:4d}  {bar}")

    # Issue summary
    all_issues = [i for r in results for i in r["issues"]]
    by_severity: dict[str, int] = defaultdict(int)
    by_rule: dict[str, int] = defaultdict(int)
    for i in all_issues:
        by_severity[i["severity"]] += 1
        by_rule[i["rule"]] += 1

    print(f"\n  Issues by Severity:")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        print(f"    {sev:10s}: {by_severity.get(sev, 0)}")

    print(f"\n  Top Issue Types:")
    for rule, count in sorted(by_rule.items(), key=lambda x: -x[1])[:10]:
        print(f"    {rule:30s}: {count}")

    # Worst offenders
    worst = sorted(results, key=lambda r: r["pct"])[:10]
    print(f"\n  Bottom 10 (needs most work):")
    for r in worst:
        high_issues = sum(1 for i in r["issues"] if i["severity"] in ("CRITICAL", "HIGH"))
        print(f"    {r['pct']:5.1f}%  {r['name'][:40]:40s}  {high_issues} high/crit  {r['word_count']:5d}w")


def print_fix_report(results: list[dict]):
    """Print actionable fix list grouped by severity."""
    print(f"\n{'='*72}")
    print(f"  Actionable Fix Report")
    print(f"{'='*72}")

    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        items = []
        for r in results:
            for i in r["issues"]:
                if i["severity"] == sev:
                    items.append((r["path"], r["name"], i))
        if not items:
            continue
        print(f"\n  [{sev}] — {len(items)} issue(s)")
        for path, name, issue in items[:20]:
            print(f"    - {path}")
            print(f"      {issue['detail']}")
        if len(items) > 20:
            print(f"      ... and {len(items) - 20} more")


def main():
    parser = argparse.ArgumentParser(description="Deep quality audit for 1ai-skills")
    parser.add_argument("--json", action="store_true", help="Output full JSON report")
    parser.add_argument("--fix-report", action="store_true", help="Print actionable fix list")
    parser.add_argument("-o", "--output", type=str, help="Write JSON report to file")
    parser.add_argument("--filter", type=str, help="Only audit skills matching name filter")
    args = parser.parse_args()

    skills = find_skills()
    if not skills:
        print("ERROR: No skills found", file=sys.stderr)
        sys.exit(2)

    # Build skill name set for cross-reference validation
    skill_names = set()
    for sk_path in skills:
        text = sk_path.read_text(encoding="utf-8")
        fm, _ = split_frontmatter(text)
        meta = parse_meta(fm) if fm else {}
        if meta and meta.get("name"):
            skill_names.add(meta["name"])

    # Load SKILLS.json for additional cross-refs
    skills_json_path = ROOT / "SKILLS.json"
    skills_json_entries = []
    if skills_json_path.exists():
        try:
            sj = json.loads(skills_json_path.read_text(encoding="utf-8"))
            skills_json_entries = sj.get("skills", [])
            for entry in skills_json_entries:
                if entry.get("name"):
                    skill_names.add(entry["name"])
        except (json.JSONDecodeError, OSError):
            pass

    # Audit
    print(f"Auditing {len(skills)} skills...", file=sys.stderr)

    results = []
    for sk_path in skills:
        audit = audit_skill(sk_path, skill_names, skills_json_entries)
        if args.filter and args.filter.lower() not in audit["name"].lower():
            continue
        results.append(audit)

    results.sort(key=lambda r: r["pct"])

    if args.output:
        out_path = ROOT / args.output
        out_path.write_text(json.dumps({
            "summary": {
                "total": len(results),
                "avg_pct": round(sum(r["pct"] for r in results) / len(results), 1),
            },
            "results": results,
        }, indent=2), encoding="utf-8")
        print(f"Report written to {out_path}", file=sys.stderr)

    if args.json or args.output:
        if not args.output:
            print(json.dumps({"summary": {"total": len(results)}, "results": results}, indent=2))
    else:
        print_summary(results)

    if args.fix_report:
        print_fix_report(results)


if __name__ == "__main__":
    main()
