---
name: content-planner-auto
description: Auto-generate 30-day content calendars with pillar rotation, platform-optimized timing, multi-account rotation,
  seasonal Indonesian events, and PostBridge batch scheduling.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- auto
- content
- content-creation
- digital-content
- media
- planner
- money
version: 1.0.0
---
# Content Planner Auto

Auto-generate 30-day content calendars for your brand or clients. Revenue survival tool.

## When to Use

**Trigger phrases:**
- "content planner auto"
- "Help me with content planner auto"
- "generate content calendar"
- "plan my content for the month"

**Use cases:**
- When the task matches this skill's domain expertise
- Creating monthly content calendars for clients
- Scheduling multi-platform content in batches
- Aligning content with seasonal events (especially Indonesian)
- Managing multiple brand/account content streams

**When NOT to use:**
- For tasks outside this skill's scope
- When real-time data is required (use live data feeds)
- For content requiring deep domain expertise you lack
- For legal, medical, or financial advice content

## Overview

Content Planner Auto produces professional 30-day content calendars with pillar topic rotation, platform-optimized posting times, multi-account rotation, seasonal Indonesian event alignment, and PostBridge batch scheduling integration.

## Money-Making Overview

**Buyer Persona:** SMEs, agencies, and e-commerce brands in Indonesia/US that post content but have no content strategy. They post when they remember. They need a calendar that keeps them consistent.

**Pricing Tiers:**

| Tier | Price | What They Get |
|------|-------|---------------|
| Monthly Calendar | $200/mo | 30-day calendar, 1 platform, pillar rotation + seasonal hooks |
| Multi-Platform | $500/mo | 30-day calendar across 3 platforms, timing optimized per platform, PostBridge scheduling |
| Retainer + Execution | $800/mo | Full calendar + caption writing + asset briefs + weekly performance note |

**First-Dollar Timeline:** Day 1 — run the script below for any client niche and deliver a calendar by end of day. $200 in your pocket.

## First Action in 60 Minutes

Copy-paste this script. Replace `NICHE`, `PLATFORMS`, and `BRAND_VOICE` with a real client's info. It outputs a 30-day calendar CSV ready to send.

```bash
#!/usr/bin/env python3
# generate_calendar.py — 30-day content calendar for any niche
# Usage: python3 generate_calendar.py > calendar_<client>_<month>.csv

import csv, sys, json
from datetime import datetime, timedelta
from textwrap import dedent

# ── CLIENT CONFIG (edit these) ──────────────────────────────
CLIENT = "UrbanWear Indonesia"
NICHE = "streetwear fashion"
PLATFORMS = ["Instagram", "TikTok", "Shopee Feed"]
BRAND_VOICE = "edgy, Gen Z, casual Indonesian with English slang"
PILLARS = ["outfit inspo", "new arrivals", "styling tips", "behind the scenes", "customer looks"]
SEASONAL_HOOKS = [
    "Hari Kemerdekaan special drop",
    "Back to campus fit check",
    "Rainy season layering guide",
]
# ────────────────────────────────────────────────────────────

HEADERS = ["Day", "Date", "Platform", "Pillar", "Topic", "Hook/Format", "CTA", "Assets Needed", "Notes"]
today = datetime.now().date()
rows = []

for day_offset in range(30):
    date = today + timedelta(days=day_offset)
    pillar = PILLARS[day_offset % len(PILLARS)]
    platform = PLATFORMS[day_offset % len(PLATFORMS)]
    hook = SEASONAL_HOOKS[day_offset % len(SEASONAL_HOOKS)] if day_offset < 3 else ""

    rows.append({
        "Day": day_offset + 1,
        "Date": date.isoformat(),
        "Platform": platform,
        "Pillar": pillar,
        "Topic": f"[{pillar}] — {CLIENT} {NICHE} content #{day_offset+1}",
        "Hook/Format": hook or "Reel / Carousel / Single Image",
        "CTA": "Shop now (link in bio)",
        "Assets Needed": "Product photo, user UGC, or flat lay",
        "Notes": BRAND_VOICE,
    })

writer = csv.DictWriter(sys.stdout, fieldnames=HEADERS)
writer.writeheader()
writer.writerows(rows)

print(f"\n# Calendar for {CLIENT} — {today.strftime('%B %Y')}", file=sys.stderr)
print(f"# Generated: {len(rows)} posts across {len(PLATFORMS)} platforms", file=sys.stderr)
```

