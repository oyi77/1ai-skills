#!/usr/bin/env python3
"""
KUMO BREAKOUT STRATEGY - Simplified Version
Ichimoku Kumo cloud breakout strategy
"""

import sys
import argparse
import pandas as pd
import yfinance as yf
from datetime import datetime
import json
import numpy as np

def calculate_ichimoku(df, tenkan=9, kijun=26, senkou=52):
    """Calculate Ichimoku Kumo cloud components."""
    # Tenkan-sen (Conversion Line)
    df['tenkan'] = (df['High'].rolling(window=tenkan).max() + df['Low'].rolling(window=tenkan).min()) / 2

    # Kijun-sen (Base Line)
    df['kijun'] = (df['High'].rolling(window=kijun).max() + df['Low'].rolling(window=kijun).min()) / 2

    # Senkou Span A (Leading Span A)
    df['senkou_a'] = ((df['tenkan'] + df['kijun']) / 2).shift(kijun)

    # Senkou Span B (Leading Span B)
    df['senkou_b'] = ((df['High'].rolling(window=senkou).max() + df['Low'].rolling(window=senkou).min()) / 2).shift(kijun)

    # Kumo Cloud (between Senkou A and B)
    df['kumo_upper'] = df[['senkou_a', 'senkou_b']].max(axis=1)
    df['kumo_lower'] = df[['senkou_a', 'senkou_b']].min(axis=1)

    return df

def kumo_breakout_strategy(df, initial_balance=100, min_cloud_size=0.0010, rr_ratio=2.0):
    """
    Kumo Breakout Strategy:
    - Entry: Break above Kumo upper (long), break below Kumo lower (short)
    - Filter: Only trade if cloud width >= min_cloud_size
    - Exit: TP = Entry + (Cloud Width × RR), SL = Entry - Cloud Width
    - Risk: 1% per trade, max 3 trades/day
    """
    balance = initial_balance
    equity_curve = [balance]
    trades = []
    daily_trades_count = 0
    last_date = None

    # Calculate Ichimoku
    df = calculate_ichimoku(df)

    # Sort by date
    df = df.sort_index()

    # Drop NaN values
    df = df.dropna()

    for i in range(1, len(df)):
        current_candle = df.iloc[i]
        prev_candle = df.iloc[i-1]

        # Date tracking for daily trade limit
        current_date = current_candle.name.date()
        if last_date != current_date:
            daily_trades_count = 0
            last_date = current_date

        # Check daily trade limit
        if daily_trades_count >= 3:
            continue

        # Kumo cloud width
        kumo_upper = prev_candle['kumo_upper']
        kumo_lower = prev_candle['kumo_lower']
        cloud_width = kumo_upper - kumo_lower

        # Filter: Minimum cloud size
        if cloud_width < min_cloud_size:
            continue

        # Previous candle was inside cloud
        prev_high = prev_candle['High']
        prev_low = prev_candle['Low']
        prev_inside = (prev_high <= kumo_upper) and (prev_low >= kumo_lower)

        if not prev_inside:
            continue

        # Calculate risk amount (1% of balance)
        risk_amount = balance * 0.01

        # Check for long breakout
        if current_candle['High'] > kumo_upper:
            entry = kumo_upper
            stop_loss = kumo_lower
            take_profit = entry + (cloud_width * rr_ratio)
            risk_per_lot = abs(entry - stop_loss)

            # Calculate position size
            if risk_per_lot > 0:
                lot_size = risk_amount / risk_per_lot
            else:
                lot_size = 0.01

            # Check if TP hit
            if current_candle['High'] >= take_profit:
                pnl = (take_profit - entry) * lot_size
                balance += pnl
                trades.append({
                    'date': str(current_candle.name),
                    'type': 'buy',
                    'entry': entry,
                    'exit': take_profit,
                    'pnl': pnl,
                    'win': True
                })
                daily_trades_count += 1

            # Check if SL hit
            elif current_candle['Low'] <= stop_loss:
                pnl = (stop_loss - entry) * lot_size
                balance += pnl
                trades.append({
                    'date': str(current_candle.name),
                    'type': 'buy',
                    'entry': entry,
                    'exit': stop_loss,
                    'pnl': pnl,
                    'win': False
                })
                daily_trades_count += 1

        # Check for short breakout
        elif current_candle['Low'] < kumo_lower:
            entry = kumo_lower
            stop_loss = kumo_upper
            take_profit = entry - (cloud_width * rr_ratio)
            risk_per_lot = abs(entry - stop_loss)

            # Calculate position size
            if risk_per_lot > 0:
                lot_size = risk_amount / risk_per_lot
            else:
                lot_size = 0.01

            # Check if TP hit
            if current_candle['Low'] <= take_profit:
                pnl = (entry - take_profit) * lot_size
                balance += pnl
                trades.append({
                    'date': str(current_candle.name),
                    'type': 'sell',
                    'entry': entry,
                    'exit': take_profit,
                    'pnl': pnl,
                    'win': True
                })
                daily_trades_count += 1

            # Check if SL hit
            elif current_candle['High'] >= stop_loss:
                pnl = (entry - stop_loss) * lot_size
                balance += pnl
                trades.append({
                    'date': str(current_candle.name),
                    'type': 'sell',
                    'entry': entry,
                    'exit': stop_loss,
                    'pnl': pnl,
                    'win': False
                })
                daily_trades_count += 1

        equity_curve.append(balance)

    # Calculate metrics
    wins = [t for t in trades if t['win']]
    losses = [t for t in trades if not t['win']]

    total_trades = len(trades)
    total_wins = len(wins)
    total_losses = len(losses)
    win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0

    net_pnl = balance - initial_balance

    total_profit = sum(t['pnl'] for t in wins)
    total_loss = abs(sum(t['pnl'] for t in losses))
    profit_factor = (total_profit / total_loss) if total_loss > 0 else 0

    # Max drawdown
    peak = max(equity_curve)
    trough = min(equity_curve)
    max_drawdown = ((peak - trough) / peak * 100) if peak > 0 else 0

    # Consecutive wins/losses
    max_consecutive_wins = 0
    max_consecutive_losses = 0
    current_consecutive_wins = 0
    current_consecutive_losses = 0

    for t in trades:
        if t['win']:
            current_consecutive_wins += 1
            current_consecutive_losses = 0
            max_consecutive_wins = max(max_consecutive_wins, current_consecutive_wins)
        else:
            current_consecutive_losses += 1
            current_consecutive_wins = 0
            max_consecutive_losses = max(max_consecutive_losses, current_consecutive_losses)

    avg_win = (total_profit / total_wins) if total_wins > 0 else 0
    avg_loss = (total_loss / total_losses) if total_losses > 0 else 0

    return {
        'pair': 'XAUUSD',  # Default
        'strategy': 'Kumo Breakout',
        'initial_balance': initial_balance,
        'final_balance': balance,
        'net_pnl': net_pnl,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'total_trades': total_trades,
        'wins': total_wins,
        'losses': total_losses,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'max_consecutive_wins': max_consecutive_wins,
        'max_consecutive_losses': max_consecutive_losses,
        'max_drawdown': max_drawdown
    }

