#!/usr/bin/env python3
"""
VILONA DEBUG FIX - Fix Trading Script Imports

Problem: Scripts can't find 'trading' module
Solution: Run scripts with proper PYTHONPATH
"""

import sys
import os
import subprocess
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

# Working directory
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up to trading directory
TRADING_BASE = os.path.dirname(WORK_DIR)

# Add to Python path
sys.path.insert(0, TRADING_BASE)

print(f"WORK_DIR: {WORK_DIR}")
print(f"TRADING_BASE: {TRADING_BASE}")
print(f"PYTHONPATH: {sys.path[0]}")
print()

# Market configurations
MARKETS = {
    "XAUUSD": {"type": "commodities", "symbol": "XAUUSD", "timeframes": ["H1", "H4", "D1"]},
    "GBPUSD": {"type": "forex", "symbol": "GBPUSD", "timeframes": ["H1", "H4", "D1"]},
    "EURUSD": {"type": "forex", "symbol": "EURUSD", "timeframes": ["H1", "H4", "D1"]},
    "USDJPY": {"type": "forex", "symbol": "USDJPY", "timeframes": ["H1", "H4", "D1"]},
    "BTCUSDT": {"type": "crypto", "symbol": "BTCUSDT", "timeframes": ["1h", "4h", "1d"]},
    "ETHUSDT": {"type": "crypto", "symbol": "ETHUSDT", "timeframes": ["1h", "4h", "1d"]},
    "SOLUSDT": {"type": "crypto", "symbol": "SOLUSDT", "timeframes": ["1h", "4h", "1d"]},
}

# Strategy scripts
STRATEGIES = {
    "forex": [
        {"name": "HOLY_GRAIL", "script": "strategy/templates/forex/holy_grail.py"},
        {"name": "MOMENTUM_ELDER", "script": "strategy/templates/forex/momentum_elder.py"},
        {"name": "KUMO_BREAKOUT", "script": "strategy/templates/forex/kumo_breakout.py"},
    ],
    "commodities": [
        {"name": "ASIA_7CANDLE", "script": "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"},
    ],
    "crypto": [
        {"name": "VOLUME_MOMENTUM", "script": "strategy/templates/crypto/volume_momentum.py"},
        {"name": "FUNDING_REVERSAL", "script": "strategy/templates/crypto/funding_reversal.py"},
    ],
}

CONFIG = {
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "initial_balance": 100.0,
}

def run_backtest(pair, timeframe, strategy):
    """Run backtest with fixed PYTHONPATH."""
    strat_name = strategy["name"]
    script = strategy["script"]

    # Build environment with PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = TRADING_BASE

    # Build command - run from TRADING_BASE
    cmd = [
        "python3", script,
        "backtest",
        CONFIG["start_date"],
        CONFIG["end_date"],
        "--initial-balance", str(int(CONFIG["initial_balance"]))
    ]

    print(f"[RUNNING] {pair} {timeframe} {strat_name}...")

    # Run from TRADING_BASE directory
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=3600,
        cwd=TRADING_BASE,
        env=env
    )

    if result.returncode != 0:
        return {
            "pair": pair,
            "timeframe": timeframe,
            "strategy": strat_name,
            "error": f"RUNTIME_ERROR: {result.stderr[:200]}",
        }

    # Parse output
    output = result.stdout
    metrics = {
        "pair": pair,
        "timeframe": timeframe,
        "strategy": strat_name,
        "period": f"{CONFIG['start_date']} to {CONFIG['end_date']}",
        "initial_capital": CONFIG["initial_balance"],
        "win_rate": 0,
        "wins": 0,
        "losses": 0,
        "avg_win_usd": 0,
        "avg_loss_usd": 0,
        "max_drawdown": 0,
        "max_drawdown_pct": 0,
        "gross_profit": 0,
        "gross_loss": 0,
        "profit_factor": 0,
        "net_pnl": 0,
        "ending_balance": CONFIG["initial_balance"],
        "total_trades": 0,
    }

    for line in output.split('\n'):
        if "Win Rate:" in line: metrics["win_rate"] = float(line.split(":")[1].strip().replace("%", ""))
        elif "Total Trades:" in line: metrics["total_trades"] = int(line.split(":")[1].strip())
        elif "Wins:" in line: metrics["wins"] = int(line.split(":")[1].strip())
        elif "Losses:" in line: metrics["losses"] = int(line.split(":")[1].strip())
        elif "Net PNL:" in line and "$" in line:
            metrics["net_pnl"] = float(line.split(":")[1].strip().replace("$", ""))
            metrics["ending_balance"] = CONFIG["initial_balance"] + metrics["net_pnl"]
        elif "Profit Factor:" in line: metrics["profit_factor"] = float(line.split(":")[1].strip())
        elif "Gross Profit:" in line and "$" in line: metrics["gross_profit"] = float(line.split(":")[1].strip().replace("$", ""))
        elif "Gross Loss:" in line and "$" in line: metrics["gross_loss"] = float(line.split(":")[1].strip().replace("$", ""))
        elif "Max Drawdown:" in line:
            dd = line.split(":")[1].strip()
            if "(" in dd:
                metrics["max_drawdown"] = float(dd.split("$")[1].split("(")[0].strip())
                metrics["max_drawdown_pct"] = float(dd.split("(")[1].replace("%", "").replace(")", ""))
        elif "Avg Win (USD)" in line: metrics["avg_win_usd"] = float(line.split(":")[1].strip().replace("$", ""))
        elif "Avg Loss (USD)" in line: metrics["avg_loss_usd"] = float(line.split(":")[1].strip().replace("$", ""))

    print(f"[DONE] {pair} {timeframe} {strat_name}: {metrics['win_rate']:.1f}% WR, ${metrics['net_pnl']:.2f} PNL")
    return metrics


