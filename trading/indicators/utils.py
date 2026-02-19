"""
Indicator Utilities

Helper functions for technical indicator calculations.
"""

from typing import List, Optional
import logging

from ..brokers.base import OHLCV

logger = logging.getLogger(__name__)


def validate_period(period: int, data_length: int) -> bool:
    """
    Validate that period is valid for given data length.

    Args:
        period: The period to validate (e.g., 14 for RSI period)
        data_length: Length of the data being analyzed

    Returns:
        True if period is valid

    Raises:
        ValueError: If period is invalid (negative, zero, or greater than data length)
    """
    if period <= 0:
        raise ValueError(f"Period must be positive, got {period}")

    if data_length < period:
        raise ValueError(
            f"Period ({period}) cannot be greater than data length ({data_length})"
        )

    return True


def calculate_change(prices: List[float]) -> List[float]:
    """
    Calculate price changes between consecutive periods.

    Args:
        prices: List of price values

    Returns:
        List of price changes (difference between current and previous price)
        First element is 0.0

    Example:
        >>> calculate_change([100, 102, 101, 103])
        [0.0, 2.0, -1.0, 2.0]
    """
    if not prices:
        return []

    if len(prices) == 1:
        return [0.0]

    changes = [0.0]  # First element has no previous value
    for i in range(1, len(prices)):
        changes.append(prices[i] - prices[i - 1])

    return changes


def extract_prices(data: List[OHLCV], price_type: str = "close") -> List[float]:
    """
    Extract price series from OHLCV data.

    Args:
        data: List of OHLCV candlestick data
        price_type: Type of price to extract ("open", "high", "low", "close")

    Returns:
        List of price values

    Raises:
        ValueError: If price_type is invalid
    """
    valid_types = ["open", "high", "low", "close"]

    if price_type not in valid_types:
        raise ValueError(f"Invalid price_type: {price_type}. Must be one of {valid_types}")

    return [getattr(candle, price_type) for candle in data]


def calculate_sma(prices: List[float], period: int) -> Optional[float]:
    """
    Calculate Simple Moving Average.

    Args:
        prices: List of price values
        period: Number of periods for average

    Returns:
        SMA value or None if insufficient data
    """
    if len(prices) < period:
        return None

    return sum(prices[-period:]) / period


def calculate_ema(prices: List[float], period: int, prev_ema: Optional[float] = None) -> Optional[float]:
    """
    Calculate Exponential Moving Average.

    Args:
        prices: List of price values
        period: Number of periods for average
        prev_ema: Previous EMA value (for recursive calculation)

    Returns:
        EMA value or None if insufficient data
    """
    if len(prices) < period:
        return None

    multiplier = 2 / (period + 1)

    if prev_ema is None:
        # First EMA is SMA
        return calculate_sma(prices, period)

    current_price = prices[-1]
    return (current_price * multiplier) + (prev_ema * (1 - multiplier))
