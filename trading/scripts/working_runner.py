#!/usr/bin/env python3
"""
WORKING BACKTEST RUNNER - Use known good paths

XAUUSD Asia 7-Candle backtest sebelumnya jalan
dengan path: 1ai-skills/trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py

Gunakan path relatif dari working directory.
"""

import sys
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Working directory
CWD = os.getcwd()
print(f"Working dir: {CWD}")

# Change to skills/trading (if we're in workspace)
if os.path.exists("skills/trading"):
    os.chdir("skills/trading")
elif os.path.exists("trading"):
    os.chdir("trading")
else:
    print("WARNING: Not in trading directory")

NEW_CWD = os.getcwd()
print(f"Changed to: {NEW_CWD}")
print()

# Now paths should be relative
TESTS = [
    ("XAUUSD", "H1", "1ai-skills/trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "H4", "1ai-skills/trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "D1", "1ai-skills/trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
]

def run_backtest(pair, tf, script):
    """Run backtest."""
    cmd = ["python3", script, "backtest", "2025-01-01", "2025-12-31", "--initial-balance", "100"]

    print(f"[{pair} {tf}] Running: {script}")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

    if result.returncode != 0:
        return {"pair": pair, "tf": tf, "status": "FAILED"}

    # Parse
    metrics = {"pair": pair, "tf": tf, "status": "OK"}
    for line in result.stdout.split('\n'):
        if "Win Rate:" in line: metrics["wr"] = float(line.split(":")[1].strip().replace("%", ""))
        elif "Net PNL:" in line and "$" in line:
            metrics["pnl"] = float(line.split(":")[1].strip().replace("$", ""))

    if "wr" in metrics:
        print(f"[{pair} {tf}] SUCCESS: {metrics['wr']:.1f}% WR, ${metrics['pnl']:.2f} PNL")

    return metrics

print("="*80)
print("WORKING BACKTEST RUNNER")
print("="*80)

results = []
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(run_backtest, p, t, s): (p, t, s) for p, t, s in TESTS}

    completed = 0
    for future in as_completed(futures):
        completed += 1
        result = future.result()
        if result and result["status"] == "OK":
            results.append(result)
            print(f"[{completed}/{len(TESTS)}] Complete")

print("\n" + "="*80)
print("RESULTS")
print("="*80)

if results:
    print(f"\nSuccessful: {len(results)}")
    print("\nRANKED:")
    print("-"*80)
    for r in sorted(results, key=lambda x: -x.get("wr", 0)):
        print(f"  {r['pair']:>7} {r['tf']:>3} WR: {r['wr']:>5.1f}% PNL: ${r.get('pnl', 0):>7.2f}")
else:
    print("No successful backtests!")

print("\n" + "="*80)
