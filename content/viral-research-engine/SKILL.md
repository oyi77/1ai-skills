---
name: viral-research-engine
description: Use when researching trending topics, generating high-retention hooks, finding content gaps, and analyzing competitors for short-form video creators on TikTok, Reels, and Shorts. Focuses on Indonesian market patterns.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- viral
- research
- trends
- hooks
- competitors
- tiktok
- reels
- shorts
- indonesia
version: 1.0.0
category: content
---

# Viral Research Engine

Stop guessing. Research trending topics, discover content gaps, and generate high-retention hooks for TikTok, Instagram Reels, and YouTube Shorts (optimized for the Indonesian creator market).

## When to Use

**Trigger phrases:**
- "find viral trends" · "what's trending in Indonesia"
- "competitor content analysis" · "generate hooks for niche X"
- "find content gaps" · "TikTok trend research"

**Use cases:**
- Planning weekly content calendars based on active algorithm signals
- Writing hooks that stop the scroll in the first 2.5 s
- Benchmarking top creators in your niche to find underserved angles

## When NOT to Use

- Long-form SEO keyword research (Google Search) — use `seo-optimizer`
- Paid ads targeting & ROAS analysis — use `paid-ads`
- Academic or market research — use `market-research`

## Workflow

### 1. Trend Gathering (What's spiking right now?)

Scan current platform signals:
- **TikTok Creative Center:** check trending hashtags, songs, and creator formats in Region: Indonesia (ID).
- **Competitor scrape:** gather the top 20 videos from the last 7 days in your niche sorted by view count.

```python
# scrape_trends.py — collect recent top posts via Apify or public scrapers
import requests, json

def fetch_trending_niche(keyword: str, region: str = "ID") -> list[dict]:
    # Using a scraper or Apify TikTok scraper API
    url = "https://api.apify.com/v2/acts/clock~tiktok-scraper/run-sync-get-dataset-items"
    payload = {"search": keyword, "region": region, "resultsPerPage": 20, "sortBy": "viewCount"}
    # r = requests.post(url, json=payload, params={"token": os.environ["APIFY_TOKEN"]})
    # return r.json()
    return []
```

### 2. Content Gap Analysis (What are people missing?)

Look at the top 20 videos:
- **Common complaints:** Read the comments. What are viewers asking that the creator didn't answer? That's your next video's hook.
- **Format gaps:** If everyone is doing talking heads, do a clay animation or kinetic typography breakdown. If everyone is 60 s, do a 15 s punchy version.

### 3. Hook Generation (The 2.5 s rule)

The first 3 seconds determine 80% of video performance. Use proven Indonesian viral hook formulas:

| Hook Type | Formula / Example (ID) | Why it works |
|---|---|---|
| **The Warning** | "Jangan beli [Produk] sebelum tahu rahasia ini…" | Fear of missing out / making a mistake |
| **The Secret** | "Orang dalam agency ini bakal marah kalau aku bongkar cara…" | Curiosity gap / insider knowledge |
| **The Contrast** | "Gaji UMR tapi bisa nabung 5 juta sebulan? Caranya…" | Status incongruity / disbelief |
| **The Mistake** | "3 kesalahan fatal yang bikin video FYP kamu sepi terus…" | Pain point / corrective desire |
| **The Test** | "Aku tes AI paling mahal vs paling murah, hasilnya bikin kaget…" | Open loop / expected payoff |

### 4. Output a Content Brief

Structure the final research into a actionable brief for production:

```markdown
### Content Brief: [Topic]
- **Target Platform:** TikTok / Reels (9:16, 15–30 s)
- **Hook (0–3s):** [Chosen hook formula]
- **Visual Metaphor:** [What's on screen — e.g. split screen before/after]
- **Audio / B-Roll:** [Pexels query or background track vibe]
- **CTA:** [Comment keyword or LYNK link in bio]
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Viral content is pure luck" | It's pattern recognition. Hooks, pacing, and comment triggers are engineered. |
| "US trends work directly in Indonesia" | Cultural context matters. Localize humor, slang, and pricing references. |
| "I'll copy viral videos word-for-word" | Platforms penalize duplicate content and audiences spot clones. Steal the *structure*, change the substance. |
| "Views are the only metric" | Comments and saves drive the algorithm harder than passive views. Design for comment triggers. |

## Verification

- [ ] Top 20 competitor posts analyzed for the week
- [ ] Comment section mined for viewer questions / gaps
- [ ] Hook tested against at least 3 proven formulas (Warning, Secret, Contrast)
- [ ] Content brief includes 9:16 visual plan, script (<150 words/min), and CTA
- [ ] Localized for Indonesian audience (slang, currency, context)
