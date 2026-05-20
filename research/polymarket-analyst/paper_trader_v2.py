#!/usr/bin/env python3
"""
Polymarket Paper Trader - Full Implementation
Simulate trading with virtual $100 balance
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class PaperTrader:
    def __init__(self, initial_balance: float = 100.0):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.positions: List[Dict] = []
        self.trade_history: List[Dict] = []
        self.decision_log: List[Dict] = []
        self.data_file = Path(__file__).parent / "paper_trading_data.json"
        self.load_data()

    def load_data(self):
        """Load existing trading data"""
        if self.data_file.exists():
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.balance = data.get("balance", self.initial_balance)
                self.positions = data.get("positions", [])
                self.trade_history = data.get("trade_history", [])
                self.decision_log = data.get("decision_log", [])

    def save_data(self):
        """Save trading data"""
        data = {
            "balance": self.balance,
            "positions": self.positions,
            "trade_history": self.trade_history,
            "decision_log": self.decision_log,
            "last_updated": datetime.now().isoformat(),
        }
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_locked_balance(self) -> float:
        """Get total locked in open positions"""
        return sum(p.get("amount", 0) for p in self.positions)

    def get_available_balance(self) -> float:
        """Get available balance for new trades"""
        return self.balance - self.get_locked_balance()

    def calculate_pnl(self, position: Dict, current_odds: float) -> float:
        """Calculate PnL for a position"""
        entry_odd = position.get("entry_odds", 0.5)
        amount = position.get("amount", 10)
        side = position.get("side", "YES")

        # Simplified PnL calculation
        if side == "YES":
            return amount * (current_odds - entry_odd)
        else:  # NO
            return amount * (entry_odd - current_odds)

    def place_trade(
        self,
        market_id: str,
        market_title: str,
        side: str,
        amount: float,
        entry_odds: float,
        strategy: str,
    ) -> Dict:
        """Place a paper trade"""

        available = self.get_available_balance()
        if amount > available:
            return {
                "error": f"Insufficient balance. Available: ${available:.2f}, Requested: ${amount:.2f}"
            }

        trade = {
            "id": f"trade_{datetime.now().timestamp()}",
            "market_id": market_id,
            "market_title": market_title[:60],
            "side": side,
            "amount": amount,
            "entry_odds": entry_odds,
            "entry_time": datetime.now().isoformat(),
            "status": "OPEN",
            "unrealized_pnl": 0.0,
            "realized_pnl": 0.0,
            "strategy": strategy,
        }

        self.positions.append(trade)
        self.trade_history.append(trade)

        # Log decision
        self.decision_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": "PLACE_TRADE",
                "market": market_title[:60],
                "side": side,
                "amount": amount,
                "odds": entry_odds,
                "reasoning": strategy,
            }
        )

        self.save_data()

        return trade

    def close_trade(self, trade_id: str, exit_odds: float, exit_reason: str) -> Dict:
        """Close an open position"""
        for pos in self.positions:
            if pos["id"] == trade_id:
                entry = pos["entry_odds"]
                amount = pos["amount"]
                side = pos["side"]

                # Calculate realized PnL
                if side == "YES":
                    pnl = amount * (exit_odds - entry)
                else:
                    pnl = amount * (entry - exit_odds)

                pos["exit_odds"] = exit_odds
                pos["exit_time"] = datetime.now().isoformat()
                pos["realized_pnl"] = pnl
                pos["status"] = "CLOSED"
                pos["exit_reason"] = exit_reason

                # Update balance
                self.balance += amount + pnl

                # Remove from open positions
                self.positions = [p for p in self.positions if p["id"] != trade_id]

                self.decision_log.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "action": "CLOSE_TRADE",
                        "trade_id": trade_id,
                        "exit_odds": exit_odds,
                        "realized_pnl": pnl,
                        "reason": exit_reason,
                    }
                )

                self.save_data()
                return pos

        return {"error": "Trade not found"}

    def scan_active_markets(self) -> List[Dict]:
        """Scan Polymarket for active markets"""
        try:
            url = "https://clob.polymarket.com/markets"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            markets = data.get("data", [])

            # Filter active markets accepting orders
            active = [
                m
                for m in markets
                if m.get("accepting_orders") and not m.get("archived")
            ]

            # Add current odds
            for m in active:
                tokens = m.get("tokens", [])
                if tokens:
                    m["yes_odds"] = tokens[0].get("price", 0.5)
                    m["no_odds"] = 1 - m["yes_odds"]
                else:
                    m["yes_odds"] = 0.5
                    m["no_odds"] = 0.5

            return active

        except Exception as e:
            return []

    def get_opportunities(self) -> List[Dict]:
        """Get trading opportunities (40-60% odds range)"""
        markets = self.scan_active_markets()

        opportunities = []
        for m in markets:
            yes_odds = m.get("yes_odds", 0.5)

            # Only markets with 30-70% odds
            if 0.3 < yes_odds < 0.7:
                opportunities.append(
                    {
                        "id": m.get("condition_id", ""),
                        "title": m.get("question", "")[:70],
                        "yes_odds": yes_odds,
                        "no_odds": 1 - yes_odds,
                        "category": (
                            m.get("tags", ["Unknown"])[0]
                            if m.get("tags")
                            else "Unknown"
                        ),
                    }
                )

        return sorted(opportunities, key=lambda x: abs(x["yes_odds"] - 0.5))

    def auto_trade_strategy(self):
        """Execute auto trading strategy"""
        available = self.get_available_balance()

        if available < 10:
            return {
                "status": "INSUFFICIENT_BALANCE",
                "message": f"Only ${available:.2f} available",
            }

        opportunities = self.get_opportunities()

        if not opportunities:
            return {"status": "NO_OPPORTUNITIES", "message": "No viable markets found"}

        trades_executed = []

        # Strategy: Top 2 opportunities closest to 50/50
        for opp in opportunities[:2]:
            if available < 10:
                break

            # Pick side based on odds
            if opp["yes_odds"] < 0.5:
                side = "YES"  # Undervalued
                odds = opp["yes_odds"]
            else:
                side = "NO"  # Undervalued
                odds = opp["no_odds"]

            trade = self.place_trade(
                market_id=opp["id"],
                market_title=opp["title"],
                side=side,
                amount=10,  # Fixed size
                entry_odds=odds,
                strategy=f"Auto-strategy: 50/50 mean reversion on {opp['category']}",
            )

            if "error" not in trade:
                trades_executed.append(trade)
                available -= 10

        return {
            "status": "EXECUTED",
            "trades": trades_executed,
            "available_after": available,
        }

    def get_report(self) -> Dict:
        """Generate comprehensive report"""
        total_locked = self.get_locked_balance()
        total_realized_pnl = sum(t.get("realized_pnl", 0) for t in self.trade_history)
        total_unrealized_pnl = sum(p.get("unrealized_pnl", 0) for p in self.positions)

        return {
            "balance": {
                "initial": self.initial_balance,
                "current": self.balance,
                "available": self.get_available_balance(),
                "locked": total_locked,
            },
            "positions": {
                "open": len(self.positions),
                "closed": len(self.trade_history) - len(self.positions),
                "total": len(self.trade_history),
            },
            "pnl": {
                "realized": total_realized_pnl,
                "unrealized": total_unrealized_pnl,
                "total": total_realized_pnl + total_unrealized_pnl,
            },
            "open_positions": self.positions,
            "decision_log": self.decision_log[-10:],  # Last 10 decisions
        }

    def print_report(self):
        """Print formatted report"""
        r = self.get_report()

        print("=" * 70)
        print("POLYMARKET PAPER TRADING REPORT")
        print("=" * 70)
        print()

        # Balance
        print("BALANCE SUMMARY")
        print("-" * 70)
        print(f"Initial Balance:      ${r['balance']['initial']:.2f}")
        print(f"Current Balance:      ${r['balance']['current']:.2f}")
        print(f"Available:            ${r['balance']['available']:.2f}")
        print(f"Locked in Positions:  ${r['balance']['locked']:.2f}")
        print()

        # PnL
        print("PROFIT/LOSS")
        print("-" * 70)
        print(f"Realized P/L:         ${r['pnl']['realized']:+.2f}")
        print(f"Unrealized P/L:       ${r['pnl']['unrealized']:+.2f}")
        print(f"Total P/L:            ${r['pnl']['total']:+.2f}")
        print(
            f"Return:               {(r['pnl']['total']/r['balance']['initial']*100):+.2f}%"
        )
        print()

        # Open positions
        print(f"OPEN POSITIONS ({r['positions']['open']})")
        print("-" * 70)
        if r["open_positions"]:
            for i, pos in enumerate(r["open_positions"], 1):
                print(f"{i}. {pos['market_title']}")
                print(
                    f"   Side: {pos['side']} | Amount: ${pos['amount']:.2f} | Entry: {pos['entry_odds']*100:.1f}%"
                )
                print(f"   Unrealized P/L: ${pos.get('unrealized_pnl', 0):+.2f}")
        else:
            print("No open positions")
        print()

        # Decision log
        print("DECISION LOG (Last 10)")
        print("-" * 70)
        for log in r["decision_log"]:
            print(f"[{log['timestamp'][:19]}] {log['action']}")
            if log["action"] == "PLACE_TRADE":
                print(
                    f"   {log['side']} ${log['amount']} on '{log['market']}' @{log['odds']*100:.1f}%"
                )
                print(f"   Reason: {log['reasoning']}")
        print()

        print("=" * 70)
        print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)


def main():
    """Main entry point"""
    trader = PaperTrader()

    print("Polymarket Paper Trader v2.0")
    print()

    # Get user command
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = "report"

    if command == "report":
        trader.print_report()

    elif command == "trade":
        result = trader.auto_trade_strategy()
        print(result)
        trader.print_report()

    elif command == "opportunities":
        opps = trader.get_opportunities()
        print(f"Found {len(opps)} opportunities:")
        for i, opp in enumerate(opps[:5], 1):
            print(f"{i}. {opp['title']}")
            print(f"   YES: {opp['yes_odds']*100:.1f}% | NO: {opp['no_odds']*100:.1f}%")

    else:
        print("Commands: report | trade | opportunities")


if __name__ == "__main__":
    main()
