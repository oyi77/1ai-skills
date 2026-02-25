#!/usr/bin/env python3
"""
Parallel Backtest Runner

Runs all strategies in parallel with $100 initial capital for each strategy.
"""

import sys
import os

# Add parent directory to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import argparse

# Import strategies
from trading.strategy.tradfi.commodities.xauusd_asia_7c_breakout.xauusd_asia_7c_breakout import Asia7CBreakout
from trading.strategy.templates.forex.holy_grail import HolyGrail
from trading.strategy.templates.forex.momentum_elder import MomentumElder
from trading.strategy.templates.forex.kumo_breakout import KumoBreakout
from trading.strategy.templates.stocks.golden_cross import GoldenCross
from trading.strategy.templates.stocks.rsi_divergence import RSIDivergence
from trading.strategy.templates.commodities.seasonal import Seasonal
from trading.strategy.templates.commodities.gold_silver_ratio import GoldSilverRatio

# Strategy configurations
STRATEGIES = [
    {
        "name": "XAUUSD Asia 7-Candle Breakout",
        "strategy": Asia7CBreakout,
        "symbol": "XAUUSD",
        "params": {}
    },
    {
        "name": "Holy Grail (Forex)",
        "strategy": HolyGrail,
        "symbol": "EURUSD",
        "params": {}
    },
    {
        "name": "Momentum Elder (Forex)",
        "strategy": MomentumElder,
        "symbol": "USDJPY",
        "params": {}
    },
    {
        "name": "Kumo Breakout (Forex)",
        "strategy": KumoBreakout,
        "symbol": "USDCAD",
        "params": {}
    },
    {
        "name": "Golden Cross (Stocks)",
        "strategy": GoldenCross,
        "symbol": "AAPL",
        "params": {}
    },
    {
        "name": "RSI Divergence (Stocks)",
        "strategy": RSIDivergence,
        "symbol": "NVDA",
        "params": {}
    },
    {
        "name": "Seasonal (Commodities)",
        "strategy": Seasonal,
        "symbol": "CLNYMEX",  # Crude Oil
        "params": {}
    },
    {
        "name": "Gold/Silver Ratio (Commodities)",
        "strategy": GoldSilverRatio,
        "symbol": "XAUUSD",
        "params": {}
    },
]

BACKTEST_CONFIG = {
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "initial_balance": 100.0,
}


