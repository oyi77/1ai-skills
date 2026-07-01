---
name: competitive-intelligence
description: Continuous competitor monitoring — pricing changes, feature launches, job postings, ad spend, SEO rankings, social
  media activity — with weekly intelligence briefs and strategic recommendations
domain: research
tags:
- analysis
- competitive
- intelligence
- investigation
- monitoring
- research
- seo
- social-media
---

## Overview

Automated competitive intelligence engine that monitors competitors across multiple signals (pricing, features, hiring, SEO, ads, social), detects meaningful changes, and generates weekly intelligence briefs with strategic recommendations. Turns raw competitor data into actionable business intelligence for a one-person company.

## Required Tools

- **Web scraping**: `curl`, `wget`, `puppeteer`/`playwright` for dynamic pages
- **RSS/Atom feeds**: `feedparser` (Python), `rss-parser` (Node.js)
- **SEO monitoring**: Ahrefs API, SEMrush API, or SerpAPI for ranking tracking
- **Social monitoring**: Twitter/X API v2, Reddit API, LinkedIn scraping
- **Job boards**: LinkedIn Jobs API, Indeed scraping, Greenhouse/Lever APIs
- **Storage**: SQLite or JSON files for historical data
- **Notification**: Slack webhook, email, or Discord webhook

## Capabilities

- Build and maintain competitor profiles with structured metadata
- Monitor pricing pages for changes via scheduled scraping
- Track feature launches through changelog RSS, blog posts, and Product Hunt
- Detect hiring surges that signal strategic shifts (e.g., hiring ML team = AI pivot)
- Monitor SEO ranking changes and new content published by competitors
- Track ad spend changes via Facebook Ad Library, Google Ads Transparency
- Monitor social media activity spikes and sentiment shifts
- Generate weekly intelligence briefs with trend analysis and strategic recommendations
- Alert on critical changes in real-time (pricing drops, new product launches)

## When to Use
**Trigger phrases:**
- "competitive intelligence"
- "Continuous competitor monitoring — pricing changes, feature launches, job postin"


- Setting up competitive monitoring for a new market or product category
- Weekly strategy review needs current competitor landscape
- Competitor launches a new feature and you need impact assessment
- Planning pricing changes and need competitor pricing intelligence
- Investor/board meeting prep requiring competitive landscape overview
- Detecting new market entrants or competitor pivots early

## When NOT to Use

- Task is about implementation, not research (use implementation skills)
- Task is about analysis of existing data (use analysis skills)
- You need to build research tools (use development skills)
- Task is about testing hypotheses (use test skills)
- You don't have access to research sources
- Task requires domain expertise (consult experts)


## Pseudo Code

Implementation patterns for common use cases with this skill.


### 1. Competitor Profile Setup

```python
# competitors.json - structured competitor profiles
competitors = [
    {
        "name": "CompetitorA",
        "domain": "competitora.com",
        "category": "direct",
        "pricing_url": "https://competitora.com/pricing",
        "blog_url": "https://competitora.com/blog",
        "changelog_url": "https://competitora.com/changelog",
        "careers_url": "https://competitora.com/careers",
        "social": {
            "twitter": "@competitora",
            "linkedin": "company/competitora"
        },
        "keywords": ["competitor brand term", "product name"]
    }
]
```

### 2. Pricing Monitor

```bash
# Cron job: daily pricing scrape
# Run via: crontab -e or scheduled task

# Scrape pricing page
curl -s "https://competitora.com/pricing" > /tmp/pricing_raw.html

# Extract pricing with text parsing
python3 -c "
from bs4 import BeautifulSoup
import json, hashlib

with open('/tmp/pricing_raw.html') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

prices = [el.text.strip() for el in soup.select('[class*=price], [class*=plan]')]
current_hash = hashlib.md5(json.dumps(prices).encode()).hexdigest()

# Compare with last known hash
try:
    with open('.intel/pricing_hash.json') as f:
        last = json.load(f)
    if last.get('hash') != current_hash:
        print(f'PRICING CHANGE DETECTED: {prices}')
        # Send alert
        import urllib.request
        urllib.request.urlopen(urllib.request.Request(
            'https://hooks.slack.com/services/YOUR/WEBHOOK',
            data=json.dumps({'text': f'🚨 Pricing change: {prices}'}).encode()
        ))
except FileNotFoundError:
    pass

# Save current state
with open('.intel/pricing_hash.json', 'w') as f:
    json.dump({'hash': current_hash, 'prices': prices, 'timestamp': '$(date -u +%FT%TZ)'}, f)
"
```

### 3. Feature Launch Detection

