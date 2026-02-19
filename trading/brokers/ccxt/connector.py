"""
CCXT Connector

Implements broker connector for cryptocurrency exchanges using CCXT.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

from trading.utils.error_handler import retry
from ..base import (
    BrokerConnector,
    BrokerType,
    OHLCV,
    Order,
    Position,
    AccountInfo,
)

logger = logging.getLogger(__name__)


class CCXTConnector(BrokerConnector):
    """CCXT broker connector for cryptocurrency exchanges."""

    def __init__(self, exchange_id: str = "binance"):
        super().__init__(BrokerType.CCXT)
        self.exchange_id = exchange_id
        self._exchange = None
        self._health_status = False

    @property
    def is_healthy(self) -> bool:
        """Check if the connector is healthy."""
        return self._health_status

    def health_check(self) -> bool:
        """Test connection to the exchange.
        
        Returns:
            True if connection is healthy, False otherwise.
        """
        try:
            exchange = self._get_exchange()
            # Try to fetch time to verify connection
            exchange.fetch_time()
            self._health_status = True
            logger.info(f"Health check passed for {self.exchange_id}")
            return True
        except Exception as e:
            self._health_status = False
            logger.error(f"Health check failed for {self.exchange_id}: {e}")
            return False

    def _get_exchange(self):
        """Get or create CCXT exchange instance."""
        if self._exchange is None:
            try:
                import ccxt

                exchange_class = getattr(ccxt, self.exchange_id)
                self._exchange = exchange_class(
                    {
                        "enableRateLimit": True,
                    }
                )
            except ImportError:
                logger.error(
                    "CCXT package not installed. Install with: pip install ccxt"
                )
                raise ImportError("CCXT package not installed")
        return self._exchange

    @retry(max_attempts=3, backoff=1.0)
    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        count: Optional[int] = None,
    ) -> List[OHLCV]:
        """Fetch OHLCV data from exchange."""
        exchange = self._get_exchange()

        # Map timeframe
        timeframe_map = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "4h": "4h",
            "1d": "1d",
            "1w": "1w",
        }
        ccxt_timeframe = timeframe_map.get(timeframe.lower(), "1h")

        # Prepare parameters
        params = {}
        if start:
            params["since"] = int(start.timestamp() * 1000)
        if count:
            params["limit"] = count

        # Let exceptions propagate to retry decorator
        ohlcv_data = exchange.fetch_ohlcv(symbol, ccxt_timeframe, **params)

        # Convert to OHLCV objects
        ohlcv_list = []
        for candle in ohlcv_data:
            ohlcv_list.append(
                OHLCV(
                    timestamp=datetime.fromtimestamp(candle[0] / 1000),
                    open=candle[1],
                    high=candle[2],
                    low=candle[3],
                    close=candle[4],
                    volume=candle[5],
                )
            )

        return ohlcv_list

    @retry(max_attempts=3, backoff=1.0)
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
        exchange = self._get_exchange()

        # Map order type
        order_type_map = {
            "BUY": "limit",
            "SELL": "limit",
            "BUY_LIMIT": "limit",
            "SELL_LIMIT": "limit",
            "BUY_MARKET": "market",
            "SELL_MARKET": "market",
        }
        ccxt_type = order_type_map.get(order_type.upper(), "limit")

        # Prepare order parameters
        order_params = {
            "symbol": symbol,
            "type": ccxt_type,
            "side": "buy" if "BUY" in order_type.upper() else "sell",
            "amount": volume,
        }

        if price:
            order_params["price"] = price

        # CCXT doesn't support SL/TP directly, implement via params
        # For now, just place basic order

        # Let exceptions propagate to retry decorator
        result = exchange.create_order(**order_params)

        return Order(
            ticket=hash(result["id"]),
            symbol=symbol,
            order_type=order_type,
            volume=volume,
            price=result.get("price", price or 0),
            sl=sl,
            tp=tp,
            comment=result.get("id", ""),
        )

    @retry(max_attempts=3, backoff=1.0)
    def get_positions(self, symbol: Optional[str] = None) -> List[Position]:
        """Get open positions."""
        exchange = self._get_exchange()

        # Let exceptions propagate to retry decorator
        positions = exchange.fetch_positions()

        position_list = []
        for pos in positions:
            if pos["contracts"] and pos["contracts"] > 0:
                if symbol and pos["symbol"] != symbol:
                    continue

                position_list.append(
                    Position(
                        ticket=hash(pos["id"]),
                        symbol=pos["symbol"],
                        order_type="BUY" if pos["side"] == "long" else "SELL",
                        volume=pos["contracts"],
                        open_price=pos["entryPrice"],
                        current_price=pos.get("markPrice", pos["entryPrice"]),
                        sl=pos.get("stopLoss"),
                        tp=pos.get("takeProfit"),
                        profit=pos.get("unrealizedPnl", 0),
                    )
                )

        return position_list

    @retry(max_attempts=3, backoff=1.0)
    def get_account_info(self) -> Optional[AccountInfo]:
        """Get account information."""
        exchange = self._get_exchange()

        # Let exceptions propagate to retry decorator
        balance = exchange.fetch_balance()

        total = balance.get("total", {})
        free = balance.get("free", {})

        return AccountInfo(
            login=0,  # CCXT doesn't have login
            balance=total.get("USD", total.get("USDT", 0)),
            equity=total.get("USD", total.get("USDT", 0)),
            margin=0,  # Not directly available
            free_margin=free.get("USD", free.get("USDT", 0)),
            margin_level=0,
            currency="USDT",
            leverage=1,  # Default
            server=self.exchange_id,
            name=exchange.id,
        )

    def set_leverage(self, symbol: str, leverage: int):
        """Set leverage for a symbol."""
        exchange = self._get_exchange()
        try:
            exchange.set_leverage(leverage, symbol)
        except Exception as e:
            logger.error(f"Failed to set leverage: {e}")
