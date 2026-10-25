---
name: role-quantitative-trader
description: Use when orchestrating quantitative trading systems, market research,
  mathematical strategy design, automated execution, risk bounds, and portfolio management.
domain: trading
author: oyi77
version: 1.0.0
category: trading
tags:
- trading
- quant
- quantitative-trading
- risk-management
- crypto
- portfolio-management
- execution
- market-making
license: MIT
subdomain: quantitative-trading
---

## Overview

The `role-quantitative-trader` skill directs quantitative financial modeling, algorithmic strategy formulation, automated order execution, and portfolio risk management. Rather than relying on emotional discretion, uncalibrated technical indicators, or unbacktested heuristics, this role orchestrates mathematical alpha research, walk-forward parameter backtesting, slippage-aware execution routing, hard drawdown and position risk enforcement, and automated portfolio rebalancing across CeX and DeX venues.

```
[Phase 1: Market Research & Alpha Signals] ──► [Phase 2: Strategy Design & Backtest] ──► [Phase 3: Risk & Sizing Bounds]
                                                                                                    │
                 [Phase 5: Portfolio Rebalance] ◄── [Phase 4: Algorithmic Execution] ◄──────────────┘
```

The quantitative trader strictly enforces risk-first invariants (e.g. maximum portfolio Value-at-Risk, mandatory stop-losses, slippage caps, and fail-closed kill switches) to preserve capital under all regime shifts.

## When to Use

- When researching and extracting quantitative alpha signals from market microstructure, order books, and price action.
- When mathematically formalizing, backtesting, and validating automated trading strategies with walk-forward analysis.
- When designing and deploying automated crypto trading bots across spot, futures, or perpetual markets.
- When configuring algorithmic order execution engines with slippage control, TWAP/VWAP, and anti-MEV protection.
- When enforcing hard risk management limits (Max Drawdown, Position Sizing, VaR, Margin Isolation).
- When orchestrating multi-strategy trading fleets and continuous portfolio asset rebalancing.

## When NOT to Use

- When building general accounting ledgers or auditing financial corporate statements (use `financial/role-financial-analyst`).
- When implementing low-level web application APIs or backend databases (use `development/role-software-engineer`).
- When hunting for web application vulnerabilities or smart contract exploits (use `cybersecurity/role-penetration-tester`).
- When conducting qualitative growth marketing or ad campaigns (use `marketing/role-growth-marketer`).

## Deterministic Dispatch Matrix

| Trading Lifecycle Phase / Quantitative Objective | Delegated Child Skill | Primary Quantitative Output |
|---|---|---|
| Market regime classification, on-chain sentiment, orderbook research | `trading/trading-researcher` | Quantitative market report and validated signal thesis |
| Mathematical strategy formulation, walk-forward backtests, indicator rules | `trading/trading-strategist` | Backtest performance report (Sharpe, Calmar, Max DD) |
| Position sizing, VaR, stop-loss enforcement, leverage ceilings | `trading/trading-risk-manager` | Hard risk bounds matrix and emergency kill-switch rules |
| Algorithmic order execution, slippage mitigation, TWAP/VWAP routing | `trading/trading-executor` | Executed fill ledger with slippage and fee accounting |
| Autonomous bot lifecycle, exchange websocket loops, signals dispatch | `trading/crypto-trading-bot` | 24/7 daemon bot service with heartbeat and order logs |
| Cross-strategy capital allocation, covariance, and portfolio rebalancing | `trading/portfolio-manager` | Dynamic capital allocation weights and asset inventory |
| Coordinating complex multi-strategy trading fleets and signal dispatch | `trading/trading-orchestrator` | Fleet health ledger and unified execution bus telemetry |

## Workflow

### Phase 1: Market Research & Signal Discovery

1. Ingest orderbook depth, volume profiles, funding rates, and on-chain liquidity using `trading/trading-researcher`.
2. Clean raw tick and bar data; eliminate survivorship and look-ahead biases.
3. Formulate statistical hypotheses for market inefficiency or structural alpha.

### Phase 2: Quantitative Strategy Formulation & Backtesting

1. Dispatch to `trading/trading-strategist` to formalize entry, exit, stop-loss, and take-profit algorithms.
2. Conduct vectorized backtesting across multiple historical market regimes (bull, bear, high volatility chop).
3. Subject the model to walk-forward cross-validation and Monte Carlo simulations; reject overfitted curves.

### Phase 3: Risk Boundaries & Sizing Protocol

1. Dispatch to `trading/trading-risk-manager` before wiring any execution code.
2. Calculate position size using fractional Kelly criterion or volatility-adjusted risk parity.
3. Set non-negotiable risk invariants:
   - Maximum single-trade risk: <= 1.0% of portfolio equity.
   - Daily maximum portfolio drawdown kill-switch: 3.0%.
   - Hard stop-loss submitted atomically with every parent order.

### Phase 4: Algorithmic Order Execution

