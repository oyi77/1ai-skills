#!/usr/bin/env python3
"""
Simple backtest runner - FIX FOR PYTHONPATH
"""

import sys
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Trading directory - absolute
TRADING_DIR = r"/home/openclaw/C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading"

# Change to trading directory
os.chdir(TRADING_DIR)

# Add to path
sys.path.insert(0, TRADING_DIR)

print(f"Working directory: {os.getcwd()}")
print(f"Python path: {sys.path[0]}")
print()

# Simple test for each strategy
STRATEGIES_TO_TEST = [
    ("XAUUSD", "H1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "H4", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "D1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("GBPUSD", "H1", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "H4", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "D1", "strategy/templates/forex/holy_grail.py"),
]

def run_backtest(pair, tf, script):
    """Run single backtest."""
    cmd = ["python3", script, "backtest", "2025-01-01", "2025-12-31", "--initial-balance", "100"]

    print(f"[{pair} {tf}] Running...")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

    if result.returncode != 0:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": result.stderr[:100]}

    # Parse basic output
    output = result.stdout
    metrics = {"pair": pair, "tf": tf, "status": "OK"}

    for line in output.split('\n'):
        if "Win Rate:" in line: metrics["wr"] = float(line.split(":")[1].strip().replace("%", ""))
        elif "Total Trades:" in line: metrics["trades"] = int(line.split(":")[1].strip())
        elif "Net PNL:" in line and "$" in line: metrics["pnl"] = float(line.split(":")[1].strip().replace("$", ""))

    if "wr" in metrics:
        print(f"[{pair} {tf}] SUCCESS: {metrics['wr']:.1f}% WR, ${metrics.get('pnl', 0):.2f} PNL")

    return metrics

# Run tests
print("="*80)
print("SIMPLE BACKTEST RUNNER")
print("="*80)
print()

results = []
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(run_backtest, p, t, s): (p, t, s) for p, t, s in STRATEGIES_TO_TEST}

    for future in as_completed(futures):
        result = future.result()
        if result:
            results.append(result)

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

successful = [r for r in results if r["status"] == "OK"]
failed = [r for r in results if r["status"] == "FAILED"]

print(f"\nSuccessful: {len(successful)}")
print(f"Failed: {len(failed)}")

if successful:
    print("\nWINNERS (by win rate):")
    print("-"*80)
    for r in sorted(successful, key=lambda x: -x.get("wr", 0)):
        print(f"{r['pair']} {r['tf']:>3} WR: {r['wr']:>5.1f}% PNL: ${r.get('pnl', 0):>7.2f}")

print("\n" + "="*80)
