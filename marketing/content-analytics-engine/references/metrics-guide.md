# 📊 BerkahKarya Content Analytics Metrics Guide

## Overview

This guide defines all metrics used in the Content Analytics Engine, their benchmarks, and interpretation guidelines.

---

## Core Metrics

### Views (view_count)
- **Source:** PostBridge analytics API
- **Definition:** Total number of times a video was viewed
- **Minimum threshold:** 100 views = proof of concept
- **Target:** 10,000+ views for meaningful funnel data
- **Current:** 469 total (all-time)

### Engagement Rate (ER%)
- **Formula:** `(likes + comments + shares) / views × 100`
- **Industry benchmarks:**
  - TikTok: 5-9% is excellent, 1-3% is average
  - YouTube Shorts: 2-5% is good
  - Instagram Reels: 3-6% is good
  - Facebook: 0.5-1% is average
- **Current:** ~0.64% (3 likes from 469 views)
- **Verdict:** Below average — need better hooks

### Likes (like_count)
- **Weight:** Medium signal (easy engagement, passive)
- **Target:** ER from likes alone: 1%+ per platform
- **Current:** 3 total

### Comments (comment_count)
- **Weight:** High signal (active engagement, algo boost)
- **Target:** >0.1% comment rate
- **Current:** 0 total

### Shares (share_count)
- **Weight:** Highest signal (viral amplifier)
- **Target:** >0.05% share rate
- **Current:** 0 total

---

## Funnel Metrics

### Funnel Stages
```
[1] Video Views         ← PostBridge analytics
    ↓ (3% conversion estimate)
[2] Profile Visits      ← Estimated (no API)
    ↓ 
[3] Bio Link Clicks     ← Estimated (no API)
    ↓
[4] LYNK.ID Clicks      ← LYNK Dashboard (manual)
    ↓ (1-3% industry standard)
[5] Sales               ← LYNK Dashboard (manual)
```

### View-to-Click Rate
- **Formula:** `LYNK clicks / views × 100`
- **Current:** 196 / 469 = 41.8% (anomaly — LYNK clicks exceed views)
- **Note:** LYNK clicks came from non-PostBridge traffic (direct shares, other sources)
- **Healthy range:** 0.5-2%

### Click-to-Sale Rate (CVR)
- **Formula:** `sales / LYNK clicks × 100`
- **Industry benchmark:** 1-3% for digital products
- **Current:** 0 / 196 = 0% ← CRITICAL ISSUE
- **Interpretation:** Landing page is NOT converting

### View-to-Sale Rate
- **Formula:** `sales / views × 100`
- **Target:** 0.01-0.1% (1 sale per 1,000-10,000 views)
- **Current:** 0%

---

## Platform Benchmarks

### TikTok
- Algorithm: Heavily reward watch-time and shares
- Best ER: 5-9%
- Best duration: 15-30 seconds for hook content
- Best posting time: 18:00-22:00 WIB
- Our accounts: 7 accounts

### YouTube Shorts
- Algorithm: Click-through rate matters most
- Best ER: 2-5%
- Best duration: 30-60 seconds
- Best posting time: 12:00-14:00 WIB
- Note: Slower ramp-up than TikTok

### Instagram Reels
- Algorithm: Saves and shares are weighted heavily
- Best ER: 3-6%
- CRITICAL: Requires media (images/videos) — no text-only posts
- Our account: 1 account (berkahkaryadigitalproduct)

### Facebook
- Algorithm: Engagement in first hour is critical
- Best ER: 0.5-1% (lower expectations)
- Best for: Community building, not viral reach
- Our accounts: 4 accounts

---

## Content Type Definitions

| Type | Description | Indicators |
|------|-------------|------------|
| cashback | Cashback/savings angle | "uang kembali", "cashback", "MOVA" |
| tutorial | How-to content | "cara", "langkah", "tips" |
| story | Personal narrative | "cerita", "ternyata", "bun aku" |
| product_promo | Direct product promotion | "lynk.id", "beli sekarang" |
| brand | BerkahKarya brand content | "berkah karya", "content factory" |
| viral_hook | Viral/trending content | "#viral", "#fyp" |

---

## ROI Benchmarks

### Cost Structure (Est. IDR per post)
- AI Generation: IDR 500
- Operator time (2 min @ IDR 50K/hr): IDR 1,667
- Platform fee: IDR 0 (PostBridge free)
- **Total per post: ~IDR 2,167**

### Revenue Model (JENDRALBOT Affiliate)
- Product price range: IDR 0 (MOVA free) to IDR 89,000
- Average paid product: IDR 49,000-59,000
- Platform fee (LYNK): ~5%
- Net per sale: ~IDR 46,550-56,050

### Break-Even
- At IDR 49,000/sale with 5% LYNK fee:
- Net per sale: IDR 46,550
- With 100 posts (IDR 216,700 cost):
  - Break-even: ~5 sales
- With 1,000 posts (IDR 2,167,000 cost):
  - Break-even: ~47 sales

---

## A/B Test Framework

### Statistical Significance
- Minimum sample per variant: 30 posts
- Confidence level required: 80%+
- Test duration: Minimum 7 days
- Current data: 4 analytics records (insufficient for statistical tests)

### Hook Types Being Tested
1. **personal_story** — "Bun, aku baru tau..."
2. **emoji_hook** — Leading with 🚀✨🔥
3. **value_hook** — Leading with "Cara.../Tips..."
4. **curiosity_hook** — "Kenapa/Mengapa..."
5. **behind_scenes** — "Inside/How we..."

### Winning Hook (Early Data)
Based on available data:
- personal_story posts: 142 views avg (best)
- Emoji hooks: 0 views avg (worst — likely non-video posts)

---

## Diagnostic Thresholds

| Metric | Green | Yellow | Red |
|--------|-------|--------|-----|
| Total Views (7d) | 10,000+ | 1,000-9,999 | <1,000 |
| Engagement Rate | 3%+ | 0.5-3% | <0.5% |
| Click-to-Sale | 2%+ | 0.5-2% | <0.5% |
| Post Success Rate | 90%+ | 70-90% | <70% |
| Weekly Growth | +10%+ | -10% to +10% | <-10% |

---

## Reporting Schedule

| Report | Frequency | Generated By |
|--------|-----------|--------------|
| Daily Performance | Every day 07:00 WIB | `report_generator.py --cache` |
| Platform Comparison | Daily | Included in daily report |
| Content Type Analysis | Daily | Included in daily report |
| Funnel Report | Daily | Included in daily report |
| Trend Analysis | Weekly (Monday) | `report_generator.py --weekly` |
| A/B Test Results | Weekly | `ab_test_tracker.py` |
| ROI Report | Weekly | `roi_calculator.py` |

---

## Data Freshness

PostBridge analytics sync schedule:
- TikTok: Every few hours (API dependent)
- YouTube: Daily
- Instagram: Daily (requires manual trigger)
- Facebook: Not tracked in analytics endpoint

To trigger fresh sync:
```bash
python3 scripts/analytics_collector.py --sync
```

---

*Last updated: 2026-03-13*
*Maintained by: BerkahKarya Content Analytics Engine*
