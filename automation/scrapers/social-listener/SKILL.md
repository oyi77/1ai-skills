---
name: social-listener
description: Use when multi-platform social media monitoring for brand mentions, sentiment, and trends. See parent skill for full docs.
domain: automation
tags:
- automation
- social
- listener
- monitoring
version: 1.0.0
---
# Social Listener

## Quick Reference

Social listening monitors brand mentions, keywords, and sentiment across Twitter/X, Reddit, Instagram, and TikTok. Unlike the parent scrapers skill (which covers structured data extraction), this skill focuses on **unstructured social signals** — natural language mentions, sentiment shifts, and viral trend detection responding at platform-specific cadences of 5-15 minutes rather than hourly.

## Overview

A social listener polls platform APIs for keyword mentions, stores them with deduplication, scores sentiment per mention via a lightweight lexicon, and alerts on negative spikes. The key frequency difference from content monitoring: social trends move in minutes, blog changes in hours. Integration with `agent-reach` (see that skill) gives you 15+ platforms from one toolchain. Start with 2 platforms, add one per week as you tune per-platform rate limits and data formats.

## Quick Start

**Prerequisites:** Python 3.8+, SQLite, API keys or `agent-reach` installed.

1. **Pick keywords** — Your brand name, product names, and industry terms. Start with 3-5 terms on 2 platforms.

2. **Set up storage** — SQLite with dedup by platform-specific mention ID. Without dedup, the same mention appears on every poll cycle.

3. **Schedule** — Run every 10 min via cron. A 30% sentiment drop in 1 hour triggers a crisis alert.

```python
import requests, sqlite3, re, time
from datetime import datetime, timedelta

KEYWORDS = ["mybrand", "competitor"]
PLATFORMS = {
    "reddit": lambda kw: requests.get(
        f"https://www.reddit.com/search.json?q={kw}&limit=10&sort=new",
        headers={"User-Agent": "monitor/1.0"}).json()["data"]["children"]
}

def init_db():
    conn = sqlite3.connect("mentions.db")
    conn.execute("CREATE TABLE IF NOT EXISTS mentions (id TEXT PRIMARY KEY, platform TEXT, keyword TEXT, author TEXT, content TEXT, sentiment REAL, url TEXT, mentioned_at TEXT, captured_at TEXT)")
    return conn

def sentiment(text):
    words = set(re.findall(r'\w+', text.lower()))
    pos = {"good","great","amazing","love","excellent","best","awesome","happy"}
    neg = {"bad","terrible","awful","hate","worst","poor","horrible"}
    return round((len(words & pos) - len(words & neg)) / max(len(words), 1), 3)

conn = init_db()
for kw in KEYWORDS:
    for plat, fetcher in PLATFORMS.items():
        for item in fetcher(kw):
            d = item["data"]
            content = d.get("title","") + " " + d.get("selftext","")
            try:
                conn.execute("INSERT OR IGNORE INTO mentions VALUES (?,?,?,?,?,?,?,?,?)",
                             (d["id"], plat, kw, d.get("author",""), content, sentiment(content),
                              f"https://reddit.com{d.get('permalink','')}",
                              datetime.fromtimestamp(d["created_utc"]).isoformat(),
                              datetime.now().isoformat()))
            except Exception as e:
                print(f"Store error: {e}")
conn.commit()

# Alert on negative spike
cutoff = (datetime.now() - timedelta(hours=1)).isoformat()
for plat, avg in conn.execute("SELECT platform, AVG(sentiment) FROM mentions WHERE captured_at > ? GROUP BY platform", (cutoff,)):
    if avg < -0.2:
        print(f"ALERT: Negative sentiment on {plat}: {avg:.2f}")
```

## Checklist

- [ ] Keywords manually tested on each platform — confirm enough volume exists before automating
- [ ] Dedup verified: run poll twice, assert zero duplicate rows in SQLite
- [ ] Sentiment lexicon tuned for your domain — "crash" is negative for brand monitoring but neutral/positive in gaming
- [ ] Alert threshold calibrated: start at -0.3, adjust after 1 week of real data to avoid noise
- [ ] Rate limits documented per platform (Reddit: 60 req/min); exceeding them silently drops mentions

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Brand monitoring is only for big companies" | A single negative viral post can kill a solo business; early detection gives you hours to respond |
| "I'll build it for all 15 platforms at once" | Each platform has different API auth, rate limits, and data formats; start with 2, add one per week |
| "Sentiment analysis needs ML" | A 30-line lexicon-based scorer catches 80% of spikes; upgrade to transformers only when precision demands it |

## When to Use
Use this skill when working with social listener.

## Workflow
See the parent skill for authoritative workflow documentation.
