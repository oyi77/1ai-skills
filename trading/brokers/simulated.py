"""
SimulatedBroker - Paper trading dengan yfinance price feed.

Tanpa koneksi broker real, menggunakan data yfinance (GC=F) untuk simulasi.
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any

import yfinance as yf

from .base import BrokerConnector, BrokerType, OHLCV, Order, Position, AccountInfo

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
PAPER_FILE = DATA_DIR / "paper_trading.json"


class SimulatedBroker(BrokerConnector):
    """Paper trading broker menggunakan yfinance untuk harga real-time."""

    def __init__(self):
        super().__init__(BrokerType.CTRADER)  # Use CTADER type for compatibility
        self._positions: Dict[int, Position] = {}
        self._orders: List[Order] = []
        self._order_counter = 1000
        self._paper_stats = self._load_stats()
        self._price_cache = {}

    def _load_stats(self) -> Dict[str, Any]:
        """Load paper trading statistics."""
        if PAPER_FILE.exists():
            with open(PAPER_FILE) as f:
                return json.load(f)
        return {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "net_profit": 0.0,
            "max_drawdown": 0.0,
            "current_balance": 10000.0,
            "trades": []
        }

    def _save_stats(self):
        """Save paper trading statistics."""
        DATA_DIR.mkdir(exist_ok=True)
        with open(PAPER_FILE, "w") as f:
            json.dump(self._paper_stats, f, indent=2)

    def _get_price(self, symbol: str) -> float:
        """Get current price dari yfinance (cached 5s)."""
        cache_key = f"{symbol}_{datetime.now().second // 5}"
        if cache_key in self._price_cache:
            cached_time, price = self._price_cache[cache_key]
            if (datetime.now() - cached_time).seconds < 5:
                return price
        
        try:
            ticker = yf.Ticker("GC=F" if symbol == "XAUUSD" else symbol)
            # Get latest price from last close or regularMarketPrice
            info = ticker.info if hasattr(ticker, 'info') else {}
            price = info.get('regularMarketPrice', info.get('previousClose', 2000.0))
            self._price_cache[cache_key] = (datetime.now(), price)
            return price
        except Exception as e:
            logger.warning(f"Failed to get price for {symbol}: {e}")
            return self._paper_stats.get("current_price", 2000.0)

    def connect(self, **kwargs) -> bool:
        """Connect ke simulated broker (selalu berhasil)."""
        self.connected = True
        logger.info("SimulatedBroker connected (paper trading mode)")
        return True

    def disconnect(self) -> bool:
        """Disconnect."""
        self.connected = False
        self._save_stats()
        logger.info("SimulatedBroker disconnected")
        return True

    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "H1",
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        count: Optional[int] = None,
    ) -> List[OHLCV]:
        """Fetch OHLCV dari yfinance."""
        tf_map = {"H1": "1h", "H4": "4h", "D1": "1d", "M15": "15m"}
        tf = tf_map.get(timeframe, "1h")
        
        ticker_symbol = "GC=F" if symbol == "XAUUSD" else symbol
        ticker = yf.Ticker(ticker_symbol)
        
        start = start or datetime.now() - timedelta(days=30)
        end = end or datetime.now()
        
        df = ticker.history(start=start, end=end, interval=tf)
        
        ohlcv_list = []
        for idx, row in df.iterrows():
            ohlcv_list.append(OHLCV(
                timestamp=idx.to_pydatetime(),
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
            ))
        
        logger.info(f"Fetched {len(ohlcv_list)} candles for {symbol}")
        return ohlcv_list

    def place_order(self, order: Order, dry_run: bool = False) -> bool:
        """Place order (simulated)."""
        order.ticket = self._order_counter
        order.time_setup = datetime.now()
        
        if dry_run:
            logger.info(f"[DRY-RUN] Order placed: {order.order_type} {order.symbol} {order.volume} @ {order.price}")
            return True
        
        current_price = self._get_price(order.symbol)
        
        if order.order_type in ["BUY", "BUYLIMIT", "BUYSTOP"]:
            order.open_price = order.price or current_price
            profit = 0.0
        else:
            order.open_price = order.price or current_price
            profit = 0.0
        
        position = Position(
            ticket=order.ticket,
            symbol=order.symbol,
            order_type=order.order_type,
            volume=order.volume,
            open_price=order.open_price,
            current_price=current_price,
            sl=order.sl,
            tp=order.tp,
            profit=0.0,
            comment=order.comment,
            time_open=datetime.now()
        )
        
        self._positions[order.ticket] = position
        self._orders.append(order)
        self._order_counter += 1
        
        logger.info(f"Order placed: {order.order_type} {order.symbol} {order.volume} lots @ {order.open_price}")
        return True

    def get_positions(self) -> List[Position]:
        """Get all open positions dengan current P&L."""
        current_price = self._get_price("XAUUSD")
        
        for pos in self._positions.values():
            pos.current_price = current_price
            if pos.order_type.startswith("BUY"):
                pos.profit = (current_price - pos.open_price) * pos.volume * 100  # Gold = 100 oz per lot
            else:
                pos.profit = (pos.open_price - current_price) * pos.volume * 100
        
        return list(self._positions.values())

    def close_position(self, ticket: int, volume: Optional[float] = None) -> bool:
        """Close position dan update stats."""
        if ticket not in self._positions:
            logger.warning(f"Position {ticket} not found")
            return False
        
        pos = self._positions[ticket]
        close_price = self._get_price(pos.symbol)
        
        # Calculate profit (gold = 100 oz per lot)
        if pos.order_type.startswith("BUY"):
            profit = (close_price - pos.open_price) * pos.volume * 100
        else:
            profit = (pos.open_price - close_price) * pos.volume * 100
        
        # Update stats
        self._paper_stats["total_trades"] += 1
        self._paper_stats["net_profit"] += profit
        
        if profit > 0:
            self._paper_stats["winning_trades"] += 1
        else:
            self._paper_stats["losing_trades"] += 1
        
        self._paper_stats["trades"].append({
            "ticket": ticket,
            "symbol": pos.symbol,
            "type": pos.order_type,
            "open": pos.open_price,
            "close": close_price,
            "profit": profit,
            "time": datetime.now().isoformat()
        })
        
        del self._positions[ticket]
        self._save_stats()
        
        logger.info(f"Position {ticket} closed: P/L = ${profit:.2f}")
        return True

    def get_account_info(self) -> AccountInfo:
        """Get account info."""
        return AccountInfo(
            balance=self._paper_stats["current_balance"] + self._paper_stats["net_profit"],
            equity=self._paper_stats["current_balance"] + self._paper_stats["net_profit"],
            margin=0.0,
            free_margin=self._paper_stats["current_balance"],
            profit=self._paper_stats["net_profit"]
        )
