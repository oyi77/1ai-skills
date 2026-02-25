#!/usr/bin/env python3
"""
VILONA BACKTEST - PATH ESCAPE FIX
"""

import sys
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Escape backslashes - replace with forward slashes
ORIGINAL_PATH = r"/home/openclaw/C:\Users\EX PC\.openclaw\workspace/skills\1ai-skills\trading"
TRADING_PATH = ORIGINAL_PATH.replace("\\", "/")

print(f"ORIGINAL: {ORIGINAL_PATH}")
print(f"FIXED: {TRADING_PATH}")
print(f"EXISTS: {os.path.exists(TRADING_PATH)}")
print()

# Add to path
sys.path.insert(0, TRADING_PATH)

# Change dir if exists
if os.path.exists(TRADING_PATH):
    os.chdir(TRADING_PATH)
    print(f"Working dir: {os.getcwd()}")
else:
    print("Trading path does not exist!")
    sys.exit(1)

print()

# Simple test list
TESTS = [
    ("XAUUSD", "H1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "H4", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("GBPUSD", "H1", "strategy/templates/forex/holy_grail.py"),
]

def run_test(pair, tf, script):
    cmd = ["python3", script, "backtest", "2025-01-01", "2025-12-31", "--initial-balance", "100"]

    print(f"[TEST] {pair} {tf} {script}")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

    if result.returncode != 0:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": result.stderr[:50]}

    metrics = {"pair": pair, "tf": tf, "status": "OK"}
    for line in result.stdout.split('\n'):
        if "Win Rate:" in line: metrics["wr"] = float(line.split(":")[1].strip().replace("%", ""))
        elif "Net PNL:" in line and "$" in line:
            metrics["pnl"] = float(line.split(":")[1].strip().replace("$", ""))

    return metrics

print("="*80)
print("VILONA BACKTEST - ESCAPED PATH")
print("="*80)
print(f"Total tests: {len(TESTS)}")
print(f"Workers: 4")
print("="*80)
print()

results = []
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(run_test, p, t, s): (p, t, s) for p, t, s in TESTS}

    completed = 0
    for future in as_completed(futures):
        completed += 1
        result = future.result()
        if result and result["status"] == "OK":
            results.append(result)
            print(f"[{completed}/{len(TESTS)}] {result['pair']} {result['tf']} WR: {result['wr']:.1f}% PNL: ${result['pnl']:.2f}")
        else:
            print(f"[{completed}/{len(TESTS)}] FAILED")

print("\n" + "="*80)
print("RESULTS")
print("="*80)

if results:
    print(f"Successful: {len(results)}")
    print("\nTOP 3 (by win rate):")
    for r in sorted(results, key=lambda x: -x.get("wr", 0))[:3]:
        print(f"  {r['pair']} {r['tf']:>3} WR: {r['wr']:>5.1f}% PNL: ${r['pnl']:>7.2f}")

print("\n" + "="*80)
