"""
Stochastic Oscillator Indicator

Technical indicator that compares a closing price to its price range over a given period.
It consists of two lines: %K (main line) and %D (signal line).
"""

from typing import List, Optional
from dataclasses import dataclass

from .base import Indicator
from .utils import validate_period, extract_prices
from ..brokers.base import OHLCV


@dataclass
class StochasticResult:
    """Result container for Stochastic Oscillator calculation."""
    
    k_value: float
    d_value: float
    period: int
    d_period: int
    overbought_level: float
    oversold_level: float
    
    def is_overbought(self) -> bool:
        """Check if Stochastic indicates overbought conditions."""
        return self.k_value >= self.overbought_level
    
    def is_oversold(self) -> bool:
        """Check if Stochastic indicates oversold conditions."""
        return self.k_value <= self.oversold_level
    
    def __repr__(self) -> str:
        status = ""
        if self.is_overbought():
            status = " (overbought)"
        elif self.is_oversold():
            status = " (oversold)"
        return f"Stochastic(%K={self.k_value:.2f}, %D={self.d_value:.2f}){status}"


class Stochastic(Indicator):
    """
    Stochastic Oscillator indicator.
    
    The Stochastic Oscillator compares the closing price to the price range
    over a given period. It consists of two lines:
    - %K: Main line that compares close to the high/low range
    - %D: Signal line (SMA of %K)
    
    Standard interpretation:
    - %K > 80: Overbought conditions (potential sell signal)
    - %K < 20: Oversold conditions (potential buy signal)
    - %K crossing above %D: Bullish signal
    - %K crossing below %D: Bearish signal
    
    Formula:
        %K = (Close - Lowest Low) / (Highest High - Lowest Low) * 100
        %D = SMA of %K (with smoothing period)
    
    Attributes:
        period: Number of periods for %K calculation (default: 14)
        d_period: Number of periods for %D SMA calculation (default: 3)
        slowing_period: Number of periods for %K smoothing (default: 3)
        overbought_level: Level considered overbought (default: 80)
        oversold_level: Level considered oversold (default: 20)
    """
    
    def __init__(
        self,
        period: int = 14,
        d_period: int = 3,
        slowing_period: int = 3,
        overbought_level: float = 80.0,
        oversold_level: float = 20.0,
    ):
        """
        Initialize Stochastic Oscillator indicator.
        
        Args:
            period: Number of periods for %K calculation (default: 14)
            d_period: Number of periods for %D SMA calculation (default: 3)
            slowing_period: Number of periods for %K smoothing (default: 3)
            overbought_level: Level considered overbought (default: 80)
            oversold_level: Level considered oversold (default: 20)
        """
        super().__init__(
            period=period,
            d_period=d_period,
            slowing_period=slowing_period,
            overbought_level=overbought_level,
            oversold_level=oversold_level,
        )
        self.period = period
        self.d_period = d_period
        self.slowing_period = slowing_period
        self.overbought_level = overbought_level
        self.oversold_level = oversold_level
    
    def get_required_period(self) -> int:
        """
        Get minimum number of candles required for calculation.
        
        Returns:
            Minimum number of candles needed (period + d_period - 1 for %D calculation)
        """
        return self.period + self.d_period - 1
    
    def calculate(self, data: List[OHLCV]) -> Optional[StochasticResult]:
        """
        Calculate Stochastic Oscillator from OHLCV data.
        
        Args:
            data: List of OHLCV candlestick data
            
        Returns:
            StochasticResult with calculated %K and %D values and helper methods,
            or None if insufficient data
            
        Raises:
            ValueError: If data is invalid
        """
        self.validate_input(data)
        validate_period(self.period, len(data))
        validate_period(self.d_period, len(data))
        
        # Need at least period + d_period - 1 candles for %D calculation
        if len(data) < self.get_required_period():
            raise ValueError(
                f"Stochastic requires at least {self.get_required_period()} candles, "
                f"got {len(data)}"
            )
        
        # Extract prices
        closes = extract_prices(data, "close")
        highs = extract_prices(data, "high")
        lows = extract_prices(data, "low")
        
        # Calculate %K values for all available data
        k_values = self._calculate_k_values(closes, highs, lows)
        
        # Calculate %D as SMA of %K
        d_value = self._calculate_d_value(k_values)
        
        # Get the last %K value (current)
        k_value = k_values[-1]
        
        return StochasticResult(
            k_value=k_value,
            d_value=d_value,
            period=self.period,
            d_period=self.d_period,
            overbought_level=self.overbought_level,
            oversold_level=self.oversold_level,
        )
    
    def _calculate_k_values(
        self, 
        closes: List[float], 
        highs: List[float], 
        lows: List[float]
    ) -> List[float]:
        """
        Calculate %K values for all periods where we have enough data.
        
        Args:
            closes: List of closing prices
            highs: List of high prices
            lows: List of low prices
            
        Returns:
            List of %K values
        """
        k_values = []
        
        # Need at least 'period' candles to start calculating
        for i in range(self.period - 1, len(closes)):
            # Get the high and low over the period
            period_highs = highs[i - self.period + 1 : i + 1]
            period_lows = lows[i - self.period + 1 : i + 1]
            
            highest_high = max(period_highs)
            lowest_low = min(period_lows)
            current_close = closes[i]
            
            # Calculate %K
            if highest_high == lowest_low:
                # Avoid division by zero - if range is zero, use 50 as neutral
                k_value = 50.0
            else:
                k_value = ((current_close - lowest_low) / (highest_high - lowest_low)) * 100.0
            
            # Apply slowing period smoothing
            if self.slowing_period > 1 and len(k_values) >= self.slowing_period - 1:
                # Calculate smoothed %K using simple average of last 'slowing_period' values
                start_idx = len(k_values) - self.slowing_period + 1
                smoothed_k = sum(k_values[start_idx:]) / self.slowing_period
                k_values.append(smoothed_k)
            else:
                k_values.append(k_value)
        
        return k_values
    
    def _calculate_d_value(self, k_values: List[float]) -> Optional[float]:
        """
        Calculate %D as SMA of %K values.
        
        Args:
            k_values: List of %K values
            
        Returns:
            %D value or None if insufficient data
        """
        if len(k_values) < self.d_period:
            return None
        
        # Get the last 'd_period' %K values and calculate their average
        recent_k_values = k_values[-self.d_period:]
        return sum(recent_k_values) / self.d_period
    
    def is_overbought(self, k_value: float) -> bool:
        """
        Check if %K value indicates overbought conditions.
        
        Args:
            k_value: The %K value to check
            
        Returns:
            True if %K >= overbought_level
        """
        return k_value >= self.overbought_level
    
    def is_oversold(self, k_value: float) -> bool:
        """
        Check if %K value indicates oversold conditions.
        
        Args:
            k_value: The %K value to check
            
        Returns:
            True if %K <= oversold_level
        """
        return k_value <= self.oversold_level


def calculate_stochastic(
    data: List[OHLCV],
    period: int = 14,
    d_period: int = 3,
    slowing_period: int = 3,
    overbought_level: float = 80.0,
    oversold_level: float = 20.0,
) -> Optional[StochasticResult]:
    """
    Convenience function to calculate Stochastic Oscillator.
    
    Args:
        data: List of OHLCV candlestick data
        period: Number of periods for %K calculation
        d_period: Number of periods for %D SMA calculation
        slowing_period: Number of periods for %K smoothing
        overbought_level: Level considered overbought
        oversold_level: Level considered oversold
        
    Returns:
        StochasticResult or None if calculation fails
    """
    indicator = Stochastic(
        period=period,
        d_period=d_period,
        slowing_period=slowing_period,
        overbought_level=overbought_level,
        oversold_level=oversold_level,
    )
    return indicator.calculate(data)
