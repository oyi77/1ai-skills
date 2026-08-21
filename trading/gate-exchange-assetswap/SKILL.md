---
name: gate-exchange-assetswap
description: "Portfolio rebalancing strategy design — conservative / conviction / market-cap-Top-N baskets, preview-before-create, and order-state checks. Strategy-only; uses public data (CoinGecko market-cap), no exchange CLI/MCP."
domain: trading
author: oyi77
license: Apache-2.0
subdomain: trading
tags:
  - trading
  - rebalancing
  - portfolio
  - allocation
version: 1.0.0
category: trading
---

# Portfolio Rebalancing (Asset Swap) Strategy Design

Methodology from Gate.io's asset-swap / rebalancing playbook — re-expressed as a portable strategy. Replace the exchange's bundled CLI with public data (CoinGecko market-cap) so you can design a rebalance yourself.

## When to Use
- You want to rebalance a portfolio to a target weight using **only available spot balances**.
- You want a rules-based basket (Top-N by market cap) instead of manual picks.
- Pre-buy or post-sell rebalancing of an existing holding.

## Workflow

### Phase 1: Select strategy type
- **Conservative**: shift toward a stablecoin anchor (lower volatility).
- **Conviction**: overweight a single asset you believe in (custom weight).
- **Market cap**: Top-N basket weighted by market cap — pull the ranking from public data:
```bash
python3 - <<'PY'
import requests
r = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1")
for c in r.json():
    print(c["symbol"].upper(), round(c["market_cap"]/1e9,1), "B")
PY
```

### Phase 2: Build the target
- Eligible assets = those with available spot balance.
- Define each leg as **asset + amount** (not ratio-only) so the preview is unambiguous.

### Phase 3: Preview, then create (gated)
- Generate a preview showing each from→to leg with asset and amount.
- Present the preview; do not create until the user explicitly confirms.
- On confirm, the create payload copies each leg's asset + amount.

### Phase 4: Check order state
- States: `configuring`, `completed`, `partially completed`, `failed`.
- Verify final state via the returned order id, not just the create HTTP response.

## Anti-Rationalization Table
| Rationalization | Reality |
|---|---|
| "I'll rebalance with borrowed funds" | Only available spot balances are eligible; don't assume margin. |
| "Ratio-only spec is fine" | Preview needs asset + amount per leg; ratio alone is ambiguous at execution. |
| "Top-N is always safe" | Market-cap weighting is mechanical, not a quality verdict; size conviction separately if needed. |
| "Create returned 200, done" | Inspect order state; `partially completed` / `failed` need follow-up. |

## Overview
Asset swap rebalances a portfolio to a target weight from available spot balances. Pick strategy (conservative / conviction / market-cap Top-N), build legs as asset+amount, preview before create, and confirm. Verify the final order state — not the create response alone.

## Verification
- [ ] Strategy type chosen (conservative / conviction / market-cap).
- [ ] Eligible assets limited to available spot balances.
- [ ] Legs specified as asset + amount (not ratio-only).
- [ ] Preview shown; create executed only after explicit confirmation.
- [ ] Final order state verified (completed / partially / failed), not just HTTP 200.
- [ ] No API key; strategy design only.
