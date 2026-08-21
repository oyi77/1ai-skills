---
name: gate-exchange-trading
description: "Use when executing trades on Gate.io Spot & Futures markets using CCXT/SDK or gate-cli. Triggers on spot buying, margin borrowing, orderbook depth checks, futures position management, or subaccount trade routing."
domain: trading
author: oyi77
license: Apache-2.0
subdomain: trading
tags:
  - gate
  - exchange
  - spot
  - futures
  - trading
version: 1.0.0
category: trading
---

## Overview

Gate Exchange Trading provides unified procedures for executing Spot, Margin, and USDT Perpetual Futures trades on Gate.io. It integrates with both the native SDK (Python/Node.js) and the `gate-cli` binary. This skill outlines risk checks, order drafting, confirmation gates, and post-state verification to prevent double-fills and margin liquidations.

## When to Use

**Trigger phrases:**
- "gate-exchange-trading", "Execute order on Gate.io"
- "futures position gate.io", "check open orders Gate"
- "margin borrow Gate exchange", "spot buy BTC on gate"

**Situations:**
- Executing spot limit/market orders and managing order books on Gate.io.
- Opening, closing, or managing leverage/margins on USDT perpetual futures contracts.
- Auditing balance requirements and performing pre-trade risk grading (GO, CAUTION, BLOCK) before order entry.

## When NOT to Use

- Task is about on-chain Gate DEX or GateChain EVM trading (use `gate-dex-wallet`).
- Task is about news analysis without active trading intent (use `social-intelligence` or `scrapers`).
- Task requires fully automated trading without user confirmation gates (bypasses safety rules).

## Operational Workflow

### Step 1: Pre-trade Risk Check (Briefing)
Before submitting any order, calculate the risk envelope.
```python
import os
from gate_api import ApiClient, Configuration, SpotApi

config = Configuration(
    key=os.getenv("GATE_API_KEY"),
    secret=os.getenv("GATE_API_SECRET")
)
api_client = ApiClient(config)
spot_api = SpotApi(api_client)

# Check spot account balance
balances = spot_api.list_spot_accounts()
```

### Step 2: Produce Order Draft
Specify symbol, order direction (buy/sell), price type, and size.

### Step 3: Confirmation and Execution
Verify user has explicitly confirmed the `Order Draft` in the immediately preceding turn. Run execution commands:
```bash
gate-cli cex spot order create --symbol BTC_USDT --side buy --amount 0.001 --price 65000 --type limit
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll store the API keys in plain text in config settings" | Configuration values slip into logs, backups or git. Keys belong strictly in `GATE_API_KEY` / `GATE_API_SECRET` environments. |
| "I can skip the confirmation gate for market close orders" | A market close during high volatility without confirmation can incur large slippage losses. User approval is always mandatory. |
| "I don't need to query account balance before placing a limit order" | Placing orders that fail for insufficient balance wastes RPC limits and disrupts agent workflow continuity. Check balances first. |

## Verification

### Verification Checklist
- [ ] Account balance checks return clean JSON before drafting
- [ ] CCXT / Gate V4 Api client registers with valid environment key pair
- [ ] CLI command `gate-cli --version` resolves successfully on PATH
- [ ] Pre-trade Trading Brief produces explicit indicator (`GO`, `CAUTION`, or `BLOCK`)

## Process

1. **Classify task mode** - Trade decision vs Trade draft + execute vs position management.
2. **Collect target details** - asset, direction, market type (spot vs futures).
3. **Build pre-trade brief** - check balance, calculate risk limits.
4. **Draft order** - produce JSON/Markdown layout of the intended trade.
5. **Request confirmation** - get explicit user go-signal.
6. **Execute trade** - invoke api/cli endpoint.
7. **Post-execution read** - verify fills and status.
