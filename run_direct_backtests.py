#!/usr/bin/env python3
"""
VILONA DIRECT BACKTEST RUNNER

Menjalankan semua strategi secara langsung tanpa trading framework.
Gunakan path yang sudah terbukti bekerja (XAUUSD Asia 7-Candle).
"""

import sys
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Path strategi yang sudah terbukti bekerja
XAUUSD_ASIA_7C = "skills/1ai-skills/trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"

# Strategi lain yang mau diuji
STRATEGIES_TO_TEST = [
    # Forex
    ("GBPUSD", "H1", "skills/1ai-skills/trading/strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "H4", "skills/1ai-skills/trading/strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "D1", "skills/1ai-skills/trading/strategy/templates/forex/holy_grail.py"),
    ("EURUSD", "H1", "skills/1ai-skills/trading/strategy/templates/forex/holy_grail.py"),
    ("EURUSD", "H4", "skills/1ai-skills/trading/strategy/templates/forex/holy_grail.py"),
    ("EURUSD", "D1", "skills/1ai-skills/trading/strategy/templates/forex/holy_grail.py"),
    ("USDJPY", "H1", "skills/1ai-skills/trading/strategy/templates/forex/holy_grail.py"),
    ("USDJPY", "H4", "skills/1ai-skills/trading/strategy/templates/forex/holy_grail.py"),
    ("USDJPY", "D1", "skills/1ai-skills/trading/strategy/templates/forex/holy_grail.py"),
    # More Forex
    ("GBPUSD", "H1", "skills/1ai-skills/trading/strategy/templates/forex/momentum_elder.py"),
    ("GBPUSD", "H4", "skills/1ai-skills/trading/strategy/templates/forex/momentum_elder.py"),
    ("GBPUSD", "D1", "skills/1ai-skills/trading/strategy/templates/forex/momentum_elder.py"),
    ("EURUSD", "H1", "skills/1ai-skills/trading/strategy/templates/forex/momentum_elder.py"),
    ("EURUSD", "H4", "skills/1ai-skills/trading/strategy/templates/forex/momentum_elder.py"),
    ("EURUSD", "D1", "skills/1ai-skills/trading/strategy/templates/forex/momentum_elder.py"),
    ("USDJPY", "H1", "skills/1ai-skills/trading/strategy/templates/forex/momentum_elder.py"),
    ("USDJPY", "H4", "skills/1ai-skills/trading/strategy/templates/forex/momentum_elder.py"),
    ("USDJPY", "D1", "skills/1ai-skills/trading/strategy/templates/forex/momentum_elder.py"),
    # Kumo
    ("GBPUSD", "H1", "skills/1ai-skills/trading/strategy/templates/forex/kumo_breakout.py"),
    ("GBPUSD", "H4", "skills/1ai-skills/trading/strategy/templates/forex/kumo_breakout.py"),
    ("GBPUSD", "D1", "skills/1ai-skills/trading/strategy/templates/forex/kumo_breakout.py"),
    ("EURUSD", "H1", "skills/1ai-skills/trading/strategy/templates/forex/kumo_breakout.py"),
    ("EURUSD", "H4", "skills/1ai-skills/trading/strategy/templates/forex/kumo_breakout.py"),
    ("EURUSD", "D1", "skills/1ai-skills/trading/strategy/templates/forex/kumo_breakout.py"),
    ("USDJPY", "H1", "skills/1ai-skills/trading/strategy/templates/forex/kumo_breakout.py"),
    ("USDJPY", "H4", "skills/1ai-skills/trading/strategy/templates/forex/kumo_breakout.py"),
    ("USDJPY", "D1", "skills/1ai-skills/trading/strategy/templates/forex/kumo_breakout.py"),
    # Crypto
    ("BTCUSDT", "1h", "skills/1ai-skills/trading/strategy/templates/crypto/volume_momentum.py"),
    ("BTCUSDT", "4h", "skills/1ai-skills/trading/strategy/templates/crypto/volume_momentum.py"),
    ("BTCUSDT", "1d", "skills/1ai-skills/trading/strategy/templates/crypto/volume_momentum.py"),
    ("ETHUSDT", "1h", "skills/1ai-skills/trading/strategy/templates/crypto/volume_momentum.py"),
    ("ETHUSDT", "4h", "skills/1ai-skills/trading/strategy/templates/crypto/volume_momentum.py"),
    ("ETHUSDT", "1d", "skills/1ai-skills/trading/strategy/templates/crypto/volume_momentum.py"),
    ("SOLUSDT", "1h", "skills/1ai-skills/trading/strategy/templates/crypto/volume_momentum.py"),
    ("SOLUSDT", "4h", "skills/1ai-skills/trading/strategy/templates/crypto/volume_momentum.py"),
    ("SOLUSDT", "1d", "skills/1ai-skills/trading/strategy/templates/crypto/volume_momentum.py"),
]

CONFIG = {
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "initial_balance": 100.0,
}

