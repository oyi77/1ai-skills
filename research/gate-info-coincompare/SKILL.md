---
name: gate-info-coincompare
description: Use when compare multiple crypto assets side-by-side — market structure, momentum, and supply metrics via public APIs (CoinGecko). Use when working with coin comparison.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
  - gate
  - info
  - research
  - crypto
  - market-analysis
  - comparison
version: 1.0.0
category: research
---

## Overview

`gate-info-coincompare` runs a **multi-coin comparison playbook** using the CoinGecko `/coins/markets` batch endpoint. It fetches a consistent metric set for N coins in one call and renders a normalized comparison table. Standalone, tool-agnostic rewrite of the upstream `gate-info-coincompare` skill.

## When to Use

- "Compare LINK, ARB, OP"
- "Which of these 3 coins has the best momentum"
- "Side-by-side market structure for [coin A] vs [coin B]"

## When NOT to Use

- Single-coin deep dive — use `gate-info-coinanalysis`.
- Whole-market snapshot — use `gate-info-marketoverview`.
- DeFi protocol comparison (TVL/yields) — use `gate-info-defianalysis`.

## Workflow

### Step 1 — Resolve ids, then batch fetch

```bash
# Get ids once
curl -s "https://api.coingecko.com/api/v3/search?query=chainlink" | jq -r '.coins[0].id'
curl -s "https://api.coingecko.com/api/v3/search?query=arbitrum"  | jq -r '.coins[0].id'
curl -s "https://api.coingecko.com/api/v3/search?query=optimism"  | jq -r '.coins[0].id'
```

### Step 2 — Batch market data

```bash
curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=chainlink,arbitrum,optimism&order=market_cap_desc&per_page=50&page=1" \
  | jq '.[] | {id, price: .current_price, change_24h: .price_change_percentage_24h, change_7d: .price_change_percentage_7d_in_currency, mcap: .market_cap, volume: .total_volume, rank: .market_cap_rank}'
```

### Step 3 — Normalize and compare

Render a table keyed on the comparison question (momentum → 24h/7d change; structure → mcap/volume/rank). Flag missing rows.

### Step 4 — Synthesize

```
## Comparison: [coin A] vs [coin B] vs [coin C]
### Table
| Metric | A | B | C |
| Price | | | |
| 24h % | | | |
| 7d % | | | |
| MCap | | | |
| Rank | | | |
### Read
- 2–4 sentences on what the comparison shows relative to the user's question.
### Risks / Caveats
- Same vs-currency and snapshot time for all rows (single call guarantees this).
### Sources
- CoinGecko /coins/markets?ids=...
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Use separate single-coin calls and paste them together" | One `/coins/markets?ids=a,b,c` call guarantees identical snapshot time and currency — comparable rows. Separate calls drift. |
| "Missing one coin = abort" | Flag the missing row; compare what you have. |
| "More coins = better" | Comparison value drops past ~5 assets. Keep it focused on the user's set. |

## Code Example

Batch-fetch three coins and emit a momentum-sorted table:

```bash
curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=chainlink,arbitrum,optimism&order=market_cap_desc" \
  | jq -r '.[] | "\(.symbol)\t\(.price_change_percentage_24h)\t\(.market_cap)"'
# → LINK  2.1   1.2e10
# → ARB  -0.8   3.4e9
# → OP    1.3   2.1e9
```

## Verification

- [ ] All compared coins fetched in a single `/coins/markets` call (same snapshot).
- [ ] Metric set identical across rows.
- [ ] Missing coins flagged, not silently dropped.
- [ ] Output follows the Comparison template (Table / Read / Risks / Sources).
