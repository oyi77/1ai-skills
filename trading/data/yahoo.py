"""
Data Provider - Yahoo Finance

Fetches OHLCV data from Yahoo Finance.
"""

from datetime import datetime
from typing import List, Optional
import yfinance as yf

from ..brokers.base import OHLCV
from .symbols import get_yahoo_ticker, get_symbol_config


class YahooFinanceProvider:
    """Yahoo Finance data provider."""

    # Symbol mapping for Yahoo Finance (fallback for symbols not in symbols.py)
    SYMBOL_MAP = {
        "XAUUSD": "GC=F",  # Gold Futures
        "XAUUSD.D": "GC=F",
        "XAUEUR": "XAUEUR=X",
        "XAUGBP": "XAUGBP=X",
        "CL=F": "CL=F",  # Crude Oil
        "ES=F": "ES=F",  # S&P 500
        "NQU=F": "NQ=F",  # Nasdaq
    }

    def __init__(self):
        self.timezone = "UTC"

    def get_symbol(self, symbol: str) -> str:
        """Map symbol to Yahoo Finance ticker."""
        # First try symbol configs
        yahoo_ticker = get_yahoo_ticker(symbol)
        if yahoo_ticker != symbol:
            return yahoo_ticker
        # Fall back to local SYMBOL_MAP
        return self.SYMBOL_MAP.get(symbol, symbol)

    def get_symbol_config(self, symbol: str):
        """Get symbol configuration if available."""
        return get_symbol_config(symbol)

    def get_ohlcv(
        self,
        symbol: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        period: Optional[str] = None,  # e.g., "30d", "1y"
        interval: str = "1h",
    ) -> List[OHLCV]:
        """
        Fetch OHLCV data from Yahoo Finance.

        Args:
            symbol: Trading symbol (e.g., "XAUUSD")
            start: Start date
            end: End date
            period: Period string (e.g., "30d", "1y") - alternative to start/end
            interval: Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo)

        Returns:
            List of OHLCV candles
        """
        yahoo_symbol = self.get_symbol(symbol)

        ticker = yf.Ticker(yahoo_symbol)

        if period:
            df = ticker.history(period=period, interval=interval)
        else:
            df = ticker.history(start=start, end=end, interval=interval)

        if df.empty:
            return []

        candles = []
        for idx, row in df.iterrows():
            # Handle timezone
            timestamp = idx
            if timestamp.tzinfo is None:
                timestamp = timestamp.tz_localize("UTC")
            else:
                timestamp = timestamp.tz_convert("UTC")

            candle = OHLCV(
                timestamp=timestamp,
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=float(row["Volume"]) if "Volume" in row else 0.0,
            )
            candles.append(candle)

        return candles


# Singleton instance
_provider = None


def get_provider() -> YahooFinanceProvider:
    """Get Yahoo Finance provider instance."""
    global _provider
    if _provider is None:
        _provider = YahooFinanceProvider()
    return _provider
