#!/usr/bin/env python3
"""
VILONA - BerkahKarya Trading Research System
HIGH THINKING MODE - MAX PROFIT OPTIMIZATION

Author: Vilona (BerkahKarya AI General Manager & Business Development)
Role: Kritikal, kreatif, logis, futuristik
Goal: Maximize profit for BerkahKarya with data-driven decision

Date: 2026-02-22
Mission: Find most profitable strategies across all pairs (2025 backtest)
"""

import sys
import os
import subprocess
import json
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor

# Working directory - where the script is running
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
TRADING_BASE = os.path.dirname(WORK_DIR)

# Market configurations - 7 pairs
MARKETS = {
    "XAUUSD": {"type": "commodities", "symbol": "XAUUSD", "timeframes": ["H1", "H4", "D1"]},
    "GBPUSD": {"type": "forex", "symbol": "GBPUSD", "timeframes": ["H1", "H4", "D1"]},
    "EURUSD": {"type": "forex", "symbol": "EURUSD", "timeframes": ["H1", "H4", "D1"]},
    "USDJPY": {"type": "forex", "symbol": "USDJPY", "timeframes": ["H1", "H4", "D1"]},
    "BTCUSDT": {"type": "crypto", "symbol": "BTCUSDT", "timeframes": ["1h", "4h", "1d"]},
    "ETHUSDT": {"type": "crypto", "symbol": "ETHUSDT", "timeframes": ["1h", "4h", "1d"]},
    "SOLUSDT": {"type": "crypto", "symbol": "SOLUSDT", "timeframes": ["1h", "4h", "1d"]},
}

# Strategy definitions
FOREX_STRATEGIES = [
    {"name": "HOLY_GRAIL", "script": "strategy/templates/forex/holy_grail.py"},
    {"name": "MOMENTUM_ELDER", "script": "strategy/templates/forex/momentum_elder.py"},
    {"name": "KUMO_BREAKOUT", "script": "strategy/templates/forex/kumo_breakout.py"},
]

COMMODITIES_STRATEGIES = [
    {"name": "ASIA_7CANDLE", "script": "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"},
]

CRYPTO_STRATEGIES = [
    {"name": "VOLUME_MOMENTUM", "script": "strategy/templates/crypto/volume_momentum.py"},
    {"name": "FUNDING_REVERSAL", "script": "strategy/templates/crypto/funding_reversal.py"},
]

# Configuration
CONFIG = {
    "PERIOD_START": "2025-01-01",
    "PERIOD_END": "2025-12-31",
    "PERIOD": "2025-01-01 to 2025-12-31",
    "INITIAL_BALANCE": 100.0,
    "TIMEOUT_SECONDS": 7200,  # 2 hours per backtest
}

# Best results tracking
BEST_RESULTS = {
    "overall": {"strategy": None, "pair": None, "timeframe": None, "win_rate": 0, "net_pnl": 0, "profit_factor": 0, "max_dd": 0},
    "by_pair": {},
    "by_strategy": {},
    "by_timeframe": {},
}


def download_data(pair, timeframes):
    """Download historical data for a pair."""
    import yfinance as yf

    ticker_map = {
        "XAUUSD": "GC=F",
        "GBPUSD": "GBPUSD=X",
        "EURUSD": "EURUSD=X",
        "USDJPY": "USDJPY=X",
        "BTCUSDT": "BTC-USD",
        "ETHUSDT": "ETH-USD",
        "SOLUSDT": "SOL-USD",
    }

    ticker = ticker_map.get(pair, pair)
    tf_map = {"H1": "1h", "H4": "1d", "D1": "1mo", "1h": "1h", "4h": "1d", "1d": "1mo"}

    data = {}
    for tf in timeframes:
        try:
            yf_ticker = yf.Ticker(ticker)
            df = yf_ticker.history(start=CONFIG["PERIOD_START"], end=CONFIG["PERIOD_END"], interval=tf_map[tf])
            data[f"{pair}_{tf}"] = df
            print(f"[DOWNLOAD] {pair} {tf}: {len(df)} bars")
        except Exception as e:
            print(f"[ERROR] {pair} {tf}: {e}")
    return data


