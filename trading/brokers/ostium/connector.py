"""
Ostium Connector

Implements broker connector for Ostium (Decentralized Perpetual Exchange).
Supports Crypto, RWA (Commodities, Indices, Forex).

Pair IDs (as of May 2025):
    0:  BTC-USD (Bitcoin)
    1:  ETH-USD (Ethereum)
    2:  EUR-USD (Euro)
    3:  GBP-USD (British Pound)
    4:  USD-JPY (US Dollar to Japanese Yen)
    5:  XAU-USD (Gold)  <-- FOR BERKAHKARYA
    6:  HG-USD (Copper)
    7:  CL-USD (Crude Oil)
    8:  XAG-USD (Silver)
    9:  SOL-USD (Solana)
    10: SPX-USD (S&P 500 Index)
    11: DJI-USD (Dow Jones Industrial Average)
    12: NDX-USD (NASDAQ-100 Index)
    13: NIK-JPY (Nikkei 225 Index)
    14: FTSE-GBP (FTSE 100 Index)
    15: DAX-EUR (DAX Index)
    16: USD-CAD (US Dollar to Canadian Dollar)
    17: USD-MXN (US Dollar to Mexican Peso)
    18: NVDA-USD (NVIDIA Stock)
    19: GOOG-USD (Alphabet/Google Stock)
    20: AMZN-USD (Amazon Stock)
    21: META-USD (Meta/Facebook Stock)
    22: TSLA-USD (Tesla Stock)
    23: AAPL-USD (Apple Stock)
    24: MSFT-USD (Microsoft Stock)
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
import logging
import asyncio
import yfinance as yf

from ..base import BrokerConnector, BrokerType, OHLCV, Order, Position, AccountInfo

logger = logging.getLogger(__name__)


class OstiumConnector(BrokerConnector):
    """Ostium broker connector using Python SDK."""

    # Symbol to pair_id mapping
    SYMBOL_TO_PAIR_ID = {
        "BTC-USD": 0, "XAU-USD": 5, "ETH-USD": 1,
        "EUR-USD": 2, "GBP-USD": 3, "USD-JPY": 4,
        "XAG-USD": 8, "SOL-USD": 9, "SPX-USD": 10,
        "NDX-USD": 12, "NIK-JPY": 13, "NVDA-USD": 18,
        "GOOG-USD": 19, "AAPL-USD": 23, "TSLA-USD": 22,
    }

    # YFinance symbol mapping (for OHLCV data)
    SYMBOL_TO_YFINANCE = {
        "XAU-USD": "GC=F",  # Gold Futures
        "BTC-USD": "BTC-USD",
        "ETH-USD": "ETH-USD",
        "EUR-USD": "EURUSD=X",
        "GBP-USD": "GBPUSD=X",
        "USD-JPY": "JPY=X",
        "XAG-USD": "SI=F",  # Silver Futures
        "SOL-USD": "SOL-USD",
        "SPX-USD": "^GSPC",
        "NDX-USD": "^NDX",
        "NVDA-USD": "NVDA",
        "GOOG-USD": "GOOGL",
        "AAPL-USD": "AAPL",
        "TSLA-USD": "TSLA",
    }

    def __init__(self):
        super().__init__(BrokerType.OSTIUM)
        self._client = None
        self._private_key = None
        self._rpc_url = None
        self._wallet_address = None
        self._is_testnet = False

    def _import_ostium(self):
        """Lazy import of Ostium library."""
        if self._client is None:
            try:
                from ostium_python_sdk import OstiumSDK, NetworkConfig
                self._OstiumSDK = OstiumSDK
                self._NetworkConfig = NetworkConfig
                logger.info("Ostium SDK imported successfully")
            except ImportError as e:
                logger.error(
                    "Ostium SDK not installed. Install with: pip install ostium-python-sdk"
                )
                raise ImportError("Ostium SDK not installed") from e
        return self._OstiumSDK, self._NetworkConfig

    def connect(self, **kwargs) -> bool:
        """Connect to Ostium blockchain.

        Args:
            private_key: EVM private key for signing transactions
            rpc_url: RPC URL for Arbitrum (mainnet or testnet)
            testnet: Boolean, True for testnet, False for mainnet
        """
        OstiumSDK, NetworkConfig = self._import_ostium()

        try:
            private_key = kwargs.get("private_key")
            rpc_url = kwargs.get("rpc_url")
            is_testnet = kwargs.get("testnet", True)

            if not private_key:
                logger.error("Missing required credential: private_key")
                return False

            if not rpc_url:
                logger.error("Missing required credential: rpc_url")
                return False

            self._private_key = private_key
            self._rpc_url = rpc_url
            self._is_testnet = is_testnet

            # Create network config
            if is_testnet:
                config = NetworkConfig.testnet()
                logger.info("Using Ostium TESTNET (Arbitrum Sepolia)")
            else:
                config = NetworkConfig.mainnet()
                logger.info("Using Ostium MAINNET (Arbitrum)")

            # Create Ostium client
            self._client = OstiumSDK(config, private_key, rpc_url, verbose=False)

            # Derive wallet address from private key
            from eth_account import Account
            account = Account.from_key(private_key)
            self._wallet_address = account.address

            self.connected = True
            logger.info(f"Connected to Ostium. Wallet: {self._wallet_address[:8]}...")
            return True

        except Exception as e:
            logger.error(f"Ostium connection failed: {e}")
            self.connected = False
            return False

    def disconnect(self) -> bool:
        """Disconnect from Ostium."""
        try:
            self._client = None
            self._private_key = None
            self._wallet_address = None
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
        """Fetch OHLCV data from yfinance (Ostium doesn't provide historical data).

        NOTE: Ostium provides price feeds for trading but not historical OHLCV data.
        We use yfinance as fallback for backtesting and analysis.
        """
        try:
            # Map Ostium symbol to yfinance symbol
            yf_symbol = self.SYMBOL_TO_YFINANCE.get(symbol, symbol)

            # Map timeframe string to yfinance interval
            timeframe_map = {
                "1m": "1m", "5m": "5m", "15m": "15m",
                "30m": "30m", "1h": "1h", "4h": "1h",
                "1d": "1d", "1w": "1w"
            }
            interval = timeframe_map.get(timeframe, "1h")

            # Set period based on count
            period_map = {
                100: "5d", 500: "1mo", 1000: "2mo",
                2000: "3mo", 5000: "6mo", None: "1y"
            }
            period = period_map.get(count, "2mo")

            # Fetch data
            ticker = yf.Ticker(yf_symbol)
            df = ticker.history(period=period, interval=interval)

            if df is None or df.empty:
                logger.warning(f"No data found for {yf_symbol}")
                return []

            # Convert to OHLCV list
            ohlcv_list = []
            for idx, row in df.iterrows():
                ohlcv = OHLCV(
                    timestamp=datetime.fromtimestamp(idx.timestamp()),
                    open=float(row['Open']),
                    high=float(row['High']),
                    low=float(row['Low']),
                    close=float(row['Close']),
                    volume=float(row['Volume']) if 'Volume' in row else 0.0,
                )
                ohlcv_list.append(ohlcv)

            # Return last 'count' candles if specified
            if count and len(ohlcv_list) > count:
                ohlcv_list = ohlcv_list[-count:]

            logger.info(f"Fetched {len(ohlcv_list)} candles for {yf_symbol} ({interval})")
            return ohlcv_list

        except Exception as e:
            logger.error(f"Failed to fetch OHLCV: {e}")
            return []

    def _run_async(self, coro):
        """Helper to run async functions in sync context."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)

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
        """Place a trading order on Ostium.

        Args:
            symbol: Trading pair (e.g., "XAU-USD")
            order_type: Order type - "BUY", "SELL", "BUY_STOP", "SELL_STOP", "BUY_LIMIT", "SELL_LIMIT"
            volume: Collateral amount in USDC
            price: Entry price (required for LIMIT/STOP orders)
            sl: Stop loss price
            tp: Take profit price
            **kwargs: Additional params like leverage, direction, asset_type
        """
        try:
            if not self.is_connected():
                logger.error("Not connected to Ostium")
                return None

            # Get pair_id
            pair_id = self.SYMBOL_TO_PAIR_ID.get(symbol)
            if pair_id is None:
                logger.error(f"Unknown symbol: {symbol}")
                return None

            # Map order_type to Ostium format
            order_type_upper = order_type.upper()
            if "BUY" in order_type_upper:
                direction = True  # Long
            elif "SELL" in order_type_upper:
                direction = False  # Short
            else:
                logger.error(f"Unknown order type: {order_type}")
                return None

            # Determine order type
            if "STOP" in order_type_upper:
                ostium_order_type = "STOP"
            elif "LIMIT" in order_type_upper:
                ostium_order_type = "LIMIT"
            else:
                ostium_order_type = "MARKET"

            # Build trade parameters
            leverage = kwargs.get("leverage", 10)

            trade_params = {
                'collateral': volume,
                'leverage': leverage,
                'asset_type': pair_id,
                'direction': direction,
                'order_type': ostium_order_type,
            }

            # Get current price if MARKET order
            if ostium_order_type == "MARKET" or price is None:
                # Map symbol to price query format
                if symbol == "XAU-USD":
                    base, quote = "XAU", "USD"
                elif symbol == "BTC-USD":
                    base, quote = "BTC", "USD"
                elif symbol == "ETH-USD":
                    base, quote = "ETH", "USD"
                else:
                    # Default: extract base and quote from symbol
                    parts = symbol.split("-")
                    base, quote = parts[0], parts[1]

                price_data = self._run_async(self._client.price.get_price(base, quote))
                price = price_data[0] if price_data else None

                if price is None:
                    logger.error(f"Failed to get price for {symbol}")
                    return None

            # Place order
            receipt = self._run_async(
                self._client.ostium.perform_trade(trade_params, at_price=price)
            )

            if receipt:
                # Get the trade index (it's the new trade)
                trades = self._run_async(
                    self._client.subgraph.get_open_trades(self._wallet_address)
                )
                if trades:
                    trade_index = trades[-1].get('index', 0)
                else:
                    trade_index = 0

                order = Order(
                    ticket=trade_index,
                    symbol=symbol,
                    order_type=order_type_upper,
                    volume=volume,
                    price=price,
                    sl=sl,
                    tp=tp,
                    time_setup=datetime.now(),
                )
                logger.info(f"Order placed: {order_type_upper} {symbol} @ {price} (ticket: {trade_index})")
                return order
            else:
                logger.error(f"Order failed")
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

            # Get all open trades
            trades = self._run_async(
                self._client.subgraph.get_open_trades(self._wallet_address)
            )

            position_list = []
            for trade in trades:
                # Map pair_id back to symbol
                pair_id = trade.get('pair', {}).get('id', 0)
                # Reverse lookup symbol from pair_id
                symbol_map = {v: k for k, v in self.SYMBOL_TO_PAIR_ID.items()}
                trade_symbol = symbol_map.get(pair_id, "UNKNOWN")

                # Filter by symbol if specified
                if symbol is not None and trade_symbol != symbol:
                    continue

                # Get current metrics (unrealized PnL, etc.)
                metrics = self._run_async(
                    self._client.get_open_trade_metrics(pair_id, trade.get('index', 0))
                )

                position = Position(
                    ticket=trade.get('index', 0),
                    symbol=trade_symbol,
                    order_type="BUY" if trade.get('is_long', True) else "SELL",
                    volume=float(trade.get('collateral', 0)),
                    open_price=float(trade.get('entry_price', 0)),
                    current_price=float(metrics.get('mark_price', trade.get('entry_price', 0))) if metrics else float(trade.get('entry_price', 0)),
                    sl=float(metrics.get('stop_loss', 0)) if metrics and metrics.get('stop_loss') else None,
                    tp=float(metrics.get('take_profit', 0)) if metrics and metrics.get('take_profit') else None,
                    profit=float(metrics.get('unrealized_pnl', 0)) if metrics else 0.0,
                    time_open=datetime.fromtimestamp(trade.get('timestamp', 0)),
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

            # Get balance (pass wallet address)
            balance = self._run_async(
                self._client.balance.get_balance(self._wallet_address)
            )

            info = AccountInfo(
                login=abs(hash(str(self._wallet_address))),  # Hash address as login
                balance=float(balance.get('usdc_balance', 0)),
                equity=float(balance.get('usdc_balance', 0)),  # Perpetual uses balance
                margin=float(balance.get('usdc_balance', 0)),  # Ostium has different margin model
                free_margin=float(balance.get('usdc_balance', 0)),
                margin_level=0,  # Ostium uses different margin model
                currency="USDC",
                leverage=1,  # Leverage is per-trade, not per-account
                server="Arbitrum Sepolia" if self._is_testnet else "Arbitrum Mainnet",
                name="Ostium Perpetual",
            )

            logger.info(f"Account info: Balance={info.balance} USDC")
            return info

        except Exception as e:
            logger.error(f"Failed to get account info: {e}")
            return None

    def get_account_info(self) -> Optional[AccountInfo]:
        """Get account information from Ostium."""
        try:
            if not self.is_connected():
                logger.error("Not connected to Ostium")
                return None

            # Get balance (SDK returns tuple: (usdc_balance, native_balance))
            usdc_balance, native_balance = self._client.balance.get_balance(self._wallet_address)



            info = AccountInfo(
                login=abs(hash(str(self._wallet_address))),  # Hash address as login
                balance=float(usdc_balance),
                equity=float(usdc_balance),  # Perpetual uses balance
                margin=float(usdc_balance),  # Ostium has different margin model
                free_margin=float(usdc_balance),
                margin_level=0,  # Ostium has different margin model
                currency="USDC",
                leverage=1,  # Leverage is per-trade, not per-account
                server="Arbitrum Sepolia" if self._is_testnet else "Arbitrum Mainnet",
                name="Ostium Perpetual",
            )

            logger.info(f"Account info: Balance={info.balance} USDC")
            return info

        except Exception as e:
            logger.error(f"Failed to get account info: {e}")
            return None

    def close_position(self, ticket: int, symbol: Optional[str] = None) -> bool:
        """Close a position by ticket ID (trade_index)."""
        try:
            if not self.is_connected():
                logger.error("Not connected to Ostium")
                return False

            # Get open positions to find pair_id
            positions = self.get_positions()
            pair_id = None
            for pos in positions:
                if pos.ticket == ticket:
                    pair_id = self.SYMBOL_TO_PAIR_ID.get(pos.symbol)
                    break

            if pair_id is None:
                logger.error(f"Position {ticket} not found")
                return False

            # Close trade
            receipt = self._run_async(
                self._client.ostium.close_trade(pair_id, ticket)
            )

            if receipt:
                logger.info(f"Position closed: {ticket}")
                return True
            else:
                logger.error(f"Failed to close position")
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

            # Get open positions to find pair_id
            positions = self.get_positions()
            pair_id = None
            for pos in positions:
                if pos.ticket == ticket:
                    pair_id = self.SYMBOL_TO_PAIR_ID.get(pos.symbol)
                    break

            if pair_id is None:
                logger.error(f"Position {ticket} not found")
                return False

            # Update TP
            if tp is not None:
                receipt_tp = self._run_async(
                    self._client.ostium.update_tp(pair_id, ticket, tp)
                )
                if not receipt_tp:
                    logger.error(f"Failed to update TP for position {ticket}")
                    return False

            # Update SL
            if sl is not None:
                receipt_sl = self._run_async(
                    self._client.ostium.update_sl(pair_id, ticket, sl)
                )
                if not receipt_sl:
                    logger.error(f"Failed to update SL for position {ticket}")
                    return False

            logger.info(f"Position modified: {ticket}")
            return True

        except Exception as e:
            logger.error(f"Failed to modify position: {e}")
            return False

    def get_available_symbols(self) -> List[str]:
        """Get available trading symbols from Ostium."""
        try:
            if not self.is_connected():
                logger.error("Not connected to Ostium")
                return []

            # Get all pairs from Ostium
            pairs = self._run_async(self._client.subgraph.get_pairs())

            symbols = []
            for pair in pairs:
                pair_id = pair.get('id', 0)
                # Map pair_id to symbol
                symbol_map = {v: k for k, v in self.SYMBOL_TO_PAIR_ID.items()}
                symbol = symbol_map.get(pair_id, f"UNKNOWN-{pair_id}")
                symbols.append(symbol)

            return symbols

        except Exception as e:
            logger.error(f"Failed to get symbols: {e}")
            return []

    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol."""
        try:
            if not self.is_connected():
                logger.error("Not connected to Ostium")
                return None

            # Map symbol to price query format
            if symbol == "XAU-USD":
                base, quote = "XAU", "USD"
            elif symbol == "BTC-USD":
                base, quote = "BTC", "USD"
            elif symbol == "ETH-USD":
                base, quote = "ETH", "USD"
            else:
                # Default: extract base and quote from symbol
                parts = symbol.split("-")
                base, quote = parts[0], parts[1]

            price_data = self._run_async(self._client.price.get_price(base, quote))
            if price_data:
                return float(price_data[0])
            else:
                return None

        except Exception as e:
            logger.error(f"Failed to get price: {e}")
            return None
