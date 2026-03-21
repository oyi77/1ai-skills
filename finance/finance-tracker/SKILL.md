---
name: finance-tracker
description: Personal and business finance tracking — cashflow analysis, revenue summaries, burn rate, runway calculation, and revenue forecasting from log data.
permissions:
  - fs
---

# Finance Tracker

Track cashflow, analyze revenue, calculate burn rate and runway, and forecast revenue trends.

## Usage

```bash
# Revenue summary (last 7 days)
python scripts/cashflow_analyzer.py summary --days 7

# Burn rate
python scripts/cashflow_analyzer.py burn-rate

# Runway calculation
python scripts/cashflow_analyzer.py runway --balance 5000

# Revenue forecast
python scripts/cashflow_analyzer.py forecast --days 30

# Full report
python scripts/cashflow_analyzer.py report --balance 5000
```

## Functions

| Function | Description |
|----------|-------------|
| `revenue_summary(days)` | Total revenue and source breakdown |
| `burn_rate()` | Daily and monthly expense rate |
| `runway(balance)` | Months remaining at current burn |
| `forecast(days)` | Revenue projection based on trend |

## Data Source

Reads from `logs/cashflow.log` (one JSON entry per line).

Expected log format:
```json
{"date": "2026-03-20", "type": "revenue", "source": "gumroad", "amount": 49.99, "note": "skill sale"}
{"date": "2026-03-20", "type": "expense", "source": "hosting", "amount": -12.00, "note": "VPS"}
```

## Dependencies

No external dependencies — pure Python.
