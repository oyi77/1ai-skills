#!/usr/bin/env python3
"""
VILONA FINAL - ALL 36 STRATEGIES
Menggunakan venv Python yang benar - backslash bukan masalah!
"""

import os
import subprocess
import json
from concurrent.futures import ProcessPoolExecutor, as_completed

# Venv Python (expand tilde!)
VENV_PYTHON = os.path.expanduser('~/.trading-venv/bin/python')
TRADING_DIR = os.path.join(os.getcwd(), 'skills', '1ai-skills', 'trading')
TRADING_DIR = os.path.normpath(TRADING_DIR)

# Config
CONFIG = {
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "initial_balance": 100.0,
}

# ALL strategies
STRATEGIES = [
    # XAUUSD - PROVEN
    ("XAUUSD", "H1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "H4", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),
    ("XAUUSD", "D1", "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"),

    # GBPUSD
    ("GBPUSD", "H1", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "H4", "strategy/templates/forex/holy_grail.py"),
    ("GBPUSD", "D1", "strategy/templates/forex/holy_grail.py"),

    # EURUSD
    ("EURUSD", "H1", "strategy/templates/forex/holy_grail.py"),
    ("EURUSD", "H4", "strategy/templates/forex/holy_grail.py"),
    ("EURUSD", "D1", "strategy/templates/forex/holy_grail.py"),

    # USDJPY
    ("USDJPY", "H1", "strategy/templates/forex/holy_grail.py"),
    ("USDJPY", "H4", "strategy/templates/forex/holy_grail.py"),
    ("USDJPY", "D1", "strategy/templates/forex/holy_grail.py"),

    # Momentum Elder
    ("GBPUSD", "H1", "strategy/templates/forex/momentum_elder.py"),
    ("GBPUSD", "H4", "strategy/templates/forex/momentum_elder.py"),
    ("GBPUSD", "D1", "strategy/templates/forex/momentum_elder.py"),

    ("EURUSD", "H1", "strategy/templates/forex/momentum_elder.py"),
    ("EURUSD", "H4", "strategy/templates/forex/momentum_elder.py"),
    ("EURUSD", "D1", "strategy/templates/forex/momentum_elder.py"),

    ("USDJPY", "H1", "strategy/templates/forex/momentum_elder.py"),
    ("USDJPY", "H4", "strategy/templates/forex/momentum_elder.py"),
    ("USDJPY", "D1", "strategy/templates/forex/momentum_elder.py"),

    # Kumo Breakout
    ("GBPUSD", "H1", "strategy/templates/forex/kumo_breakout.py"),
    ("GBPUSD", "H4", "strategy/templates/forex/kumo_breakout.py"),
    ("GBPUSD", "D1", "strategy/templates/forex/kumo_breakout.py"),

    ("EURUSD", "H1", "strategy/templates/forex/kumo_breakout.py"),
    ("EURUSD", "H4", "strategy/templates/forex/kumo_breakout.py"),
    ("EURUSD", "D1", "strategy/templates/forex/kumo_breakout.py"),

    ("USDJPY", "H1", "strategy/templates/forex/kumo_breakout.py"),
    ("USDJPY", "H4", "strategy/templates/forex/kumo_breakout.py"),
    ("USDJPY", "D1", "strategy/templates/forex/kumo_breakout.py"),

    # Crypto - Volume Momentum
    ("BTCUSDT", "1h", "strategy/templates/crypto/volume_momentum.py"),
    ("BTCUSDT", "4h", "strategy/templates/crypto/volume_momentum.py"),
    ("BTCUSDT", "1d", "strategy/templates/crypto/volume_momentum.py"),

    ("ETHUSDT", "1h", "strategy/templates/crypto/volume_momentum.py"),
    ("ETHUSDT", "4h", "strategy/templates/crypto/volume_momentum.py"),
    ("ETHUSDT", "1d", "strategy/templates/crypto/volume_momentum.py"),

    ("SOLUSDT", "1h", "strategy/templates/crypto/volume_momentum.py"),
    ("SOLUSDT", "4h", "strategy/templates/crypto/volume_momentum.py"),
    ("SOLUSDT", "1d", "strategy/templates/crypto/volume_momentum.py"),
]

def run_backtest(pair, tf, script):
    """Run backtest dengan venv Python."""
    script_path = os.path.normpath(os.path.join(TRADING_DIR, script))

    cmd = [VENV_PYTHON, script_path, "backtest", CONFIG["start_date"], CONFIG["end_date"], "--initial-balance", "100"]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=3600,
        cwd=TRADING_DIR
    )

    if result.returncode != 0:
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": result.stderr[:100]}

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
        return {"pair": pair, "tf": tf, "status": "FAILED", "error": f"JSON parse: {str(e)[:100]}"}

print("="*100)
print("VILONA FINAL BACKTEST - 36 STRATEGIES - BERKAHKARYA QUANT FUND")
print("="*100)
print(f"Period: {CONFIG['start_date']} to {CONFIG['end_date']}")
print(f"Total configs: {len(STRATEGIES)}")
print(f"Workers: 4")
print(f"Venv Python: {VENV_PYTHON}")
print(f"Working dir: {TRADING_DIR}")
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
            print(f"[{completed}/{len(STRATEGIES)}] ❌ {result['pair']:>7} {result['tf']:>3} - {result.get('error', 'Unknown')}")

