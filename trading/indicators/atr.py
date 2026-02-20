"""
Average True Range (ATR) Indicator

Technical indicator that measures market volatility by decomposing the entire
range of an asset price for that period.
"""

from typing import List, Optional
from dataclasses import dataclass

from .base import Indicator
from .utils import validate_period, extract_prices
from ..brokers.base import OHLCV


@dataclass
class ATRResult:
    """Result container for ATR calculation."""
    
    value: float
    period: int
    
    def is_volatile(self, threshold: float = 2.0) -> bool:
        """
        Check if market volatility is high based on threshold.
        
        Args:
            threshold: Multiplier for average volatility (default: 2.0)
            
        Returns:
            True if volatility is above threshold
        """
        return self.value > threshold
    
    def is_low_volatility(self, threshold: float = 0.5) -> bool:
        """
        Check if market volatility is low based on threshold.
        
        Args:
            threshold: Multiplier for low volatility (default: 0.5)
            
        Returns:
            True if volatility is below threshold
        """
        return self.value < threshold
    
    def calculate_stop_loss_distance(
        self, 
        atr_multiplier: float = 2.0,
        price_precision: int = 2
    ) -> float:
        """
        Calculate stop loss distance based on ATR volatility.
        
        Args:
            atr_multiplier: Multiplier for ATR (default: 2.0 for 2x ATR)
            price_precision: Decimal places for rounding
            
        Returns:
            Stop loss distance in price units
        """
        return round(self.value * atr_multiplier, price_precision)
    
    def __repr__(self) -> str:
        volatility_status = ""
        if self.is_volatile():
            volatility_status = " (high volatility)"
        elif self.is_low_volatility():
            volatility_status = " (low volatility)"
        return f"ATR({self.value:.2f}){volatility_status}"


class ATR(Indicator):
    """
    Average True Range (ATR) indicator.
    
    ATR measures market volatility by decomposing the entire range of an
    asset price for that period. It does not indicate price direction,
    only volatility.
    
    Formula:
        True Range (TR) = max(High - Low, |High - Previous Close|, |Low - Previous Close|)
        ATR = Smoothed TR using Wilder's smoothing (14-period default)
    
    The first ATR calculation uses simple average of first TR values.
    Subsequent ATR calculations use Wilder's smoothing method.
    
    Common uses:
        - Stop loss placement: 2x ATR for stop distance
        - Position sizing: Higher ATR = smaller position
        - Market condition assessment: High ATR = trending/moving market
        - Trailing stops: ATR-based trailing stops
    
    Attributes:
        period: Number of periods for calculation (default: 14)
    """
    
    def __init__(self, period: int = 14):
        """
        Initialize ATR indicator.
        
        Args:
            period: Number of periods for ATR calculation (default: 14)
        """
        super().__init__(period=period)
        self.period = period
    
    def get_required_period(self) -> int:
        """
        Get minimum number of candles required for calculation.
        
        Returns:
            Minimum number of candles needed (period + 1 for previous close reference)
        """
        return self.period + 1
    
    def calculate(self, data: List[OHLCV]) -> Optional[ATRResult]:
        """
        Calculate ATR from OHLCV data.
        
        Args:
            data: List of OHLCV candlestick data
            
        Returns:
            ATRResult with calculated ATR value and helper methods,
            or None if insufficient data
            
        Raises:
            ValueError: If data is invalid
        """
        self.validate_input(data)
        validate_period(self.period, len(data))
        
        # Need at least period + 1 candles for True Range calculation
        if len(data) < self.get_required_period():
            raise ValueError(
                f"ATR requires at least {self.get_required_period()} candles, "
                f"got {len(data)}"
            )
        
        # Calculate True Range values
        true_ranges = self._calculate_true_ranges(data)
        
        # Calculate ATR using Wilder's smoothing
        atr_value = self._calculate_atr(true_ranges)
        
        return ATRResult(
            value=atr_value,
            period=self.period,
        )
    
    def _calculate_true_ranges(self, data: List[OHLCV]) -> List[float]:
        """
        Calculate True Range values for each candle.
        
        True Range is the greatest of:
        - Current High - Current Low
        - |Current High - Previous Close|
        - |Current Low - Previous Close|
        
        Args:
            data: List of OHLCV candlestick data
            
        Returns:
            List of True Range values
        """
        true_ranges = []
        
        for i in range(len(data)):
            current = data[i]
            
            if i == 0:
                # First candle: use High - Low
                true_range = current.high - current.low
            else:
                previous_close = data[i - 1].close
                
                # Calculate the three components
                high_low_range = current.high - current.low
                high_prev_close = abs(current.high - previous_close)
                low_prev_close = abs(current.low - previous_close)
                
                # True Range is the maximum
                true_range = max(high_low_range, high_prev_close, low_prev_close)
            
            true_ranges.append(true_range)
        
        return true_ranges
    
    def _calculate_atr(self, true_ranges: List[float]) -> float:
        """
        Calculate ATR using Wilder's smoothing method.
        
        For the first ATR calculation, we use simple average.
        For subsequent calculations, we use smoothed moving average.
        
        Args:
            true_ranges: List of True Range values
            
        Returns:
            ATR value
        """
        # Skip the first True Range (it doesn't have previous close reference)
        valid_trs = true_ranges[1:]
        
        # Calculate initial ATR using simple average of first 'period' TR values
        initial_trs = valid_trs[:self.period]
        atr = sum(initial_trs) / self.period
        
        # Apply Wilder's smoothing for remaining periods
        for i in range(self.period, len(valid_trs)):
            atr = (atr * (self.period - 1) + valid_trs[i]) / self.period
        
        return atr
    
    def calculate_stop_loss(
        self, 
        entry_price: float, 
        atr_multiplier: float = 2.0,
        is_long: bool = True
    ) -> float:
        """
        Calculate stop loss price based on ATR volatility.
        
        Args:
            entry_price: Entry price for the position
            atr_multiplier: Multiplier for ATR (default: 2.0)
            is_long: True for long position, False for short
            
        Returns:
            Stop loss price level
        """
        stop_distance = self.calculate_stop_loss_distance(atr_multiplier)
        
        if is_long:
            return entry_price - stop_distance
        else:
            return entry_price + stop_distance
    
    def calculate_trailing_stop(
        self, 
        current_price: float, 
        atr_multiplier: float = 2.0,
        is_long: bool = True
    ) -> float:
        """
        Calculate trailing stop price based on ATR.
        
        Args:
            current_price: Current market price
            atr_multiplier: Multiplier for ATR (default: 2.0)
            is_long: True for long position, False for short
            
        Returns:
            Trailing stop price level
        """
        return self.calculate_stop_loss(
            current_price, 
            atr_multiplier, 
            is_long
        )


def calculate_atr(
    data: List[OHLCV],
    period: int = 14,
) -> Optional[ATRResult]:
    """
    Convenience function to calculate ATR.
    
    Args:
        data: List of OHLCV candlestick data
        period: Number of periods for ATR calculation
        
    Returns:
        ATRResult or None if calculation fails
    """
    indicator = ATR(period=period)
    return indicator.calculate(data)
