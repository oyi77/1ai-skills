---
name: gate-info-web3
description: Use when Web3 / on-chain + DeFi analysis on Gate.io — token contract checks, DeFi protocol risk, and on-chain signal playbooks via gate-cli. Use when working with gate web3 / defi analysis.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
  - gate
  - info
  - web3
  - defi
  - on-chain
  - crypto
version: 1.0.0
category: research
---

## Overview

`gate-info-web3` runs **Web3 / on-chain investigation playbooks** through `gate-cli` (official Gate.io skills CLI). It maps a Web3 intent to the on-chain playbook set, gathers signals via `gate-cli info` (and optionally `gate-cli news`), and synthesizes a structured on-chain finding.

> **Routing alias**: upstream also ships `gate-info-defianalysis` as a **legacy alias** pointing at this same `gate-info-web3` skill — both IDs resolve here. Canonical id is `gate-info-web3`.

> **Upstream dependency**: `gate-cli` and shared playbook YAMLs live in `gate/gate-skills` (GitHub). This skill is a portable command + synthesis reference — `gate-cli` must be installed and authenticated. Piping third-party install scripts to bash is out of scope (see Anti-Rationalization).

## When to Use

- "Check this token contract [addr]" / "is [contract] safe"
- "Analyze this DeFi protocol [name]" / "DeFi risk on [chain]"
- "On-chain signals for [coin]" / "whale / flow analysis"
- Due-diligence on a Web3 asset listed or referenced via Gate.io

## When NOT to Use

- You want to execute a trade — use `gate-exchange-trading`.
- You want wallet-level fund tracing across chains — use `gate-dex-wallet`.
- You want plain market research (no on-chain/contract focus) — use `gate-info-research`.
- Non-Gate.io scoped assets where the playbook adds no value.

## Workflow

### Step 0 — Preflight

```bash
gate-cli info --preflight
# Legacy: gate-cli check-info-env
```

### Step 1 — Route intent

| User says | Playbook | Command |
|---|---|---|
| "check contract [addr]" | `token_contract` | `info +[addr] +web3` |
| "DeFi analysis [name]" | `defi_analysis` | `info +[name] +web3` |
| "on-chain signals [coin]" | `onchain_signals` | `info +[coin] +web3` |

### Step 2 — Collect

```bash
gate-cli info +0x...contract +web3 --format json
gate-cli news +[coin] --limit 10 --format json   # optional context
```

### Step 3 — Synthesize

```
## Web3: [target]  (playbook: token_contract | defi_analysis | onchain_signals)
### On-chain snapshot
- Contract verified? holders / concentration / mint authority
- Protocol TVL / audits / anomalies
### Signals
- Notable flows, whale activity, red flags
### Risks
- What would invalidate the assessment
### Sources
- gate-cli info +[target] +web3 (json), gate-cli news (if used)
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "No news module, Web3 analysis incomplete" | News is optional context. State scope. |
| "Missing on-chain field = scam" | Absent data is a gap, not a verdict. Report what's missing. |
| "Pipe the install script to bash" | Out-of-repo scripts fail (HTTP 566 observed) and are a supply-chain risk. Use documented `gate-cli` channel. |
| "One holder metric = full DeFi risk" | `defi_analysis` combines TVL/audits/flows; a single metric is not the playbook. |

## Code Example

```bash
gate-cli info +0xABC...DEF +web3 --format json | jq '{verified, holders, concentration}'
# → {"verified":true,"holders":1240,"concentration":0.18}
gate-cli news +[coin] --limit 5 --format json | jq '.[].title'
```

## Verification

- [ ] `gate-cli info --preflight` passes.
- [ ] Intent mapped to exactly one web3 playbook.
- [ ] Output uses `--format json`.
- [ ] Synthesis follows On-chain snapshot / Signals / Risks / Sources.
- [ ] If news used, both calls cited.
