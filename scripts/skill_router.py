#!/usr/bin/env python3
"""
skill-router.py — Skill Routing & Discovery Engine

Takes a natural-language query and returns ranked skills from SKILLS.json.
Uses exact matching, category scoping, tag overlap, and description ("Use when") triggers.

Usage:
    python3 scripts/skill-router.py "test driven development python"
    python3 scripts/skill-router.py "docker deployment" --category devops --top 10
    python3 scripts/skill-router.py "crypto trading" --json
"""

import json
import re
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_JSON = REPO_ROOT / "SKILLS.json"


def load_skills() -> dict[str, Any]:
    """Load SKILLS.json and return skills list + metadata."""
    with open(SKILLS_JSON) as f:
        data = json.load(f)
    return data


def tokenize(text: str) -> set[str]:
    """Split text into lowercased tokens, dropping short/common words."""
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
    tokens = re.findall(r"[a-z0-9][a-z0-9\-]{1,}", text.lower())
    return {t for t in tokens if t not in STOP_WORDS and len(t) > 1}


def score_skill(
    query_tokens: set[str],
    skill: dict[str, Any],
) -> float:
    """Score a single skill against query tokens.

    Scoring factors (weights):
    - Exact name match: +100
    - Name substring match: +50
    - Category match: +20
    - Tag overlap (fractional): max +30
    - Description "Use when" phrase overlap: +2 per token
    - Description body overlap: +1 per token
    - Domain match: +10
    """
    score = 0.0
    name = skill.get("name", "").lower()
    description = skill.get("description", "").lower()
    category = skill.get("category", "").lower()
    domain = skill.get("domain", "").lower()
    tags = [t.lower() for t in skill.get("tags", [])]

    # Exact name match
    if query_tokens & {name}:
        score += 100
    # Name part match
    name_parts = set(name.replace("-", " ").split())
    matched_name = query_tokens & name_parts
    score += len(matched_name) * 50 / max(len(name_parts), 1)

    # Category match
    cat_tokens = tokenize(category)
    matched_cat = query_tokens & cat_tokens
    score += len(matched_cat) * 20

    # Tag overlap
    if tags:
        tag_tokens = set(tags)
        matched_tags = query_tokens & tag_tokens
        score += (len(matched_tags) / max(len(tag_tokens), 1)) * 30

    # Domain match
    dom_tokens = tokenize(domain)
    matched_dom = query_tokens & dom_tokens
    score += len(matched_dom) * 10

    # Description "Use when" section — extract the trigger clause
    use_when_match = re.search(r"use when\s*(.*?)(?:\.|$)", description)
    if use_when_match:
        trigger_tokens = tokenize(use_when_match.group(1))
        matched_triggers = query_tokens & trigger_tokens
        score += len(matched_triggers) * 2

    # General description overlap
    desc_tokens = tokenize(description)
    matched_desc = query_tokens & desc_tokens
    score += len(matched_desc) * 1

    return score


def route(
    query: str,
    category: str | None = None,
    top: int = 15,
    min_score: float = 1.0,
) -> list[dict[str, Any]]:
    """Rank skills by relevance to query."""
    data = load_skills()
    skills = data["skills"]
    query_tokens = tokenize(query)

    # Filter by category if specified
    if category:
        skills = [s for s in skills if s.get("category", "").lower() == category.lower()]

    scored = []
    for skill in skills:
        s = score_skill(query_tokens, skill)
        if s >= min_score:
            scored.append((s, skill))

    scored.sort(key=lambda x: -x[0])
    return [{"score": round(s, 1), **skill} for s, skill in scored[:top]]


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

    # Direct substring match
    matches = [n for n in all_names if query_lower in n.lower() or n.lower() in query_lower]
    if matches:
        return matches[:top]

    # Token overlap with names
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
    else:
        results = route(query, category=args.category, top=args.top)

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
    main()
