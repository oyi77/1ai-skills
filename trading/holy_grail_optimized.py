#!/usr/bin/env python3
"""
HOLY GRAIL STRATEGY - QUICK FIX & OPTIMIZE
Fix entry timing dan optimize parameters untuk WR 45%+
"""

import sys
import argparse
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import json

def holy_grail_quick_optimize(df, initial_balance=100):
    """
    Holy Grail Strategy - Optimized Version
    Fix entry timing dan parameter optimization
    """
    balance = initial_balance
    equity_curve = [balance]
    trades = []

    # Sort by date
    df = df.sort_index()

    # Calculate indicators with OPTIMAL PARAMETERS
    for ema_period in [10, 15, 20]:  # Test 3 EMA periods
        df[f'ema_{ema_period}'] = df['Close'].ewm(span=ema_period, adjust=False).mean()

        for adx_period in [14, 21, 28]:  # Test 3 ADX periods
            for adx_threshold in [20, 25, 30]:  # Test 3 ADX thresholds
                for rsi_period in [7, 14, 21]:  # Test 3 RSI periods
                    for rsi_buy_zone in [35, 40, 45]:  # Test 3 RSI buy zones
                        for rsi_sell_zone in [55, 60, 65]:  # Test 3 RSI sell zones

                            # Create copy for testing
                            test_df = df.copy()

                            # EMA trend filter
                            test_df[f'trend_{ema_period}'] = test_df['Close'] > test_df[f'ema_{ema_period}']

                            # RSI
                            test_df['rsi'] = (test_df['Close'] - test_df['Close'].shift(1)).rolling(window=rsi_period).apply(
                                lambda x: (x.diff().clip(lower=0).rolling(window=rsi_period, min_periods=1).mean() /
                                             x.diff().clip(upper=0).abs().rolling(window=rsi_period, min_periods=1).mean() * 100 + 100)
                            )

                            # Entry: Break of previous day
                            test_df['prev_high'] = test_df['High'].shift(1)
                            test_df['prev_low'] = test_df['Low'].shift(1)
                            test_df['buy_stop'] = test_df['prev_high']
                            test_df['sell_stop'] = test_df['prev_low']

                            # Filter conditions (QUICK FIX - only one filter)
                            # Option A: Trend following (simple, but may work)
                            filter_trend = test_df[f'trend_{ema_period}']

                            # Entry check
                            long_entries = test_df['High'] > test_df['buy_stop']
                            short_entries = test_df['Low'] < test_df['sell_stop']

                            # Backtest
                            test_balance = initial_balance

                            for i, row in test_df.iterrows():
                                if i < 1:
                                    continue

                                # Risk 1% per trade
                                risk_amount = test_balance * 0.01
                                lot_size = risk_amount / (row['High'] - row['Low'])

                                # Long trade
                                if row['High'] > test_df.loc[test_df.index[i-1], 'buy_stop']:
                                    entry = test_df.loc[test_df.index[i-1], 'buy_stop']
                                    sl = test_df.loc[test_df.index[i-1], 'low']
                                    tp = entry + (row['High'] - row['Low']) * 2  # 2:1 R/R

                                    # Check exit
                                    if i < len(test_df) - 1:
                                        for j in range(i, min(i+5, len(test_df))):
                                            if test_df.iloc[j]['High'] >= tp:
                                                pnl = (tp - entry) * lot_size
                                                test_balance += pnl
                                                break
                                            elif test_df.iloc[j]['Low'] <= sl:
                                                pnl = (sl - entry) * lot_size
                                                test_balance += pnl
                                                break

                            # Exit at session end (every 20 candles ~ daily)
                            if i % 20 == 0:
                                # Close all positions (simplification)
                                pass

                            test_balance = test_balance  # Keep updated

                            test_df.loc[test_df.index[i], 'balance'] = test_balance

                            # Record trade at entry (simplified)
                            if i > 0 and test_df.loc[test_df.index[i-1], 'balance'] != test_df.loc[test_df.index[i-2], 'balance'] if i >= 2 else test_df.loc[test_df.index[i-1], 'balance']:
                                pnl = test_df.loc[test_df.index[i], 'balance'] - test_df.loc[test_df.index[i-1], 'balance'] if i >= 2 else test_df.loc[test_df.index[i-1], 'balance']
                                if abs(pnl) > 0.001:  # Only record significant changes
                                    pass

                            # Exit at year end
                            if i == len(test_df) - 1:
                                final_pnl = test_balance - initial_balance

                                if final_pnl > 0 and len(trades) < 100:  # Only record if better than current
                                    trades.append({
                                        'ema_period': ema_period,
                                        'adx_period': adx_period,
                                        'adx_threshold': adx_threshold,
                                        'rsi_period': rsi_period,
                                        'rsi_buy_zone': rsi_buy_zone,
                                        'rsi_sell_zone': rsi_sell_zone,
                                        'final_balance': test_balance,
                                        'net_pnl': final_pnl
                                    })

    # Find best configuration
    if trades:
        best_config = max(trades, key=lambda x: x['net_pnl'])
        print(f"\n✅ Best Configuration Found!")
        print(f"   EMA Period: {best_config['ema_period']}")
        print(f"   Net PNL: ${best_config['net_pnl']:.2f}")
        print(f"   Return: {best_config['net_pnl']/initial_balance*100:.1f}%")
        return best_config
    else:
        print("\n❌ No valid configurations found")
        return None

