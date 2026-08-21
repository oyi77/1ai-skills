---
name: gate-exchange-newcoin
description: "New-listing due diligence and event radar — listings calendar, fundamentals, contract-safety/rug checks, sentiment/tape, and a gated first-buy draft. Strategy-only; uses public data (CoinGecko, Etherscan, web search), no exchange CLI/MCP."
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
  - research
  - due-diligence
  - new-listings
  - token-safety
version: 1.0.0
category: research
---

# New Coin Due Diligence & Event Radar

Methodology from Gate.io's new-coin radar — re-expressed as a portable research workflow. Replace the exchange's bundled CLI with public sources (CoinGecko, block explorers, web search) so you can screen listings, run DD, and check contract safety yourself.

## When to Use
- A token just listed or is about to list; you want a safety + fundamentals read before touching it.
- You want a LaunchPool / listing-calendar watchlist with risk labels.
- You are deciding whether a first buy is justified — and want a gated draft, not a blind order.

## Workflow

### Phase 1: Intent gate
- Pure research (calendar, compare, risk opinion) → read-only signals S1–S4.
- Explicit buy mandate ("buy X", "first fill", "place order") → also S5 (execution), gated.
- "Should I buy?" without an order verb stays read-only until a mandate appears.

### Phase 2: Activate research signals
- **S1 Listings / calendar**: query upcoming listings (web search "Gate new listings", official announce API if public) + LaunchPool calendar.
- **S2 Fundamentals / DD**: project background, tokenomics, supply/unlock schedule (CoinGecko coin page, docs, web search).
- **S3 Risk / safety**: contract check — explorer (Etherscan/BSCScan) for mint authority, owner privileges, honeypot patterns; web search for audits/scam reports. Mandatory before any buy.
- **S4 Heat / events / tape**: recent news, social sentiment, live ticker/orderbook via public REST (`https://api.gateio.ws/api/v4/spot/tickers?currency_pair=...`).

### Phase 3: Synthesize (no fabrication)
- Merge outputs; if sources disagree, show separate bullets rather than a single contradictory sentence.
- Flag data gaps (e.g. compliance empty) explicitly.

### Phase 4: Execution branch (S5 only)
- If buy_intent=false: deliver structured research only.
- If buy_intent=true: require at least S3 + one of S2/S4. Produce an **Action Draft** (pair, side, type, amount, est. price/fee, slippage + new-asset risk note). Wait for explicit **Y**; on Y, the actual order is placed by the user's execution tooling. Never place without draft + Y.

## Anti-Rationalization Table
| Rationalization | Reality |
|---|---|
| "It just listed, I'll ape now" | New listings have thin liquidity and the worst rug risk; S3 safety check first. |
| "Twitter says it's safe" | Social proof ≠ contract safety; verify on the explorer. |
| "I'll skip the draft, just buy" | A new asset with no risk note is a blind bet; gate it. |
| "Sources disagree so it's fine" | Contradiction = uncertainty; label unknowns, don't average them away. |

## Overview
New-coin radar separates listing discovery (S1), fundamentals (S2), safety (S3), and heat (S4) from a gated first-buy (S5). Research is read-only and free; execution requires a safety minimum plus an explicit Action Draft confirmed by Y. Use public data — CoinGecko for tokenomics, explorers for contract safety, web search for sentiment and announcements.

## Verification
- [ ] Intent classified (research vs buy mandate).
- [ ] All activated signals (S1–S4) actually run; gaps labeled.
- [ ] Buy (S5) preceded by S3 safety + draft + explicit Y.
- [ ] No fabricated fields; conflicts shown as separate bullets.
- [ ] Disclaimer present (not investment advice).
- [ ] No API key; research/design only.