def run_backtest(strategy_config):
    """Run backtest for a single strategy."""
    try:
        strategy_name = strategy_config["name"]
        print(f"[{strategy_name}] Starting backtest...")

        # Initialize strategy
        strategy = strategy_config["strategy"]()

        # Run backtest
        result = strategy.run_backtest(
            start_date=datetime.strptime(BACKTEST_CONFIG["start_date"], "%Y-%m-%d"),
            end_date=datetime.strptime(BACKTEST_CONFIG["end_date"], "%Y-%m-%d")
        )

        if not result or result.get("error"):
            print(f"[{strategy_name}] Failed: {result.get('error', 'Unknown error')}")
            return None

        # Calculate additional metrics
        trades = result.get("trades", [])
        if not trades:
            print(f"[{strategy_name}] No trades generated")
            return None

        # Max drawdown calculation
        balance_curve = [BACKTEST_CONFIG["initial_balance"]]
        for trade in trades:
            balance_curve.append(balance_curve[-1] + trade.get("pnl_usd", 0))

        peak = max(balance_curve) if balance_curve else BACKTEST_CONFIG["initial_balance"]
        trough = min(balance_curve[len(balance_curve)//2:]) if len(balance_curve) > 1 else BACKTEST_CONFIG["initial_balance"]
        max_drawdown = peak - trough if peak > 0 else 0
        max_drawdown_pct = (max_drawdown / peak * 100) if peak > 0 else 0

        # Build report
        report = {
            "strategy": strategy_name,
            "symbol": strategy_config["symbol"],
            "initial_capital": BACKTEST_CONFIG["initial_balance"],
            "ending_balance": result.get("ending_balance", 0),
            "win_rate": result.get("win_rate", 0),
            "wins": result.get("wins", 0),
            "losses": result.get("losses", 0),
            "avg_win_usd": result.get("avg_win_usd", 0),
            "avg_win_points": result.get("avg_win_points", 0),
            "avg_loss_usd": result.get("avg_loss_usd", 0),
            "avg_loss_points": result.get("avg_loss_points", 0),
            "max_drawdown": max_drawdown,
            "max_drawdown_pct": round(max_drawdown_pct, 2),
            "gross_profit": result.get("gross_profit_usd", 0),
            "gross_loss": abs(result.get("gross_loss_usd", 0)),
            "profit_factor": result.get("profit_factor", 0),
            "net_pnl": result.get("net_pnl", 0),
            "total_trades": len(trades),
        }

        print(f"[{strategy_name}] Completed: {result.get('win_rate', 0):.1f}% WR")
        return report

    except Exception as e:
        print(f"[{strategy_config['name']}] Error: {e}")
        return None


def format_report(reports):
    """Format all backtest reports into a summary."""
    if not reports:
        return {"error": "No reports generated"}

    # Generate comparison table
    print("\n" + "="*80)
    print("PARALLEL BACKTEST REPORT - 2025")
    print("="*80)
    print(f"Period: {BACKTEST_CONFIG['start_date']} to {BACKTEST_CONFIG['end_date']}")
    print(f"Initial Capital: ${BACKTEST_CONFIG['initial_balance']:.2f} per strategy")
    print("="*80)

    # Sort by win rate
    sorted_reports = sorted(reports, key=lambda x: x.get("win_rate", 0), reverse=True)

    print("\nSTRATEGY COMPARISON:")
    print("-" * 80)
    print(f"{'Strategy':<30} {'WR':>8} {'Trades':>8} {'Wins':>7} {'Losses':>8} {'Avg Win':>12} {'Avg Loss':>12} {'Max DD':>10} {'Profit Factor':>14} {'Net PNL':>12}")
    print("-" * 80)

    for i, report in enumerate(sorted_reports, 1):
        print(f"{i}. {report['strategy']:<29} {report['win_rate']:>6.1f}% {report['total_trades']:>6} {report['wins']:>5} {report['losses']:>7} ${report['avg_win_usd']:>8.2f} ${report['avg_loss_usd']:>9.2f} ${report['max_drawdown']:>9.2f} ({report['max_drawdown_pct']:>5.1f}%) {report['profit_factor']:>10.2f} ${report['net_pnl']:>10.2f}")

    # Summary statistics
    total_trades = sum(r.get("total_trades", 0) for r in reports)
    total_wins = sum(r.get("wins", 0) for r in reports)
    total_losses = sum(r.get("losses", 0) for r in reports)
    total_net_pnl = sum(r.get("net_pnl", 0) for r in reports)
    avg_win_rate = sum(r.get("win_rate", 0) for r in reports) / len(reports)

    best_strategy = max(reports, key=lambda x: x.get("win_rate", 0)) if reports else None
    worst_strategy = min(reports, key=lambda x: x.get("win_rate", 0)) if reports else None

    print("\n" + "="*80)
    print("SUMMARY STATISTICS:")
    print("="*80)
    print(f"Total Strategies Tested: {len(reports)}")
    print(f"Total Trades: {total_trades}")
    print(f"Total Wins: {total_wins}")
    print(f"Total Losses: {total_losses}")
    print(f"Average Win Rate: {avg_win_rate:.1f}%")
    print(f"Total Net PNL: ${total_net_pnl:.2f}")
    print(f"Best Strategy: {best_strategy['strategy'] if best_strategy else 'N/A'} ({best_strategy['win_rate']:.1f}% WR)")
    print(f"Worst Strategy: {worst_strategy['strategy'] if worst_strategy else 'N/A'} ({worst_strategy['win_rate']:.1f}% WR)")
    print("="*80)

    return {
        "total_strategies": len(reports),
        "total_trades": total_trades,
        "total_wins": total_wins,
        "total_losses": total_losses,
        "total_net_pnl": total_net_pnl,
        "average_win_rate": avg_win_rate,
        "best_strategy": best_strategy.get("strategy") if best_strategy else None,
        "worst_strategy": worst_strategy.get("strategy") if worst_strategy else None,
        "reports": reports,
    }


def save_json_report(reports, summary):
    """Save detailed reports to JSON."""
    output = {
        "config": BACKTEST_CONFIG,
        "summary": summary,
        "reports": reports,
        "timestamp": datetime.now().isoformat()
    }

    with open("backtest_results_2025.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved results to: backtest_results_2025.json")


def main():
    parser = argparse.ArgumentParser(description="Parallel Backtest Runner")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers")
    parser.add_argument("--strategies", type=str, help="Comma-separated list of strategies to run")
    parser.add_argument("--json", action="store_true", help="Output JSON report")

    args = parser.parse_args()

    # Filter strategies if specified
    strategies_to_run = STRATEGIES
    if args.strategies:
        strategy_names = [s.strip().lower() for s in args.strategies.split(",")]
        strategies_to_run = [s for s in STRATEGIES if s["name"].lower() in strategy_names]

    print(f"\nStarting parallel backtest with {len(strategies_to_run)} strategies...")
    print(f"Workers: {args.workers}")
    print(f"Initial Capital: ${BACKTEST_CONFIG['initial_balance']:.2f} per strategy")
    print()

    # Run backtests in parallel
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(run_backtest, strategy) for strategy in strategies_to_run}

        # Wait for all to complete
        reports = []
        for future in as_completed(futures):
            report = future.result()
            if report:
                reports.append(report)

    # Format and display report
    summary = format_report(reports)

    # Save JSON if requested
    if args.json:
        save_json_report(reports, summary)


if __name__ == "__main__":
    main()
