---
name: influencer-scouting
version: 1.0.0
description: "|\n  >\n    Full influencer scouting, outreach, and performance tracking\
  \ system for BerkahKarya.\n    Covers platform search across TikTok, Instagram,\
  \ and YouTube for Indonesian creators,\n    scoring/qualification, DM outreach,\
  \ negotiation, deal tracking, and ROI measurement.\n    Integrates with Kalodata\
  \ for TikTok analytics.\n"
author: Vilona / BerkahKarya
language: id-ID / en
tags:
- influencer
- marketing
- tiktok
- instagram
- youtube
- kol
- affiliate
- indonesia
scripts: "|\n  - scripts/ig_scout.py\n    - scripts/tiktok_scout.py\n"
domain: sales
---



# Influencer Scouting Skill 🔍

Find, qualify, and close Indonesian creators for BerkahKarya campaigns.

---

## 1. Target Creator Profile (ICP)

- Configure across, analytics, berkahkarya, covers, creators settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Sweet Spot Parameters

| Metric | Minimum | Ideal | Maximum |
|--------|---------|-------|---------|
| Followers | 10,000 | 50K–200K | 500,000 |
| Engagement Rate | 3% | 5–8% | — |
| Content quality | Good | Very good | — |
| Fake follower % | — | <10% | 20% |
| Account age | 6 months | 1–3 years | — |
| Post frequency | 3x/week | Daily | — |

### Why 10K–500K (Micro/Mid-tier)?
- **Cheaper:** IDR 200K–5M per post vs IDR 10M+ for mega
- **Higher ER:** Micro = 5–8% vs mega = 1–3%
- **More authentic:** Followers trust them more
- **Open to barter:** New income stream for them
- **Easier to manage:** Responsive, professional

### Niches for BerkahKarya

| Niche | Priority | Why |
|-------|----------|-----|
| Digital products / online business | 🔥 HIGH | Direct product match |
| Business / entrepreneurship | 🔥 HIGH | Audience = buyers |
| Finance / investasi | 🔥 HIGH | High-value audience |
| Lifestyle / produktivitas | MEDIUM | Wide reach |
| Tech / AI / gadget | MEDIUM | Progressive audience |
| Self-improvement / motivasi | MEDIUM | Receptive audience |
| F&B / kuliner | LOW | Product mismatch |
| Beauty / fashion | LOW | Wrong demographic |

---

## 2. Platform Search Strategy

- Configure across, analytics, berkahkarya, covers, creators settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### 2A. TikTok Scouting

**Manual search:**
```
Hashtags to monitor:
#digitalproduct #jualdigital #passiveincome
#bisnisonline #jualan #entrepreneur
#investasi #finansial #money
#produktivitas #workfromhome
#kontenindonesia #contentcreator
```

**Kalodata Integration:**
```bash
# Use existing Kalodata skill for TikTok analytics
# Key metrics to extract:
- Creator GMV (Gross Merchandise Value)
- Product categories they promote
- Average video views / engagement
- Commission rates they accept
- Live streaming frequency

# Kalodata workflow
1. Search creator by niche keyword
2. Filter by follower range (10K-500K)
3. Sort by GMV or ER
4. Export creator list
5. Feed into scripts/tiktok_scout.py for scoring
```

**TikTok Creator Marketplace:**
- URL: creators.tiktok.com
- Filter: Indonesia, niche, follower range
- Export contacts directly

### 2B. Instagram Scouting

**Hashtag research:**
```
Primary hashtags (high intent):
#digitalproductindonesia #jualproduklist
#affiliateindonesia #kelasdigital

Secondary hashtags:
#pengusahamuda #bisnisonline
#financialfreedom #investasicerdas
#contentcreatorindonesia
```

**Public API approach (via ig_scout.py):**
```python
# scripts/ig_scout.py uses public data only
# No login required for basic profile data
# Data available: bio, follower count, post count, recent posts

python3 scripts/ig_scout.py --search \
  --hashtag "digitalproductindonesia" \
  --min-followers 10000 \
  --max-followers 500000 \
  --output creators_ig.json
```

### 2C. YouTube Scouting

**Search queries:**
```
"cara jualan digital product" site:youtube.com
"review produk digital indonesia"
"passive income online indonesia 2025"
"bisnis digital pemula"
"investasi saham pemula indonesia"
```

**YouTube Data API metrics:**
- Subscriber count
- Average views per video (last 10 videos)
- View-to-subscriber ratio (engagement proxy)
- Upload frequency
- Comment engagement

---

## 3. Scoring System