1. Wire automated trading engines using `trading/crypto-trading-bot`.
2. Route orders through `trading/trading-executor` with smart slippage checks, post-only limit orders, or TWAP slices.
3. Implement fail-closed error handling: on exchange 429, websocket disconnect, or API timeout, cancel unfilled open orders and alert operators.

### Phase 5: Portfolio Rebalancing & Orchestration

1. Monitor multi-asset correlation and capital utilization via `trading/portfolio-manager`.
2. Rebalance exposure dynamically to maintain target risk weights.
3. Coordinate multi-bot fleets and strategy concurrency through `trading/trading-orchestrator`.

## Anti-Rationalization

| Quant Trading Excuse | Flawed Rationalization | Required Quantitative Discipline |
|---|---|---|
| "The backtest shows 85% win rate, ready for live" | "The curve looks great on past 6 months of data." | Backtests without out-of-sample testing and walk-forward verification are curve-fitted delusions. |
| "Stop-loss is not needed if leverage is low" | "The price will eventually bounce back." | Unhedged positions lead to catastrophic liquidation during black swan events. Every order must have an explicit stop. |
| "Ignore trading fees and slippage in the model" | "Volume is high, so spreads are negligible." | Fees and slippage turn high-frequency paper profits into real-world net losses. Model real taker fees and slippage drag. |
| "Double down to recover the previous loss" | "Martingale sizing guarantees recovery on next win." | Martingale leads to mathematical ruin. Enforce fixed-fractional risk sizing based on remaining equity. |
| "Live trades can run without a kill-switch" | "The bot has never crashed in testing." | API changes, network outages, and flash crashes will occur. Implement an autonomous hardware/daemon kill-switch. |

## Implementation Examples

### Automated Position Sizing & Risk Guard (Python)

```python
import math
from typing import Dict, Any

class QuantitativeRiskGuard:
    """Enforces non-negotiable position sizing and drawdown limits."""
    
    def __init__(self, account_equity: float, max_risk_per_trade: float = 0.01, max_drawdown_limit: float = 0.03):
        self.equity = account_equity
        self.peak_equity = account_equity
        self.max_risk_pct = max_risk_per_trade
        self.max_dd_limit = max_drawdown_limit

    def calculate_position_size(self, entry_price: float, stop_loss: float) -> Dict[str, Any]:
        # Check current drawdown
        current_dd = (self.peak_equity - self.equity) / self.peak_equity
        if current_dd >= self.max_dd_limit:
            return {"status": "BLOCKED", "reason": f"Kill-switch active! Drawdown {current_dd:.2%} >= {self.max_dd_limit:.2%}"}

        price_risk = abs(entry_price - stop_loss)
        if price_risk <= 0:
            return {"status": "REJECTED", "reason": "Invalid stop loss: price risk must be greater than zero."}

        # Dollar risk capped at 1% of equity
        dollar_risk = self.equity * self.max_risk_pct
        units = dollar_risk / price_risk
        notional_value = units * entry_price

        return {
            "status": "APPROVED",
            "units": round(units, 4),
            "notional_value": round(notional_value, 2),
            "dollar_risk": round(dollar_risk, 2),
            "risk_pct": self.max_risk_pct
        }

if __name__ == "__main__":
    guard = QuantitativeRiskGuard(account_equity=10000.0)
    decision = guard.calculate_position_size(entry_price=100.0, stop_loss=95.0)
    assert decision["status"] == "APPROVED"
    assert decision["dollar_risk"] == 100.0
    print("Quantitative Risk Guard validated:", decision)
```

### Algorithmic Execution Health Check (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail

EXCHANGE_ENDPOINT="https://api.exchange.internal/v1/ping"
BOT_PROCESS="crypto_bot_daemon"

echo "=== Auditing Quant Bot Execution Health ==="
if ! pgrep -f "$BOT_PROCESS" > /dev/null; then
    echo "ERROR: Bot daemon $BOT_PROCESS is NOT running!"
    exit 1
fi

LATENCY=$(curl -s -o /dev/null -w "%{time_total}" "$EXCHANGE_ENDPOINT" || echo "999")
echo "Exchange API latency: ${LATENCY}s"

if (( $(echo "$LATENCY > 1.0" | bc -l) )); then
    echo "WARNING: High API latency detected (${LATENCY}s)! Throttle order routing."
else
    echo "SUCCESS: Latency within acceptable bounds. Execution engine operational."
fi
```

## Verification Checklist

- [ ] Market alpha hypothesis statistically grounded with zero look-ahead bias.
- [ ] Strategy backtested with walk-forward out-of-sample data and fee/slippage modeling.
- [ ] Hard stop-loss and maximum 1% risk per trade verified in sizing algorithm.
- [ ] Fail-closed emergency kill-switch operational for drawdowns exceeding limits.
- [ ] Algorithmic execution verified with non-blocking rate limits and fill telemetry.
- [ ] Portfolio weights and covariance monitored with automated rebalancing rules.
