"""
Momentum Elder FOREX Strategy

Strategy based on the Momentum Elder method from ForexTester.
Combines EMA(19) for trend direction and Momentum(18, close, 100) for signal generation.

Entry BUY:
- Closing price above EMA(19) (uptrend)
- Momentum crosses 100 from bottom up

Entry SELL:
- Closing price below EMA(19) (downtrend)
- Momentum crosses 100 from top to bottom

Exit:
- Opposite momentum crossover
- Price closes beyond EMA in opposite direction

Timeframe: H1 minimum
Support major pairs: EUR/USD, GBP/USD, USD/JPY (configurable)
"""

from datetime import datetime
from typing import List, Optional, Tuple

from trading.brokers.base import OHLCV
from trading.strategy.templates.base import StrategyTemplate, Signal, SignalType
from trading.indicators.moving_averages import EMA


class MomentumElderStrategy(StrategyTemplate):
    """
    Momentum Elder FOREX strategy implementation.

    Combines EMA(19) for trend direction and Momentum(18, close, 100) for signal generation.

    Attributes:
        ema_period: Period for EMA (default: 19)
        momentum_period: Period for Momentum calculation (default: 18)
        momentum_baseline: Baseline level for Momentum (default: 100)
        min_timeframe: Minimum timeframe (default: H1)
    """

    # Valid timeframes for this strategy (H1 minimum)
    VALID_TIMEFRAMES = ["H1", "H4", "D1", "W1"]

    # Major FOREX pairs supported
    MAJOR_PAIRS = [
        "EUR/USD",
        "GBP/USD",
        "USD/JPY",
        "USD/CHF",
        "AUD/USD",
        "USD/CAD",
        "NZD/USD",
        "EUR/GBP",
        "EUR/JPY",
        "GBP/JPY",
    ]

    def __init__(
        self,
        symbol: str = "EUR/USD",
        timeframe: str = "H1",
        ema_period: int = 19,
        momentum_period: int = 18,
        momentum_baseline: float = 100.0,
        risk_per_trade: float = 0.02,
        config: Optional[dict] = None,
    ):
        """
        Initialize Momentum Elder strategy.

        Args:
            symbol: Trading symbol (default: EUR/USD)
            timeframe: Chart timeframe (default: H1)
            ema_period: EMA period (default: 19)
            momentum_period: Period for Momentum calculation (default: 18)
            momentum_baseline: Baseline level for Momentum (default: 100)
            risk_per_trade: Risk per trade as fraction (default: 0.02 = 2%)
            config: Additional configuration dictionary
        """
        super().__init__(
            name="MomentumElderStrategy",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )

        # Indicator parameters
        self.ema_period = ema_period
        self.momentum_period = momentum_period
        self.momentum_baseline = momentum_baseline

        # Initialize EMA indicator
        self.ema_indicator = EMA(period=ema_period)

    def calculate_momentum(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Optional[float]:
        """
        Calculate Momentum value.

        Momentum formula: (Current Close - Close N periods ago) / Close N periods ago * 100

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            Momentum value or None if insufficient data
        """
        if current_idx < self.momentum_period:
            return None

        current_close = ohlcv_data[current_idx].close
        past_close = ohlcv_data[current_idx - self.momentum_period].close

        if past_close == 0:
            return None

        momentum = ((current_close - past_close) / past_close) * 100
        return momentum

    def calculate_momentum_previous(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Optional[float]:
        """
        Calculate previous Momentum value (for crossover detection).

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            Previous Momentum value or None if insufficient data
        """
        if current_idx < self.momentum_period + 1:
            return None

        prev_close = ohlcv_data[current_idx - 1].close
        past_close = ohlcv_data[current_idx - 1 - self.momentum_period].close

        if past_close == 0:
            return None

        momentum = ((prev_close - past_close) / past_close) * 100
        return momentum

    def _get_ema_values(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Tuple[Optional[float], Optional[float]]:
        """
        Get EMA values for current and previous candle.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            Tuple of (current_ema, prev_ema)
        """
        if current_idx < self.ema_period:
            return None, None

        # Get all EMA values up to current index
        ema_values = self.ema_indicator.calculate(ohlcv_data[: current_idx + 1])

        if ema_values[-1] is None:
            return None, None

        current_ema = ema_values[-1]
        prev_ema = ema_values[-2] if len(ema_values) > 1 else None

        return current_ema, prev_ema

    def _is_uptrend(self, ohlcv_data: List[OHLCV], current_idx: int) -> bool:
        """
        Check if market is in uptrend based on EMA position.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            True if price is above EMA (uptrend)
        """
        current_ema, _ = self._get_ema_values(ohlcv_data, current_idx)
        if current_ema is None:
            return False

        current_price = ohlcv_data[current_idx].close
        return current_price > current_ema

    def _is_downtrend(self, ohlcv_data: List[OHLCV], current_idx: int) -> bool:
        """
        Check if market is in downtrend based on EMA position.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            True if price is below EMA (downtrend)
        """
        current_ema, _ = self._get_ema_values(ohlcv_data, current_idx)
        if current_ema is None:
            return False

        current_price = ohlcv_data[current_idx].close
        return current_price < current_ema

    def _detect_momentum_crossover(
        self, ohlcv_data: List[OHLCV], current_idx: int, direction: str
    ) -> bool:
        """
        Detect Momentum crossover of baseline.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index
            direction: "up" for bullish crossover, "down" for bearish crossover

        Returns:
            True if crossover detected
        """
        current_momentum = self.calculate_momentum(ohlcv_data, current_idx)
        prev_momentum = self.calculate_momentum_previous(ohlcv_data, current_idx)

        if current_momentum is None or prev_momentum is None:
            return False

        if direction == "up":
            # Bullish crossover: Momentum crosses 100 from bottom up
            return prev_momentum <= self.momentum_baseline and current_momentum > self.momentum_baseline
        elif direction == "down":
            # Bearish crossover: Momentum crosses 100 from top to bottom
            return prev_momentum >= self.momentum_baseline and current_momentum < self.momentum_baseline

        return False

    def _calculate_atr(
        self, ohlcv_data: List[OHLCV], period: int = 14
    ) -> float:
        """
        Calculate Average True Range for stop loss placement.

        Args:
            ohlcv_data: OHLCV data
            period: ATR period (default: 14)

        Returns:
            ATR value
        """
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
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if entry criteria are met for Momentum Elder strategy.

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        current = ohlcv_data[current_idx]

        # Check minimum index requirements
        min_required = max(self.ema_period, self.momentum_period + 1) + 5
        if current_idx < min_required:
            return False, None

        # Check for BUY entry
        if self._is_uptrend(ohlcv_data, current_idx):
            if self._detect_momentum_crossover(ohlcv_data, current_idx, direction="up"):
                # Calculate stop loss and take profit
                current_ema, _ = self._get_ema_values(ohlcv_data, current_idx)
                atr = self._calculate_atr(ohlcv_data)

                entry_price = current.close
                stop_loss = current.low - (atr * 2) if atr > 0 else current.close * 0.02
                risk = entry_price - stop_loss
                take_profit = entry_price + (risk * 2)

                current_momentum = self.calculate_momentum(ohlcv_data, current_idx)

                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.BUY,
                    price=entry_price,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    confidence=0.8,
                    metadata={
                        "type": "momentum_elder_buy",
                        "ema_period": self.ema_period,
                        "momentum_period": self.momentum_period,
                        "momentum_baseline": self.momentum_baseline,
                        "ema_value": current_ema,
                        "momentum_value": current_momentum,
                    }
                )

        # Check for SELL entry
        if self._is_downtrend(ohlcv_data, current_idx):
            if self._detect_momentum_crossover(ohlcv_data, current_idx, direction="down"):
                # Calculate stop loss and take profit
                current_ema, _ = self._get_ema_values(ohlcv_data, current_idx)
                atr = self._calculate_atr(ohlcv_data)

                entry_price = current.close
                stop_loss = current.high + (atr * 2) if atr > 0 else current.close * 0.02
                risk = stop_loss - entry_price
                take_profit = entry_price - (risk * 2)

                current_momentum = self.calculate_momentum(ohlcv_data, current_idx)

                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.SELL,
                    price=entry_price,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    confidence=0.8,
                    metadata={
                        "type": "momentum_elder_sell",
                        "ema_period": self.ema_period,
                        "momentum_period": self.momentum_period,
                        "momentum_baseline": self.momentum_baseline,
                        "ema_value": current_ema,
                        "momentum_value": current_momentum,
                    }
                )

        return False, None

    def exit_conditions(
        self, ohlcv_data: List[OHLCV], current_idx: int, position
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if exit criteria are met for Momentum Elder strategy.

        Exit when:
        - Opposite momentum crossover occurs
        - Price closes beyond EMA in opposite direction

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            position: Current position to check

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        current = ohlcv_data[current_idx]

        # Check for opposite momentum crossover
        if position.side == "LONG":
            # Check for bearish momentum crossover (exit long)
            if self._detect_momentum_crossover(ohlcv_data, current_idx, direction="down"):
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.85,
                    metadata={"reason": "momentum_bearish_crossover"}
                )

            # Check if price closed below EMA (trend reversal)
            current_ema, _ = self._get_ema_values(ohlcv_data, current_idx)
            if current_ema is not None and current.close < current_ema:
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.75,
                    metadata={"reason": "price_below_ema"}
                )

        elif position.side == "SHORT":
            # Check for bullish momentum crossover (exit short)
            if self._detect_momentum_crossover(ohlcv_data, current_idx, direction="up"):
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.85,
                    metadata={"reason": "momentum_bullish_crossover"}
                )

            # Check if price closed above EMA (trend reversal)
            current_ema, _ = self._get_ema_values(ohlcv_data, current_idx)
            if current_ema is not None and current.close > current_ema:
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.75,
                    metadata={"reason": "price_above_ema"}
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

        stop_loss_pips = self.calculate_stop_loss_pips(entry_price, stop_loss)

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
        # Need enough candles for EMA and Momentum calculations
        return max(self.ema_period, self.momentum_period + 1) + 20

    def validate_config(self) -> bool:
        """
        Validate strategy configuration.

        Returns:
            True if configuration is valid
        """
        if not super().validate_config():
            return False

        # Validate timeframe
        if self.timeframe not in self.VALID_TIMEFRAMES:
            self.logger.warning(
                f"Timeframe {self.timeframe} is below minimum H1. "
                f"Strategy may not perform optimally."
            )

        # Validate EMA period
        if self.ema_period <= 0:
            self.logger.error(f"Invalid ema_period: {self.ema_period}")
            return False

        # Validate momentum period
        if self.momentum_period <= 0:
            self.logger.error(f"Invalid momentum_period: {self.momentum_period}")
            return False

        # Validate momentum baseline
        if self.momentum_baseline <= 0:
            self.logger.error(f"Invalid momentum_baseline: {self.momentum_baseline}")
            return False

        return True

    def get_supported_symbols(self) -> List[str]:
        """
        Get list of supported trading symbols.

        Returns:
            List of supported symbol strings
        """
        return self.MAJOR_PAIRS.copy()
