"""
Real Trade Engine

Real trading with broker integration and guardrails.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional

from ..brokers.base import BrokerConnector
from ..strategy.base import TradingSignal
from ..risk.manager import RiskManager


@dataclass
class TradeRequest:
    """Trade request with all parameters."""

    symbol: str
    side: str  # BUY or SELL
    volume: float
    entry_price: float
    sl: float
    tp: float
    spread: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "side": self.side,
            "volume": self.volume,
            "entry_price": self.entry_price,
            "sl": self.sl,
            "tp": self.tp,
            "spread": self.spread,
        }


class RealTradeEngine:
    """Real trading engine with guardrails."""

    def __init__(
        self,
        broker: BrokerConnector,
        risk_manager: RiskManager,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.broker = broker
        self.risk_manager = risk_manager
        self.config = config or {}

        # Guardrail settings
        self.max_spread = self.config.get("max_spread_points", 30.0)
        self.max_daily_trades = self.config.get("max_daily_trades", 1)
        self.one_trade_per_day = self.config.get("one_trade_per_day", True)

        # State
        self.daily_trade_count = 0
        self.last_trade_date = None
        self.armed = False

    def arm(self) -> bool:
        """Arm the trading system for real trading."""
        # Check broker connection
        if not self.broker.is_connected():
            if not self.broker.connect():
                return False

        self.armed = True
        return True

    def disarm(self):
        """Disarm the trading system."""
        self.armed = False

    def check_guardrails(
        self,
        signal: TradingSignal,
        current_spread: float = 0.0,
        account_balance: float = 0.0,
        current_drawdown: float = 0.0,
    ) -> tuple:
        """
        Check all guardrails before trade execution.

        Returns:
            (is_valid, reason)
        """
        # Check if armed
        if not self.armed:
            return (False, "System not armed")

        # Check broker connection
        if not self.broker.is_connected():
            return (False, "Broker not connected")

        # Check daily trade limit
        today = datetime.now().date()
        if self.last_trade_date != today:
            self.daily_trade_count = 0
            self.last_trade_date = today

        if self.one_trade_per_day and self.daily_trade_count >= self.max_daily_trades:
            return (False, f"Daily trade limit reached ({self.daily_trade_count})")

        # Check spread
        if current_spread > self.max_spread:
            return (False, f"Spread {current_spread} exceeds max {self.max_spread}")

        # Check drawdown (if balance provided)
        if current_drawdown > 10.0:  # 10% max drawdown
            return (False, f"Drawdown {current_drawdown}% exceeds 10%")

        return (True, "OK")

    def generate_guardrail_summary(
        self, signal: TradingSignal, spread: float, account_balance: float
    ) -> str:
        """Generate pre-trade guardrail summary."""
        return f"""
=== PRE-TRADE GUARDRAIL SUMMARY ===
Symbol: {signal.symbol}
Entry Price: {signal.buy_stop if signal.triggered_side == "BUY" else signal.sell_stop}
Side: {signal.triggered_side or "PENDING"}

Risk Parameters:
  SL: {signal.buy_sl if signal.triggered_side == "BUY" else signal.sell_sl}
  TP: {signal.buy_tp if signal.triggered_side == "BUY" else signal.sell_tp}
  R: {signal.r_points} points
  RR: {self.risk_manager.config.rr_ratio}

Guardrails:
  Spread: {spread} (max: {self.max_spread})
  Daily Trades: {self.daily_trade_count}/{self.max_daily_trades}
  Account Balance: ${account_balance:.2f}

Status: {"READY" if self.armed else "NOT ARMED"}
=========================================
"""

    def execute_trade(self, request: TradeRequest) -> Optional[Dict[str, Any]]:
        """Execute a trade with the broker."""
        if not self.armed:
            return {"success": False, "error": "System not armed"}

        # Determine order type
        order_type = (
            f"{request.side}_MARKET"
            if request.entry_price is None
            else f"{request.side}_STOP"
        )

        # Place order through broker
        order = self.broker.place_order(
            symbol=request.symbol,
            order_type=order_type,
            volume=request.volume,
            price=request.entry_price,
            sl=request.sl,
            tp=request.tp,
        )

        if order is None:
            return {"success": False, "error": "Order placement failed"}

        # Update daily count
        self.daily_trade_count += 1

        return {
            "success": True,
            "order": order.to_dict(),
            "timestamp": datetime.now().isoformat(),
        }

    def generate_execution_plan(
        self, signal: TradingSignal, side: str, volume: float
    ) -> str:
        """Generate execution plan for manual trading (when API unavailable)."""
        entry = signal.buy_stop if side == "BUY" else signal.sell_stop
        sl = signal.buy_sl if side == "BUY" else signal.sell_sl
        tp = signal.buy_tp if side == "BUY" else signal.sell_tp

        return f"""
=== EXECUTION PLAN (Manual Trading) ===

Symbol: {signal.symbol}
Type: {side}
Volume: {volume} lots

Entry: {entry}
Stop Loss: {sl}
Take Profit: {tp}

Instructions:
1. Open {signal.symbol} chart on MT5
2. Set pending {side} STOP at {entry}
3. Set SL at {sl}
4. Set TP at {tp}
5. Wait for trigger

Note: Cancel opposite pending order when one triggers.
Note: Cancel all pending orders at session end ({self.config.get("session_end", "15:00")})
"""

    def get_status(self) -> Dict[str, Any]:
        """Get current trading status."""
        return {
            "armed": self.armed,
            "connected": self.broker.is_connected(),
            "daily_trades": self.daily_trade_count,
            "last_trade_date": self.last_trade_date.isoformat()
            if self.last_trade_date
            else None,
        }
