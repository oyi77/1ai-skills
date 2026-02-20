"""
Ichimoku Kinko Hyo (Cloud Chart) Indicator

Comprehensive technical indicator system that provides multiple signals
for trend direction, momentum, and support/resistance levels.

Components:
- Tenkan-shi (Conversion Line): Short-term momentum
- Kijun-shi (Base Line): Medium-term trend direction
- Senkou Span A (Leading Span A): First cloud boundary
- Senkou Span B (Leading Span B): Second cloud boundary
- Chikou Span (Lagging Span): Confirmation line
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple

from .base import Indicator
from .utils import validate_period, extract_prices
from ..brokers.base import OHLCV


@dataclass
class IchimokuResult:
    """
    Result container for Ichimoku Kinko Hyo calculation.

    Attributes:
        tenkan: Conversion Line value (short-term momentum)
        kijun: Base Line value (medium-term trend)
        senkou_a: Leading Span A (first cloud boundary)
        senkou_b: Leading Span B (second cloud boundary)
        chikou: Lagging Span (confirmation line)
        tenkan_period: Period used for Tenkan calculation
        kijun_period: Period used for Kijun calculation
        senkou_b_period: Period used for Senkou B calculation
        cloud_future: Number of periods cloud is projected into future
    """

    tenkan: float
    kijun: float
    senkou_a: float
    senkou_b: float
    chikou: float
    tenkan_period: int
    kijun_period: int
    senkou_b_period: int
    cloud_future: int = 26

    def is_bullish(self) -> bool:
        """
        Check if Ichimoku indicates bullish conditions.

        Returns:
            True if price is above the cloud (Tenkan > Kijun and price > Senkou A/B)
        """
        return self.tenkan > self.kijun

    def is_bearish(self) -> bool:
        """
        Check if Ichimoku indicates bearish conditions.

        Returns:
            True if price is below the cloud (Tenkan < Kijun and price < Senkou A/B)
        """
        return self.tenkan < self.kijun

    def is_above_cloud(self, current_close: float) -> bool:
        """
        Check if current price is above the cloud.

        Args:
            current_close: Current closing price

        Returns:
            True if price is above both Senkou A and Senkou B
        """
        return current_close > self.senkou_a and current_close > self.senkou_b

    def is_below_cloud(self, current_close: float) -> bool:
        """
        Check if current price is below the cloud.

        Args:
            current_close: Current closing price

        Returns:
            True if price is below both Senkou A and Senkou B
        """
        return current_close < self.senkou_a and current_close < self.senkou_b

    def is_in_cloud(self, current_close: float) -> bool:
        """
        Check if current price is inside the cloud.

        Args:
            current_close: Current closing price

        Returns:
            True if price is between Senkou A and Senkou B
        """
        return (
            self.senkou_a <= current_close <= self.senkou_b
            or self.senkou_b <= current_close <= self.senkou_a
        )

    def get_cloud_direction(self) -> str:
        """
        Get the direction of the cloud (Kumo).

        Returns:
            "bullish" if Senkou A > Senkou B, "bearish" if Senkou B > Senkou A, "neutral" if equal
        """
        if self.senkou_a > self.senkou_b:
            return "bullish"
        elif self.senkou_b > self.senkou_a:
            return "bearish"
        return "neutral"

    def get_signal(self, current_close: float) -> str:
        """
        Get overall Ichimoku signal based on all components.

        Args:
            current_close: Current closing price

        Returns:
            Signal string: "buy", "sell", "neutral", or "caution"
        """
        bullish_signals = 0
        bearish_signals = 0

        # Tenkan-Kijun cross signal
        if self.tenkan > self.kijun:
            bullish_signals += 1
        elif self.tenkan < self.kijun:
            bearish_signals += 1

        # Price vs cloud position
        if self.is_above_cloud(current_close):
            bullish_signals += 2
        elif self.is_below_cloud(current_close):
            bearish_signals += 2

        # Cloud direction
        cloud_dir = self.get_cloud_direction()
        if cloud_dir == "bullish":
            bullish_signals += 1
        elif cloud_dir == "bearish":
            bearish_signals += 1

        # Chikou position (confirming with price 26 periods ago would be ideal,
        # but we use current close for simplified signal)
        if self.chikou > current_close:
            bearish_signals += 1
        elif self.chikou < current_close:
            bullish_signals += 1

        if bullish_signals >= 4:
            return "buy"
        elif bearish_signals >= 4:
            return "sell"
        elif bullish_signals >= 2 or bearish_signals >= 2:
            return "caution"
        return "neutral"

    def __repr__(self) -> str:
        signal = self.get_signal(self.senkou_a)  # Use Senkou A as proxy for current price
        return (
            f"Ichimoku(tenkan={self.tenkan:.2f}, kijun={self.kijun:.2f}, "
            f"senkou_a={self.senkou_a:.2f}, senkou_b={self.senkou_b:.2f}, "
            f"chikou={self.chikou:.2f}, signal={signal})"
        )


class Ichimoku(Indicator):
    """
    Ichimoku Kinko Hyo (Cloud Chart) indicator.

    A comprehensive technical analysis indicator that provides multiple
    signals for trend identification and trading decisions.

    Standard Parameters (for stocks/indices):
        - Tenkan period: 9
        - Kijun period: 26
        - Senkou B period: 52

    Forex-Optimized Parameters (recommended for forex):
        - Tenkan period: 8
        - Kijun period: 29
        - Senkou B period: 34

    Components:
        1. Tenkan-shi (Conversion Line): (Highest High + Lowest Low) / 2 over short period
        2. Kijun-shi (Base Line): (Highest High + Lowest Low) / 2 over medium period
        3. Senkou Span A: (Tenkan + Kijun) / 2, plotted 26 periods ahead
        4. Senkou Span B: (Highest High + Lowest Low) / 2 over long period, plotted 26 ahead
        5. Chikou Span: Close price plotted 26 periods behind

    Trading Signals:
        - Buy: Tenkan crosses above Kijun, price above cloud, cloud bullish
        - Sell: Tenkan crosses below Kijun, price below cloud, cloud bearish
        - Caution: Mixed signals or price in cloud
        - Neutral: No clear trend

    Attributes:
        tenkan_period: Period for Tenkan-shi calculation (default: 9 for standard, 8 for forex)
        kijun_period: Period for Kijun-shi calculation (default: 26 for standard, 29 for forex)
        senkou_b_period: Period for Senkou Span B calculation (default: 52 for standard, 34 for forex)
        cloud_future: Periods to project cloud into future (default: 26)
        forex_mode: Use forex-optimized parameters (8, 29, 34) instead of standard (9, 26, 52)
    """

    def __init__(
        self,
        tenkan_period: int = 9,
        kijun_period: int = 26,
        senkou_b_period: int = 52,
        cloud_future: int = 26,
        forex_mode: bool = False,
    ):
        """
        Initialize Ichimoku indicator.

        Args:
            tenkan_period: Period for Tenkan-shi (Conversion Line) calculation
            kijun_period: Period for Kijun-shi (Base Line) calculation
            senkou_b_period: Period for Senkou Span B (Leading Span B) calculation
            cloud_future: Number of periods to project cloud into future
            forex_mode: If True, use forex-optimized parameters (8, 29, 34)
        """
        # Apply forex-optimized parameters if requested
        if forex_mode:
            tenkan_period = 8
            kijun_period = 29
            senkou_b_period = 34

        super().__init__(
            tenkan_period=tenkan_period,
            kijun_period=kijun_period,
            senkou_b_period=senkou_b_period,
            cloud_future=cloud_future,
            forex_mode=forex_mode,
        )

        self.tenkan_period = tenkan_period
        self.kijun_period = kijun_period
        self.senkou_b_period = senkou_b_period
        self.cloud_future = cloud_future
        self.forex_mode = forex_mode

    def get_required_period(self) -> int:
        """
        Get minimum number of candles required for calculation.

        Returns:
            Minimum number of candles needed (max period + cloud_future)
        """
        max_period = max(self.tenkan_period, self.kijun_period, self.senkou_b_period)
        return max_period + self.cloud_future

    def calculate(self, data: List[OHLCV]) -> Optional[IchimokuResult]:
        """
        Calculate Ichimoku Kinko Hyo from OHLCV data.

        Args:
            data: List of OHLCV candlestick data (oldest to newest)

        Returns:
            IchimokuResult with all component values, or None if insufficient data

        Raises:
            ValueError: If data is invalid or insufficient
        """
        self.validate_input(data)

        required = self.get_required_period()
        if len(data) < required:
            raise ValueError(
                f"Ichimoku requires at least {required} candles "
                f"(max period {max(self.tenkan_period, self.kijun_period, self.senkou_b_period)} "
                f"+ {self.cloud_future} for cloud projection), got {len(data)}"
            )

        # Extract high and low prices
        highs = extract_prices(data, "high")
        lows = extract_prices(data, "low")
        closes = extract_prices(data, "close")

        # Calculate Tenkan (Conversion Line)
        tenkan = self._calculate_tenkan(highs, lows)

        # Calculate Kijun (Base Line)
        kijun = self._calculate_kijun(highs, lows)

        # Calculate Senkou Span A (Leading Span A)
        senkou_a = self._calculate_senkou_a(tenkan, kijun)

        # Calculate Senkou Span B (Leading Span B)
        senkou_b = self._calculate_senkou_b(highs, lows)

        # Calculate Chikou (Lagging Span) - close price 26 periods ago
        chikou = self._calculate_chikou(closes)

        return IchimokuResult(
            tenkan=tenkan,
            kijun=kijun,
            senkou_a=senkou_a,
            senkou_b=senkou_b,
            chikou=chikou,
            tenkan_period=self.tenkan_period,
            kijun_period=self.kijun_period,
            senkou_b_period=self.senkou_b_period,
            cloud_future=self.cloud_future,
        )

    def _calculate_tenkan(self, highs: List[float], lows: List[float]) -> float:
        """
        Calculate Tenkan-shi (Conversion Line).

        Formula: (Highest High + Lowest Low) / 2 over period

        Args:
            highs: List of high prices
            lows: List of low prices

        Returns:
            Tenkan value
        """
        period = self.tenkan_period
        high_slice = highs[-period:]
        low_slice = lows[-period:]

        highest_high = max(high_slice)
        lowest_low = min(low_slice)

        return (highest_high + lowest_low) / 2

    def _calculate_kijun(self, highs: List[float], lows: List[float]) -> float:
        """
        Calculate Kijun-shi (Base Line).

        Formula: (Highest High + Lowest Low) / 2 over longer period

        Args:
            highs: List of high prices
            lows: List of low prices

        Returns:
            Kijun value
        """
        period = self.kijun_period
        high_slice = highs[-period:]
        low_slice = lows[-period:]

        highest_high = max(high_slice)
        lowest_low = min(low_slice)

        return (highest_high + lowest_low) / 2

    def _calculate_senkou_a(self, tenkan: float, kijun: float) -> float:
        """
        Calculate Senkou Span A (Leading Span A).

        Formula: (Tenkan + Kijun) / 2, plotted 26 periods ahead

        Args:
            tenkan: Tenkan value
            kijun: Kijun value

        Returns:
            Senkou A value (already projected forward)
        """
        return (tenkan + kijun) / 2

    def _calculate_senkou_b(self, highs: List[float], lows: List[float]) -> float:
        """
        Calculate Senkou Span B (Leading Span B).

        Formula: (Highest High + Lowest Low) / 2 over longest period,
        plotted 26 periods ahead

        Args:
            highs: List of high prices
            lows: List of low prices

        Returns:
            Senkou B value (already projected forward)
        """
        period = self.senkou_b_period
        high_slice = highs[-period:]
        low_slice = lows[-period:]

        highest_high = max(high_slice)
        lowest_low = min(low_slice)

        return (highest_high + lowest_low) / 2

    def _calculate_chikou(self, closes: List[float]) -> float:
        """
        Calculate Chikou Span (Lagging Span).

        Formula: Close price plotted 26 periods behind (current close value)

        Note: In the Ichimoku system, Chikou is the current close price
        that will be compared to the cloud 26 periods in the past when
        analyzing historical signals.

        Args:
            closes: List of close prices

        Returns:
            Chikou value (current close)
        """
        return closes[-1]

    def get_cloud_boundaries(
        self, data: List[OHLCV]
    ) -> Tuple[List[float], List[float]]:
        """
        Get cloud boundaries for visualization.

        Returns Senkou A and Senkou B values shifted by cloud_future periods
        to align with current price action.

        Args:
            data: List of OHLCV candlestick data

        Returns:
            Tuple of (senkou_a_list, senkou_b_list) for cloud plotting
        """
        self.validate_input(data)

        if len(data) < self.get_required_period():
            raise ValueError(
                f"Ichimoku requires at least {self.get_required_period()} candles"
            )

        highs = extract_prices(data, "high")
        lows = extract_prices(data, "low")

        # Calculate current values
        tenkan = self._calculate_tenkan(highs, lows)
        kijun = self._calculate_kijun(highs, lows)
        senkou_a = self._calculate_senkou_a(tenkan, kijun)
        senkou_b = self._calculate_senkou_b(highs, lows)

        # Return shifted values for cloud visualization
        # The cloud is projected cloud_future periods ahead
        return [senkou_a] * self.cloud_future, [senkou_b] * self.cloud_future


def calculate_ichimoku(
    data: List[OHLCV],
    tenkan_period: int = 9,
    kijun_period: int = 26,
    senkou_b_period: int = 52,
    cloud_future: int = 26,
    forex_mode: bool = False,
) -> Optional[IchimokuResult]:
    """
    Convenience function to calculate Ichimoku Kinko Hyo.

    Args:
        data: List of OHLCV candlestick data
        tenkan_period: Period for Tenkan-shi calculation
        kijun_period: Period for Kijun-shi calculation
        senkou_b_period: Period for Senkou Span B calculation
        cloud_future: Periods to project cloud into future
        forex_mode: Use forex-optimized parameters (8, 29, 34)

    Returns:
        IchimokuResult or None if calculation fails
    """
    indicator = Ichimoku(
        tenkan_period=tenkan_period,
        kijun_period=kijun_period,
        senkou_b_period=senkou_b_period,
        cloud_future=cloud_future,
        forex_mode=forex_mode,
    )
    return indicator.calculate(data)