def run_backtest(pair, timeframe, strategy_info):
    """Run a single backtest and return all metrics."""
    strategy_name = strategy_info["name"]
    script_path = os.path.join(TRADING_BASE, strategy_info["script"])

    if not os.path.exists(script_path):
        return {"error": f"SCRIPT_NOT_FOUND: {script_path}", "pair": pair, "strategy": strategy_name, "timeframe": timeframe}

    # Build command
    cmd = ["python3", script_path, "backtest", CONFIG["PERIOD_START"], CONFIG["PERIOD_END"], "--initial-balance", "100"]

    # Run with timeout
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=CONFIG["TIMEOUT_SECONDS"],
            cwd=TRADING_BASE
        )

        if result.returncode != 0:
            return {
                "error": f"RUNTIME_ERROR: {result.stderr[:200]}",
                "pair": pair, "strategy": strategy_name, "timeframe": timeframe
            }

        # Parse output
        output = result.stdout
        metrics = {
            "pair": pair,
            "timeframe": timeframe,
            "strategy": strategy_name,
            "period": CONFIG["PERIOD"],
            "initial_capital": CONFIG["INITIAL_BALANCE"],
            "win_rate": 0,
            "wins": 0,
            "losses": 0,
            "avg_win_usd": 0,
            "avg_win_points": 0,
            "avg_loss_usd": 0,
            "avg_loss_points": 0,
            "max_drawdown": 0,
            "max_drawdown_pct": 0,
            "gross_profit": 0,
            "gross_loss": 0,
            "profit_factor": 0,
            "net_pnl": 0,
            "ending_balance": CONFIG["INITIAL_BALANCE"],
            "total_trades": 0,
        }

        for line in output.split('\n'):
            if "Win Rate:" in line: metrics["win_rate"] = float(line.split(":")[1].strip().replace("%", ""))
            elif "Total Trades:" in line: metrics["total_trades"] = int(line.split(":")[1].strip())
            elif "Wins:" in line: metrics["wins"] = int(line.split(":")[1].strip())
            elif "Losses:" in line: metrics["losses"] = int(line.split(":")[1].strip())
            elif "Net PNL:" in line and "$" in line:
                pnl = float(line.split(":")[1].strip().replace("$", ""))
                metrics["net_pnl"] = pnl
                metrics["ending_balance"] = CONFIG["INITIAL_BALANCE"] + pnl
            elif "Profit Factor:" in line: metrics["profit_factor"] = float(line.split(":")[1].strip())
            elif "Gross Profit:" in line and "$" in line: metrics["gross_profit"] = float(line.split(":")[1].strip().replace("$", ""))
            elif "Gross Loss:" in line and "$" in line: metrics["gross_loss"] = float(line.split(":")[1].strip().replace("$", ""))
            elif "Max Drawdown:" in line:
                dd = line.split(":")[1].strip()
                if "(" in dd:
                    metrics["max_drawdown"] = float(dd.split("$")[1].split("(")[0].strip())
                    metrics["max_drawdown_pct"] = float(dd.split("(")[1].replace("%", "").replace(")", ""))
            elif "Avg Win (USD)" in line: metrics["avg_win_usd"] = float(line.split(":")[1].strip().replace("$", ""))
            elif "Avg Win" in line and "points" in line: metrics["avg_win_points"] = float(line.split(":")[1].strip())
            elif "Avg Loss (USD)" in line: metrics["avg_loss_usd"] = float(line.split(":")[1].strip().replace("$", ""))
            elif "Avg Loss" in line and "points" in line: metrics["avg_loss_points"] = float(line.split(":")[1].strip())
            elif "Total Points:" in line: metrics["total_points"] = float(line.split(":")[1].strip())

        # Calculate avg win/loss points if not in output
        if metrics["total_trades"] > 0:
            if metrics.get("total_points", 0) > 0 and metrics["wins"] > 0:
                metrics["avg_win_points"] = metrics["total_points"] / metrics["wins"]
            if metrics.get("total_points", 0) > 0 and metrics["losses"] > 0:
                metrics["avg_loss_points"] = abs(metrics["total_points"]) / metrics["losses"]

        return metrics

    except subprocess.TimeoutExpired:
        return {"error": "TIMEOUT", "pair": pair, "strategy": strategy_name, "timeframe": timeframe}
    except Exception as e:
        return {"error": f"EXCEPTION: {str(e)}", "pair": pair, "strategy": strategy_name, "timeframe": timeframe}


def update_best_results(metrics):
    """Update and track best results."""
    if "error" in metrics:
        return

    # Update overall best
    if metrics["win_rate"] > BEST_RESULTS["overall"]["win_rate"]:
        BEST_RESULTS["overall"] = metrics.copy()
        print(f"\n[NEW BEST OVERALL] {metrics['strategy']} on {metrics['pair']} {metrics['timeframe']}")
        print(f"  WR: {metrics['win_rate']:.1f}% | PNL: ${metrics['net_pnl']:.2f} | PF: {metrics['profit_factor']:.2f}")

    # Update by pair
    pair = metrics["pair"]
    if pair not in BEST_RESULTS["by_pair"] or metrics["win_rate"] > BEST_RESULTS["by_pair"][pair]["win_rate"]:
        BEST_RESULTS["by_pair"][pair] = metrics

    # Update by strategy
    strategy = metrics["strategy"]
    if strategy not in BEST_RESULTS["by_strategy"] or metrics["net_pnl"] > BEST_RESULTS["by_strategy"][strategy]["net_pnl"]:
        BEST_RESULTS["by_strategy"][strategy] = metrics

    # Update by timeframe
    tf = metrics["timeframe"]
    if tf not in BEST_RESULTS["by_timeframe"] or metrics["win_rate"] > BEST_RESULTS["by_timeframe"][tf]["win_rate"]:
        BEST_RESULTS["by_timeframe"][tf] = metrics


