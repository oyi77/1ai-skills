"""
Funding Rate Reversal Strategy Template

Strategy based on funding rate persistence and mean reversion for crypto.
Crowded positioning from persistent funding often leads to reversals.

Strategy Rules:
- Entry SHORT: Funding persists elevated (>14 days) = reversal signal
- Entry BUY: Funding negative persistence = mean reversion
- Exit: Funding normalization or profit target

Timeframe: Daily-Weekly
Supported Pairs: BTC/USD, ETH/USD
"""

from datetime import datetime
from typing import List, Optional, Tuple

from ....brokers.base import OHLCV
from ..base import StrategyTemplate, Signal, SignalType
from ....data.funding import FundingRateData, PersistenceData


class FundingReversalStrategy(StrategyTemplate):
    """
    Funding Rate Reversal Strategy for Crypto.

    Uses funding rate persistence to identify crowded positioning and
    potential reversals. When funding rates persist elevated for extended
    periods, it often indicates overcrowded trades that are due for reversal.

    Entry Signals:
    - SELL: Positive funding persists >14 days (crowded longs = reversal short)
    - BUY: Negative funding persists (crowded shorts = mean reversion)

    Exit Signals:
    - Funding rate normalizes
    - Profit target reached
    - Stop loss hit
    """

    # Supported trading pairs
    SUPPORTED_PAIRS = ["BTC/USD", "ETH/USD"]

    def __init__(
        self,
        symbol: str = "BTC/USD",
        timeframe: str = "D1",
        persistence_days: int = 14,
        elevated_threshold: float = 0.0005,
        profit_target_pct: float = 0.05,
        risk_per_trade: float = 0.02,
        config: Optional[dict] = None,
    ):
        """
        Initialize Funding Reversal Strategy.

        Args:
            symbol: Trading pair (BTC/USD or ETH/USD)
            timeframe: Timeframe (D1, W1 for daily-weekly)
            persistence_days: Days of elevated funding to trigger signal
            elevated_threshold: Threshold for elevated funding rate
            profit_target_pct: Profit target as percentage
            risk_per_trade: Risk per trade (default 2%)
            config: Additional configuration
        """
        if symbol not in self.SUPPORTED_PAIRS:
            raise ValueError(f"Unsupported symbol: {symbol}. Supported: {self.SUPPORTED_PAIRS}")

        super().__init__(
            name="FundingReversalStrategy",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )
        self.persistence_days = persistence_days
        self.elevated_threshold = elevated_threshold
        self.profit_target_pct = profit_target_pct

        # Initialize funding rate data handler
        self.funding_data = FundingRateData()

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
            prev_close = ohlcv_data[i-1].close

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            true_ranges.append(tr)

        return sum(true_ranges[-period:]) / period if true_ranges else 0.0

    def get_funding_persistence(self) -> PersistenceData:
        """
        Get funding rate persistence data for current symbol.

        Returns:
            PersistenceData with analysis results
        """
        return self.funding_data.calculate_persistence(
            symbol=self.symbol,
            days=30  # Look back 30 days for analysis
        )

    def _calculate_confidence(
        self,
        persistence: PersistenceData,
        current_price: float,
        atr: float
    ) -> float:
        """
        Calculate signal confidence based on persistence and market conditions.

        Args:
            persistence: Funding rate persistence data
            current_price: Current price
            atr: Average True Range

        Returns:
            Confidence score (0.0 to 1.0)
        """
        base_confidence = 0.5

        # Increase confidence based on persistence duration
        if persistence.consecutive_days_elevated >= 21:
            base_confidence = 0.95
        elif persistence.consecutive_days_elevated >= 14:
            base_confidence = 0.85
        elif persistence.consecutive_days_elevated >= 7:
            base_confidence = 0.70
        elif persistence.consecutive_days_elevated >= 3:
            base_confidence = 0.60

        # Adjust for severity
        severity_multipliers = {
            "extreme": 1.0,
            "high": 0.9,
            "medium": 0.75,
            "low": 0.5
        }
        base_confidence *= severity_multipliers.get(persistence.severity, 0.5)

        return min(base_confidence, 1.0)

    def entry_conditions(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if funding reversal entry criteria are met.

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        if current_idx < 1:
            return False, None

        current = ohlcv_data[current_idx]

        # Get funding rate persistence
        persistence = self.get_funding_persistence()

        # Need at least some funding data to make decision
        if persistence.consecutive_days_elevated < 3:
            return False, None

        atr = self.calculate_atr(ohlcv_data[:current_idx+1])

        # Entry SHORT: Positive funding persists elevated (>14 days)
        # This indicates crowded long positions = reversal short signal
        if (
            persistence.direction == "positive" and
            persistence.consecutive_days_elevated >= self.persistence_days
        ):
            entry_price = current.close
            stop_loss = current.high + (atr * 2.0)  # 2x ATR stop loss
            take_profit = current.close * (1 - self.profit_target_pct)

            confidence = self._calculate_confidence(
                persistence=persistence,
                current_price=current.close,
                atr=atr
            )

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
                    "type": "funding_reversal_short",
                    "persistence_days": persistence.consecutive_days_elevated,
                    "funding_direction": persistence.direction,
                    "current_funding_rate": persistence.current_funding_rate,
                    "severity": persistence.severity,
                    "atr": atr,
                    "is_warning": persistence.is_warning
                }
            )

        # Entry BUY: Negative funding persists = mean reversion
        # This indicates crowded short positions = buy signal
        if (
            persistence.direction == "negative" and
            persistence.consecutive_days_elevated >= 3
        ):
            entry_price = current.close
            stop_loss = current.low - (atr * 2.0)  # 2x ATR stop loss
            take_profit = current.close * (1 + self.profit_target_pct)

            # Higher confidence for negative funding (mean reversion)
            base_confidence = 0.6
            if persistence.consecutive_days_elevated >= 14:
                base_confidence = 0.90
            elif persistence.consecutive_days_elevated >= 7:
                base_confidence = 0.75

            confidence = min(base_confidence, 1.0)

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
                    "type": "funding_mean_reversion",
                    "persistence_days": persistence.consecutive_days_elevated,
                    "funding_direction": persistence.direction,
                    "current_funding_rate": persistence.current_funding_rate,
                    "severity": persistence.severity,
                    "atr": atr
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
        Check if exit criteria are met for existing position.

        Exit triggers:
        - Funding rate normalizes
        - Profit target reached
        - Stop loss hit

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            position: Current position to check

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        if current_idx < 1:
            return False, None

        current = ohlcv_data[current_idx]
        persistence = self.get_funding_persistence()

        # Stop loss exits are handled by broker, but we check for early exit
        if position.side == "LONG":
            # Check if funding has normalized (no longer negative persistence)
            if persistence.direction != "negative" or persistence.consecutive_days_elevated < 3:
                # Funding normalization - consider taking profit or partial exit
                if current.close >= position.take_profit:
                    return True, Signal(
                        timestamp=current.timestamp,
                        symbol=self.symbol,
                        timeframe=self.timeframe,
                        signal_type=SignalType.CLOSE_LONG,
                        price=current.close,
                        confidence=0.9,
                        metadata={"reason": "profit_target"}
                    )

            # Stop loss hit
            if current.low <= position.stop_loss:
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=position.stop_loss,
                    confidence=1.0,
                    metadata={"reason": "stop_loss"}
                )

        elif position.side == "SHORT":
            # Check if funding has normalized (positive funding no longer elevated)
            if persistence.direction != "positive" or persistence.consecutive_days_elevated < self.persistence_days:
                # Funding normalization - consider taking profit
                if current.close <= position.take_profit:
                    return True, Signal(
                        timestamp=current.timestamp,
                        symbol=self.symbol,
                        timeframe=self.timeframe,
                        signal_type=SignalType.CLOSE_SHORT,
                        price=current.close,
                        confidence=0.9,
                        metadata={"reason": "profit_target"}
                    )

            # Stop loss hit
            if current.high >= position.stop_loss:
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=position.stop_loss,
                    confidence=1.0,
                    metadata={"reason": "stop_loss"}
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
            Position size (units)
        """
        if stop_loss == entry_price:
            return 0.0

        # Calculate stop loss distance as percentage
        stop_loss_distance = abs(entry_price - stop_loss) / entry_price

        if stop_loss_distance == 0:
            return 0.0

        # Risk amount in account currency
        risk_amount = account_balance * self.risk_per_trade

        # Position size = risk_amount / stop_loss_distance
        position_size = risk_amount / stop_loss_distance

        return position_size

    def get_required_candles(self) -> int:
        """Get number of candles required for signal generation."""
        return 30  # Need enough candles for ATR calculation

    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        if not super().validate_config():
            return False

        if self.symbol not in self.SUPPORTED_PAIRS:
            self.logger.error(f"Unsupported symbol: {self.symbol}")
            return False

        if self.persistence_days < 1:
            self.logger.error(f"Invalid persistence_days: {self.persistence_days}")
            return False

        if self.elevated_threshold <= 0:
            self.logger.error(f"Invalid elevated_threshold: {self.elevated_threshold}")
            return False

        if self.profit_target_pct <= 0:
            self.logger.error(f"Invalid profit_target_pct: {self.profit_target_pct}")
            return False

        return True

    def get_strategy_info(self) -> dict:
        """
        Get current strategy status and funding analysis.

        Returns:
            Dictionary with strategy information
        """
        persistence = self.get_funding_persistence()

        return {
            "strategy": self.name,
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "funding_analysis": {
                "current_rate": persistence.current_funding_rate,
                "direction": persistence.direction,
                "consecutive_days_elevated": persistence.consecutive_days_elevated,
                "is_warning": persistence.is_warning,
                "severity": persistence.severity
            },
            "configuration": {
                "persistence_days": self.persistence_days,
                "elevated_threshold": self.elevated_threshold,
                "profit_target_pct": self.profit_target_pct,
                "risk_per_trade": self.risk_per_trade
            },
            "supported_pairs": self.SUPPORTED_PAIRS
        }
