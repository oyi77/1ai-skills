#!/usr/bin/env python3
"""
Risk Calculator — position sizing, R:R, drawdown, daily risk, Kelly criterion.

Usage:
    python risk_calculator.py --balance 1000 --risk 1 --entry 2300 --sl 2290 --tp 2320
    python risk_calculator.py size --balance 5000 --risk 2 --entry 2300 --sl 2280
    python risk_calculator.py rr --entry 2300 --sl 2290 --tp 2330
    python risk_calculator.py drawdown --history trades.json
    python risk_calculator.py daily-check --positions positions.json --balance 10000
    python risk_calculator.py kelly --win-rate 0.55 --avg-win 200 --avg-loss 100
"""

import argparse
import json
import sys
from pathlib import Path


def calculate_position_size(account_balance, risk_pct, entry, stop_loss):
    """Calculate position size (lot size) based on risk parameters.

    Returns lot size where risk_amount = account_balance * risk_pct / 100,
    and lot_size = risk_amount / abs(entry - stop_loss).
    """
    risk_amount = account_balance * (risk_pct / 100)
    pip_risk = abs(entry - stop_loss)
    if pip_risk == 0:
        return {"error": "Entry and stop loss cannot be the same price"}
    lot_size = risk_amount / pip_risk
    return {
        "account_balance": account_balance,
        "risk_pct": risk_pct,
        "risk_amount": round(risk_amount, 2),
        "entry": entry,
        "stop_loss": stop_loss,
        "pip_risk": round(pip_risk, 4),
        "lot_size": round(lot_size, 4),
    }


def calculate_rr(entry, stop_loss, take_profit):
    """Calculate risk:reward ratio."""
    risk = abs(entry - stop_loss)
    reward = abs(take_profit - entry)
    if risk == 0:
        return {"error": "Entry and stop loss cannot be the same price"}
    ratio = reward / risk
    return {
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_pips": round(risk, 4),
        "reward_pips": round(reward, 4),
        "rr_ratio": round(ratio, 2),
        "rr_display": f"1:{ratio:.2f}",
    }


def calculate_max_drawdown(trade_history):
    """Calculate maximum drawdown from a list of trade P&L values.

    trade_history: list of dicts with 'pnl' key, or list of floats.
    """
    if not trade_history:
        return {"error": "Empty trade history"}

    pnls = []
    for t in trade_history:
        if isinstance(t, dict):
            pnls.append(float(t.get("pnl", 0)))
        else:
            pnls.append(float(t))

    cumulative = []
    running = 0
    for pnl in pnls:
        running += pnl
        cumulative.append(running)

    peak = cumulative[0]
    max_dd = 0
    max_dd_pct = 0
    for val in cumulative:
        if val > peak:
            peak = val
        dd = peak - val
        if dd > max_dd:
            max_dd = dd
            max_dd_pct = (dd / peak * 100) if peak > 0 else 0

    total_pnl = sum(pnls)
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]

    return {
        "total_trades": len(pnls),
        "total_pnl": round(total_pnl, 2),
        "max_drawdown": round(max_dd, 2),
        "max_drawdown_pct": round(max_dd_pct, 2),
        "win_count": len(wins),
        "loss_count": len(losses),
        "win_rate": round(len(wins) / len(pnls) * 100, 1) if pnls else 0,
        "avg_win": round(sum(wins) / len(wins), 2) if wins else 0,
        "avg_loss": round(sum(losses) / len(losses), 2) if losses else 0,
    }


