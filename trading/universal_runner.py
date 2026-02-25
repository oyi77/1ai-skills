#!/usr/bin/env python3
"""
VILONA UNIVERSAL STRATEGY RUNNER
Wrapper untuk menjalankan SEMUA strategi dengan CLI interface.
"""

import sys
import os
import argparse
import json
import subprocess

# Add current dir to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import strategy modules
from trading.brokers.base import BrokerType, OHLCV
from trading.indicators.moving_averages import EMA
from trading.indicators.adx import ADX, calculate_adx
from trading.indicators.rsi import RSI, calculate_rsi

# Strategy classes
from strategy.templates.forex.holy_grail import HolyGrailStrategy
from strategy.templates.forex.kumo_breakout import KumoBreakoutStrategy
from strategy.templates.forex.momentum_elder import MomentumElderStrategy
from strategy.templates.crypto.volume_momentum import VolumeMomentumStrategy

STRATEGIES = {
    "holy_grail": HolyGrailStrategy,
    "kumo_breakout": KumoBreakoutStrategy,
    "momentum_elder": MomentumElderStrategy,
    "volume_momentum": VolumeMomentumStrategy,
}

# Asset classes for symbol mapping
class AssetClass:
    FOREX = "forex"
    CRYPTO = "crypto"

ASSET_MAPPING = {
    # Forex
    "GBPUSD": {"symbol": "GBP/USD", "yfinance": "GBPUSD=X"},
    "EURUSD": {"symbol": "EUR/USD", "yfinance": "EURUSD=X"},
    "USDJPY": {"symbol": "USD/JPY", "yfinance": "USDJPY=X"},
    # Crypto
    "BTCUSDT": {"symbol": "BTC/USDT", "yfinance": "BTC-USD"},
    "ETHUSDT": {"symbol": "ETH/USDT", "yfinance": "ETH-USD"},
    "SOLUSDT": {"symbol": "SOL/USDT", "yfinance": "SOL-USD"},
    # Commodities
    "XAUUSD": {"symbol": "XAU/USD", "yfinance": "GC=F"},
}

def download_data(symbol, start_date, end_date):
    """Download OHLCV data using yfinance."""
    import yfinance as yf
    import pandas as pd

    ticker = ASSET_MAPPING[symbol]["yfinance"]
    print(f"Downloading {symbol} data...")

    try:
        df = yf.Ticker(ticker).history(start=start_date, end=end_date, interval="1d")
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
        print(f"Error downloading data: {e}")
        return None

def run_backtest(strategy_name, symbol, start_date, end_date, initial_balance):
    """Run backtest for a strategy."""
    strategy_class = STRATEGIES.get(strategy_name)

    if not strategy_class:
        print(f"❌ Strategy '{strategy_name}' not found")
        return None

    try:
        # Initialize strategy
        strategy = strategy_class({
            'symbol': symbol,
            'pair': symbol,
            'timeframe': 'D1',  # Default to daily
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
        return {"error": str(e)}

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
    print(f"VILONA UNIVERSAL RUNNER - {args.strategy} on {args.symbol}")
    print("="*80)

    # Run backtest
    result = run_backtest(
        args.strategy,
        args.symbol,
        args.start_date,
        args.end_date,
        args.initial_balance
    )

    # Output JSON
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
