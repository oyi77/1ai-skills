---
name: gate-exchange-marketanalysis
description: "Read-only crypto market structure and sentiment analysis for any spot/perp market — trend, support/resistance, volume profile, funding, and social/news sentiment. Produces a structured market brief with no execution glue."
domain: trading
author: oyi77
license: Apache-2.0
subdomain: trading
tags:
  - trading
  - market-analysis
  - sentiment
  - technical-analysis
version: 1.0.0
category: trading
---

# Crypto Market Analysis (Strategy-Only)

Methodology distilled from Gate.io's marketanalysis playbook — stripped of any exchange-specific CLI/MCP glue. Use public market data (CoinGecko, exchange public REST, DeFiLlama) and social/news search.

## When to Use
- Pre-trade context: decide IF and WHERE to trade before committing capital.
- Weekly/bi-weekly market brief for a watchlist.
- Triangulating a thesis from price structure + sentiment before running a grid/dual/DCA strategy.

## Workflow

### Phase 1: Pull Market Snapshot
- Spot price, 24h change, 24h volume, circulating supply, market cap from CoinGecko or exchange public ticker.
```bash
pip install requests
python3 - <<'PY'
import requests
r = requests.get("https://api.coingecko.com/api/v3/coins/markets",
    params={"vs_currency":"usd","ids":"bitcoin,ethereum","order":"market_cap_desc"})
for c in r.json():
    print(c["symbol"], c["current_price"], c["price_change_percentage_24h"], c["total_volume"])
PY
```
- Order book depth + recent trades from exchange public REST (no auth):
```bash
curl -s "https://api.gateio.ws/api/v4/spot/order_book?currency_pair=BTC_USDT&limit=20" | head -c 800
```

### Phase 2: Structure Analysis
- Identify trend (HH/HL vs LH/LL on 4h/1d).
- Mark key support/resistance from volume nodes and prior swing highs/lows.
- Compute 24h volume vs 7d average — volume confirms or rejects moves.

### Phase 3: Sentiment Layer
- News: search last 7 days for the asset + "partnership|hack|delisting|listing|regulation".
- Social: search X/Reddit for mention velocity and sentiment skew.
- Funding (perp): positive funding = crowded long; negative = crowded short.

### Phase 4: Emit Brief
- One-line thesis, confidence (low/med/high), key levels, sentiment read, open questions.
- Explicitly label unknowns — analysis is not a prediction.

## Anti-Rationalization Table
| Rationalization | Reality |
|---|---|
| "Chart looks bullish, I'll just buy" | Structure + sentiment only justify a plan; size and invalidation still required. |
| "Volume doesn't matter for a quick trade" | Low-volume moves reverse fast; you get slipped on exit. |
| "Social is super bullish so it'll moon" | Crowded retail sentiment is often a contrarian top signal. |
| "I'll skip the brief, I already have a feel" | Feel is untestable; the brief is the receipt you re-check at invalidation. |

## Overview
Read-only analysis. No orders, no keys, no execution. The output is a decision-support brief: trend, levels, sentiment, and explicit unknowns. Pair with a separate execution playbook (grid/dual/DCA) only after the brief clears.

## Verification
- [ ] Snapshot pulled from a live public endpoint (not hardcoded numbers).
- [ ] Brief names at least 1 support and 1 resistance level with source.
- [ ] Sentiment section cites at least 1 dated news/social signal.
- [ ] Thesis states confidence AND invalidation condition.
- [ ] No execution step, no API key, no trade placed.
