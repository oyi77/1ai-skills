#!/usr/bin/env python3
"""Generate eval cases for all 23 role anchors (22 remaining after CEO)."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "evals" / "cases"

# role-anchor-dir -> (eval-category, role-label, specific-pattern)
ANCHORS = {
    # corporate
    "corporate/ceo": ("corporate", "CEO", "CEO"),
    "corporate/cto": ("corporate", "CTO", "CTO"),
    "corporate/cfo": ("corporate", "CFO", "CFO"),
    "corporate/cmo": ("corporate", "CMO", "CMO"),
    "corporate/coo": ("corporate", "COO", "COO"),
    "corporate/cco": ("corporate", "CCO", "CCO"),
    # functional
    "development/role-software-engineer": ("development", "Software Engineer", "Software Engineer"),
    "development/role-system-architect": ("development", "System Architect", "System Architect"),
    "development/role-qa-automation-engineer": ("development", "QA Automation Engineer", "QA"),
    "cybersecurity/role-security-engineer": ("cybersecurity", "Security Engineer", "Security Engineer"),
    "cybersecurity/role-penetration-tester": ("cybersecurity", "Penetration Tester", "Penetration Tester"),
    "devops/role-devops-sre-engineer": ("devops", "DevOps/SRE Engineer", "DevOps/SRE"),
    "data/role-data-engineer": ("data", "Data Engineer", "Data Engineer"),
    "core/role-ai-ml-engineer": ("core", "AI/ML Engineer", "AI/ML Engineer"),
    "operations/role-product-manager": ("operations", "Product Manager", "Product Manager"),
    "marketing/role-growth-marketer": ("marketing", "Growth Marketer", "Growth Marketer"),
    "sales/role-sales-engineer": ("sales", "Sales Engineer", "Sales Engineer"),
    "sales/role-customer-support": ("sales", "Customer Support", "Customer Support"),
    "research/role-research-analyst": ("research", "Research Analyst", "Research Analyst"),
    "financial/role-financial-analyst": ("financial", "Financial Analyst", "Financial Analyst"),
    "trading/role-quantitative-trader": ("trading", "Quantitative Trader", "Quantitative Trader"),
    "content/role-content-creator": ("content", "Content Creator", "Content Creator"),
    "content/role-ui-ux-designer": ("content", "UI/UX Designer", "UI/UX Designer"),
}

made = 0
for anchor_path, (cat, role_label, pattern) in ANCHORS.items():
    skill_name = anchor_path.split("/")[-1]
    case_path = CASES / cat / f"{skill_name}.json"
    if case_path.exists():
        print(f"  skip (exists): {case_path.name}")
        continue

    case = {
        "skill": skill_name,
        "category": cat,
        "name": f"{role_label} — Role Anchor Quality",
        "description": f"Verify {skill_name} carries expert persona, When to Use, anti-rationalization, verification checklist, and trigger phrase",
        "checks": [
            {"type": "contains", "pattern": pattern, "name": "has-role-reference"},
            {"type": "section_exists", "pattern": "When to Use", "name": "has-when-to-use"},
            {"type": "section_exists", "pattern": "Anti-Rationalization", "name": "has-anti-rat"},
            {"type": "section_exists", "pattern": "Verification Checklist", "name": "has-verification"},
            {"type": "frontmatter_field_exists", "field": "persona", "name": "has-persona"},
            {"type": "frontmatter_field_exists", "field": "version", "name": "has-version"},
            {"type": "trigger_phrase", "name": "has-use-when"},
        ],
    }
    case_path.parent.mkdir(parents=True, exist_ok=True)
    case_path.write_text(json.dumps(case, indent=2) + "\n")
    made += 1
    print(f"  made: {case_path.name}")

print(f"\nDone: {made} cases created")