def run_parallel_backtests():
    """Run all backtests in parallel with highest thinking."""
    print("\n" + "="*80)
    print("VILONA - BERBAHKARYA AI TRADING RESEARCH SYSTEM")
    print("="*80)
    print(f"Mode: HIGHEST THINKING - MAX PROFIT OPTIMIZATION")
    print(f"Period: {CONFIG['PERIOD']}")
    print(f"Initial Balance: ${CONFIG['INITIAL_BALANCE']:.2f} per strategy")
    print("="*80)
    print(f"\nMission: Find most profitable strategies for BerkahKarya Quant Division")
    print(f"Cashflow Target: Maximize with lowest risk\n")

    # Build all test configurations
    configs = []

    for pair, info in MARKETS.items():
        strategies = []
        if info["type"] == "forex": strategies = FOREX_STRATEGIES
        elif info["type"] == "commodities": strategies = COMMODITIES_STRATEGIES
        elif info["type"] == "crypto": strategies = CRYPTO_STRATEGIES

        for tf in info["timeframes"]:
            for strat in strategies:
                configs.append({
                    "pair": pair,
                    "timeframe": tf,
                    "strategy": strat,
                })

    print(f"\nTotal Configurations: {len(configs)}")
    print(f"Pairs: {len(MARKETS)} (XAUUSD, GBPUSD, EURUSD, USDJPY, BTCUSDT, ETHUSDT, SOLUSDT)")
    print(f"Timeframes: H1, H4, D1 (Forex/Commodities) | 1h, 4h, 1d (Crypto)")
    print(f"Workers: 6 (parallel execution)")
    print("="*80 + "\n")

    # Shuffle for balanced execution
    import random
    random.shuffle(configs)

    # Run in parallel with 6 workers
    results = []
    with ProcessPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(run_backtest, cfg["pair"], cfg["timeframe"], cfg["strategy"]): cfg for cfg in configs}

        completed = 0
        for future in as_completed(futures):
            completed += 1
            metrics = future.result()

            if metrics and "error" not in metrics:
                update_best_results(metrics)
                results.append(metrics)
                print(f"[{completed}/{len(configs)}] {metrics['pair']:<8} {metrics['timeframe']:<4} {metrics['strategy']:<18} WR: {metrics['win_rate']:>5.1f}% PNL: ${metrics['net_pnl']:>7.2f}")
            else:
                print(f"[{completed}/{len(configs)}] FAILED: {metrics['error'][:60]}...")

    return results


