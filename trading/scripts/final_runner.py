#!/usr/bin/env python3
"""
FINAL FIXED BACKTEST RUNNER - CORRECT PATHS

Working directory structure:
/home/openclaw/C:\Users\EX PC\.openclaw\workspace/skills/1ai-skills/trading
"""

import sys
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Get current directory and build correct path
CWD = os.getcwd()
# 1ai-skills is a subdirectory under skills/
# So the trading base would be skills/1ai-skills/trading
# But we're running from workspace root
# Let me check if we're running from skills/ or workspace/
if "1ai-skills" in CWD or "trading" in CWD:
    # We're in the right place
    TRADING_BASE = CWD
else:
    # We're in workspace root, need to go to skills/1ai-skills/trading
    TRADING_BASE = os.path.join(CWD, "skills", "1ai-skills", "trading")

print(f"CWD: {CWD}")
print(f"TRADING_BASE: {TRADING_BASE}")
print(f"TRADING_BASE exists: {os.path.exists(TRADING_BASE)}")
print()

# Add to path
sys.path.insert(0, TRADING_BASE)

# Change to trading directory
os.chdir(TRADING_BASE)

STRATEGIES_TO_TEST = [
    ("XAUUSD", "H1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "H4", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "D1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("GBPUSD", "H1", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "H4", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "D1", "strategy/templates/forex/holy_grail.py"),
]

def run_backtest(pair, tf, script):
    """Run backtest."""
    cmd = ["python3", script, "backtest", "2025-01-01", "2025-12-31", "--initial-balance", "100"]

    print(f"[{pair} {tf}] Running...")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, cwd=TRADING_BASE)

    if result.returncode != 0:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": result.stderr[:100]}

    # Parse output
    metrics = {"pair": pair, "tf": tf, "status": "OK"}
    for line in result.stdout.split('\n'):
        if "Win Rate:" in line: metrics["wr"] = float(line.split(":")[1].strip().replace("%", ""))
        elif "Total Trades:" in line: metrics["trades"] = int(line.split(":")[1].strip())
        elif "Net PNL:" in line and "$" in line: metrics["pnl"] = float(line.split(":")[1].strip().replace("$", ""))

    if "wr" in metrics:
        print(f"[{pair} {tf}] SUCCESS: {metrics['wr']:.1f}% WR, ${metrics.get('pnl', 0):.2f} PNL")

    return metrics

print("="*80)
print("FINAL BACKTEST RUNNER - CORRECT PATHS")
print("="*80)

results = []
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(run_backtest, p, t, s): (p, t, s) for p, t, s in STRATEGIES_TO_TEST}

    completed = 0
    for future in as_completed(futures):
        completed += 1
        result = future.result()
        if result and result["status"] == "OK":
            results.append(result)
        print(f"[{completed}/{len(STRATEGIES_TO_TEST)}] Complete")

print("\n" + "="*80)
print("RESULTS")
print("="*80)

if results:
    print("\nWINNERS (by win rate):")
    print("-"*80)
    for r in sorted(results, key=lambda x: -x.get("wr", 0)):
        print(f"{r['pair']} {r['tf']:>3} WR: {r['wr']:>5.1f}% PNL: ${r.get('pnl', 0):>7.2f}")

    best = max(results, key=lambda x: x.get("wr", 0))
    print("\nBEST:")
    print(f"Strategy: Asia 7-Candle if pair == XAUUSD else Holy Grail")
    print(f"Pair: {best['pair']}")
    print(f"Timeframe: {best['tf']}")
    print(f"Win Rate: {best['wr']:.1f}%")
    print(f"PNL: ${best.get('pnl', 0):.2f}")
else:
    print("No successful backtests!")

print("\n" + "="*80)
