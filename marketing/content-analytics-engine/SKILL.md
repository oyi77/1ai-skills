---
name: content-analytics-engine
description: Collect content performance data from PostBridge API and generate daily/weekly reports tracking the full revenue
  funnel — views, engagement, clicks, and sales.
domain: marketing
tags:
- analytics
- api
- content
- engine
- growth
- marketing
- seo
---

# Content Analytics Engine
## When to Use

**Trigger phrases:**
- "content analytics engine"
- "Help me with content analytics engine"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


**Category:** Marketing Analytics | Revenue Intelligence  
**Status:** Production-Ready  
**Version:** 1.0.0  
**Location:** `skills/1ai-skills/marketing/content-analytics-engine/`

---

## Purpose

Collect, analyze, and report on content performance from PostBridge API.
Tracks the full revenue funnel: Views → Engagement → LYNK Clicks → Sales.
Generates daily/weekly markdown reports and JSON output for other skills.

**Revenue Context:** BerkahKarya JENDRALBOT affiliate campaign. 469 views, 0 sales. This tool exists to fix that.

---

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/1ai-skills/marketing/content-analytics-engine/scripts

# Generate full report NOW
python3 report_generator.py

# Generate with fresh data sync
python3 report_generator.py --sync

# Use cached data (faster)
python3 report_generator.py --cache

# Run tests
python3 test_analytics.py
```

---

## Scripts

- Configure analytics, content, domain, engine, relevant settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### `analytics_collector.py`
Fetches all data from PostBridge API with pagination support.

```python
from analytics_collector import collect_all, build_lookup_maps

# Collect everything
dataset = collect_all(use_cache=False, force_sync=True)
# dataset = {analytics, posts, post_results, social_accounts, collected_at}

# Build cross-reference maps
maps = build_lookup_maps(dataset)
```

**Endpoints used:**
- `GET /v1/analytics?limit=100` — View/like/comment/share counts
- `GET /v1/posts?limit=100` — Post captions, status, social accounts
- `GET /v1/post-results?limit=100` — Success/failure per account
- `GET /v1/social-accounts` — Connected platform accounts
- `POST /v1/analytics/sync?platform=tiktok|youtube|instagram` — Trigger refresh

---

### `performance_analyzer.py`
Analyzes best/worst posts, platform rankings, content types.

```python
from performance_analyzer import full_analysis, platform_summary

analysis = full_analysis(dataset)
# Returns: summary, platform_breakdown, content_types, top_posts, error_analysis

platforms = platform_summary(analytics_list)
# Returns: {platform: {views, likes, avg_views_per_post, avg_engagement_rate}}
```

---

### `trend_detector.py`
Detects engagement trends over time, best posting hours/days.

```python
from trend_detector import weekly_trend_report, best_posting_times

trend = weekly_trend_report(analytics_list)
# Returns: daily_breakdown, growth_analysis, platform_trends, timing

timing = best_posting_times(analytics_list)
# Returns: best_hours, best_days, hourly_breakdown
```

---

### `funnel_analyzer.py`
Views → LYNK Clicks → Sales drop-off analysis.

```python
from funnel_analyzer import compute_funnel

funnel = compute_funnel(analytics_list, lynk_clicks=196, lynk_sales=0)
# Returns: funnel_stages, conversion_rates, bottleneck, recommendation
```

**Important:** LYNK click data must be manually updated in the script (PostBridge doesn't track LYNK).

---

### `roi_calculator.py`
Cost per content vs revenue generated.

```python
from roi_calculator import compute_roi, platform_roi_breakdown

roi = compute_roi(analytics, posts, lynk_sales=0, lynk_clicks=196)
# Returns: status, investment, revenue, profitability, unit_economics, break_even
```

---

### `optimization_engine.py`
Recommendations: what to post more/less of.

```python
from optimization_engine import full_optimization_report

report = full_optimization_report(dataset)
# Returns: platform_rankings, content_type_rankings, recommendations, action_plan
```

---

### `ab_test_tracker.py`
Auto-detects A/B test patterns from existing data.

```python
from ab_test_tracker import run_all_auto_tests

tests = run_all_auto_tests(analytics_list)
# Returns: hook_test, platform_test, length_test (all with winners)
```

---

### `report_generator.py`
Master report builder. Calls all other modules.

```python
from report_generator import generate_all_reports

