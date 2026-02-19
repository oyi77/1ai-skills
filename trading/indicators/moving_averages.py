"""
Moving Averages Indicators

Implementation of Simple Moving Average (SMA), Exponential Moving Average (EMA),
and Weighted Moving Average (WMA) technical indicators.
"""

from typing import List, Optional
from ..brokers.base import OHLCV
from .base import Indicator
from .utils import extract_prices


class SMA(Indicator):
    """
    Simple Moving Average (SMA) indicator.
    
    SMA is the arithmetic mean of a given set of prices over a specific number of days.
    Formula: sum(period) / period
    """

    def __init__(self, period: int = 20):
        """
        Initialize SMA indicator.
        
        Args:
            period: Number of periods for the moving average (default: 20)
        """
        super().__init__(period=period)
        self.period = period
        self._name = f"SMA_{period}"

    def calculate(self, data: List[OHLCV]) -> List[Optional[float]]:
        """
        Calculate SMA values for the given OHLCV data.
        
        Args:
            data: List of OHLCV candlestick data
            
        Returns:
            List of SMA values. First (period-1) values are None (insufficient data)
        """
        self.validate_input(data)
        
        if len(data) < self.period:
            raise ValueError(
                f"{self.name}: Insufficient data. Need at least {self.period} candles, got {len(data)}"
            )

        closes = extract_prices(data, "close")
        results: List[Optional[float]] = []

        for i in range(len(closes)):
            if i < self.period - 1:
                results.append(None)
            else:
                window = closes[i - self.period + 1 : i + 1]
                sma_value = sum(window) / self.period
                results.append(sma_value)

        return results

    def get_required_period(self) -> int:
        """Get minimum number of candles required for calculation."""
        return self.period


class EMA(Indicator):
    """
    Exponential Moving Average (EMA) indicator.
    
    EMA gives more weight to recent prices, making it more responsive to new information.
    Formula: EMA = (Price * k) + (Previous EMA * (1-k)), where k = 2/(period+1)
    """

    def __init__(self, period: int = 20):
        """
        Initialize EMA indicator.
        
        Args:
            period: Number of periods for the moving average (default: 20)
        """
        super().__init__(period=period)
        self.period = period
        self._name = f"EMA_{period}"
        self.multiplier = 2 / (period + 1)

    def calculate(self, data: List[OHLCV]) -> List[Optional[float]]:
        """
        Calculate EMA values for the given OHLCV data.
        
        Args:
            data: List of OHLCV candlestick data
            
        Returns:
            List of EMA values. First (period-1) values are None (insufficient data)
        """
        self.validate_input(data)
        
        if len(data) < self.period:
            raise ValueError(
                f"{self.name}: Insufficient data. Need at least {self.period} candles, got {len(data)}"
            )

        closes = extract_prices(data, "close")
        results: List[Optional[float]] = []
        prev_ema: Optional[float] = None

        for i in range(len(closes)):
            if i < self.period - 1:
                results.append(None)
            elif i == self.period - 1:
                # First EMA is SMA of first 'period' prices
                window = closes[: self.period]
                prev_ema = sum(window) / self.period
                results.append(prev_ema)
            else:
                current_price = closes[i]
                ema_value = (current_price * self.multiplier) + (
                    prev_ema * (1 - self.multiplier)
                )
                results.append(ema_value)
                prev_ema = ema_value

        return results

    def get_required_period(self) -> int:
        """Get minimum number of candles required for calculation."""
        return self.period


class WMA(Indicator):
    """
    Weighted Moving Average (WMA) indicator.
    
    WMA assigns linearly increasing weights to more recent prices.
    Formula: sum(weight * price) / sum(weights)
    Weights: 1, 2, 3, ..., period (most recent = highest weight)
    """

    def __init__(self, period: int = 20):
        """
        Initialize WMA indicator.
        
        Args:
            period: Number of periods for the moving average (default: 20)
        """
        super().__init__(period=period)
        self.period = period
        self._name = f"WMA_{period}"
        # Pre-calculate weights: 1, 2, 3, ..., period
        self.weights = list(range(1, period + 1))
        self.weight_sum = sum(self.weights)

    def calculate(self, data: List[OHLCV]) -> List[Optional[float]]:
        """
        Calculate WMA values for the given OHLCV data.
        
        Args:
            data: List of OHLCV candlestick data
            
        Returns:
            List of WMA values. First (period-1) values are None (insufficient data)
        """
        self.validate_input(data)
        
        if len(data) < self.period:
            raise ValueError(
                f"{self.name}: Insufficient data. Need at least {self.period} candles, got {len(data)}"
            )

        closes = extract_prices(data, "close")
        results: List[Optional[float]] = []

        for i in range(len(closes)):
            if i < self.period - 1:
                results.append(None)
            else:
                window = closes[i - self.period + 1 : i + 1]
                # Apply weights: oldest gets weight 1, newest gets weight 'period'
                weighted_sum = sum(
                    price * weight for price, weight in zip(window, self.weights)
                )
                wma_value = weighted_sum / self.weight_sum
                results.append(wma_value)

        return results

    def get_required_period(self) -> int:
        """Get minimum number of candles required for calculation."""
        return self.period
