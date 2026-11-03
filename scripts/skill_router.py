#!/usr/bin/env python3
"""skill-router.py — Skill Routing & Discovery Engine

Takes a natural-language query and returns ranked skills from SKILLS.json.
Uses exact matching, category scoping, tag overlap, and description ("Use when") triggers.

Role expansion: when the top-1 result is a role anchor whose score >= 30.0,
the result list is expanded to include that role's cluster members (all skills
whose `roles` field contains the anchor's role). Weak matches do NOT expand
(hijack guard). Use --no-expand to disable; --role <name> to force a role.

Usage:
    python3 scripts/skill-router.py "test driven development python"
    python3 scripts/skill-router.py "docker deployment" --category devops --top 10
    python3 scripts/skill-router.py "crypto trading" --json
    python3 scripts/skill-router.py "write python code" --role software-engineer
"""
import json
import re
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_JSON = REPO_ROOT / "SKILLS.json"

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "need",
    "use", "used", "using", "when", "how", "what", "why", "where", "which",
    "who", "this", "that", "these", "those", "it", "its", "you", "your",
    "i", "we", "they", "he", "she", "not", "no", "nor", "so", "if",
    "then", "than", "too", "very", "just", "about", "also", "into",
    "over", "such", "only", "own", "same", "both", "each", "other",
    "some", "any", "all", "more", "most", "much", "many", "up", "down",
    "out", "off", "well", "here", "there",
}


def load_skills() -> dict[str, Any]:
    """Load SKILLS.json and return skills list + metadata."""
    with open(SKILLS_JSON) as f:
        return json.load(f)


def tokenize(text: str) -> set[str]:
    """Split text into lowercased tokens, dropping short/common words."""
    tokens = re.findall(r"[a-z0-9][a-z0-9\-]{1,}", text.lower())
    return {t for t in tokens if t not in STOP_WORDS and len(t) > 1}


def score_skill(query_tokens: set[str], skill: dict[str, Any]) -> float:
    """Score a single skill against query tokens.

    Scoring factors (weights):
    - Name part match: +50 / max(parts, 1) per matched hyphenated part
    - Category match: +20 per token
    - Explicit triggers (frontmatter): +15 per token
    - Tag overlap (fractional): max +30
    - Description "Use when" phrase overlap: +2 per token
    - Description body overlap: +1 per token
    - Domain match: +10 per token
    """
    score = 0.0
    name = skill.get("name", "").lower()
    description = skill.get("description", "").lower()
    category = skill.get("category", "").lower()
    domain = skill.get("domain", "").lower()
    tags = [t.lower() for t in skill.get("tags", [])]
    triggers = [t.lower() for t in skill.get("triggers", [])]

    name_parts = set(name.replace("-", " ").split())
    matched_name = query_tokens & name_parts
    score += len(matched_name) * 50 / max(len(name_parts), 1)

    cat_tokens = tokenize(category)
    matched_cat = query_tokens & cat_tokens
    score += len(matched_cat) * 20

    if tags:
        tag_tokens: set[str] = set()
        for t in tags:
            tag_tokens |= tokenize(t.replace("-", " "))
        matched_tags = query_tokens & tag_tokens
        score += (len(matched_tags) / max(len(tag_tokens), 1)) * 30

    if triggers:
        trigger_tokens: set[str] = set()
        for t in triggers:
            trigger_tokens |= tokenize(t.replace("-", " "))
        matched_triggers = query_tokens & trigger_tokens
        score += len(matched_triggers) * 15

    dom_tokens = tokenize(domain)
    matched_dom = query_tokens & dom_tokens
    score += len(matched_dom) * 10

    use_when_match = re.search(r"use when\s*(.*?)(?:\.\s|$)", description)
    if use_when_match:
        use_when_tokens = tokenize(use_when_match.group(1))
        matched_use_when = query_tokens & use_when_tokens
        score += len(matched_use_when) * 2

    desc_tokens = tokenize(description)
    matched_desc = query_tokens & desc_tokens
    score += len(matched_desc) * 1
    return score


