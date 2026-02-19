"""
Integration test for OpenClaw - tests full pipeline.
Run with: python -m pytest scripts/test_integration.py -v
"""

import pytest
from data.symbols import get_symbol_config
from indicators.rsi import RSI
from indicators.macd import MACD
from indicators.bollinger_bands import BollingerBands
from indicators.moving_averages import SMA, EMA, WMA
from risk.manager import RiskManager
from exceptions import TradingError
from utils.error_handler import retry
from brokers.base import OHLCV
from datetime import datetime, timedelta


def test_symbol_configs():
    """Test symbol configurations."""
    for symbol in ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]:
        config = get_symbol_config(symbol)
        assert config is not None
        assert config.yahoo_ticker is not None


def test_indicators():
    """Test indicator calculations."""
    # Create sample data
    data = []
    base = datetime(2024, 1, 1)
    for i in range(30):
        data.append(OHLCV(
            timestamp=base + timedelta(hours=i),
            open=100.0 + i,
            high=101.0 + i,
            low=99.0 + i,
            close=100.0 + i,
            volume=1000.0
        ))
    
    rsi = RSI()
    result = rsi.calculate(data)
    assert result is not None
    
    sma = SMA(period=10)
    result = sma.calculate(data)
    assert result is not None


def test_risk_manager():
    """Test risk manager."""
    rm = RiskManager()
    lot = rm.calculate_fixed_lot(10000, 0.1)
    assert lot > 0


def test_exceptions():
    """Test exceptions exist."""
    assert issubclass(TradingError, Exception)
    from exceptions import BrokerConnectionError
    assert issubclass(BrokerConnectionError, TradingError)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
