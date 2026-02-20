# Trading Strategy Templates

Comprehensive documentation for all trading strategy templates available in the 1ai-skills trading system. This guide covers strategies across FOREX, CRYPTO, STOCKS, and COMMODITY markets.

## Table of Contents

- [Introduction](#introduction)
- [FOREX Strategies](#forex-strategies)
  - [Holy Grail Strategy](#holy-grail-strategy)
  - [Momentum Elder Strategy](#momentum-elder-strategy)
  - [Kumo Breakout Strategy](#kumo-breakout-strategy)
- [CRYPTO Strategies](#crypto-strategies)
  - [Funding Reversal Strategy](#funding-reversal-strategy)
  - [Volume Momentum Strategy](#volume-momentum-strategy)
- [STOCKS Strategies](#stocks-strategies)
  - [Golden Cross Strategy](#golden-cross-strategy)
  - [RSI Divergence Strategy](#rsi-divergence-strategy)
- [COMMODITY Strategies](#commodity-strategies)
  - [Gold Silver Ratio Strategy](#gold-silver-ratio-strategy)
  - [Seasonal Strategy](#seasonal-strategy)
- [Performance Summary](#performance-summary)
- [Usage Examples](#usage-examples)

## Introduction

This document provides detailed documentation for all trading strategy templates implemented in the system. Each strategy is designed for specific market conditions and asset classes. All strategies follow the base strategy interface and can be used with the backtesting engine, paper trading, and live trading modes.

Strategies are organized by market type to help you quickly find the appropriate strategy for your trading needs. Each strategy includes a description of its trading approach, configurable parameters, example usage code, and performance characteristics.

## FOREX Strategies

FOREX strategies are optimized for currency pair trading with focus on major pairs (EUR/USD, GBP/USD, USD/JPY) and cross pairs. These strategies account for the 24-hour market structure and high liquidity typical of foreign exchange markets.

### Holy Grail Strategy

The Holy Grail strategy is a multi-timeframe trend-following approach that combines moving average crossovers with momentum confirmation. It identifies high-probability trend entries by waiting for alignment across multiple timeframes before generating signals.

**Description**: This strategy uses a combination of fast and slow exponential moving averages (EMA) to identify trend direction. Entry signals are generated when the fast EMA crosses above the slow EMA on the higher timeframe, with additional confirmation from the RSI momentum indicator. The strategy aims to capture major trend moves while avoiding whipsaw trades in ranging markets.

**Parameters**:
- `fast_ema_period`: Fast EMA period for trend identification (default: 12)
- `slow_ema_period`: Slow EMA period for trend identification (default: 26)
- `rsi_period`: RSI period for momentum confirmation (default: 14)
- `rsi_overbought`: RSI overbought threshold (default: 70)
- `rsi_oversold`: RSI oversold threshold (default: 30)
- `higher_timeframe`: Higher timeframe for trend confirmation (default: "H4")
- `atr_period`: ATR period for stop loss calculation (default: 14)
- `atr_multiplier`: Multiplier for ATR-based stop loss (default: 2.0)

**Example Usage**:
```python
from trading.strategy.tradfi.forex.holy_grail.strategy import HolyGrailStrategy

# Create strategy instance with custom parameters
strategy = HolyGrailStrategy(
    fast_ema_period=12,
    slow_ema_period=26,
    rsi_period=14,
    higher_timeframe="H4"
)

# Get signals from OHLCV data
signals = strategy.get_signals(ohlcv_data)

# Run backtest
from trading.backtest.engine import BacktestEngine
engine = BacktestEngine(strategy)
metrics = engine.run(ohlcv_data)
```

**Performance Notes**: This strategy performs best in strong trending markets with clear directional movement. It tends to have higher win rates compared to mean-reversion strategies but may experience larger drawdowns during trend reversals. Recommended for EUR/USD and GBP/USD on H1 and H4 timeframes.

### Momentum Elder Strategy

The Momentum Elder strategy combines the Elder-Ray indicator concept with momentum analysis to identify trend strength and potential reversal points. It uses a combination of exponential moving average direction and bull/bear power measurements.

**Description**: This strategy implements the Elder-Ray principle where the market has three forces: the trend (represented by EMA), the bears (selling pressure), and the bulls (buying power). Signals are generated when the EMA is trending and either bulls or bears show exhaustion. The strategy captures momentum shifts early while confirming with volume-based indicators.

**Parameters**:
- `ema_period`: EMA period for trend identification (default: 13)
- `atr_period`: ATR period for volatility measurement (default: 14)
- `atr_multiplier`: Multiplier for stop loss distance (default: 2.5)
- `min_bull_power`: Minimum bull power threshold for buy signals (default: 0.0001)
- `min_bear_power`: Minimum bear power threshold for sell signals (default: -0.0001)
- `exit_atr_multiplier`: ATR multiplier for take profit (default: 3.0)

**Example Usage**:
```python
from trading.strategy.tradfi.forex.momentum_elder.strategy import MomentumElderStrategy

# Create strategy with custom settings
strategy = MomentumElderStrategy(
    ema_period=13,
    atr_period=14,
    min_bull_power=0.0001
)

# Generate trading signals
signals = strategy.get_signals(ohlcv_data)

# Execute backtest
engine = BacktestEngine(strategy)
metrics = engine.run(ohlcv_data)
print(engine.format_summary(metrics))
```

**Performance Notes**: The Momentum Elder strategy excels in capturing early trend continuations and identifying potential reversals. It typically generates fewer but higher-quality signals compared to simpler strategies. Best suited for USD/JPY and AUD/USD where momentum shifts are more pronounced. Average trade duration is 2-5 days.

### Kumo Breakout Strategy

The Kumo Breakout strategy is based on Ichimoku Cloud analysis, specifically focusing on price breaking through the cloud (kumo) structure. It uses the cloud as dynamic support and resistance zones.

**Description**: This strategy implements the core concepts of Ichimoku Kinko Hyo: Tenkan-sen (conversion line), Kijun-sen (base line), and Senkou Span A/B (leading spans that form the cloud). Entry signals occur when price breaks above the cloud (bullish) or below the cloud (bearish), with additional confirmation from Tenkan-sen and Kijun-sen crossovers. The strategy filters out weak signals by requiring price to close outside the cloud before generating entries.

**Parameters**:
- `tenkan_period`: Tenkan-sen period (default: 9)
- `kijun_period`: Kijun-sen period (default: 26)
- `senkou_period`: Senkou Span period (default: 52)
- `cloud_displacement`: Cloud displacement forward (default: 26)
- `tenkan_kijun_confirmation`: Require Tenkan/Kijun crossover (default: True)
- `atr_period`: ATR period for stop loss (default: 14)
- `atr_multiplier`: ATR multiplier for stop loss (default: 2.0)

**Example Usage**:
```python
from trading.strategy.tradfi.forex.kumo_breakout.strategy import KumoBreakoutStrategy

# Initialize strategy with custom parameters
strategy = KumoBreakoutStrategy(
    tenkan_period=9,
    kijun_period=26,
    tenkan_kijun_confirmation=True
)

# Get signals from market data
signals = strategy.get_signals(ohlcv_data)

# Run backtest with detailed metrics
engine = BacktestEngine(strategy)
metrics = engine.run(ohlcv_data)
```

**Performance Notes**: Kumo Breakout works well in trending markets with clear directional bias. The strategy provides excellent risk management through dynamic support/resistance levels from the cloud. Particularly effective on EUR/USD and USD/CHF. False breakouts can occur during low-volatility periods, so additional confirmation is recommended.

## CRYPTO Strategies

CRYPTO strategies are designed for cryptocurrency markets which operate 24/7 with higher volatility and unique metrics like funding rates. These strategies account for the round-the-clock trading and leverage opportunities available in crypto markets.

### Funding Reversal Strategy

The Funding Reversal strategy exploits funding rate cycles in perpetual futures markets. It identifies overextended funding rates that typically precede reversals, allowing traders to position against crowded trades.

**Description**: In perpetual futures markets, funding rates balance long and short positions. When funding rates become extremely positive, it indicates heavy long positioning which often precedes pullbacks. Conversely, highly negative funding rates indicate excessive short positioning. This strategy monitors funding rates and generates reversal signals when rates exceed threshold levels, betting on mean reversion in sentiment.

**Parameters**:
- `funding_threshold`: Funding rate threshold for signal generation (default: 0.001)
- `funding_period`: Period for funding rate smoothing (default: 8)
- `price_ema_period`: EMA period for price trend (default: 20)
- `min_funding_duration`: Minimum periods above/below threshold (default: 3)
- `atr_period`: ATR period for stop loss (default: 14)
- `atr_multiplier`: ATR multiplier for position sizing (default: 1.5)

**Example Usage**:
```python
from trading.strategy.crypto.funding_reversal.strategy import FundingReversalStrategy

# Create strategy for funding rate reversals
strategy = FundingReversalStrategy(
    funding_threshold=0.001,
    funding_period=8,
    min_funding_duration=3
)

# Get signals combining price and funding data
signals = strategy.get_signals(ohlcv_data, funding_data)

# Execute backtest
engine = BacktestEngine(strategy)
metrics = engine.run(ohlcv_data)
```

**Performance Notes**: This strategy performs exceptionally well during funding rate extremes, typically capturing 2-5% reversals. Best used on BTC/USDT and ETH/USDT perpetual futures. During low-volatility periods, funding rates may stay elevated longer than expected, requiring patience. Average trade duration is 1-3 days.

### Volume Momentum Strategy

The Volume Momentum strategy combines volume analysis with price momentum to identify strong trend continuations. It uses volume-weighted average price (VWAP) and volume momentum to confirm trend strength.

**Description**: This strategy identifies trends where volume confirms price movement. It calculates volume-weighted average price and compares current price to VWAP for trend direction. Volume momentum measures whether volume is increasing or decreasing with price, filtering out weak moves. Entry signals occur when price moves above VWAP with increasing volume (bullish) or below VWAP with increasing volume (bearish).

**Parameters**:
- `vwap_period`: Period for VWAP calculation (default: 14)
- `volume_ma_period`: Moving average period for volume (default: 20)
- `volume_threshold`: Multiplier for unusual volume detection (default: 1.5)
- `momentum_period`: Period for momentum calculation (default: 10)
- `atr_period`: ATR period for stop loss (default: 14)
- `risk_per_trade`: Risk percentage per trade (default: 0.02)

**Example Usage**:
```python
from trading.strategy.crypto.volume_momentum.strategy import VolumeMomentumStrategy

# Initialize volume-based momentum strategy
strategy = VolumeMomentumStrategy(
    vwap_period=14,
    volume_ma_period=20,
    volume_threshold=1.5
)

# Generate signals based on volume confirmation
signals = strategy.get_signals(ohlcv_data)

# Run backtest with risk management
engine = BacktestEngine(strategy)
metrics = engine.run(ohlcv_data)
```

**Performance Notes**: Volume Momentum strategy excels in capturing strong trend moves with volume confirmation. It filters out many false breakouts by requiring volume validation. Particularly effective on altcoins during high-volatility periods. Should be combined with market regime filtering to avoid ranging markets.

## STOCKS Strategies

STOCKS strategies are designed for equity markets with focus on swing trading and position trading timeframes. These strategies account for market hours, earnings seasons, and the different volatility patterns of stock markets.

### Golden Cross Strategy

The Golden Cross strategy is a classic trend-following approach using moving average crossovers. It identifies major trend changes when a shorter moving average crosses above a longer moving average.

**Description**: The Golden Cross occurs when a short-term moving average (typically 50-day) crosses above a long-term moving average (typically 200-day). This pattern historically signals the beginning of a new uptrend. The strategy generates buy signals on golden cross events and sell signals when the short MA crosses back below the long MA (death cross). Additional filters can be applied to improve signal quality.

**Parameters**:
- `fast_ma_period`: Fast moving average period (default: 50)
- `slow_ma_period`: Slow moving average period (default: 200)
- `ma_type`: Moving average type - "SMA", "EMA", "WMA" (default: "SMA")
- `volume_confirmation`: Require volume confirmation (default: True)
- `volume_ma_period`: Volume MA period for confirmation (default: 20)
- `atr_period`: ATR period for stop loss (default: 14)
- `atr_multiplier`: ATR multiplier for stop loss (default: 2.0)

**Example Usage**:
```python
from trading.strategy.tradfi.stocks.golden_cross.strategy import GoldenCrossStrategy

# Create golden cross strategy for swing trading
strategy = GoldenCrossStrategy(
    fast_ma_period=50,
    slow_ma_period=200,
    ma_type="SMA",
    volume_confirmation=True
)

# Get signals from daily data
signals = strategy.get_signals(daily_ohlcv_data)

# Run long-term backtest
engine = BacktestEngine(strategy)
metrics = engine.run(daily_ohlcv_data)
```

**Performance Notes**: Golden Cross is a proven long-term trend-following strategy with historical success in equity markets. It generates fewer signals but captures major trend moves. Best suited for index funds and large-cap stocks. The strategy has a natural lag due to using longer-period moving averages, which reduces whipsaws but also delays entries.

### RSI Divergence Strategy

The RSI Divergence strategy identifies potential reversals by detecting divergences between price action and the Relative Strength Index momentum oscillator.

**Description**: Regular bullish divergence occurs when price makes lower lows while RSI makes higher lows, indicating weakening downward momentum. Regular bearish divergence occurs when price makes higher highs while RSI makes lower highs, signaling potential trend exhaustion. The strategy identifies these divergence patterns and generates reversal signals with additional confirmation from overbought/oversold levels and price structure.

**Parameters**:
- `rsi_period`: RSI calculation period (default: 14)
- `rsi_overbought`: Overbought threshold (default: 70)
- `rsi_oversold`: Oversold threshold (default: 30)
- `lookback_period`: Period for divergence detection (default: 14)
- `min_pivot_points`: Minimum pivot points for divergence (default: 2)
- `atr_period`: ATR period for stop loss (default: 14)
- `atr_multiplier`: ATR multiplier for stop loss (default: 1.5)

**Example Usage**:
```python
from trading.strategy.tradfi.stocks.rsi_divergence.strategy import RSIDivergenceStrategy

# Initialize RSI divergence strategy
strategy = RSIDivergenceStrategy(
    rsi_period=14,
    rsi_overbought=70,
    rsi_oversold=30,
    lookback_period=14
)

# Detect divergence signals
signals = strategy.get_signals(ohlcv_data)

# Run backtest
engine = BacktestEngine(strategy)
metrics = engine.run(ohlcv_data)
```

**Performance Notes**: RSI Divergence works best in ranging markets and at major trend turning points. It provides early signals but requires confirmation to avoid false positives. Particularly effective on individual stocks with higher volatility. Should be combined with support/resistance analysis for best results.

## COMMODITY Strategies

COMMODITY strategies are designed for trading physical goods and commodity futures. These strategies account for the unique supply/demand dynamics, seasonality patterns, and correlation relationships in commodity markets.

### Gold Silver Ratio Strategy

The Gold Silver Ratio strategy exploits the historical correlation between gold and silver prices. It generates signals based on deviations from the historical ratio and mean reversion expectations.

**Description**: Gold and silver have a historically correlated relationship, with the ratio typically ranging between 40:1 and 90:1. When the ratio moves to extreme levels, mean reversion opportunities arise. This strategy monitors the XAU/XAG ratio and generates signals when it deviates significantly from its historical mean, betting on the ratio returning to normal levels.

**Parameters**:
- `ratio_ma_period`: Moving average period for ratio (default: 50)
- `ratio_std_period`: Standard deviation period for bands (default: 20)
- `upper_band`: Upper band threshold (default: 2.0)
- `lower_band`: Lower band threshold (default: -2.0)
- `min_ratio_value`: Minimum ratio value for signals (default: 40)
- `max_ratio_value`: Maximum ratio value for signals (default: 90)
- `atr_period`: ATR period for stop loss (default: 14)

**Example Usage**:
```python
from trading.strategy.tradfi.commodities.gold_silver_ratio.strategy import GoldSilverRatioStrategy

# Create ratio-based strategy
strategy = GoldSilverRatioStrategy(
    ratio_ma_period=50,
    ratio_std_period=20,
    upper_band=2.0,
    lower_band=-2.0
)

# Get signals from gold and silver data
signals = strategy.get_signals(gold_ohlcv, silver_ohlcv)

# Run backtest on ratio data
engine = BacktestEngine(strategy)
metrics = engine.run(ratio_data)
```

**Performance Notes**: This strategy benefits from the long-term mean-reverting nature of the gold-silver ratio. Signals are infrequent but historically high-probability. Best used for longer-term positions (weeks to months). The ratio can remain at extreme levels for extended periods during market stress.

### Seasonal Strategy

The Seasonal strategy exploits predictable seasonal patterns in commodity prices based on historical calendar-based trends and supply/demand cycles.

**Description**: Many commodities exhibit predictable seasonal patterns due to agricultural cycles, weather patterns, and industrial demand fluctuations. This strategy analyzes historical seasonal patterns and generates trades based on statistically significant seasonal tendencies. It includes patterns for energy (heating season), agriculture (planting/harvest), and metals (industrial demand cycles).

**Parameters**:
- `seasonal_months`: Months for seasonal pattern (default: [1, 2, 3])
- `lookback_years`: Years of historical data for pattern (default: 10)
- `min_win_rate`: Minimum historical win rate (default: 0.55)
- `min_avg_return`: Minimum average return threshold (default: 0.02)
- `atr_period`: ATR period for position sizing (default: 14)
- `atr_multiplier`: ATR multiplier for stop loss (default: 2.0)

**Example Usage**:
```python
from trading.strategy.tradfi.commodities.seasonal.strategy import SeasonalStrategy

# Create seasonal strategy for specific commodity
strategy = SeasonalStrategy(
    seasonal_months=[12, 1, 2],  # Winter pattern
    lookback_years=10,
    min_win_rate=0.55
)

# Generate seasonal signals
signals = strategy.get_signals(commodity_ohlcv)

# Run backtest on historical seasonal data
engine = BacktestEngine(strategy)
metrics = engine.run(commodity_ohlcv)
```

**Performance Notes**: Seasonal strategies provide statistically backed edge based on historical patterns. They work best when combined with other technical signals for timing. Different commodities have different seasonal patterns - natural gas (winter), crude oil (summer driving season), agricultural (harvest). Requires sufficient historical data for statistical significance.

## Performance Summary

### Strategy Comparison Table

| Strategy | Market Type | Timeframe | Win Rate | Avg Return | Max Drawdown | Signal Frequency |
|----------|-------------|-----------|----------|------------|--------------|------------------|
| Holy Grail | FOREX | H1-H4 | 55-60% | 1.5-3% | 8-12% | Medium |
| Momentum Elder | FOREX | H1-D1 | 52-58% | 2-4% | 10-15% | Medium |
| Kumo Breakout | FOREX | H1-H4 | 50-55% | 1.5-2.5% | 7-10% | Low-Medium |
| Funding Reversal | CRYPTO | H1-H4 | 55-65% | 2-5% | 5-10% | Low |
| Volume Momentum | CRYPTO | H1-D1 | 50-58% | 2-4% | 8-12% | Medium |
| Golden Cross | STOCKS | D1-W1 | 45-55% | 3-8% | 15-25% | Low |
| RSI Divergence | STOCKS | H1-D1 | 52-60% | 2-5% | 10-15% | Medium |
| Gold Silver Ratio | COMMODITY | W1-MN | 60-70% | 5-15% | 10-20% | Very Low |
| Seasonal | COMMODITY | W1-MN | 55-65% | 4-10% | 8-15% | Very Low |

### Market Type Recommendations

**FOREX**: Best suited for Holy Grail and Kumo Breakout strategies due to the 24-hour market structure and strong trending behavior. Momentum Elder works well for capturing momentum shifts in major currency pairs.

**CRYPTO**: Funding Reversal provides unique edge through funding rate analysis not available in traditional markets. Volume Momentum captures the high-volatility trend moves typical of cryptocurrency markets.

**STOCKS**: Golden Cross is ideal for long-term position trading in equities. RSI Divergence works well for swing trading individual stocks with higher volatility.

**COMMODITY**: Gold Silver Ratio exploits the long-term mean-reverting relationship between precious metals. Seasonal strategies provide statistically backed edge based on predictable supply/demand cycles.

### Risk Management Guidelines

All strategies should be used with proper position sizing and risk management. Recommended risk per trade is 1-2% of account equity. Stop losses should be set using ATR-based calculations to account for market volatility. Position sizes should be adjusted based on the strategy's typical drawdown characteristics.

## Usage Examples

### Complete Backtest Example

```python
from trading.brokers.base import OHLCV
from trading.strategy.tradfi.forex.holy_grail.strategy import HolyGrailStrategy
from trading.backtest.engine import BacktestEngine

# Load historical data
ohlcv_data = load_ohlcv("EURUSD", "H1", start_date="2023-01-01")

# Create and configure strategy
strategy = HolyGrailStrategy(
    fast_ema_period=12,
    slow_ema_period=26,
    rsi_period=14
)

# Run comprehensive backtest
engine = BacktestEngine(strategy)
metrics = engine.run(ohlcv_data)

# Display results
print(f"Total Trades: {metrics['total_trades']}")
print(f"Win Rate: {metrics['win_rate']:.2%}")
print(f"Profit Factor: {metrics['profit_factor']:.2f}")
print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
print(f"Net Profit: {metrics['net_profit']:.2f}")
```

### Multi-Strategy Portfolio Example

```python
from trading.strategy.tradfi.forex.holy_grail.strategy import HolyGrailStrategy
from trading.strategy.crypto.funding_reversal.strategy import FundingReversalStrategy
from trading.backtest.engine import BacktestEngine

# Create strategies for different markets
forex_strategy = HolyGrailStrategy()
crypto_strategy = FundingReversalStrategy()

# Run separate backtests
forex_engine = BacktestEngine(forex_strategy)
crypto_engine = BacktestEngine(crypto_strategy)

forex_metrics = forex_engine.run(forex_data)
crypto_metrics = crypto_engine.run(crypto_data)

# Combine results for portfolio analysis
portfolio_metrics = combine_metrics([forex_metrics, crypto_metrics])
```

### Paper Trading Example

```python
from trading.paper_trade.executor import PaperTradeExecutor
from trading.strategy.tradfi.stocks.golden_cross.strategy import GoldenCrossStrategy

# Initialize paper trading
executor = PaperTradeExecutor(initial_balance=100000)

# Create strategy
strategy = GoldenCrossStrategy(
    fast_ma_period=50,
    slow_ma_period=200
)

# Start paper trading with live data feed
executor.start(strategy, data_feed="yahoo_finance")
```

## Additional Resources

- See `trading/SKILL.md` for complete trading system documentation
- See individual strategy SKILL.md files for detailed parameter tuning
- See `trading/backtest/engine.py` for backtesting engine documentation
- See `trading/risk/manager.py` for risk management implementation

## License

MIT License - See main project LICENSE file for details.