CATEGORY_FALLBACK: dict[str, str] = {
    "agents": "software-engineer",
    "automation": "devops-sre-engineer",
    "content": "content-creator",
    "core": "ai-ml-engineer",
    "cybersecurity": "security-engineer",
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

from role_map import ROLE_ANCHORS as _ROLE_ANCHOR_BY_NAME


def role_of(skill: dict[str, Any]) -> str | None:
    """Return the role name for a skill, reading the `roles` field first."""
    roles = skill.get("roles")
    if isinstance(roles, list) and roles:
        return roles[0]
    name = skill.get("name", "")
    if name in _ROLE_ANCHOR_BY_NAME:
        return _ROLE_ANCHOR_BY_NAME[name]
    cat = skill.get("category", "").lower()
    return CATEGORY_FALLBACK.get(cat)


ROLE_INTENT: dict[str, list[str]] = {
    "software-engineer": ["programming", "code", "coding", "implement", "refactor", "bug", "debug",
                          "api", "endpoint", "script", "function", "class", "feature"],
    "ui-ux-designer": ["design", "redesign", "revamp", "ui", "ux", "layout", "typography",
                       "color", "theme", "css", "figma", "responsive", "wireframe"],
    "growth-marketer": ["marketing", "marketer", "seo", "campaign", "growth", "audience",
                        "traffic", "funnel", "newsletter", "backlink"],
    "sales-engineer": ["sales", "sell", "deal", "pipeline", "lead", "prospect", "outreach",
                       "quota", "close", "b2b", "crm"],
    "customer-support": ["support", "complaint", "ticket", "refund", "churn", "helpdesk",
                         "csat", "escalation", "satisfaction"],
    "devops-sre-engineer": ["deploy", "deployment", "docker", "kubernetes", "terraform",
                            "infra", "sre", "monitoring", "observability", "ci"],
    "security-engineer": ["security", "hardening", "compliance", "siem", "forensics", "incident"],
    "penetration-tester": ["pentest", "exploit", "vulnerability", "recon", "redteam"],
    "data-engineer": ["etl", "warehouse", "dbt", "airflow", "ingestion"],
    "ai-ml-engineer": ["llm", "rag", "embedding", "fine-tune", "mcp", "inference"],
    "qa-automation-engineer": ["test", "testing", "qa", "e2e", "coverage", "flaky", "regression"],
    "system-architect": ["architecture", "system-design", "monolith", "modular", "scalability"],
    "product-manager": ["roadmap", "prd", "backlog", "sprint", "priorit", "requirement"],
    "research-analyst": ["research", "competitive", "osint", "market-analysis"],
    "financial-analyst": ["financial", "valuation", "dcf", "budget", "forecast", "p&l"],
    "quantitative-trader": ["trading", "trade", "backtest", "quant", "indicator", "crypto", "futures", "perp", "spot trading"],
    "content-creator": ["video", "podcast", "book", "caption", "storyboard", "narration"],
}


def detect_roles(query: str) -> list[str]:
    """Rank roles by how many intent keywords appear as whole words in the query."""
    tokens = set(re.findall(r"[a-z0-9][a-z0-9\-]*", query.lower()))
    hits = []
    for role, keywords in ROLE_INTENT.items():
        n = sum(1 for k in keywords if k in tokens)
        if n:
            hits.append((n, role))
    hits.sort(key=lambda x: -x[0])
    return [role for _, role in hits]


def expand_role(
    results: list[dict[str, Any]],
    query: str,
    top_n: int = 25,
) -> list[dict[str, Any]]:
    """Expand a flat results list to include cluster members.

    Expansion happens ONLY when top-1 is a role anchor scoring >= 30.0
    (hijack guard). Anchor stays at position 0; cluster members are scored
    against the USER QUERY, deduplicated, and appended up to top_n.
    """
    if not results:
        return results
    top_skill = results[0]
    top_name = top_skill.get("name", "")
    top_role = _ROLE_ANCHOR_BY_NAME.get(top_name)
    if not top_role:
        return results
    if top_skill.get("score", 0.0) < 30.0:
        return results

    data = load_skills()
    query_tokens = tokenize(query)
    cluster: list[dict[str, Any]] = []
    seen = {top_name}
    for s in data["skills"]:
        s_role = _ROLE_ANCHOR_BY_NAME.get(s.get("name", ""), role_of(s))
        if s_role == top_role and s["name"] not in seen:
            cluster.append({"score": round(score_skill(query_tokens, s), 1), **s})
            seen.add(s["name"])
    cluster.sort(key=lambda x: -x.get("score", 0.0))
    return ([top_skill] + cluster)[:top_n]


def expand_role_by_name(
    query: str,
    role_name: str,
    top_n: int = 25,
) -> list[dict[str, Any]]:
    """Return cluster members for a named role, scored against query."""
    data = load_skills()
    query_tokens = tokenize(query)
    cluster = []
    for s in data["skills"]:
        s_role = _ROLE_ANCHOR_BY_NAME.get(s.get("name", ""), role_of(s))
        if s_role == role_name:
            sc = score_skill(query_tokens, s)
            cluster.append({"score": round(sc, 1), **s})
    cluster.sort(key=lambda x: -x.get("score", 0.0))
    return cluster[:top_n]


def route(
    query: str,
    category: str | None = None,
    top: int = 15,
    min_score: float = 1.0,
    expand: bool = True,
    expand_extra: int = 6,
) -> list[dict[str, Any]]:
    """Rank skills by relevance to query, optionally expanding a detected role."""
    data = load_skills()
    skills = data["skills"]
    query_tokens = tokenize(query)

    if category:
        skills = [s for s in skills if s.get("category", "").lower() == category.lower()]

    scored = []
    for skill in skills:
        s = score_skill(query_tokens, skill)
        if s >= min_score:
            scored.append((s, skill))

    scored.sort(key=lambda x: -x[0])
    flat = [{"score": round(s, 1), **skill} for s, skill in scored[:top]]
    out = flat
    if expand:
        detected = detect_roles(query)
        if detected:
            target_role = detected[0]
            # Role confidence = number of intent keywords matched; establishes a
            # relevance floor for the cluster so role intent outranks incidental
            # token matches, WITHOUT displacing genuine high scorers like the
            # 58.0 exact-name hit for "adhd design brainstorming".
            hits = sum(1 for k in ROLE_INTENT[target_role] if k in query_tokens)
            role_floor = min(25.0, 12.0 * max(hits, 1))
            data_all = load_skills()
            existing = {r.get("name") for r in flat}
            merged = list(flat)
            for s in data_all["skills"]:
                if s["name"] in existing:
                    continue
                if _ROLE_ANCHOR_BY_NAME.get(s.get("name", ""), role_of(s)) == target_role:
                    own = score_skill(query_tokens, s)
                    merged.append({"score": round(max(own, role_floor), 1), **s})
            merged.sort(key=lambda x: -x.get("score", 0.0))
            out = merged[:top + expand_extra]
    return out


def should_delegate_external(
    scored_results: list[dict[str, Any]],
    threshold: float = 30.0,
) -> bool:
    """Determine if a query should fall back to external skill discovery (find-skills)."""
    if not scored_results:
        return True
    return scored_results[0].get("score", 0.0) < threshold


def search_categories(query: str) -> list[dict[str, Any]]:
    """Return categories ranked by relevance to query."""
    data = load_skills()
    query_tokens = tokenize(query)
    scores = {}
    counts = {}
    for skill in data["skills"]:
        cat = skill.get("category", "")
        if cat not in scores:
            scores[cat] = 0.0
            counts[cat] = 0
        scores[cat] += score_skill(query_tokens, skill)
        counts[cat] += 1

    ranked = []
    for cat in scores:
        avg = scores[cat] / max(counts[cat], 1)
        ranked.append({"category": cat, "avg_score": round(avg, 1), "skill_count": counts[cat]})
    ranked.sort(key=lambda x: -x["avg_score"])
    return ranked


def suggest(query: str, top: int = 5) -> list[str]:
    """Suggest skill names that might be what the user intended."""
    data = load_skills()
    all_names = [s["name"] for s in data["skills"]]
    query_lower = query.lower().strip()

    matches = [n for n in all_names if query_lower in n.lower() or n.lower() in query_lower]
    if matches:
        return matches[:top]

    query_tokens = tokenize(query)
    scored = []
    for name in all_names:
        name_tokens = set(name.lower().replace("-", " ").split())
        overlap = len(query_tokens & name_tokens)
        if overlap > 0:
            scored.append((overlap, name))
    scored.sort(key=lambda x: -x[0])
    return [n for _, n in scored[:top]]


def main() -> None:
    parser = ArgumentParser(description="Skill Routing & Discovery Engine")
    parser.add_argument("query", nargs="?", help="Search query (reads from stdin if omitted)")
    parser.add_argument("--category", "-c", help="Filter to category")
    parser.add_argument("--top", "-t", type=int, default=15, help="Max results (default: 15)")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--suggest", "-s", action="store_true", help="Suggest names instead of ranking")
    parser.add_argument("--categories", action="store_true", help="Rank categories by relevance")
    parser.add_argument("--role", "-r", help="Expand this role explicitly (e.g. software-engineer)")
    parser.add_argument("--no-expand", action="store_true",
                        help="Disable role expansion — flat routing only")
    args = parser.parse_args()

    query = args.query
    if not query and not sys.stdin.isatty():
        query = sys.stdin.read().strip()
    if not query:
        parser.print_help()
        sys.exit(1)

    if args.categories:
        results = search_categories(query)
    elif args.suggest:
        results = suggest(query, top=args.top)
    elif args.no_expand:
        results = route(query, category=args.category, top=args.top, expand=False)
    elif args.role:
        results = expand_role_by_name(query, args.role, top_n=args.top)
    else:
        results = route(query, category=args.category, top=args.top, expand=True)

    if args.json or args.categories:
        print(json.dumps(results, indent=2))
    else:
        if not results:
            print("No matching skills found.")
            return
        if args.suggest:
            print("Suggestions:")
            for r in results:
                print(f"  {r}")
        else:
            print(f"{'Score':>6}  {'Category':<18}  {'Name':<35}  Description")
            print(f"{'─'*6}  {'─'*18}  {'─'*35}  {'─'*50}")
            for r in results:
                desc = r.get("description", "")[:70]
                print(f"{r['score']:>6.1f}  {r.get('category',''):<18}  {r.get('name',''):<35}  {desc}")


if __name__ == "__main__":
    sys.exit(main())
