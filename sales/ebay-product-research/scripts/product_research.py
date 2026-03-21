#!/usr/bin/env python3
"""
eBay Product Research — Analyze market opportunity for any product keyword.

Uses DuckDuckGo search for product listings/prices/trends, then LLM analysis
for market opportunity assessment.

Usage:
    python product_research.py --product "digital planner"
    python product_research.py --product "wireless earbuds" --marketplace US
    python product_research.py --product "..." --output json
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime

try:
    from duckduckgo_search import DDGS
    HAS_DDGS = True
except ImportError:
    HAS_DDGS = False


def search_product(keyword, marketplace="US", max_results=15):
    """Search for product listings and pricing data."""
    results = {
        "listings": [],
        "price_points": [],
        "raw_snippets": []
    }

    if not HAS_DDGS:
        print("Warning: duckduckgo_search not installed. pip install duckduckgo_search",
              file=sys.stderr)
        return results

    queries = [
        f"eBay {keyword} {marketplace} sold listings price",
        f"eBay {keyword} best selling {marketplace}",
        f"{keyword} market demand trend 2025 2026",
    ]

    ddgs = DDGS()
    for query in queries:
        try:
            search_results = ddgs.text(query, max_results=max_results)
            for r in search_results:
                snippet = f"{r.get('title', '')} — {r.get('body', '')}"
                results["raw_snippets"].append(snippet)

                # Extract price patterns
                prices = re.findall(r'\$[\d,]+\.?\d*', snippet)
                for p in prices:
                    try:
                        val = float(p.replace("$", "").replace(",", ""))
                        if 0.5 < val < 10000:
                            results["price_points"].append(val)
                    except ValueError:
                        pass

                results["listings"].append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", "")[:200],
                    "url": r.get("href", "")
                })

        except Exception as e:
            print(f"Search error for '{query}': {e}", file=sys.stderr)

    return results


def analyze_with_llm(keyword, search_data):
    """Use LLM to analyze market opportunity."""
    omniroute = os.path.expanduser("~/.openclaw/workspace/scripts/omniroute")
    if not os.path.exists(omniroute):
        omniroute = "omniroute"

    snippets_text = "\n".join(search_data["raw_snippets"][:20])
    prices = search_data["price_points"]

    price_summary = ""
    if prices:
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        price_summary = f"Prices found: avg=${avg_price:.2f}, min=${min_price:.2f}, max=${max_price:.2f}, {len(prices)} data points"

    prompt = (
        f"Analyze the eBay market opportunity for: {keyword}\n\n"
        f"Search data:\n{snippets_text}\n\n"
        f"{price_summary}\n\n"
        f"Provide analysis as JSON:\n"
        f'{{"market_size_estimate": "small/medium/large", '
        f'"avg_price": N.NN, "price_range": "low-high", '
        f'"competition_level": "low/medium/high", '
        f'"demand_level": "low/medium/high", '
        f'"top_sellers_insight": "...", '
        f'"trend": "growing/stable/declining", '
        f'"recommendation": "..." }}'
    )

    try:
        result = subprocess.run([omniroute, "--prompt", prompt],
                                capture_output=True, text=True, timeout=90)
        if result.returncode == 0:
            text = result.stdout.strip()
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        pass

    return None


def basic_analysis(keyword, search_data):
    """Fallback analysis without LLM."""
    prices = search_data["price_points"]
    listings = search_data["listings"]

    avg_price = sum(prices) / len(prices) if prices else 0
    num_listings = len(listings)

    # Simple heuristics
    if num_listings > 30:
        competition = "high"
    elif num_listings > 15:
        competition = "medium"
    else:
        competition = "low"

    if num_listings > 20:
        demand = "high"
    elif num_listings > 10:
        demand = "medium"
    else:
        demand = "low"

    return {
        "market_size_estimate": demand,
        "avg_price": round(avg_price, 2) if avg_price else "N/A",
        "price_range": f"${min(prices):.2f}-${max(prices):.2f}" if prices else "N/A",
        "competition_level": competition,
        "demand_level": demand,
        "top_sellers_insight": f"Found {num_listings} relevant listings",
        "trend": "stable",
        "recommendation": (
            f"{'Strong' if demand == 'high' and competition != 'high' else 'Moderate' if demand != 'low' else 'Weak'} "
            f"opportunity. Average price ~${avg_price:.2f}. "
            f"Competition is {competition}."
        ) if avg_price else "Insufficient data — try broader keywords",
        "note": "Basic analysis (no LLM). Install omniroute for deeper insights."
    }


def main():
    parser = argparse.ArgumentParser(description="eBay product research tool")
    parser.add_argument("--product", required=True, help="Product keyword to research")
    parser.add_argument("--marketplace", default="US", choices=["US", "UK", "DE", "AU"],
                        help="eBay marketplace (default: US)")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                        help="Output format")
    args = parser.parse_args()

    print(f"Researching: {args.product} (eBay {args.marketplace})...", file=sys.stderr)

    search_data = search_product(args.product, args.marketplace)

    # Try LLM analysis, fall back to basic
    analysis = analyze_with_llm(args.product, search_data)
    if not analysis:
        analysis = basic_analysis(args.product, search_data)

    result = {
        "product": args.product,
        "marketplace": args.marketplace,
        "timestamp": datetime.now().isoformat(),
        "analysis": analysis,
        "data_points": {
            "listings_found": len(search_data["listings"]),
            "price_points": len(search_data["price_points"])
        }
    }

    if args.output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        a = result["analysis"]
        print(f"\n{'='*50}")
        print(f"  eBay Product Research: {args.product}")
        print(f"  Marketplace: {args.marketplace}")
        print(f"{'='*50}\n")

        print(f"  Market Size:    {a.get('market_size_estimate', 'N/A')}")
        print(f"  Avg Price:      ${a['avg_price']}" if isinstance(a.get('avg_price'), (int, float)) else f"  Avg Price:      {a.get('avg_price', 'N/A')}")
        print(f"  Price Range:    {a.get('price_range', 'N/A')}")
        print(f"  Competition:    {a.get('competition_level', 'N/A')}")
        print(f"  Demand:         {a.get('demand_level', 'N/A')}")
        print(f"  Trend:          {a.get('trend', 'N/A')}")
        print(f"\n  Sellers:        {a.get('top_sellers_insight', 'N/A')}")
        print(f"\n  Recommendation: {a.get('recommendation', 'N/A')}")

        dp = result["data_points"]
        print(f"\n  Data: {dp['listings_found']} listings, {dp['price_points']} price points")

        if a.get("note"):
            print(f"\n  Note: {a['note']}")


if __name__ == "__main__":
    main()
