---
name: gate-exchange-autoinvest
description: "Dollar-cost-averaging (auto-invest) plan design — investment currency, target allocation, cadence, and fund-flow discipline. Strategy-only; uses public data, no exchange CLI/MCP."
domain: trading
author: oyi77
license: Apache-2.0
subdomain: trading
tags:
  - trading
  - dca
  - auto-invest
  - portfolio
version: 1.0.0
category: trading
---

# Auto-Invest / DCA Plan Design

Methodology from Gate.io's auto-invest playbook — re-expressed as a portable DCA strategy. Replace the exchange's bundled CLI with public coin/market data so you can design a dollar-cost-averaging plan yourself.

## When to Use
- You want to accumulate an asset on a fixed schedule rather than timing entries.
- You want to split a recurring buy across multiple targets (max 10, min 10% each).
- Trigger phrases: "auto-invest", "DCA", "dollar cost averaging", "invest plan".

## Workflow

### Phase 1: Pick investment currency + cadence
- **Investment currency**: USDT or BTC — what you fund the plan with.
- **Cadence**: hourly / daily / weekly / biweekly / monthly. Match frequency to your cash flow; don't over-trade with hourly if fees eat the edge.

### Phase 2: Define targets + allocation
- List target coins from a supported set (verify via CoinGecko or the exchange's public market list).
- Up to 10 targets; each ≥10%. The plan buys per the allocation split every cycle.
- Example: BTC 50% / ETH 30% / SOL 20%.

### Phase 3: Choose fund flow
- **Spot**: bought assets land in your spot wallet (tradable immediately).
- **Earn**: bought assets auto-deposit into a savings/earn product (illiquid until redeemed). Pick deliberately.

### Phase 4: Confirmation gate (mandatory)
- Present a draft: currency, cadence, targets+%, fund flow, per-cycle amount.
- Do not create until the user explicitly confirms.
- Verify result by inspecting the returned plan id and status — not just HTTP 200.

## Anti-Rationalization Table
| Rationalization | Reality |
|---|---|
| "DCA means I don't need a plan" | Allocation and cadence are the plan; undefined targets = undefined outcome. |
| "Hourly is best for compounding" | Higher frequency = more fee drag; match cadence to edge. |
| "I'll set 5% allocations" | Minimum per-target is 10%; sub-threshold splits are rejected. |
| "HTTP 200 means the plan is live" | Inspect the returned plan id/status; 200 can wrap a rejected config. |

## Overview
Auto-invest is mechanical accumulation: fixed currency, fixed cadence, weighted targets. Design allocation from a supported set, choose spot vs earn deliberately, and confirm before any write. Discipline over emotion — DCA removes timing risk but not selection risk.

## Verification
- [ ] Investment currency and cadence explicit.
- [ ] Targets from a supported set; each ≥10%, ≤10 total.
- [ ] Fund flow (spot vs earn) chosen deliberately.
- [ ] Draft presented; create executed only after explicit confirmation.
- [ ] Result verified via returned plan id/status, not HTTP code alone.
- [ ] No API key; plan design only.
