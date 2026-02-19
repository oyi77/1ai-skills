"""
MACD (Moving Average Convergence Divergence) Indicator

MACD is a trend-following momentum indicator that shows the relationship
between two moving averages of a security's price.

Formula:
- MACD Line = EMA(fast_period) - EMA(slow_period)
- Signal Line = EMA(signal_period) of MACD Line
- Histogram = MACD Line - Signal Line

Standard parameters: MACD(12, 26, 9)
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from ..brokers.base import OHLCV
from .base import Indicator
from .moving_averages import EMA


@dataclass
class MACDResult:
    """Container for MACD calculation results."""
    macd_line: List[Optional[float]]
    signal_line: List[Optional[float]]
    histogram: List[Optional[float]]


class MACD(Indicator):
    """
    Moving Average Convergence Divergence (MACD) indicator.
    
    MACD is a trend-following momentum indicator that shows the relationship
    between two exponential moving averages of a security's price.
    
    Standard parameters (12, 26, 9):
    - Fast EMA period: 12
    - Slow EMA period: 26
    - Signal EMA period: 9
    
    Components:
    - MACD Line: Difference between fast and slow EMAs
    - Signal Line: EMA of the MACD Line
    - Histogram: Difference between MACD Line and Signal Line
    
    Interpretation:
    - Bullish: MACD Line crosses above Signal Line
    - Bearish: MACD Line crosses below Signal Line
    - Histogram positive: MACD above Signal (bullish momentum)
    - Histogram negative: MACD below Signal (bearish momentum)
    """

    def __init__(
        self,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9
    ):
        """
        Initialize MACD indicator.
        
        Args:
            fast_period: Period for fast EMA (default: 12)
            slow_period: Period for slow EMA (default: 26)
            signal_period: Period for signal line EMA (default: 9)
            
        Raises:
            ValueError: If fast_period >= slow_period or any period <= 0
        """
        super().__init__(
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period
        )
        
        if fast_period <= 0 or slow_period <= 0 or signal_period <= 0:
            raise ValueError("All periods must be positive integers")
            
        if fast_period >= slow_period:
            raise ValueError(
                f"Fast period ({fast_period}) must be less than "
                f"slow period ({slow_period})"
            )
        
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self._name = f"MACD({fast_period},{slow_period},{signal_period})"
        
        # Initialize EMA calculators
        self._fast_ema = EMA(period=fast_period)
        self._slow_ema = EMA(period=slow_period)
        self._signal_ema = EMA(period=signal_period)

    def calculate(self, data: List[OHLCV]) -> MACDResult:
        """
        Calculate MACD values for the given OHLCV data.
        
        Args:
            data: List of OHLCV candlestick data
            
        Returns:
            MACDResult containing macd_line, signal_line, and histogram
            
        Raises:
            ValueError: If insufficient data for calculation
        """
        self.validate_input(data)
        
        min_required = self.get_required_period()
        if len(data) < min_required:
            raise ValueError(
                f"{self.name}: Insufficient data. "
                f"Need at least {min_required} candles, got {len(data)}"
            )

        # Calculate fast and slow EMAs
        fast_ema_values = self._fast_ema.calculate(data)
        slow_ema_values = self._slow_ema.calculate(data)

        # Calculate MACD Line = Fast EMA - Slow EMA
        macd_line: List[Optional[float]] = []
        for fast, slow in zip(fast_ema_values, slow_ema_values):
            if fast is None or slow is None:
                macd_line.append(None)
            else:
                macd_line.append(fast - slow)

        # Calculate Signal Line = EMA of MACD Line
        signal_line = self._calculate_signal_line(macd_line)

        # Calculate Histogram = MACD Line - Signal Line
        histogram: List[Optional[float]] = []
        for macd, signal in zip(macd_line, signal_line):
            if macd is None or signal is None:
                histogram.append(None)
            else:
                histogram.append(macd - signal)

        return MACDResult(
            macd_line=macd_line,
            signal_line=signal_line,
            histogram=histogram
        )

    def _calculate_signal_line(
        self,
        macd_line: List[Optional[float]]
    ) -> List[Optional[float]]:
        """
        Calculate Signal Line as EMA of MACD Line values.
        
        Args:
            macd_line: List of MACD Line values
            
        Returns:
            List of Signal Line values
        """
        signal_line: List[Optional[float]] = []
        prev_signal: Optional[float] = None
        multiplier = 2 / (self.signal_period + 1)

        for i, macd in enumerate(macd_line):
            if macd is None:
                signal_line.append(None)
            elif prev_signal is None:
                # Need at least signal_period valid MACD values for first signal
                # Count valid MACD values up to current index
                valid_macd_count = sum(
                    1 for m in macd_line[:i+1] if m is not None
                )
                if valid_macd_count < self.signal_period:
                    signal_line.append(None)
                else:
                    # First signal is SMA of first 'signal_period' valid MACD values
                    valid_macds = [
                        m for m in macd_line[:i+1] if m is not None
                    ][-self.signal_period:]
                    prev_signal = sum(valid_macds) / self.signal_period
                    signal_line.append(prev_signal)
            else:
                signal_value = (macd * multiplier) + (
                    prev_signal * (1 - multiplier)
                )
                signal_line.append(signal_value)
                prev_signal = signal_value

        return signal_line

    def get_required_period(self) -> int:
        """
        Get minimum number of candles required for calculation.
        
        Returns:
            Minimum number of candles needed
            (slow_period + signal_period - 1 to have enough data for all calculations)
        """
        return self.slow_period + self.signal_period - 1

    def is_bullish(self, result: MACDResult, index: int = -1) -> bool:
        """
        Check if MACD indicates bullish momentum at given index.
        
        Bullish signals:
        - MACD Line crosses above Signal Line
        - Histogram turns positive (MACD > Signal)
        
        Args:
            result: MACDResult from calculate()
            index: Index to check (default: -1 for latest)
            
        Returns:
            True if bullish signal detected
            
        Raises:
            ValueError: If index is out of range
        """
        if not result.macd_line or not result.signal_line:
            return False
            
        idx = index if index >= 0 else len(result.macd_line) + index
        
        if idx < 0 or idx >= len(result.macd_line):
            raise ValueError(f"Index {index} out of range")
            
        if idx == 0:
            # Can't determine crossover with only one data point
            return False
            
        macd_current = result.macd_line[idx]
        macd_previous = result.macd_line[idx - 1]
        signal_current = result.signal_line[idx]
        signal_previous = result.signal_line[idx - 1]
        
        if any(v is None for v in [
            macd_current, macd_previous, signal_current, signal_previous
        ]):
            return False
        
        # Bullish crossover: MACD was below Signal, now above
        return macd_previous <= signal_previous and macd_current > signal_current

    def is_bearish(self, result: MACDResult, index: int = -1) -> bool:
        """
        Check if MACD indicates bearish momentum at given index.
        
        Bearish signals:
        - MACD Line crosses below Signal Line
        - Histogram turns negative (MACD < Signal)
        
        Args:
            result: MACDResult from calculate()
            index: Index to check (default: -1 for latest)
            
        Returns:
            True if bearish signal detected
            
        Raises:
            ValueError: If index is out of range
        """
        if not result.macd_line or not result.signal_line:
            return False
            
        idx = index if index >= 0 else len(result.macd_line) + index
        
        if idx < 0 or idx >= len(result.macd_line):
            raise ValueError(f"Index {index} out of range")
            
        if idx == 0:
            # Can't determine crossover with only one data point
            return False
            
        macd_current = result.macd_line[idx]
        macd_previous = result.macd_line[idx - 1]
        signal_current = result.signal_line[idx]
        signal_previous = result.signal_line[idx - 1]
        
        if any(v is None for v in [
            macd_current, macd_previous, signal_current, signal_previous
        ]):
            return False
        
        # Bearish crossover: MACD was above Signal, now below
        return macd_previous >= signal_previous and macd_current < signal_current

    def get_last_values(self, result: MACDResult) -> Dict[str, Optional[float]]:
        """
        Get the most recent MACD values.
        
        Args:
            result: MACDResult from calculate()
            
        Returns:
            Dictionary with last macd, signal, and histogram values
        """
        return {
            'macd': result.macd_line[-1] if result.macd_line else None,
            'signal': result.signal_line[-1] if result.signal_line else None,
            'histogram': result.histogram[-1] if result.histogram else None
        }
