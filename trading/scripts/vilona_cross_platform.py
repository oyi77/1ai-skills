#!/usr/bin/env python3
"""
FINAL CROSS-PLATFORM BACKTEST RUNNER

Uses relative paths - no more backslash issues!
"""

import sys
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Script dir: {SCRIPT_DIR}")

# TRADING_BASE is parent of scripts/
TRADING_BASE = os.path.dirname(SCRIPT_DIR)
print(f"Trading base: {TRADING_BASE}")

# Add to Python path
sys.path.insert(0, TRADING_BASE)

# Strategies to test
TESTS = [
    ("XAUUSD", "H1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "H4", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "D1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("GBPUSD", "H1", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "H4", "strategy/templates/forex/holy_grail.py"),
]

def run_backtest(pair, tf, script):
    """Run backtest."""
    cmd = ["python3", script, "backtest", "2025-01-01", "2025-12-31", "--initial-balance", "100"]

    print(f"[{pair} {tf}] Running...")

    # Run from TRADING_BASE
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=3600,
        cwd=TRADING_BASE
    )

    if result.returncode != 0:
        return {"pair": pair, "tf": tf, "status": "FAILED"}

    # Parse output
    metrics = {"pair": pair, "tf": tf, "status": "OK"}
    for line in result.stdout.split('\n'):
        if "Win Rate:" in line: metrics["wr"] = float(line.split(":")[1].strip().replace("%", ""))
        elif "Net PNL:" in line and "$" in line: metrics["pnl"] = float(line.split(":")[1].strip().replace("$", ""))

    if "wr" in metrics:
        print(f"[{pair} {tf}] WR: {metrics['wr']:.1f}% PNL: ${metrics.get('pnl', 0):.2f}")

    return metrics

# Run tests
print("="*80)
print("VILONA CROSS-PLATFORM BACKTEST")
print("="*80)
print()

results = []
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(run_backtest, p, t, s): (p, t, s) for p, t, s in TESTS}

    for future in as_completed(futures):
        result = future.result()
        if result and result["status"] == "OK":
            results.append(result)

print("\n" + "="*80)
print("RESULTS")
print("="*80)

if results:
    print(f"\nSuccessful: {len(results)}")
    print("\nRANKED (by win rate):")
    for r in sorted(results, key=lambda x: -x.get("wr", 0)):
        print(f"  {r['pair']:>7} {r['tf']:>3} WR: {r['wr']:>5.1f}% PNL: ${r.get('pnl', 0):>7.2f}")

    best = max(results, key=lambda x: x.get("wr", 0))
    print("\nBEST:")
    print(f"  {best['pair']} {best['tf']}")
    print(f"  WR: {best['wr']:.1f}% PNL: ${best.get('pnl', 0):.2f}")
else:
    print("No successful backtests!")

print("\n" + "="*80)