```bash
# Monitor changelog RSS + blog RSS for new entries
python3 << 'PYEOF'
import feedparser
import json
import os

INTEL_DIR = ".intel"
SEEN_FILE = f"{INTEL_DIR}/seen_entries.json"

os.makedirs(INTEL_DIR, exist_ok=True)
seen = json.load(open(SEEN_FILE)) if os.path.exists(SEEN_FILE) else {}

feeds = {
    "changelog": "https://competitora.com/changelog/rss",
    "blog": "https://competitora.com/blog/rss",
    "product_hunt": "https://www.producthunt.com/feed"
}

alerts = []
for source, url in feeds.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:10]:
        entry_id = entry.get("id", entry.get("link"))
        if entry_id not in seen:
            seen[entry_id] = {"source": source, "title": entry.title, "link": entry.link}
            alerts.append(f"[{source}] {entry.title}: {entry.link}")

if alerts:
    print("NEW ENTRIES DETECTED:")
    for a in alerts:
        print(f"  - {a}")
    # Send to Slack/Discord

json.dump(seen, open(SEEN_FILE, "w"), indent=2)
PYEOF
```

### 4. Job Posting Intelligence

```bash
# Scrape careers page for hiring signals
python3 << 'PYEOF'
import requests
from bs4 import BeautifulSoup
import json

url = "https://competitora.com/careers"
resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(resp.text, "html.parser")

jobs = []
for el in soup.select("[class*=job], [class*=position], [class*=opening]"):
    title = el.select_one("h2, h3, .title")
    dept = el.select_one("[class*=department], [class*=team]")
    loc = el.select_one("[class*=location]")
    if title:
        jobs.append({
            "title": title.text.strip(),
            "department": dept.text.strip() if dept else "Unknown",
            "location": loc.text.strip() if loc else "Unknown"
        })

# Analyze hiring signals
signals = {"engineering": 0, "sales": 0, "marketing": 0, "ml/ai": 0, "security": 0}
for job in jobs:
    title_lower = job["title"].lower()
    if any(k in title_lower for k in ["engineer", "developer", "sre", "platform"]):
        signals["engineering"] += 1
    elif any(k in title_lower for k in ["sales", "account", "revenue"]):
        signals["sales"] += 1
    elif any(k in title_lower for k in ["market", "growth", "content"]):
        signals["marketing"] += 1
    elif any(k in title_lower for k in ["ml", "ai", "machine learning", "data scien"]):
        signals["ml/ai"] += 1
    elif any(k in title_lower for k in ["security", "infosec", "appsec"]):
        signals["security"] += 1

print(f"Total jobs: {len(jobs)}")
print(f"Hiring signals: {json.dumps(signals, indent=2)}")

# Flag significant signals
if signals["ml/ai"] >= 2:
    print("⚠️  SIGNAL: Heavy ML/AI hiring — possible AI pivot")
if signals["sales"] >= 3:
    print("⚠️  SIGNAL: Sales team expansion — scaling revenue")
PYEOF
```

### 5. SEO & Content Monitoring

```bash
# Track competitor's new content and ranking changes
python3 << 'PYEOF'
import requests
import json
from datetime import datetime

# Option A: Use SerpAPI for ranking tracking
SERPAPI_KEY = "your_key"
competitor_domain = "competitora.com"
keywords = ["best project management tool", "task automation software"]

for kw in keywords:
    resp = requests.get("https://serpapi.com/search", params={
        "q": kw,
        "api_key": SERPAPI_KEY,
        "num": 20
    })
    results = resp.json().get("organic_results", [])
    for i, r in enumerate(results):
        if competitor_domain in r.get("link", ""):
            print(f"Keyword: '{kw}' → Position {i+1}: {r['link']}")
            break
    else:
        print(f"Keyword: '{kw}' → Not in top 20")

# Option B: Use Ahrefs API for backlink/content monitoring
# GET https://apiv2.ahrefs.com?token=TOKEN&target=competitora.com&mode=subdomains&limit=10&output=json
PYEOF
```

### 6. Weekly Intelligence Brief Generation

