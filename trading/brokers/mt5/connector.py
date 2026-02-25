"""
MetaTrader 5 Connector (via mt5linux / rpyc bridge)

Uses mt5linux package which provides a remote MetaTrader5 instance
over rpyc — NOT the local MetaTrader5 package.

Host: 5.189.138.144:18812
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

from ..base import BrokerConnector, BrokerType, OHLCV, Order, Position, AccountInfo

logger = logging.getLogger(__name__)


class MT5Connector(BrokerConnector):
    """MetaTrader 5 broker connector via mt5linux (rpyc bridge)."""

    def __init__(self, host: str = "5.189.138.144", port: int = 18812):
        super().__init__(BrokerType.MT5)
        self._mt5 = None
        self._host = host
        self._port = port

    def _import_mt5(self):
        """Lazy import and connect to MT5 via mt5linux."""
        if self._mt5 is None:
            try:
                from mt5linux import MetaTrader5
                self._mt5 = MetaTrader5(host=self._host, port=self._port)
                logger.info(f"mt5linux connected to {self._host}:{self._port}")
            except ImportError:
                raise ImportError(
                    "mt5linux not installed. Run: pip install mt5linux"
                )
        return self._mt5

    def connect(self, **kwargs) -> bool:
        """Connect to MetaTrader 5 via mt5linux bridge."""
        mt5 = self._import_mt5()

        if not mt5.initialize():
            error = mt5.last_error()
            logger.error(f"MT5 initialize failed: {error}")
            return False

        login = kwargs.get("login")
        password = kwargs.get("password", "")
        server = kwargs.get("server", "")

        if login:
            if not mt5.login(login, password=password, server=server):
                logger.error(f"MT5 login failed: {mt5.last_error()}")
                mt5.shutdown()
                return False

        self.connected = True
        logger.info("Connected to MT5 via mt5linux")
        return True

    def disconnect(self) -> bool:
        """Disconnect from MetaTrader 5."""
        if self._mt5 is not None:
            try:
                self._mt5.shutdown()
            except Exception as e:
                logger.warning(f"MT5 shutdown error: {e}")
            self._mt5 = None
            self.connected = False
            logger.info("Disconnected from MT5")
        return True

    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "H1",
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        count: Optional[int] = None,
    ) -> List[OHLCV]:
        """Fetch OHLCV data from MT5."""
        mt5 = self._import_mt5()

        # Convert timeframe string to MT5 constant
        timeframe_map = {
            "M1":  mt5.TIMEFRAME_M1,
            "M5":  mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1":  mt5.TIMEFRAME_H1,
            "H4":  mt5.TIMEFRAME_H4,
            "D1":  mt5.TIMEFRAME_D1,
            "W1":  mt5.TIMEFRAME_W1,
            "MN1": mt5.TIMEFRAME_MN1,
        }
        mt5_timeframe = timeframe_map.get(timeframe.upper(), mt5.TIMEFRAME_H1)

        # Fetch data
        if count and not start:
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
        elif start:
            rates = mt5.copy_rates_from(symbol, mt5_timeframe, start, count or 1000)
        else:
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count or 100)

        if rates is None:
            error = mt5.last_error()
            logger.error(f"Failed to get OHLCV for {symbol}: {error}")
            return []

        ohlcv_list = []
        for rate in rates:
            ohlcv_list.append(
                OHLCV(
                    timestamp=datetime.fromtimestamp(rate[0]),
                    open=float(rate[1]),
                    high=float(rate[2]),
                    low=float(rate[3]),
                    close=float(rate[4]),
                    volume=float(rate[5]),
                )
            )

        logger.info(f"Fetched {len(ohlcv_list)} candles for {symbol} {timeframe}")
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
        """Place a market or pending order."""
        mt5 = self._import_mt5()

        # Get price for market orders
        if price is None:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                logger.error(f"Failed to get tick for {symbol}")
                return None
            price = tick.ask if order_type.upper() == "BUY" else tick.bid

        # Order type mapping
        order_type_map = {
            "BUY":        mt5.ORDER_TYPE_BUY,
            "SELL":       mt5.ORDER_TYPE_SELL,
            "BUY_LIMIT":  mt5.ORDER_TYPE_BUY_LIMIT,
            "SELL_LIMIT": mt5.ORDER_TYPE_SELL_LIMIT,
            "BUY_STOP":   mt5.ORDER_TYPE_BUY_STOP,
            "SELL_STOP":  mt5.ORDER_TYPE_SELL_STOP,
            # alternate underscore-free spellings
            "BUYLIMIT":   mt5.ORDER_TYPE_BUY_LIMIT,
            "SELLLIMIT":  mt5.ORDER_TYPE_SELL_LIMIT,
            "BUYSTOP":    mt5.ORDER_TYPE_BUY_STOP,
            "SELLSTOP":   mt5.ORDER_TYPE_SELL_STOP,
        }
        mt5_order_type = order_type_map.get(order_type.upper(), mt5.ORDER_TYPE_BUY)

        # Market vs pending
        is_pending = order_type.upper() in (
            "BUY_LIMIT", "SELL_LIMIT", "BUY_STOP", "SELL_STOP",
            "BUYLIMIT", "SELLLIMIT", "BUYSTOP", "SELLSTOP"
        )
        action = mt5.TRADE_ACTION_PENDING if is_pending else mt5.TRADE_ACTION_DEAL

        request = {
            "action":       action,
            "symbol":       symbol,
            "volume":       float(volume),
            "type":         mt5_order_type,
            "price":        float(price),
            "deviation":    kwargs.get("deviation", 20),
            "magic":        kwargs.get("magic", 234000),
            "comment":      kwargs.get("comment", "berkahkarya"),
            "type_time":    mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        if sl is not None:
            request["sl"] = float(sl)
        if tp is not None:
            request["tp"] = float(tp)

        result = mt5.order_send(request)

        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            err = result.comment if result else "No result"
            logger.error(f"Order failed ({order_type} {symbol}): {err}")
            return None

        return Order(
            ticket=result.order,
            symbol=symbol,
            order_type=order_type,
            volume=float(volume),
            price=float(price),
            sl=sl,
            tp=tp,
            magic=request["magic"],
            comment=request["comment"],
            time_setup=datetime.now(),
        )

    def get_positions(self, symbol: Optional[str] = None) -> List[Position]:
        """Get open positions."""
        mt5 = self._import_mt5()

        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        else:
            positions = mt5.positions_get()

        if positions is None:
            return []

        position_list = []
        for pos in positions:
            position_list.append(
                Position(
                    ticket=pos.ticket,
                    symbol=pos.symbol,
                    order_type="BUY" if pos.type == 0 else "SELL",
                    volume=float(pos.volume),
                    open_price=float(pos.price_open),
                    current_price=float(pos.price_current),
                    sl=float(pos.sl) if pos.sl else None,
                    tp=float(pos.tp) if pos.tp else None,
                    profit=float(pos.profit),
                    comment=pos.comment,
                    time_open=datetime.fromtimestamp(pos.time),
                )
            )

        return position_list

    def close_position(self, ticket: int, volume: Optional[float] = None) -> bool:
        """Close an open position by ticket."""
        mt5 = self._import_mt5()

        # Find the position
        positions = mt5.positions_get()
        if positions is None:
            logger.error("Could not fetch positions")
            return False

        pos = None
        for p in positions:
            if p.ticket == ticket:
                pos = p
                break

        if pos is None:
            logger.warning(f"Position {ticket} not found")
            return False

        # Opposite action to close
        if pos.type == mt5.ORDER_TYPE_BUY:
            close_type = mt5.ORDER_TYPE_SELL
            tick = mt5.symbol_info_tick(pos.symbol)
            price = tick.bid if tick else pos.price_current
        else:
            close_type = mt5.ORDER_TYPE_BUY
            tick = mt5.symbol_info_tick(pos.symbol)
            price = tick.ask if tick else pos.price_current

        request = {
            "action":       mt5.TRADE_ACTION_DEAL,
            "symbol":       pos.symbol,
            "volume":       float(volume or pos.volume),
            "type":         close_type,
            "position":     ticket,
            "price":        float(price),
            "deviation":    20,
            "magic":        234000,
            "comment":      "berkahkarya-close",
            "type_time":    mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        result = mt5.order_send(request)

        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            err = result.comment if result else "No result"
            logger.error(f"Close position {ticket} failed: {err}")
            return False

        logger.info(f"Position {ticket} closed")
        return True

    def get_account_info(self) -> Optional[AccountInfo]:
        """Get account information."""
        mt5 = self._import_mt5()

        info = mt5.account_info()
        if info is None:
            logger.error(f"Failed to get account info: {mt5.last_error()}")
            return None

        return AccountInfo(
            login=int(info.login),
            balance=float(info.balance),
            equity=float(info.equity),
            margin=float(info.margin),
            free_margin=float(info.margin_free),
            margin_level=float(info.margin_level) if info.margin_level else 0.0,
            currency=str(info.currency),
            leverage=int(info.leverage),
            server=str(info.server),
            name=str(info.name),
        )

    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get symbol information."""
        mt5 = self._import_mt5()

        info = mt5.symbol_info(symbol)
        if info is None:
            return None

        return {
            "name":             info.name,
            "point":            info.point,
            "digits":           info.digits,
            "trade_tick_size":  info.trade_tick_size,
            "trade_tick_value": info.trade_tick_value,
            "volume_min":       info.volume_min,
            "volume_max":       info.volume_max,
            "volume_step":      info.volume_step,
        }

    # =========================================================
    # Pending Order Helpers
    # =========================================================

    def place_pending_order(
        self,
        symbol: str,
        order_type: str,
        volume: float,
        price: float,
        sl: Optional[float] = None,
        tp: Optional[float] = None,
        **kwargs,
    ) -> Optional[Order]:
        """Place a pending order (BUY_STOP, SELL_STOP, BUY_LIMIT, SELL_LIMIT)."""
        return self.place_order(
            symbol=symbol,
            order_type=order_type,
            volume=volume,
            price=price,
            sl=sl,
            tp=tp,
            **kwargs,
        )

    def cancel_pending_order(self, ticket: int) -> bool:
        """Cancel a pending order."""
        mt5 = self._import_mt5()

        request = {
            "action":  mt5.TRADE_ACTION_REMOVE,
            "order":   ticket,
            "comment": "berkahkarya-cancel",
        }

        result = mt5.order_send(request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            err = result.comment if result else "No result"
            logger.error(f"Cancel order {ticket} failed: {err}")
            return False

        logger.info(f"Pending order {ticket} cancelled")
        return True

    def get_pending_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """Get pending orders."""
        mt5 = self._import_mt5()

        if symbol:
            orders = mt5.orders_get(symbol=symbol)
        else:
            orders = mt5.orders_get()

        if orders is None:
            return []

        type_map = {
            mt5.ORDER_TYPE_BUY_LIMIT:  "BUY_LIMIT",
            mt5.ORDER_TYPE_SELL_LIMIT: "SELL_LIMIT",
            mt5.ORDER_TYPE_BUY_STOP:   "BUY_STOP",
            mt5.ORDER_TYPE_SELL_STOP:  "SELL_STOP",
        }

        order_list = []
        for order in orders:
            order_list.append(
                Order(
                    ticket=order.ticket,
                    symbol=order.symbol,
                    order_type=type_map.get(order.type, "UNKNOWN"),
                    volume=float(order.volume_initial),
                    price=float(order.price_open),
                    sl=float(order.sl) if order.sl else None,
                    tp=float(order.tp) if order.tp else None,
                    magic=order.magic,
                    comment=order.comment,
                    time_setup=datetime.fromtimestamp(order.time_setup),
                    time_done=datetime.fromtimestamp(order.time_done) if order.time_done > 0 else None,
                )
            )

        return order_list

    def cancel_all_pending_orders(self, symbol: Optional[str] = None) -> int:
        """Cancel all pending orders, optionally filtered by symbol."""
        pending = self.get_pending_orders(symbol)
        cancelled = 0
        for order in pending:
            if symbol is None or order.symbol == symbol:
                if self.cancel_pending_order(order.ticket):
                    cancelled += 1
        logger.info(f"Cancelled {cancelled} pending orders")
        return cancelled

    def get_history_deals(
        self,
        symbol: Optional[str] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """Get historical deals."""
        mt5 = self._import_mt5()

        if start is None:
            start = datetime.now().replace(day=1)
        if end is None:
            end = datetime.now()

        if symbol:
            deals = mt5.history_deals_get(symbol, start, end)
        else:
            deals = mt5.history_deals_get(start, end)

        if deals is None:
            return []

        deal_list = []
        for deal in deals:
            deal_list.append({
                "ticket":     deal.ticket,
                "order":      deal.order,
                "symbol":     deal.symbol,
                "type":       "BUY" if deal.type == 0 else "SELL",
                "volume":     float(deal.volume),
                "price":      float(deal.price),
                "profit":     float(deal.profit),
                "fee":        float(deal.fee),
                "commission": float(deal.commission),
                "time":       datetime.fromtimestamp(deal.time),
                "comment":    deal.comment,
            })

        return deal_list
