# Trading Skills System

Comprehensive trading automation system for 1ai-skills.

## Features

- **Multi-Broker Support**: MetaTrader 5, MetaTrader 4, CCXT (cryptocurrency)
- **Trading Modes**: Backtest, Paper Trade, Real Trade
- **Strategy Framework**: Extensible strategy base class
- **XAUUSD Strategy**: Asia 7-Candle Breakout strategy included
- **Risk Management**: Position sizing, SL/TP calculation, guardrails

## Installation

### Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install MetaTrader5
pip install ccxt
pip install pandas
pip install pytz
pip install yfinance  # For free XAUUSD/Gold data
```

### Quick Test

```bash
# Test the backtest engine
python3 -c "
from trading.brokers.base import OHLCV
from trading.strategy.tradfi.commodities.xauusd_asia_7c_breakout.strategy import XAUUSDAsia7CBreakout
from trading.backtest.engine import BacktestEngine
print('All imports OK!')
"
```

## Quick Start

```python
from trading.brokers.mt5 import MT5Connector
from trading.strategy.tradfi.commodities.xauusd_asia_7c_breakout.strategy import XAUUSDAsia7CBreakout
from trading.backtest.engine import BacktestEngine

# Connect to broker
broker = MT5Connector()
broker.connect(login=12345, password="xxx", server="Broker-Server")

# Create strategy
strategy = XAUUSDAsia7CBreakout()

# Get signals
ohlcv_data = broker.get_ohlcv("XAUUSD", "H1", count=100)
signals = strategy.get_signals(ohlcv_data)

# Run backtest
engine = BacktestEngine(strategy)
metrics = engine.run(ohlcv_data)
print(engine.format_summary(metrics))
```

## Structure

```
trading/
├── brokers/           # Broker connectors
│   ├── mt5/         # MetaTrader 5
│   ├── mt4/         # MetaTrader 4
│   └── ccxt/        # CCXT crypto
├── strategy/         # Trading strategies
│   ├── base.py      # Strategy base class
│   ├── crypto/      # Crypto strategies
│   └── tradfi/      # Traditional finance
│       ├── forex/
│       ├── stocks/
│       └── commodities/
├── backtest/        # Backtesting
├── paper_trade/     # Paper trading
├── real_trade/      # Real trading with guardrails
├── risk/           # Risk management
├── data/           # Data storage
└── team/           # Trading team skills
```

## Commands

See individual SKILL.md files for command reference.

## License

MIT
