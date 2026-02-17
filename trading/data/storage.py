"""
Data Storage Module

Handles persistent storage for OHLCV data and trade logs.
"""

import csv
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from ..brokers.base import OHLCV, Order, Position


class DataStorage:
    """Handles data persistence for trading data."""

    def __init__(self, base_path: str = "./trading_data"):
        self.base_path = Path(base_path)
        self.ohlcv_path = self.base_path / "ohlcv"
        self.trades_path = self.base_path / "trades"
        self._ensure_directories()

    def _ensure_directories(self):
        """Create directories if they don't exist."""
        self.ohlcv_path.mkdir(parents=True, exist_ok=True)
        self.trades_path.mkdir(parents=True, exist_ok=True)

    def _get_ohlcv_filename(self, symbol: str, timeframe: str) -> Path:
        """Get filename for OHLCV data."""
        return self.ohlcv_path / f"{symbol}_{timeframe}.csv"

    def save_ohlcv(
        self, symbol: str, timeframe: str, ohlcv_list: List[OHLCV], mode: str = "a"
    ):
        """Save OHLCV data to CSV."""
        filepath = self._get_ohlcv_filename(symbol, timeframe)

        file_exists = filepath.exists()

        with open(filepath, mode, newline="") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])

            for ohlcv in ohlcv_list:
                writer.writerow(
                    [
                        ohlcv.timestamp.isoformat(),
                        ohlcv.open,
                        ohlcv.high,
                        ohlcv.low,
                        ohlcv.close,
                        ohlcv.volume,
                    ]
                )

    def load_ohlcv(self, symbol: str, timeframe: str) -> List[OHLCV]:
        """Load OHLCV data from CSV."""
        filepath = self._get_ohlcv_filename(symbol, timeframe)

        if not filepath.exists():
            return []

        ohlcv_list = []

        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ohlcv_list.append(
                    OHLCV(
                        timestamp=datetime.fromisoformat(row["timestamp"]),
                        open=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                        volume=float(row["volume"]),
                    )
                )

        return ohlcv_list

    def save_trade(self, trade: Dict[str, Any], filename: str = "trades.json"):
        """Save a single trade to JSON."""
        filepath = self.trades_path / filename

        trades = self.load_trades(filename)
        trades.append(trade)

        with open(filepath, "w") as f:
            json.dump(trades, f, indent=2)

    def load_trades(self, filename: str = "trades.json") -> List[Dict[str, Any]]:
        """Load trades from JSON."""
        filepath = self.trades_path / filename

        if not filepath.exists():
            return []

        with open(filepath, "r") as f:
            return json.load(f)

    def export_trades(
        self,
        filename: str = "trades_export.csv",
        trades: Optional[List[Dict[str, Any]]] = None,
    ):
        """Export trades to CSV."""
        if trades is None:
            trades = self.load_trades()

        if not trades:
            return

        filepath = self.trades_path / filename

        # Get all unique keys from trades
        fieldnames = set()
        for trade in trades:
            fieldnames.update(trade.keys())
        fieldnames = sorted(fieldnames)

        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(trades)

    def get_latest_ohlcv(self, symbol: str, timeframe: str) -> Optional[OHLCV]:
        """Get the most recent OHLCV candle."""
        ohlcv_list = self.load_ohlcv(symbol, timeframe)
        return ohlcv_list[-1] if ohlcv_list else None

    def clear_ohlcv(self, symbol: str, timeframe: str):
        """Clear OHLCV data for a symbol/timeframe."""
        filepath = self._get_ohlcv_filename(symbol, timeframe)
        if filepath.exists():
            filepath.unlink()

    def clear_trades(self, filename: str = "trades.json"):
        """Clear all trades."""
        filepath = self.trades_path / filename
        if filepath.exists():
            filepath.unlink()
