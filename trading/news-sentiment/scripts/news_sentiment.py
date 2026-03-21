#!/usr/bin/env python3
"""
News Sentiment Analyzer — fetch news + LLM sentiment scoring.

Usage:
    python news_sentiment.py --asset "gold XAUUSD" --limit 10
    python news_sentiment.py --asset "bitcoin BTC" --json
"""

import argparse
import json
import sys
from datetime import datetime

OMNIROUTE_BASE = "http://localhost:20128/v1"
OMNIROUTE_KEY = "omniroute"
OMNIROUTE_MODEL = "auto/pro-chat"


def fetch_news(query, limit=10):
    """Fetch news headlines via duckduckgo-search."""
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        print("ERROR: duckduckgo-search not installed. Run: pip install duckduckgo-search")
        sys.exit(1)

    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.news(query, max_results=limit):
                results.append({
                    "title": r.get("title", ""),
                    "source": r.get("source", ""),
                    "date": r.get("date", ""),
                    "body": r.get("body", "")[:200],
                    "url": r.get("url", ""),
                })
    except Exception as e:
        print(f"Warning: News fetch error: {e}")
    return results


def analyze_sentiment(asset, headlines):
    """Score sentiment via OmniRoute LLM."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai not installed. Run: pip install openai")
        sys.exit(1)

    client = OpenAI(base_url=OMNIROUTE_BASE, api_key=OMNIROUTE_KEY)

    news_text = "\n".join(
        f"- [{h['source']}] {h['title']}: {h['body']}" for h in headlines
    )

    prompt = f"""Analyze the sentiment for {asset} based on these recent news headlines:

{news_text}

Return ONLY valid JSON with this exact structure:
{{
  "sentiment": "bullish" | "bearish" | "neutral",
  "confidence": 0.0 to 1.0,
  "key_themes": ["theme1", "theme2", "theme3"],
  "social_buzz": "high" | "moderate" | "low",
  "summary": "one sentence summary"
}}"""

    try:
        resp = client.chat.completions.create(
            model=OMNIROUTE_MODEL,
            messages=[
                {"role": "system", "content": "You are a financial sentiment analyst. Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )
        raw = resp.choices[0].message.content
        # Extract JSON from response
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except Exception as e:
        print(f"Warning: LLM analysis error: {e}")

    return {
        "sentiment": "neutral",
        "confidence": 0.0,
        "key_themes": [],
        "social_buzz": "unknown",
        "summary": "Analysis unavailable",
    }


def run_sentiment(asset, limit=10):
    """Full sentiment analysis pipeline."""
    print(f"[News Sentiment] Analyzing: {asset}")
    print(f"  Fetching up to {limit} news items...")

    headlines = fetch_news(asset, limit)
    print(f"  Found {len(headlines)} headlines")

    if not headlines:
        return {
            "asset": asset,
            "sentiment": "neutral",
            "confidence": 0.0,
            "key_themes": [],
            "news_headlines": [],
            "social_buzz": "none",
            "timestamp": datetime.now().isoformat(),
            "error": "No news found",
        }

    print("  Running LLM sentiment analysis...")
    analysis = analyze_sentiment(asset, headlines)

    result = {
        "asset": asset,
        "sentiment": analysis.get("sentiment", "neutral"),
        "confidence": analysis.get("confidence", 0.0),
        "key_themes": analysis.get("key_themes", []),
        "news_headlines": [h["title"] for h in headlines],
        "social_buzz": analysis.get("social_buzz", "unknown"),
        "summary": analysis.get("summary", ""),
        "timestamp": datetime.now().isoformat(),
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="News Sentiment Analyzer")
    parser.add_argument("--asset", required=True, help="Asset name (e.g., 'gold XAUUSD', 'bitcoin BTC')")
    parser.add_argument("--limit", type=int, default=10, help="Number of news items to fetch")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()
    result = run_sentiment(args.asset, args.limit)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print()
        s = result["sentiment"].upper()
        c = result["confidence"]
        print(f"  Sentiment: {s} (confidence: {c:.0%})")
        print(f"  Buzz: {result['social_buzz']}")
        if result.get("summary"):
            print(f"  Summary: {result['summary']}")
        if result["key_themes"]:
            print(f"  Themes: {', '.join(result['key_themes'])}")
        print(f"  Headlines ({len(result['news_headlines'])}):")
        for h in result["news_headlines"][:5]:
            print(f"    • {h}")


if __name__ == "__main__":
    main()
