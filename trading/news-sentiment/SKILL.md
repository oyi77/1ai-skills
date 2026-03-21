---
name: news-sentiment
description: Fetch news and social sentiment for any asset via DuckDuckGo + LLM scoring. Returns bullish/bearish/neutral with confidence, key themes, and headlines. Use for pre-trade sentiment checks.
permissions:
  - fs
  - network
---

# News Sentiment Analyzer

Fetch recent news and social signals for any asset, then score sentiment via OmniRoute LLM.

## Usage

```bash
python scripts/news_sentiment.py --asset "gold XAUUSD" --limit 10
python scripts/news_sentiment.py --asset "bitcoin BTC" --limit 5
python scripts/news_sentiment.py --asset "NVDA nvidia" --json
```

## Output

```json
{
  "asset": "gold XAUUSD",
  "sentiment": "bullish",
  "confidence": 0.78,
  "key_themes": ["safe haven demand", "Fed pause expectations"],
  "news_headlines": [...],
  "social_buzz": "moderate",
  "timestamp": "..."
}
```

## Pipeline

1. Fetch news via duckduckgo-search
2. Aggregate headlines and summaries
3. LLM sentiment scoring (bullish/bearish/neutral, confidence 0-1)
4. Extract key themes and buzz level

## Dependencies

```bash
pip install duckduckgo-search openai
```
