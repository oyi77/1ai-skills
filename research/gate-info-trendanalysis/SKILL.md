---
name: gate-info-trendanalysis
description: Use when analyze crypto price trends and momentum — multi-window performance, trending assets, and directional read via public APIs (CoinGecko). Use when working with trend analysis.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
  - gate
  - info
  - research
  - crypto
  - trend
  - momentum
version: 1.0.0
category: research
---

## Overview

`gate-info-trendanalysis` runs a **trend/momentum playbook** using CoinGecko's `market_chart` (multi-window history) and `/search/trending`. It computes directional reads (short/medium/long momentum) and pairs them with attention signals. Standalone, tool-agnostic rewrite of the upstream `gate-info-trendanalysis` skill.

## When to Use

- "What's the trend on [coin]"
- "Is [coin] trending up or down"
- "Show me momentum for [coin] across timeframes"

## When NOT to Use

- Whole-market snapshot — use `gate-info-marketoverview`.
- Single-coin fundamentals/supply — use `gate-info-coinanalysis`.
- A fixed coin comparison — use `gate-info-coincompare`.

## Workflow

### Step 1 — Multi-window history

```bash
# 1-day hourly, 7-day, 30-day — compute momentum from first vs last close
curl -s "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1"   | jq '[.prices[0][1], .prices[-1][1]]'
curl -s "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7"   | jq '[.prices[0][1], .prices[-1][1]]'
curl -s "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30"  | jq '[.prices[0][1], .prices[-1][1]]'
```

### Step 2 — Trending attention

```bash
curl -s "https://api.coingecko.com/api/v3/search/trending" | jq '.coins[].item.symbol'
```

### Step 3 — Compute momentum

```
momentum_1d  = (last/first - 1) * 100
momentum_7d  = (last/first - 1) * 100
momentum_30d = (last/first - 1) * 100
```

### Step 4 — Synthesize

```
## Trend Analysis: [coin]  (playbook: trend)
### Momentum
- 1d %, 7d %, 30d %
### Attention
- Trending list membership (yes/no) + peers
### Read
- 2–3 sentences: aligned or divergent timeframes, strength of trend
### Caveats
- Momentum is descriptive, not predictive; thin liquidity distorts short windows
### Sources
- CoinGecko /coins/{id}/market_chart, /search/trending
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "30d up = will keep going up" | Momentum is descriptive. State direction; never imply forecast. |
| "1d spike = trend" | A 1-day window is noise without 7d/30d context. Report all three. |
| "Trending = momentum confirmed" | Trending is attention, often a lagging or contrarian signal. Keep it separate. |

## Code Example

7-day momentum in one line:

```bash
curl -s "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7" \
  | jq '([.prices[0][1], .prices[-1][1]] | (.[1]/.[0]-1)*100)'
# → 3.4   (i.e. +3.4% over 7d)
```

## Verification

- [ ] History pulled for at least 1d/7d/30d windows from `/market_chart`.
- [ ] Momentum computed first-vs-last for each window.
- [ ] Trending attention checked via `/search/trending`.
- [ ] Output follows the Trend Analysis template (Momentum / Attention / Read / Caveats / Sources).
- [ ] No predictive language used.