def run_backtest(pair, tf, script):
    """Run single backtest."""
    cmd = ["python3", script, "backtest", CONFIG["start_date"], CONFIG["end_date"], "--initial-balance", "100"]

    print(f"[{pair} {tf}] Running...")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

    if result.returncode != 0:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": result.stderr[:100]}

    # Parse output
    output = result.stdout
    metrics = {"pair": pair, "tf": tf, "status": "OK"}

    for line in output.split('\n'):
        if "Win Rate:" in line: metrics["wr"] = float(line.split(":")[1].strip().replace("%", ""))
        elif "Total Trades:" in line: metrics["trades"] = int(line.split(":")[1].strip())
        elif "Wins:" in line: metrics["wins"] = int(line.split(":")[1].strip())
        elif "Losses:" in line: metrics["losses"] = int(line.split(":")[1].strip())
        elif "Net PNL:" in line and "$" in line: metrics["pnl"] = float(line.split(":")[1].strip().replace("$", ""))
        elif "Profit Factor:" in line: metrics["pf"] = float(line.split(":")[1].strip())
        elif "Gross Profit:" in line and "$" in line: metrics["gp"] = float(line.split(":")[1].strip().replace("$", ""))
        elif "Gross Loss:" in line and "$" in line: metrics["gl"] = float(line.split(":")[1].strip().replace("$", ""))
        elif "Max Drawdown:" in line:
            dd = line.split(":")[1].strip()
            if "(" in dd:
                metrics["dd"] = float(dd.split("$")[1].split("(")[0].strip())
                metrics["dd_pct"] = float(dd.split("(")[1].replace("%", "").replace(")", ""))

    if "wr" in metrics:
        print(f"[{pair} {tf}] SUCCESS: {metrics['wr']:.1f}% WR, ${metrics['pnl']:.2f} PNL")

    return metrics

print("\n" + "="*80)
print("VILONA DIRECT BACKTEST RUNNER - NO FRAMEWORK DEPENDENCIES")
print("="*80)
print(f"Period: {CONFIG['start_date']} to {CONFIG['end_date']}")
print(f"Total tests: {len(STRATEGIES_TO_TEST)}")
print(f"Workers: 4")
print("="*80)
print()

results = []
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(run_backtest, p, t, s): (p, t, s) for (p, t, s) in STRATEGIES_TO_TEST}

    completed = 0
    for future in as_completed(futures):
        completed += 1
        result = future.result()
        if result and result["status"] == "OK":
            results.append(result)
            print(f"[{completed}/{len(STRATEGIES_TO_TEST)}] SUCCESS")
        else:
            print(f"[{completed}/{len(STRATEGIES_TO_TEST)}] FAILED")

# Generate report
print("\n" + "="*80)
print("FINAL RESULTS")
print("="*80)

if results:
    # Strategy summary
    strategy_summary = {}
    for r in results:
        s = r["script"].split("/")[-1].replace(".py", "").replace("_", " ").title()
        if s not in strategy_summary:
            strategy_summary[s] = {"wr": [], "pnl": [], "dd": [], "trades": []}
        strategy_summary[s]["wr"].append(r["wr"])
        strategy_summary[s]["pnl"].append(r["pnl"])
        strategy_summary[s]["dd"].append(r.get("dd", 0))
        strategy_summary[s]["trades"].append(r["trades"])

    print("\nSTRATEGY RANKING (by average win rate):")
    print("-"*80)
    print(f"{'Strategy':<30} {'Tests':>6} {'Avg WR':>8} {'Avg PNL':>10} {'Best Pair':<12}")
    print("-"*80)

    for strat, data in sorted(strategy_summary.items(), key=lambda x: -sum(x[1]["wr"])/len(x[1]["wr"]) if x[1]["wr"] else 0):
        tests = len(data["wr"])
        avg_wr = sum(data["wr"]) / tests
        avg_pnl = sum(data["pnl"]) / tests
        avg_dd = max(data["dd"]) if data["dd"] else 0

        # Find best config
        best_idx = data["pnl"].index(max(data["pnl"]))
        best_pair = results[best_idx]["pair"] if best_idx < len(results) else "N/A"

        print(f"{strat:<30} {tests:>6} {avg_wr:>7.1f}% ${avg_pnl:>9.2f} {best_pair:<12}")

    # Overall best
    best = max(results, key=lambda x: x.get("wr", 0))
    print("\n" + "="*80)
    print("OVERALL WINNER")
    print("="*80)
    print(f"Strategy: {best['script'].split('/')[-1].replace('.py', '').replace('_', ' ').title()}")
    print(f"Pair: {best['pair']}")
    print(f"Timeframe: {best['tf']}")
    print(f"Win Rate: {best['wr']:.1f}%")
    print(f"Net PNL: ${best['pnl']:.2f}")
    print(f"Profit Factor: {best.get('pf', 0):.2f}")
    print(f"Max Drawdown: ${best.get('dd', 0):.2f} ({best.get('dd_pct', 0):.1f}%)")
    print(f"Total Trades: {best['trades']}")
    print(f"Balance: ${100 + best['pnl']:.2f}")

    # Save results
    import json
    from datetime import datetime

    report = {
        "config": CONFIG,
        "results": results,
        "strategy_summary": {strat: {
            "avg_win_rate": sum(d["wr"]) / len(d["wr"]),
            "avg_net_pnl": sum(d["pnl"]) / len(d["pnl"]),
            "avg_max_drawdown": max(d["dd"]) if d["dd"] else 0,
            "total_tests": len(d["wr"]),
        } for strat, d in strategy_summary.items()
        },
        "best_overall": best,
        "timestamp": datetime.now().isoformat()
    }

    with open("backtest_all_strategies_direct.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[SAVED] backtest_all_strategies_direct.json")

else:
    print("\nNo successful backtests!")

print("\n" + "="*80)
print("VILONA DIRECT BACKTEST COMPLETE")
print("="*80)
