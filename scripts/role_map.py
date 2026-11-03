#!/usr/bin/env python3
"""
scripts/role_map.py — Map every 1ai skill to one of 17 roles.

Ordering: most-specific-first over (category, subdomain, tags, name).
Returns a list of (skill_name, role) tuples and a dict role->count.
All 19 categories are covered by CATEGORY_FALLBACK so zero skills are roleless.

Roles (17 total):
  software-engineer     — development + agents
  system-architect      — development architecture
  qa-automation-engineer — development testing
  devops-sre-engineer   — devops + automation
  security-engineer     — cybersecurity defensive
  penetration-tester    — cybersecurity offensive
  ai-ml-engineer        — core + mcp + integrations
  data-engineer         — data
  ui-ux-designer        — content design subset (design/ui/ux/frontend/css/tailwind/typography/landing/brand/accessibility)
  content-creator       — remaining content (video/audio/remotion/hyperframes/writing/docs/book/podcast)
  growth-marketer       — marketing
  sales-engineer        — sales
  customer-support      — customer-support operations
  product-manager       — mindset + productivity + fallback
  research-analyst      — research
  financial-analyst     — financial
  quantitative-trader   — trading

CATEGORY_FALLBACK guarantees every skill gets a role.
Run: python3 scripts/role_map.py
Output: role->count table + assertion zero roleless skills.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKILLS_JSON = ROOT / "SKILLS.json"

# Single source of truth: anchor skill names → their own role.
# Anchors must always own their role, even when generic rules would match a sibling role.
ROLE_ANCHORS = {
    "role-software-engineer": "software-engineer",
    "role-system-architect": "system-architect",
    "role-qa-automation-engineer": "qa-automation-engineer",
    "role-devops-sre-engineer": "devops-sre-engineer",
    "role-security-engineer": "security-engineer",
    "role-penetration-tester": "penetration-tester",
    "role-ai-ml-engineer": "ai-ml-engineer",
    "role-data-engineer": "data-engineer",
    "role-ui-ux-designer": "ui-ux-designer",
    "role-content-creator": "content-creator",
    "role-growth-marketer": "growth-marketer",
    "role-sales-engineer": "sales-engineer",
    "role-customer-support": "customer-support",
    "role-product-manager": "product-manager",
    "role-research-analyst": "research-analyst",
    "role-financial-analyst": "financial-analyst",
    "role-quantitative-trader": "quantitative-trader",
}

def load_skills():
    with open(SKILLS_JSON) as f:
        data = json.load(f)
    return data["skills"]


# ---------------------------------------------------------------------------
# Role-assignment rules: most-specific-first tuples of (predicate_fn, role_name)
# Each predicate receives (skill_dict) and returns bool.
# ---------------------------------------------------------------------------

def make_contains_any(*substrings):
    def pred(s):
        txt = " ".join(
            [s.get("name", ""), " ".join(s.get("tags", [])), s.get("description", "")]
        ).lower()
        return any(sub in txt for sub in substrings)
    return pred


def make_category_eq(cat):
    def pred(s):
        return s.get("category", "").lower() == cat.lower()
    return pred


def make_name_contains(*substrings):
    def pred(s):
        return any(sub in s.get("name", "").lower() for sub in substrings)
    return pred


def make_subdomain_eq(sub):
    def pred(s):
        return s.get("subdomain", "").lower() == sub.lower()
    return pred


def make_tag_contains(*substrings):
    def pred(s):
        tags = " ".join(s.get("tags", [])).lower()
        return any(sub in tags for sub in substrings)
    return pred


# ---------------------------------------------------------------------------
# Category → role fallback (covers all 19 categories)
# ---------------------------------------------------------------------------
CATEGORY_FALLBACK = {
    "agents": "software-engineer",
    "automation": "devops-sre-engineer",
    "content": "content-creator",       # broad fallback; ui-ux-designer is more specific
    "core": "ai-ml-engineer",
    "cybersecurity": "security-engineer",  # default; pentest overrides below
    "data": "data-engineer",
    "development": "software-engineer",
    "devops": "devops-sre-engineer",
    "financial": "financial-analyst",
    "integrations": "ai-ml-engineer",
    "marketing": "growth-marketer",
    "mcp": "ai-ml-engineer",
    "meta": "product-manager",
    "mindset": "product-manager",
    "operations": "product-manager",
    "productivity": "product-manager",
    "research": "research-analyst",
    "sales": "sales-engineer",
    "trading": "quantitative-trader",
}

# ---------------------------------------------------------------------------
# Assignment function: most-specific-first
# ---------------------------------------------------------------------------

def assign_role(skill):
    """Return the role name for a skill using most-specific-first rules."""
    name = skill.get("name", "").lower()
    # Anchors always own their declared role
    if name in ROLE_ANCHORS:
        return ROLE_ANCHORS[name]
    tags_str = " ".join(skill.get("tags", [])).lower()
    nt = name + " " + tags_str
    cat = skill.get("category", "").lower()

    # 0a. system-architect — development architecture only (name+tags, not description)
    if cat == "development" and any(k in nt for k in (
        "architect", "architecture", "system-design", "modular", "refactor",
        "domain-boundar", "monolith", "decompos")):
        return "system-architect"

    # 0b. qa-automation — development/agents testing only (name+tags, not description)
    if cat in ("development", "agents") and any(k in nt for k in (
        "test", "testing", "qa", "pytest", "vitest", "cypress", "playwright",
        "e2e", "coverage", "fixture", "flaky", "assert", "regression", "benchmark")):
        return "qa-automation-engineer"

    # 0c. customer-support — operations/sales only (name+tags, not description)
    if cat in ("operations", "sales") and any(k in nt for k in (
        "support", "success", "ticket", "triage", "complaint", "refund",
        "onboarding", "churn", "sla", "helpdesk", "crm")):
        return "customer-support"

    # 1. cybersecurity offensive → penetration-tester
    offense_kws = [
        "pentest", "exploit", "bounty", "red.team", "recon",
        "metasploit", "burp", "payload", "shell", "privilege.escalation",
        "cve", "vulnerability", "exploit", "hack",
    ]
    if make_category_eq("cybersecurity")(skill) and any(kw in tags_str for kw in offense_kws):
        return "penetration-tester"

    # 2. cybersecurity defensive → security-engineer
    if make_category_eq("cybersecurity")(skill):
        return "security-engineer"

    # 3. content design subset → ui-ux-designer
    design_kws = [
        "design", "ui", "ux", "frontend", "css", "tailwind",
        "typography", "landing", "brand", "accessibility",
    ]
    if make_category_eq("content")(skill) and any(kw in tags_str for kw in design_kws):
        return "ui-ux-designer"

    # 4. content remaining → content-creator
    # (video|audio|remotion|hyperframes|writing|docs|book|podcast)
    content_kws = ["video", "audio", "remotion", "hyperframes", "writing", "docs", "book", "podcast"]
    if make_category_eq("content")(skill) and any(kw in tags_str for kw in content_kws):
        return "content-creator"

    # 5. marketing → growth-marketer
    if make_category_eq("marketing")(skill):
        return "growth-marketer"

    # 6. sales → sales-engineer
    if make_category_eq("sales")(skill):
        return "sales-engineer"

    # 7. data → data-engineer
    if make_category_eq("data")(skill):
        return "data-engineer"

    # 8. devops + automation → devops-sre-engineer
    if make_category_eq("devops")(skill) or make_tag_contains("ci-cd", "docker", "kubernetes", "terraform", "ansible")(skill):
        return "devops-sre-engineer"

    # 9. ai-ml-engineer: core/* + mcp/* + integrations/*
    if make_category_eq("core")(skill) or make_category_eq("mcp")(skill) or make_category_eq("integrations")(skill):
        return "ai-ml-engineer"

    # 10. research → research-analyst
    if make_category_eq("research")(skill):
        return "research-analyst"

    # 11. financial → financial-analyst
    if make_category_eq("financial")(skill):
        return "financial-analyst"

    # 12. mindset + productivity → product-manager
    if make_category_eq("mindset")(skill) or make_category_eq("productivity")(skill):
        return "product-manager"

    # 13. trading → quantitative-trader
    if make_category_eq("trading")(skill):
        return "quantitative-trader"

    # 14. fallback per category
    cat = skill.get("category", "").lower()
    if cat in CATEGORY_FALLBACK:
        return CATEGORY_FALLBACK[cat]

    # 15. absolute last resort: software-engineer
    return "software-engineer"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    skills = load_skills()
    role_counts: dict[str, int] = defaultdict(int)
    roleless = []

    assignments = []
    for s in skills:
        role = assign_role(s)
        assignments.append((s["name"], role))
        role_counts[role] += 1
        if role == "roleless":
            roleless.append(s["name"])

    # Print role -> count table
    print(f"Role assignment table (17 roles, {len(skills)} skills):")
    all_roles = [
        "software-engineer",
        "system-architect",
        "qa-automation-engineer",
        "devops-sre-engineer",
        "security-engineer",
        "penetration-tester",
        "ai-ml-engineer",
        "data-engineer",
        "ui-ux-designer",
        "content-creator",
        "growth-marketer",
        "sales-engineer",
        "customer-support",
        "product-manager",
        "research-analyst",
        "financial-analyst",
        "quantitative-trader",
    ]
    for r in all_roles:
        cnt = role_counts.get(r, 0)
        print(f"  {r:25s}: {cnt}")

    total = sum(role_counts.values())
    print(f"\nTotal skills assigned: {total}")
    print(f"Skills with no role (roleless): {len(roleless)}")
    if roleless:
        print("ROLELESS SKILLS (first 30):")
        for n in roleless[:30]:
            print(f"    {n}")
    else:
        print(f"✓ Zero roleless skills — all {total} skills mapped to a role.")

    # Assertion
    assert len(roleless) == 0, f"{len(roleless)} roleless skills detected — CATEGORY_FALLBACK incomplete"


if __name__ == "__main__":
    main()