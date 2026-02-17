"""
Paper Trade Engine

Virtual trading with real-time simulation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

from ..brokers.base import OHLCV
from ..strategy.base import TradingSignal


@dataclass
class VirtualPosition:
    """Virtual trading position."""

    id: str
    symbol: str
    side: str  # BUY or SELL
    entry_price: float
    volume: float
    sl: float
    tp: float
    open_time: datetime
    status: str = "open"  # open, closed

    @property
    def is_profitable(self, current_price: float) -> bool:
        if self.side == "BUY":
            return current_price > self.entry_price
        return current_price < self.entry_price


@dataclass
class VirtualTrade:
    """Completed virtual trade."""

    id: str
    symbol: str
    side: str
    entry_price: float
    exit_price: float
    volume: float
    pnl: float
    open_time: datetime
    close_time: datetime
    result: str  # WIN, LOSS
    reason: str


class PaperTradeEngine:
    """Paper trading engine for strategy simulation."""

    def __init__(self, initial_balance: float = 10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions: List[VirtualPosition] = []
        self.trades: List[VirtualTrade] = []
        self.pending_orders: List[TradingSignal] = []
        self.daily_briefing: Dict[str, Any] = {}

    def place_pending(self, signal: TradingSignal):
        """Place pending order."""
        self.pending_orders.append(signal)

    def check_trigger(self, current_price: float) -> Optional[str]:
        """Check if any pending order is triggered."""
        for signal in self.pending_orders:
            if signal.status != "pending":
                continue

            # Check buy trigger
            if current_price >= signal.buy_stop:
                self._open_position(signal, "BUY", signal.buy_stop)
                return "BUY"

            # Check sell trigger
            if current_price <= signal.sell_stop:
                self._open_position(signal, "SELL", signal.sell_stop)
                return "SELL"

        return None

    def _open_position(self, signal: TradingSignal, side: str, entry_price: float):
        """Open a virtual position."""
        pos = VirtualPosition(
            id=f"pos_{len(self.positions)}_{datetime.now().timestamp()}",
            symbol=signal.symbol,
            side=side,
            entry_price=entry_price,
            volume=0.01,  # Default lot
            sl=signal.buy_sl if side == "BUY" else signal.sell_sl,
            tp=signal.buy_tp if side == "BUY" else signal.sell_tp,
            open_time=datetime.now(),
        )

        self.positions.append(pos)

        # Cancel opposite pending
        self._cancel_opposite(signal, side)

        # Update status
        signal.status = "triggered"
        signal.triggered_side = side

    def _cancel_opposite(self, signal: TradingSignal, triggered_side: str):
        """Cancel opposite pending orders."""
        opposite = "SELL" if triggered_side == "BUY" else "BUY"

        self.pending_orders = [
            o
            for o in self.pending_orders
            if o.status == "pending"
            or (o.status == "triggered" and o.triggered_side != opposite)
        ]

    def update(self, current_price: float, current_time: datetime):
        """Update positions with current price."""
        for pos in self.positions:
            if pos.status != "open":
                continue

            # Check SL/TP
            if pos.side == "BUY":
                if current_price <= pos.sl:
                    self._close_position(pos, pos.sl, "SL hit")
                elif current_price >= pos.tp:
                    self._close_position(pos, pos.tp, "TP hit")
            else:  # SELL
                if current_price >= pos.sl:
                    self._close_position(pos, pos.sl, "SL hit")
                elif current_price <= pos.tp:
                    self._close_position(pos, pos.tp, "TP hit")

    def _close_position(self, pos: VirtualPosition, exit_price: float, reason: str):
        """Close a virtual position."""
        # Calculate PnL
        if pos.side == "BUY":
            pnl = (exit_price - pos.entry_price) * 100
        else:
            pnl = (pos.entry_price - exit_price) * 100

        result = "WIN" if pnl > 0 else "LOSS"

        trade = VirtualTrade(
            id=pos.id,
            symbol=pos.symbol,
            side=pos.side,
            entry_price=pos.entry_price,
            exit_price=exit_price,
            volume=pos.volume,
            pnl=pnl,
            open_time=pos.open_time,
            close_time=datetime.now(),
            result=result,
            reason=reason,
        )

        self.trades.append(trade)
        self.balance += pnl
        pos.status = "closed"

    def cancel_all_pending(self):
        """Cancel all pending orders."""
        for signal in self.pending_orders:
            if signal.status == "pending":
                signal.status = "cancelled"
        self.pending_orders = []

    def get_daily_briefing(self) -> Dict[str, Any]:
        """Generate daily briefing."""
        if not self.pending_orders:
            self.daily_briefing = {
                "time": datetime.now().isoformat(),
                "balance": self.balance,
                "open_positions": len(
                    [p for p in self.positions if p.status == "open"]
                ),
                "pending_orders": 0,
                "status": "no signals",
            }
        else:
            signal = self.pending_orders[0]
            self.daily_briefing = {
                "time": datetime.now().isoformat(),
                "balance": self.balance,
                "open_positions": len(
                    [p for p in self.positions if p.status == "open"]
                ),
                "pending_orders": len(self.pending_orders),
                "status": "pending placed",
                "hh": signal.hh,
                "ll": signal.ll,
                "r": signal.r_points,
                "buy_stop": signal.buy_stop,
                "buy_sl": signal.buy_sl,
                "buy_tp": signal.buy_tp,
                "sell_stop": signal.sell_stop,
                "sell_sl": signal.sell_sl,
                "sell_tp": signal.sell_tp,
            }

        return self.daily_briefing

    def save_state(self, filename: str = "paper_trade_state.json"):
        """Save paper trading state."""
        state = {
            "balance": self.balance,
            "positions": [
                {
                    "id": p.id,
                    "symbol": p.symbol,
                    "side": p.side,
                    "entry_price": p.entry_price,
                    "volume": p.volume,
                    "sl": p.sl,
                    "tp": p.tp,
                    "open_time": p.open_time.isoformat(),
                    "status": p.status,
                }
                for p in self.positions
            ],
            "trades": [
                {
                    "id": t.id,
                    "symbol": t.symbol,
                    "side": t.side,
                    "entry_price": t.entry_price,
                    "exit_price": t.exit_price,
                    "volume": t.volume,
                    "pnl": t.pnl,
                    "open_time": t.open_time.isoformat(),
                    "close_time": t.close_time.isoformat(),
                    "result": t.result,
                    "reason": t.reason,
                }
                for t in self.trades
            ],
        }

        with open(filename, "w") as f:
            json.dump(state, f, indent=2)

        return filename

    def load_state(self, filename: str = "paper_trade_state.json"):
        """Load paper trading state."""
        with open(filename, "r") as f:
            state = json.load(f)

        self.balance = state["balance"]

        self.positions = []
        for p in state["positions"]:
            pos = VirtualPosition(
                id=p["id"],
                symbol=p["symbol"],
                side=p["side"],
                entry_price=p["entry_price"],
                volume=p["volume"],
                sl=p["sl"],
                tp=p["tp"],
                open_time=datetime.fromisoformat(p["open_time"]),
                status=p["status"],
            )
            self.positions.append(pos)

        self.trades = []
        for t in state["trades"]:
            trade = VirtualTrade(
                id=t["id"],
                symbol=t["symbol"],
                side=t["side"],
                entry_price=t["entry_price"],
                exit_price=t["exit_price"],
                volume=t["volume"],
                pnl=t["pnl"],
                open_time=datetime.fromisoformat(t["open_time"]),
                close_time=datetime.fromisoformat(t["close_time"]),
                result=t["result"],
                reason=t["reason"],
            )
            self.trades.append(trade)
