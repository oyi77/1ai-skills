"""
Trading Guardrails
Circuit breaker, kill switch, and risk management
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class TradingGuardrails:
    """Trading safety guardrails"""

    def __init__(self, config_path: str = None):
        # Default limits
        self.config = {
            "max_consecutive_losses": 3,
            "daily_loss_limit": 50.0,  # USD
            "max_drawdown_pct": 5.0,  # Percentage
            "max_position_size_pct": 1.0,  # % of account
            "kill_switch_enabled": True,
            "emergency_stop_pin": "1234",  # Change this!
        }

        if config_path and os.path.exists(config_path):
            with open(config_path) as f:
                self.config.update(json.load(f))

        self.state_file = "/home/openclaw/.openclaw/workspace/data/trading_state.json"
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load trading state"""
        if os.path.exists(self.state_file):
            with open(self.state_file) as f:
                return json.load(f)

        return {
            "consecutive_losses": 0,
            "daily_pnl": 0.0,
            "total_pnl": 0.0,
            "positions": [],
            "circuit_breaker_triggered": False,
            "last_reset": datetime.now().isoformat(),
            "trades_today": 0,
        }

    def _save_state(self):
        """Save trading state"""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def can_trade(self) -> Dict:
        """Check if trading is allowed"""
        reasons = []
        allowed = True

        # Check circuit breaker
        if self.state.get("circuit_breaker_triggered"):
            reasons.append("Circuit breaker triggered")
            allowed = False

        # Check daily loss limit
        if self.state.get("daily_pnl", 0) <= -self.config["daily_loss_limit"]:
            reasons.append("Daily loss limit reached")
            allowed = False

        # Check consecutive losses
        if (
            self.state.get("consecutive_losses", 0)
            >= self.config["max_consecutive_losses"]
        ):
            reasons.append("Max consecutive losses reached")
            allowed = False

        return {"allowed": allowed, "reasons": reasons, "state": self.state}

    def record_trade(self, direction: str, pnl: float, position_size: float) -> Dict:
        """Record a trade and check limits"""
        # Update state
        self.state["trades_today"] += 1
        self.state["daily_pnl"] += pnl
        self.state["total_pnl"] += pnl

        if pnl < 0:
            self.state["consecutive_losses"] += 1
        else:
            self.state["consecutive_losses"] = 0

        # Check limits
        checks = {
            "circuit_breaker": self.state["consecutive_losses"]
            >= self.config["max_consecutive_losses"],
            "daily_loss": self.state["daily_pnl"] <= -self.config["daily_loss_limit"],
            "max_drawdown": False,  # Would need account balance to calculate
        }

        # Trigger circuit breaker if needed
        if checks["circuit_breaker"]:
            self.state["circuit_breaker_triggered"] = True

        self._save_state()

        return {
            "recorded": True,
            "new_state": self.state,
            "limits_triggered": checks,
            "can_continue": self.can_trade()["allowed"],
        }

    def reset_daily(self):
        """Reset daily counters"""
        self.state["daily_pnl"] = 0.0
        self.state["trades_today"] = 0
        self.state["consecutive_losses"] = 0
        self.state["last_reset"] = datetime.now().isoformat()
        self._save_state()

    def kill_switch(self, pin: str) -> Dict:
        """Emergency kill switch"""
        if pin != self.config["emergency_stop_pin"]:
            return {"success": False, "error": "Invalid PIN"}

        self.state["circuit_breaker_triggered"] = True
        self._save_state()

        return {
            "success": True,
            "message": "KILL SWITCH ACTIVATED - All trading halted",
            "state": self.state,
        }

    def reset_circuit_breaker(self, pin: str) -> Dict:
        """Reset circuit breaker (requires PIN)"""
        if pin != self.config["emergency_stop_pin"]:
            return {"success": False, "error": "Invalid PIN"}

        self.state["circuit_breaker_triggered"] = False
        self.state["consecutive_losses"] = 0
        self._save_state()

        return {"success": True, "message": "Circuit breaker reset"}


class RiskManager:
    """Position size calculator and risk controls"""

    def __init__(self, account_balance: float = 10000.0):
        self.account_balance = account_balance

    def calculate_position_size(
        self, risk_pct: float, stop_loss_pips: float, pip_value: float = 10.0
    ) -> float:
        """Calculate position size in lots"""
        risk_amount = self.account_balance * (risk_pct / 100)
        position_size = (risk_amount / stop_loss_pips) / pip_value
        return round(position_size, 2)

    def validate_position(self, position_size: float, account_pct: float) -> Dict:
        """Validate position size"""
        actual_pct = (position_size * 100) / self.account_balance

        return {
            "valid": actual_pct <= 1.0,
            "requested_pct": account_pct,
            "actual_pct": actual_pct,
            "max_allowed_pct": 1.0,
        }


if __name__ == "__main__":
    guardrails = TradingGuardrails()

    # Test can_trade
    result = guardrails.can_trade()
    print(f"Can trade: {result['allowed']}")
    print(f"Reasons: {result['reasons']}")

    # Test record trade
    trade_result = guardrails.record_trade("buy", -20.0, 0.1)
    print(f"Trade recorded: {trade_result['can_continue']}")
