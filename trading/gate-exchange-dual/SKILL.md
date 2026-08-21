---
name: gate-exchange-dual
description: "Dual investment (sell-high / buy-low) yield strategy design — strike selection, settlement logic, and forced-position risk. Strategy-only; uses public market data, no exchange CLI/MCP."
domain: trading
author: oyi77
license: Apache-2.0
subdomain: trading
tags:
  - trading
  - yield
  - options-like
  - structured-products
version: 1.0.0
category: trading
---

# Dual Investment (Sell-High / Buy-Low)

Methodology from Gate.io's dual-investment playbook — re-expressed as a portable strategy. Replace the exchange's bundled CLI with public spot/funding data so you can model strikes, yields, and settlement outcomes yourself.

## When to Use
- You hold an asset and want yield by committing to SELL at a higher price (sell-high).
- You hold stablecoins and want to accumulate an asset by committing to BUY at a lower price (buy-low).
- Sideways-to-range markets where you have a price opinion but no urgency to transact.

## Workflow

### Phase 1: Pick Direction
- **Sell-high**: You are bullish-ish but happy to part at a premium. Commit asset A, target sell price = strike (> current spot). If spot ≥ strike at settlement → you sell at strike + earn yield; else you keep A.
- **Buy-low**: You want asset A cheaper. Commit stablecoin, target buy price = strike (< current spot). If spot ≤ strike at settlement → you buy at strike + earn yield; else you keep stablecoin.

### Phase 2: Select Strike & Tenor
- Strike should sit at a level you genuinely accept the trade at. Selling at +8% above spot is only good if you'd sell there anyway.
- Use current spot + historical volatility to sanity-check the strike distance:
```bash
pip install requests
python3 - <<'PY'
import requests
# last price as anchor for strike math
r = requests.get("https://api.gateio.ws/api/v4/spot/tickers?currency_pair=ETH_USDT")
last = float(r.json()[0]["last"])
for pct in (0.05, 0.08, 0.12):
    print(f"sell-high strike +{int(pct*100)}% = {last*(1+pct):.2f}")
PY
```

### Phase 3: Model Settlement
- At settlement time T: compare spot_T vs strike.
- Sell-high: spot_T ≥ strike → settled (sold at strike, yield paid). spot_T < strike → not settled (asset returned, NO yield).
- Buy-low: spot_T ≤ strike → settled (bought at strike, yield paid). spot_T > strike → not settled (stablecoin returned, NO yield).
- APR shown by the product = yield / notional / tenor. Verify it against your own capital-at-risk.

### Phase 4: Pre-Commit Checklist
- [ ] Strike is a price you accept the trade at, not a "wouldn't it be nice" number.
- [ ] You understand the worse-case: being forced into the asset (sell-high not hit → you keep asset, miss rally) or forced out (buy-low hit → you now hold a falling asset).
- [ ] Tenor matches your view horizon.

## Anti-Rationalization Table
| Rationalization | Reality |
|---|---|
| "High APR means free yield" | APR is paid ONLY if the option settles in your favor; otherwise you get nothing and possibly the wrong asset. |
| "I'll just pick the farthest OTM strike for max APR" | Farther OTM = lower settlement probability = you mostly keep capital and earn zero. |
| "It's basically staking" | No. It's a short option. Forced execution at strike is the whole point. |
| "Spot will definitely stay below strike" | Nothing is definite; size so a settled outcome is acceptable either way. |

## Overview
Dual investment is a covered short option dressed as yield. Sell-high = covered call; buy-low = cash-secured put. The edge is the premium (yield) for giving up upside/downside at a level you pre-accept. Model it yourself before committing; do not trust the product's APR headline.

## Verification
- [ ] Direction (sell-high vs buy-low) matches your actual inventory intent.
- [ ] Strike computed from live spot, not guessed.
- [ ] Settlement matrix (both outcomes) written explicitly.
- [ ] Worst-case (forced position) is acceptable at your size.
- [ ] No API key, no order placed — this is strategy design only.
