#!/usr/bin/env python3
"""
VILONA SIMPLE BACKTEST RUNNER - CLI untuk semua strategi
Tanpa trading framework dependency - langsung ke scripts.
"""

import sys
import os
import argparse
import json
from datetime import datetime
import subprocess

# Strategies yang sudah proven punya CLI
PROVEN_STRATEGIES = {
    "xauusd_asia_7c": {
        "script": "strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py",
        "name": "XAUUSD Asia 7-Candle Breakout",
    },
}

def run_strategy(strategy_name, start_date, end_date, initial_balance):
    """Run strategy via subprocess."""
    if strategy_name not in PROVEN_STRATEGIES:
        return {"error": f"Strategy '{strategy_name}' not available"}

    strategy_info = PROVEN_STRATEGIES[strategy_name]
    script_path = strategy_info["script"]

    cmd = [
        "~/.trading-venv/bin/python",
        script_path,
        "backtest",
        start_date,
        end_date,
        "--initial-balance",
        str(int(initial_balance))
    ]

    print(f"Running: {strategy_info['name']}")
    print(f"Script: {script_path}")
    print()

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=3600
    )

    if result.returncode != 0:
        return {
            "error": f"Script failed: {result.stderr[:200]}",
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    # Parse JSON output
    for line in result.stdout.split('\n'):
        line = line.strip()
        if line.startswith('{') and line.endswith('}'):
            try:
                data = json.loads(line)
                if 'win_rate' in data:
                    data['strategy_name'] = strategy_name
                    data['strategy_display'] = strategy_info['name']
                    return data
            except:
                continue

    return {"error": "No valid output found"}

def main():
    parser = argparse.ArgumentParser(description='Vilona Simple Backtest Runner')
    parser.add_argument('strategy', help='Strategy name (xauusd_asia_7c)')
    parser.add_argument('start_date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('end_date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--initial-balance', type=float, default=100.0, help='Initial balance')

    args = parser.parse_args()

    print("="*80)
    print("VILONA SIMPLE BACKTEST RUNNER")
    print("="*80)
    print()

    result = run_strategy(
        args.strategy,
        args.start_date,
        args.end_date,
        args.initial_balance
    )

    print()
    print("="*80)
    print("RESULTS")
    print("="*80)
    print()
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