```bash
# Generate weekly brief from collected data
python3 << 'PYEOF'
import json
import os
from datetime import datetime, timedelta

INTEL_DIR = ".intel"
BRIEF_DIR = f"{INTEL_DIR}/briefs"
os.makedirs(BRIEF_DIR, exist_ok=True)

week_start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
week_end = datetime.now().strftime("%Y-%m-%d")

# Load all signal data
signals = {
    "pricing_changes": json.load(open(f"{INTEL_DIR}/pricing_changes.json")) if os.path.exists(f"{INTEL_DIR}/pricing_changes.json") else [],
    "feature_launches": json.load(open(f"{INTEL_DIR}/feature_launches.json")) if os.path.exists(f"{INTEL_DIR}/feature_launches.json") else [],
    "hiring_signals": json.load(open(f"{INTEL_DIR}/hiring_signals.json")) if os.path.exists(f"{INTEL_DIR}/hiring_signals.json") else [],
    "seo_changes": json.load(open(f"{INTEL_DIR}/seo_changes.json")) if os.path.exists(f"{INTEL_DIR}/seo_changes.json") else [],
}

brief = f"""# Competitive Intelligence Brief
## Week of {week_start} to {week_end}

Key aspects of competitive-intelligence relevant to this section.


### Key Changes This Week
- Pricing: {len(signals['pricing_changes'])} changes detected
- Features: {len(signals['feature_launches'])} launches/updates
- Hiring: {len(signals['hiring_signals'])} new postings
- SEO: {len(signals['seo_changes'])} ranking shifts

### Pricing Changes
{chr(10).join(f'- {c}' for c in signals['pricing_changes']) or 'No changes detected.'}

### Feature Launches
{chr(10).join(f'- {f}' for f in signals['feature_launches']) or 'No launches detected.'}

### Hiring Signals
{chr(10).join(f'- {h}' for h in signals['hiring_signals']) or 'No significant postings.'}

### Strategic Recommendations
1. [AI-generated based on signal analysis]
2. [Actionable next steps]

### Sources
- Pricing: automated daily scrape
- Features: RSS/changelog monitoring
- Hiring: careers page scraping
- SEO: SerpAPI/Ahrefs tracking
"""

brief_path = f"{BRIEF_DIR}/brief-{week_end}.md"
with open(brief_path, "w") as f:
    f.write(brief)
print(f"Brief written to {brief_path}")
PYEOF
```

### 7. Full Pipeline Orchestration

```bash
#!/bin/bash
# competitive-intel-pipeline.sh — run daily via cron
# 0 8 * * * /path/to/competitive-intel-pipeline.sh

set -euo pipefail
INTEL_DIR=".intel"
mkdir -p "$INTEL_DIR"

echo "[$(date)] Starting competitive intelligence pipeline"

# 1. Pricing check
python3 scripts/pricing_monitor.py

# 2. Feature/changelog check
python3 scripts/feature_monitor.py

# 3. Job posting check (daily)
python3 scripts/hiring_monitor.py

# 4. SEO check (weekly — Monday only)
if [ "$(date +%u)" = "1" ]; then
    python3 scripts/seo_monitor.py
fi

# 5. Social monitoring
python3 scripts/social_monitor.py

# 6. Weekly brief (Friday only)
if [ "$(date +%u)" = "5" ]; then
    python3 scripts/generate_brief.py
    # Email/Slack the brief
    cat "$INTEL_DIR/briefs/brief-$(date +%Y-%m-%d).md" | \
        curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\": \"$(cat)\"}" \
        "https://hooks.slack.com/services/YOUR/WEBHOOK"
fi

echo "[$(date)] Pipeline complete"
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|---------|
| HTTP 429 (rate limit) | Too many requests to target site | Implement exponential backoff, reduce scrape frequency |
| HTTP 403 (blocked) | Anti-bot detection | Rotate User-Agent, add delays, use proxy rotation |
| Empty RSS feed | Feed URL changed or down | Log warning, try alternative source (direct page scrape) |
| Stale data | Scraper silently failing | Track last-successful-run timestamp, alert if >24h stale |
| API key expired | Ahrefs/SerpAPI key rotated | Check API health at pipeline start, fail fast with clear error |
| Parse failure | Website HTML structure changed | Store raw HTML snapshot, alert for manual review |

## Common Patterns

**Pattern 1: Signal Accumulation** — Store raw signals in append-only JSON files. Deduplicate on brief generation. Never delete historical signals — they enable trend analysis.

**Pattern 2: Change Detection via Hashing** — Hash the relevant content (pricing table, feature list) and compare with previous hash. Only trigger alerts on actual changes, not page noise.

**Pattern 3: Tiered Alerting** — Real-time alerts for critical changes (pricing drops, new product launches) via Slack webhook. Daily digest for minor changes. Weekly brief for trends.

**Pattern 4: Graceful Degradation** — If one data source fails, continue with others. Mark failed sources in the brief so you know what's missing. Don't let one broken scraper block the entire pipeline.

**Pattern 5: Historical Baseline** — On first run, capture a full baseline snapshot. All subsequent runs compare against baseline + recent history. This prevents false positives from initial setup.

## Red Flags

- Using outdated or unreliable sources
- Not verifying competitive intelligence
- Ignoring ethical considerations
- Not protecting confidential information
- Missing source documentation

## Verification

- [ ] Sources are reliable and current
- [ ] Intelligence is verified
- [ ] Ethical guidelines are followed
- [ ] Confidential information is protected
- [ ] Sources are documented

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "First result is good enough" | Deep research finds better answers. Keep digging. |
| "I do not need to verify sources" | Unverified sources lead to wrong conclusions. Always cross-check. |
| "Research is a one-time thing" | Markets change. Research needs to be continuous, not one-off. |