#!/usr/bin/env python3
"""
VILONA FINAL BACKTEST RUNNER - FIX PYTHONPATH

Menjalankan dari ROOT trading package agar imports bekerja.
Working dir: skills/trading/ (di sini trading package bisa ditemukan)
"""

import sys
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Dapatkan script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Trading ROOT adalah parent dari scripts/ (jadi skills/trading/)
TRADING_ROOT = os.path.dirname(SCRIPT_DIR)

print(f"SCRIPT_DIR: {SCRIPT_DIR}")
print(f"TRADING_ROOT: {TRADING_ROOT}")
print(f"TRADING_ROOT exists: {os.path.exists(TRADING_ROOT)}")
print()

# Add TRADING_ROOT ke Python path
sys.path.insert(0, TRADING_ROOT)

# Import test - sekarang harus bisa
try:
    from trading.brokers.base import BrokerType, OHLCV
    print(f"✅ Import SUCCESS: trading.brokers.base.{BrokerType.__name__}")
    print(f"✅ OHLCV class imported")
except Exception as e:
    print(f"❌ Import FAILED: {e}")
    sys.exit(1)

# Config
CONFIG = {
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "initial_balance": 100.0,
}

# Strategies to test
STRATEGIES = [
    ("XAUUSD", "H1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "H4", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "D1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("GBPUSD", "H1", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "H4", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "D1", "strategy/templates/forex/holy_grail.py"),
    ("USDJPY", "H1", "strategy/templates/forex/holy_grail.py"),
    ("USDJPY", "H4", "strategy/templates/forex/holy_grail.py"),
    ("USDJPY", "D1", "strategy/templates/forex/holy_grail.py"),
]

def run_backtest(pair, tf, script):
    """Run backtest dari TRADING_ROOT (path relatif bekerja)."""
    cmd = ["python3", script, "backtest", CONFIG["start_date"], CONFIG["end_date"], "--initial-balance", "100"]

    print(f"[{pair} {tf}] Running: {script}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=3600,
        cwd=TRADING_ROOT  # Jalankan dari ROOT trading!
    )

    if result.returncode != 0:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": result.stderr[:100]}

    # Parse output
    metrics = {"pair": pair, "tf": tf, "status": "OK"}
    for line in result.stdout.split('\n'):
        if "Win Rate:" in line: metrics["wr"] = float(line.split(":")[1].strip().replace("%", ""))
        elif "Total Trades:" in line: metrics["trades"] = int(line.split(":")[1].strip())
        elif "Net PNL:" in line and "$" in line:
            metrics["pnl"] = float(line.split(":")[1].strip().replace("$", ""))
            metrics["balance"] = 100 + metrics["pnl"]
        elif "Profit Factor:" in line: metrics["pf"] = float(line.split(":")[1].strip())
        elif "Gross Profit:" in line and "$" in line: metrics["gp"] = float(line.split(":")[1].strip().replace("$", ""))
        elif "Gross Loss:" in line and "$" in line: metrics["gl"] = float(line.split(":")[1].strip().replace("$", ""))
        elif "Max Drawdown:" in line:
            dd = line.split(":")[1].strip()
            if "(" in dd:
                metrics["dd"] = float(dd.split("$")[1].split("(")[0].strip())
                metrics["dd_pct"] = float(dd.split("(")[1].replace("%", "").replace(")", ""))

    if "wr" in metrics:
        print(f"[{pair} {tf}] WR: {metrics['wr']:.1f}% PNL: ${metrics['pnl']:.2f} PF: {metrics['pf']:.2f}")

    return metrics

# Run tests
print("="*80)
print("VILONA FINAL BACKTEST - PYTHONPATH FIXED")
print("="*80)
print(f"PYTHONPATH: {TRADING_ROOT}")
print(f"Working dir: {TRADING_ROOT}")
print(f"Total configs: {len(STRATEGIES)}")
print(f"Workers: 4")
print("="*80)
print()

results = []
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(run_backtest, p, t, s): (p, t, s) for (p, t, s) in STRATEGIES}

    completed = 0
    for future in as_completed(futures):
        completed += 1
        result = future.result()
        if result and result["status"] == "OK":
            results.append(result)
            print(f"[{completed}/{len(STRATEGIES)}] SUCCESS")
        else:
            print(f"[{completed}/{len(STRATEGIES)}] FAILED: {result.get('error', 'Unknown')}")