- Configure across, analytics, berkahkarya, covers, creators settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Creator Score Formula

```python
# Total score: 0–100

score = (
    follower_score       * 0.20 +  # Range fit
    engagement_score     * 0.30 +  # ER quality
    niche_match_score    * 0.25 +  # Content alignment
    content_quality      * 0.15 +  # Visual/copy quality
    authenticity_score   * 0.10    # Fake follower check
)

# Follower scoring (20 pts)
if 50_000 <= followers <= 200_000: score = 20  # Ideal
elif 20_000 <= followers < 50_000: score = 15
elif 10_000 <= followers < 20_000: score = 10
elif 200_000 < followers <= 500_000: score = 10
else: score = 0  # Out of range

# Engagement Rate scoring (30 pts)
if er >= 0.08: score = 30  # Excellent
elif er >= 0.05: score = 25  # Good
elif er >= 0.03: score = 15  # Acceptable minimum
else: score = 0  # Disqualify

# Niche match (25 pts) — manual assessment
# Digital products/business: 25
# Finance/tech: 20
# Lifestyle/self-improvement: 15
# General: 5

# Score thresholds
# 70–100: TIER A — Priority partnership
# 50–69:  TIER B — Good candidate
# 30–49:  TIER C — Low priority / monitor
# 0–29:   REJECT — Don't pursue
```

### Fake Follower Check

```python
# Red flags (auto-score penalty):
RED_FLAGS = {
    "sudden_spike": "1M+ followers gained in <30 days",
    "low_er": "ER < 0.5% with 100K+ followers",
    "bot_comments": "Comments like 'Nice!', '🔥🔥🔥' dominate",
    "ghost_followers": "Following >> Followers ratio",
    "no_story_views": "100K followers but 200 story views"
}

# Tools to use:
# - HypeAuditor (paid): hypeauditor.com
# - Social Blade (free): socialblade.com
# - IGaudit (free): igaudit.io
# - Modash Fake Follower Check
```

---

## 4. Outreach DM Templates (Bahasa Indonesia, Casual)

Reusable templates for influencer-scouting.

Standard config:
```yaml
name: influencer-scouting_standard
mode: production
output: results/
format: json
```

Test config:
```yaml
name: influencer-scouting_test
mode: development
dry_run: true
verbose: true
```


### Template 1: Standard influencer-scouting
```yaml
name: influencer-scouting_standard
mode: production
output: results/
format: json
```

### Template 2: Quick Test
```yaml
name: influencer-scouting_test
mode: development
dry_run: true
verbose: true
```


### 4A. TikTok DM

**Template 1 — Collab offer:**
```
Haii [Nama] 👋

Gue [Nama] dari BerkahKarya. Udah lama sering liat konten 
lo tentang [topik] — genuinely bagus dan relatable banget!

Kita lagi cari kreator yang aligned buat collab produk digital.
Ada yang cocok banget sama audience lo.

Mau gue share detailnya? No pressure, santai aja 😊
```

**Template 2 — Direct value:**
```
Hey [Nama]! 

Konten lo di [topik tertentu] kena banget. Gue dari BerkahKarya.

Kita punya produk digital yang literally cocok banget sama 
niche lo — bisa jadi income stream baru yang passive.

Tertarik collab? Bisa barter atau ada rate juga kok 🙌
```

### 4B. Instagram DM

**Template 1 — Compliment + offer:**
```
Haiiii [Nama]! ✨

Baru scroll feed lo dan konten [topik spesifik] lo itu 
kena banget! Gue suka cara lo explain yang complex jadi simple.

Gue [Nama] dari BerkahKarya — kita produce digital products 
untuk [niche]. Pengen banget collab sama lo untuk campaign 
yang gue rasa cocok sama konten lo.

Ada waktu untuk ngobrol singkat? 🙏
```

**Template 2 — After engaging content:**
```
[Nama]! Baru liat video lo yang [judul/topik].

Relate banget sama audience gue. Kebetulan kita lagi ada 
campaign yang super aligned sama ini.

Boleh DM balik untuk share detail kolaborasinya? 💌
```

### 4C. WhatsApp (setelah dapat nomor)

```
Halo [Nama], ini [Nama Lo] dari BerkahKarya.

Udah DM di [platform] tapi mau mastiin pesan gue nyampe 😅

Singkatnya: kita mau collab sama lo untuk promosiin produk 
digital kami yang relevan sama audience lo.

Bisa barter konten atau ada bayaran juga — tergantung mau 
lonya kayak gimana.

Lagi available untuk ngobrol sebentar? 🙏
```

---

## 5. Negotiation Framework

