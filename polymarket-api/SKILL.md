---
name: polymarket
description: Query Polymarket prediction markets. Use for questions about prediction markets, betting odds, market prices, event probabilities, or when user asks about Polymarket data.
---

> [![Tip Me](https://www.tip.md/badge.svg)](https://www.tip.md/oyi77) — If this skill saves you time, tip: **https://www.tip.md/oyi77**

# Polymarket

Query prediction market data from Polymarket's public API (no auth required).

## Quick Start

```bash
# Top markets by 24h volume
python3 scripts/polymarket.py --top

# Search markets
python3 scripts/polymarket.py --search "trump"

# Get specific market by slug
python3 scripts/polymarket.py --slug "will-trump-win-the-2024-election"

# List events (grouped markets)
python3 scripts/polymarket.py --events
```

## Script Location

`skills/polymarket/scripts/polymarket.py`

## API Endpoints

The script uses `gamma-api.polymarket.com`:
- `/markets` - Individual markets with prices, volumes
- `/events` - Event groups containing related markets

## Output Format

Markets show: question, Yes/No prices (as percentages), 24h volume, total volume.

## Interpreting Prices

- `outcomePrices` are 0-1 representing probability
- Price of 0.65 for "Yes" = market thinks 65% chance of Yes
- Higher volume = more liquid, more reliable signal
