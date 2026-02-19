"""
Strategy Template Base Class

Modular strategy template with configurable hooks for entry, exit, and position sizing.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Tuple
import logging

from trading.brokers.base import OHLCV

logger = logging.getLogger(__name__)


class SignalType(Enum):
    """Trading signal types."""
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"
    CLOSE_LONG = "CLOSE_LONG"
    CLOSE_SHORT = "CLOSE_SHORT"


@dataclass
class Signal:
    """Trading signal with entry/exit information."""
    timestamp: datetime
    symbol: str
    timeframe: str
    signal_type: SignalType
    price: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    confidence: float = 1.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "signal_type": self.signal_type.value,
            "price": self.price,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }


@dataclass
class Position:
    """Position information."""
    symbol: str
    entry_price: float
    quantity: float
    side: str  # LONG or SHORT
    entry_time: datetime
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class StrategyTemplate(ABC):
    """
    Base class for strategy templates.
    
    Provides extensible hooks for:
    - entry_conditions(): Check if entry criteria are met
    - exit_conditions(): Check if exit criteria are met
    - position_sizing(): Calculate position size based on risk
    """
    
    def __init__(
        self,
        name: str,
        symbol: str = "XAUUSD",
        timeframe: str = "H1",
        risk_per_trade: float = 0.02,  # 2% risk per trade
        config: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.symbol = symbol
        self.timeframe = timeframe
        self.risk_per_trade = risk_per_trade
        self.config = config or {}
        self.logger = logging.getLogger(f"strategy.templates.{name}")
        
        # State
        self.positions: List[Position] = []
        self.signals: List[Signal] = []
    
    @abstractmethod
    def entry_conditions(
        self, 
        ohlcv_data: List[OHLCV], 
        current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if entry criteria are met.
        
        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            
        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        pass
    
    @abstractmethod
    def exit_conditions(
        self, 
        ohlcv_data: List[OHLCV], 
        current_idx: int,
        position: Position
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if exit criteria are met for an existing position.
        
        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            position: Current position to check
            
        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        pass
    
    @abstractmethod
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
        pass
    
    def calculate_pip_value(self, symbol: str) -> float:
        """
        Calculate pip value for a symbol.
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Pip value in price terms
        """
        # Default pip values by symbol type
        pip_values = {
            "XAUUSD": 0.01,  # Gold
            "XAGUSD": 0.01,  # Silver
            "EURUSD": 0.0001,
            "GBPUSD": 0.0001,
            "USDJPY": 0.01,
        }
        return pip_values.get(symbol, 0.0001)
    
    def calculate_stop_loss_pips(
        self,
        entry_price: float,
        stop_loss: float,
        is_long: bool = True
    ) -> float:
        """Calculate stop loss in pips."""
        price_diff = abs(entry_price - stop_loss)
        pip_value = self.calculate_pip_value(self.symbol)
        return price_diff / pip_value if pip_value > 0 else price_diff
    
    def calculate_position_size_from_risk(
        self,
        account_balance: float,
        stop_loss_pips: float,
        pip_value: float = None
    ) -> float:
        """
        Calculate position size based on risk amount.
        
        Args:
            account_balance: Account balance
            stop_loss_pips: Stop loss in pips
            pip_value: Value per pip (optional)
            
        Returns:
            Position size
        """
        if pip_value is None:
            pip_value = self.calculate_pip_value(self.symbol)
        
        risk_amount = account_balance * self.risk_per_trade
        
        if stop_loss_pips <= 0:
            return 0.0
        
        # For forex: position_size = risk / (stop_loss_pips * pip_value)
        # For commodities: position_size = risk / stop_loss_distance
        if pip_value > 0:
            position_size = risk_amount / (stop_loss_pips * pip_value)
        else:
            position_size = risk_amount / stop_loss_pips
        
        return position_size
    
    def get_signals(self, ohlcv_data: List[OHLCV]) -> List[Signal]:
        """
        Generate trading signals from OHLCV data.
        
        Args:
            ohlcv_data: List of OHLCV candles
            
        Returns:
            List of Signal objects
        """
        self.signals = []
        
        for idx in range(self.get_required_candles(), len(ohlcv_data)):
            # Check for entry signals
            entry_met, entry_signal = self.entry_conditions(ohlcv_data, idx)
            if entry_met and entry_signal:
                self.signals.append(entry_signal)
            
            # Check for exit signals on open positions
            for position in self.positions:
                exit_met, exit_signal = self.exit_conditions(ohlcv_data, idx, position)
                if exit_met and exit_signal:
                    self.signals.append(exit_signal)
        
        return self.signals
    
    def get_required_candles(self) -> int:
        """Get number of candles required for signal generation."""
        return 50  # Default minimum
    
    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        if self.risk_per_trade <= 0 or self.risk_per_trade > 1.0:
            self.logger.error(f"Invalid risk_per_trade: {self.risk_per_trade}")
            return False
        return True
    
    def format_signal(self, signal: Signal) -> str:
        """Format signal for display."""
        return f"""
=== {self.name} Signal ===
Symbol: {signal.signal_type.value}
Time: {signal.timestamp.isoformat()}
Price: {signal.price}
SL: {signal.stop_loss}
TP: {signal.take_profit}
Confidence: {signal.confidence:.2%}
"""
