---
name: trading
description: Comprehensive trading skills system with multi-broker support, strategy execution, and autonomous trading capabilities
permissions:
  - fs
  - network
---

# Trading Skills System

Comprehensive trading automation system with multi-broker support, strategy development, and autonomous trading capabilities.

## Capabilities

### Broker Connectors
- **MetaTrader 5 (MT5)**: Full support for forex, commodities, stocks, indices
- **MetaTrader 4 (MT4)**: Legacy broker support
- **CCXT**: Cryptocurrency exchange integration (Binance, Bybit, OKX, KuCoin, etc.)

### Trading Modes
- **Backtest**: Historical strategy testing with detailed metrics
- **Paper Trade**: Virtual trading with real-time simulation
- **Real Trade**: Live execution with guardrails and safety checks

### Strategy Support
- **Crypto**: Cryptocurrency trading strategies
- **TradFi**:
  - Forex: Major, minor, and exotic pairs
  - Stocks: Individual equities
  - Commodities: Gold, silver, oil, etc.

### Trading Team
- **Researcher**: Market analysis and data collection
- **Strategist**: Strategy building and optimization
- **Risk Manager**: Position sizing and risk control
- **Executor**: Trade execution with broker integration
- **Orchestrator**: Team coordination for autonomous operations

## Commands

### `setup`
Initialize trading configuration and broker connection.

**Usage**: `setup broker=mt5 path=/path/to/mt5 terminal login=12345 password=xxx server=Broker-Server`

### `signal today`
Get trading signals for today.

**Usage**: `signal today symbol=XAUUSD timeframe=H1`

### `backtest`
Run historical backtest.

**Usage**: `backtest symbol=XAUUSD start=2024-01-01 end=2024-12-31`

### `paper start`
Start paper trading mode.

**Usage**: `paper start symbol=XAUUSD`

### `paper status`
Check paper trading status.

**Usage**: `paper status`

### `paper stop`
Stop paper trading.

**Usage**: `paper stop`

### `real arm`
Arm real trading with guardrail check.

**Usage**: `real arm symbol=XAUUSD volume=0.01`

### `real status`
Check real trading status.

**Usage**: `real status`

### `real disarm`
Disarm real trading.

**Usage**: `real disarm`

### `export trades`
Export trade history.

**Usage**: `export trades format=csv`

## Configuration

### Session Settings
- `timezone`: Trading timezone (default: "Asia/Jakarta")
- `session_start`: Session start time (default: "07:00")
- `session_end`: Session end time (default: "15:00")

### Risk Settings
- `risk_mode`: "fixed_lot" or "fixed_risk_percent"
- `fixed_lot`: Fixed lot size (default: 0.01)
- `risk_percent`: Risk percentage per trade (default: 1.0)
- `rr_ratio`: Risk-reward ratio (default: 2.0)

### Execution Settings
- `max_spread_points`: Maximum spread allowed
- `one_trade_per_day`: Limit to one trade per day
- `cancel_opposite_on_trigger`: Cancel opposite pending order on trigger
- `cancel_all_at_session_end`: Cancel pending orders at session end

## Examples

### XAUUSD Asia Session Breakout
```
setup symbol=XAUUSD broker=mt5
signal today
backtest start=2024-01-01 end=2024-12-31
paper start
```

### Crypto Strategy
```
setup symbol=BTC/USDT broker=ccxt exchange=binance
signal today
backtest start=2024-01-01 end=2024-12-31
```

## Safety Guardrails

1. **Pre-trade validation**: Spread check, drawdown check, daily limit check
2. **Parameter confirmation**: Always show summary before real execution
3. **Hard limits**: 1 trade per day, max spread, max drawdown
4. **Opposite cancellation**: Cancel pending order when opposite triggers

## Dependencies

### Python Environment (Required)

```bash
# Create virtual environment in trading directory
cd /path/to/1ai-skills/trading
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install MetaTrader5  # For MT5 broker
pip install ccxt         # For crypto exchanges
pip install pandas pytz  # For data analysis
```

### Note
- Run Python from project root (parent of `trading/` directory)
- Or add `trading/` to Python path: `export PYTHONPATH=$PYTHONPATH:/path/to/1ai-skills`
