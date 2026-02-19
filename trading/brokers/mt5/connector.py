"""
MetaTrader 5 Connector

Implements broker connector for MetaTrader 5 using the official MT5 Python library.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

from ..base import BrokerConnector, BrokerType, OHLCV, Order, Position, AccountInfo

logger = logging.getLogger(__name__)


class MT5Connector(BrokerConnector):
    """MetaTrader 5 broker connector."""

    def __init__(self):
        super().__init__(BrokerType.MT5)
        self._mt5 = None

    def _import_mt5(self):
        """Lazy import of MT5 library."""
        if self._mt5 is None:
            try:
                import MetaTrader5 as mt5

                self._mt5 = mt5
            except ImportError:
                logger.error(
                    "MetaTrader5 package not installed. Install with: pip install MetaTrader5"
                )
                raise ImportError("MetaTrader5 package not installed")
        return self._mt5

    def connect(self, **kwargs) -> bool:
        """Connect to MetaTrader 5 terminal."""
        mt5 = self._import_mt5()

        # Initialize connection
        path = kwargs.get("path")
        login = kwargs.get("login")
        password = kwargs.get("password")
        server = kwargs.get("server")
        timeout = kwargs.get("timeout", 60000)

        if not mt5.initialize():
            error = mt5.last_error()
            logger.error(f"MT5 initialize failed: {error}")
            return False

        # Login if credentials provided
        if login:
            if not mt5.login(login, password=password, server=server):
                logger.error(f"MT5 login failed: {mt5.last_error()}")
                mt5.shutdown()
                return False

        self.connected = True
        logger.info("Connected to MetaTrader 5")
        return True

    def disconnect(self) -> bool:
        """Disconnect from MetaTrader 5."""
        if self._mt5:
            self._mt5.shutdown()
            self.connected = False
            logger.info("Disconnected from MetaTrader 5")
        return True

    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        count: Optional[int] = None,
    ) -> List[OHLCV]:
        """Fetch OHLCV data from MT5."""
        mt5 = self._import_mt5()

        # Convert timeframe string to MT5 constant
        timeframe_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
            "W1": mt5.TIMEFRAME_W1,
            "MN1": mt5.TIMEFRAME_MN1,
        }
        mt5_timeframe = timeframe_map.get(timeframe.upper(), mt5.TIMEFRAME_H1)

        # Fetch data
        if count:
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
        elif start:
            rates = mt5.copy_rates_from(symbol, mt5_timeframe, start, count or 1000)
        else:
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count or 1000)

        if rates is None:
            error = mt5.last_error()
            logger.error(f"Failed to get OHLCV for {symbol}: {error}")
            return []

        # Convert to OHLCV objects
        ohlcv_list = []
        for rate in rates:
            ohlcv_list.append(
                OHLCV(
                    timestamp=datetime.fromtimestamp(rate[0]),
                    open=rate[1],
                    high=rate[2],
                    low=rate[3],
                    close=rate[4],
                    volume=rate[5],
                )
            )

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
        """Place a trading order."""
        mt5 = self._import_mt5()

        # Get current price if not specified
        if price is None:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                logger.error(f"Failed to get tick for {symbol}")
                return None
            price = tick.ask if order_type.upper() == "BUY" else tick.bid

        # Map order type
        order_type_map = {
            "BUY": mt5.ORDER_TYPE_BUY,
            "SELL": mt5.ORDER_TYPE_SELL,
            "BUY_LIMIT": mt5.ORDER_TYPE_BUY_LIMIT,
            "SELL_LIMIT": mt5.ORDER_TYPE_SELL_LIMIT,
            "BUY_STOP": mt5.ORDER_TYPE_BUY_STOP,
            "SELL_STOP": mt5.ORDER_TYPE_SELL_STOP,
        }
        mt5_order_type = order_type_map.get(order_type.upper(), mt5.ORDER_TYPE_BUY)

        # Build request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5_order_type,
            "price": price,
            "deviation": kwargs.get("deviation", 20),
            "magic": kwargs.get("magic", 234000),
            "comment": kwargs.get("comment", "trading-skill"),
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        if sl:
            request["sl"] = sl
        if tp:
            request["tp"] = tp

        # Send order
        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Order failed: {result.comment}")
            return None

        return Order(
            ticket=result.order,
            symbol=symbol,
            order_type=order_type,
            volume=volume,
            price=price,
            sl=sl,
            tp=tp,
            magic=request["magic"],
            comment=request["comment"],
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
                    volume=pos.volume,
                    open_price=pos.price_open,
                    current_price=pos.price_current,
                    sl=pos.sl,
                    tp=pos.tp,
                    profit=pos.profit,
                    comment=pos.comment,
                    time_open=datetime.fromtimestamp(pos.time),
                )
            )

        return position_list

    def get_account_info(self) -> Optional[AccountInfo]:
        """Get account information."""
        mt5 = self._import_mt5()

        info = mt5.account_info()
        if info is None:
            logger.error("Failed to get account info")
            return None

        return AccountInfo(
            login=info.login,
            balance=info.balance,
            equity=info.equity,
            margin=info.margin,
            free_margin=info.margin_free,
            margin_level=info.margin_level,
            currency=info.currency,
            leverage=info.leverage,
            server=info.server,
            name=info.name,
        )

    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get symbol information."""
        mt5 = self._import_mt5()

        info = mt5.symbol_info(symbol)
        if info is None:
            return None

        return {
            "name": info.name,
            "point": info.point,
            "digits": info.digits,
            "trade_tick_size": info.trade_tick_size,
            "trade_tick_value": info.trade_tick_value,
            "volume_min": info.volume_min,
            "volume_max": info.volume_max,
            "volume_step": info.volume_step,
        }

    # ============ PENDING ORDER SUPPORT (For XAUUSD 7-Candle Strategy) ============

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
        """Place a pending order (BUY_STOP, SELL_STOP, BUY_LIMIT, SELL_LIMIT).
        
        This is essential for the XAUUSD 7-Candle Breakout strategy.
        """
        mt5 = self._import_mt5()

        # Map order type for pending orders
        order_type_map = {
            "BUY_STOP": mt5.ORDER_TYPE_BUY_STOP,
            "SELL_STOP": mt5.ORDER_TYPE_SELL_STOP,
            "BUY_LIMIT": mt5.ORDER_TYPE_BUY_LIMIT,
            "SELL_LIMIT": mt5.ORDER_TYPE_SELL_LIMIT,
        }
        mt5_order_type = order_type_map.get(order_type.upper())

        if mt5_order_type is None:
            logger.error(f"Invalid pending order type: {order_type}")
            return None

        # Build request for pending order
        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": mt5_order_type,
            "price": price,
            "deviation": kwargs.get("deviation", 20),
            "magic": kwargs.get("magic", 234000),
            "comment": kwargs.get("comment", "trading-skill-pending"),
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        if sl:
            request["sl"] = sl
        if tp:
            request["tp"] = tp

        # Send order
        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Pending order failed: {result.comment}")
            return None

        return Order(
            ticket=result.order,
            symbol=symbol,
            order_type=order_type,
            volume=volume,
            price=price,
            sl=sl,
            tp=tp,
            magic=request["magic"],
            comment=request["comment"],
        )

    def cancel_pending_order(self, ticket: int) -> bool:
        """Cancel a pending order by ticket number."""
        mt5 = self._import_mt5()

        request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": ticket,
            "comment": "trading-skill-cancel",
        }

        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Cancel order failed: {result.comment}")
            return False

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

        order_list = []
        for order in orders:
            # Map MT5 order type back to string
            type_map = {
                mt5.ORDER_TYPE_BUY_LIMIT: "BUY_LIMIT",
                mt5.ORDER_TYPE_SELL_LIMIT: "SELL_LIMIT",
                mt5.ORDER_TYPE_BUY_STOP: "BUY_STOP",
                mt5.ORDER_TYPE_SELL_STOP: "SELL_STOP",
            }
            order_type_str = type_map.get(order.type, "UNKNOWN")

            order_list.append(
                Order(
                    ticket=order.ticket,
                    symbol=order.symbol,
                    order_type=order_type_str,
                    volume=order.volume_initial,
                    price=order.price_open,
                    sl=order.sl,
                    tp=order.tp,
                    magic=order.magic,
                    comment=order.comment,
                    time_setup=datetime.fromtimestamp(order.time_setup),
                    time_done=datetime.fromtimestamp(order.time_done) if order.time_done > 0 else None,
                )
            )

        return order_list

    def cancel_all_pending_orders(self, symbol: Optional[str] = None) -> int:
        """Cancel all pending orders."""
        pending_orders = self.get_pending_orders(symbol)
        cancelled = 0

        for order in pending_orders:
            if order.symbol == symbol or symbol is None:
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
            start = datetime.now().replace(day=1)  # Default to first of month

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
                "ticket": deal.ticket,
                "order": deal.order,
                "symbol": deal.symbol,
                "type": "BUY" if deal.type == 0 else "SELL",
                "volume": deal.volume,
                "price": deal.price,
                "profit": deal.profit,
                "fee": deal.fee,
                "commission": deal.commission,
                "time": datetime.fromtimestamp(deal.time),
                "comment": deal.comment,
            })

        return deal_list
