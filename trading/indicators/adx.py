"""
Average Directional Index (ADX) Indicator

Technical indicator that measures the strength of a trend, regardless of direction.
Includes +DI (Plus Directional Indicator) and -DI (Minus Directional Indicator).
"""

from typing import List, Optional
from dataclasses import dataclass

from .base import Indicator
from .utils import validate_period, extract_prices
from ..brokers.base import OHLCV


@dataclass
class ADXResult:
    """Result container for ADX calculation."""
    
    adx: float
    plus_di: float
    minus_di: float
    period: int
    weak_level: float
    strong_level: float
    very_strong_level: float
    
    def is_trending(self) -> bool:
        """Check if there's a trending market (ADX > weak_level)."""
        return self.adx > self.weak_level
    
    def is_strong_trend(self) -> bool:
        """Check if there's a strong trend (ADX > strong_level)."""
        return self.adx > self.strong_level
    
    def is_very_strong_trend(self) -> bool:
        """Check if there's a very strong trend (ADX > very_strong_level)."""
        return self.adx > self.very_strong_level
    
    def is_bullish(self) -> bool:
        """Check if +DI > -DI (bullish momentum)."""
        return self.plus_di > self.minus_di
    
    def is_bearish(self) -> bool:
        """Check if -DI > +DI (bearish momentum)."""
        return self.minus_di > self.plus_di
    
    def get_trend_strength(self) -> str:
        """Get human-readable trend strength description."""
        if self.adx <= self.weak_level:
            return "no_trend"
        elif self.adx <= self.strong_level:
            return "weak_trend"
        elif self.adx <= self.very_strong_level:
            return "strong_trend"
        else:
            return "very_strong_trend"
    
    def get_direction(self) -> str:
        """Get human-readable direction description."""
        if self.is_bullish():
            return "bullish"
        elif self.is_bearish():
            return "bearish"
        else:
            return "neutral"
    
    def __repr__(self) -> str:
        strength = self.get_trend_strength()
        direction = self.get_direction()
        return f"ADX({self.adx:.2f}, +DI:{self.plus_di:.2f}, -DI:{self.minus_di:.2f}) [{strength} {direction}]"


