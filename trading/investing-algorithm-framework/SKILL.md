---
name: investing-algorithm-framework
version: "2.0.0"
description: Build algorithmic investing strategies with backtesting, signal generation, and portfolio optimization frameworks. Use when building algorithmic investing strategies with backtesting, signal generation, and portfolio.
domain: trading
tags:
- algorithm
- algorithms
- framework
- investing
- markets
- testing
- trading
- money
---
## Overview

Full quantitative trading framework based on [coding-kitties/investing-algorithm-framework](https://github.com/coding-kitties/investing-algorithm-framework). Python-native workflow covering strategy definition, vectorized backtesting, event-driven simulation, Monte Carlo robustness testing, and live deployment to CCXT exchanges.

```bash
pip install investing-algorithm-framework
```

## Strategy Definition

Define trading strategies by subclassing `TradingStrategy`. Each strategy declares symbols, data sources, and signal logic.

```python
from investing_algorithm_framework import TradingStrategy, OrderSide

class MomentumStrategy(TradingStrategy):
    symbols = ["BTC/USDT", "ETH/USDT"]
    data_sources = ["ohlcv:1h"]
    
    def buy_signal(self, symbol, data):
        return data["close"].iloc[-1] > data["close"].rolling(20).mean().iloc[-1]
    
    def sell_signal(self, symbol, data):
        return data["close"].iloc[-1] < data["close"].rolling(20).mean().iloc[-1]
    
    def position_size(self, symbol, portfolio):
        return portfolio.available_capital * 0.1
    
    def stop_loss(self, symbol, entry_price):
        return entry_price * 0.95  # 5% stop loss
    
    def take_profit(self, symbol, entry_price):
        return entry_price * 1.15  # 15% take profit
```

**Key components**:
- `symbols`: List of trading pairs to monitor
- `data_sources`: OHLCV timeframes or custom data feeds
- `buy_signal` / `sell_signal`: Boolean signal functions
- `position_size`: Risk-based position sizing
- `stop_loss` / `take_profit`: Risk management levels

## Vectorized Backtesting

Polars-powered vectorized backtesting for rapid iteration. Test thousands of parameter combinations in seconds.

```python
from investing_algorithm_framework import Backtest

backtest = Backtest(
    strategy=MomentumStrategy,
    start_date="2023-01-01",
    end_date="2024-01-01",
    initial_capital=10000,
)

# Parameter sweeps
results = backtest.optimize(
    params={
        "lookback_period": range(10, 50, 5),
        "stop_loss_pct": [0.02, 0.05, 0.10],
    },
    metric="sharpe_ratio",
)

# Multi-window robustness checks
robustness = backtest.walk_forward(
    train_window="180D",
    test_window="30D",
    step="30D",
)
```

**Capabilities**:
- Polars DataFrames for speed (orders of magnitude faster than loop-based)
- Parameter sweeps across arbitrary dimensions
- Walk-forward analysis with configurable train/test windows
- Out-of-sample validation built into the workflow

## Event-Driven Backtesting

Bar-by-bar simulation with realistic fill models. Closer to live trading conditions.

```python
backtest = Backtest(
    strategy=MomentumStrategy,
    mode="event_driven",
    slippage_model="percentage",  # or "fixed", "volume_based"
    slippage_pct=0.001,
    fill_model="realistic",       # accounts for partial fills
    commission_pct=0.001,
)
```

**Features**:
- Bar-by-bar processing (no lookahead bias)
- Configurable slippage models (percentage, fixed, volume-based)
- Realistic fill simulation with partial fills
- Commission modeling per exchange fee structure

## Backtest Reports

HTML dashboard reports with full performance visualization.

```python
report = backtest.run()
report.save_html("backtest_report.html")
```

**Report contents**:
- Equity curve with benchmark comparison
- Drawdown chart (depth, duration, recovery)
- Monthly returns heatmap
- Trade log with entry/exit details
- Risk metrics summary table
- Rolling Sharpe ratio chart

## Storage System

Three-tier storage architecture for efficient data management.

- **Tier 1 — SQLite Index**: Metadata, trade logs, portfolio snapshots. Fast queries.
- **Tier 2 — Swappable Adapters**: Pluggable storage backends (local disk, S3, database). Swap without code changes.
- **Tier 3 — Content-Addressed OHLCV Dedup**: Hash-based deduplication of OHLCV data. Same candle data stored once regardless of how many strategies reference it.

## Live Trading

Deploy strategies to live exchanges via CCXT integration.

```python
from investing_algorithm_framework import LiveTrader

trader = LiveTrader(
    strategy=MomentumStrategy,
    exchange="binance",
    api_key="...",
    api_secret="...",
    dry_run=True,  # paper trade first
)

trader.start()
```

**Exchange support**:
- All CCXT-supported exchanges (Binance, Bybit, Kraken, Coinbase, etc.)
- Custom `OrderExecutor` for non-CCXT venues
- Serverless deployment: AWS Lambda, Azure Functions scheduled triggers
- Built-in reconnect logic and error handling

## Cross-Sectional Pipelines

Rank, filter, and score entire symbol universes — not just individual pairs.

```python
class UniverseStrategy(TradingStrategy):
    universe = "top_100_crypto"
    
    def rank(self, symbols, data):
        # Rank by 7-day momentum
        return sorted(symbols, key=lambda s: data[s]["close"].pct_change(7).iloc[-1], reverse=True)
    
    def filter(self, ranked_symbols, data):
        # Only trade top 10
        return ranked_symbols[:10]
    
    def score(self, symbol, data):
        # Position size by conviction
        return data[symbol]["volume"].iloc[-1] / data[symbol]["volume"].rolling(30).mean().iloc[-1]
```

## Monte Carlo Testing

Statistical robustness checks — does the strategy survive random perturbations?

```python
mc_results = backtest.monte_carlo(
    simulations=1000,
    perturbation="trade_order",   # shuffle trade sequence
    confidence_interval=0.95,
)

print(mc_results.percentile_5)   # worst 5% outcome
print(mc_results.percentile_95)  # best 5% outcome
print(mc_results.probability_of_ruin)
```

## MCP Server

AI agents can query backtest results via the built-in MCP server. Enables agent-driven strategy iteration.

## Performance Metrics

30+ metrics computed automatically:

| Category | Metrics |
|----------|---------|
| Return | CAGR, total return, annualized return |
| Risk-Adjusted | Sharpe ratio, Sortino ratio, Calmar ratio |
| Risk | Max drawdown, VaR, CVaR, volatility |
| Efficiency | Win rate, profit factor, avg win/loss ratio |
| Activity | Total trades, avg holding period, turnover |

## When to Use
**Trigger phrases:**
- "investing algorithm framework"
- "Build algorithmic investing strategies with backtesting, signal generation, and "


- Developing and backtesting quantitative trading strategies
- Optimizing strategy parameters across multiple dimensions
- Validing strategy robustness with Monte Carlo simulation
- Deploying strategies to live exchanges
- Building cross-sectional ranking and selection systems
- Generating professional backtest reports for review


## When NOT to Use

- When you cannot afford to lose the capital at risk
- For instruments you do not understand
- When emotional state impairs judgment (revenge trading, FOMO)


## Red Flags

- Backtest uses future data (lookahead bias in signal generation)
- Strategy overfit to training data (Sharpe collapses out-of-sample)
- Monte Carlo probability of ruin exceeds 5% threshold
- Live trading not running dry-run paper trade first
- Slippage and commission not modeled in backtest (overly optimistic results)

## Verification

After completing strategy development, confirm:

- [ ] Strategy defined with clear entry/exit rules and position sizing
- [ ] Backtest covers minimum 2 years of historical data
- [ ] Walk-forward analysis shows consistent out-of-sample performance
- [ ] Monte Carlo simulation run with 1000+ iterations
- [ ] Live deployment starts with dry_run=True paper trading

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will cut losses later" | Later never comes. Set stop-losses before entering any trade. |
| "This time is different" | It never is. Follow your strategy, not your emotions. |
| "I do not need to journal" | Journaling reveals patterns in your behavior. Track every trade. |

## Money-Making Overview

Deploy quantitative strategies that generate consistent alpha. This framework enables algorithmic trading with $100K-$10M AUM targeting 15-30% annualized returns through systematic backtesting, Monte Carlo robustness validation, and live execution. The same engine powers a consulting revenue stream via strategy development, backtesting audits, and signal subscriptions — turning quantitative skill into a diversified income portfolio.

## Revenue Streams

| Stream | Description | Target Income |
|--------|-------------|---------------|
| **Live Algo Trading** | Deploy verified strategies to CCXT exchanges. Capital at risk; requires dry-run validation first. | 15-30% annualized on $100K-$10M AUM |
| **Strategy-as-a-Service** | Build and manage custom strategies for hedge funds, family offices, or crypto funds. Includes parameter optimization, walk-forward analysis, and monthly rebalancing. | $500-$5,000/month per client |
| **Backtesting Audits** | Audit existing strategies for lookahead bias, overfitting, survivorship bias, and realistic slippage/commission modeling. Deliver HTML report with Monte Carlo results. | $200-$2,000 per project |
| **Signal Subscription** | Run strategies serverless (AWS Lambda, scheduled triggers), push BUY/SELL signals via webhook or Telegram. Tiered by number of pairs and update frequency. | $50-$500/month per subscriber |
| **Education & Courses** | Sell the backtesting framework as a course or workshop — strategy definition, parameter optimization, walk-forward analysis, live deployment. | $500-$2,000 per student |

## First Action in 60 Minutes

Run this script to implement a simple SMA crossover strategy, backtest on SPY data, and get a trade-ready signal in under 60 minutes. It validates the full pipeline: data acquisition, signal generation, backtesting, and performance reporting.

```python
"""
sma_crossover_backtest.py — SMA Crossover strategy that generates cash.

What this does:
1. Downloads 3 years of daily SPY data via yfinance
2. Computes 50/200 SMA crossover signals
3. Backtests with 0.1% slippage + commission
4. Prints equity curve, Sharpe ratio, max drawdown
5. Outputs a trade-ready signal for TOMORROW
6. Saves HTML report to sma_crossover_report.html

Run:  pip install yfinance pandas investing-algorithm-framework && python sma_crossover_backtest.py
Exit: $5-$10 potential on first trade if signal is BUY and price moves 0.1%
"""

import yfinance as yf
import pandas as pd
from investing_algorithm_framework import Backtest, TradingStrategy, OrderSide


class SmaCrossoverStrategy(TradingStrategy):
    """Classic 50/200 SMA crossover — the 'hello world' of quant trading."""

    symbols = ["SPY"]
    data_sources = ["ohlcv:1d"]

    def buy_signal(self, symbol, data):
        fast = data["close"].rolling(50).mean()
        slow = data["close"].rolling(200).mean()
        return fast.iloc[-2] <= slow.iloc[-2] and fast.iloc[-1] > slow.iloc[-1]

    def sell_signal(self, symbol, data):
        fast = data["close"].rolling(50).mean()
        slow = data["close"].rolling(200).mean()
        return fast.iloc[-2] >= slow.iloc[-2] and fast.iloc[-1] < slow.iloc[-1]

    def position_size(self, symbol, portfolio):
        return portfolio.available_capital * 0.95  # 95% allocation per signal

    def stop_loss(self, symbol, entry_price):
        return entry_price * 0.93  # 7% stop loss

    def take_profit(self, symbol, entry_price):
        return entry_price * 1.20  # 20% take profit


if __name__ == "__main__":
    print("=" * 60)
    print("SMA CROSSOVER BACKTEST — 3 Years SPY Data")
    print("=" * 60)

    backtest = Backtest(
        strategy=SmaCrossoverStrategy,
        start_date="2023-01-01",
        end_date="2026-01-01",
        initial_capital=100_000,
        mode="event_driven",
        slippage_model="percentage",
        slippage_pct=0.001,
        commission_pct=0.001,
    )

    report = backtest.run()

    print(f"\n{'RESULTS':-^60}")
    print(f"CAGR:                {report.metrics.cagr:>8.2%}")
    print(f"Total Return:        {report.metrics.total_return:>8.2%}")
    print(f"Sharpe Ratio:        {report.metrics.sharpe_ratio:>8.2f}")
    print(f"Sortino Ratio:       {report.metrics.sortino_ratio:>8.2f}")
    print(f"Max Drawdown:        {report.metrics.max_drawdown:>8.2%}")
    print(f"Win Rate:            {report.metrics.win_rate:>8.2%}")
    print(f"Profit Factor:       {report.metrics.profit_factor:>8.2f}")
    print(f"Total Trades:        {report.metrics.total_trades:>8d}")

    # Monte Carlo robustness check
    mc = backtest.monte_carlo(simulations=500, confidence_interval=0.95)
    print(f"\n{'MONTE CARLO (500 sims)':-^60}")
    print(f"5th Percentile:       ${mc.percentile_5:>8,.2f}")
    print(f"95th Percentile:      ${mc.percentile_95:>8,.2f}")
    print(f"Prob of Ruin:         {mc.probability_of_ruin:>8.2%}")

    # Trade-ready signal for next day
    data = yf.download("SPY", period="1y", interval="1d")["Close"]
    fast = data.rolling(50).mean()
    slow = data.rolling(200).mean()
    signal = "BUY" if fast.iloc[-1] > slow.iloc[-1] else "SELL"
    print(f"\n{'NEXT SIGNAL':-^60}")
    print(f"  50 SMA: {fast.iloc[-1]:>8.2f}  |  200 SMA: {slow.iloc[-1]:>8.2f}")
    print(f"  >>> {signal} SPY at next market open <<<")

    report.save_html("sma_crossover_report.html")
    print(f"\nHTML report saved to sma_crossover_report.html")
    print("=" * 60)
```

## Output Format

Every strategy run — whether backtest or live — MUST produce this standardized output:

```yaml
strategy_name: "<Python class name>"
status: "backtested" | "live" | "paper"
timeframe: "<start_date> → <end_date>"
metrics:
  cagr: "<percent>"
  sharpe_ratio: "<float>"
  sortino_ratio: "<float>"
  max_drawdown: "<percent>"
  win_rate: "<percent>"
  profit_factor: "<float>"
  total_trades: "<int>"
  monte_carlo_5th_pct: "<dollar>"
  monte_carlo_95th_pct: "<dollar>"
  prob_of_ruin: "<percent>"
next_signal:
  symbol: "<ticker>"
  direction: "BUY" | "SELL" | "HOLD"
  entry_price: "<dollar>"
  conviction: "<low | medium | high>"
target_allocation: "<percent of portfolio>"
```