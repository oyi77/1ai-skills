---
name: gate-news-briefing
description: Use when produce a crypto news + sentiment briefing — latest events, trending stories, and social sentiment via web search and public sources. Use when working with crypto news briefing.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
  - gate
  - news
  - research
  - crypto
  - sentiment
  - briefing
version: 1.0.0
category: research
---

## Overview

`gate-news-briefing` runs a **news + sentiment briefing playbook** using web search and public crypto-news sources. It assembles recent major events, trending stories, and a social-sentiment read. Standalone, tool-agnostic rewrite of the upstream `gate-news-briefing` skill (which used 3 MCP tools: news events, news feed search, social sentiment). Here those map to general web_search + source aggregation.

## When to Use

- "What happened recently in crypto"
- "Today's crypto highlights"
- "Any new updates / news"
- "Crypto news briefing"

## When NOT to Use

- A specific coin's fundamentals — use `gate-info-coinanalysis`.
- Market-wide price snapshot — use `gate-info-marketoverview`.
- Multi-dimension research (price + news combined) — use `gate-info-research`.

## Workflow

### Step 1 — Major events (last 24–72h)

```bash
# Use web_search (general tool) for recent crypto news
web_search("crypto major news last 24 hours", recency="day", limit=10)
```

### Step 2 — Trending stories

```bash
web_search("trending crypto stories today", recency="day", limit=10)
```

### Step 3 — Social sentiment

Search X/Twitter and major crypto forums for the top 3 stories; classify sentiment (bullish/bearish/neutral) per story from headline + reply tone.

### Step 4 — Synthesize

```
## News Briefing  (playbook: news_briefing)
### Major Events
- [event] — [1-line impact]
### Trending
- [story] — [why it's trending]
### Sentiment
- Overall: bullish / neutral / bearish (with the 1–2 drivers)
### Sources
- web_search queries + named outlets
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "One headline = the story" | Triangulate 2–3 sources before stating impact. |
| "Trending = important" | Trending is attention; weight by source credibility. |
| "Sentiment is a price call" | Sentiment is a read on attention/mood, not a forecast. |

## Code Example

Pull recent crypto news with the general web tool:

```bash
web_search("crypto market news today", recency="day", limit=8)
# → [ {title:"ETF inflows resume", url:...}, {title:"L2 TVL dips", url:...}, ... ]
```

## Verification

- [ ] Major events pulled for the stated window (24–72h) via web_search.
- [ ] Trending stories separated from major events.
- [ ] Social sentiment classified per top story with drivers named.
- [ ] Output follows the News Briefing template (Major / Trending / Sentiment / Sources).
- [ ] Sources named (queries + outlets); no unattributed claims.
