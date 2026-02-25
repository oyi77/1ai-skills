#!/usr/bin/env python3
"""
Simple Parallel Backtest Runner - Simplified

Runs all strategies with $100 initial capital.
"""

import sys
import os
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import subprocess

# Strategy configurations
STRATEGIES = [
    {
        "name": "XAUUSD Asia 7-Candle Breakout",
        "script": "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py",
        "symbol": "XAUUSD",
        "args": ["backtest", "2025-01-01", "2025-12-31"]
    },
    {
        "name": "Holy Grail (EURUSD)",
        "script": "strategy/templates/forex/holy_grail.py",
        "symbol": "EURUSD",
        "args": []
    },
    {
        "name": "Momentum Elder (USDJPY)",
        "script": "strategy/templates/forex/momentum_elder.py",
        "symbol": "USDJPY",
        "args": []
    },
    {
        "name": "Kumo Breakout (USDCAD)",
        "script": "strategy/templates/forex/kumo_breakout.py",
        "symbol": "USDCAD",
        "args": []
    },
    {
        "name": "Golden Cross (AAPL)",
        "script": "strategy/templates/stocks/golden_cross.py",
        "symbol": "AAPL",
        "args": []
    },
    {
        "name": "RSI Divergence (NVDA)",
        "script": "strategy/templates/stocks/rsi_divergence.py",
        "symbol": "NVDA",
        "args": []
    },
]

BACKTEST_DIR = os.path.dirname(os.path.abspath(__file__))


def run_strategy(strategy):
    """Run a single strategy using subprocess."""
    try:
        script_path = os.path.join(BACKTEST_DIR, strategy["script"])
        cmd = ["python3", script_path] + strategy["args"]

        print(f"[{strategy['name']}] Starting...")

        # Run subprocess
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes timeout
        )

        # Parse output
        output = result.stdout
        if result.returncode != 0:
            print(f"[{strategy['name']}] Error: {output[-500:]}")
            return None

        # Extract metrics from output
        lines = output.split('\n')

        metrics = {
            "strategy": strategy["name"],
            "symbol": strategy["symbol"],
            "initial_capital": 100.0,
            "ending_balance": 0.0,
            "win_rate": 0.0,
            "wins": 0,
            "losses": 0,
            "avg_win_usd": 0.0,
            "avg_win_points": 0.0,
            "avg_loss_usd": 0.0,
            "avg_loss_points": 0.0,
            "max_drawdown": 0.0,
            "max_drawdown_pct": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "profit_factor": 0.0,
            "net_pnl": 0.0,
            "total_trades": 0,
        }

        for line in lines:
            if "Total Trades" in line:
                metrics["total_trades"] = int(line.split(":")[1].strip())
            elif "Wins:" in line:
                metrics["wins"] = int(line.split(":")[1].strip())
            elif "Losses:" in line:
                metrics["losses"] = int(line.split(":")[1].strip())
            elif "Win Rate:" in line:
                metrics["win_rate"] = float(line.split(":")[1].strip().replace("%", ""))
            elif "Net PNL:" in line:
                pnl_line = line.split(":")[1].strip()
                if "$" in pnl_line:
                    metrics["net_pnl"] = float(pnl_line.replace("$", ""))
            elif "Gross Profit:" in line:
                metrics["gross_profit"] = float(line.split(":")[1].strip().replace("$", ""))
            elif "Gross Loss:" in line:
                metrics["gross_loss"] = float(line.split(":")[1].strip().replace("$", ""))
            elif "Profit Factor:" in line:
                metrics["profit_factor"] = float(line.split(":")[1].strip())
            elif "Max Drawdown:" in line:
                dd_line = line.split(":")[1].strip()
                if "(" in dd_line:
                    # Format: "$100.00 (10.0%)"
                    metrics["max_drawdown"] = float(dd_line.split("$")[1].split("(")[0].strip())
                    metrics["max_drawdown_pct"] = float(dd_line.split("(")[1].replace("%", "").replace(")", ""))
            elif "Avg Win" in line and "USD" in line:
                metrics["avg_win_usd"] = float(line.split("$")[1].strip())
            elif "Avg Win" in line and "points" in line:
                metrics["avg_win_points"] = float(line.split("points")[1].strip())
            elif "Avg Loss" in line and "USD" in line:
                metrics["avg_loss_usd"] = float(line.split("$")[1].strip())
            elif "Avg Loss" in line and "points" in line:
                metrics["avg_loss_points"] = float(line.split("points")[1].strip())

        metrics["ending_balance"] = 100.0 + metrics["net_pnl"]

        print(f"[{strategy['name']}] Completed: {metrics['win_rate']:.1f}% WR")
        return metrics

    except Exception as e:
        print(f"[{strategy['name']}] Error: {e}")
        return None


