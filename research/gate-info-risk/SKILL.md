---
name: gate-info-risk
description: Use when crypto risk assessment on Gate.io — single-coin risk scoring, comparative risk check, and risk-plus-news overlay via gate-cli. Use when working with gate crypto risk analysis.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
  - gate
  - info
  - risk
  - crypto
  - risk-assessment
  - due-diligence
version: 1.0.0
category: research
---

## Overview

`gate-info-risk` runs **risk-assessment playbooks** through `gate-cli` (official Gate.io skills CLI). It maps a risk intent to one of three `info` risk playbooks, gathers signals via `gate-cli info` (optionally `gate-cli news` for context), and produces a scored risk verdict.

Three risk playbooks ship with `gate-cli >= 0.7.6`:

| Intent | Playbook | Core gate-cli call |
|---|---|---|
| Single-coin risk score | `single_coin_risk` | `info +[coin] +risk` |
| Compare risk across coins | `multi_coin_risk` | `info +[coin1] +[coin2] +risk` |
| Risk + news overlay | `risk_plus_news` | `info +[coin] +risk` then `news +[coin]` |

> **Upstream dependency**: `gate-cli` and the shared `gate-runtime-rules.md` / `info-news-runtime-rules.md` live in `gate/gate-skills` (GitHub). This skill is a portable command + synthesis reference — `gate-cli` must be installed and authenticated. Piping third-party install scripts to bash is out of scope (see Anti-Rationalization).

## When to Use

- "Risk check on [coin]" / "is [coin] safe to hold"
- "Compare risk: LINK vs ARB vs OP"
- "Risk assessment for [coin] + recent news"
- Due-diligence before allocating to a Gate.io-listed asset

## When NOT to Use

- You want a trade executed — use `gate-exchange-trading`.
- You want wallet fund tracing — use `gate-dex-wallet` or `gate-info-web3`.
- You want a plain price quote — a bare `info +[coin]` is enough; do not run a full risk playbook.
- Non-Gate.io assets (playbooks are Gate.io-scoped).

## Workflow

### Step 0 — Preflight

```bash
gate-cli info --preflight
# Legacy: gate-cli check-info-env
```

### Step 1 — Route intent

| User says | Playbook | Command |
|---|---|---|
| "risk check [coin]" | `single_coin_risk` | `info +[coin] +risk` |
| "compare risk [a] [b]" | `multi_coin_risk` | `info +[a] +[b] +risk` |
| "risk + news [coin]" | `risk_plus_news` | `info +[coin] +risk` then `news +[coin]` |

### Step 2 — Collect

```bash
gate-cli info +BTC +risk --format json
gate-cli news +BTC --limit 10 --format json   # risk_plus_news
```

### Step 3 — Synthesize

```
## Risk: [coin]  (playbook: single_coin_risk)
### Score
- Composite risk band (low / medium / high) + driver weights
### Drivers
- Volatility, liquidity, concentration, on-chain anomalies
### Red flags
- Any dealbreaker signals
### Sources
- gate-cli info +[coin] +risk (json), gate-cli news +[coin] (if used)
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "No news module, risk is incomplete" | `risk_plus_news` exists; for others news is optional. State the scope explicitly. |
| "Missing field = automatically high risk" | Absent data is a gap, not a verdict. Report what's missing and why. |
| "Pipe the install script to bash" | Out-of-repo scripts fail (HTTP 566 observed) and are a supply-chain risk. Use the documented `gate-cli` channel. |
| "One metric = full risk score" | `single_coin_risk` combines multiple drivers; a single ratio is not a risk playbook. |

## Code Example

```bash
gate-cli info +BTC +risk --format json | jq '{band, drivers, red_flags}'
# → {"band":"medium","drivers":["volatility","concentration"],"red_flags":[]}
gate-cli news +BTC --limit 5 --format json | jq '.[].title'
```

## Verification

- [ ] `gate-cli info --preflight` passes.
- [ ] Intent mapped to exactly one risk playbook.
- [ ] Output uses `--format json`.
- [ ] Synthesis follows Score / Drivers / Red flags / Sources.
- [ ] If news used, both calls cited.
