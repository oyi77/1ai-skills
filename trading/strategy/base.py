"""
Strategy Base Class

Abstract base class for all trading strategies.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

from ..brokers.base import OHLCV

logger = logging.getLogger(__name__)


@dataclass
class TradingSignal:
    """Trading signal with entry levels."""

    symbol: str
    timeframe: str
    timestamp: datetime
    # Levels
    hh: float  # Highest High
    ll: float  # Lowest Low
    r_points: float  # Range of last candle
    # Pending orders
    buy_stop: float
    sell_stop: float
    # SL/TP
    buy_sl: float
    buy_tp: float
    sell_sl: float
    sell_tp: float
    # Status
    status: str = "pending"  # pending, triggered, cancelled, done
    triggered_side: Optional[str] = None  # BUY or SELL

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "timestamp": self.timestamp.isoformat(),
            "hh": self.hh,
            "ll": self.ll,
            "r_points": self.r_points,
            "buy_stop": self.buy_stop,
            "sell_stop": self.sell_stop,
            "buy_sl": self.buy_sl,
            "buy_tp": self.buy_tp,
            "sell_sl": self.sell_sl,
            "sell_tp": self.sell_tp,
            "status": self.status,
            "triggered_side": self.triggered_side,
        }


class Strategy(ABC):
    """Abstract base class for trading strategies."""

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"strategy.{name}")

    @abstractmethod
    def get_signals(self, ohlcv_data: List[OHLCV]) -> List[TradingSignal]:
        """
        Generate trading signals from OHLCV data.

        Args:
            ohlcv_data: List of OHLCV candles

        Returns:
            List of TradingSignal objects
        """
        pass

    @abstractmethod
    def calculate_hh_ll(self, ohlcv_data: List[OHLCV]) -> tuple:
        """
        Calculate Highest High and Lowest Low from data.

        Returns:
            (hh, ll) tuple
        """
        pass

    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        return True

    def get_required_timeframe(self) -> str:
        """Get required timeframe for this strategy."""
        return "H1"

    def get_required_candles(self) -> int:
        """Get number of candles required for signal generation."""
        return 7

    def format_signal(self, signal: TradingSignal) -> str:
        """Format signal for display."""
        return f"""
=== {self.name} Signal ===
Symbol: {signal.symbol}
Timeframe: {signal.timeframe}
Time: {signal.timestamp.isoformat()}

Levels:
  HH: {signal.hh}
  LL: {signal.ll}
  R: {signal.r_points} points

Buy Stop: {signal.buy_stop}
  SL: {signal.buy_sl}
  TP: {signal.buy_tp}

Sell Stop: {signal.sell_stop}
  SL: {signal.sell_sl}
  TP: {signal.sell_tp}

Status: {signal.status}
"""
