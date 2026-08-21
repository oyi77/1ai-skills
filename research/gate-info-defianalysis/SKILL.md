---
name: gate-info-defianalysis
description: Use when analyze a DeFi protocol — TVL, chains, yield pools, and audit/risk posture via public APIs (DeFiLlama). Use when working with DeFi protocol analysis.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
  - gate
  - info
  - research
  - defi
  - tvl
  - risk
version: 1.0.0
category: research
---

## Overview

`gate-info-defianalysis` runs a **DeFi protocol analysis playbook** using DeFiLlama's free public API (no key required). It pulls protocol TVL, supported chains, audit metadata, and current yield pools, then synthesizes a risk-weighted assessment. Standalone, tool-agnostic rewrite of the upstream `gate-info-defianalysis` skill.

## When to Use

- "Analyze the Aave protocol"
- "What's the TVL and risk on [protocol]"
- "Compare yield pools for [protocol]"
- "Is [protocol] audited / multichain"

## When NOT to Use

- Single ERC-20 token risk (honeypot/tax) — use `gate-info-riskcheck`.
- A Layer-1 coin deep dive — use `gate-info-coinanalysis`.
- Whole-market snapshot — use `gate-info-marketoverview`.

## Workflow

### Step 1 — Resolve protocol slug

```bash
curl -s "https://api.llama.fi/protocols" | jq -r '.[] | select(.name=="Aave") | .slug'
# → aave
```

### Step 2 — Protocol TVL + chains + audits

```bash
curl -s "https://api.llama.fi/protocol/aave" \
  | jq '{tvl: .tvl, chains: .chains, audits: .audits, category: .category, listedAt: .listedAt}'
```

### Step 3 — Yield pools (if relevant)

```bash
curl -s "https://yields.llama.fi/pools" \
  | jq '.data[] | select(.project=="aave") | {symbol, chain, apy, tvlUsd, pool: .pool}'
```

### Step 4 — Synthesize

```
## DeFi Analysis: [protocol]  (playbook: defi)
### Snapshot
- Current TVL, category, # chains
- Audit count / recency (DeFiLlama `audits` field; cross-check on the protocol site)
- Top yield pools (apy, tvlUsd, chain)
### Risk Read
- 2–4 sentences: concentration, audit posture, chain spread
### Risks
- What would invalidate the bullish read (TVL cliff, exploit history, unaudited pool)
### Sources
- DeFiLlama /protocol/{slug}, /pools
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "DeFiLlama TVL is the whole story" | TVL is necessary, not sufficient. Audit posture and pool-level risk matter. |
| "No audit endpoint = unaudited" | DeFiLlama reports `audits`; absence means verify on the protocol's own disclosures before concluding. |
| "Higher APY = better" | APY without TVL and audit context is a yield trap. Always pair apy with tvlUsd. |

## Code Example

Fetch Aave TVL, chains, and audit metadata:

```bash
curl -s "https://api.llama.fi/protocol/aave" \
  | jq '{tvl: .tvl, chains: .chains, audits: .audits}'
# → {"tvl":12000000000,"chains":["Ethereum","Arbitrum","Optimism"],"audits":4}
```

## Verification

- [ ] Protocol slug resolved to exactly one entry from `/protocols`.
- [ ] TVL, chains, and audit fields pulled from `/protocol/{slug}`.
- [ ] If yields requested, pools filtered by `project` from `/pools`.
- [ ] Output follows the DeFi Analysis template (Snapshot / Risk Read / Risks / Sources).
- [ ] Audit absence explicitly verified, not assumed.