def main():
    print("\n" + "="*80)
    print("VILONA DEBUG - FIXED PYTHONPATH")
    print("="*80)
    print(f"PYTHONPATH: {TRADING_BASE}")
    print(f"Working Dir: {TRADING_BASE}")
    print(f"Period: {CONFIG['start_date']} to {CONFIG['end_date']}")
    print(f"Initial Balance: ${CONFIG['initial_balance']}")
    print("="*80 + "\n")

    # Build configs
    configs = []
    for pair, info in MARKETS.items():
        strategies = STRATEGIES.get(info["type"], [])
        for tf in info["timeframes"]:
            for strat in strategies:
                configs.append({
                    "pair": pair,
                    "timeframe": tf,
                    "strategy": strat,
                })

    print(f"Total Configurations: {len(configs)}")
    print(f"Running with 4 workers...\n")

    # Run in parallel
    results = []
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run_backtest, cfg["pair"], cfg["timeframe"], cfg["strategy"]): cfg for cfg in configs}

        completed = 0
        for future in as_completed(futures):
            completed += 1
            metrics = future.result()
            if metrics and "error" not in metrics:
                results.append(metrics)
                print(f"[{completed}/{len(configs)}] SUCCESS")
            else:
                print(f"[{completed}/{len(configs)}] FAILED: {metrics.get('error', 'Unknown')[:60]}")

    # Generate report
    print("\n" + "="*80)
    print("DEBUG BACKTEST RESULTS")
    print("="*80)

    if results:
        print(f"\nSuccessful Backtests: {len(results)}")
        print("\nSTRATEGY RANKING:")
        print("-" * 80)

        strategy_summary = {}
        for r in results:
            s = r["strategy"]
            if s not in strategy_summary:
                strategy_summary[s] = {"wr": [], "pnl": []}
            strategy_summary[s]["wr"].append(r["win_rate"])
            strategy_summary[s]["pnl"].append(r["net_pnl"])

        for strat, data in sorted(strategy_summary.items(), key=lambda x: -sum(x[1]["wr"])/len(x[1]["wr"]) if x[1]["wr"] else 0):
            tests = len(data["wr"])
            avg_wr = sum(data["wr"]) / tests
            avg_pnl = sum(data["pnl"]) / tests
            print(f"{strat:<25} {tests:>6} {avg_wr:>6.1f}% ${avg_pnl:>9.2f}")

        # Best overall
        best = max(results, key=lambda x: x["win_rate"])
        print("\n" + "="*80)
        print("BEST STRATEGY:")
        print("="*80)
        print(f"Strategy: {best['strategy']}")
        print(f"Pair: {best['pair']}")
        print(f"Timeframe: {best['timeframe']}")
        print(f"Win Rate: {best['win_rate']:.1f}%")
        print(f"Net PNL: ${best['net_pnl']:.2f}")
    else:
        print("\nNo successful backtests!")

    print("\n" + "="*80)
    print("DEBUG COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
