---
name: content-planner-auto
description: content-planner-auto. Use when relevant to this domain.
---

# content-planner-auto

**Auto-generate 30-day content calendars for BerkahKarya. Revenue survival tool.**

## What This Does

Generates fully-planned content calendars with:
- Pillar rotation (AI Demo 40%, Tips 25%, Social Proof 15%, BTS 10%, Promo 10%)
- Platform-optimized timing (TikTok, Instagram, YouTube Shorts, Facebook)
- Account rotation across 7 TikTok + 4 Facebook + 1 Instagram accounts
- Seasonal adjustments (Ramadan, Harbolnas, 11.11, Lebaran)
- PostBridge batch scheduling
- Media inventory tracking

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/1ai-skills/content/content-planner-auto/scripts

# Generate 7-day calendar (default)
python3 calendar_generator.py --start 2026-03-14 --days 7 --print

# Generate 30-day calendar
python3 calendar_generator.py --start 2026-03-14 --days 30 --output ~/calendars/march_2026.json

# Schedule to PostBridge (dry run first)
python3 batch_scheduler.py ~/calendars/march_2026.json --dry-run

# Schedule for real
python3 batch_scheduler.py ~/calendars/march_2026.json

# Check media inventory gaps
python3 content_inventory.py ~/calendars/march_2026.json --shoot-list /tmp/shoot_list.md

# Run all tests
python3 test_planner.py
```

## Files

```
content-planner-auto/
├── SKILL.md                  ← You are here
├── scripts/
│   ├── calendar_generator.py # Main orchestrator - generates full calendar
│   ├── pillar_rotator.py     # Content pillar rotation + product selection
│   ├── platform_optimizer.py # Timing, formats, account rotation
│   ├── seasonal_calendar.py  # Ramadan, Harbolnas, Indonesian events
│   ├── batch_scheduler.py    # PostBridge API batch scheduler
│   ├── content_inventory.py  # Media asset tracking + shoot list
│   └── test_planner.py       # Full test suite + POC calendar generator
└── references/
    └── calendar-templates.md # Hook templates, caption formats, platform rules
```

## Output Format

Each calendar day follows this structure:

```json
{
  "date": "2026-03-14",
  "day_name": "Saturday",
  "seasonal_event": "ramadan",
  "total_posts": 8,
  "posts": [
    {
      "time": "07:00",
      "platform": "instagram",
      "account_id": 48186,
      "account_name": "@berkahkaryadigitalproduct",
      "pillar": "ai_tools_demo",
      "product": "JobMagnet Ai",
      "content_type": "reel",
      "hook": "Kamu masih apply kerja manual? 😱",
      "caption": "...",
      "hashtags": ["#aitools", "#jobhunting", "#fyp"],
      "media_needed": "product_demo_video",
      "lynk_url": "https://lynk.id/jendralbot/45r5yvze3vy4",
      "seasonal_event": "ramadan"
    }
  ]
}
```

## Content Pillars

| Pillar | Weight | Description |
|--------|--------|-------------|
| `ai_tools_demo` | 40% | Show products in action, tutorials |
| `tips_tricks` | 25% | Quick actionable tips |
| `social_proof` | 15% | Testimonials, results |
| `behind_the_scenes` | 10% | Build in public |
| `promo_cta` | 10% | Direct promotion |

## Platform Rules

| Platform | Best Times (WIB) | Max/Day | Format |
|----------|-----------------|---------|--------|
| TikTok | 11:00-13:00 & 19:00-21:00 | 3 | 9:16 video |
| Instagram | 07:00-09:00 & 17:00-19:00 | 3 | reel/carousel/story |
| YouTube Shorts | 14:00-17:00 | 2 | 9:16 video |
| Facebook | 09:00-11:00 | 2 | any format |

## Connected Accounts

- **TikTok**: 7 accounts (content rotated across all)
- **Instagram**: 1 account (@berkahkaryadigitalproduct)
- **Facebook**: 4 pages (rotated)
- **YouTube**: 1 channel

## PostBridge API

- Base: `https://api.post-bridge.com/v1`
- Key: `REDACTED_ROTATED_CREDENTIAL`
- Auth: `Bearer {key}` header

Key endpoints:
- `GET /v1/social-accounts` — Get account IDs
- `POST /v1/posts` — Schedule a post
- `POST /v1/media/create-upload-url` — Upload media

## Seasonal Events (2026)

| Event | Dates | Strategy |
|-------|-------|----------|
| Ramadan | Feb 17 - Mar 17 | Post-iftar timing, productivity theme |
| Lebaran | Mar 18-27 | THR investment angle |
| 11.11 | Nov 8-12 | Flash sale, midnight posts |
| 12.12 (Harbolnas) | Dec 10-13 | Year-end clearance |
| HUT RI ke-80 | Aug 15-19 | Patriotic AI theme |

## Agent Instructions

When asked to generate a content calendar:

1. Run `python3 calendar_generator.py --start YYYY-MM-DD --days N --output /tmp/calendar.json --print`
2. Review output for seasonal events
3. Check media inventory: `python3 content_inventory.py /tmp/calendar.json`
4. Dry run scheduler: `python3 batch_scheduler.py /tmp/calendar.json --dry-run`
5. If all looks good, schedule for real: `python3 batch_scheduler.py /tmp/calendar.json`

When asked to check media assets:
- Run `python3 content_inventory.py /tmp/calendar.json --shoot-list /tmp/shoot_list.md`
- Share the shoot list with the production team

When asked to schedule to PostBridge:
- ALWAYS dry run first
- Only schedule with actual media files if TikTok/YouTube posts
- Facebook/text posts can be scheduled without media

## Products Reference

| Product | Price | LYNK URL |
|---------|-------|----------|
| JobMagnet Ai | IDR 49K | https://lynk.id/jendralbot/45r5yvze3vy4 |
| ContentAI Pro | IDR 79K | https://lynk.id/jendralbot/contentai |
| TradingBot Ai | IDR 89K | https://lynk.id/jendralbot/tradingbot |
| CopywriterAi | IDR 59K | https://lynk.id/jendralbot/copywriter |
| Free AI Toolkit | FREE | https://lynk.id/jendralbot/freetoolkit |

## Dependencies

- Python 3.8+
- `requests` library (for PostBridge API)

Install:
```bash
pip install requests
```

No other external dependencies. All scheduling logic is pure Python.

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- Check readability score (target grade 8 or below for general audiences)
- Verify all images have alt text and proper dimensions per platform
- Confirm links work and point to correct destinations
- Test video/audio quality before publishing
- Validate content renders correctly on mobile devices