- Configure across, analytics, berkahkarya, covers, creators settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### 5A. Rate Card Benchmarks Indonesia 2025

| Tier | Platform | Followers | Rate per Post |
|------|----------|-----------|---------------|
| Nano | TikTok/IG | 1K–10K | IDR 100K–500K |
| Micro | TikTok/IG | 10K–50K | IDR 500K–2M |
| Mid-tier | TikTok/IG | 50K–200K | IDR 2M–8M |
| Macro | TikTok/IG | 200K–500K | IDR 8M–20M |
| Mega | TikTok/IG | 500K+ | IDR 20M+ |
| YouTube | YouTube | 50K–200K | IDR 3M–15M |
| YouTube | YouTube | 200K+ | IDR 15M–50M |

**Note:** Rates vary by niche. Finance/business = 30–50% premium.

### 5B. Barter vs Paid Decision Matrix

| Situation | Recommendation |
|-----------|---------------|
| Creator < 50K followers | Barter first (product access) |
| Creator 50K–200K | Negotiate: barter + small fee OR affiliate commission |
| Creator 200K+ | Paid (market rate or slight discount) |
| Creator loves product natively | Affiliate commission only (sustainable) |
| High authority niche (finance/bisnis) | Always paid — credibility matters |

### 5C. Barter Package Structure

```
Basic Barter (for nano/micro):
- Free access to [product] (nilai IDR 297K–597K)
- Content: 1 TikTok/Reels + 1 Story
- Rights: Reshare allowed by BerkahKarya

Enhanced Barter (for mid-tier):
- Free product + affiliate link (15% commission)
- Content: 2 TikTok/Reels + 3 Stories + 1 highlight
- Rights: Full reshare rights 30 days

Affiliate-only (ongoing):
- No upfront fee
- Commission: 15–20% per sale via unique link
- Tracking: LYNK affiliate dashboard
- Payment: Monthly, minimum IDR 100K
```

### 5D. Negotiation Script

```
Jika kreator minta rate tinggi:

"Harga lo masuk akal untuk ukuran audience lo. 
Kita mau coba dulu dengan struktur hybrid:
- [Bayar IDR X] + affiliate commission 15% per sale
Jadi lo bisa dapat lebih kalau konten lo convert.

Gimana?"

Jika kreator hanya mau barter:

"Oke deal! Barter product senilai IDR [X] ya.
Kita butuh: 1 TikTok/Reels (min 30 detik) + 2 Stories.
Boleh gue tau brief deliverable-nya dipake kapan?"
```

---

## 6. Performance Tracking

- Configure across, analytics, berkahkarya, covers, creators settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Campaign Metrics per Creator

```json
{
  "creator_id": "IG_@username",
  "campaign": "JENDRALBOT Q1 2026",
  "posts": [
    {
      "post_id": "post_001",
      "platform": "instagram",
      "type": "reels",
      "posted_date": "2026-03-10",
      "views": 25000,
      "likes": 1800,
      "comments": 120,
      "shares": 450,
      "saves": 890,
      "er": 0.0728,
      "link_clicks": 340,
      "conversions": 12,
      "revenue_generated": 3588000
    }
  ],
  "deal_type": "barter",
  "barter_value": 297000,
  "total_conversions": 12,
  "total_revenue": 3588000,
  "roi": 1107.07,
  "status": "completed"
}
```

### ROI Calculation

```python
# ROI formula
roi = ((revenue_generated - campaign_cost) / campaign_cost) * 100

# For barter:
campaign_cost = product_cogs  # Cost of goods/digital product

# For paid:
campaign_cost = creator_fee + product_cogs

# Target ROI:
# Barter campaigns: >500% (product COGS is low)
# Paid campaigns: >200%
# Affiliate only: Infinite ROI (no upfront cost)
```

### Weekly Performance Report

```
📊 INFLUENCER PERFORMANCE — WEEK [W]

Active Campaigns: [N]
Total Posts Published: [N]
Total Reach: [N]
Total Clicks to LYNK: [N]
Total Conversions: [N]
Total Revenue: IDR [X]

Top Performer:
  @[username] — [N] konversi / IDR [X] revenue
  ROI: [X]%

Bottom Performer:
  @[username] — [N] konversi / IDR [X] revenue
  Action: [review/cancel/renegotiate]

Pipeline:
  Outreach sent: [N]
  Waiting response: [N]
  In negotiation: [N]
  Deal confirmed: [N]
```

---

## 7. Blacklist Criteria

- Configure across, analytics, berkahkarya, covers, creators settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Auto-Blacklist (immediate DQ)

