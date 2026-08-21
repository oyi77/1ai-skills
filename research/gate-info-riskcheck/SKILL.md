---
name: gate-info-riskcheck
description: Use when risk-score a token — contract verification, honeypot heuristics, buy/sell tax, and open-source status via public explorers (Etherscan and equivalents). Use when working with token risk check.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
  - gate
  - info
  - research
  - crypto
  - risk
  - token
version: 1.0.0
category: research
---

## Overview

`gate-info-riskcheck` runs a **token risk-scoring playbook** using block explorer APIs. It assembles a structured risk report: contract verification, open-source status, buy/sell tax (from verified source or token-security APIs), honeypot heuristics, and high-risk-item flags. Standalone, tool-agnostic rewrite of the upstream `gate-info-riskcheck` skill.

## When to Use

- "Risk check [token]"
- "Is [token] a honeypot / safe to interact with"
- "What are the buy/sell taxes on [token]"
- "Contract risk for [contract address]"

## When NOT to Use

- General on-chain activity (supply/holders/transfers) — use `gate-info-tokenonchain`.
- Market fundamentals — use `gate-info-coinanalysis`.
- DeFi protocol TVL/audit — use `gate-info-defianalysis`.

## Workflow

### Step 1 — Contract + source verification

```bash
curl -s "https://api.etherscan.io/api?module=contract&action=getsourcecode&address=0xTOKEN&apikey=$ETHERSCAN_KEY" \
  | jq '.result[0] | {is_verified: (.SourceCode | length > 0),
                     compiler: .CompilerVersion,
                     proxy: .Proxy,
                     owner: .Owner}'
```

### Step 2 — Tax + honeypot signals

- If source is verified: inspect `transfer`/`_transfer` for fee-on-transfer math (buy/sell tax %).
- If source unavailable: defer to a token-security API (e.g. GoPlus) `GET /api/v1/token_security/{chain_id}?contract_addresses=0xTOKEN` for `buy_tax`/`sell_tax`/`is_honeypot`/`is_open_source`.
- Honeypot heuristic: can the contract be sold? Check for `is_honeypot` flag or a test sell simulation note.

### Step 3 — Open-source + high-risk items

Collect: `is_open_source`, owner renounce status, mint authority, blacklist/whitelist functions present.

### Step 4 — Synthesize

```
## Risk Check: [chain] / [contract]  (playbook: riskcheck)
### Summary
- Overall Risk Level: High / Medium / Low
- Honeypot Detected: Yes / No
- Open Source: Yes / No
### High-Risk Items
| Item | Severity | Note |
| Unverified source | High | no public code |
| Buy tax 15% | Medium | slippage risk |
### Tax Analysis
- Buy Tax: X%  | Sell Tax: Y%
### Sources
- Etherscan contract/source, token-security API (if used)
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Unverified = automatically High risk" | Correct to flag High, but still enumerate other signals; don't stop at one. |
| "0% tax = safe" | Tax is one axis. Honeypot, mint, and blacklist controls matter more. |
| "I'll pipe an install script to get the checker" | Out-of-repo scripts are supply-chain risk; use the documented explorer/security APIs. |

## Code Example

Verify source + proxy status:

```bash
curl -s "https://api.etherscan.io/api?module=contract&action=getsourcecode&address=0xTOKEN&apikey=$ETHERSCAN_KEY" \
  | jq '.result[0] | {is_verified: (.SourceCode | length > 0), proxy: .Proxy, owner: .Owner}'
# → {"is_verified":true,"proxy":"0x...","owner":"0x0"}
```

## Verification

- [ ] Contract + source verification checked (source length / CompilerVersion / Proxy).
- [ ] Buy/sell tax and honeypot signal collected (verified source math or token-security API).
- [ ] Open-source + owner/mint/blacklist controls enumerated.
- [ ] Output follows the Risk Check template (Summary / High-Risk Items / Tax / Sources).
- [ ] Overall level derived from all signals, not a single field.
