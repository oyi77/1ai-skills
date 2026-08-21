---
name: gate-news-intel
description: Use when crypto news / events / UGC intelligence on Gate.io — latest news, event calendars, and market-wide intel via gate-cli; optional info overlay for market context. Use when working with gate news intelligence.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
  - gate
  - news
  - intel
  - crypto
  - events
  - sentiment
version: 1.0.0
category: research
---

## Overview

`gate-news-intel` runs **news / events / UGC intelligence playbooks** through `gate-cli` (official Gate.io skills CLI). It maps a news intent to the news playbook set, gathers signals via `gate-cli news` (and optionally `gate-cli info` for market context), and synthesizes a structured intelligence brief.

> **Note on prefix**: this is `gate-news-intel` (NOT `gate-info-news-intel` — that id does not exist upstream). The news playbooks are a distinct family from the `gate-info-*` research/risk/web3 family.

Two news playbooks ship with `gate-cli >= 0.7.6`:

| Intent | Playbook | Core gate-cli call |
|---|---|---|
| Latest news + events | `news_intel` | `news +[coin]` or `news +market` |
| News + market context | `intel_plus_market` / `market_wide_intel` | `news +[coin]` then `info +[coin]` |

> **Upstream dependency**: `gate-cli` and shared `info-news-runtime-rules.md` live in `gate/gate-skills` (GitHub). This skill is a portable command + synthesis reference — `gate-cli` must be installed and authenticated. Piping third-party install scripts to bash is out of scope (see Anti-Rationalization).

## When to Use

- "Latest crypto news" / "what happened with [coin]"
- "Upcoming events / catalysts for [coin]"
- "Market-wide sentiment right now"
- "News + market context for [coin]"

## When NOT to Use

- You want to execute a trade — use `gate-exchange-trading`.
- You want deep on-chain research — use `gate-info-research` / `gate-info-web3`.
- You want a plain price quote — `info +[coin]` is enough; do not invoke a news playbook.
- Non-Gate.io scoped assets.

## Workflow

### Step 0 — Preflight

```bash
gate-cli info --preflight
# Legacy: gate-cli check-info-env
```

### Step 1 — Route intent

| User says | Playbook | Command |
|---|---|---|
| "news [coin]" / "events [coin]" | `news_intel` | `news +[coin]` |
| "market-wide news" | `news_intel` | `news +market` |
| "news + market [coin]" | `intel_plus_market` | `news +[coin]` then `info +[coin]` |

### Step 2 — Collect

```bash
gate-cli news +BTC --limit 10 --format json
gate-cli info +BTC --format json   # intel_plus_market context
```

### Step 3 — Synthesize

```
## News Intel: [target]  (playbook: news_intel | intel_plus_market)
### Headlines
- Top 3–5 items with timestamp + source
### Events / Catalysts
- Upcoming dated events
### Market context
- (if used) price/volume backdrop from info
### Sentiment
- Bullish / bearish / mixed + why
### Sources
- gate-cli news +[target] (json), gate-cli info (if used)
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "No info module, news is incomplete" | `intel_plus_market` exists; for plain `news_intel` info is optional. State scope. |
| "One headline = market sentiment" | Aggregate multiple items; a single story is not a sentiment read. |
| "Pipe the install script to bash" | Out-of-repo scripts fail (HTTP 566 observed) and are a supply-chain risk. Use documented `gate-cli` channel. |
| "UGC = verified fact" | Treat UGC/social as signal, not proof. Label source type. |

## Code Example

```bash
gate-cli news +BTC --limit 5 --format json | jq '.[].title'
# → ["Gate.io lists new BTC pairs","ETF inflows resume",...]
gate-cli info +BTC --format json | jq '{price, change_24h}'
```

## Verification

- [ ] `gate-cli info --preflight` passes.
- [ ] Intent mapped to exactly one news playbook.
- [ ] Output uses `--format json`.
- [ ] Synthesis follows Headlines / Events / Sentiment / Sources.
- [ ] If info used, both calls cited.
