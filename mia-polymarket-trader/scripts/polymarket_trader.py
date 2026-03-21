#!/usr/bin/env python3
"""
Polymarket Trader - Analysis-only tool for Polymarket prediction markets.

Fetches market data from Polymarket's public API and uses OmniRoute LLM
to analyze probability, sentiment, and suggest trades.

NOTE: This is analysis only. No actual trading execution.
"""

import argparse
import json
import sys
from datetime import datetime, timezone

import requests
from openai import OpenAI

POLYMARKET_API = "https://gamma-api.polymarket.com/markets"
OMNIROUTE_BASE_URL = "http://localhost:20128/v1"
OMNIROUTE_API_KEY = "omniroute"
LLM_MODEL = "auto"


def fetch_markets(limit: int = 20, search: str | None = None) -> list[dict]:
    """Fetch active markets from Polymarket API."""
    params = {"limit": limit, "active": "true"}
    if search:
        params["tag"] = search
    try:
        resp = requests.get(POLYMARKET_API, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(json.dumps({"error": f"Failed to fetch markets: {e}"}), file=sys.stderr)
        sys.exit(1)


def fetch_market_by_id(market_id: str) -> dict | None:
    """Fetch a specific market by its ID."""
    url = f"{POLYMARKET_API}/{market_id}"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(json.dumps({"error": f"Failed to fetch market {market_id}: {e}"}), file=sys.stderr)
        sys.exit(1)


def build_analysis_prompt(markets: list[dict]) -> str:
    """Build the LLM prompt for market analysis."""
    market_summaries = []
    for m in markets:
        summary = {
            "id": m.get("id", "unknown"),
            "question": m.get("question", m.get("title", "N/A")),
            "description": (m.get("description") or "")[:300],
            "outcomePrices": m.get("outcomePrices", m.get("bestAsk", "N/A")),
            "volume": m.get("volume", "N/A"),
            "liquidity": m.get("liquidity", "N/A"),
            "endDate": m.get("endDate", m.get("end_date_iso", "N/A")),
        }
        market_summaries.append(summary)

    return f"""You are a prediction market analyst. Analyze the following Polymarket markets and provide trade suggestions.

For each market, evaluate:
1. Current probability/price and whether it seems mispriced
2. Market sentiment and any informational edge
3. A recommendation: buy YES, buy NO, or hold
4. Confidence level (low/medium/high)
5. Brief reasoning

Markets data:
{json.dumps(market_summaries, indent=2)}

Respond ONLY with valid JSON — an array of objects, one per market, with these exact keys:
- "market_id": string
- "title": string (the market question)
- "current_price": string (outcome prices or best ask)
- "recommendation": "buy_yes" | "buy_no" | "hold"
- "confidence": "low" | "medium" | "high"
- "reasoning": string (2-3 sentences)

No markdown fences, no commentary — just the JSON array."""


def analyze_with_llm(markets: list[dict]) -> list[dict]:
    """Send market data to OmniRoute LLM for analysis."""
    if not markets:
        return []

    client = OpenAI(base_url=OMNIROUTE_BASE_URL, api_key=OMNIROUTE_API_KEY)
    prompt = build_analysis_prompt(markets)

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a quantitative prediction market analyst. "
                        "Always respond with valid JSON only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=4096,
        )
        content = response.choices[0].message.content.strip()
        # Strip markdown fences if the model wraps them anyway
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            content = content.rsplit("```", 1)[0]
        return json.loads(content)
    except json.JSONDecodeError:
        return [{"error": "LLM returned invalid JSON", "raw": content}]
    except Exception as e:
        return [{"error": f"LLM analysis failed: {e}"}]


def run_analyze(limit: int = 20) -> None:
    """Analyze top active markets."""
    markets = fetch_markets(limit=limit)
    suggestions = analyze_with_llm(markets)
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "analyze",
        "markets_analyzed": len(markets),
        "suggestions": suggestions,
    }
    print(json.dumps(output, indent=2))


def run_search(query: str, limit: int = 20) -> None:
    """Search and analyze markets matching a query."""
    markets = fetch_markets(limit=limit, search=query)
    # Also do a client-side filter on the question/title text
    filtered = [
        m
        for m in markets
        if query.lower() in (m.get("question", "") + m.get("title", "")).lower()
    ]
    targets = filtered if filtered else markets
    suggestions = analyze_with_llm(targets)
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "search",
        "query": query,
        "markets_found": len(targets),
        "suggestions": suggestions,
    }
    print(json.dumps(output, indent=2))


def run_market(market_id: str) -> None:
    """Analyze a specific market by ID."""
    market = fetch_market_by_id(market_id)
    if market is None:
        print(json.dumps({"error": f"Market {market_id} not found"}))
        sys.exit(1)
    markets = [market] if isinstance(market, dict) else market
    suggestions = analyze_with_llm(markets)
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "market",
        "market_id": market_id,
        "suggestions": suggestions,
    }
    print(json.dumps(output, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Polymarket prediction market analyzer (analysis only, no trading)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze top active markets",
    )
    group.add_argument(
        "--search",
        type=str,
        metavar="QUERY",
        help='Search and analyze markets (e.g. --search "AI")',
    )
    group.add_argument(
        "--market-id",
        type=str,
        metavar="ID",
        help="Analyze a specific market by ID",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of markets to fetch (default: 20)",
    )
    args = parser.parse_args()

    if args.analyze:
        run_analyze(limit=args.limit)
    elif args.search:
        run_search(args.search, limit=args.limit)
    elif args.market_id:
        run_market(args.market_id)


if __name__ == "__main__":
    main()
