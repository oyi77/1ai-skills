#!/usr/bin/env python3
"""
VILONA FINAL WITH PYTHONPATH FIX
Set PYTHONPATH agar trading package ditemukan
"""

import os
import subprocess
import json
from concurrent.futures import ProcessPoolExecutor, as_completed

# Python & paths
VENV_PYTHON = os.path.expanduser('~/.trading-venv/bin/python')
CWD = os.getcwd()
TRADING_DIR = os.path.join(CWD, 'skills', '1ai-skills', 'trading')
TRADING_DIR = os.path.normpath(TRADING_DIR)

# PYTHONPATH agar trading package ditemukan
PYTHONPATH = os.pathsep.join([
    TRADING_DIR,  # trading/__init__.py ada di sini
    os.path.dirname(TRADING_DIR),  # skills/1ai-skills
])

# Config
CONFIG = {
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "initial_balance": 100.0,
}

# Strategies (XAUUSD Asia 7-Candle sudah terbukti profitable)
STRATEGIES = [
    # XAUUSD
    ("XAUUSD", "H1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "H4", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "D1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),

    # GBPUSD Holy Grail
    ("GBPUSD", "H1", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "H4", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "D1", "strategy/templates/forex/holy_grail.py"),
]

def run_backtest(pair, tf, script):
    """Run backtest dengan PYTHONPATH."""
    script_path = os.path.normpath(os.path.join(TRADING_DIR, script))

    cmd = [VENV_PYTHON, script_path, "backtest", CONFIG["start_date"], CONFIG["end_date"], "--initial-balance", "100"]

    # Set environment dengan PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = PYTHONPATH

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=3600,
        cwd=TRADING_DIR,
        env=env  # CRITICAL: pass PYTHONPATH
    )

    if result.returncode != 0:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": result.stderr[:150]}

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
                            "gp": data.get("gross_profit", 0),
                            "gl": data.get("gross_loss", 0),
                            "avg_win": data.get("avg_win", {}).get("usd", 0),
                            "avg_loss": data.get("avg_loss", {}).get("usd", 0),
                        }
                except:
                    continue
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": "No JSON found"}
    except Exception as e:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": f"JSON parse: {str(e)[:150]}"}

print("="*100)
print("VILONA FINAL - PYTHONPATH FIXED - BERKAHKARYA QUANT FUND")
print("="*100)
print(f"PYTHONPATH: {PYTHONPATH}")
print(f"Working dir: {TRADING_DIR}")
print(f"Configs: {len(STRATEGIES)}")
print("="*100)
print()

results = []
with ProcessPoolExecutor(max_workers=4) as executor:
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
    print(f"\n{'Pair':<10} {'TF':<6} {'Strategy':<50} {'WR':>8} {'PNL':>10} {'Trades':>8}")
    print("-"*100)

    for r in results:
        strat_name = r["script"].split("/")[-2].replace("_", " ")[:48].title()
        print(f"{r['pair']:<10} {r['tf']:<6} {strat_name:<50} {r['wr']:>7.1f}% ${r['pnl']:>9.2f} {r['trades']:>8}")

    best = max(results, key=lambda x: x["wr"])
    print("\n" + "="*100)
    print("🏆 WINNER")
    print("="*100)
    print(f"Strategy: {best['script'].split('/')[-2].replace('_', ' ').title()}")
    print(f"Pair: {best['pair']} {best['tf']}")
    print(f"WR: {best['wr']:.1f}% | PNL: ${best['pnl']:.2f} | Trades: {best['trades']}")
    print(f"Balance: ${best['balance']:.2f} | Profit Factor: {best['pf']:.2f}")

    report = {"config": CONFIG, "results": results, "best": best}
    with open("berkahkarya_quant_final.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[📁 SAVED] berkahkarya_quant_final.json")

else:
    print("\n❌ All backtests failed!")

print(f"\n{'='*100}")
print(f"Total: {len(STRATEGIES)} | Success: {len(results)} | Failed: {len(STRATEGIES) - len(results)}")
print(f"{'='*100}")
