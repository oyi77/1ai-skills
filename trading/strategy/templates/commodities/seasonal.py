"""
Seasonal Pattern Strategy Template

Strategy based on monthly/quarterly recurring patterns in commodity prices.
Entry when seasonal patterns align with favorable conditions.
Exit when seasonal window closes or risk management triggers.

Seasonality is probabilistic, not deterministic - always use confirmation filters.
"""

from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass

from trading.brokers.base import OHLCV
from trading.strategy.templates.base import StrategyTemplate, Signal, SignalType


@dataclass
class SeasonalPattern:
    """Represents a seasonal pattern for a commodity."""
    name: str
    symbol: str
    months: List[int]  # 1-12, months when pattern is active
    direction: str  # "BULLISH" or "BEARISH"
    historical_success_rate: float  # 0.0 to 1.0
    avg_return_pct: float  # Average historical return during pattern
    confidence_weight: float  # Weight for confidence calculation (0.0-1.0)
    description: str


# Seasonal Pattern Database for Commodities
# Based on historical research - these are probabilistic patterns, not guarantees
SEASONAL_PATTERNS: Dict[str, List[SeasonalPattern]] = {
    # Gold (XAUUSD) patterns
    "XAUUSD": [
        SeasonalPattern(
            name="January Effect",
            symbol="XAUUSD",
            months=[1],  # January
            direction="BULLISH",
            historical_success_rate=0.72,
            avg_return_pct=2.5,
            confidence_weight=0.8,
            description="Gold often rises in January due to new year demand and Asian buying"
        ),
        SeasonalPattern(
            name="September Strength",
            symbol="XAUUSD",
            months=[9],  # September
            direction="BULLISH",
            historical_success_rate=0.68,
            avg_return_pct=2.0,
            confidence_weight=0.75,
            description="Gold tends to strengthen in September - Indian wedding season, festival demand"
        ),
        SeasonalPattern(
            name="Summer Doldrums",
            symbol="XAUUSD",
            months=[7, 8],  # July-August
            direction="BEARISH",
            historical_success_rate=0.65,
            avg_return_pct=-1.5,
            confidence_weight=0.7,
            description="Gold often weakens in summer due to reduced investment activity"
        ),
    ],
    # Silver (XAGUSD) patterns
    "XAGUSD": [
        SeasonalPattern(
            name="January Silver",
            symbol="XAGUSD",
            months=[1],
            direction="BULLISH",
            historical_success_rate=0.70,
            avg_return_pct=3.0,
            confidence_weight=0.75,
            description="Silver follows gold higher in January with industrial demand pickup"
        ),
        SeasonalPattern(
            name="September Silver",
            symbol="XAGUSD",
            months=[9],
            direction="BULLISH",
            historical_success_rate=0.66,
            avg_return_pct=2.8,
            confidence_weight=0.70,
            description="Silver strength in September with gold and industrial demand"
        ),
        SeasonalPattern(
            name="Spring Weakness",
            symbol="XAGUSD",
            months=[4, 5],  # April-May
            direction="BEARISH",
            historical_success_rate=0.62,
            avg_return_pct=-2.0,
            confidence_weight=0.65,
            description="Silver often weakens in spring before summer rally"
        ),
    ],
    # Oil (CL or similar) patterns
    "CL": [
        SeasonalPattern(
            name="Q4 Winter Demand",
            symbol="CL",
            months=[10, 11, 12],  # Q4
            direction="BULLISH",
            historical_success_rate=0.75,
            avg_return_pct=4.0,
            confidence_weight=0.85,
            description="Oil typically rises in Q4 due to winter heating demand"
        ),
        SeasonalPattern(
            name="Summer Driving Season",
            symbol="CL",
            months=[6, 7, 8],  # Summer
            direction="BULLISH",
            historical_success_rate=0.68,
            avg_return_pct=2.5,
            confidence_weight=0.75,
            description="Oil rises in summer due to increased gasoline demand"
        ),
        SeasonalPattern(
            name="Spring Refill",
            symbol="CL",
            months=[3, 4],  # March-April
            direction="BEARISH",
            historical_success_rate=0.60,
            avg_return_pct=-2.0,
            confidence_weight=0.60,
            description="Oil often falls in spring as refineries undergo maintenance"
        ),
    ],
    # Natural Gas (NG) patterns
    "NG": [
        SeasonalPattern(
            name="Winter Peak",
            symbol="NG",
            months=[12, 1, 2],  # Winter
            direction="BULLISH",
            historical_success_rate=0.78,
            avg_return_pct=8.0,
            confidence_weight=0.90,
            description="Natural gas spikes in winter for heating demand"
        ),
        SeasonalPattern(
            name="Shoulder Season",
            symbol="NG",
            months=[4, 5, 10],  # Spring/Fall shoulder
            direction="BEARISH",
            historical_success_rate=0.65,
            avg_return_pct=-3.0,
            confidence_weight=0.70,
            description="Natural gas weakens in shoulder seasons between peak demand"
        ),
    ],
    # Copper (HG) patterns
    "HG": [
        SeasonalPattern(
            name="Q1 Industrial",
            symbol="HG",
            months=[1, 2, 3],  # Q1
            direction="BULLISH",
            historical_success_rate=0.68,
            avg_return_pct=2.5,
            confidence_weight=0.75,
            description="Copper rises in Q1 as industrial activity picks up"
        ),
        SeasonalPattern(
            name="Chinese New Year",
            symbol="HG",
            months=[1, 2],  # Around Chinese New Year
            direction="BEARISH",
            historical_success_rate=0.58,
            avg_return_pct=-1.5,
            confidence_weight=0.55,
            description="Copper may weaken around Chinese New Year factory closures"
        ),
    ],
    # Platinum (PL) patterns
    "PL": [
        SeasonalPattern(
            name="Auto Sector Demand",
            symbol="PL",
            months=[3, 4, 9, 10],  # Spring and Fall
            direction="BULLISH",
            historical_success_rate=0.65,
            avg_return_pct=2.0,
            confidence_weight=0.70,
            description="Platinum benefits from auto sector demand cycles"
        ),
    ],
    # Palladium (PA) patterns
    "PA": [
        SeasonalPattern(
            name="Auto Sector Demand",
            symbol="PA",
            months=[3, 4, 9, 10],  # Spring and Fall
            direction="BULLISH",
            historical_success_rate=0.67,
            avg_return_pct=2.5,
            confidence_weight=0.72,
            description="Palladium tied to auto catalyst demand"
        ),
    ],
}


