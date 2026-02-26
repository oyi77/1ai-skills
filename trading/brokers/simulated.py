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

    def __init__(self, symbol: str = "XAUUSD"):
        super().__init__(BrokerType.CTRADER)  # Use CTRADER type for compatibility
        self._symbol = symbol
        self._positions: Dict[int, Position] = {}
        self._orders: List[Order] = []
        self._position_counter = 1000  # Start at 1000 for positions
        self._order_counter = 2000      # Start at 2000 for orders
        self._paper_stats = self._load_stats()
        self._price_cache = {}
        self._point = 0.01  # Default for XAUUSD

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

    # ========== EA Compatibility Methods ==========

    def get_point(self) -> float:
        """Get symbol point size."""
        return self._point

    def get_ask(self) -> float:
        """Get current ask price."""
        return self._get_price(self._symbol)

    def get_bid(self) -> float:
        """Get current bid price."""
        # For gold, bid is slightly lower than ask
        return self._get_price(self._symbol) - self._point

    def subscribe(self, symbol: str):
        """Subscribe to symbol for price updates."""
        self._symbol = symbol
        logger.info(f"Subscribed to {symbol}")

    def refresh(self):
        """Refresh price data."""
        self._get_price(self._symbol)
        # Update positions with current price
        for pos in self._positions.values():
            pos.current_price = self._get_price(self._symbol)

    def position_modify(self, ticket: int, sl: Optional[float] = None, tp: Optional[float] = None) -> bool:
        """Modify position SL/TP."""
        if ticket not in self._positions:
            logger.warning(f"Position {ticket} not found")
            return False
        
        if sl is not None:
            self._positions[ticket].sl = sl
        if tp is not None:
            self._positions[ticket].tp = tp
        
        logger.info(f"Position {ticket} modified: SL={sl}, TP={tp}")
        return True

    def order_modify(self, ticket: int, price: Optional[float] = None, sl: Optional[float] = None, tp: Optional[float] = None) -> bool:
        """Modify pending order."""
        for i, order in enumerate(self._orders):
            if order.ticket == ticket:
                if price is not None:
                    order.price = price
                if sl is not None:
                    order.sl = sl
                if tp is not None:
                    order.tp = tp
                logger.info(f"Order {ticket} modified: Price={price}, SL={sl}, TP={tp}")
                return True
        
        logger.warning(f"Order {ticket} not found")
        return False

    def buy(self, volume: float, symbol: str, price: float, sl: float, tp: float, magic: int = 0, comment: str = "") -> bool:
        """Place BUY market order (creates position immediately)."""
        order = self.place_order(
            symbol=symbol,
            order_type="BUY",
            volume=volume,
            price=price,
            sl=sl,
            tp=tp,
            magic=magic,
            comment=comment,
            create_position=True  # Market order creates position
        )
        return order is not None

    def sell(self, volume: float, symbol: str, price: float, sl: float, tp: float, magic: int = 0, comment: str = "") -> bool:
        """Place SELL market order (creates position immediately)."""
        order = self.place_order(
            symbol=symbol,
            order_type="SELL",
            volume=volume,
            price=price,
            sl=sl,
            tp=tp,
            magic=magic,
            comment=comment,
            create_position=True  # Market order creates position
        )
        return order is not None

    def buy_stop(self, volume: float, symbol: str, price: float, sl: float, tp: float, magic: int = 0, comment: str = "") -> bool:
        """Place BUY STOP pending order (creates order only, not position)."""
        order = self.place_order(
            symbol=symbol,
            order_type="BUY_STOP",
            volume=volume,
            price=price,
            sl=sl,
            tp=tp,
            magic=magic,
            comment=comment,
            create_position=False  # Pending order doesn't create position yet
        )
        return order is not None

    def sell_stop(self, volume: float, symbol: str, price: float, sl: float, tp: float, magic: int = 0, comment: str = "") -> bool:
        """Place SELL STOP pending order (creates order only, not position)."""
        order = self.place_order(
            symbol=symbol,
            order_type="SELL_STOP",
            volume=volume,
            price=price,
            sl=sl,
            tp=tp,
            magic=magic,
            comment=comment,
            create_position=False  # Pending order doesn't create position yet
        )
        return order is not None

    @property
    def positions(self) -> List[Position]:
        """Get all positions (compatibility property)."""
        return self.get_positions()

    @property
    def orders(self) -> List[Order]:
        """Get all orders (compatibility property)."""
        return self._orders

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
        """Place order (simulated). Returns Order object or None."""
        dry_run = kwargs.get("dry_run", False)
        create_position = kwargs.get("create_position", False)  # False for pending orders
        current_price = self._get_price(symbol)
        open_price = price if price is not None else current_price
        magic = kwargs.get("magic", 0)

        # Separate ticket numbers for orders (2000+) and positions (1000+)
        order_ticket = self._order_counter
        self._order_counter += 1

        order = Order(
            ticket=order_ticket,
            symbol=symbol,
            order_type=order_type,
            volume=volume,
            price=open_price,
            sl=sl,
            tp=tp,
            magic=magic,
            comment=kwargs.get("comment", "paper"),
            time_setup=datetime.now(),
        )

        if dry_run:
            logger.info(
                f"[DRY-RUN] Order: {order_type} {symbol} {volume} lots @ {open_price}"
                f" SL={sl} TP={tp}"
            )
            return order

        # Only create position for market orders (not pending orders)
        if create_position:
            position_ticket = self._position_counter
            self._position_counter += 1
            position = Position(
                ticket=position_ticket,
                symbol=symbol,
                order_type=order_type,
                volume=volume,
                open_price=open_price,
                current_price=current_price,
                sl=sl,
                tp=tp,
                profit=0.0,
                magic=magic,
                comment=kwargs.get("comment", "paper"),
                time_open=datetime.now(),
            )
            self._positions[position_ticket] = position
            logger.info(
                f"[PAPER] Position opened: {order_type} {symbol} {volume} lots @ {open_price}"
                f" SL={sl} TP={tp} ticket={position_ticket}"
            )

        self._orders.append(order)

        logger.info(
            f"[PAPER] Order placed: {order_type} {symbol} {volume} lots @ {open_price}"
            f" SL={sl} TP={tp} order_ticket={order_ticket} {'(position created)' if create_position else '(pending)'}"
        )
        return order

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

    def close_position(self, ticket: int, volume: Optional[float] = None, dry_run: bool = False) -> bool:
        """Close position dan update stats."""
        if ticket not in self._positions:
            logger.warning(f"Position {ticket} not found")
            return False

        if dry_run:
            logger.info(f"[DRY-RUN] Would close position {ticket}")
            return True
        
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
        """Get account info (paper trading, no real positions)."""
        balance = self._paper_stats["current_balance"] + self._paper_stats["net_profit"]
        return AccountInfo(
            login=0,
            balance=balance,
            equity=balance,
            margin=0.0,
            free_margin=balance,
            margin_level=0.0,
            currency="USD",
            leverage=100,
            server="paper",
            name="Paper Trader",
        )