def main():
    parser = argparse.ArgumentParser(description='Kumo Breakout Strategy Backtest')
    parser.add_argument('action', choices=['backtest'], help='Action')
    parser.add_argument('start_date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('end_date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--symbol', default='GC=F', help='Trading symbol (default: Gold)')
    parser.add_argument('--initial-balance', type=float, default=100, help='Initial balance')
    parser.add_argument('--min-cloud-size', type=float, default=0.0010, help='Minimum cloud size')
    parser.add_argument('--rr-ratio', type=float, default=2.0, help='Risk/Reward ratio')

    args = parser.parse_args()

    if args.action == 'backtest':
        print("="*80)
        print("KUMO BREAKOUT STRATEGY BACKTEST")
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

        # Run backtest
        print("Running backtest...")
        results = kumo_breakout_strategy(
            df=df,
            initial_balance=args.initial_balance,
            min_cloud_size=args.min_cloud_size,
            rr_ratio=args.rr_ratio
        )

        # Print results
        print()
        print("="*80)
        print("BACKTEST RESULTS")
        print("="*80)
        print(f"Initial Balance:  ${results['initial_balance']:.2f}")
        print(f"Final Balance:    ${results['final_balance']:.2f}")
        print(f"Net PNL:          ${results['net_pnl']:.2f}")
        print(f"Return:           {results['net_pnl']/results['initial_balance']*100:.1f}%")
        print()
        print(f"Total Trades:     {results['total_trades']}")
        print(f"Wins:            {results['wins']}")
        print(f"Losses:          {results['losses']}")
        print(f"Win Rate:        {results['win_rate']:.1f}%")
        print()
        print(f"Avg Win:         ${results['avg_win']:.2f}")
        print(f"Avg Loss:        ${results['avg_loss']:.2f}")
        print(f"Profit Factor:   {results['profit_factor']:.1f}")
        print()
        print(f"Max Consecutive Wins:  {results['max_consecutive_wins']}")
        print(f"Max Consecutive Losses: {results['max_consecutive_losses']}")
        print(f"Max Drawdown:         {results['max_drawdown']:.1f}%")
        print("="*80)
        print()

        # Save results
        output_file = "/tmp/kumo_breakout_backtest.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"✅ Results saved to: {output_file}")
        print()

        # Recommendation
        if results['win_rate'] >= 55 and results['net_pnl'] > 0:
            print("🎯 RECOMMENDATION: Strategy is profitable!")
            print("   Consider live trading with this strategy.")
        elif results['win_rate'] >= 50:
            print("⚠️  Strategy shows promise. Optimize parameters.")
        else:
            print("❌ Strategy not profitable. Reconsider approach.")

        print()
        print("="*80)
        print("COMPLETE")
        print("="*80)

if __name__ == "__main__":
    main()