# Generate report
print("\n" + "="*100)
print("FINAL REPORT - BERKAHKARYA QUANT FUND")
print("="*100)

if results:
    # Strategy summary
    strategy_summary = {}
    for r in results:
        s = r["script"].split("/")[-2].replace("_", " ").title()
        if s not in strategy_summary:
            strategy_summary[s] = {"wr": [], "pnl": [], "trades": []}
        strategy_summary[s]["wr"].append(r["wr"])
        strategy_summary[s]["pnl"].append(r["pnl"])
        strategy_summary[s]["trades"].append(r["trades"])

    print(f"\n{'='*100}")
    print("STRATEGY RANKING (by average win rate)")
    print(f"{'='*100}")
    print(f"{'Strategy':<40} {'Tests':>6} {'Avg WR':>8} {'Avg PNL':>10} {'Total Trades':>12}")
    print("-"*100)

    for strat, data in sorted(strategy_summary.items(), key=lambda x: -sum(x[1]["wr"])/len(x[1]["wr"]) if x[1]["wr"] else 0):
        tests = len(data["wr"])
        avg_wr = sum(data["wr"]) / tests
        avg_pnl = sum(data["pnl"]) / tests
        total_trades = sum(data["trades"])

        print(f"{strat:<40} {tests:>6} {avg_wr:>7.1f}% ${avg_pnl:>9.2f} {total_trades:>12}")

    # Top 10
    print(f"\n{'='*100}")
    print("📊 TOP 10 CONFIGURATIONS")
    print(f"{'='*100}")
    print(f"{'Rank':<6} {'Pair':<10} {'TF':<6} {'Strategy':<30} {'WR':>8} {'PNL':>10} {'Trades':>8}")
    print("-"*100)

    for i, r in enumerate(sorted(results, key=lambda x: -x["wr"])[:10], 1):
        strat_name = r["script"].split("/")[-2].replace("_", " ")[:28].title()
        print(f"{i:<6} {r['pair']:<10} {r['tf']:<6} {strat_name:<30} {r['wr']:>7.1f}% ${r['pnl']:>9.2f} {r['trades']:>8}")

    # Best overall
    best = max(results, key=lambda x: x["wr"])
    print(f"\n{'='*100}")
    print("🏆 OVERALL WINNER - BEST STRATEGY")
    print(f"{'='*100}")
    print(f"Strategy: {best['script'].split('/')[-2].replace('_', ' ').title()}")
    print(f"Pair: {best['pair']}")
    print(f"Timeframe: {best['tf']}")
    print(f"Win Rate: {best['wr']:.1f}%")
    print(f"Net PNL: ${best['pnl']:.2f} (+{best['pnl']/100*100:.1f}%)")
    print(f"Profit Factor: {best['pf']:.2f}")
    print(f"Total Trades: {best['trades']} (Wins: {best['wins']}, Losses: {best['losses']})")
    print(f"Balance: ${best['balance']:.2f}")
    print(f"Avg Win: ${best['avg_win']:.2f} | Avg Loss: ${best['avg_loss']:.2f}")

    # Save report
    report = {
        "config": CONFIG,
        "total_tests": len(STRATEGIES),
        "successful_tests": len(results),
        "failed_tests": len(STRATEGIES) - len(results),
        "results": results,
        "strategy_summary": {strat: {
            "tests": len(d["wr"]),
            "avg_win_rate": sum(d["wr"]) / len(d["wr"]),
            "avg_net_pnl": sum(d["pnl"]) / len(d["pnl"]),
            "total_trades": sum(d["trades"]),
            "best_wr": max(d["wr"]),
            "best_pnl": max(d["pnl"]),
        } for strat, d in strategy_summary.items()
        },
        "best_overall": best,
        "top_10": sorted(results, key=lambda x: -x["wr"])[:10],
    }

    with open("berkahkarya_quant_final_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[📁 SAVED] berkahkarya_quant_final_report.json")

else:
    print("\n❌ No successful backtests!")

print(f"\n{'='*100}")
print(f"SUMMARY")
print(f"{'='*100}")
print(f"   Total configs tested: {len(STRATEGIES)}")
print(f"   Successful: {len(results)}")
print(f"   Failed: {len(STRATEGIES) - len(results)}")
print(f"\n💡 REKOMENDASI VILONA:")
if results and best["wr"] > 55 and best["pnl"] > 0:
    print(f"   ✅ PROCEED dengan strategy terbaik:")
    print(f"      {best['script'].split('/')[-2].replace('_', ' ').title()}")
    print(f"      WR: {best['wr']:.1f}% | PNL: ${best['pnl']:.2f}")
    print(f"   → Setup Fusion Markets cTrader DEMO")
    print(f"   → Test 2 minggu lalu scale ke LIVE")
else:
    print(f"   ❌ Tidak ada strategy yang profitable")
    print(f"   → Perlu develop strategy baru")
print(f"{'='*100}")
