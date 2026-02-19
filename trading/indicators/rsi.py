"""
Relative Strength Index (RSI) Indicator

Technical indicator that measures the speed and magnitude of recent price changes
to evaluate overbought or oversold conditions.
"""

from typing import List, Optional
from dataclasses import dataclass

from .base import Indicator
from .utils import validate_period, extract_prices, calculate_change
from ..brokers.base import OHLCV


@dataclass
class RSIResult:
    """Result container for RSI calculation."""
    
    value: float
    period: int
    overbought_level: float
    oversold_level: float
    
    def is_overbought(self) -> bool:
        """Check if RSI indicates overbought conditions."""
        return self.value >= self.overbought_level
    
    def is_oversold(self) -> bool:
        """Check if RSI indicates oversold conditions."""
        return self.value <= self.oversold_level
    
    def __repr__(self) -> str:
        status = ""
        if self.is_overbought():
            status = " (overbought)"
        elif self.is_oversold():
            status = " (oversold)"
        return f"RSI({self.value:.2f}){status}"


class RSI(Indicator):
    """
    Relative Strength Index (RSI) indicator.
    
    RSI is a momentum oscillator that measures the speed and magnitude
    of price movements. It ranges from 0 to 100.
    
    Standard interpretation:
    - RSI > 70: Overbought conditions (potential sell signal)
    - RSI < 30: Oversold conditions (potential buy signal)
    - RSI between 30-70: Neutral zone
    
    Formula:
        RS = Average Gain / Average Loss
        RSI = 100 - (100 / (1 + RS))
    
    The first RSI calculation uses simple average, subsequent calculations
    use smoothed moving average (Wilder's smoothing).
    
    Attributes:
        period: Number of periods for calculation (default: 14)
        overbought_level: Level considered overbought (default: 70)
        oversold_level: Level considered oversold (default: 30)
    """
    
    def __init__(
        self,
        period: int = 14,
        overbought_level: float = 70.0,
        oversold_level: float = 30.0,
    ):
        """
        Initialize RSI indicator.
        
        Args:
            period: Number of periods for RSI calculation (default: 14)
            overbought_level: Level considered overbought (default: 70)
            oversold_level: Level considered oversold (default: 30)
        """
        super().__init__(
            period=period,
            overbought_level=overbought_level,
            oversold_level=oversold_level,
        )
        self.period = period
        self.overbought_level = overbought_level
        self.oversold_level = oversold_level
    
    def get_required_period(self) -> int:
        """
        Get minimum number of candles required for calculation.
        
        Returns:
            Minimum number of candles needed (period + 1 for price change calculation)
        """
        return self.period + 1
    
    def calculate(self, data: List[OHLCV]) -> Optional[RSIResult]:
        """
        Calculate RSI from OHLCV data.
        
        Args:
            data: List of OHLCV candlestick data
            
        Returns:
            RSIResult with calculated RSI value and helper methods,
            or None if insufficient data
            
        Raises:
            ValueError: If data is invalid
        """
        self.validate_input(data)
        validate_period(self.period, len(data))
        
        # Need at least period + 1 candles to calculate price changes
        if len(data) < self.get_required_period():
            raise ValueError(
                f"RSI requires at least {self.get_required_period()} candles, "
                f"got {len(data)}"
            )
        
        # Extract closing prices
        closes = extract_prices(data, "close")
        
        # Calculate price changes
        changes = calculate_change(closes)
        
        # Calculate RSI using Wilder's smoothing method
        rsi_value = self._calculate_rsi(changes)
        
        return RSIResult(
            value=rsi_value,
            period=self.period,
            overbought_level=self.overbought_level,
            oversold_level=self.oversold_level,
        )
    
    def _calculate_rsi(self, changes: List[float]) -> float:
        """
        Calculate RSI using Wilder's smoothing method.
        
        For the first RSI calculation, we use simple average.
        For subsequent calculations, we use smoothed moving average.
        
        Args:
            changes: List of price changes (first element is typically 0.0)
            
        Returns:
            RSI value (0-100)
        """
        # Skip the first element (which is 0.0 as it has no previous value)
        valid_changes = changes[1:]
        
        # Separate gains and losses
        gains = [max(0.0, change) for change in valid_changes]
        losses = [max(0.0, -change) for change in valid_changes]
        
        # Calculate initial averages using simple average
        avg_gain = sum(gains[:self.period]) / self.period
        avg_loss = sum(losses[:self.period]) / self.period
        
        # Apply Wilder's smoothing for remaining periods
        for i in range(self.period, len(gains)):
            avg_gain = (avg_gain * (self.period - 1) + gains[i]) / self.period
            avg_loss = (avg_loss * (self.period - 1) + losses[i]) / self.period
        
        # Calculate RS and RSI
        if avg_loss == 0:
            # If no losses, RSI is 100 (pure upward movement)
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))
        
        # Clamp RSI to valid range [0, 100]
        return max(0.0, min(100.0, rsi))
    
    def is_overbought(self, rsi_value: float) -> bool:
        """
        Check if RSI value indicates overbought conditions.
        
        Args:
            rsi_value: The RSI value to check
            
        Returns:
            True if RSI >= overbought_level
        """
        return rsi_value >= self.overbought_level
    
    def is_oversold(self, rsi_value: float) -> bool:
        """
        Check if RSI value indicates oversold conditions.
        
        Args:
            rsi_value: The RSI value to check
            
        Returns:
            True if RSI <= oversold_level
        """
        return rsi_value <= self.oversold_level


def calculate_rsi(
    data: List[OHLCV],
    period: int = 14,
    overbought_level: float = 70.0,
    oversold_level: float = 30.0,
) -> Optional[RSIResult]:
    """
    Convenience function to calculate RSI.
    
    Args:
        data: List of OHLCV candlestick data
        period: Number of periods for RSI calculation
        overbought_level: Level considered overbought
        oversold_level: Level considered oversold
        
    Returns:
        RSIResult or None if calculation fails
    """
    indicator = RSI(
        period=period,
        overbought_level=overbought_level,
        oversold_level=oversold_level,
    )
    return indicator.calculate(data)