def main():
    print("\n" + "="*80)
    print("PARALLEL BACKTEST RUNNER - SIMPLIFIED")
    print("="*80)
    print(f"Period: 2025-01-01 to 2025-12-31")
    print(f"Initial Capital: $100.00 per strategy")
    print(f"Strategies to test: {len(STRATEGIES)}")
    print("="*80)
    print()

    # Run all strategies in parallel with 4 workers
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run_strategy, strategy) for strategy in STRATEGIES}

        # Wait for all to complete
        reports = []
        for future in as_completed(futures):
            report = future.result()
            if report:
                reports.append(report)

    # Generate report
    print("\n" + "="*80)
    print("BACKTEST RESULTS SUMMARY")
    print("="*80)

    # Sort by win rate
    sorted_reports = sorted(reports, key=lambda x: x.get("win_rate", 0), reverse=True)

    for i, report in enumerate(sorted_reports):
        print(f"\n{i}. {report['strategy']:<30} {report['win_rate']:>6.1f}% WR")
        print(f"   Trades: {report['total_trades']:>4} | Wins: {report['wins']:>4} | Losses: {report['losses']:>4}")
        print(f"   Net PNL: ${report['net_pnl']:>10.2f}")
        print(f"   Gross Profit: ${report['gross_profit']:>9.2f}")
        print(f"   Gross Loss: ${report['gross_loss']:>9.2f}")
        print(f"   Max DD: ${report['max_drawdown']:>9.2f} ({report['max_drawdown_pct']:>5.1f}%)")
        print(f"   Profit Factor: {report['profit_factor']:>5.2f}")

    # Summary statistics
    total_trades = sum(r.get("total_trades", 0) for r in reports)
    total_wins = sum(r.get("wins", 0) for r in reports)
    total_losses = sum(r.get("losses", 0) for r in reports)
    total_net_pnl = sum(r.get("net_pnl", 0) for r in reports)
    avg_win_rate = sum(r.get("win_rate", 0) for r in reports) / len(reports)

    best_strategy = max(reports, key=lambda x: x.get("win_rate", 0)) if reports else None
    worst_strategy = min(reports, key=lambda x: x.get("win_rate", 0)) if reports else None

    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
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

    # Save JSON
    output = {
        "period": "2025-01-01 to 2025-12-31",
        "initial_capital": 100.0,
        "reports": reports,
        "summary": {
            "total_strategies": len(reports),
            "total_trades": total_trades,
            "total_wins": total_wins,
            "total_losses": total_losses,
            "average_win_rate": avg_win_rate,
            "total_net_pnl": total_net_pnl,
            "best_strategy": best_strategy.get("strategy") if best_strategy else None,
            "worst_strategy": worst_strategy.get("strategy") if worst_strategy else None,
        },
        "timestamp": datetime.now().isoformat()
    }

    with open("backtest_results_all_strategies_2025.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved results to: backtest_results_all_strategies_2025.json")


if __name__ == "__main__":
    main()
