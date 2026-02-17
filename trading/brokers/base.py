"""
Trading Broker Base Classes

Defines abstract interfaces for broker connectors.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any


class BrokerType(Enum):
    """Supported broker types."""

    MT5 = "mt5"  # MetaTrader 5
    MT4 = "mt4"  # MetaTrader 4
    CCXT = "ccxt"  # CCXT (Crypto exchanges)


@dataclass
class OHLCV:
    """OHLCV candlestick data."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
        }


@dataclass
class Order:
    """Trading order."""

    ticket: int
    symbol: str
    order_type: str
    volume: float
    price: float
    sl: Optional[float] = None
    tp: Optional[float] = None
    magic: int = 0
    comment: str = ""
    time_setup: Optional[datetime] = None
    time_done: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticket": self.ticket,
            "symbol": self.symbol,
            "order_type": self.order_type,
            "volume": self.volume,
            "price": self.price,
            "sl": self.sl,
            "tp": self.tp,
            "magic": self.magic,
            "comment": self.comment,
            "time_setup": self.time_setup.isoformat() if self.time_setup else None,
            "time_done": self.time_done.isoformat() if self.time_done else None,
        }


@dataclass
class Position:
    """Open position."""

    ticket: int
    symbol: str
    order_type: str  # BUY or SELL
    volume: float
    open_price: float
    current_price: float
    sl: Optional[float] = None
    tp: Optional[float] = None
    profit: float = 0.0
    comment: str = ""
    time_open: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticket": self.ticket,
            "symbol": self.symbol,
            "order_type": self.order_type,
            "volume": self.volume,
            "open_price": self.open_price,
            "current_price": self.current_price,
            "sl": self.sl,
            "tp": self.tp,
            "profit": self.profit,
            "comment": self.comment,
            "time_open": self.time_open.isoformat() if self.time_open else None,
        }


@dataclass
class AccountInfo:
    """Trading account information."""

    login: int
    balance: float
    equity: float
    margin: float
    free_margin: float
    margin_level: float
    currency: str
    leverage: int
    server: str = ""
    name: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "login": self.login,
            "balance": self.balance,
            "equity": self.equity,
            "margin": self.margin,
            "free_margin": self.free_margin,
            "margin_level": self.margin_level,
            "currency": self.currency,
            "leverage": self.leverage,
            "server": self.server,
            "name": self.name,
        }


class BrokerConnector(ABC):
    """Abstract base class for broker connectors."""

    def __init__(self, broker_type: BrokerType):
        self.broker_type = broker_type
        self.connected = False

    @abstractmethod
    def connect(self, **kwargs) -> bool:
        """Connect to broker."""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from broker."""
        pass

    @abstractmethod
    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        count: Optional[int] = None,
    ) -> List[OHLCV]:
        """Fetch OHLCV data."""
        pass

    @abstractmethod
    def place_order(
        self,
        symbol: str,
        order_type: str,
        volume: float,
        price: Optional[float] = None,
        sl: Optional[float] = None,
        tp: Optional[float] = None,
        **kwargs,
    ) -> Optional[Order]:
        """Place a trading order."""
        pass

    @abstractmethod
    def get_positions(self, symbol: Optional[str] = None) -> List[Position]:
        """Get open positions."""
        pass

    @abstractmethod
    def get_account_info(self) -> Optional[AccountInfo]:
        """Get account information."""
        pass

    def is_connected(self) -> bool:
        """Check if connected to broker."""
        return self.connected