def generate_comprehensive_report(results):
    """Generate detailed report with all requested metrics."""
    print("\n" + "="*80)
    print("COMPREHENSIVE BACKTEST REPORT - VILONA EDITION")
    print("="*80)
    print(f"Period: {CONFIG['PERIOD']}")
    print(f"Initial Balance: ${CONFIG['INITIAL_BALANCE']:.2f} per strategy")
    print(f"Total Tests Run: {len(results)}")
    print("="*80)

    # Strategy summary
    strategy_summary = {}
    for r in results:
        s = r["strategy"]
        if s not in strategy_summary:
            strategy_summary[s] = {"results": [], "wr": [], "pnl": []}
        strategy_summary[s]["results"].append(r)
        strategy_summary[s]["wr"].append(r["win_rate"])
        strategy_summary[s]["pnl"].append(r["net_pnl"])

    print("\nSTRATEGY RANKING (by average win rate):")
    print("-"*80)
    print(f"{'Strategy':<25} {'Tests':>6} {'Avg WR':>7} {'Avg PNL':>10} {'Best Pair':>10} {'Best TF':>6}")
    print("-"*80)

    for strategy, data in sorted(strategy_summary.items(), key=lambda x: -sum(x[1]["wr"])/len(x[1]["wr"]) if x[1]["wr"] else 0):
        avg_wr = sum(data["wr"]) / len(data["wr"])
        avg_pnl = sum(data["pnl"]) / len(data["pnl"])

        # Find best configuration for this strategy
        best_result = max(data["results"], key=lambda x: x["net_pnl"])

        print(f"{strategy:<25} {len(data['results']):>6} {avg_wr:>6.1f}% ${avg_pnl:>9.2f} {best_result['pair']:>10} {best_result['timeframe']:>6}")

    # Pair summary
    print("\nPAIR RANKING (by best win rate):")
    print("-"*80)
    print(f"{'Pair':<10} {'Strategy':<20} {'WR':>6} {'PNL':>10} {'TF':>4} {'Balance':>12}")
    print("-"*80)

    for pair, result in sorted(BEST_RESULTS["by_pair"].items(), key=lambda x: -x[1]["win_rate"]):
        print(f"{pair:<10} {result['strategy']:<20} {result['win_rate']:>5.1f}% ${result['net_pnl']:>9.2f} {result['timeframe']:>4} ${result['ending_balance']:>11.2f}")

    # Timeframe summary
    print("\nTIMEFRAME RANKING (by average win rate):")
    print("-"*80)
    print(f"{'Timeframe':<10} {'Avg WR':>7} {'Avg PNL':>10} {'Best Strat':<20} {'Best Pair':<10}")
    print("-"*80)

    for tf, result in sorted(BEST_RESULTS["by_timeframe"].items(), key=lambda x: -x[1]["win_rate"]):
        print(f"{tf:<10} {result['win_rate']:>6.1f}% ${result['net_pnl']:>9.2f} {result['strategy']:<20} {result['pair']:<10}")

    # Overall winner
    print("\n" + "="*80)
    print("OVERALL WINNER - MOST PROFITABLE STRATEGY")
    print("="*80)

    best = BEST_RESULTS["overall"]
    if best["strategy"]:
        print(f"\nBest Strategy: {best['strategy']}")
        print(f"Best Pair: {best['pair']}")
        print(f"Best Timeframe: {best['timeframe']}")
        print(f"Win Rate: {best['win_rate']:.1f}%")
        print(f"Net PNL: ${best['net_pnl']:.2f}")
        print(f"Profit Factor: {best['profit_factor']:.2f}")
        print(f"Max Drawdown: ${best['max_drawdown']:.2f} ({best['max_drawdown_pct']:.1f}%)")
        print(f"Total Trades: {best['total_trades']}")
        print(f"Wins: {best['wins']}")
        print(f"Losses: {best['losses']}")
        print(f"Average Win: ${best['avg_win_usd']:.2f} USD ({best['avg_win_points']:.2f} points)")
        print(f"Average Loss: ${best['avg_loss_usd']:.2f} USD ({best['avg_loss_points']:.2f} points)")
        print(f"Gross Profit: ${best['gross_profit']:.2f}")
        print(f"Gross Loss: ${best['gross_loss']:.2f}")
        print(f"Initial Capital: ${best['initial_capital']:.2f}")
        print(f"Ending Balance: ${best['ending_balance']:.2f}")
        print(f"Period: {best['period']}")
        print(f"Return: {best['net_pnl']/best['initial_capital']*100:.1f}%")
    else:
        print("No profitable strategies found!")

    # Save full report
    report = {
        "config": CONFIG,
        "results": results,
        "strategy_summary": {
            strat: {
                "avg_win_rate": sum(data["wr"]) / len(data["wr"]),
                "avg_net_pnl": sum(data["pnl"]) / len(data["pnl"]),
                "total_tests": len(data["results"]),
            }
            for strat, data in strategy_summary.items()
        },
        "best_overall": BEST_RESULTS["overall"],
        "best_by_pair": BEST_RESULTS["by_pair"],
        "best_by_timeframe": BEST_RESULTS["by_timeframe"],
        "timestamp": datetime.now().isoformat(),
    }

    #XS|    # Report output path - use home directory by default
#XS|    home_dir = os.path.expanduser("~")
#XS|    report_file = os.path.join(home_dir, ".openclaw", "workspace", "berkahkarya_backtest_report_2025.json")
#XS|    # Ensure directory exists
#XS|    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n[REPORT SAVED] {report_file}")


def main():
    print("\nVILONA - BERBAHKARYA AI TRADING RESEARCH")
    print("Starting comprehensive backtest analysis...")
    print("This may take 1-2 hours to complete all configurations.\n")

    # Step 1: Download all data
    print("="*80)
    print("STEP 1: DOWNLOADING HISTORICAL DATA")
    print("="*80)
    for pair, info in MARKETS.items():
        download_data(pair, info["timeframes"])
    print()

    # Step 2: Run comprehensive backtests
    print("="*80)
    print("STEP 2: RUNNING PARALLEL BACKTESTS")
    print("="*80)
    results = run_parallel_backtests()

    # Step 3: Generate comprehensive report
    print("="*80)
    print("STEP 3: GENERATING REPORT")
    print("="*80)
    generate_comprehensive_report(results)

    print("\n" + "="*80)
    print("VILONA BACKTEST COMPLETE")
    print("="*80)
    print(f"Total Results: {len(results)}")
    print(f"Best Win Rate: {BEST_RESULTS['overall']['win_rate']:.1f}%")
    print(f"Best PNL: ${BEST_RESULTS['overall']['net_pnl']:.2f}")
    print("="*80)


if __name__ == "__main__":
    main()
