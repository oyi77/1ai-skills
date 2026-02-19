#!/usr/bin/env python3
"""
Trading Backtest Summary Generator

Generates trading performance summary with:
- PNL in USD
- PNL in Points/Pips
- Avg Win/Loss in USD
- Avg Win/Loss in Points/Pips
- Profit Factor
- Pair
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional


def analyze_trades(trades: List[Dict[str, Any]], use_points: bool = False, 
                   initial_balance: float = None) -> Dict[str, Any]:
    """Analyze trading results and return metrics including drawdown."""
    
    if not trades:
        return {
            "total_trades": 0,
            "win_count": 0,
            "loss_count": 0,
            "win_rate": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "net_pnl": 0.0,
            "avg_win": 0.0,
            "avg_loss": 0.0,
            "avg_trade": 0.0,
            "profit_factor": 0.0,
            "max_drawdown": 0.0,
            "max_drawdown_pct": 0.0,
            "initial_balance": 0.0,
            "ending_balance": 0.0,
            "pairs": []
        }
    
    total_trades = len(trades)
    win_count = sum(1 for t in trades if t.get("win", False))
    loss_count = total_trades - win_count
    
    # Check if we use points or USD
    if use_points:
        pnl_key = "pnl_points"
        wins = [t["pnl_points"] for t in trades if t.get("win", False)]
        losses = [abs(t["pnl_points"]) for t in trades if not t.get("win", True)]
    else:
        pnl_key = "pnl_usd"
        wins = [t["pnl_usd"] for t in trades if t.get("win", False)]
        losses = [abs(t["pnl_usd"]) for t in trades if not t.get("win", True)]
    
    gross_profit = sum(wins) if wins else 0.0
    gross_loss = sum(losses) if losses else 0.0
    net_pnl = gross_profit - gross_loss
    
    avg_win = gross_profit / len(wins) if wins else 0.0
    avg_loss = gross_loss / len(losses) if losses else 0.0
    avg_trade = net_pnl / total_trades if total_trades else 0.0
    
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf') if gross_profit > 0 else 0.0
    
    pairs = list(set(t.get("pair", "UNKNOWN") for t in trades))
    
    # Calculate Max Drawdown and Balance metrics
    equity_curve = []
    current_equity = initial_balance if initial_balance else 10000.0  # Default $10k if not specified
    start_balance = current_equity
    
    for t in trades:
        pnl = t.get("pnl_usd", 0)
        current_equity += pnl
        equity_curve.append(current_equity)
    
    if equity_curve:
        # Calculate max drawdown
        peak = start_balance
        max_drawdown = 0.0
        max_drawdown_pct = 0.0
        
        for equity in equity_curve:
            if equity > peak:
                peak = equity
            drawdown = peak - equity
            if drawdown > max_drawdown:
                max_drawdown = drawdown
                max_drawdown_pct = (drawdown / peak * 100) if peak > 0 else 0.0
        
        ending_balance = equity_curve[-1]
    else:
        max_drawdown = 0.0
        max_drawdown_pct = 0.0
        ending_balance = start_balance
    
    # Calculate USD metrics if available
    usd_metrics = None
    if any("pnl_usd" in t for t in trades):
        usd_wins = [t["pnl_usd"] for t in trades if t.get("win", False)]
        usd_losses = [abs(t["pnl_usd"]) for t in trades if not t.get("win", True)]
        usd_gross_profit = sum(usd_wins) if usd_wins else 0.0
        usd_gross_loss = sum(usd_losses) if usd_losses else 0.0
        usd_metrics = {
            "gross_profit": usd_gross_profit,
            "gross_loss": -usd_gross_loss,
            "net_pnl": usd_gross_profit - usd_gross_loss,
            "avg_win": usd_gross_profit / len(usd_wins) if usd_wins else 0.0,
            "avg_loss": -usd_gross_loss / len(usd_losses) if usd_losses else 0.0,
        }
    
    # Calculate Points metrics if available
    points_metrics = None
    if any("pnl_points" in t for t in trades):
        pt_wins = [t["pnl_points"] for t in trades if t.get("win", False)]
        pt_losses = [abs(t["pnl_points"]) for t in trades if not t.get("win", True)]
        pt_gross_profit = sum(pt_wins) if pt_wins else 0.0
        pt_gross_loss = sum(pt_losses) if pt_losses else 0.0
        points_metrics = {
            "gross_profit": pt_gross_profit,
            "gross_loss": -pt_gross_loss,
            "net_pnl": pt_gross_profit - pt_gross_loss,
            "avg_win": pt_gross_profit / len(pt_wins) if pt_wins else 0.0,
            "avg_loss": -pt_gross_loss / len(pt_losses) if pt_losses else 0.0,
        }
    
    return {
        "total_trades": total_trades,
        "win_count": win_count,
        "loss_count": loss_count,
        "win_rate": (win_count / total_trades * 100) if total_trades > 0 else 0.0,
        "gross_profit": gross_profit,
        "gross_loss": -gross_loss,
        "net_pnl": net_pnl,
        "avg_win": avg_win,
        "avg_loss": -avg_loss,
        "avg_trade": avg_trade,
        "profit_factor": profit_factor,
        "max_drawdown": max_drawdown,
        "max_drawdown_pct": max_drawdown_pct,
        "initial_balance": start_balance,
        "ending_balance": ending_balance,
        "pairs": pairs,
        "usd": usd_metrics,
        "points": points_metrics,
    }


def generate_summary(metrics: Dict[str, Any], pair: str = None, use_points: bool = False) -> str:
    """Generate formatted summary string with both USD and Points metrics."""
    
    pair_name = pair or (metrics["pairs"][0] if metrics["pairs"] else "UNKNOWN")
    
    # Calculate return percentage
    initial = metrics.get("initial_balance", 10000.0)
    ending = metrics.get("ending_balance", initial)
    return_pct = ((ending - initial) / initial * 100) if initial > 0 else 0.0
    
    lines = [
        "=" * 60,
        f"{'BACKTEST SUMMARY':^60}",
        "=" * 60,
        f"PAIR              : {pair_name}",
        "-" * 60,
        f"Total Trades      : {metrics['total_trades']}",
        f"Win Rate          : {metrics['win_rate']:.2f}%",
        "-" * 60,
        "BALANCE",
        f"  Initial Balance : ${initial:,.2f}",
        f"  Ending Balance  : ${ending:,.2f}",
        f"  Net PNL         : ${metrics['net_pnl']:,.2f} ({return_pct:+.2f}%)",
        "-" * 60,
        "DRAWDOWN",
        f"  Max Drawdown    : ${metrics['max_drawdown']:,.2f} ({metrics['max_drawdown_pct']:.2f}%)",
        "-" * 60,
    ]
    
    # USD Section
    if metrics.get("usd"):
        usd = metrics["usd"]
        lines.extend([
            "PNL (USD)",
            f"  Gross Profit    : ${usd['gross_profit']:,.2f}",
            f"  Gross Loss      : ${usd['gross_loss']:,.2f}",
            f"  Avg Win         : ${usd['avg_win']:,.2f}",
            f"  Avg Loss        : ${usd['avg_loss']:,.2f}",
            "-" * 60,
        ])
    
    # Points Section
    if metrics.get("points"):
        pts = metrics["points"]
        lines.extend([
            "PNL (Points/Pips)",
            f"  Gross Profit    : {pts['gross_profit']:,.2f}",
            f"  Gross Loss      : {pts['gross_loss']:,.2f}",
            f"  Net PNL         : {pts['net_pnl']:,.2f}",
            f"  Avg Win         : {pts['avg_win']:,.2f}",
            f"  Avg Loss        : {pts['avg_loss']:,.2f}",
            "-" * 60,
        ])
    
    # Fallback if no USD or Points
    if not metrics.get("usd") and not metrics.get("points"):
        lines.extend([
            "PNL SUMMARY",
            f"  Gross Profit    : ${metrics['gross_profit']:,.2f}",
            f"  Gross Loss      : ${metrics['gross_loss']:,.2f}",
            "-" * 60,
        ])
    
    lines.extend([
        f"PROFIT FACTOR     : {metrics['profit_factor']:.2f}",
        "=" * 60,
    ])
    
    return "\n".join(lines)


def load_trades_from_csv(filepath: str) -> List[Dict[str, Any]]:
    """Load trades from CSV file - supports both USD and Points."""
    trades = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                trade = {
                    "pair": row.get("pair", "UNKNOWN"),
                    "win": row.get("win", "").lower() in ("true", "1", "yes")
                }
                # Support both USD and Points columns
                if "pnl_usd" in row:
                    trade["pnl_usd"] = float(row.get("pnl_usd", 0))
                if "pnl_points" in row:
                    trade["pnl_points"] = float(row.get("pnl_points", 0))
                if "pnl_pips" in row:
                    trade["pnl_points"] = float(row.get("pnl_pips", 0))
                # Fallback to any pnl column
                if "pnl_usd" not in trade and "pnl_points" not in trade:
                    trade["pnl_usd"] = float(row.get("pnl", row.get("profit", 0)))
                trades.append(trade)
            except (ValueError, KeyError) as e:
                print(f"Warning: Skipping invalid row: {e}", file=sys.stderr)
    
    return trades


def main():
    parser = argparse.ArgumentParser(
        description="Generate trading backtest summary"
    )
    parser.add_argument(
        "--file", "-f",
        required=False,
        help="Path to CSV file with trades"
    )
    parser.add_argument(
        "--pair", "-p",
        required=False,
        help="Trading pair symbol (e.g., XAUUSD)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--points", "-P",
        action="store_true",
        help="Use points/pips instead of USD for analysis"
    )
    parser.add_argument(
        "--initial-balance", "-i",
        type=float,
        default=10000.0,
        help="Initial balance (default: $10,000)"
    )
    
    args = parser.parse_args()
    
    # Demo data if no file provided (includes both USD and Points)
    if not args.file:
        # Sample trades with both USD and Points for demonstration
        trades = [
            {"pair": "XAUUSD", "pnl_usd": 27.00, "pnl_points": 2.7, "win": True},
            {"pair": "XAUUSD", "pnl_usd": -45.00, "pnl_points": -4.5, "win": False},
            {"pair": "XAUUSD", "pnl_usd": 120.50, "pnl_points": 12.05, "win": True},
            {"pair": "XAUUSD", "pnl_usd": -32.00, "pnl_points": -3.2, "win": False},
            {"pair": "XAUUSD", "pnl_usd": 89.00, "pnl_points": 8.9, "win": True},
            {"pair": "XAUUSD", "pnl_usd": -28.50, "pnl_points": -2.85, "win": False},
            {"pair": "XAUUSD", "pnl_usd": 156.00, "pnl_points": 15.6, "win": True},
            {"pair": "XAUUSD", "pnl_usd": -41.00, "pnl_points": -4.1, "win": False},
            {"pair": "XAUUSD", "pnl_usd": 95.00, "pnl_points": 9.5, "win": True},
            {"pair": "XAUUSD", "pnl_usd": -55.00, "pnl_points": -5.5, "win": False},
        ]
    else:
        trades = load_trades_from_csv(args.file)
    
    metrics = analyze_trades(trades, use_points=args.points, initial_balance=args.initial_balance)
    
    if args.json:
        import json
        print(json.dumps(metrics, indent=2))
    else:
        pair = args.pair or (metrics["pairs"][0] if metrics["pairs"] else None)
        summary = generate_summary(metrics, pair, use_points=args.points)
        print(summary)


if __name__ == "__main__":
    main()
