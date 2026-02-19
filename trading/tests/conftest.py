"""
Pytest fixtures for trading skill tests.
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock
import pandas as pd


@pytest.fixture
def broker_mock():
    """Mock broker fixture for testing."""
    broker = Mock()
    broker.connect = Mock(return_value=True)
    broker.disconnect = Mock(return_value=True)
    broker.get_account_info = Mock(return_value={
        'balance': 10000.0,
        'equity': 10000.0,
        'margin': 0.0,
        'free_margin': 10000.0
    })
    broker.place_order = Mock(return_value={'ticket': 12345, 'status': 'filled'})
    broker.close_position = Mock(return_value={'ticket': 12345, 'status': 'closed'})
    return broker


@pytest.fixture
def strategy_mock():
    """Mock strategy fixture for testing."""
    strategy = Mock()
    strategy.initialize = Mock(return_value=True)
    strategy.on_data = Mock(return_value={'signal': 'buy', 'strength': 0.8})
    strategy.on_tick = Mock(return_value=None)
    strategy.get_parameters = Mock(return_value={
        'period': 14,
        'threshold': 0.5
    })
    return strategy


@pytest.fixture
def sample_ohlcv_data():
    """Sample OHLCV data fixture for testing."""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='1h')
    data = pd.DataFrame({
        'timestamp': dates,
        'open': [100.0 + i * 0.1 for i in range(100)],
        'high': [101.0 + i * 0.1 for i in range(100)],
        'low': [99.0 + i * 0.1 for i in range(100)],
        'close': [100.5 + i * 0.1 for i in range(100)],
        'volume': [1000 + i * 10 for i in range(100)]
    })
    return data


@pytest.fixture
def sample_trade():
    """Sample trade fixture for testing."""
    return {
        'ticket': 12345,
        'symbol': 'EURUSD',
        'type': 'buy',
        'volume': 0.1,
        'open_price': 1.0850,
        'open_time': datetime.now(),
        'sl': 1.0800,
        'tp': 1.0900,
        'profit': 0.0
    }
