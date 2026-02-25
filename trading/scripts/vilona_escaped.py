#!/usr/bin/env python3
"""
VILONA BACKTEST - Cross-platform path handling
"""

import sys
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Auto-detect trading directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRADING_PATH = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))

print(f"TRADING_PATH: {TRADING_PATH}")
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

print()

STRATEGIES_TO_TEST = [
    (
        "XAUUSD",
        "H1",
        "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py",
    ),
    (
        "XAUUSD",
        "H4",
        "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py",
    ),
    (
        "XAUUSD",
        "D1",
        "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py",
    ),
    ("GBPUSD", "H1", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "H4", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "D1", "strategy/templates/forex/holy_grail.py"),
]


def run_backtest(pair, tf, script):
    """Run backtest."""
    cmd = [
        "python3",
        script,
        "backtest",
        "2025-01-01",
        "2025-12-31",
        "--initial-balance",
        "100",
    ]

    print(f"[{pair} {tf}] Running {script}...")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

    if result.returncode != 0:
        return {
            "pair": pair,
            "tf": tf,
            "status": "FAILED",
            "error": result.stderr[:100],
        }

    # Parse
    metrics = {"pair": pair, "tf": tf, "status": "OK"}
    for line in result.stdout.split("\n"):
        if "Win Rate:" in line:
            metrics["wr"] = float(line.split(":")[1].strip().replace("%", ""))
        elif "Net PNL:" in line and "$" in line:
            metrics["pnl"] = float(line.split(":")[1].strip().replace("$", ""))

    if "wr" in metrics:
        print(
            f"[{pair} {tf}] SUCCESS: {metrics['wr']:.1f}% WR, ${metrics.get('pnl', 0):.2f} PNL"
        )

    return metrics


print("=" * 80)
print("VILONA BACKTEST - CROSS-PLATFORM MODE")
print("=" * 80)
print()

results = []
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {
        executor.submit(run_backtest, p, t, s): (p, t, s)
        for p, t, s in STRATEGIES_TO_TEST
    }

    for future in as_completed(futures):
        result = future.result()
        if result and result["status"] == "OK":
            results.append(result)

print("\n" + "=" * 80)
print("RESULTS")
print("=" * 80)

if results:
    print(f"Successful: {len(results)}")
    print("\nSTRATEGY PERFORMANCE:")
    print("-" * 80)
    for r in sorted(results, key=lambda x: -x.get("wr", 0)):
        print(
            f"{r['pair']:<8} {r['tf']:>3} WR: {r['wr']:>5.1f}% PNL: ${r.get('pnl', 0):>7.2f}"
        )

    best = max(results, key=lambda x: x.get("wr", 0))
    print("\nBEST:")
    print(f"Pair: {best['pair']}")
    print(f"TF: {best['tf']}")
    print(f"WR: {best['wr']:.1f}%")
    print(f"PNL: ${best.get('pnl', 0):.2f}")

print("\n" + "=" * 80)