paths = generate_all_reports(dataset, date="2026-03-13")
# Returns: {daily_md, weekly_md, json}
# Saves to: ~/.openclaw/workspace/reports/YYYY-MM-DD-analytics-*.md
```

---

## Output Files

```
~/.openclaw/workspace/reports/
├── YYYY-MM-DD-analytics-daily.md      # Human-readable daily report
├── YYYY-MM-DD-analytics-weekly.md     # Weekly summary
├── YYYY-MM-DD-analytics-full.json     # Machine-readable full data
├── ab_tests.json                       # Persistent A/B test records
└── cache/
    └── YYYY-MM-DD-raw.json            # Raw API response cache
```

---

## Reports Generated

- Configure analytics, content, domain, engine, relevant settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### 1. Daily Performance Report
Contains:
- Executive summary (views, engagement, LYNK clicks, sales vs targets)
- Platform breakdown table
- Top 5 / Worst 5 posts
- Funnel analysis with drop-off rates
- Trend analysis + best posting times
- Error analysis (failed posts)
- ⚡ Prioritized action items (CRITICAL/HIGH/MEDIUM)

### 2. Weekly Trend Report
Contains:
- Week-over-week growth rate
- Platform trend comparison
- ROI status and break-even analysis

### 3. Full JSON Output
Machine-readable data for consumption by:
- `content-generator` skill (optimize content)
- `social-media-engagement` skill (prioritize platforms)
- Notification systems (alert on critical issues)

---

## API Configuration

```python
POSTBRIDGE_BASE = "https://api.post-bridge.com/v1"
POSTBRIDGE_KEY = "REDACTED_ROTATED_CREDENTIAL"
```

---

## Cron Schedule (Recommended)

```cron
# Daily analytics report at 07:00 WIB (00:00 UTC)
0 0 * * * cd ~/.openclaw/workspace/skills/1ai-skills/marketing/content-analytics-engine/scripts && python3 report_generator.py --sync >> ~/.openclaw/workspace/reports/analytics-cron.log 2>&1

# Quick cached report at 12:00 and 18:00 WIB
0 5,11 * * * cd ~/.openclaw/workspace/skills/1ai-skills/marketing/content-analytics-engine/scripts && python3 report_generator.py --cache >> ~/.openclaw/workspace/reports/analytics-cron.log 2>&1
```

---

## Current Status (2026-03-13)

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total Views | 469 | 10,000+ | 🔴 Critical |
| Engagement Rate | 0.64% | 1%+ | 🔴 Below target |
| LYNK Clicks | 196 | 500+ | 🟡 Improving |
| Sales | 0 | 5+ | 🔴 Zero revenue |
| Post Errors (IG) | 40 | 0 | 🔴 Fix needed |

### Critical Issues
1. **Instagram posts fail** — Must include media (no text-only)
2. **0% sales conversion** — LYNK landing page not converting
3. **Low view volume** — Need 10K+ views for meaningful data

---

## References

- `references/metrics-guide.md` — Full metrics definitions, benchmarks, diagnostics
- PostBridge API docs: https://api.post-bridge.com/reference
- LYNK Dashboard: https://lynk.id/jendralbot

## How to Use

1. Define campaign objective and target KPIs
2. Set up tracking and attribution (UTMs, pixels, events)
3. Create campaign assets (copy, creatives, landing pages)
4. Launch with small budget for testing
5. Monitor metrics daily, optimize underperformers
6. Scale winners, pause losers, document learnings

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Red Flags

- **Metrics declining 3+ days**: Investigate funnel leaks or audience fatigue
- **Ad spend with zero conversions**: Pause and review targeting/creative
- **Email open rates below 15%**: Subject lines or sender reputation issue
- **Bounce rate above 70%**: Landing page mismatch or slow load times
- **Attribution gaps**: Missing UTM parameters or broken tracking pixels

## Verification

- Run A/B test with control group before full rollout
- Verify tracking pixels fire correctly on all conversion pages
- Check UTM parameters parse correctly in analytics dashboard
- Confirm email deliverability via seed list test
- Validate landing page speed (target < 3s load time)

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
