"""
Gold-Silver Ratio Mean Reversion Strategy

Pair trading strategy between XAUUSD (Gold) and XAGUSD (Silver).

Concept:
- Gold and silver have a historically correlated relationship
- The ratio (XAUUSD / XAGUSD) oscillates between extremes
- Mean reversion: ratio tends to return to historical mean

Entry Rules:
- Ratio > 80: Short gold, buy silver (silver is cheap relative to gold)
- Ratio < 70: Buy gold, short silver (gold is cheap relative to silver)

Exit Rules:
- Ratio returns to mean (75)

Timeframe: Daily-Weekly for swing trading

Position Sizing:
- Pair trades require hedged positions to match dollar exposure
- Calculate position sizes to equalize dollar risk
"""

from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
import logging

from ...brokers.base import OHLCV
from ..base import StrategyTemplate, Signal, SignalType

logger = logging.getLogger("strategy.templates.gold_silver_ratio")


class GoldSilverRatioStrategy(StrategyTemplate):
    """
    Gold-Silver Ratio Mean Reversion Strategy.

    Implements pair trading between XAUUSD and XAGUSD based on
    the historical gold-silver ratio. The strategy goes long one
    metal and short the other when the ratio reaches extremes,
    exiting when the ratio returns to the mean.

    Default Parameters:
        - ratio_overbought: 80 (short gold, buy silver)
        - ratio_oversold: 70 (buy gold, short silver)
        - ratio_mean: 75 (exit level)
        - lookback_period: 20 (candles for ratio calculation)
    """

    def __init__(
        self,
        symbol: str = "XAUUSD",
        timeframe: str = "D1",
        risk_per_trade: float = 0.02,
        ratio_overbought: float = 80.0,
        ratio_oversold: float = 70.0,
        ratio_mean: float = 75.0,
        lookback_period: int = 20,
        config: Optional[Dict[str, Any]] = None,
    ):
        # Initialize config with strategy parameters
        strategy_config = {
            "ratio_overbought": ratio_overbought,
            "ratio_oversold": ratio_oversold,
            "ratio_mean": ratio_mean,
            "lookback_period": lookback_period,
            "gold_symbol": "XAUUSD",
            "silver_symbol": "XAGUSD",
        }
        if config:
            strategy_config.update(config)

        super().__init__(
            name="GoldSilverRatioStrategy",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=strategy_config,
        )

        self.gold_symbol = "XAUUSD"
        self.silver_symbol = "XAGUSD"
        self.ratio_overbought = ratio_overbought
        self.ratio_oversold = ratio_oversold
        self.ratio_mean = ratio_mean
        self.lookback_period = lookback_period

        # Track pair positions (both legs)
        self.pair_position: Optional[Dict[str, Position]] = None

    def calculate_ratio(
        self,
        gold_data: List[OHLCV],
        silver_data: List[OHLCV],
        current_idx: int
    ) -> Optional[float]:
        """
        Calculate the gold-silver ratio (XAUUSD / XAGUSD).

        Args:
            gold_data: OHLCV data for XAUUSD
            silver_data: OHLCV data for XAGUSD
            current_idx: Current candle index

        Returns:
            Current ratio value or None if insufficient data
        """
        if current_idx < 0:
            return None

        # Use current close prices
        gold_idx = min(current_idx, len(gold_data) - 1)
        silver_idx = min(current_idx, len(silver_data) - 1)

        gold_close = gold_data[gold_idx].close
        silver_close = silver_data[silver_idx].close

        if silver_close <= 0:
            logger.warning("Silver price is zero or negative")
            return None

        ratio = gold_close / silver_close
        return ratio

    def calculate_moving_average_ratio(
        self,
        gold_data: List[OHLCV],
        silver_data: List[OHLCV],
        period: int
    ) -> Optional[float]:
        """
        Calculate the moving average of the gold-silver ratio.

        Args:
            gold_data: OHLCV data for XAUUSD
            silver_data: OHLCV data for XAGUSD
            period: Lookback period for MA

        Returns:
            MA ratio value or None if insufficient data
        """
        if len(gold_data) < period or len(silver_data) < period:
            return None

        ratios = []
        min_len = min(len(gold_data), len(silver_data))
        start_idx = max(0, min_len - period)

        for i in range(start_idx, min_len):
            gold_close = gold_data[i].close
            silver_close = silver_data[i].close

            if silver_close > 0:
                ratio = gold_close / silver_close
                ratios.append(ratio)

        if not ratios:
            return None

        return sum(ratios) / len(ratios)

    def entry_conditions(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if entry criteria are met for pair trade.

        For pair trades, ohlcv_data should contain both gold and silver data
        interleaved or the strategy should be called with combined data.

        Args:
            ohlcv_data: Historical OHLCV data (expects gold then silver)
            current_idx: Current candle index

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        # For pair trading, we need both gold and silver data
        # This implementation expects gold_data and silver_data to be passed
        # via metadata or handled separately

        # Check if we have required data in config
        gold_data = self.config.get("gold_ohlcv_data", [])
        silver_data = self.config.get("silver_ohlcv_data", [])

        if not gold_data or not silver_data:
            # Try to extract from ohlcv_data (first half gold, second half silver)
            mid_point = len(ohlcv_data) // 2
            gold_data = ohlcv_data[:mid_point]
            silver_data = ohlcv_data[mid_point:]

        if len(gold_data) < self.lookback_period or len(silver_data) < self.lookback_period:
            return False, None

        # Get current ratio
        current_ratio = self.calculate_ratio(gold_data, silver_data, current_idx)
        if current_ratio is None:
            return False, None

        # Get MA ratio for trend confirmation
        ma_ratio = self.calculate_moving_average_ratio(
            gold_data, silver_data, self.lookback_period
        )

        current = ohlcv_data[current_idx] if current_idx < len(ohlcv_data) else None
        if current is None:
            return False, None

        # Entry condition: Ratio at extreme
        # Ratio > 80: Short gold, buy silver (silver is cheap)
        if current_ratio >= self.ratio_overbought:
            # Check if we're not already in a position
            if self.pair_position is not None:
                return False, None

            # Short gold, buy silver
            gold_signal = self._create_pair_signal(
                ohlcv_data,
                current_idx,
                "SHORT_GOLD_LONG_SILVER",
                current_ratio,
                ma_ratio,
                current
            )

            if gold_signal:
                return True, gold_signal

        # Ratio < 70: Buy gold, short silver (gold is cheap)
        elif current_ratio <= self.ratio_oversold:
            # Check if we're not already in a position
            if self.pair_position is not None:
                return False, None

            # Buy gold, short silver
            gold_signal = self._create_pair_signal(
                ohlcv_data,
                current_idx,
                "LONG_GOLD_SHORT_SILVER",
                current_ratio,
                ma_ratio,
                current
            )

            if gold_signal:
                return True, gold_signal

        return False, None

    def _create_pair_signal(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int,
        trade_type: str,
        current_ratio: float,
        ma_ratio: Optional[float],
        current_candle: OHLCV
    ) -> Optional[Signal]:
        """
        Create a pair trade signal with proper position sizing.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current index
            trade_type: Type of pair trade
            current_ratio: Current gold-silver ratio
            ma_ratio: Moving average ratio
            current_candle: Current OHLCV candle

        Returns:
            Signal object or None
        """
        gold_data = self.config.get("gold_ohlcv_data", [])
        silver_data = self.config.get("silver_ohlcv_data", [])

        if not gold_data or not silver_data:
            return None

        gold_idx = min(current_idx, len(gold_data) - 1)
        silver_idx = min(current_idx, len(silver_data) - 1)

        gold_price = gold_data[gold_idx].close
        silver_price = silver_data[silver_idx].close

        # Calculate stop loss based on ratio deviation
        if trade_type == "SHORT_GOLD_LONG_SILVER":
            # Short gold at current price
            entry_price = gold_price
            # Stop loss if ratio reverts too far (e.g., back to mean + buffer)
            stop_loss = gold_price * (self.ratio_mean / current_ratio)
            # Take profit when ratio mean reverts
            take_profit = gold_price * (self.ratio_oversold / current_ratio)
        else:  # LONG_GOLD_SHORT_SILVER
            entry_price = gold_price
            stop_loss = gold_price * (self.ratio_mean / current_ratio)
            take_profit = gold_price * (self.ratio_overbought / current_ratio)

        # Calculate position sizes for hedged pair trade
        # Match dollar exposure: gold_lots * gold_price = silver_lots * silver_price
        dollar_exposure = 10000  # Example: $10,000 per leg
        gold_lots = dollar_exposure / gold_price
        silver_lots = dollar_exposure / silver_price

        # Adjust for risk
        risk_amount = 200  # 2% of $10,000 account
        stop_distance = abs(entry_price - stop_loss)
        if stop_distance > 0:
            adjusted_lots = risk_amount / stop_distance
            gold_lots = adjusted_lots
            silver_lots = adjusted_lots * (gold_price / silver_price)

        # Store pair position info
        self.pair_position = {
            "type": trade_type,
            "gold_lots": gold_lots,
            "silver_lots": silver_lots,
            "gold_entry": gold_price,
            "silver_entry": silver_price,
            "ratio": current_ratio,
        }

        return Signal(
            timestamp=current_candle.time,
            symbol=self.symbol,
            timeframe=self.timeframe,
            signal_type=SignalType.SELL if "SHORT" in trade_type else SignalType.BUY,
            price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            confidence=0.75,
            metadata={
                "type": "pair_trade",
                "trade_type": trade_type,
                "gold_symbol": self.gold_symbol,
                "silver_symbol": self.silver_symbol,
                "gold_price": gold_price,
                "silver_price": silver_price,
                "ratio": current_ratio,
                "ma_ratio": ma_ratio,
                "gold_lots": gold_lots,
                "silver_lots": silver_lots,
                "ratio_overbought": self.ratio_overbought,
                "ratio_oversold": self.ratio_oversold,
                "ratio_mean": self.ratio_mean,
            }
        )

    def exit_conditions(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int,
        position: "Position"
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if exit criteria are met for pair trade.

        Exit when ratio returns to mean (75).

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            position: Current position to check

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        if self.pair_position is None:
            return False, None

        gold_data = self.config.get("gold_ohlcv_data", [])
        silver_data = self.config.get("silver_ohlcv_data", [])

        if not gold_data or not silver_data:
            mid_point = len(ohlcv_data) // 2
            gold_data = ohlcv_data[:mid_point]
            silver_data = ohlcv_data[mid_point:]

        if len(gold_data) < 1 or len(silver_data) < 1:
            return False, None

        current_ratio = self.calculate_ratio(gold_data, silver_data, current_idx)
        if current_ratio is None:
            return False, None

        trade_type = self.pair_position["type"]
        current = ohlcv_data[current_idx] if current_idx < len(ohlcv_data) else None
        if current is None:
            return False, None

        # Exit when ratio returns to mean
        mean_tolerance = 2.0  # Exit when within 2 points of mean

        if trade_type == "SHORT_GOLD_LONG_SILVER":
            # Exit when ratio drops toward mean (70-75 range)
            if current_ratio <= (self.ratio_mean + mean_tolerance):
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.85,
                    metadata={
                        "type": "pair_trade_exit",
                        "trade_type": trade_type,
                        "reason": "ratio_mean_reversion",
                        "exit_ratio": current_ratio,
                        "target_ratio": self.ratio_mean,
                        "gold_symbol": self.gold_symbol,
                        "silver_symbol": self.silver_symbol,
                    }
                )

        elif trade_type == "LONG_GOLD_SHORT_SILVER":
            # Exit when ratio rises toward mean (75-80 range)
            if current_ratio >= (self.ratio_mean - mean_tolerance):
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.85,
                    metadata={
                        "type": "pair_trade_exit",
                        "trade_type": trade_type,
                        "reason": "ratio_mean_reversion",
                        "exit_ratio": current_ratio,
                        "target_ratio": self.ratio_mean,
                        "gold_symbol": self.gold_symbol,
                        "silver_symbol": self.silver_symbol,
                    }
                )

        # Also exit if ratio reaches opposite extreme (stop loss)
        if trade_type == "SHORT_GOLD_LONG_SILVER":
            if current_ratio < self.ratio_oversold - 5:
                # Ratio went too far down, exit with loss
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.9,
                    metadata={
                        "type": "pair_trade_exit",
                        "trade_type": trade_type,
                        "reason": "stop_loss",
                        "exit_ratio": current_ratio,
                    }
                )

        elif trade_type == "LONG_GOLD_SHORT_SILVER":
            if current_ratio > self.ratio_overbought + 5:
                # Ratio went too far up, exit with loss
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.9,
                    metadata={
                        "type": "pair_trade_exit",
                        "trade_type": trade_type,
                        "reason": "stop_loss",
                        "exit_ratio": current_ratio,
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
        Calculate position size for pair trade.

        For pair trades, this calculates the size for the gold leg.
        Silver leg is sized to match dollar exposure.

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            entry_price: Planned entry price
            stop_loss: Stop loss price
            account_balance: Current account balance

        Returns:
            Position size (lots for gold)
        """
        if stop_loss == entry_price:
            return 0.0

        stop_distance = abs(entry_price - stop_loss)
        if stop_distance == 0:
            return 0.0

        risk_amount = account_balance * self.risk_per_trade
        position_size = risk_amount / stop_distance

        return position_size

    def calculate_pair_position_sizes(
        self,
        gold_price: float,
        silver_price: float,
        account_balance: float,
        stop_loss_gold: float,
        stop_loss_silver: float
    ) -> Tuple[float, float]:
        """
        Calculate hedged position sizes for both legs of pair trade.

        Ensures both legs have equal dollar risk.

        Args:
            gold_price: Current gold price
            silver_price: Current silver price
            account_balance: Account balance
            stop_loss_gold: Stop loss for gold position
            stop_loss_silver: Stop loss for silver position

        Returns:
            Tuple of (gold_lots, silver_lots)
        """
        risk_per_leg = (account_balance * self.risk_per_trade) / 2

        gold_stop_distance = abs(gold_price - stop_loss_gold)
        silver_stop_distance = abs(silver_price - stop_loss_silver)

        if gold_stop_distance > 0:
            gold_lots = risk_per_leg / gold_stop_distance
        else:
            gold_lots = 0.0

        if silver_stop_distance > 0:
            silver_lots = risk_per_leg / silver_stop_distance
        else:
            silver_lots = 0.0

        return gold_lots, silver_lots

    def get_required_candles(self) -> int:
        """Get number of candles required for signal generation."""
        return self.lookback_period + 10

    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        if not super().validate_config():
            return False

        if self.ratio_overbought <= self.ratio_oversold:
            self.logger.error(
                f"ratio_overbought ({self.ratio_overbought}) must be greater "
                f"than ratio_oversold ({self.ratio_oversold})"
            )
            return False

        if self.ratio_mean <= self.ratio_oversold or self.ratio_mean >= self.ratio_overbought:
            self.logger.warning(
                f"ratio_mean ({self.ratio_mean}) should be between "
                f"ratio_oversold ({self.ratio_oversold}) and "
                f"ratio_overbought ({self.ratio_overbought})"
            )

        if self.lookback_period < 5:
            self.logger.error(f"lookback_period ({self.lookback_period}) must be >= 5")
            return False

        return True

    def set_market_data(
        self,
        gold_ohlcv: List[OHLCV],
        silver_ohlcv: List[OHLCV]
    ):
        """
        Set market data for both gold and silver.

        Call this before generating signals to provide the required data.

        Args:
            gold_ohlcv: OHLCV data for XAUUSD
            silver_ohlcv: OHLCV data for XAGUSD
        """
        self.config["gold_ohlcv_data"] = gold_ohlcv
        self.config["silver_ohlcv_data"] = silver_ohlcv

    def clear_position(self):
        """Clear the current pair position after exit."""
        self.pair_position = None
