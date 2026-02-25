#!/usr/bin/env python3
"""
VILONA BACKTEST - FIX PYTHONPATH

Menambahkan PYTHONPATH: skills/1ai-skills
"""

import sys
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Dapatkan workspace root
CWD = os.getcwd()

# Tambahkan PYTHONPATH: skills/1ai-skills
PYTHONPATHS = [
    os.path.join(CWD, "skills", "1ai-skills"),
    os.path.join(CWD, "skills"),
]

# Add to sys.path
for path in PYTHONPATHS:
    if path not in sys.path:
        sys.path.insert(0, path)

print(f"CWD: {CWD}")
print(f"PYTHONPATH: {sys.path[0]}")
print(f"PYTHONPATH[1]: {sys.path[1] if len(sys.path) > 1 else ''}")
print()

# Import test
try:
    from trading.brokers.base import OHLCV, BrokerType
    print(f"✅ Import SUCCESS: trading.brokers.base.OHLCV")
    print(f"✅ Import SUCCESS: trading.brokers.base.BrokerType")
except Exception as e:
    print(f"❌ Import FAILED: {e}")

# Config
CONFIG = {
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "initial_balance": 100.0,
}

# Strategies
STRATEGIES = [
    ("XAUUSD", "H1", "1ai-skills/trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "H4", "1ai-skills/trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("GBPUSD", "H1", "1ai-skills/trading/strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "H4", "1ai-skills/trading/strategy/templates/forex/holy_grail.py"),
    ("EURUSD", "H1", "1ai-skills/trading/strategy/templates/forex/holy_grail.py"),
]

def run_backtest(pair, tf, script):
    """Run backtest dengan PYTHONPATH yang benar."""
    cmd = ["python3", script, "backtest", CONFIG["start_date"], CONFIG["end_date"], "--initial-balance", "100"]

    print(f"[{pair} {tf}] Running...")

    # Run dari workspace root
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(PYTHONPATHS)

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, env=env)

    if result.returncode != 0:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": result.stderr[:100]}

    # Parse output
    output = result.stdout
    metrics = {"pair": pair, "tf": tf, "status": "OK"}

    for line in output.split('\n'):
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
        elif "Wins:" in line: metrics["wins"] = int(line.split(":")[1].strip())
        elif "Losses:" in line: metrics["losses"] = int(line.split(":")[1].strip())

    if "wr" in metrics:
        print(f"[{pair} {tf}] WR: {metrics['wr']:.1f}% PNL: ${metrics['pnl']:.2f}")

    return metrics

print("="*80)
print("VILONA BACKTEST - PYTHONPATH FIXED")
print("="*80)
print()

# Run tests
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
            print(f"[{completed}/{len(STRATEGIES)}] FAILED")

# Generate report
print("\n" + "="*80)
print("RESULTS")
print("="*80)

if results:
    # Strategy summary
    strategy_summary = {}
    for r in results:
        s = r.get("script", "unknown").split("/")[-1].replace(".py", "")
        if s not in strategy_summary:
            strategy_summary[s] = {"wr": [], "pnl": [], "dd": []}
        strategy_summary[s]["wr"].append(r["wr"])
        strategy_summary[s]["pnl"].append(r["pnl"])
        strategy_summary[s]["dd"].append(r.get("dd", 0))

    print("\nSTRATEGY RANKING:")
    print("-"*80)
    for strat, data in sorted(strategy_summary.items(), key=lambda x: -sum(x[1]["wr"])/len(x[1]["wr"]) if x[1]["wr"] else 0):
        tests = len(data["wr"])
        avg_wr = sum(data["wr"]) / tests
        avg_pnl = sum(data["pnl"]) / tests
        print(f"{strat:<30} {tests:>6} {avg_wr:>7.1f}% ${avg_pnl:>9.2f}")

    # Best overall
    best = max(results, key=lambda x: x["wr"])
    print("\n" + "="*80)
    print("BEST OVERALL:")
    print("="*80)
    print(f"Strategy: {best.get('script', 'unknown').split('/')[-1].replace('.py', '')}")
    print(f"Pair: {best['pair']}")
    print(f"Timeframe: {best['tf']}")
    print(f"Win Rate: {best['wr']:.1f}%")
    print(f"Net PNL: ${best['pnl']:.2f}")
    print(f"Profit Factor: {best.get('pf', 0):.2f}")
    print(f"Max Drawdown: ${best.get('dd', 0):.2f} ({best.get('dd_pct', 0):.1f}%)")
    print(f"Total Trades: {best['trades']}")
    print(f"Balance: ${best['balance']:.2f}")

else:
    print("\nNo successful backtests!")

print("\n" + "="*80)
