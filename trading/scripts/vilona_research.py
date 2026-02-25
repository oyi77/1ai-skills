#!/usr/bin/env python3
"""
Comprehensive Trading Research & Backtest System - Vilona Edition

Author: Vilona (BerkahKarya AI General Manager & Business Development)
Role: Kritikal, kreatif, logis, futuristik, tidak suka menjilat
Goal: Maximize profit untuk berkahkarya dengan data-driven decision

"""

import sys
import os
import subprocess
import json
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import argparse

# Cross-platform path detection for trading system
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRADING_BASE = os.path.dirname(SCRIPT_DIR)  # Parent of scripts/
REPORT_PATH = os.path.join(TRADING_BASE, "backtest_report_vilona.json")

# Market configurations - 7 pairs for research
MARKETS = {
    "GBPUSD": {"type": "forex", "symbol": "GBPUSD", "timeframes": ["H1", "H4", "D1"]},
    "EURUSD": {"type": "forex", "symbol": "EURUSD", "timeframes": ["H1", "H4", "D1"]},
    "USDJPY": {"type": "forex", "symbol": "USDJPY", "timeframes": ["H1", "H4", "D1"]},
    "XAUUSD": {"type": "commodities", "symbol": "XAUUSD", "timeframes": ["H1", "H4", "D1"]},
    "BTCUSDT": {"type": "crypto", "symbol": "BTC/USDT", "timeframes": ["1h", "4h", "1d"]},
    "ETHUSDT": {"type": "crypto", "symbol": "ETH/USDT", "timeframes": ["1h", "4h", "1d"]},
    "SOLUSDT": {"type": "crypto", "symbol": "SOL/USDT", "timeframes": ["1h", "4h", "1d"]},
}

# Strategy configurations - optimized for each market
FOREX_STRATEGIES = [
    {"name": "HOLY_GRAIL", "script": "strategy/templates/forex/holy_grail.py", 
     "desc": "Multi-timeframe EMA crossover + ADX trend confirmation"},
    {"name": "MOMENTUM_ELDER", "script": "strategy/templates/forex/momentum_elder.py",
     "desc": "Elder Ray impulse system with volume confirmation"},
    {"name": "KUMO_BREAKOUT", "script": "strategy/templates/forex/kumo_breakout.py",
     "desc": "Ichimoku Kumo breakout with cloud analysis"},
    {"name": "RSI_DIVERGENCE", "script": "strategy/templates/forex/rsi_divergence.py",
     "desc": "RSI divergence detection for reversal signals"},
]

COMMODITIES_STRATEGIES = [
    {"name": "ASIA_7CANDLE", "script": "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py",
     "desc": "XAUUSD Asia session breakout with 7-candle window"},
]

CRYPTO_STRATEGIES = [
    {"name": "VOLUME_MOMENTUM", "script": "strategy/templates/crypto/volume_momentum.py",
     "desc": "Volume-weighted momentum with volume spike detection"},
    {"name": "FUNDING_REVERSAL", "script": "strategy/templates/crypto/funding_reversal.py",
     "desc": "Arbitrage based on funding rate divergences"},
]

# Configuration
BACKTEST_CONFIG = {
    "PERIOD": "2025-01-01 to 2025-12-31",
    "INITIAL_BALANCE": 100.0,
    "TIMEOUT_SECONDS": 3600,
}

# Results storage
BEST_RESULTS = {
    "overall": {"strategy": None, "pair": None, "win_rate": 0, "net_pnl": 0, "profit_factor": 0, "max_dd": 0},
    "by_pair": {},
}

