"""
Trading Pipeline
Signal → Guardrail Check → Paper Trade workflow
"""

import sys
import os

sys.path.insert(0, "/home/openclaw/.openclaw/workspace")

from skills.trading.guardrails import TradingGuardrails
from skills.revenue_dashboard.dashboard import RevenueDashboard


class TradingPipeline:
    """End-to-end trading pipeline"""

    def __init__(self, paper_mode: bool = True):
        self.paper_mode = paper_mode
        self.guardrails = TradingGuardrails()
        self.dashboard = RevenueDashboard()

    def run(self, signal: dict) -> dict:
        """
        Run trading pipeline

        Args:
            signal: {
                "symbol": "EURUSD",
                "direction": "buy" | "sell",
                "entry": 1.0850,
                "stop_loss": 1.0830,
                "take_profit": 1.0900,
                "size": 0.1
            }
        """
        # Step 1: Check guardrails
        can_trade = self.guardrails.can_trade()
        if not can_trade["allowed"]:
            return {
                "success": False,
                "step": "guardrails",
                "message": f"Cannot trade: {can_trade['reasons']}",
            }

        # Step 2: Risk management check
        risk_check = self._check_risk(signal)
        if not risk_check["valid"]:
            return {
                "success": False,
                "step": "risk_check",
                "message": f"Risk validation failed: {risk_check['reason']}",
            }

        # Step 3: Execute trade (paper or live)
        if self.paper_mode:
            result = self._paper_trade(signal)
        else:
            result = self._live_trade(signal)

        # Step 4: Record result
        if result.get("success"):
            self.guardrails.record_trade(
                signal.get("direction"), result.get("pnl", 0), signal.get("size", 0.1)
            )

            # Record revenue
            if result.get("pnl", 0) > 0:
                self.dashboard.record_revenue(
                    "trading",
                    result.get("pnl", 0),
                    f"{signal.get('symbol')} {signal.get('direction')}",
                    "USD",
                )

        return {
            "success": result.get("success", False),
            "trade_result": result,
            "guardrails_state": self.guardrails.state,
            "step": "complete",
        }

    def _check_risk(self, signal: dict) -> dict:
        """Check risk management constraints"""
        # Check position size
        max_size = 1.0  # 1% of account
        if signal.get("size", 0) > max_size:
            return {
                "valid": False,
                "reason": f"Position size {signal['size']} exceeds max {max_size}%",
            }

        # Check stop loss exists
        if not signal.get("stop_loss"):
            return {"valid": False, "reason": "Stop loss required"}

        return {"valid": True}

    def _paper_trade(self, signal: dict) -> dict:
        """Execute paper trade"""
        return {
            "success": True,
            "mode": "paper",
            "trade_id": f"paper-{signal['symbol']}-{signal['direction']}-001",
            "entry": signal.get("entry"),
            "stop_loss": signal.get("stop_loss"),
            "take_profit": signal.get("take_profit"),
            "size": signal.get("size"),
            "pnl": 0.0,  # Would be calculated when trade closes
            "opened_at": "2026-02-28T12:00:00Z",
        }

    def _live_trade(self, signal: dict) -> dict:
        """Execute live trade (requires credentials)"""
        return {
            "success": False,
            "mode": "live",
            "error": "Live trading not implemented - requires cTrader credentials",
        }

    def close_trade(self, trade_id: str, exit_price: float) -> dict:
        """Close a trade and calculate P&L"""
        # Simulated close
        pnl = 10.0  # Would calculate based on entry/exit

        return {
            "success": True,
            "trade_id": trade_id,
            "exit_price": exit_price,
            "pnl": pnl,
            "closed_at": "2026-02-28T12:30:00Z",
        }


if __name__ == "__main__":
    pipeline = TradingPipeline(paper_mode=True)

    # Test trade
    result = pipeline.run(
        {
            "symbol": "EURUSD",
            "direction": "buy",
            "entry": 1.0850,
            "stop_loss": 1.0830,
            "take_profit": 1.0900,
            "size": 0.1,
        }
    )

    print(f"Trading result: {result['success']}")
    print(f"Trade ID: {result.get('trade_result', {}).get('trade_id')}")
