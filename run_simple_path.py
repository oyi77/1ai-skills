#!/usr/bin/env python3
"""
VILONA FINAL - PYTHONPATH FIX WITHOUT BACKSLASH
"""

import os
import subprocess
import json
from concurrent.futures import ProcessPoolExecutor, as_completed

# Python venv
VENV_PYTHON = os.path.expanduser('~/.trading-venv/bin/python')

# Working dir dengan backslash literal
CWD = os.getcwd()  # /home/openclaw/C:\Users\EX PC\.openclaw\workspace

# Trading dir - gunakan current directory karena sudah di skills/1ai-skills/trading
TRADING_DIR = os.getcwd()

# PYTHONPATH - gunakan TRADING_DIR saja
PYTHONPATH = TRADING_DIR

# Config
CONFIG = {
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "initial_balance": 100.0,
}

# Strategies
STRATEGIES = [
    ("XAUUSD", "H1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "H4", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "D1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
]

def run_backtest(pair, tf, script):
    """Run backtest."""
    script_path = os.path.normpath(os.path.join(TRADING_DIR, script))

    cmd = [VENV_PYTHON, script_path, "backtest", CONFIG["start_date"], CONFIG["end_date"], "--initial-balance", "100"]

    # Environment with PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = PYTHONPATH

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=3600,
        cwd=TRADING_DIR,
        env=env
    )

    if result.returncode != 0:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": result.stderr[:200]}

    # Parse JSON
    try:
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    data = json.loads(line)
                    if 'win_rate' in data:
                        return {
                            "pair": pair,
                            "tf": tf,
                            "status": "OK",
                            "script": script,
                            "wr": data.get("win_rate", 0),
                            "pnl": data.get("pnl", {}).get("usd", 0),
                            "balance": 100 + data.get("pnl", {}).get("usd", 0),
                            "trades": data.get("total_trades", 0),
                            "wins": data.get("wins", 0),
                            "losses": data.get("losses", 0),
                            "pf": data.get("profit_factor", 0),
                        }
                except:
                    continue
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": "No JSON found"}
    except Exception as e:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": f"JSON parse: {str(e)[:200]}"}

print("="*100)
print("VILONA FINAL - SIMPLE PYTHONPATH - BERKAHKARYA QUANT")
print("="*100)
print(f"PYTHONPATH: {PYTHONPATH}")
print(f"Working dir: {TRADING_DIR}")
print(f"Configs: {len(STRATEGIES)}")
print("="*100)
print()

results = []
with ProcessPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(run_backtest, p, t, s): (p, t, s) for (p, t, s) in STRATEGIES}

    completed = 0
    for future in as_completed(futures):
        completed += 1
        result = future.result()
        if result and result["status"] == "OK":
            results.append(result)
            print(f"[{completed}/{len(STRATEGIES)}] ✅ {result['pair']:>7} {result['tf']:>3} WR: {result['wr']:>5.1f}% PNL: ${result['pnl']:>7.2f}")
        else:
            print(f"[{completed}/{len(STRATEGIES)}] ❌ {result['pair']:>7} {result['tf']:>3}")

# Report
print("\n" + "="*100)
print("RESULTS")
print("="*100)

if results:
    for r in results:
        print(f"{r['pair']} {r['tf']} WR: {r['wr']:.1f}% PNL: ${r['pnl']:.2f}")

    best = max(results, key=lambda x: x["wr"])
    print(f"\n🏆 BEST: {best['pair']} {best['tf']}")
    print(f"   WR: {best['wr']:.1f}% | PNL: ${best['pnl']:.2f}")

    with open("berkahkarya_xauusd_only.json", "w") as f:
        json.dump({"results": results, "best": best}, f, indent=2)
    print(f"\n[📁 SAVED] berkahkarya_xauusd_only.json")
else:
    print("All failed")

print(f"\n{'='*100}")