def run_backtest(cfg):
    """Run single backtest with proper path handling."""
    try:
        pair = cfg["pair"]
        tf = cfg["timeframe"]
        strat = cfg["strategy"]
        script = strat["script"]
        strat_name = strat["name"]
        strat_desc = strat.get("desc", "Unknown strategy")

        # Use relative path from TRADING_BASE
        full_path = os.path.join(TRADING_BASE, script)

        if not os.path.exists(full_path):
            return {"error": f"SCRIPT_NOT_FOUND: {full_path}"}

        # Build command
        cmd = ["python3", full_path, "backtest", "2025-01-01", "2025-12-31", "--initial-balance", "100"]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

        if result.returncode != 0:
            return {"error": f"RUNTIME_ERROR: {result.stderr[:200]}"}

        # Parse output
        output = result.stdout

        # Extract metrics
        metrics = {
            "pair": pair, "timeframe": tf, "strategy": strat_name, "strategy_desc": strat_desc,
            "period": BACKTEST_CONFIG["PERIOD"], "initial_capital": BACKTEST_CONFIG["INITIAL_BALANCE"],
            "win_rate": 0, "wins": 0, "losses": 0, "avg_win_usd": 0, "avg_loss_usd": 0,
            "max_drawdown": 0, "max_drawdown_pct": 0, "gross_profit": 0, "gross_loss": 0,
            "profit_factor": 0, "net_pnl": 0, "ending_balance": BACKTEST_CONFIG["INITIAL_BALANCE"],
            "total_trades": 0,
        }

        for line in output.split('\n'):
            if "Win Rate:" in line: metrics["win_rate"] = float(line.split(":")[1].strip().replace("%", ""))
            elif "Total Trades:" in line: metrics["total_trades"] = int(line.split(":")[1].strip())
            elif "Wins:" in line: metrics["wins"] = int(line.split(":")[1].strip())
            elif "Losses:" in line: metrics["losses"] = int(line.split(":")[1].strip())
            elif "Net PNL:" in line and "$" in line: 
                metrics["net_pnl"] = float(line.split(":")[1].strip().replace("$", ""))
                metrics["ending_balance"] = 100 + metrics["net_pnl"]
            elif "Profit Factor:" in line: metrics["profit_factor"] = float(line.split(":")[1].strip())
            elif "Gross Profit:" in line and "$" in line: metrics["gross_profit"] = float(line.split(":")[1].strip().replace("$", ""))
            elif "Gross Loss:" in line and "$" in line: metrics["gross_loss"] = float(line.split(":")[1].strip().replace("$", ""))
            elif "Max Drawdown:" in line:
                dd = line.split(":")[1].strip()
                if "(" in dd:
                    metrics["max_drawdown"] = float(dd.split("$")[1].split("(")[0].strip())
                    metrics["max_drawdown_pct"] = float(dd.split("(")[1].replace("%", "").replace(")", ""))
            elif "Avg Win (USD)" in line: metrics["avg_win_usd"] = float(line.split(":")[1].strip().replace("$", ""))
            elif "Avg Loss (USD)" in line: metrics["avg_loss_usd"] = float(line.split(":")[1].strip().replace("$", ""))
            elif "Avg Win (points)" in line: metrics["avg_win_points"] = float(line.split(":")[1].strip())
            elif "Avg Loss (points)" in line: metrics["avg_loss_points"] = float(line.split(":")[1].strip())

        return metrics

    except subprocess.TimeoutExpired:
        return {"error": "TIMEOUT"}
    except Exception as e:
        return {"error": f"EXCEPTION: {str(e)}"}


def run_comprehensive_backtests():
    """Run all backtests in parallel with highest thinking."""
    print("\n" + "="*80)
    print(f"VILONA - BerkahKarya AI Trading Research System")
    print(f"{'='*80}")
    print(f"CONFIG: {BACKTEST_CONFIG['PERIOD']} | INITIAL: ${BACKTEST_CONFIG['INITIAL_BALANCE']}/strategi")
    print(f"{'='*80}\n")

    # Prepare all test configurations
    configs = []
    for pair, info in MARKETS.items():
        if info["type"] == "forex": strategies = FOREX_STRATEGIES
        elif info["type"] == "commodities": strategies = COMMODITIES_STRATEGIES
        elif info["type"] == "crypto": strategies = CRYPTO_STRATEGIES
        else: strategies = []

        for tf in info["timeframes"]:
            for strat in strategies:
                configs.append({"pair": pair, "timeframe": tf, "strategy": strat})

    print(f"Total Configurations: {len(configs)}")
    print(f"Running with 4 parallel workers...")
    print(f"{'='*80}\n")

    # Run in parallel
    results = []
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run_backtest, cfg): cfg for cfg in configs}

        completed = 0
        for future in as_completed(futures):
            completed += 1
            metrics = future.result()

            if metrics and "error" not in metrics:
                # Update best results
                if metrics["win_rate"] > BEST_RESULTS["overall"]["win_rate"]:
                    BEST_RESULTS["overall"] = metrics.copy()
                    print(f"\n[NEW BEST OVERALL] {metrics['pair']} {metrics['strategy']}")
                    print(f"  WR: {metrics['win_rate']:.1f}% | PNL: ${metrics['net_pnl']:.2f} | PF: {metrics['profit_factor']:.2f}\n")

                # Update by-pair best
                pair = metrics["pair"]
                if pair not in BEST_RESULTS["by_pair"]:
                    BEST_RESULTS["by_pair"][pair] = metrics
                elif metrics["win_rate"] > BEST_RESULTS["by_pair"][pair]["win_rate"]:
                    BEST_RESULTS["by_pair"][pair] = metrics

                results.append(metrics)
                print(f"[{completed}/{len(configs)}] {pair} {tf} {strat_name}: {metrics['win_rate']:.1f}% WR")

            elif metrics:
                print(f"[{completed}/{len(configs)}] FAILED: {metrics['error'][:50]}...")

    return results


