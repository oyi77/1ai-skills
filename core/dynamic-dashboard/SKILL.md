---
name: dynamic-dashboard
description: >
  Real-time data aggregation dashboard — PostBridge analytics, cashflow,
  trading P&L, LYNK clicks. Generates markdown summary saved to notes/.
version: "1.0.0"
author: BerkahKarya AI
tags: [dashboard, analytics, postbridge, cashflow, trading, lynk, metrics]
---

# Dynamic Dashboard

## Overview

Aggregates real-time data from multiple sources into a unified markdown dashboard. Fetches PostBridge analytics, cashflow data, trading P&L, and LYNK click metrics in parallel.

## Data Sources

| Source | What | File/API |
|--------|------|----------|
| PostBridge | Social media analytics | logs/postbridge_health.log, notes/postbridge-analytics-latest.md |
| Cashflow | Revenue & expenses | scripts/cashflow_monitor.py output |
| Trading | P&L from Polymarket/weather | logs/fastloop_trader.log, logs/weather_trader.log |
| LYNK | Click/conversion metrics | logs/lynk_monitoring.log |

## Usage

```bash
# Generate full dashboard
python3 scripts/dashboard_generator.py generate

# Specific section only
python3 scripts/dashboard_generator.py generate --section postbridge

# Save to custom location
python3 scripts/dashboard_generator.py generate --output notes/custom-dashboard.md
```

## Output

Markdown file saved to `notes/dashboard-{date}.md` with:
- Key metrics summary (top of file)
- PostBridge section: post counts, engagement, account health
- Cashflow section: revenue, expenses, net
- Trading section: P&L by strategy
- LYNK section: clicks, conversions, top links
- Generated timestamp
