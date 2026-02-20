"""
Golden Cross Screener Strategy

Strategy based on 50/200 SMA crossover - a classic trend-following indicator.
Widely used in stock trading for identifying major trend changes.

Entry BUY: 50 SMA crosses above 200 SMA (golden cross) - bullish signal
Entry SELL: 50 SMA crosses below 200 SMA (death cross) - bearish signal
Exit: Opposite crossover or trailing stop loss

Timeframe: Daily-Weekly (optimized for swing trading)
Risk Management: ATR-based stop loss with trailing stop support
"""

from datetime import datetime
from typing import List, Optional, Tuple

from trading.brokers.base import OHLCV
from trading.strategy.templates.base import StrategyTemplate, Signal, SignalType


class GoldenCrossStrategy(StrategyTemplate):
    """
    Golden Cross Screener Strategy for stocks.

    Uses the classic 50/200 Simple Moving Average crossover to identify
    major trend changes. The golden cross (50 SMA crosses above 200 SMA)
    is one of the most widely-followed bullish signals in technical analysis.

    Entry Conditions:
        BUY: 50 SMA crosses above 200 SMA (golden cross)
        SELL: 50 SMA crosses below 200 SMA (death cross)

    Exit Conditions:
        - Opposite crossover (death cross for long, golden cross for short)
        - Price closes beyond opposite SMA
        - Trailing stop triggered

    Timeframe:
        - Daily: Primary for swing trading signals
        - Weekly: For longer-term trend confirmation

    Risk Management:
        - Stop loss: ATR-based (2x ATR for stocks)
        - Take profit: 2:1 risk-reward ratio
        - Trailing stop: Optional, configurable distance

    Parameters:
        symbol: Stock symbol (e.g., AAPL, MSFT)
        timeframe: Chart timeframe (D1, W1 recommended)
        fast_sma_period: Fast SMA period (default: 50)
        slow_sma_period: Slow SMA period (default: 200)
        risk_per_trade: Risk percentage per trade (default: 2%)
        use_trailing_stop: Enable trailing stop loss (default: True)
        trailing_stop_percent: Trailing stop distance in percent (default: 5%)
        atr_period: ATR period for stop loss calculation (default: 14)
    """

    def __init__(
        self,
        symbol: str = "SPY",
        timeframe: str = "D1",
        fast_sma_period: int = 50,
        slow_sma_period: int = 200,
        risk_per_trade: float = 0.02,
        use_trailing_stop: bool = True,
        trailing_stop_percent: float = 5.0,
        atr_period: int = 14,
        config: Optional[dict] = None,
    ):
        """
        Initialize Golden Cross Strategy.

        Args:
            symbol: Stock symbol to trade (default: SPY)
            timeframe: Chart timeframe - D1 or W1 recommended (default: D1)
            fast_sma_period: Fast SMA period (default: 50)
            slow_sma_period: Slow SMA period (default: 200)
            risk_per_trade: Risk per trade as fraction (default: 0.02 = 2%)
            use_trailing_stop: Enable trailing stop (default: True)
            trailing_stop_percent: Trailing stop distance in percent (default: 5%)
            atr_period: ATR period for volatility-based stops (default: 14)
            config: Additional configuration options
        """
        super().__init__(
            name="GoldenCrossStrategy",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )

        # SMA periods - configurable but defaults to classic 50/200
        self.fast_sma_period = fast_sma_period
        self.slow_sma_period = slow_sma_period

        # Trailing stop settings
        self.use_trailing_stop = use_trailing_stop
        self.trailing_stop_percent = trailing_stop_percent

        # ATR settings for stop loss
        self.atr_period = atr_period

    def calculate_sma(self, ohlcv_data: List[OHLCV], period: int) -> Optional[float]:
        """
        Calculate Simple Moving Average for close prices.

        Args:
            ohlcv_data: List of OHLCV candlestick data
            period: SMA period

        Returns:
            SMA value or None if insufficient data
        """
        if len(ohlcv_data) < period:
            return None

        closes = [c.close for c in ohlcv_data[-period:]]
        return sum(closes) / period

    def calculate_sma_series(
        self, ohlcv_data: List[OHLCV], period: int
    ) -> List[Optional[float]]:
        """
        Calculate SMA series for all available data points.

        Args:
            ohlcv_data: List of OHLCV candlestick data
            period: SMA period

        Returns:
            List of SMA values (None for insufficient data at start)
        """
        sma_series: List[Optional[float]] = []

        for i in range(len(ohlcv_data)):
            if i < period - 1:
                sma_series.append(None)
            else:
                window = ohlcv_data[i - period + 1 : i + 1]
                closes = [c.close for c in window]
                sma_series.append(sum(closes) / period)

        return sma_series

    def calculate_atr(
        self, ohlcv_data: List[OHLCV], period: int = None
    ) -> float:
        """
        Calculate Average True Range for volatility-based stops.

        Args:
            ohlcv_data: List of OHLCV candlestick data
            period: ATR period (uses instance default if None)

        Returns:
            ATR value
        """
        atr_period = period or self.atr_period

        if len(ohlcv_data) < atr_period + 1:
            return 0.0

        true_ranges = []
        for i in range(1, len(ohlcv_data)):
            high = ohlcv_data[i].high
            low = ohlcv_data[i].low
            prev_close = ohlcv_data[i - 1].close

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            true_ranges.append(tr)

        return sum(true_ranges[-atr_period:]) / atr_period if true_ranges else 0.0

    def calculate_sma_crossover(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Tuple[Optional[float], Optional[float], str]:
        """
        Calculate SMA values and detect crossover at current index.

        Args:
            ohlcv_data: List of OHLCV data
            current_idx: Current candle index

        Returns:
            Tuple of (fast_sma_current, slow_sma_current, crossover_type)
            crossover_type: "golden" (bullish), "death" (bearish), or "none"
        """
        if current_idx < self.slow_sma_period:
            return None, None, "none"

        # Calculate current SMAs
        fast_sma_curr = self.calculate_sma(
            ohlcv_data[:current_idx + 1], self.fast_sma_period
        )
        slow_sma_curr = self.calculate_sma(
            ohlcv_data[:current_idx + 1], self.slow_sma_period
        )

        # Calculate previous SMAs (at previous candle)
        fast_sma_prev = self.calculate_sma(
            ohlcv_data[:current_idx], self.fast_sma_period
        )
        slow_sma_prev = self.calculate_sma(
            ohlcv_data[:current_idx], self.slow_sma_period
        )

        if fast_sma_curr is None or slow_sma_curr is None:
            return None, None, "none"

        # Detect crossover
        if fast_sma_prev is not None and slow_sma_prev is not None:
            # Golden cross: fast SMA crosses above slow SMA (bullish)
            if fast_sma_prev <= slow_sma_prev and fast_sma_curr > slow_sma_curr:
                return fast_sma_curr, slow_sma_curr, "golden"

            # Death cross: fast SMA crosses below slow SMA (bearish)
            elif fast_sma_prev >= slow_sma_prev and fast_sma_curr < slow_sma_curr:
                return fast_sma_curr, slow_sma_curr, "death"

        return fast_sma_curr, slow_sma_curr, "none"

    def get_required_candles(self) -> int:
        """
        Get minimum number of candles required for signal generation.

        Returns:
            Number of candles needed (slow SMA period + ATR buffer)
        """
        return self.slow_sma_period + self.atr_period + 10

    def entry_conditions(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if entry criteria are met.

        BUY: Golden cross detected (50 SMA crosses above 200 SMA)
        SELL: Death cross detected (50 SMA crosses below 200 SMA)

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        if current_idx < self.slow_sma_period:
            return False, None

        current = ohlcv_data[current_idx]
        fast_sma, slow_sma, crossover_type = self.calculate_sma_crossover(
            ohlcv_data, current_idx
        )

        if crossover_type == "none" or fast_sma is None or slow_sma is None:
            return False, None

        # Calculate ATR for stop loss
        atr = self.calculate_atr(ohlcv_data)

        if crossover_type == "golden":
            # Golden cross - BULLISH signal
            entry_price = current.close
            # Stop loss: Below recent low or 2x ATR below entry
            stop_loss = min(current.low - atr * 2, fast_sma - atr * 2)
            risk = entry_price - stop_loss
            # Take profit: 2:1 risk-reward
            take_profit = entry_price + risk * 2

            return True, Signal(
                timestamp=current.time,
                symbol=self.symbol,
                timeframe=self.timeframe,
                signal_type=SignalType.BUY,
                price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                confidence=0.75,
                metadata={
                    "type": "golden_cross",
                    "fast_sma": fast_sma,
                    "slow_sma": slow_sma,
                    "atr": atr,
                    "crossover_type": "golden",
                    "reason": "50 SMA crossed above 200 SMA - bullish signal",
                }
            )

        elif crossover_type == "death":
            # Death cross - BEARISH signal
            entry_price = current.close
            # Stop loss: Above recent high or 2x ATR above entry
            stop_loss = max(current.high + atr * 2, fast_sma + atr * 2)
            risk = stop_loss - entry_price
            # Take profit: 2:1 risk-reward
            take_profit = entry_price - risk * 2

            return True, Signal(
                timestamp=current.time,
                symbol=self.symbol,
                timeframe=self.timeframe,
                signal_type=SignalType.SELL,
                price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                confidence=0.75,
                metadata={
                    "type": "death_cross",
                    "fast_sma": fast_sma,
                    "slow_sma": slow_sma,
                    "atr": atr,
                    "crossover_type": "death",
                    "reason": "50 SMA crossed below 200 SMA - bearish signal",
                }
            )

        return False, None

    def exit_conditions(
        self, ohlcv_data: List[OHLCV], current_idx: int, position
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if exit criteria are met for existing position.

        Exit conditions:
        - Opposite crossover detected
        - Price closes beyond opposite SMA
        - Trailing stop triggered (if enabled)

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            position: Current position to check

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        if current_idx < self.slow_sma_period:
            return False, None

        current = ohlcv_data[current_idx]
        fast_sma, slow_sma, crossover_type = self.calculate_sma_crossover(
            ohlcv_data, current_idx
        )

        if fast_sma is None or slow_sma is None:
            return False, None

        # Check for opposite crossover
        if position.side == "LONG":
            # Exit long on death cross (opposite crossover)
            if crossover_type == "death":
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.85,
                    metadata={
                        "reason": "death_cross_exit",
                        "crossover_type": "death",
                        "fast_sma": fast_sma,
                        "slow_sma": slow_sma,
                    }
                )

            # Exit if price closes below slow SMA (200 SMA)
            if current.close < slow_sma:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.7,
                    metadata={
                        "reason": "price_below_slow_sma",
                        "slow_sma": slow_sma,
                    }
                )

            # Check trailing stop if enabled
            if self.use_trailing_stop:
                trailing_stop_price = position.entry_price * (
                    1 - self.trailing_stop_percent / 100
                )
                if current.close < trailing_stop_price:
                    return True, Signal(
                        timestamp=current.time,
                        symbol=self.symbol,
                        timeframe=self.timeframe,
                        signal_type=SignalType.CLOSE_LONG,
                        price=current.close,
                        confidence=0.8,
                        metadata={
                            "reason": "trailing_stop_triggered",
                            "trailing_stop_price": trailing_stop_price,
                        }
                    )

        elif position.side == "SHORT":
            # Exit short on golden cross (opposite crossover)
            if crossover_type == "golden":
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.85,
                    metadata={
                        "reason": "golden_cross_exit",
                        "crossover_type": "golden",
                        "fast_sma": fast_sma,
                        "slow_sma": slow_sma,
                    }
                )

            # Exit if price closes above slow SMA (200 SMA)
            if current.close > slow_sma:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.7,
                    metadata={
                        "reason": "price_above_slow_sma",
                        "slow_sma": slow_sma,
                    }
                )

            # Check trailing stop if enabled
            if self.use_trailing_stop:
                trailing_stop_price = position.entry_price * (
                    1 + self.trailing_stop_percent / 100
                )
                if current.close > trailing_stop_price:
                    return True, Signal(
                        timestamp=current.time,
                        symbol=self.symbol,
                        timeframe=self.timeframe,
                        signal_type=SignalType.CLOSE_SHORT,
                        price=current.close,
                        confidence=0.8,
                        metadata={
                            "reason": "trailing_stop_triggered",
                            "trailing_stop_price": trailing_stop_price,
                        }
                    )

        return False, None

    def position_sizing(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int,
        entry_price: float,
        stop_loss: float,
        account_balance: float
    ) -> float:
        """
        Calculate position size based on risk management.

        Uses the standard risk formula:
        position_size = (account_balance * risk_per_trade) / stop_loss_distance

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            entry_price: Planned entry price
            stop_loss: Stop loss price
            account_balance: Current account balance

        Returns:
            Position size (number of shares/units)
        """
        if stop_loss == entry_price or entry_price <= 0:
            return 0.0

        # Calculate stop loss distance
        stop_loss_distance = abs(entry_price - stop_loss)

        if stop_loss_distance <= 0:
            return 0.0

        # Risk amount in currency
        risk_amount = account_balance * self.risk_per_trade

        # Position size = risk / stop_loss_distance
        position_size = risk_amount / stop_loss_distance

        # Round down to whole shares for stocks
        return int(position_size)

    def validate_config(self) -> bool:
        """
        Validate strategy configuration.

        Returns:
            True if configuration is valid
        """
        if not super().validate_config():
            return False

        # Validate SMA periods
        if self.fast_sma_period >= self.slow_sma_period:
            self.logger.error(
                f"fast_sma_period ({self.fast_sma_period}) must be "
                f"less than slow_sma_period ({self.slow_sma_period})"
            )
            return False

        if self.fast_sma_period < 10:
            self.logger.error(
                f"fast_sma_period ({self.fast_sma_period}) too small, minimum 10"
            )
            return False

        if self.slow_sma_period < 50:
            self.logger.error(
                f"slow_sma_period ({self.slow_sma_period}) too small, minimum 50"
            )
            return False

        # Validate trailing stop
        if self.trailing_stop_percent < 0:
            self.logger.error(
                f"trailing_stop_percent ({self.trailing_stop_percent}) cannot be negative"
            )
            return False

        # Validate ATR period
        if self.atr_period < 1:
            self.logger.error(f"atr_period ({self.atr_period}) must be >= 1")
            return False

        return True
