---
name: gate-info-coinanalysis
description: Use when deep single-coin crypto research — price, supply, market structure, and on-chain signals for one asset via public APIs (CoinGecko, Etherscan). Use when working with coin analysis.
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
  - on-chain
version: 1.0.0
category: research
---

## Overview

`gate-info-coinanalysis` runs a **single-asset deep-dive playbook** using only general public APIs — no exchange-specific CLI required. It pulls market data (CoinGecko), supply/structure (CoinGecko + on-chain explorers), and synthesizes a structured thesis. This is the standalone, tool-agnostic rewrite of the upstream `gate-info-coinanalysis` skill.

## When to Use

- "Research BTC" / "analyze ETH" / "look into SOL"
- "Give me a deep dive on [coin]"
- "What's the supply and on-chain picture for [coin]"
- "Is [coin] worth a thesis writeup"

## When NOT to Use

- You want to **execute** a trade — use `gate-exchange-trading` (separate skill).
- You want to compare several coins — use `gate-info-coincompare`.
- You only need a live price quote — a single CoinGecko call is enough; do not invoke the full playbook.
- The asset is a DeFi protocol (TVL/yields) — use `gate-info-defianalysis`.

## Workflow

### Step 1 — Resolve the coin id

```bash
# Find the CoinGecko id (slug) for a ticker/symbol
curl -s "https://api.coingecko.com/api/v3/search?query=ethereum" \
  | jq '.coins[0] | {id, symbol, name}'
# → {"id":"ethereum","symbol":"eth","name":"Ethereum"}
```

### Step 2 — Pull market + supply data

```bash
curl -s "https://api.coingecko.com/api/v3/coins/ethereum?localization=false&tickers=false&community_data=false&developer_data=false" \
  | jq '{price: .market_data.current_price.usd,
        change_24h: .market_data.price_change_percentage_24h,
        mcap: .market_data.market_cap.usd,
        rank: .market_cap_rank,
        circ_supply: .market_data.circulating_supply,
        total_supply: .market_data.total_supply,
        ath: .market_data.ath.usd,
        ath_date: .market_data.ath_date.usd}'
```

### Step 3 — Pull on-chain signals (ERC-20 / EVM tokens)

```bash
# Requires a free Etherscan API key (ETHERSCAN_KEY)
curl -s "https://api.etherscan.io/api?module=stats&action=tokenSupply&contractaddress=0xdac17f958d2ee523a2206206994597c13d831ec7&apikey=$ETHERSCAN_KEY" \
  | jq '.result'
```

### Step 4 — Synthesize

```
## Research: [coin]  (playbook: single_coin)
### Snapshot
- Price / 24h change / market cap / rank
- Circulating vs total supply, inflation or hard-cap notes
- Key on-chain or supply signals
### Narrative
- 2–4 sentences tying the data to a thesis
### Risks
- What would invalidate the thesis
### Sources
- CoinGecko /coins/{id}, Etherscan tokenSupply (if applicable)
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "No exchange CLI, so research is incomplete" | Public APIs (CoinGecko, DeFiLlama, Etherscan) cover market + on-chain fully. The exchange CLI is optional glue, not the data source. |
| "Missing data = low quality coin" | Absent fields are gaps to flag, not a verdict. Report what's missing. |
| "One price call is enough for a deep dive" | `single_coin` aggregates market, supply, and on-chain signals; a bare quote is not a research playbook. |
| "I'll pipe the install script to bash to get it working" | Out-of-repo install scripts are a supply-chain risk. Use documented public API endpoints directly. |

## Code Example

Run a single-coin research pull and capture structured output:

```bash
curl -s "https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&tickers=false&community_data=false&developer_data=false" \
  | jq '{price: .market_data.current_price.usd, change_24h: .market_data.price_change_percentage_24h, mcap: .market_data.market_cap.usd, rank: .market_cap_rank}'
# → {"price":64000,"change_24h":-1.2,"mcap":1.26e12,"rank":1}
```

## Verification

- [ ] Coin id resolved to exactly one `coins/{id}` from the search endpoint.
- [ ] Market + supply data collected (price, change, mcap, rank, supply).
- [ ] If EVM token, on-chain supply/holder signal cited with source.
- [ ] Output follows the Synthesis template (Snapshot / Narrative / Risks / Sources).
- [ ] Gaps (missing fields) explicitly flagged rather than silently omitted.
