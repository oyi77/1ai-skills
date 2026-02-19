"""
Pytest fixtures for strategy template tests.
"""
import pytest
from datetime import datetime, timedelta
from typing import List

from trading.brokers.base import OHLCV


def create_ohlcv(
    timestamp: datetime,
    open_price: float,
    high: float,
    low: float,
    close: float,
    volume: float = 1000.0
) -> OHLCV:
    """Create a single OHLCV candle."""
    return OHLCV(
        timestamp=timestamp,
        open=open_price,
        high=high,
        low=low,
        close=close,
        volume=volume
    )


def generate_ohlcv_data(
    start_time: datetime,
    count: int,
    start_price: float = 100.0,
    trend: str = "up",
    volatility: float = 0.5
) -> List[OHLCV]:
    """
    Generate OHLCV data for testing.
    
    Args:
        start_time: Starting timestamp
        count: Number of candles
        start_price: Starting price
        trend: "up", "down", or "sideways"
        volatility: Price volatility factor
        
    Returns:
        List of OHLCV objects
    """
    data = []
    current_price = start_price
    
    for i in range(count):
        timestamp = start_time + timedelta(hours=i)
        
        # Generate price with trend
        if trend == "up":
            change = volatility * (1 + i * 0.001)
        elif trend == "down":
            change = -volatility * (1 + i * 0.001)
        else:
            change = volatility * ((i % 10) - 5) * 0.1
        
        current_price = current_price + change
        
        # Generate OHLC
        high_offset = abs(volatility * 0.5 * (1 + (i % 3) * 0.1))
        low_offset = abs(volatility * 0.5 * (1 + (i % 3) * 0.1))
        
        high = current_price + high_offset
        low = current_price - low_offset
        open_price = current_price - (low_offset * 0.3) + (high_offset * 0.3)
        
        data.append(create_ohlcv(
            timestamp=timestamp,
            open_price=open_price,
            high=high,
            low=low,
            close=current_price,
            volume=1000 + i * 10
        ))
    
    return data


@pytest.fixture
def sample_ohlcv_bullish():
    """Generate bullish OHLCV data."""
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    return generate_ohlcv_data(
        start_time=start_time,
        count=100,
        start_price=100.0,
        trend="up",
        volatility=0.3
    )


@pytest.fixture
def sample_ohlcv_bearish():
    """Generate bearish OHLCV data."""
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    return generate_ohlcv_data(
        start_time=start_time,
        count=100,
        start_price=100.0,
        trend="down",
        volatility=0.3
    )


@pytest.fixture
def sample_ohlcv_sideways():
    """Generate sideways OHLCV data."""
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    return generate_ohlcv_data(
        start_time=start_time,
        count=100,
        start_price=100.0,
        trend="sideways",
        volatility=0.5
    )


@pytest.fixture
def sample_ohlcv_with_breakout():
    """Generate OHLCV data with breakout pattern."""
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    data = []
    current_price = 100.0
    
    for i in range(50):
        timestamp = start_time + timedelta(hours=i)
        
        if i < 30:
            # Sideways market
            current_price = 100.0 + (i % 10) * 0.1
        else:
            # Breakout
            current_price = 100.0 + (i - 30) * 0.5
        
        high = current_price + 0.2
        low = current_price - 0.2
        open_price = current_price - 0.1
        
        data.append(create_ohlcv(
            timestamp=timestamp,
            open_price=open_price,
            high=high,
            low=low,
            close=current_price,
            volume=1000 + i * 20  # Increasing volume on breakout
        ))
    
    return data