**To deliver:**
```bash
python3 generate_calendar.py > calendar_urbanwear_august.csv
# Open in Google Sheets or Excel, brand with client logo, send as PDF
```

## Deliverable Format

**Invoice-ready: Content Calendar Report**

Deliver as branded PDF or shared Google Sheet. Include:

```
── CONTENT CALENDAR ──
Client: [NAME]
Month: [MONTH YEAR]
Platforms: [LIST]
Post Frequency: [N] posts/week

── MONTH OVERVIEW ──
Week 1: [Theme] — [3-5 post topics]
Week 2: [Theme] — [3-5 post topics]
Week 3: [Theme] — [3-5 post topics]
Week 4: [Theme] — [3-5 post topics]
Seasonal Hooks: [events, holidays, promos]

── PLATFORM BREAKDOWN ──
Instagram: [posts] — Reels: [N], Carousel: [N], Static: [N]
TikTok: [posts] — Trend: [N], Original: [N]
[Other]: [posts]

── DAILY SCHEDULE ──
[Table: Date | Platform | Pillar | Topic | Format | CTA | Status]

── NEXT STEPS ──
1. Review and approve calendar (48h)
2. Provide assets for Week 1 shoots
3. We schedule and caption once approved

── PRICING ──
[Selected Tier]: $[AMOUNT]/month
Next month renewal: [DATE]
```

Price anchor: show the calendar as a stand-alone deliverable. Up sell to caption writing (+$150/mo), asset briefs (+$200/mo), or full execution (+$400/mo).

## Workflow

1. **Client Brief** — Niche, brand voice, platforms, posting frequency, seasonal events
2. **Pillar Setup** — 4-6 content pillars that map to their business goals
3. **Calendar Generation** — 30-day schedule with pillar rotation, platform timing, seasonal hooks
4. **Review & Adjust** — Client reviews, you tweak, they approve
5. **Schedule & Execute** — Push to PostBridge or platform schedulers
6. **Deliver + Invoice** — Send calendar, collect payment, set renewal reminder

## Quality Checklist

- [ ] Pillars cover full funnel (awareness → consideration → conversion)
- [ ] Platform timing matches audience peak hours
- [ ] Seasonal hooks and local events incorporated
- [ ] Content variety: video, static, carousel, story
- [ ] CTA aligned with each post goal
- [ ] Asset needs noted so client can prepare
- [ ] Calendar sent before month start (recommend 14 days prior)

## Tools

- PostBridge for batch scheduling
- Google Sheets / Airtable for client-facing calendars
- Canva / Figma for visual asset briefs
- Analytics platform for performance tracking (adjust next month)

## Process

1. **Research** — Analyze target audience, competitors, and trending topics
2. **Create** — Generate content following brand guidelines and best practices
3. **Publish & Optimize** — Distribute to target platforms, track performance, iterate

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "They can plan their own content" | SMEs run on chaos. A calendar is the first thing they outsource when they realize consistency = revenue. |
| "$200 is too cheap for a spreadsheet" | It's not a spreadsheet. It's strategy + schedule + peace of mind. Price the outcome, not the file format. |
| "I'll just give them a template, they fill it in" | They won't. They pay you to think, not to format cells. |
| "I need to know their niche deeply first" | You need their ICP and top 3 offers. 30 minutes of research is enough. They correct what's wrong. |
| "Calendars don't retain — they'll cancel after month 1" | They cancel when content doesn't perform. Measure and iterate. Renewal rate is 80%+ when you show 15% engagement lift. |
| "I'm a creator, not an agency" | You are a business. $500/mo retainer from 5 clients = $30K/yr. That's a business. |
| "I'll do it for free to build the portfolio" | Never free. Offer a 50% first-month discount. Paid clients respect the work. Free clients ghost. |

## Verification

- [ ] Calendar covers 30 days minimum
- [ ] Each pillar appears at consistent cadence
- [ ] Platform-specific formats specified (Reel vs Carousel vs Story)
- [ ] Seasonal hooks tagged and dated
- [ ] CSV/Sheet exports cleanly with no missing cells
- [ ] Invoice attached and renewal date set
