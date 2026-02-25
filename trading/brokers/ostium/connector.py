"""
Ostium Connector

Implements broker connector for Ostium (Decentralized Perpetual Exchange).
Supports Crypto, RWA (Commodities, Indices, Forex).
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

from ..base import BrokerConnector, BrokerType, OHLCV, Order, Position, AccountInfo

logger = logging.getLogger(__name__)


class OstiumConnector(BrokerConnector):
    """Ostium broker connector using Python SDK."""

    def __init__(self):
        super().__init__(BrokerType.CCXT)  # Using CCXT type for now, may need new type
        self._client = None
        self._api_key = None
        self._wallet_address = None

    def _import_ostium(self):
        """Lazy import of Ostium library."""
        if self._client is None:
            try:
                from ostium_python_sdk import OstiumClient
                self._OstiumClient = OstiumClient
                logger.info("Ostium SDK imported successfully")
            except ImportError as e:
                logger.error(
                    "Ostium SDK not installed. Install with: pip install ostium-python-sdk"
                )
                raise ImportError("Ostium SDK not installed") from e
        return self._OstiumClient

    def connect(self, **kwargs) -> bool:
        """Connect to Ostium blockchain.

        Args:
            api_key: Ostium API Key
            wallet_address: Ethereum wallet address for signing
        """
        OstiumClient = self._import_ostium()

        try:
            api_key = kwargs.get("api_key")
            wallet_address = kwargs.get("wallet_address")

            if not api_key:
                logger.error("Missing required credential: api_key")
                return False

            self._api_key = api_key
            self._wallet_address = wallet_address

            # Create Ostium client
            self._client = OstiumClient(
                api_key=api_key
            )

            # Test connection
            account = self._client.get_account()
            if account:
                self.connected = True
                logger.info(f"Connected to Ostium")
                return True
            else:
                logger.error("Failed to connect to Ostium")
                return False

        except Exception as e:
            logger.error(f"Ostium connection failed: {e}")
            self.connected = False
            return False

    def disconnect(self) -> bool:
        """Disconnect from Ostium."""
        try:
            self._client = None
            self.connected = False
            logger.info("Disconnected from Ostium")
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
        """Fetch OHLCV data from Ostium."""
        try:
            if not self.is_connected():
                logger.error("Not connected to Ostium")
                return []

            # Ostium uses standard trading pair symbols like "ETH-USDT", "XAU-USDT"
            # Map timeframe to Ostium format (seconds)
            timeframe_map = {
                "1m": 60, "5m": 300, "15m": 900,
                "30m": 1800, "1h": 3600, "4h": 14400,
                "1d": 86400, "1w": 604800
            }

            tf = timeframe_map.get(timeframe, 3600)  # Default 1h

            # Fetch OHLCV data via REST API
            candles = self._client.get_klines(
                symbol=symbol,
                interval=tf,
                limit=count or 100
            )

            ohlcv_list = []
            for candle in candles:
                ohlcv = OHLCV(
                    timestamp=datetime.fromtimestamp(candle[0] / 1000),
                    open=float(candle[1]),
                    high=float(candle[2]),
                    low=float(candle[3]),
                    close=float(candle[4]),
                    volume=float(candle[5]) if len(candle) > 5 else 0,
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
        """Place a trading order on Ostium."""
        try:
            if not self.is_connected():
                logger.error("Not connected to Ostium")
                return None

            # Ostium supports MARKET and LIMIT orders
            # Determine side: 'buy' or 'sell' based on order_type
            side = order_type.lower()

            # Build order parameters
            order_params = {
                "symbol": symbol,
                "side": side,
                "type": "limit" if price is not None else "market",
                "amount": volume,
            }

            if price is not None:
                order_params["price"] = price

            # Place order via Ostium API
            result = self._client.place_order(**order_params)

            if result and result.get("success"):
                order = Order(
                    ticket=result.get("order_id", 0),
                    symbol=symbol,
                    order_type=order_type.upper(),
                    volume=volume,
                    price=result.get("price", 0),
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
        """Get open positions from Ostium."""
        try:
            if not self.is_connected():
                logger.error("Not connected to Ostium")
                return []

            positions = self._client.get_open_positions()

            position_list = []
            for pos in positions:
                if symbol is None or pos["symbol"] == symbol:
                    position = Position(
                        ticket=pos.get("order_id", 0),
                        symbol=pos["symbol"],
                        order_type=pos.get("side", "").upper(),
                        volume=float(pos.get("amount", 0)),
                        open_price=float(pos.get("entry_price", 0)),
                        current_price=float(pos.get("mark_price", 0)),
                        sl=float(pos.get("stop_loss")) if pos.get("stop_loss") else None,
                        tp=float(pos.get("take_profit")) if pos.get("take_profit") else None,
                        profit=float(pos.get("unrealized_pnl", 0)),
                        time_open=datetime.fromtimestamp(pos.get("open_time", 0)),
                    )
                    position_list.append(position)

            return position_list

        except Exception as e:
            logger.error(f"Failed to get positions: {e}")
            return []

    def get_account_info(self) -> Optional[AccountInfo]:
        """Get account information from Ostium."""
        try:
            if not self.is_connected():
                logger.error("Not connected to Ostium")
                return None

            account = self._client.get_account()

            info = AccountInfo(
                login=int(hash(account.get("address", ""))[:10], 16),  # Hash address as login
                balance=float(account.get("balance", 0)),
                equity=float(account.get("balance", 0)),  # Perpetual uses balance
                margin=float(account.get("margin_used", 0)),
                free_margin=float(account.get("free_balance", 0)),
                margin_level=0,  # Ostium uses different margin model
                currency="USDT",
                leverage=int(account.get("leverage", 1)),
                server="Ostium",
                name="Ostium Perpetual",
            )

            logger.info(f"Account info: Balance={info.balance}")
            return info

        except Exception as e:
            logger.error(f"Failed to get account info: {e}")
            return None

    def close_position(self, ticket: int) -> bool:
        """Close a position by ticket ID."""
        try:
            if not self.is_connected():
                logger.error("Not connected to Ostium")
                return False

            result = self._client.cancel_order(str(ticket))

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
                logger.error("Not connected to Ostium")
                return False

            # Ostium uses modify_order endpoint
            result = self._client.modify_order(
                order_id=str(ticket),
                stop_loss=sl,
                take_profit=tp,
            )

            if result and result.get("success"):
                logger.info(f"Position modified: {ticket}")
                return True
            else:
                logger.error(f"Failed to modify position: {result}")
                return False

        except Exception as e:
            logger.error(f"Failed to modify position: {e}")
            return False

    def get_available_symbols(self) -> List[str]:
        """Get available trading symbols from Ostium."""
        try:
            if not self.is_connected():
                logger.error("Not connected to Ostium")
                return []

            # Ostium supports various RWA assets
            # Common symbols: ETH-USDT, BTC-USDT, XAU-USDT (Gold), EUR-USDT, etc.
            symbols = self._client.get_symbols()

            return symbols

        except Exception as e:
            logger.error(f"Failed to get symbols: {e}")
            return []
