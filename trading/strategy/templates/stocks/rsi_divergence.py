"""
RSI Divergence Detector Strategy

Strategy based on detecting regular RSI divergences between price and RSI.
Entry on bullish/bearish divergence, exit when RSI crosses centerline (50).

Divergence Rules:
- Bullish Divergence: Price makes lower low, RSI makes higher low
- Bearish Divergence: Price makes higher high, RSI makes lower high

Timeframe: Daily
RSI Period: 14 (configurable)
Exit: RSI crosses 50 centerline or opposite signal
"""

from datetime import datetime
from typing import List, Optional, Tuple

from ...brokers.base import OHLCV
from ..base import StrategyTemplate, Signal, SignalType
from ...indicators.rsi import RSI, calculate_rsi


class RSIDivergenceStrategy(StrategyTemplate):
    """
    RSI Divergence Detector Strategy.

    Detects regular bullish and bearish divergences between price action
    and RSI indicator momentum.

    Entry BUY: Price makes lower low, RSI makes higher low (bullish divergence)
    Entry SELL: Price makes higher high, RSI makes lower high (bearish divergence)
    Exit: RSI crosses 50 centerline or opposite divergence signal

    Attributes:
        rsi_period: Period for RSI calculation (default: 14)
        lookback_period: Number of candles to look back for divergence (default: 14)
        overbought_level: RSI level considered overbought (default: 70)
        oversold_level: RSI level considered oversold (default: 30)
    """

    def __init__(
        self,
        symbol: str = "AAPL",
        timeframe: str = "D1",
        rsi_period: int = 14,
        lookback_period: int = 14,
        overbought_level: float = 70.0,
        oversold_level: float = 30.0,
        risk_per_trade: float = 0.02,
        use_trailing_stop: bool = True,
        trailing_stop_pips: float = 50.0,
        config: Optional[dict] = None,
    ):
        super().__init__(
            name="RSIDivergenceStrategy",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )
        self.rsi_period = rsi_period
        self.lookback_period = lookback_period
        self.overbought_level = overbought_level
        self.oversold_level = oversold_level
        self.use_trailing_stop = use_trailing_stop
        self.trailing_stop_pips = trailing_stop_pips

    def calculate_rsi_series(self, ohlcv_data: List[OHLCV]) -> List[float]:
        """
        Calculate RSI values for all candles in the dataset.

        Args:
            ohlcv_data: List of OHLCV candlestick data

        Returns:
            List of RSI values (one per candle, starting from valid period)
        """
        if len(ohlcv_data) < self.rsi_period + 1:
            return []

        rsi_values = []
        # Start from the first candle where RSI can be calculated
        for i in range(self.rsi_period, len(ohlcv_data)):
            data_slice = ohlcv_data[:i + 1]
            result = calculate_rsi(
                data_slice,
                period=self.rsi_period,
                overbought_level=self.overbought_level,
                oversold_level=self.oversold_level,
            )
            if result:
                rsi_values.append(result.value)
            else:
                rsi_values.append(50.0)  # Neutral default

        return rsi_values

    def detect_divergence(
        self,
        ohlcv_data: List[OHLCV],
        rsi_values: List[float],
        current_idx: int
    ) -> Tuple[Optional[str], Optional[float], Optional[float]]:
        """
        Detect bullish or bearish divergence at current candle.

        Compares current price/RSI swing with previous swing within lookback period.

        Args:
            ohlcv_data: List of OHLCV candlestick data
            rsi_values: List of calculated RSI values
            current_idx: Current candle index

        Returns:
            Tuple of (divergence_type, entry_price, confidence)
            divergence_type: "bullish", "bearish", or None
        """
        if current_idx < self.lookback_period + self.rsi_period:
            return None, None, None

        # Get the actual RSI index (offset by rsi_period)
        rsi_idx = current_idx - self.rsi_period
        if rsi_idx < 0 or rsi_idx >= len(rsi_values):
            return None, None, None

        current_rsi = rsi_values[rsi_idx]
        current_price = ohlcv_data[current_idx].close

        # Find swing highs and lows in lookback period
        swing_high_idx = None
        swing_low_idx = None
        swing_high_price = None
        swing_low_price = None
        swing_high_rsi = None
        swing_low_rsi = None

        # Look for swing high (local maximum in lookback period)
        for i in range(rsi_idx - self.lookback_period, rsi_idx):
            if i < 0 or i >= len(rsi_values):
                continue
            price = ohlcv_data[i].close
            rsi = rsi_values[i]

            if swing_high_price is None or price > swing_high_price:
                swing_high_price = price
                swing_high_rsi = rsi
                swing_high_idx = i

        # Look for swing low (local minimum in lookback period)
        for i in range(rsi_idx - self.lookback_period, rsi_idx):
            if i < 0 or i >= len(rsi_values):
                continue
            price = ohlcv_data[i].close
            rsi = rsi_values[i]

            if swing_low_price is None or price < swing_low_price:
                swing_low_price = price
                swing_low_rsi = rsi
                swing_low_idx = i

        # Check for bullish divergence (price lower low, RSI higher low)
        if swing_low_price is not None and swing_low_rsi is not None:
            if current_price < swing_low_price and current_rsi > swing_low_rsi:
                # Bullish divergence detected
                # Only valid if RSI is in oversold territory or crossing up
                if current_rsi < 50:  # Strengthening the signal
                    return "bullish", current_price, 0.75

        # Check for bearish divergence (price higher high, RSI lower high)
        if swing_high_price is not None and swing_high_rsi is not None:
            if current_price > swing_high_price and current_rsi < swing_high_rsi:
                # Bearish divergence detected
                # Only valid if RSI is in overbought territory or crossing down
                if current_rsi > 50:  # Strengthening the signal
                    return "bearish", current_price, 0.75

        return None, None, None

    def calculate_atr(
        self,
        ohlcv_data: List[OHLCV],
        period: int = 14
    ) -> float:
        """Calculate Average True Range for stop loss placement."""
        if len(ohlcv_data) < period + 1:
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

        return sum(true_ranges[-period:]) / period if true_ranges else 0.0

    def entry_conditions(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if RSI divergence entry criteria are met.

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        if current_idx < self.lookback_period + self.rsi_period:
            return False, None

        # Calculate RSI series
        rsi_values = self.calculate_rsi_series(ohlcv_data)
        if not rsi_values:
            return False, None

        # Detect divergence
        divergence_type, entry_price, confidence = self.detect_divergence(
            ohlcv_data, rsi_values, current_idx
        )

        if divergence_type is None or entry_price is None:
            return False, None

        current = ohlcv_data[current_idx]
        atr = self.calculate_atr(ohlcv_data)

        if divergence_type == "bullish":
            # Bullish divergence - BUY signal
            stop_loss = current.low - (atr * 2)
            risk = entry_price - stop_loss
            take_profit = entry_price + (risk * 2)

            return True, Signal(
                timestamp=current.time,
                symbol=self.symbol,
                timeframe=self.timeframe,
                signal_type=SignalType.BUY,
                price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                confidence=confidence,
                metadata={
                    "type": "bullish_divergence",
                    "rsi_value": rsi_values[-1] if rsi_values else 50.0,
                    "atr": atr,
                }
            )

        elif divergence_type == "bearish":
            # Bearish divergence - SELL signal
            stop_loss = current.high + (atr * 2)
            risk = stop_loss - entry_price
            take_profit = entry_price - (risk * 2)

            return True, Signal(
                timestamp=current.time,
                symbol=self.symbol,
                timeframe=self.timeframe,
                signal_type=SignalType.SELL,
                price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                confidence=confidence,
                metadata={
                    "type": "bearish_divergence",
                    "rsi_value": rsi_values[-1] if rsi_values else 50.0,
                    "atr": atr,
                }
            )

        return False, None

    def exit_conditions(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int,
        position
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if exit criteria are met.

        Exit when:
        - RSI crosses 50 centerline (opposite momentum)
        - Opposite divergence signal

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            position: Current position to check

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        if current_idx < self.lookback_period + self.rsi_period:
            return False, None

        # Calculate RSI series
        rsi_values = self.calculate_rsi_series(ohlcv_data)
        if len(rsi_values) < 2:
            return False, None

        current_rsi = rsi_values[-1]
        prev_rsi = rsi_values[-2]
        current = ohlcv_data[current_idx]

        if position.side == "LONG":
            # Exit long when RSI crosses below 50 (momentum reversal)
            if prev_rsi >= 50 and current_rsi < 50:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.8,
                    metadata={"reason": "rsi_centerline_cross_down"}
                )

            # Also check for opposite divergence (bearish)
            divergence_type, _, _ = self.detect_divergence(
                ohlcv_data, rsi_values, current_idx
            )
            if divergence_type == "bearish":
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.85,
                    metadata={"reason": "bearish_divergence_exit"}
                )

        elif position.side == "SHORT":
            # Exit short when RSI crosses above 50 (momentum reversal)
            if prev_rsi <= 50 and current_rsi > 50:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.8,
                    metadata={"reason": "rsi_centerline_cross_up"}
                )

            # Also check for opposite divergence (bullish)
            divergence_type, _, _ = self.detect_divergence(
                ohlcv_data, rsi_values, current_idx
            )
            if divergence_type == "bullish":
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.85,
                    metadata={"reason": "bullish_divergence_exit"}
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

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            entry_price: Planned entry price
            stop_loss: Stop loss price
            account_balance: Current account balance

        Returns:
            Position size (units/lots)
        """
        if stop_loss == entry_price:
            return 0.0

        stop_loss_pips = self.calculate_stop_loss_pips(
            entry_price, stop_loss, is_long=entry_price > stop_loss
        )

        return self.calculate_position_size_from_risk(
            account_balance=account_balance,
            stop_loss_pips=stop_loss_pips,
        )

    def get_required_candles(self) -> int:
        """
        Get number of candles required for signal generation.

        Returns:
            Minimum number of candles needed
        """
        return self.lookback_period + self.rsi_period + 14

    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        if not super().validate_config():
            return False

        if self.rsi_period < 2:
            self.logger.error(f"rsi_period ({self.rsi_period}) must be >= 2")
            return False

        if self.lookback_period < 5:
            self.logger.error(f"lookback_period ({self.lookback_period}) must be >= 5")
            return False

        if self.overbought_level <= self.oversold_level:
            self.logger.error(
                f"overbought_level ({self.overbought_level}) must be > "
                f"oversold_level ({self.oversold_level})"
            )
            return False

        return True