def generate_report(results):
    """Generate comprehensive report with period/timeframe included."""
    print("\n" + "="*80)
    print("COMPREHENSIVE BACKTEST REPORT - VILONA EDITION")
    print("="*80)
    print(f"Period: {BACKTEST_CONFIG['PERIOD']}")
    print(f"Initial Balance: ${BACKTEST_CONFIG['INITIAL_BALANCE']:.2f} per strategy")
    print(f"Timeframes Tested: H1, H4, D1 (Forex/Commodities) | 1h, 4h, 1d (Crypto)")
    print(f"{'='*80}")

    # Strategy summary
    strategy_summary = {}
    for r in results:
        s = r["strategy"]
        if s not in strategy_summary:
            strategy_summary[s] = {"wr": [], "pnl": [], "desc": r.get("strategy_desc", "N/A")}
        strategy_summary[s]["wr"].append(r["win_rate"])
        strategy_summary[s]["pnl"].append(r["net_pnl"])

    print("\nSTRATEGY PERFORMANCE (sorted by avg win rate):")
    print("-"*80)
    print(f"{'Strategy':<25} {'WR':>7} {'Avg PNL':>10} {'Best Pair':>15} | {'Period':<20}")
    print("-"*80)

    for strat, data in sorted(strategy_summary.items(), key=lambda x: -sum(x[1]["wr"])/len(x[1]["wr"]) if x[1]["wr"] else 0):
        print(f"{strat:<25} {sum(data['wr'])/len(data['wr']):>6.1f}% ${sum(data['pnl'])/len(data['pnl']):>9.2f} {r['pair']:>15} | {data['desc'][:20]}")

    # Best overall
    print("\n" + "="*80)
    print("OVERALL WINNER")
    print("="*80)
    if BEST_RESULTS["overall"]["strategy"]:
        print(f"Best Strategy: {BEST_RESULTS['overall']['strategy']}")
        print(f"Best Pair: {BEST_RESULTS['overall']['pair']}")
        print(f"Win Rate: {BEST_RESULTS['overall']['win_rate']:.1f}%")
        print(f"Net PNL: ${BEST_RESULTS['overall']['net_pnl']:.2f}")
        print(f"Profit Factor: {BEST_RESULTS['overall']['profit_factor']:.2f}")
        print(f"Max Drawdown: ${BEST_RESULTS['overall']['max_drawdown']:.2f} ({BEST_RESULTS['overall']['max_drawdown_pct']:.1f}%)")
        print(f"Total Trades: {BEST_RESULTS['overall']['total_trades']}")
        print(f"Period: {BEST_RESULTS['overall']['period']}")
        print(f"Timeframe: {BEST_RESULTS['overall']['timeframe']}")
    else:
        print("No profitable strategies found!")

    # Save report
    report = {
        "config": BACKTEST_CONFIG,
        "results": results,
        "best_overall": BEST_RESULTS["overall"],
        "best_by_pair": BEST_RESULTS["by_pair"],
        "timestamp": datetime.now().isoformat(),
    }

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n[REPORT SAVED] {REPORT_PATH}")


if __name__ == "__main__":
    results = run_comprehensive_backtests()
    generate_report(results)
    print("\n" + "="*80)
    print("BACKTEST COMPLETE - VILONA OUT!")
    print("="*80)