```python
BLACKLIST_CRITERIA = {
    "bought_followers": {
        "signal": "Sudden 50K+ follower spike in <7 days",
        "check": "Social Blade history graph",
        "action": "Immediate reject"
    },
    "fake_engagement": {
        "signal": "ER < 0.5% with 50K+ followers",
        "check": "Manual post inspection",
        "action": "Immediate reject"
    },
    "competitor_contract": {
        "signal": "Active promotion of competitor product",
        "check": "Last 30 days posts",
        "action": "Hold — check exclusivity clause"
    },
    "negative_reputation": {
        "signal": "News of scam, sexual harassment, racism",
        "check": "Google search [name] + controversy",
        "action": "Immediate reject + document"
    },
    "previous_no_show": {
        "signal": "Agreed to collab but never posted",
        "check": "Internal deal history",
        "action": "Immediate reject + add to blacklist DB"
    },
    "hate_speech": {
        "signal": "Divisive political/religious content",
        "check": "Post history scan",
        "action": "Immediate reject"
    }
}
```

### Soft Blacklist (monitor, low priority)

- Content quality consistently declining
- ER dropped >50% in last 60 days
- Long inactive periods (>2 months no post)
- Audience demographics shifted away from ICP

---

## 8. Database Schema

- Configure across, analytics, berkahkarya, covers, creators settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Creator Profile

```sql
-- Table: creators
CREATE TABLE creators (
  id              TEXT PRIMARY KEY,    -- platform_username
  platform        TEXT NOT NULL,       -- tiktok | instagram | youtube
  username        TEXT NOT NULL,
  display_name    TEXT,
  bio             TEXT,
  profile_url     TEXT,
  followers       INTEGER,
  following       INTEGER,
  total_posts     INTEGER,
  avg_er          REAL,                -- Average engagement rate
  niche           TEXT,                -- primary niche
  location        TEXT,                -- city/province
  contact_wa      TEXT,
  contact_email   TEXT,
  contact_tg      TEXT,
  icp_score       REAL,               -- 0-100 score
  tier            TEXT,               -- A | B | C | REJECT | BLACKLIST
  fake_follower_pct REAL,             -- estimated % fake
  kalodata_gmv    REAL,               -- TikTok GMV if available
  created_at      TEXT,
  last_updated    TEXT,
  notes           TEXT
);

-- Table: outreach
CREATE TABLE outreach (
  id              TEXT PRIMARY KEY,
  creator_id      TEXT REFERENCES creators(id),
  channel         TEXT,               -- dm_tiktok | dm_ig | wa | telegram
  message_template TEXT,
  sent_at         TEXT,
  response_at     TEXT,
  response_text   TEXT,
  status          TEXT,               -- sent | replied | negotiating | agreed | rejected
  follow_up_count INTEGER DEFAULT 0,
  next_followup   TEXT
);

-- Table: deals
CREATE TABLE deals (
  id              TEXT PRIMARY KEY,
  creator_id      TEXT REFERENCES creators(id),
  campaign_name   TEXT,
  deal_type       TEXT,               -- barter | paid | affiliate
  deal_value      REAL,               -- IDR
  barter_product  TEXT,
  commission_pct  REAL,
  deliverables    TEXT,               -- JSON array
  deadline        TEXT,
  status          TEXT,               -- negotiating | agreed | briefed | posted | completed | cancelled
  contract_signed INTEGER DEFAULT 0,
  created_at      TEXT,
  closed_at       TEXT
);

-- Table: posts
CREATE TABLE posts (
  id              TEXT PRIMARY KEY,
  deal_id         TEXT REFERENCES deals(id),
  creator_id      TEXT REFERENCES creators(id),
  platform        TEXT,
  post_url        TEXT,
  post_type       TEXT,               -- video | reels | story | short
  posted_at       TEXT,
  views           INTEGER,
  likes           INTEGER,
  comments        INTEGER,
  shares          INTEGER,
  saves           INTEGER,
  link_clicks     INTEGER,
  conversions     INTEGER,
  revenue         REAL,
  er              REAL,
  last_synced     TEXT
);
```

---

## 9. Scripts Reference

- Configure across, analytics, berkahkarya, covers, creators settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### 9A. `scripts/ig_scout.py`

