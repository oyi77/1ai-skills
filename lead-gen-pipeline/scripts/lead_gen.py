#!/usr/bin/env python3
"""
lead_gen.py — Lightweight CLI lead-generation wrapper
=====================================================
Scrape leads from DuckDuckGo, score by relevance, generate outreach via OmniRoute LLM.

Usage:
    python lead_gen.py --niche "digital products Indonesia" --limit 20
"""

import argparse
import json
import os
import re
import sys
from typing import List, Dict

from duckduckgo_search import DDGS
from openai import OpenAI

# ─── Paths ────────────────────────────────────────────────────────────────────

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SKILL_DIR, "data")
LEADS_FILE = os.path.join(DATA_DIR, "leads.json")

# ─── OmniRoute LLM client ────────────────────────────────────────────────────

llm = OpenAI(base_url="http://localhost:20128/v1", api_key="omniroute")

# ─── Business-quality indicators ─────────────────────────────────────────────

BUSINESS_INDICATORS = [
    "official", "store", "shop", "agency", "studio", "company",
    "service", "solution", "digital", "product", "brand", "enterprise",
    "consult", "partner", "platform", "marketplace", "startup",
    "indonesia", "jakarta", "surabaya", "bandung", "bali",
]


def scrape_leads(niche: str, limit: int) -> List[Dict]:
    """Search DuckDuckGo for leads matching the niche."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(niche, max_results=limit):
            results.append({
                "name": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
            })
    return results


def score_lead(lead: Dict, keywords: List[str]) -> int:
    """Score a lead 0-10 based on keyword matches and business indicators."""
    text = f"{lead['name']} {lead['snippet']}".lower()

    score = 0

    # Keyword relevance (up to 5 points)
    keyword_hits = sum(1 for kw in keywords if kw.lower() in text)
    score += min(keyword_hits * 2, 5)

    # Business indicator matches (up to 4 points)
    indicator_hits = sum(1 for ind in BUSINESS_INDICATORS if ind in text)
    score += min(indicator_hits, 4)

    # Has a proper URL (1 point)
    url = lead.get("url", "")
    if url and not any(g in url for g in ["wikipedia.org", "reddit.com", "quora.com"]):
        score += 1

    return min(score, 10)


def generate_outreach(lead: Dict, niche: str) -> str:
    """Generate a personalized outreach message using OmniRoute LLM."""
    prompt = (
        f"Write a short, personalized cold-outreach message (3-4 sentences) "
        f"for a business lead in the '{niche}' niche.\n\n"
        f"Lead info:\n"
        f"- Name: {lead['name']}\n"
        f"- URL: {lead['url']}\n"
        f"- Snippet: {lead['snippet']}\n\n"
        f"The message should be professional, reference something specific about "
        f"the lead, and include a clear call-to-action. No subject line needed."
    )
    try:
        resp = llm.chat.completions.create(
            model="auto",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[outreach generation failed: {e}]"


def save_leads(leads: List[Dict]) -> None:
    """Save leads to data/leads.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Lightweight lead-gen CLI: scrape, score, outreach."
    )
    parser.add_argument(
        "--niche", required=True,
        help='Search niche, e.g. "digital products Indonesia"',
    )
    parser.add_argument(
        "--limit", type=int, default=20,
        help="Max number of leads to scrape (default: 20)",
    )
    args = parser.parse_args()

    niche = args.niche
    keywords = [w for w in niche.split() if len(w) > 2]

    print(f"[*] Scraping up to {args.limit} leads for niche: {niche}")
    raw_leads = scrape_leads(niche, args.limit)
    print(f"[+] Found {len(raw_leads)} results")

    leads = []
    for i, lead in enumerate(raw_leads, 1):
        lead["score"] = score_lead(lead, keywords)
        print(f"[{i}/{len(raw_leads)}] Scoring: {lead['name'][:60]}  -> {lead['score']}/10")
        lead["outreach_message"] = generate_outreach(lead, niche)
        leads.append(lead)

    # Sort by score descending
    leads.sort(key=lambda x: x["score"], reverse=True)

    save_leads(leads)
    print(f"\n[+] Saved {len(leads)} leads to {LEADS_FILE}")

    # Print top 5 summary
    print("\n── Top leads ──")
    for lead in leads[:5]:
        print(f"  [{lead['score']}/10] {lead['name'][:70]}")
        print(f"          {lead['url']}")


if __name__ == "__main__":
    main()