# Generate comprehensive report
print("\n" + "="*80)
print("FINAL RESULTS")
print("="*80)

if results:
    # Strategy summary
    strategy_summary = {}
    for r in results:
        s = r.get("script", "unknown").split("/")[-2].replace(".py", "")
        if s not in strategy_summary:
            strategy_summary[s] = {"wr": [], "pnl": [], "dd": [], "trades": []}
        strategy_summary[s]["wr"].append(r["wr"])
        strategy_summary[s]["pnl"].append(r["pnl"])
        strategy_summary[s]["dd"].append(r.get("dd", 0))
        strategy_summary[s]["trades"].append(r["trades"])

    print(f"\nSTRATEGY PERFORMANCE (by average win rate):")
    print("-"*80)
    print(f"{'Strategy':<25} {'Tests':>6} {'Avg WR':>8} {'Avg PNL':>10} {'Max DD':>10} {'Best Pair':>10}")
    print("-"*80)

    for strat, data in sorted(strategy_summary.items(), key=lambda x: -sum(x[1]["wr"])/len(x[1]["wr"]) if x[1]["wr"] else 0):
        tests = len(data["wr"])
        avg_wr = sum(data["wr"]) / tests
        avg_pnl = sum(data["pnl"]) / tests
        avg_dd = max(data["dd"]) if data["dd"] else 0

        # Find best config
        best_pnl = max(data["pnl"])
        best_idx = data["pnl"].index(best_pnl)

        print(f"{strat:<25} {tests:>6} {avg_wr:>7.1f}% ${avg_pnl:>9.2f} ${avg_dd:>9.2f} {results[best_idx]['pair']:>10}")

    # Overall best
    best = max(results, key=lambda x: x.get("wr", 0))
    print(f"\n{'='*80}")
    print("OVERALL WINNER")
    print(f"{'='*80}")
    print(f"Pair: {best['pair']}")
    print(f"Timeframe: {best['tf']}")
    print(f"Script: {best.get('script', 'N/A')}")
    print(f"Win Rate: {best['wr']:.1f}%")
    print(f"Net PNL: ${best['pnl']:.2f}")
    print(f"Profit Factor: {best.get('pf', 'N/A')}")
    print(f"Max Drawdown: ${best.get('dd', 'N/A'):.2f} ({best.get('dd_pct', 'N/A'):.1f}%)")
    print(f"Total Trades: {best['trades']}")
    print(f"Balance: ${best.get('balance', 'N/A'):.2f}")

    # Save report
    import json
    from datetime import datetime

    report = {
        "config": CONFIG,
        "pythonpath": TRADING_ROOT,
        "results": results,
        "strategy_summary": {strat: {
            "avg_win_rate": sum(data["wr"]) / len(data["wr"]),
            "avg_net_pnl": sum(data["pnl"]) / len(data["pnl"]),
            "avg_max_drawdown": max(data["dd"]) if data["dd"] else 0,
            "total_trades": sum(data["trades"]),
        } for strat, data in strategy_summary.items()
        },
        "best_overall": best,
        "timestamp": datetime.now().isoformat()
    }

    report_path = os.path.join(TRADING_ROOT, "backtest_final_comprehensive.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[SAVED] {report_path}")

else:
    print("\nNo successful backtests!")

print("\n" + "="*80)
print("VILONA BACKTEST COMPLETE")
print("="*80)
