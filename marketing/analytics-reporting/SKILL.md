---
name: analytics-reporting
description: "Quick reference for automated analytics reporting — scheduled report generation, alert triggers, and cross-platform metric aggregation. Use when working with analytics reporting."
domain: marketing
tags: [analytics, reporting, automation, dashboards, metrics]
version: 1.1.0
---

# Quick Reference: Analytics Reporting

> **Full analytics dashboard skill**: See `../analytics-dashboard/SKILL.md` for complete dashboard implementation, metrics tracking, and growth strategy frameworks. This page focuses specifically on automated report generation and distribution.

## Overview

Analytics reporting transforms raw platform metrics (social media engagement, ad performance, website traffic, revenue) into digestible, scheduled reports that drive business decisions. While dashboards provide real-time monitoring, reports serve as periodic snapshots — daily, weekly, monthly — that track trends, compare periods, and flag anomalies. Automated report pipelines reduce manual data gathering from hours to minutes.

## When to Use

- You need scheduled daily/weekly/monthly reports pushed to Slack, email, or Telegram
- You want automated anomaly detection (e.g., "engagement dropped 30% this week")
- You're aggregating data from multiple platforms into a unified business review
- You need to distribute tailored reports to different stakeholders (team, investors, clients)

## Quick Start

1. **Define report cadence** — Choose period (daily ops, weekly growth, monthly executive) and list metrics per report; every metric must answer a specific business question
2. **Collect data** — Build a collector that pulls from each platform's API and stores raw data in a SQLite staging table
3. **Generate and send** — Render a formatted report with trend comparisons and anomaly flags, push via webhook or email

## Code Example: Weekly Growth Report

```python
import sqlite3
from datetime import datetime, timedelta

def generate_weekly_report(db_path: str = "analytics.db") -> str:
    """Build a weekly report comparing current vs previous week."""
    conn = sqlite3.connect(db_path)
    conn.execute("""CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL, metric TEXT NOT NULL,
        value REAL NOT NULL, recorded_at TEXT NOT NULL)""")
    cursor = conn.cursor()
    today, last_week = datetime.utcnow(), datetime.utcnow() - timedelta(days=7)
    prev_week = today - timedelta(days=14)

    def sum_metric(platform, metric, since):
        cursor.execute("SELECT COALESCE(SUM(value), 0) FROM metrics "
            "WHERE platform=? AND metric=? AND recorded_at BETWEEN ? AND ?",
            (platform, metric, since.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")))
        return cursor.fetchone()[0]

    platforms = {"x": "X", "instagram": "Instagram", "tiktok": "TikTok"}
    lines = [f"# Weekly Report ({last_week.strftime('%b %d')} - {today.strftime('%b %d, %Y')})", ""]

    for key, label in platforms.items():
        lines.append(f"## {label}")
        cur = sum_metric(key, "followers_gained", last_week)
        prev = sum_metric(key, "followers_gained", prev_week)
        pct = round(((cur / prev) - 1) * 100, 1) if prev else 0
        arrow = "↑" if pct > 5 else "↓" if pct < -5 else "→"
        lines.append(f"- **Followers**: {cur:.0f} {arrow} {pct:+.1f}%")
        lines.append("")

    conn.close()
    return "\n".join(lines)

# Usage: print(generate_weekly_report("analytics.db"))
```

## Verification Checklist

- [ ] Reports run on schedule (cron/systemd timer) and deliver to correct channels
- [ ] All platform APIs return valid data before generation (fail gracefully with partial data)
- [ ] Week-over-week trend calculations are correct (test with known data)
- [ ] Anomaly thresholds are tuned per metric (engagement is noisier than revenue)
- [ ] Reports include both absolute values AND percentage changes
- [ ] Webhook/email delivery failures trigger an alert, not silent data loss
- [ ] Historical data is append-only — never overwrite, always insert with timestamp

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just check the dashboard, I don't need reports" | Dashboards show current state but miss trends. A weekly report captures momentum, compares periods, and surfaces anomalies you'd scroll past. |
| "More metrics = better reporting" | Every metric that doesn't drive a decision is noise. Apply the "So what?" test — if it wouldn't change a decision, drop it. |
| "Manual reporting is faster than coding" | Manual takes 2+ hours/week, scales linearly, and introduces errors. A 30-minute script pays for itself in 2 weeks. |

## Workflow
Redirected to parent skill at `../analytics-dashboard/SKILL.md`.
