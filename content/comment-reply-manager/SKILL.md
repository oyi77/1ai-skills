---
name: comment-reply-manager
description: Monitor TikTok/Instagram comments, classify sentiment, auto-reply with FAQ answers, and DM high-intent commenters
  with LYNK affiliate links to convert engagement into sales.
domain: content
tags:
- comment
- content-creation
- digital-content
- manager
- media
- reply
---

# comment-reply-manager
## When to Use

**Trigger phrases:**
- "comment reply manager"
- "Help me with comment reply manager"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


**Purpose:** Convert comment engagement into LYNK affiliate sales. Detect, analyze, and reply to comments on TikTok/Instagram posts. Auto-DM high-intent commenters with LYNK product links.

**Revenue Context:** 196 clicks → 0 sales. This skill creates the missing engagement funnel between viewer and buyer.

---

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/1ai-skills/content/comment-reply-manager/scripts

# Run tests first
python3 test_comment_manager.py

# Check PostBridge connection + post status
python3 comment_monitor.py

# Full cycle (dry run — safe to run anytime)
python3 run_manager.py --dry-run

# View pending DMs
python3 run_manager.py --mode dms

# Status report
python3 run_manager.py --mode report
```

---

## Architecture

```
comment-reply-manager/
├── SKILL.md                    ← You are here
├── scripts/
│   ├── run_manager.py          ← Main entry point
│   ├── comment_monitor.py      ← PostBridge API → posts with engagement
│   ├── sentiment_analyzer.py   ← Classify comment intent
│   ├── faq_responder.py        ← FAQ pattern → instant answer
│   ├── auto_replier.py         ← Orchestrate reply decisions
│   ├── dm_funnel.py            ← Auto-DM high-intent commenters
│   ├── comment_templates.py    ← Indonesian reply templates + product catalog
│   └── test_comment_manager.py ← Full test suite
├── references/
│   └── reply-strategies.md     ← Conversion strategy guide
├── logs/
│   ├── replies.jsonl           ← All reply decisions logged
│   ├── dm_sent.jsonl           ← DM send history
│   ├── dm_queue.jsonl          ← Pending DMs for manual execution
│   └── manual_queue.jsonl      ← Manual replies queue
└── cache/
    ├── posts_cache.json        ← PostBridge posts cache
    ├── replied_ids.json        ← Deduplication set
    └── dm_cooldowns.json       ← Per-user DM cooldowns
```

---

## Products Catalog

| Product | Price | LYNK URL |
|---------|-------|----------|
| JobMagnet Ai | IDR 75,000 | https://lynk.id/jendralbot/45r5yvze3vy4 |
| AI Creative Ad Engine | IDR 75,000 | https://lynk.id/jendralbot/9r8rj1o38q59 |
| Food Menu AI Studio | IDR 75,000 | https://lynk.id/jendralbot/l4q49jj3z383 |
| Studio Marketplace Pro | IDR 75,000 | https://lynk.id/jendralbot/emne05mm7v25 |
| AI Creative Tools | IDR 75,000 | https://lynk.id/jendralbot/89d30qd3ddnj |
| Guru Pintar AI | IDR 75,000 | https://lynk.id/jendralbot/6821op5e24kn |
| Mesin Cetak Bisnis Kuliner | IDR 75,000 | https://lynk.id/jendralbot/kzryk28dxmpx |
| Belanja Duit Balik | FREE | https://lynk.id/jendralbot/kkjk0mv1vg7o |
| Kelas Affiliate TikTok | IDR 1,000,000 | https://lynk.id/jendralbot/regxdn7xkpz6 |

---

## Conversation Flow

```
[Comment detected]
       ↓
[Sentiment analysis] → spam → SKIP
       ↓
[price_ask / interest] → Public reply "DM ya kak!" + Auto-DM with LYNK link
       ↓
[question] → FAQ check → product-matched answer + bio CTA
       ↓
[positive] → engagement reply + soft CTA
       ↓
[negative] → professional de-escalation
       ↓
[neutral] → generic engagement
```

---

## Reply Templates (Indonesian)

**Price question:** `"Cuma 75rb kak! Lagi promo 🔥 Link di bio ya"`

**Interest:** `"DM aku kak buat detail + promo spesial! 😊"`

**Question:** `"Hai kak, [product] bisa [benefit]. Cek link di bio ya, lagi promo! 🎁"`

**Positive:** `"Makasih kak! 🔥 Udah coba belum? Link di bio ya"`

**Negative:** `"Makasih feedbacknya kak, appreciate it 🙏"`

**DM message:**
```
Hai kak! Makasih udah tertarik sama [product] 😊

Ini linknya: [LYNK URL]

[product] bisa [benefit].

Harganya [price] aja — lagi ada promo spesial hari ini! 🎁
```

---

## API Configuration

- Configure comment, domain, manager, relevant, reply settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### PostBridge (for post discovery)
```bash
export POSTBRIDGE_KEY="REDACTED_ROTATED_CREDENTIAL"
```

Endpoints used:
- `GET /v1/posts` — list published posts
- `GET /v1/post-results` — platform IDs + comment counts
- `GET /v1/analytics` — engagement metrics

### Platform APIs

**TikTok:** Official v2 API doesn't support posting comments. Options:
1. **Manual execution** — Use dm_queue.jsonl as action list
2. **Browser automation** — Use Playwright/Selenium with TikTok web

**Instagram:** Graph API supports comment replies with Business account token.
```bash
export INSTAGRAM_ACCESS_TOKEN="your_token"
export INSTAGRAM_ACCOUNT_ID="your_account_id"
```

---

## Manual Workflow (When APIs Unavailable)

1. **Monitor posts** — Run `python3 comment_monitor.py` to get post URLs
2. **Visit posts** — Open TikTok/IG posts from the list
3. **Queue comments** — Copy comments to `cache/comment_queue.jsonl`:
   ```json
   {"id":"c1","platform":"tiktok","username":"user123","text":"Harganya berapa?","post_caption":"AI Tools","post_url":"https://tiktok.com/..."}
   ```
4. **Generate replies** — `python3 run_manager.py --dry-run`
5. **Review decisions** — Check `logs/replies.jsonl`
6. **Execute replies** — Use suggestions from `logs/manual_queue.jsonl`
7. **Send DMs** — Use suggestions from `logs/dm_queue.jsonl`

---

## Cron Setup (Every 30 mins)

```bash
*/30 * * * * cd ~/.openclaw/workspace/skills/1ai-skills/content/comment-reply-manager/scripts && python3 run_manager.py --dry-run >> /tmp/comment_manager.log 2>&1
```

---

## Revenue Tracking

```
Target conversion: 5% of engaged commenters
At 10 DMs/day: 0.5 sales/day × IDR 75,000 = IDR 37,500/day
At 50 DMs/day: 2.5 sales/day × IDR 75,000 = IDR 187,500/day
At 100 DMs/day: 5 sales/day = IDR 375,000/day
```

**Key metric:** DM → click → purchase rate. Track via LYNK dashboard.

---

## Troubleshooting

**PostBridge returns empty results:**
- Check API key is correct
- Sync analytics: `POST /v1/analytics/sync`
- Verify posts are published (not draft/scheduled)

**Tests fail on sentiment:**
- Check `sentiment_analyzer.py` keyword lists
- Indonesian slang varies — add new keywords as needed

**DMs not sending:**
- TikTok API doesn't support DMs → use manual queue
- Instagram requires Business API approval
- Check `logs/dm_queue.jsonl` for queued DMs to execute manually

---

*Production-ready. Revenue-critical. Execute immediately.* 🔥

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

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
