#!/usr/bin/env python3
"""
VILONA STRATEGY WRAPPER - Convert class-based strategies to CLI
Membuat semua strategi punya interface seperti XAUUSD Asia 7-Candle
"""

import sys
import os
import argparse
import json
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add current dir to sys.path SEBELUM import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import strategies
from strategy.templates.forex.holy_grail import HolyGrailStrategy
from strategy.templates.forex.kumo_breakout import KumoBreakoutStrategy
from strategy.templates.forex.momentum_elder import MomentumElderStrategy
from strategy.templates.crypto.volume_momentum import VolumeMomentumStrategy

STRATEGY_CLASSES = {
    "holy_grail": HolyGrailStrategy,
    "kumo_breakout": KumoBreakoutStrategy,
    "momentum_elder": MomentumElderStrategy,
    "volume_momentum": VolumeMomentumStrategy,
}

# Symbol mappings
SYMBOL_MAPS = {
    # Forex
    "GBPUSD": "GBPUSD=X",
    "EURUSD": "EURUSD=X",
    "USDJPY": "USDJPY=X",
    # Crypto
    "BTCUSDT": "BTC-USD",
    "ETHUSDT": "ETH-USD",
    "SOLUSDT": "SOL-USD",
    # Commodities
    "XAUUSD": "GC=F",
}

def download_data(symbol, start_date, end_date):
    """Download OHLCV data."""
    yf_symbol = SYMBOL_MAPS.get(symbol, symbol)
    print(f"Downloading {symbol} data...")

    try:
        ticker = yf.Ticker(yf_symbol)
        df = ticker.history(start=start_date, end=end_date, interval="1d")
        print(f"Downloaded {len(df)} bars")

        # Rename columns
        df = df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

def run_backtest(strategy_name, symbol, start_date, end_date, initial_balance):
    """Run backtest for a strategy."""
    strategy_class = STRATEGY_CLASSES.get(strategy_name)

    if not strategy_class:
        return {"error": f"Strategy '{strategy_name}' not found"}

    try:
        # Initialize strategy
        strategy = strategy_class({
            'symbol': symbol,
            'pair': symbol,
            'initial_balance': initial_balance,
        })

        # Download data
        df = download_data(symbol, start_date, end_date)

        if df is None or len(df) == 0:
            return {"error": "No data available"}

        # Run backtest
        print(f"Running backtest for {strategy_name} on {symbol}...")

        result = strategy.backtest(start_date, end_date, df)

        if 'error' in result:
            return result

        # Add metadata
        result['strategy'] = strategy_name
        result['symbol'] = symbol
        result['period'] = f"{start_date} to {end_date}"

        return result

    except Exception as e:
        import traceback
        return {
            "error": f"Backtest failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

def main():
    parser = argparse.ArgumentParser(description='Vilona Universal Strategy Runner')
    parser.add_argument('strategy', help='Strategy name (holy_grail, kumo_breakout, momentum_elder, volume_momentum)')
    parser.add_argument('symbol', help='Trading symbol (XAUUSD, GBPUSD, EURUSD, USDJPY, BTCUSDT, ETHUSDT, SOLUSDT)')
    parser.add_argument('command', choices=['backtest'], help='Command to run')
    parser.add_argument('start_date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('end_date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--initial-balance', type=float, default=100.0, help='Initial balance')

    args = parser.parse_args()

    print("="*80)
    print(f"VILONA STRATEGY WRAPPER - {args.strategy.upper()}")
    print("="*80)
    print(f"Symbol: {args.symbol}")
    print(f"Period: {args.start_date} to {args.end_date}")
    print(f"Initial Balance: ${args.initial_balance}")
    print("="*80)
    print()

    result = run_backtest(
        args.strategy,
        args.symbol,
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
