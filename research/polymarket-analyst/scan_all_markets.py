#!/usr/bin/env python3
"""
Polymarket Market Scanner - Working version
Scan all active markets with proper categorization
"""

import requests
import json
from datetime import datetime
from typing import Dict, List


class MarketCategorizer:
    """Categorize markets based on question/slug keywords"""

    CATEGORIES = {
        "Politics": [
            "trump",
            "biden",
            "ukraine",
            "russia",
            "election",
            "vote",
            "democrat",
            "republican",
            "congress",
            "senate",
            "president",
            "cabinet",
            "nomination",
            "nominee",
            "primary",
            "governor",
            "mayor",
            "clinton",
            "yang",
            "omar",
            "politics",
            "deport",
            "immigration",
        ],
        "Sports": [
            "nba",
            "epl",
            "premier",
            "football",
            "soccer",
            "baseball",
            "nfl",
            "nhl",
            "mlb",
            "arsenal",
            "chelsea",
            "manchester",
            "liverpool",
            "city",
            "united",
            "leeds",
            "basketball",
            "tennis",
            "golf",
            "mma",
            "boxing",
            "ufc",
            "olympics",
            "fifa",
            "lebron",
            "curry",
            "pacers",
            "ncaa",
            "march",
            "madness",
            "sun devils",
            "wolf pack",
        ],
        "Crypto": [
            "bitcoin",
            "btc",
            "ethereum",
            "eth",
            "crypto",
            "token",
            "blockchain",
            "defi",
            "nft",
            "altcoin",
            "mining",
            "bull",
            "bear",
            "marketcap",
            "satoshi",
        ],
        "Entertainment": [
            "gta",
            "vi",
            "grand theft",
            "game",
            "gaming",
            "movie",
            "film",
            "oscar",
            "emmy",
            "grammy",
            "award",
            "netflix",
            "disney",
            "spotify",
            "stream",
            "taylor",
            "swift",
            "kanye",
            "drake",
            "music",
            "album",
            "jesus",
            "bible",
        ],
        "Tech": [
            "ai",
            "artificial",
            "openai",
            "chatgpt",
            "google",
            "microsoft",
            "apple",
            "tesla",
            "elon",
            "musk",
            "twitter",
            "x.com",
            "spacex",
            "tech",
        ],
        "Economy": [
            "recession",
            "inflation",
            "fed",
            "interest",
            "rate",
            "gdp",
            "economy",
            "market",
            "stock",
            "nasdaq",
            "dow",
            "snp",
            "finance",
            "bank",
            "debt",
        ],
        "Science": [
            "space",
            "nasa",
            "mars",
            "moon",
            "rocket",
            "launch",
            "climate",
            "temperature",
        ],
        "Other": [],
    }

    def categorize(self, question: str, slug: str, description: str = "") -> str:
        """Categorize market based on content"""
        text = f"{question} {slug} {description}".lower()

        for category, keywords in self.CATEGORIES.items():
            for keyword in keywords:
                if keyword in text:
                    return category

        return "Other"


def scan_markets(limit: int = 1000) -> Dict:
    """Scan active markets from Polymarket CLOB API"""
    url = "https://clob.polymarket.com/markets"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        markets = data.get("data", [])

        # Filter for markets accepting orders (actively trading)
        active_markets = [
            m for m in markets if m.get("accepting_orders") and not m.get("archived")
        ]

        return {
            "markets": active_markets,
            "total": len(active_markets),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        return {
            "error": str(e),
            "markets": [],
            "total": 0,
            "timestamp": datetime.now().isoformat(),
        }


def get_market_price(market: Dict) -> float:
    """Extract YES probability from market tokens"""
    tokens = market.get("tokens", [])
    if tokens:
        # First token is usually YES
        return float(tokens[0].get("price", 0.5))
    return 0.5


def analyze_markets(markets_data: Dict) -> Dict:
    """Analyze and categorize markets"""
    categorizer = MarketCategorizer()

    if "error" in markets_data:
        return markets_data

    markets = markets_data.get("markets", [])

    # Categorize
    categories = {}
    for market in markets:
        category = categorizer.categorize(
            market.get("question", ""),
            market.get("market_slug", ""),
            market.get("description", ""),
        )
        if category not in categories:
            categories[category] = []
        categories[category].append(market)

    # Calculate stats
    stats = {
        "total_markets": len(markets),
        "by_category": {cat: len(mkt) for cat, mkt in categories.items()},
        "categories_detail": {},
    }

    # Sort categories
    stats["by_category"] = dict(
        sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True)
    )

    return {
        "stats": stats,
        "categories": categories,
        "timestamp": markets_data.get("timestamp", datetime.now().isoformat()),
    }


def print_report(analysis: Dict):
    """Print formatted report"""
    print("=" * 70)
    print("POLYMARKET MARKET SCAN")
    print("=" * 70)
    print()

    if "error" in analysis:
        print(f"ERROR: {analysis['error']}")
        return

    stats = analysis.get("stats", {})
    categories = analysis.get("categories", {})

    # Summary
    print(f"Total Active Markets: {stats.get('total_markets', 0)}")
    print(f"Timestamp: {analysis.get('timestamp', datetime.now().isoformat())}")
    print()

    # Category breakdown
    print("CATEGORY BREAKDOWN")
    print("-" * 70)
    for cat, count in stats.get("by_category", {}).items():
        pct = (count / stats.get("total_markets", 1)) * 100
        print(f"{cat:15s}: {count:4d} markets ({pct:5.1f}%)")
    print("-" * 70)
    print(f"{'TOTAL':15s}: {stats.get('total_markets', 0):4d} markets (100.0%)")
    print()

    # Detailed markets by category
    print("DETAILED MARKET LISTING")
    print("-" * 70)
    for cat, markets in sorted(
        categories.items(), key=lambda x: len(x[1]), reverse=True
    ):
        print(f"\n[{cat.upper()}] - {len(markets)} markets")
        print("-" * 70)
        for i, m in enumerate(markets, 1):
            question = m.get("question", "N/A")[:45]
            price = get_market_price(m)
            yes_pct = price * 100
            no_pct = 100 - yes_pct
            print(f"{i:2d}. {question:45s} | YES {yes_pct:5.1f}% | NO {no_pct:5.1f}%")

    print()
    print("=" * 70)
    print(f"Scan completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)


def main():
    """Main entry point"""
    print("Scanning Polymarket CLOB API...")
    data = scan_markets()

    if "error" in data:
        print(f"Error: {data['error']}")
        return

    print(f"Found {data['total']} active markets")
    print("Categorizing...")

    analysis = analyze_markets(data)
    print_report(analysis)

    # Save to file
    output_file = "market_scan_latest.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
