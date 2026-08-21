---
name: gate-info-research
description: Use when deep crypto market + on-chain research on Gate.io — single or multi-coin analysis, market overview, trend, macro, and research-plus-news playbooks via gate-cli. Use when working with gate crypto research.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
  - gate
  - info
  - research
  - crypto
  - market-analysis
  - on-chain
version: 1.0.0
category: research
---

## Overview

`gate-info-research` runs **research-grade crypto investigation playbooks** through `gate-cli` (the official Gate.io skills CLI). It maps a natural-language research intent to one of six `info` playbooks, gathers the data via `gate-cli info` (and optionally `gate-cli news` for context), and synthesizes a structured finding.

Six playbooks ship with `gate-cli >= 0.7.6`:

| Intent | Playbook | Core gate-cli call |
|---|---|---|
| Single coin deep dive | `single_coin` | `info +[coin]` |
| Whole-market snapshot | `market_overview` | `info +market` |
| Compare several coins | `multi_coin` | `info +[coin1] +[coin2] ...` |
| Trend / momentum read | `trend` | `info +trend` |
| Macro driver analysis | `macro` | `info +macro` |
| Research + news overlay | `research_plus_news` | `info +[coin]` then `news +[coin]` |

> **Upstream dependency**: `gate-cli` and the shared playbook YAMLs live in `gate/gate-skills` (GitHub). This skill is a portable reference for the **commands and synthesis patterns** — you still need `gate-cli` installed and authenticated. Piping random install scripts to bash is out of scope here (see Anti-Rationalization).

## When to Use

- "Research BTC / analyze ETH / look into SOL"
- "Give me a market overview / what's moving today"
- "Compare these 3 coins: LINK, ARB, OP"
- "What's the macro backdrop for crypto right now"
- "Trend analysis for [coin]" / "is [coin] trending up"
- "Research [coin] and also pull recent news"

## When NOT to Use

- You want to **execute** a trade — use `gate-exchange-trading` (separate skill).
- You want wallet / on-chain fund tracing — use `gate-dex-wallet` or `gate-info-web3`.
- You only need a price quote — a simple `info +[coin]` call is enough; do not invoke the full playbook.
- Gate.io is not the exchange in question (playbooks are Gate.io-scoped).

## Workflow

### Step 0 — Preflight

```bash
# Modern shortcut (>= 0.7.6)
gate-cli info --preflight

# Legacy fallback (<= 0.5.2)
gate-cli check-info-env
```

Resolve any missing API keys / `gate-cli` version before proceeding.

### Step 1 — Route intent to playbook

| User says | Playbook | Command |
|---|---|---|
| "研究 BTC" / "analyze ETH" | `single_coin` | `info +BTC` |
| "市场概览" / "market overview" | `market_overview` | `info +market` |
| "对比 LINK ARB OP" | `multi_coin` | `info +LINK +ARB +OP` |
| "趋势分析" / "trend" | `trend` | `info +trend` |
| "宏观" / "macro" | `macro` | `info +macro` |
| "研究 + 新闻" | `research_plus_news` | `info +BTC` then `news +BTC` |

### Step 2 — Collect data

Always request structured output for research aggregation:

```bash
gate-cli info +BTC --format json
gate-cli info +market --format json
gate-cli news +BTC --limit 10 --format json   # for research_plus_news
```

### Step 3 — Synthesize

Produce the finding in this shape:

```
## Research: [coin]  (playbook: single_coin)
### Snapshot
- Price / 24h change / volume / rank
- Key on-chain or supply signals
### Narrative
- 2–4 sentences tying the data to a thesis
### Risks
- What would invalidate the thesis
### Sources
- gate-cli info +[coin] (json), gate-cli news +[coin] (if used)
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "No news module, so research is incomplete" | `research_plus_news` exists; for other playbooks, news is optional context, not required. State the scope. |
| "Missing data = low quality coin" | Absent fields are gaps to flag, not a verdict. Report what's missing. |
| "I'll pipe the install script to bash to get it working" | Out-of-repo install scripts fail (HTTP 566 observed) and are a supply-chain risk. Install `gate-cli` through its documented channel only. |
| "One price call is enough for a deep dive" | `single_coin` aggregates multiple signals; a bare quote is not a research playbook. |

## Code Example

Run a single-coin research playbook and capture structured output:

```bash
gate-cli info +BTC --format json | jq '{price, change_24h, volume, rank}'
# → {"price": 64000, "change_24h": -1.2, "volume": 28000000, "rank": 1}
gate-cli news +BTC --limit 5 --format json | jq '.[].title'
```

## Verification

- [ ] `gate-cli info --preflight` passes (no missing keys / version error).
- [ ] Intent mapped to exactly one playbook from the routing table.
- [ ] Data collected with `--format json` (machine-parseable).
- [ ] Output follows the Synthesis template (Snapshot / Narrative / Risks / Sources).
- [ ] If news was used, both `info` and `news` calls are cited in Sources.
