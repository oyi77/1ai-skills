---
name: gate-info-tokenonchain
description: Use when investigate a token's on-chain footprint — supply, holders, transfers, and contract verification via public explorers (Etherscan and equivalents). Use when working with token on-chain analysis.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
  - gate
  - info
  - research
  - crypto
  - on-chain
  - token
version: 1.0.0
category: research
---

## Overview

`gate-info-tokenonchain` runs a **token on-chain investigation playbook** using block explorer APIs (Etherscan for EVM; equivalent explorers for BSC/Solana/Polygon). It pulls supply, holder concentration, recent transfer activity, and contract source-verification status. Standalone, tool-agnostic rewrite of the upstream `gate-info-tokenonchain` skill. For risk scoring (honeypot/tax), route to `gate-info-riskcheck`.

## When to Use

- "Check the on-chain activity for [token]"
- "How concentrated are [token] holders"
- "Is [token] contract verified / active transfers"
- "On-chain footprint for [contract address]"

## When NOT to Use

- Risk scoring (honeypot, buy/sell tax) — use `gate-info-riskcheck`.
- Single-coin market fundamentals — use `gate-info-coinanalysis`.
- DeFi protocol TVL — use `gate-info-defianalysis`.

## Workflow

### Step 1 — Supply + verification

```bash
# Free Etherscan key (ETHERSCAN_KEY) for EVM tokens
curl -s "https://api.etherscan.io/api?module=stats&action=tokenSupply&contractaddress=0xdac17f958d2ee523a2206206994597c13d831ec7&apikey=$ETHERSCAN_KEY" | jq '.result'

# Contract source verification status
curl -s "https://api.etherscan.io/api?module=contract&action=getsourcecode&address=0xdac17f958d2ee523a2206206994597c13d831ec7&apikey=$ETHERSCAN_KEY" | jq '.result[0].CompilerVersion, .result[0].SourceCode | length'
```

### Step 2 — Recent transfers (activity proxy)

```bash
curl -s "https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0xdac17f958d2ee523a2206206994597c13d831ec7&page=1&offset=100&sort=desc&apikey=$ETHERSCAN_KEY" \
  | jq '[.result[] | {from: .from, to: .to, value: .value, ts: .timeStamp}] | length'  # count recent transfers
```

### Step 3 — Holder concentration

Use the explorer UI "Holders" tab or the `tokenholderlist` (Pro) endpoint; if unavailable, sample top transfer counterparties from Step 2 to estimate concentration qualitatively.

### Step 4 — Synthesize

```
## Token On-Chain: [contract]  (playbook: token_onchain)
### Supply
- Total supply, verified (Y/N), chain
### Activity
- Recent transfer count (proxy for liquidity/usage)
### Concentration
- Qualitative holder spread (verified source / sampled counterparties)
### Read
- 2–3 sentences: is this an active, verifiable token or a thin/unverified one
### Sources
- Etherscan stats/account/contract endpoints
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Unverified source = scam" | Unverified is a gap to flag, not a verdict. Pair with activity + concentration. |
| "100 transfers = healthy" | Count without counterparty spread says nothing about distribution. Note the limitation. |
| "Etherscan-only covers everything" | Only EVM. For BSC/Solana use the chain-equivalent explorer. |

## Code Example

Token supply + verification status in one call:

```bash
curl -s "https://api.etherscan.io/api?module=stats&action=tokenSupply&contractaddress=0xdac17f958d2ee523a2206206994597c13d831ec7&apikey=$ETHERSCAN_KEY" | jq '.result'
# → "1063422977229699987405542112"   (raw wei string)
```

## Verification

- [ ] Token supply pulled from the chain-equivalent explorer.
- [ ] Contract verification status checked (source code length / CompilerVersion).
- [ ] Recent transfer activity sampled as an activity proxy.
- [ ] Holder concentration noted with explicit method limitation.
- [ ] Output follows the Token On-Chain template (Supply / Activity / Concentration / Read / Sources).
