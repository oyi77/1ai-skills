#!/usr/bin/env python3
"""
Comprehensive Trading Research & Backtest System - FIXED VERSION

- Downloads all historical data for multiple pairs
- Runs parallel backtests with multiple strategies
- Generates comprehensive reports

Author: Vilona (BerkahKarya AI General Manager & Business Development)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import argparse
import time
import subprocess

# Base path for trading skill
TRADING_BASE = "/home/openclaw/C:\\Users\\EX PC\\.openclaw\\workspace/skills/1ai-skills/trading"

# Convert to proper Unix path
if "\\" in TRADING_BASE:
    # Remove Windows path parts and use Unix-style path
    TRADING_BASE = "/home/openclaw/C:/Users/EX PC/.openclaw/workspace/skills/1ai-skills/trading"

# Market configurations
MARKETS = {
    # Forex
    "GBPUSD": {"type": "forex", "symbol": "GBPUSD", "timeframes": ["H1", "H4", "D1"]},
    "EURUSD": {"type": "forex", "symbol": "EURUSD", "timeframes": ["H1", "H4", "D1"]},
    "USDJPY": {"type": "forex", "symbol": "USDJPY", "timeframes": ["H1", "H4", "D1"]},

    # Commodities
    "XAUUSD": {"type": "commodities", "symbol": "XAUUSD", "timeframes": ["H1", "H4", "D1"]},

    # Crypto
    "BTCUSDT": {"type": "crypto", "symbol": "BTC/USDT", "timeframes": ["1h", "4h", "1d"]},
    "ETHUSDT": {"type": "crypto", "symbol": "ETH/USDT", "timeframes": ["1h", "4h", "1d"]},
    "SOLUSDT": {"type": "crypto", "symbol": "SOL/USDT", "timeframes": ["1h", "4h", "1d"]},
}

# Strategy pool per market type
FOREX_STRATEGIES = [
    {"name": "Holy Grail", "script": "strategy/templates/forex/holy_grail.py", "params": {}},
    {"name": "Momentum Elder", "script": "strategy/templates/forex/momentum_elder.py", "params": {}},
    {"name": "Kumo Breakout", "script": "strategy/templates/forex/kumo_breakout.py", "params": {}},
    {"name": "RSI Divergence", "script": "strategy/templates/forex/rsi_divergence.py", "params": {}},
]

COMMODITIES_STRATEGIES = [
    {"name": "Asia 7-Candle", "script": "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py", "params": {}},
]

CRYPTO_STRATEGIES = [
    {"name": "Volume Momentum", "script": "strategy/templates/crypto/volume_momentum.py", "params": {}},
    {"name": "Funding Reversal", "script": "strategy/templates/crypto/funding_reversal.py", "params": {}},
]

# Best results tracker
BEST_RESULTS = {
    "overall": {
        "strategy": None,
        "pair": None,
        "win_rate": 0,
        "net_pnl": 0,
        "profit_factor": 0,
        "max_drawdown": 0,
    },
    "by_pair": {},
}

BACKTEST_CONFIG = {
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "initial_balance": 100.0,
}


def download_historical_data(pair, timeframes):
    """Download historical data for a pair across multiple timeframes."""
    import yfinance as yf

    pair_data = {}

    # Map pair symbol to yfinance ticker
    ticker_map = {
        "XAUUSD": "GC=F",
        "GBPUSD": "GBPUSD=X",
        "EURUSD": "EURUSD=X",
        "USDJPY": "USDJPY=X",
        "BTCUSDT": "BTC-USD",
        "ETHUSDT": "ETH-USD",
        "SOLUSDT": "SOL-USD",
    }

    ticker_symbol = ticker_map.get(pair, pair)

    for tf in timeframes:
        try:
            print(f"[DOWNLOAD] {pair} {tf}...")

            # Map timeframe to yfinance interval
            tf_map = {
                "H1": "1h", "H4": "1d", "D1": "1mo",
                "1h": "1h", "4h": "1d", "1d": "1mo",
            }

            yf_ticker = yf.Ticker(ticker_symbol)
            df = yf_ticker.history(
                start=BACKTEST_CONFIG["start_date"],
                end=BACKTEST_CONFIG["end_date"],
                interval=tf_map.get(tf, "1h")
            )

            if df.empty:
                print(f"[WARNING] {pair} {tf}: No data")
            else:
                print(f"[SUCCESS] {pair} {tf}: {len(df)} bars")
                pair_data[f"{pair}_{tf}"] = df

        except Exception as e:
            print(f"[ERROR] {pair} {tf}: {e}")

    return pair_data


def run_single_backtest(cfg):
    """Run a single backtest and return metrics."""
    try:
        pair = cfg["pair"]
        timeframe = cfg["timeframe"]
        strategy = cfg["strategy"]

        script_path = os.path.join(TRADING_BASE, strategy["script"])
        if not os.path.exists(script_path):
            print(f"[ERROR] Script not found: {script_path}")
            return None

        # Build command
        cmd = [
            "python3", script_path,
            "backtest",
            BACKTEST_CONFIG["start_date"],
            BACKTEST_CONFIG["end_date"],
            "--initial-balance", str(BACKTEST_CONFIG["initial_balance"])
        ]

        print(f"[RUN] {pair} {timeframe} {strategy['name']}...")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600,  # 60 minutes per backtest
            cwd=TRADING_BASE
        )

        if result.returncode != 0:
            print(f"[FAIL] {pair} {timeframe} {strategy['name']}")
            return None

        # Parse output to extract metrics
        output = result.stdout

        # Look for key metrics in output
        metrics = parse_backtest_output(output, pair, timeframe, strategy["name"])

        if metrics:
            print(f"[DONE] {pair} {timeframe} {strategy['name']}: {metrics['win_rate']:.1f}% WR")
            return metrics

    except Exception as e:
        print(f"[ERROR] {pair} {timeframe} {strategy['name']}: {e}")
        return None


def parse_backtest_output(output, pair, timeframe, strategy_name):
    """Parse backtest output to extract key metrics."""
    metrics = {
        "pair": pair,
        "timeframe": timeframe,
        "strategy": strategy_name,
        "initial_capital": BACKTEST_CONFIG["initial_balance"],
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
        "ending_balance": BACKTEST_CONFIG["initial_balance"],
        "total_trades": 0,
    }

    lines = output.split('\n')

    for line in lines:
        if "Total Trades:" in line:
            metrics["total_trades"] = int(line.split(":")[1].strip())
        elif "Wins:" in line:
            metrics["wins"] = int(line.split(":")[1].strip())
        elif "Losses:" in line:
            metrics["losses"] = int(line.split(":")[1].strip())
        elif "Win Rate:" in line:
            metrics["win_rate"] = float(line.split(":")[1].strip().replace("%", ""))
        elif "Net PNL:" in line:
            pnl_line = line.split(":")[1].strip()
            if "$" in pnl_line:
                metrics["net_pnl"] = float(pnl_line.replace("$", ""))
                metrics["ending_balance"] = BACKTEST_CONFIG["initial_balance"] + metrics["net_pnl"]
        elif "Profit Factor:" in line:
            metrics["profit_factor"] = float(line.split(":")[1].strip())
        elif "Gross Profit:" in line:
            gp_line = line.split(":")[1].strip()
            if "$" in gp_line:
                metrics["gross_profit"] = float(gp_line.replace("$", ""))
        elif "Gross Loss:" in line:
            gl_line = line.split(":")[1].strip()
            if "$" in gl_line:
                metrics["gross_loss"] = float(gl_line.replace("$", ""))
        elif "Max Drawdown:" in line:
            dd_line = line.split(":")[1].strip()
            # Format: "$100.00 (10.0%)"
            if "(" in dd_line:
                metrics["max_drawdown"] = float(dd_line.split("$")[1].split("(")[0].strip())
                metrics["max_drawdown_pct"] = float(dd_line.split("(")[1].replace("%", "").replace(")", ""))
        elif "Avg Win (USD)" in line:
            metrics["avg_win_usd"] = float(line.split(":")[1].strip().replace("$", ""))
        elif "Avg Win" in line and "points" in line:
            metrics["avg_win_points"] = float(line.split("points")[1].strip())
        elif "Avg Loss (USD)" in line:
            metrics["avg_loss_usd"] = float(line.split(":")[1].strip().replace("$", ""))
        elif "Avg Loss" in line and "points" in line:
            metrics["avg_loss_points"] = float(line.split("points")[1].strip())

    # Calculate derived metrics
    if metrics["total_trades"] > 0:
        metrics["avg_win_points"] = metrics.get("total_points", 0) / max(metrics["wins"], 1) if metrics["wins"] > 0 else 0
        metrics["avg_loss_points"] = metrics.get("total_points", 0) / max(metrics["losses"], 1) if metrics["losses"] > 0 else 0

    return metrics


def update_best_results(metrics):
    """Update best results tracker."""
    # Update overall best
    if metrics["win_rate"] > BEST_RESULTS["overall"]["win_rate"]:
        BEST_RESULTS["overall"]["win_rate"] = metrics["win_rate"]
        BEST_RESULTS["overall"]["strategy"] = metrics["strategy"]
        BEST_RESULTS["overall"]["pair"] = metrics["pair"]
        BEST_RESULTS["overall"]["net_pnl"] = metrics["net_pnl"]
        BEST_RESULTS["overall"]["profit_factor"] = metrics["profit_factor"]
        BEST_RESULTS["overall"]["max_drawdown"] = metrics["max_drawdown"]

    # Update by pair best
    pair = metrics["pair"]
    if pair not in BEST_RESULTS["by_pair"]:
        BEST_RESULTS["by_pair"][pair] = {}
    BEST_RESULTS["by_pair"][pair]["win_rate"] = metrics["win_rate"]
    BEST_RESULTS["by_pair"][pair]["strategy"] = metrics["strategy"]
    BEST_RESULTS["by_pair"][pair]["net_pnl"] = metrics["net_pnl"]
    BEST_RESULTS["by_pair"][pair]["profit_factor"] = metrics["profit_factor"]

    # Log update
    print(f"[BEST] {pair} {metrics['strategy']}: {metrics['win_rate']:.1f}% WR, ${metrics['net_pnl']:.2f} PNL")
    if metrics["win_rate"] > BEST_RESULTS["overall"]["win_rate"]:
        print(f"[NEW BEST OVERALL] {metrics['strategy']} on {pair}")


def run_parallel_backtests(pairs):
    """Run all backtests in parallel with highest thinking."""
    print(f"\n{'='*80}")
    print(f"PARALLEL BACKTEST SYSTEM - HIGHEST THINKING MODE")
    print(f"{'='*80}")
    print(f"Pairs: {len(pairs)} | Strategies: Varies per market")
    print(f"Total Tests: {len(pairs) * 12} average")  # Each pair: 3 timeframes, multiple strategies
    print(f"{'='*80}\n")

    test_configs = []

    for pair in pairs:
        market_info = MARKETS.get(pair, {})
        if not market_info:
            print(f"[SKIP] Unknown pair: {pair}")
            continue

        strategies_to_test = FOREX_STRATEGIES if market_info["type"] == "forex" else \
                               COMMODITIES_STRATEGIES if market_info["type"] == "commodities" else \
                               CRYPTO_STRATEGIES if market_info["type"] == "crypto" else []

        for timeframe in market_info["timeframes"]:
            for strategy in strategies_to_test:
                test_configs.append({
                    "pair": pair,
                    "timeframe": timeframe,
                    "strategy": strategy,
                })

    # Shuffle configs for balanced execution
    import random
    random.shuffle(test_configs)

    # Run in parallel with 4 workers
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run_single_backtest, cfg): cfg for cfg in test_configs}

        results = []
        for future in as_completed(futures):
            metrics = future.result()
            if metrics:
                update_best_results(metrics)
                results.append(metrics)

    return results


def generate_comprehensive_report(results):
    """Generate comprehensive report with all results."""
    print(f"\n{'='*80}")
    print("COMPREHENSIVE BACKTEST REPORT - 2025")
    print(f"{'='*80}")
    print(f"Period: {BACKTEST_CONFIG['start_date']} to {BACKTEST_CONFIG['end_date']}")
    print(f"Initial Capital: ${BACKTEST_CONFIG['initial_balance']:.2f} per strategy")
    print(f"Total Strategies Tested: {len(set(r['strategy'] for r in results))}")
    print(f"Total Tests Run: {len(results)}")
    print(f"{'='*80}\n")

    # Group results by strategy
    strategy_summary = {}
    for result in results:
        strategy = result["strategy"]
        if strategy not in strategy_summary:
            strategy_summary[strategy] = {
                "win_rates": [],
                "pnls": [],
                "total_trades": [],
            }
        strategy_summary[strategy]["win_rates"].append(result["win_rate"])
        strategy_summary[strategy]["pnls"].append(result["net_pnl"])
        strategy_summary[strategy]["total_trades"].append(result["total_trades"])

    # Calculate strategy averages
    print("\nSTRATEGY PERFORMANCE:")
    print("-" * 80)
    print(f"{'Strategy':<30} {'Tests':>7} {'Avg WR':>8} {'Avg PNL':>10} {'Best Pair':>15}")
    print("-" * 80)

    for strategy, data in sorted(strategy_summary.items()):
        tests = len(data["win_rates"])
        avg_wr = sum(data["win_rates"]) / tests
        avg_pnl = sum(data["pnls"]) / tests
        total_trades = sum(data["total_trades"])

        # Find best pair for this strategy
        best_pair = None
        best_pnl = -float('inf')
        for result in results:
            if result["strategy"] == strategy:
                if result["net_pnl"] > best_pnl:
                    best_pnl = result["net_pnl"]
                    best_pair = result["pair"]

        print(f"{strategy:<30} {tests:>7} {avg_wr:>7.1f}% ${avg_pnl:>9.2f} {best_pair or 'N/A':>15}")

    # Find overall best
    print("\n" + "="*80)
    print("OVERALL BEST PERFORMANCE")
    print("="*80)

    if BEST_RESULTS["overall"]["strategy"]:
        print(f"Best Strategy: {BEST_RESULTS['overall']['strategy']}")
        print(f"Best Pair: {BEST_RESULTS['overall']['pair']}")
        print(f"Best Win Rate: {BEST_RESULTS['overall']['win_rate']:.1f}%")
        print(f"Best Net PNL: ${BEST_RESULTS['overall']['net_pnl']:.2f}")
        print(f"Best Profit Factor: {BEST_RESULTS['overall']['profit_factor']:.2f}")
        print(f"Max Drawdown: ${BEST_RESULTS['overall']['max_drawdown']:.2f}")

    # Save comprehensive report
    report = {
        "config": BACKTEST_CONFIG,
        "results": results,
        "strategy_summary": strategy_summary,
        "best_overall": BEST_RESULTS["overall"],
        "best_by_pair": BEST_RESULTS["by_pair"],
        "timestamp": datetime.now().isoformat()
    }

    with open("comprehensive_backtest_2025_final.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n[SAVED] Results to: comprehensive_backtest_2025_final.json")


def main():
    parser = argparse.ArgumentParser(description="Comprehensive Trading Research System")
    parser.add_argument("--download-only", action="store_true", help="Download data only, no backtests")
    parser.add_argument("--backtest-only", action="store_true", help="Run backtests only, assume data exists")
    parser.add_argument("--pairs", type=str, default="all", help="Comma-separated list of pairs (e.g., GBPUSD,EURUSD,XAUUSD,BTCUSDT)")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers")
    parser.add_argument("--pair", type=str, help="Test single pair only (e.g., XAUUSD)")

    args = parser.parse_args()

    # Select pairs to test
    if args.pair:
        pairs_to_test = [args.pair.strip()] if args.pair.strip() in MARKETS else []
    else:
        pairs_to_test = list(MARKETS.keys()) if args.pairs == "all" else \
                        [p.strip() for p in args.pairs.split(",") if p.strip() in MARKETS]

    # Step 1: Download historical data
    if not args.backtest_only:
        print("\n" + "="*80)
        print("STEP 1: DOWNLOADING HISTORICAL DATA")
        print("="*80)

        for pair in pairs_to_test:
            market_info = MARKETS.get(pair, {})
            if market_info:
                download_historical_data(pair, market_info["timeframes"])
            else:
                print(f"[SKIP] Unknown pair: {pair}")

        print(f"\n✅ Data download complete!")

    # Step 2: Run comprehensive backtests
    print("\n" + "="*80)
    print("STEP 2: RUNNING COMPREHENSIVE BACKTESTS")
    print("="*80)

    if args.download_only:
        print("\nData download complete. Use --backtest-only to run backtests.")
        return

    all_results = []

    for pair in pairs_to_test:
        results = run_parallel_backtests([pair])
        all_results.extend(results)

    # Step 3: Generate comprehensive report
    generate_comprehensive_report(all_results)

    print(f"\n{'='*80}")
    print("SYSTEM COMPLETE - Total Tests Run: " + str(len(all_results)))
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