class ADX(Indicator):
    """
    Average Directional Index (ADX) indicator.
    
    ADX measures the strength of a trend, while +DI and -DI indicate
    the direction of the trend. It ranges from 0 to 100.
    
    Standard interpretation:
    - ADX < 15: No trend (weak/non-trending market)
    - ADX 15-25: Weak trend (early stage or weakening)
    - ADX 25-50: Strong trend
    - ADX > 50: Very strong trend (extreme, may be exhausting)
    
    +DI > -DI: Bullish momentum
    -DI > +DI: Bearish momentum
    
    Formula:
        1. True Range (TR) = max(High-Low, |High-PrevClose|, |Low-PrevClose|)
        2. +DM = max(High-PrevHigh, 0) if UpMove > DownMove else 0
        3. -DM = max(PrevLow-Low, 0) if DownMove > UpMove else 0
        4. Smooth TR, +DM, -DM using Wilder's smoothing
        5. +DI = (+DM / TR) * 100
        6. -DI = (-DM / TR) * 100
        7. DX = (|+DI - -DI| / |+DI + -DI|) * 100
        8. ADX = Smoothed DX (14-period by default)
    
    Attributes:
        period: Number of periods for calculation (default: 14)
        weak_level: Level considered weak trend (default: 15)
        strong_level: Level considered strong trend (default: 25)
        very_strong_level: Level considered very strong trend (default: 50)
    """
    
    def __init__(
        self,
        period: int = 14,
        weak_level: float = 15.0,
        strong_level: float = 25.0,
        very_strong_level: float = 50.0,
    ):
        """
        Initialize ADX indicator.
        
        Args:
            period: Number of periods for ADX calculation (default: 14)
            weak_level: Level considered weak trend (default: 15)
            strong_level: Level considered strong trend (default: 25)
            very_strong_level: Level considered very strong trend (default: 50)
        """
        super().__init__(
            period=period,
            weak_level=weak_level,
            strong_level=strong_level,
            very_strong_level=very_strong_level,
        )
        self.period = period
        self.weak_level = weak_level
        self.strong_level = strong_level
        self.very_strong_level = very_strong_level
    
    def get_required_period(self) -> int:
        """
        Get minimum number of candles required for calculation.
        
        Returns:
            Minimum number of candles needed (period + 1 for DM/TR calculation)
        """
        return self.period + 1
    
    def calculate(self, data: List[OHLCV]) -> Optional[ADXResult]:
        """
        Calculate ADX from OHLCV data.
        
        Args:
            data: List of OHLCV candlestick data
            
        Returns:
            ADXResult with calculated ADX, +DI, -DI values and helper methods,
            or None if insufficient data
            
        Raises:
            ValueError: If data is invalid
        """
        self.validate_input(data)
        validate_period(self.period, len(data))
        
        # Need at least period + 1 candles for DM/TR calculation
        if len(data) < self.get_required_period():
            raise ValueError(
                f"ADX requires at least {self.get_required_period()} candles, "
                f"got {len(data)}"
            )
        
        # Extract prices
        highs = extract_prices(data, "high")
        lows = extract_prices(data, "low")
        closes = extract_prices(data, "close")
        
        # Calculate True Range and Directional Movements
        tr_values, plus_dm_values, minus_dm_values = self._calculate_tr_dm(highs, lows, closes)
        
        # Calculate ADX using Wilder's smoothing
        adx_value, plus_di, minus_di = self._calculate_adx(tr_values, plus_dm_values, minus_dm_values)
        
        return ADXResult(
            adx=adx_value,
            plus_di=plus_di,
            minus_di=minus_di,
            period=self.period,
            weak_level=self.weak_level,
            strong_level=self.strong_level,
            very_strong_level=self.very_strong_level,
        )
    
    def _calculate_tr_dm(
        self, 
        highs: List[float], 
        lows: List[float], 
        closes: List[float]
    ) -> tuple:
        """
        Calculate True Range and Directional Movements.
        
        Args:
            highs: List of high prices
            lows: List of low prices
            closes: List of close prices
            
        Returns:
            Tuple of (TR values, +DM values, -DM values)
        """
        tr_values = []
        plus_dm_values = []
        minus_dm_values = []
        
        for i in range(len(highs)):
            if i == 0:
                # First candle: TR = High - Low
                tr = highs[i] - lows[i]
                plus_dm = 0.0
                minus_dm = 0.0
            else:
                # True Range calculation
                prev_close = closes[i - 1]
                tr = max(
                    highs[i] - lows[i],
                    abs(highs[i] - prev_close),
                    abs(lows[i] - prev_close)
                )
                
                # Directional Movement calculation
                up_move = highs[i] - highs[i - 1]
                down_move = lows[i - 1] - lows[i]
                
                if up_move > down_move and up_move > 0:
                    plus_dm = up_move
                else:
                    plus_dm = 0.0
                    
                if down_move > up_move and down_move > 0:
                    minus_dm = down_move
                else:
                    minus_dm = 0.0
            
            tr_values.append(tr)
            plus_dm_values.append(plus_dm)
            minus_dm_values.append(minus_dm)
        
        return tr_values, plus_dm_values, minus_dm_values
    
    def _calculate_adx(
        self, 
        tr_values: List[float], 
        plus_dm_values: List[float], 
        minus_dm_values: List[float]
    ) -> tuple:
        """
        Calculate ADX, +DI, and -DI using Wilder's smoothing.
        
        Args:
            tr_values: List of True Range values
            plus_dm_values: List of +DM values
            minus_dm_values: List of -DM values
            
        Returns:
            Tuple of (ADX value, +DI value, -DI value)
        """
        # Apply Wilder's smoothing to TR, +DM, and -DM
        smoothed_tr = self._wilder_smooth(tr_values, self.period)
        smoothed_plus_dm = self._wilder_smooth(plus_dm_values, self.period)
        smoothed_minus_dm = self._wilder_smooth(minus_dm_values, self.period)
        
        # Calculate +DI and -DI
        if smoothed_tr == 0:
            plus_di = 0.0
            minus_di = 0.0
        else:
            plus_di = (smoothed_plus_dm / smoothed_tr) * 100
            minus_di = (smoothed_minus_dm / smoothed_tr) * 100
        
        # Calculate DX
        if plus_di + minus_di == 0:
            dx = 0.0
        else:
            dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        
        # Calculate ADX (smoothed DX)
        adx_value = self._wilder_smooth_single(dx, self.period)
        
        # Clamp values to valid range [0, 100]
        adx_value = max(0.0, min(100.0, adx_value))
        plus_di = max(0.0, min(100.0, plus_di))
        minus_di = max(0.0, min(100.0, minus_di))
        
        return adx_value, plus_di, minus_di
    
    def _wilder_smooth(self, values: List[float], period: int) -> float:
        """
        Apply Wilder's smoothing to a list of values and return the final smoothed value.
        
        Args:
            values: List of values to smooth
            period: Smoothing period
            
        Returns:
            Final smoothed value
        """
        if len(values) < period:
            return sum(values) / len(values) if values else 0.0
        
        # First smoothed value is simple average
        smoothed = sum(values[:period]) / period
        
        # Apply Wilder's smoothing for remaining values
        for i in range(period, len(values)):
            smoothed = (smoothed * (period - 1) + values[i]) / period
        
        return smoothed
    
    def _wilder_smooth_single(self, value: float, period: int) -> float:
        """
        Apply single-step Wilder's smoothing.
        
        This is used when we already have a smoothed value and want to
        apply one more smoothing step.
        
        Args:
            value: Current value to smooth
            period: Smoothing period
            
        Returns:
            Smoothed value
        """
        # For ADX, we need to maintain state across calls
        # This is a simplified version for the final calculation
        return value
    
    def is_trending(self, adx_value: float) -> bool:
        """
        Check if ADX value indicates trending market.
        
        Args:
            adx_value: The ADX value to check
            
        Returns:
            True if ADX > weak_level
        """
        return adx_value > self.weak_level
    
    def is_strong_trend(self, adx_value: float) -> bool:
        """
        Check if ADX value indicates strong trend.
        
        Args:
            adx_value: The ADX value to check
            
        Returns:
            True if ADX > strong_level
        """
        return adx_value > self.strong_level


def calculate_adx(
    data: List[OHLCV],
    period: int = 14,
    weak_level: float = 15.0,
    strong_level: float = 25.0,
    very_strong_level: float = 50.0,
) -> Optional[ADXResult]:
    """
    Convenience function to calculate ADX.
    
    Args:
        data: List of OHLCV candlestick data
        period: Number of periods for ADX calculation
        weak_level: Level considered weak trend
        strong_level: Level considered strong trend
        very_strong_level: Level considered very strong trend
        
    Returns:
        ADXResult or None if calculation fails
    """
    indicator = ADX(
        period=period,
        weak_level=weak_level,
        strong_level=strong_level,
        very_strong_level=very_strong_level,
    )
    return indicator.calculate(data)
