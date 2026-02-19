"""
Bollinger Bands Indicator

Implementation of Bollinger Bands technical indicator.
Bollinger Bands consist of a middle band (SMA) and two outer bands
(standard deviations away from the middle band).
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import statistics

from ..brokers.base import OHLCV
from .base import Indicator
from .utils import extract_prices


@dataclass
class BollingerBandsResult:
    """Result container for Bollinger Bands calculation."""
    
    upper: Optional[float] = None
    middle: Optional[float] = None
    lower: Optional[float] = None
    bandwidth: Optional[float] = None
    percent_b: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'upper': self.upper,
            'middle': self.middle,
            'lower': self.lower,
            'bandwidth': self.bandwidth,
            'percent_b': self.percent_b
        }


class BollingerBands(Indicator):
    """
    Bollinger Bands indicator.
    
    Bollinger Bands are volatility bands placed above and below a moving average.
    The bands widen when volatility increases and narrow when volatility decreases.
    
    Standard Bollinger Bands (20, 2):
    - Middle Band = 20-period SMA
    - Upper Band = Middle + (2 * StdDev)
    - Lower Band = Middle - (2 * StdDev)
    - Band Width = (Upper - Lower) / Middle
    - %B = (Close - Lower) / (Upper - Lower)
    
    Args:
        period: Number of periods for the SMA (default: 20)
        multiplier: Standard deviation multiplier (default: 2.0)
    """

    def __init__(self, period: int = 20, multiplier: float = 2.0):
        """
        Initialize Bollinger Bands indicator.
        
        Args:
            period: Number of periods for the moving average (default: 20)
            multiplier: Standard deviation multiplier (default: 2.0)
        """
        super().__init__(period=period, multiplier=multiplier)
        self.period = period
        self.multiplier = multiplier
        self._name = f"BB_{period}_{multiplier}"

    def calculate(self, data: List[OHLCV]) -> List[BollingerBandsResult]:
        """
        Calculate Bollinger Bands values for the given OHLCV data.
        
        Args:
            data: List of OHLCV candlestick data
            
        Returns:
            List of BollingerBandsResult. First (period-1) values have None for all fields
        """
        self.validate_input(data)
        
        if len(data) < self.period:
            raise ValueError(
                f"{self.name}: Insufficient data. Need at least {self.period} candles, got {len(data)}"
            )

        closes = extract_prices(data, "close")
        results: List[BollingerBandsResult] = []

        for i in range(len(closes)):
            if i < self.period - 1:
                # Not enough data for calculation
                results.append(BollingerBandsResult())
            else:
                window = closes[i - self.period + 1 : i + 1]
                result = self._calculate_bands(window, closes[i])
                results.append(result)

        return results

    def _calculate_bands(self, prices: List[float], current_price: float) -> BollingerBandsResult:
        """
        Calculate Bollinger Bands for a single window of prices.
        
        Args:
            prices: List of closing prices for the period
            current_price: Current closing price for %B calculation
            
        Returns:
            BollingerBandsResult with all calculated values
        """
        # Middle Band = SMA
        middle = sum(prices) / len(prices)
        
        # Standard Deviation
        std_dev = statistics.stdev(prices)
        
        # Upper and Lower Bands
        upper = middle + (self.multiplier * std_dev)
        lower = middle - (self.multiplier * std_dev)
        
        # Band Width = (Upper - Lower) / Middle
        bandwidth = (upper - lower) / middle if middle != 0 else None
        
        # %B = (Price - Lower) / (Upper - Lower)
        band_range = upper - lower
        percent_b = (current_price - lower) / band_range if band_range != 0 else None
        
        return BollingerBandsResult(
            upper=upper,
            middle=middle,
            lower=lower,
            bandwidth=bandwidth,
            percent_b=percent_b
        )

    def get_required_period(self) -> int:
        """Get minimum number of candles required for calculation."""
        return self.period

    def is_price_above_upper(self, result: BollingerBandsResult, price: float) -> bool:
        """
        Check if price is above the upper band.
        
        Args:
            result: BollingerBandsResult
            price: Price to check
            
        Returns:
            True if price is above upper band
        """
        return result.upper is not None and price > result.upper

    def is_price_below_lower(self, result: BollingerBandsResult, price: float) -> bool:
        """
        Check if price is below the lower band.
        
        Args:
            result: BollingerBandsResult
            price: Price to check
            
        Returns:
            True if price is below lower band
        """
        return result.lower is not None and price < result.lower

    def is_price_inside_bands(self, result: BollingerBandsResult, price: float) -> bool:
        """
        Check if price is inside the bands (inclusive).
        
        Args:
            result: BollingerBandsResult
            price: Price to check
            
        Returns:
            True if price is between lower and upper bands (inclusive)
        """
        if result.lower is None or result.upper is None:
            return False
        return result.lower <= price <= result.upper

    def get_position_within_bands(self, result: BollingerBandsResult, price: float) -> Optional[float]:
        """
        Get the relative position of price within the bands (0-1 scale).
        
        0 = at lower band
        0.5 = at middle band
        1 = at upper band
        
        Args:
            result: BollingerBandsResult
            price: Price to check
            
        Returns:
            Position as float between 0 and 1, or None if bands not calculated
        """
        if result.lower is None or result.upper is None:
            return None
        
        band_range = result.upper - result.lower
        if band_range == 0:
            return None
            
        position = (price - result.lower) / band_range
        return max(0.0, min(1.0, position))  # Clamp between 0 and 1

    def __repr__(self) -> str:
        """String representation of indicator."""
        return f"{self._name}(period={self.period}, multiplier={self.multiplier})"