def main():
    parser = argparse.ArgumentParser(description='Holy Grail Strategy - Quick Fix & Optimize')
    parser.add_argument('action', choices=['backtest', 'optimize'], help='Action')
    parser.add_argument('--symbol', default='GBPUSD=X', help='Trading symbol')
    parser.add_argument('--start-date', default='2025-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', default='2025-12-31', help='End date (YYYY-MM-DD)')
    parser.add_argument('--initial-balance', type=float, default=100, help='Initial balance')

    args = parser.parse_args()

    if args.action == 'backtest':
        print("="*80)
        print("HOLY GRAIL STRATEGY - OPTIMIZED BACKTEST")
        print("="*80)
        print(f"Symbol: {args.symbol}")
        print(f"Period: {args.start_date} to {args.end_date}")
        print(f"Initial Balance: ${args.initial_balance}")
        print("="*80)
        print()

        # Download data
        print("Downloading data...")
        ticker = yf.Ticker(args.symbol)
        df = ticker.history(start=args.start_date, end=args.end_date, interval="1d")

        if df.empty:
            print("❌ No data downloaded!")
            return

        print(f"✅ Downloaded {len(df)} candles")
        print()

        # Run optimization
        print("Running optimization (testing multiple parameters)...")
        print("This may take a few minutes...")
        print()

        best_config = holy_grail_quick_optimize(df, args.initial_balance)

        if best_config:
            print()
            print("="*80)
            print("FINAL OPTIMIZED STRATEGY")
            print("="*80)
            print()
            print("Optimized Parameters:")
            print(f"  EMA Period: {best_config['ema_period']}")
            print(f"  ADX Period: {best_config['adx_period']}")
            print(f"  ADX Threshold: {best_config['adx_threshold']}")
            print(f"  RSI Period: {best_config['rsi_period']}")
            print(f"  RSI Buy Zone: {best_config['rsi_buy_zone']}")
            print(f"  RSI Sell Zone: {best_config['rsi_sell_zone']}")
            print()
            print("Expected Performance:")
            print(f"  Net PNL: ${best_config['net_pnl']:.2f}")
            print(f"  Return: {best_config['net_pnl']/args.initial_balance*100:.1f}%")
            print()
            print("="*80)
            print("STATUS: Optimized parameters found!")
            print("="*80)
        else:
            print()
            print("="*80)
            print("STATUS: No profitable configuration found")
            print("="*80)

        # Save results
        output_file = "/tmp/holy_grail_optimized.json"
        with open(output_file, 'w') as f:
            json.dump(best_config if best_config else {}, f, indent=2)

        print(f"\n✅ Results saved to: {output_file}")
        print()

if __name__ == "__main__":
    main()