```python
# Usage
python3 scripts/ig_scout.py [OPTIONS]

Options:
  --search          Search creators by hashtag/keyword
  --hashtag TEXT    Hashtag to search (without #)
  --min-followers N Minimum follower count [default: 10000]
  --max-followers N Maximum follower count [default: 500000]
  --score           Score discovered creators against ICP
  --output FILE     Save results to JSON file
  --fake-check      Run fake follower estimation
  --update-db       Sync results to creator database

# Example
python3 scripts/ig_scout.py \
  --search \
  --hashtag "digitalproductindonesia" \
  --min-followers 10000 \
  --max-followers 200000 \
  --score \
  --fake-check \
  --output results/ig_creators_$(date +%Y%m%d).json

# Note: Uses public Instagram data (no login required)
# Rate limit: ~200 profiles/hour without token
# With Basic Display API token: higher limits
```

### 9B. `scripts/tiktok_scout.py`

```python
# Usage
python3 scripts/tiktok_scout.py [OPTIONS]

Options:
  --search          Search by hashtag or keyword
  --hashtag TEXT    Hashtag to search
  --kalodata        Pull from Kalodata API (requires kalodata skill)
  --min-followers N Minimum followers [default: 10000]
  --score           Auto-score creators
  --gmv-filter      Only show creators with GMV data
  --output FILE     Output JSON file

# Example — Kalodata integration
python3 scripts/tiktok_scout.py \
  --kalodata \
  --hashtag "digitalproduct" \
  --min-followers 10000 \
  --gmv-filter \
  --score \
  --output results/tiktok_creators_$(date +%Y%m%d).json

# Kalodata provides:
# - Creator GMV history
# - Product categories promoted
# - Shop conversion rates
# - Commission acceptance rates
```

---

## 10. Tools & Integrations

- Configure across, analytics, berkahkarya, covers, creators settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Kalodata (TikTok Analytics)
```bash
# Already installed — see kalodata skill
# Use for: TikTok creator GMV, shop analytics, trending products
# Key command: kalodata creator search --niche "digital product" --country ID
```

### Social Blade (Free tier)
```
URL: socialblade.com
Use for: Follower history graph (detect artificial spikes)
Manual check: search creator → view Monthly Follower Change chart
Red flag: Any month with >50K sudden gain
```

### HypeAuditor (if budget available)
```
URL: hypeauditor.com
Use for: Fake follower %, audience demographics
Pricing: ~$149/month for 100 audits
Recommended: Spend on Tier A candidates only before paying
```

---

## 11. Quick Reference

```
SCOUTING SHORTCUTS:
  Find IG creators:   python3 scripts/ig_scout.py --search --hashtag "bisnisonline"
  Find TikTok:        python3 scripts/tiktok_scout.py --kalodata --hashtag "digitalproduct"
  Score creator:      python3 scripts/ig_scout.py --score --username @creator
  View database:      sqlite3 influencers.db "SELECT * FROM creators WHERE tier='A'"

SCORING TIERS:
  A (70-100): Priority outreach this week
  B (50-69):  Outreach when bandwidth available
  C (30-49):  Monitor, no active outreach
  REJECT:     DQ'd, archived
  BLACKLIST:  Never contact again

RATE BENCHMARKS (2025):
  Micro  (10K-50K):   IDR 500K – 2M/post
  Mid    (50K-200K):  IDR 2M – 8M/post
  Macro  (200K-500K): IDR 8M – 20M/post
  Default approach:   Barter first, paid second

DEAL TYPES:
  Barter:     Product for content (best ROI)
  Paid:       Cash fee (larger creators)
  Affiliate:  Commission only (scalable, zero upfront)
  Hybrid:     Small fee + affiliate (sweet spot)
```

---

*Skill version 1.0 — BerkahKarya Influencer Engine 🔍*
*Last updated: 2026-03-13*

## How to Use

1. Define ideal customer profile (ICP) and buyer personas
2. Build lead list from qualified sources
3. Craft personalized outreach sequences
4. Track engagement and follow up on signals
5. Qualify leads through discovery calls
6. Present solution tailored to pain points
7. Handle objections with value reframing
8. Close and hand off to onboarding

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- **Lead response time > 5 minutes**: Conversion drops 80% after 5 min. Automate instant response.
- **Pipeline has stale deals**: Deals stuck 30+ days need re-qualification or disqualification.
- **Low email reply rates (<3%)**: Messaging is too generic. Personalize with research.
- **High churn in first 90 days**: Onboarding gap. Fix handoff from sales to success.
- **Discounting above 20%**: Value perception problem. Reframe ROI, don't cut price.

## Verification

- Test email sequences with seed accounts before full send
- Verify CRM data integrity (no duplicates, correct stages)
- Check lead scoring model against actual conversion data
- Confirm proposal/contract templates are current and branded
- Validate payment links and checkout flow end-to-end
