---
name: gate-info-marketoverview
description: Use when produce a crypto market-wide snapshot — total cap, BTC dominance, top movers, and trending assets via public APIs (CoinGecko). Use when working with market overview.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
  - gate
  - info
  - research
  - crypto
  - market-overview
  - macro
version: 1.0.0
category: research
---

## Overview

`gate-info-marketoverview` runs a **market-wide snapshot playbook** using CoinGecko's `/global` and `/coins/markets` endpoints. It produces a macro picture (total cap, BTC dominance, volume) plus the day's notable movers. Standalone, tool-agnostic rewrite of the upstream `gate-info-marketoverview` skill. For a specific coin, route to `gate-info-coinanalysis` instead.

## When to Use

- "How is the market"
- "Market overview"
- "What's happening in crypto today"
- "Give me the macro picture"

## When NOT to Use

- A specific single coin — use `gate-info-coinanalysis`.
- Comparing a fixed set of coins — use `gate-info-coincompare`.
- A DeFi protocol — use `gate-info-defianalysis`.

## Workflow

### Step 1 — Macro totals

```bash
curl -s "https://api.coingecko.com/api/v3/global" \
  | jq '.data | {total_mcap: .total_market_cap.usd,
                 total_vol: .total_volume.usd,
                 btc_dominance: .market_cap_percentage.btc,
                 eth_dominance: .market_cap_percentage.eth,
                 mcap_change_24h: .market_cap_change_percentage_24h_usd}'
```

### Step 2 — Top movers

```bash
curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1" \
  | jq '.[] | {symbol, price: .current_price, change_24h: .price_change_percentage_24h, mcap: .market_cap}'
```

### Step 3 — Trending

```bash
curl -s "https://api.coingecko.com/api/v3/search/trending" \
  | jq '.coins[].item | {symbol, name, rank: .market_cap_rank}'
```

### Step 4 — Synthesize

```
## Market Overview  (playbook: market_overview)
### Macro
- Total cap / 24h change, BTC + ETH dominance, total volume
### Top movers (top 20 by cap)
- Biggest 24h gainers / losers
### Trending
- Named trending assets
### Read
- 2–3 sentences on regime (risk-on/off, concentration, breadth)
### Sources
- CoinGecko /global, /coins/markets, /search/trending
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "BTC dominance alone defines the regime" | Pair dominance with total-cap change and breadth (gainers vs losers). One metric is a hint, not a verdict. |
| "Trending list = buy list" | Trending is attention, not conviction. Report it as signal, not recommendation. |
| "Top 20 by cap is the whole market" | It's a proxy. State it as a proxy; full breadth needs more sampling. |

## Code Example

Macro snapshot in one call:

```bash
curl -s "https://api.coingecko.com/api/v3/global" | jq '.data | {total_mcap: .total_market_cap.usd, btc_dominance: .market_cap_percentage.btc}'
# → {"total_mcap":2.4e12,"btc_dominance":54.2}
```

## Verification

- [ ] `/global` pulled (total cap, 24h change, BTC/ETH dominance, volume).
- [ ] Top movers pulled from `/coins/markets` (consistent vs_currency + snapshot).
- [ ] Trending pulled from `/search/trending`.
- [ ] Output follows the Market Overview template (Macro / Movers / Trending / Read / Sources).
- [ ] Single-coin questions routed to `gate-info-coinanalysis`, not answered here.