class SeasonalStrategy(StrategyTemplate):
    """
    Seasonal Pattern Strategy for commodities.

    Entry: When current month matches a configured seasonal pattern
    Exit: When seasonal window closes or risk management triggers

    IMPORTANT: Seasonality is probabilistic. Always use confirmation filters
    (trend direction, momentum, support/resistance) before entry.

    Configuration:
        - seasonal_patterns: Override default patterns for symbol
        - min_confidence: Minimum confidence threshold for signals
        - require_confirmation: Require additional technical confirmation
        - confirmation_lookback: Lookback period for confirmation indicators
    """

    def __init__(
        self,
        symbol: str = "XAUUSD",
        timeframe: str = "W1",  # Weekly for seasonal patterns
        risk_per_trade: float = 0.02,
        seasonal_patterns: Optional[List[SeasonalPattern]] = None,
        min_confidence: float = 0.60,
        require_confirmation: bool = True,
        confirmation_lookback: int = 8,
        atr_period: int = 14,
        atr_multiplier: float = 2.0,
        config: Optional[dict] = None,
    ):
        super().__init__(
            name="SeasonalStrategy",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )

        # Seasonal configuration
        self.seasonal_patterns = seasonal_patterns or SEASONAL_PATTERNS.get(symbol, [])
        self.min_confidence = min_confidence
        self.require_confirmation = require_confirmation
        self.confirmation_lookback = confirmation_lookback

        # Risk management
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier

        self.logger.info(
            f"Initialized SeasonalStrategy for {symbol} with {len(self.seasonal_patterns)} patterns"
        )

    def get_active_patterns(self, current_date: datetime) -> List[SeasonalPattern]:
        """Get seasonal patterns active for the current month."""
        current_month = current_date.month
        active_patterns = [
            pattern for pattern in self.seasonal_patterns
            if current_month in pattern.months
        ]
        return active_patterns

    def calculate_pattern_confidence(
        self,
        pattern: SeasonalPattern,
        current_price: float,
        ohlcv_data: List[OHLCV]
    ) -> float:
        """
        Calculate confidence score for a seasonal pattern signal.

        Combines:
        - Historical success rate
        - Pattern weight
        - Current price position relative to recent range
        """
        # Base confidence from historical performance
        base_confidence = pattern.historical_success_rate * pattern.confidence_weight

        # Adjust based on current price position
        if len(ohlcv_data) >= 10:
            recent_high = max(c.high for c in ohlcv_data[-10:])
            recent_low = min(c.low for c in ohlcv_data[-10:])
            price_range = recent_high - recent_low

            if price_range > 0:
                # For bullish patterns, prefer buying near support (lower in range)
                if pattern.direction == "BULLISH":
                    price_position = (current_price - recent_low) / price_range
                    # Lower price = higher confidence for bullish
                    position_factor = 1.0 - (price_position * 0.3)
                else:
                    # For bearish patterns, prefer selling near resistance (higher in range)
                    price_position = (current_price - recent_low) / price_range
                    position_factor = 0.7 + (price_position * 0.3)
            else:
                position_factor = 1.0
        else:
            position_factor = 1.0

        # Combine factors
        final_confidence = base_confidence * position_factor

        # Clamp to valid range
        return max(0.0, min(1.0, final_confidence))

    def check_confirmation(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int,
        direction: str
    ) -> bool:
        """
        Check if price action confirms the seasonal direction.

        Returns True if confirmation is satisfied or not required.
        """
        if not self.require_confirmation:
            return True

        if current_idx < self.confirmation_lookback:
            return False

        # Simple trend confirmation using recent price action
        lookback_data = ohlcv_data[current_idx - self.confirmation_lookback:current_idx + 1]

        if len(lookback_data) < 5:
            return False

        # Calculate simple moving average
        closes = [c.close for c in lookback_data]
        sma_short = sum(closes[-3:]) / 3
        sma_long = sum(closes[-5:]) / 5

        if direction == "BULLISH":
            # Confirm if price is above short-term MA and short MA above long MA
            return closes[-1] > sma_short and sma_short > sma_long
        else:  # BEARISH
            # Confirm if price is below short-term MA and short MA below long MA
            return closes[-1] < sma_short and sma_short < sma_long

    def calculate_atr(
        self,
        ohlcv_data: List[OHLCV],
        period: int = None
    ) -> float:
        """Calculate Average True Range."""
        period = period or self.atr_period
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

    def calculate_stop_loss(
        self,
        entry_price: float,
        direction: str,
        atr: float
    ) -> float:
        """Calculate stop loss based on ATR."""
        if direction == "BULLISH":
            return entry_price - (atr * self.atr_multiplier)
        else:
            return entry_price + (atr * self.atr_multiplier)

    def calculate_take_profit(
        self,
        entry_price: float,
        direction: str,
        risk: float
    ) -> float:
        """Calculate take profit based on risk-reward ratio."""
        if direction == "BULLISH":
            return entry_price + (risk * 2)  # 2:1 reward ratio
        else:
            return entry_price - (risk * 2)

    def entry_conditions(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if seasonal entry criteria are met.

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        if current_idx < 1:
            return False, None

        current = ohlcv_data[current_idx]
        current_date = current.time if hasattr(current, 'time') else datetime.now()

        # Get active seasonal patterns for current month
        active_patterns = self.get_active_patterns(current_date)

        if not active_patterns:
            return False, None

        # Evaluate each active pattern
        for pattern in active_patterns:
            # Calculate confidence
            confidence = self.calculate_pattern_confidence(
                pattern,
                current.close,
                ohlcv_data
            )

            # Skip if below minimum confidence
            if confidence < self.min_confidence:
                continue

            # Check for confirmation
            if not self.check_confirmation(
                ohlcv_data,
                current_idx,
                pattern.direction
            ):
                self.logger.debug(
                    f"Pattern {pattern.name} lacks confirmation for {self.symbol}"
                )
                continue

            # Calculate risk management levels
            atr = self.calculate_atr(ohlcv_data)
            stop_loss = self.calculate_stop_loss(
                current.close,
                pattern.direction,
                atr
            )
            risk = abs(current.close - stop_loss)
            take_profit = self.calculate_take_profit(
                current.close,
                pattern.direction,
                risk
            )

            # Determine signal type
            if pattern.direction == "BULLISH":
                signal_type = SignalType.BUY
            else:
                signal_type = SignalType.SELL

            self.logger.info(
                f"Seasonal signal: {pattern.name} - {pattern.direction} "
                f"for {self.symbol} @ {current.close:.2f} "
                f"(confidence: {confidence:.2%})"
            )

            return True, Signal(
                timestamp=current.time if hasattr(current, 'time') else datetime.now(),
                symbol=self.symbol,
                timeframe=self.timeframe,
                signal_type=signal_type,
                price=current.close,
                stop_loss=stop_loss,
                take_profit=take_profit,
                confidence=confidence,
                metadata={
                    "type": "seasonal_pattern",
                    "pattern_name": pattern.name,
                    "pattern_direction": pattern.direction,
                    "historical_success_rate": pattern.historical_success_rate,
                    "avg_return_pct": pattern.avg_return_pct,
                    "description": pattern.description,
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
        Check if exit criteria are met for an existing position.

        Exit when:
        - Seasonal pattern window closes (month changes)
        - Price hits stop loss
        - Price hits take profit
        """
        if current_idx < 1:
            return False, None

        current = ohlcv_data[current_idx]
        current_date = current.time if hasattr(current, 'time') else datetime.now()
        current_month = current_date.month

        # Get pattern direction from metadata
        pattern_direction = position.metadata.get("pattern_direction", "BULLISH")
        pattern_name = position.metadata.get("pattern_name", "Unknown")

        # Check if we're still in the seasonal window
        active_patterns = self.get_active_patterns(current_date)
        still_in_pattern = any(
            pattern.name == pattern_name
            for pattern in active_patterns
        )

        if not still_in_pattern:
            self.logger.info(
                f"Exiting {pattern_name} position - seasonal window closed"
            )
            return True, Signal(
                timestamp=current.time if hasattr(current, 'time') else datetime.now(),
                symbol=self.symbol,
                timeframe=self.timeframe,
                signal_type=SignalType.CLOSE_LONG if position.side == "LONG" else SignalType.CLOSE_SHORT,
                price=current.close,
                confidence=0.95,
                metadata={
                    "reason": "seasonal_window_closed",
                    "pattern_name": pattern_name,
                }
            )

        # Check for stop loss or take profit hit
        if position.side == "LONG":
            if current.close <= position.stop_loss:
                return True, Signal(
                    timestamp=current.time if hasattr(current, 'time') else datetime.now(),
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=1.0,
                    metadata={"reason": "stop_loss_hit"}
                )
            if current.close >= position.take_profit:
                return True, Signal(
                    timestamp=current.time if hasattr(current, 'time') else datetime.now(),
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=1.0,
                    metadata={"reason": "take_profit_hit"}
                )

        elif position.side == "SHORT":
            if current.close >= position.stop_loss:
                return True, Signal(
                    timestamp=current.time if hasattr(current, 'time') else datetime.now(),
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=1.0,
                    metadata={"reason": "stop_loss_hit"}
                )
            if current.close <= position.take_profit:
                return True, Signal(
                    timestamp=current.time if hasattr(current, 'time') else datetime.now(),
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=1.0,
                    metadata={"reason": "take_profit_hit"}
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
        """Calculate position size based on risk management."""
        if stop_loss == entry_price:
            return 0.0

        stop_loss_pips = self.calculate_stop_loss_pips(entry_price, stop_loss)

        return self.calculate_position_size_from_risk(
            account_balance=account_balance,
            stop_loss_pips=stop_loss_pips,
        )

    def get_required_candles(self) -> int:
        """Get number of candles required for signal generation."""
        return max(self.confirmation_lookback + 5, self.atr_period + 5)

    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        if not super().validate_config():
            return False

        if self.min_confidence < 0.0 or self.min_confidence > 1.0:
            self.logger.error(f"Invalid min_confidence: {self.min_confidence}")
            return False

        if self.atr_multiplier <= 0:
            self.logger.error(f"Invalid atr_multiplier: {self.atr_multiplier}")
            return False

        return True

    def add_custom_pattern(self, pattern: SeasonalPattern) -> None:
        """Add a custom seasonal pattern to the strategy."""
        self.seasonal_patterns.append(pattern)
        self.logger.info(f"Added custom pattern: {pattern.name}")

    def get_pattern_summary(self) -> List[Dict[str, Any]]:
        """Get summary of all configured seasonal patterns."""
        return [
            {
                "name": p.name,
                "months": p.months,
                "direction": p.direction,
                "success_rate": p.historical_success_rate,
                "avg_return": p.avg_return_pct,
                "description": p.description,
            }
            for p in self.seasonal_patterns
        ]
