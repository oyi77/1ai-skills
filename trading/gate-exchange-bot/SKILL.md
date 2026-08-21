---
name: gate-exchange-bot
description: "Grid and martingale trading-bot strategy design — parameter discipline, range/leverage/direction selection, and confirmation gates. Strategy-only; uses public market data, no exchange CLI/MCP."
domain: trading
author: oyi77
license: Apache-2.0
subdomain: trading
tags:
  - trading
  - grid
  - martingale
  - automation
version: 1.0.0
category: trading
---

# Grid & Martingale Bot Strategy Design

Methodology from Gate.io's trading-bot playbook — re-expressed as a portable strategy. Replace the exchange's bundled CLI with public spot/futures data so you can design grid and martingale parameters yourself and reason about risk before any order.

## When to Use
- You want automated range capture (grid) instead of timing single entries.
- You want to average down on dips (martingale) with a defined cap.
- You are comparing spot-grid vs futures-grid (leverage) vs infinite-grid (no upper bound).

## Workflow

### Phase 1: Classify bot type
- **Spot grid**: buys low / sells high within [lower, upper] on spot. No leverage. Best in sideways/range markets.
- **Infinite grid**: like spot grid but only a lower bound; above it, profit is taken as the asset keeps rising. Captures trends without a fixed ceiling.
- **Futures grid**: adds leverage and a direction (neutral/long/short). Amplifies both grid profit and liquidation risk.
- **Spot/Contract martingale**: after each adverse move of N%, add a position of increasing size. Needs an explicit stop/cap or it becomes unbounded.

### Phase 2: Anchor to live data
Pull the current price to center your range; never pick range endpoints blind:
```bash
python3 - <<'PY'
import requests
r = requests.get("https://api.gateio.ws/api/v4/spot/tickers?currency_pair=BTC_USDT")
last = float(r.json()[0]["last"])
print(f"last={last:.2f}  grid_low={last*0.92:.2f}  grid_high={last*1.08:.2f}")
PY
```

### Phase 3: Set parameters explicitly
- **Range**: lower/upper must reflect actual support/resistance, not wishful bounds.
- **Grid count**: more grids = smaller per-grid profit, smoother capture; more fee exposure.
- **Leverage (futures only)**: >1x multiplies liquidation speed. Size so a 10–20% adverse move does not liquidate the whole grid.
- **Martingale deviation**: the % drop that triggers the next add. Pair it with a HARD max add count / max capital.

### Phase 4: Confirmation gate (mandatory)
- Every bot creation is a write. Present a draft: type, pair, range, grid count, leverage, direction, total capital at risk.
- Do not execute until the user explicitly confirms the draft.
- Verify result by inspecting the returned order/strategy id and status — not just HTTP 200.

## Anti-Rationalization Table
| Rationalization | Reality |
|---|---|
| "The bot will handle the timing for me" | Bots execute your parameters blindly; bad range/leverage = systematic loss. |
| "I'll let it run, no need to set a stop" | Martingale without a cap is a liquidation engine. Define max adds before starting. |
| "Futures grid with 10x doubles my profit" | It also halves your adverse-move tolerance. Liquidation ends the bot. |
| "HTTP 200 means it worked" | Inspect the returned strategy id/status; a 200 can wrap a rejected or partially-filled order. |

## Overview
Grid bots monetize range; martingale monetizes dips — both assume you accept the range and its risks. Design parameters from live data, separate strategy recommendation from creation, and never guess core inputs (range, grid count, leverage, direction, martingale deviation). Confirm before any write.

## Verification
- [ ] Bot type matches market view (range vs trend vs leverage).
- [ ] Range/leverage anchored to live price, not guessed.
- [ ] Martingale has an explicit max-add / max-capital stop.
- [ ] Draft presented; write executed only after explicit confirmation.
- [ ] Result verified via returned id/status, not HTTP code alone.
- [ ] No API key placed; strategy design only.
