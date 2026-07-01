---
name: investing-algorithm-framework
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