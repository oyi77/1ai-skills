"""
cTrader Connector

Implements broker connector for cTrader using cTrader Open API (Python SDK).
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

from ..base import BrokerConnector, BrokerType, OHLCV, Order, Position, AccountInfo

logger = logging.getLogger(__name__)


class CTraderConnector(BrokerConnector):
    """cTrader broker connector using Open API."""

    def __init__(self):
        super().__init__(BrokerType.CTRADER)
        self._client = None
        self._client_id = None
        self._client_secret = None
        self._access_token = None

    def _import_ctrader(self):
        """Lazy import of cTrader libraries."""
        if self._client is None:
            try:
                from ctrader_open_api import ApiClient
                self._ApiClient = ApiClient
                logger.info("cTrader Open API imported successfully")
            except ImportError as e:
                logger.error(
                    "cTrader Open API not installed. Install with: pip install ctrader-open-api ejtraderCT"
                )
                raise ImportError("cTrader Open API not installed") from e
        return self._ApiClient

    def connect(self, **kwargs) -> bool:
        """Connect to cTrader broker.

        Args:
            client_id: cTrader App Client ID
            client_secret: cTrader App Client Secret
            access_token: cTrader Access Token
            account_id: Optional, Account ID to use
        """
        ApiClient = self._import_ctrader()

        try:
            client_id = kwargs.get("client_id")
            client_secret = kwargs.get("client_secret")
            access_token = kwargs.get("access_token")

            if not all([client_id, client_secret, access_token]):
                logger.error("Missing required credentials: client_id, client_secret, access_token")
                return False

            self._client_id = client_id
            self._client_secret = client_secret
            self._access_token = access_token

            # Create API client
            self._client = ApiClient(
                client_id=client_id,
                client_secret=client_secret,
                access_token=access_token
            )

            # Connect
            self._client.connect()
            self.connected = True

            logger.info(f"Connected to cTrader account {kwargs.get('account_id', 'default')}")
            return True

        except Exception as e:
            logger.error(f"cTrader connection failed: {e}")
            self.connected = False
            return False

    def disconnect(self) -> bool:
        """Disconnect from cTrader."""
        try:
            if self._client:
                self._client.disconnect()
                self.connected = False
                logger.info("Disconnected from cTrader")
                return True
        except Exception as e:
            logger.error(f"Disconnect failed: {e}")
            return False

    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        count: Optional[int] = None,
    ) -> List[OHLCV]:
        """Fetch OHLCV data from cTrader."""
        try:
            if not self.is_connected():
                logger.error("Not connected to cTrader")
                return []

            # Map timeframe to cTrader format
            timeframe_map = {
                "M1": "m1", "M5": "m5", "M15": "m15",
                "M30": "m30", "H1": "h1", "H4": "h4",
                "D1": "d1", "W1": "w1", "MN": "mn"
            }

            tf = timeframe_map.get(timeframe, timeframe)

            # Fetch OHLCV data
            candles = self._client.get_ohlcv_data(symbol, tf, count=count or 100)

            ohlcv_list = []
            for candle in candles:
                ohlcv = OHLCV(
                    timestamp=datetime.fromtimestamp(candle.timestamp),
                    open=float(candle.open),
                    high=float(candle.high),
                    low=float(candle.low),
                    close=float(candle.close),
                    volume=float(candle.volume),
                )
                ohlcv_list.append(ohlcv)

            return ohlcv_list

        except Exception as e:
            logger.error(f"Failed to fetch OHLCV: {e}")
            return []

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
        """Place a trading order on cTrader."""
        try:
            if not self.is_connected():
                logger.error("Not connected to cTrader")
                return None

            # Place order via cTrader API
            result = self._client.place_order(
                symbol=symbol,
                side=order_type.lower(),  # "buy" or "sell"
                volume=volume,
                order_type="market" if price is None else "limit",
                price=price,
                sl=sl,
                tp=tp,
                **kwargs
            )

            if result and result.get("success"):
                order = Order(
                    ticket=result.get("order_id", 0),
                    symbol=symbol,
                    order_type=order_type.upper(),
                    volume=volume,
                    price=price or result.get("price", 0),
                    sl=sl,
                    tp=tp,
                    time_setup=datetime.now(),
                )
                logger.info(f"Order placed: {order.ticket} on {symbol}")
                return order
            else:
                logger.error(f"Order failed: {result}")
                return None

        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            return None

    def get_positions(self, symbol: Optional[str] = None) -> List[Position]:
        """Get open positions from cTrader."""
        try:
            if not self.is_connected():
                logger.error("Not connected to cTrader")
                return []

            positions = self._client.get_open_positions()

            position_list = []
            for pos in positions:
                if symbol is None or pos.symbol == symbol:
                    position = Position(
                        ticket=pos.position_id,
                        symbol=pos.symbol,
                        order_type=pos.direction.upper(),  # "BUY" or "SELL"
                        volume=float(pos.volume),
                        open_price=float(pos.entry_price),
                        current_price=float(pos.current_price),
                        sl=float(pos.stop_loss) if pos.stop_loss else None,
                        tp=float(pos.take_profit) if pos.take_profit else None,
                        profit=float(pos.gross_profit),
                        time_open=datetime.fromtimestamp(pos.open_time),
                    )
                    position_list.append(position)

            return position_list

        except Exception as e:
            logger.error(f"Failed to get positions: {e}")
            return []

    def get_account_info(self) -> Optional[AccountInfo]:
        """Get account information from cTrader."""
        try:
            if not self.is_connected():
                logger.error("Not connected to cTrader")
                return None

            account = self._client.get_account()

            info = AccountInfo(
                login=int(account.account_id),
                balance=float(account.balance),
                equity=float(account.equity),
                margin=float(account.margin),
                free_margin=float(account.free_margin),
                margin_level=float(account.margin_level) if account.margin_level else 0,
                currency=account.currency,
                leverage=1,  # cTrader uses netting, not leverage
                server=account.server if hasattr(account, "server") else "",
                name=account.name if hasattr(account, "name") else "",
            )

            logger.info(f"Account info: Balance={info.balance}, Equity={info.equity}")
            return info

        except Exception as e:
            logger.error(f"Failed to get account info: {e}")
            return None

    def close_position(self, ticket: int) -> bool:
        """Close a position by ticket ID."""
        try:
            if not self.is_connected():
                logger.error("Not connected to cTrader")
                return False

            result = self._client.close_position(ticket)

            if result and result.get("success"):
                logger.info(f"Position closed: {ticket}")
                return True
            else:
                logger.error(f"Failed to close position: {result}")
                return False

        except Exception as e:
            logger.error(f"Failed to close position: {e}")
            return False

    def modify_position(
        self,
        ticket: int,
        sl: Optional[float] = None,
        tp: Optional[float] = None,
    ) -> bool:
        """Modify a position's SL/TP."""
        try:
            if not self.is_connected():
                logger.error("Not connected to cTrader")
                return False

            result = self._client.modify_position(ticket, sl=sl, tp=tp)

            if result and result.get("success"):
                logger.info(f"Position modified: {ticket}")
                return True
            else:
                logger.error(f"Failed to modify position: {result}")
                return False

        except Exception as e:
            logger.error(f"Failed to modify position: {e}")
            return False