def daily_risk_check(open_positions, account_balance):
    """Check if total risk from open positions exceeds 2% of account.

    open_positions: list of dicts with 'entry', 'stop_loss', 'size' keys.
    """
    total_risk = 0
    position_risks = []
    for pos in open_positions:
        entry = float(pos.get("entry", 0))
        sl = float(pos.get("stop_loss", 0))
        size = float(pos.get("size", 0))
        risk = abs(entry - sl) * size
        total_risk += risk
        position_risks.append({
            "asset": pos.get("asset", "unknown"),
            "risk_amount": round(risk, 2),
            "risk_pct": round(risk / account_balance * 100, 2) if account_balance > 0 else 0,
        })

    risk_pct = (total_risk / account_balance * 100) if account_balance > 0 else 0
    return {
        "account_balance": account_balance,
        "total_risk": round(total_risk, 2),
        "total_risk_pct": round(risk_pct, 2),
        "max_allowed_pct": 2.0,
        "status": "WARNING: OVER LIMIT" if risk_pct > 2.0 else "OK",
        "positions": position_risks,
    }


def kelly_criterion(win_rate, avg_win, avg_loss):
    """Calculate Kelly criterion for optimal position sizing.

    Kelly % = W - (1 - W) / R
    where W = win probability, R = win/loss ratio
    """
    if avg_loss == 0:
        return {"error": "Average loss cannot be zero"}
    avg_loss_abs = abs(avg_loss)
    win_loss_ratio = avg_win / avg_loss_abs
    kelly_pct = win_rate - ((1 - win_rate) / win_loss_ratio)
    # Half-Kelly is commonly used for more conservative sizing
    half_kelly = kelly_pct / 2
    return {
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "win_loss_ratio": round(win_loss_ratio, 2),
        "kelly_pct": round(kelly_pct * 100, 2),
        "half_kelly_pct": round(half_kelly * 100, 2),
        "recommendation": "Use half-Kelly for conservative sizing",
    }


def main():
    parser = argparse.ArgumentParser(description="Risk Calculator")
    sub = parser.add_subparsers(dest="command")

    # Default: full calculation
    parser.add_argument("--balance", type=float, help="Account balance")
    parser.add_argument("--risk", type=float, help="Risk percentage")
    parser.add_argument("--entry", type=float, help="Entry price")
    parser.add_argument("--sl", type=float, help="Stop loss price")
    parser.add_argument("--tp", type=float, help="Take profit price")

    # Subcommands
    s = sub.add_parser("size", help="Position size only")
    s.add_argument("--balance", required=True, type=float)
    s.add_argument("--risk", required=True, type=float)
    s.add_argument("--entry", required=True, type=float)
    s.add_argument("--sl", required=True, type=float)

    r = sub.add_parser("rr", help="Risk:Reward ratio")
    r.add_argument("--entry", required=True, type=float)
    r.add_argument("--sl", required=True, type=float)
    r.add_argument("--tp", required=True, type=float)

    d = sub.add_parser("drawdown", help="Max drawdown from history")
    d.add_argument("--history", required=True, help="JSON file with trade history")

    dc = sub.add_parser("daily-check", help="Daily risk check")
    dc.add_argument("--positions", required=True, help="JSON file with open positions")
    dc.add_argument("--balance", required=True, type=float)

    k = sub.add_parser("kelly", help="Kelly criterion")
    k.add_argument("--win-rate", required=True, type=float)
    k.add_argument("--avg-win", required=True, type=float)
    k.add_argument("--avg-loss", required=True, type=float)

    args = parser.parse_args()

    if args.command == "size":
        result = calculate_position_size(args.balance, args.risk, args.entry, args.sl)
    elif args.command == "rr":
        result = calculate_rr(args.entry, args.sl, args.tp)
    elif args.command == "drawdown":
        history = json.loads(Path(args.history).read_text())
        result = calculate_max_drawdown(history)
    elif args.command == "daily-check":
        positions = json.loads(Path(args.positions).read_text())
        result = daily_risk_check(positions, args.balance)
    elif args.command == "kelly":
        result = kelly_criterion(args.win_rate, args.avg_win, args.avg_loss)
    elif args.balance and args.risk and args.entry and args.sl:
        # Default: full calculation with all provided params
        result = {"position_size": calculate_position_size(args.balance, args.risk, args.entry, args.sl)}
        if args.tp:
            result["risk_reward"] = calculate_rr(args.entry, args.sl, args.tp)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
