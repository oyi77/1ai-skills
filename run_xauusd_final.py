#!/usr/bin/env python3
"""
VILONA FINAL - PATH FIX WITH OS.NORMPATH

Fix semua backslash issues dengan os.path.normpath()
"""

import sys
import os
import subprocess
import json
from concurrent.futures import ProcessPoolExecutor, as_completed

# Workspace directory
CWD = os.getcwd()
TRADING_DIR = os.path.join(CWD, "skills", "1ai-skills", "trading")

# Fix path with normpath
TRADING_DIR = os.path.normpath(TRADING_DIR)

# Config
CONFIG = {
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "initial_balance": 100.0,
}

# XAUUSD Asia 7-Candle (PROVEN - sudah test sukses)
XAUUSD_STRATEGIES = [
    ("XAUUSD", "H1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "H4", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "D1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
]

def run_backtest(pair, tf, script):
    """Run backtest dengan path yang normalized."""
    # Normalize path
    script_path = os.path.normpath(os.path.join(TRADING_DIR, script))

    cmd = ["python3", script_path, "backtest", CONFIG["start_date"], CONFIG["end_date"], "--initial-balance", "100"]

    print(f"[{pair} {tf}] Running: {script_path}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=3600,
        cwd=TRADING_DIR
    )

    if result.returncode != 0:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": result.stderr[:200]}

    # Parse JSON
    try:
        lines = result.stdout.split('\n')
        json_str = None

        for line in lines:
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    data = json.loads(line)
                    if 'win_rate' in data:
                        json_str = line
                        break
                except:
                    continue

        if not json_str:
            return {"pair": pair, "tf": tf, "status": "FAILED", "error": "No JSON found"}

        data = json.loads(json_str)

        metrics = {
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
            "gp": data.get("gross_profit", 0),
            "gl": data.get("gross_loss", 0),
            "avg_win": data.get("avg_win", {}).get("usd", 0),
            "avg_loss": data.get("avg_loss", {}).get("usd", 0),
        }

        print(f"[{pair} {tf}] WR: {metrics['wr']:.1f}% PNL: ${metrics['pnl']:.2f}")

        return metrics

    except Exception as e:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": f"JSON parse: {str(e)[:200]}"}

print("="*80)
print("VILONA FINAL BACKTEST - PATH NORMPATH FIX")
print("="*80)
print(f"Working dir: {TRADING_DIR}")
print(f"Configs: {len(XAUUSD_STRATEGIES)}")
print("="*80)
print()

results = []
with ProcessPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(run_backtest, p, t, s): (p, t, s) for (p, t, s) in XAUUSD_STRATEGIES}

    completed = 0
    for future in as_completed(futures):
        completed += 1
        result = future.result()
        if result and result["status"] == "OK":
            results.append(result)
            print(f"[{completed}/{len(XAUUSD_STRATEGIES)}] ✅")
        else:
            print(f"[{completed}/{len(XAUUSD_STRATEGIES)}] ❌")

# Report
print("\n" + "="*80)
print("XAUUSD ASIA 7-CANDLE BACKTEST RESULTS")
print("="*80)

if results:
    print(f"\n{'Pair':<10} {'TF':<6} {'WR':>8} {'PNL':>10} {'Trades':>8} {'Wins':>6} {'Losses':>7}")
    print("-"*80)

    for r in results:
        print(f"{r['pair']:<10} {r['tf']:<6} {r['wr']:>7.1f}% ${r['pnl']:>9.2f} {r['trades']:>8} {r['wins']:>6} {r['losses']:>7}")

    # Best
    best = max(results, key=lambda x: x["wr"])
    print("\n" + "="*80)
    print("🏆 BEST TIMEFRAME")
    print("="*80)
    print(f"Timeframe: {best['tf']}")
    print(f"Win Rate: {best['wr']:.1f}%")
    print(f"Net PNL: ${best['pnl']:.2f} (+{best['pnl']/100*100:.1f}%)")
    print(f"Profit Factor: {best['pf']:.2f}")
    print(f"Total Trades: {best['trades']}")
    print(f"Avg Win: ${best['avg_win']:.2f} | Avg Loss: ${best['avg_loss']:.2f}")
    print(f"Balance: ${best['balance']:.2f}")

    # Save
    report = {
        "strategy": "XAUUSD Asia 7-Candle Breakout",
        "period": CONFIG,
        "results": results,
        "best": best,
        "timestamp": "2026-02-23T02:41:00+07:00"
    }

    with open("xauusd_asia_7c_backtest.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[📁 SAVED] xauusd_asia_7c_backtest.json")

else:
    print("\n❌ All backtests failed!")

print(f"\n{'='*80}")
