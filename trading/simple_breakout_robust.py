#!/usr/bin/env python3
"""
XAUUSD SIMPLE BREAKOUT STRATEGY - ROBUST VERSION
No complex pandas calculations - simple entry/exit logic
"""

import sys
import argparse
import yfinance as yf
import json
from datetime import datetime

def simple_breakout_strategy(df, initial_balance=100, min_range=5, rr_ratio=2.0):
    """
    Simple Breakout Strategy - No complex indicators

    Entry: Previous day's High/Low
    Exit: TP = Entry + (Range × RR), SL = Entry - Range
    Filter: Minimum range filter
    """
    balance = initial_balance
    trades = []
    daily_trades = 0
    last_date = None

    # Sort by date
    df = df.sort_index()

    print("Starting backtest...")
    print(f"Initial Balance: ${balance:.2f}")
    print(f"Strategy: Simple Breakout")
    print(f"Parameters: Min Range {min_range} pips, R/R {rr_ratio}:1")
    print()

    for i in range(1, len(df)):
        row = df.iloc[i]
        current_date = row.name.date()

        # Date tracking for daily trade limit
        if last_date != current_date:
            daily_trades = 0
            last_date = current_date

        # Check daily trade limit
        if daily_trades >= 3:
            continue

        # Get previous day's data
        if i < 1:
            continue

        prev_row = df.iloc[i-1]

        # Calculate range from previous day
        high = prev_row['High']
        low = prev_row['Low']
        prev_close = prev_row['Close']
        range_val = high - low

        # Filter: Only trade if range >= min_range pips (5 pips = 0.0050 for XAUUSD)
        if range_val < min_range / 10000:  # Convert pips to price
            continue

        # Entry points
        buy_stop = high
        sell_stop = low

        # Calculate TP/SL
        tp_long = buy_stop + (range_val * rr_ratio)
        sl_long = low

        tp_short = sell_stop - (range_val * rr_ratio)
        sl_short = high

        # Check entries
        risk_amount = balance * 0.01
        lot_size = 0.01  # Fixed lot size

        # Risk per lot (based on range)
        risk_per_lot = range_val

        if risk_per_lot > 0:
            actual_lot = risk_amount / risk_per_lot
        else:
            actual_lot = lot_size

        # Check if buy stop hit
        if row['High'] >= buy_stop:
            # Long trade
            entry = buy_stop
            tp = tp_long
            sl = sl_long

            # Check exit
            if row['Low'] <= sl:
                pnl = (sl - entry) * actual_lot
                balance += pnl
                trades.append({
                    'date': str(current_date),
                    'type': 'LONG',
                    'entry': entry,
                    'exit': sl,
                    'pnl': pnl,
                    'win': pnl < 0
                })
                daily_trades += 1
            elif row['High'] >= tp:
                pnl = (tp - entry) * actual_lot
                balance += pnl
                trades.append({
                    'date': str(current_date),
                    'type': 'LONG',
                    'entry': entry,
                    'exit': tp,
                    'pnl': pnl,
                    'win': pnl > 0
                })
                daily_trades += 1

        # Check if sell stop hit
        elif row['Low'] <= sell_stop:
            # Short trade
            entry = sell_stop
            tp = tp_short
            sl = sl_short

            # Check exit
            if row['High'] >= sl:
                pnl = (entry - sl) * actual_lot
                balance += pnl
                trades.append({
                    'date': str(current_date),
                    'type': 'SHORT',
                    'entry': entry,
                    'exit': sl,
                    'pnl': pnl,
                    'win': pnl < 0
                })
                daily_trades += 1
            elif row['Low'] <= tp:
                pnl = (entry - tp) * actual_lot
                balance += pnl
                trades.append({
                    'date': str(current_date),
                    'type': "SHORT",
                    'entry': entry,
                    'exit': tp,
                    'pnl': pnl,
                    'win': pnl > 0
                })
                daily_trades += 1

        # Exit at session end (every 20 candles = 1 day in real trading)
        # For backtest, we don't exit, but for paper trading we would

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

    max_drawdown = 0
    peak = initial_balance
    for t in trades:
        peak += t['pnl']
        dd = ((peak - peak) / peak * 100) if peak != 0 else 0
        max_drawdown = max(max_drawdown, dd)

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
        'pair': 'XAUUSD',
        'strategy': 'Simple Breakout',
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
    parser = argparse.ArgumentParser(description='XAUUSD Simple Breakout Strategy - Robust Version')
    parser.add_argument('action', choices=['backtest'], help='Action')
    parser.add_argument('--symbol', default='GC=F', help='Trading symbol')
    parser.add_argument('--start-date', default='2025-01-01', help='Start date')
    parser.add_argument('--end-date', default='2025-12-31', help='End date')
    parser.add_argument('--initial-balance', type=float, default=100, help='Initial balance')

    args = parser.parse_args()

    if args.action == 'backtest':
        print("="*80)
        print("XAUUSD SIMPLE BREAKOUT STRATEGY BACKTEST")
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
        results = simple_breakout_strategy(df, args.initial_balance)

        # Print results
        print()
        print("="*80)
        print("BACKTEST RESULTS")
        print("="*80)
        print(f"Initial Balance: ${results['initial_balance']:.2f}")
        print(f"Final Balance: ${results['final_balance']:.2f}")
        print(f"Net PNL: ${results['net_pnl']:.2f}")
        print(f"Return: {results['net_pnl']/results['initial_balance']*100:.1f}%")
        print()
        print(f"Total Trades: {results['total_trades']}")
        print(f"Wins: {results['wins']}")
        print(f"Losses: {results['losses']}")
        print(f"Win Rate: {results['win_rate']:.1f}%")
        print()
        print(f"Avg Win: ${results['avg_win']:.2f}")
        print(f"Avg Loss: ${results['avg_loss']:.2f}")
        print(f"Profit Factor: {results['profit_factor']:.1f}")
        print()
        print(f"Max Consecutive Wins: {results['max_consecutive_wins']}")
        print(f"Max Consecutive Losses: {results['max_consecutive_losses']}")
        print(f"Max Drawdown: {results['max_drawdown']:.1f}%")
        print("="*80)
        print()

        # Check profitability
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

        # Save results
        output_file = "/tmp/simple_breakout.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"✅ Results saved to: {output_file}")
        print()

if __name__ == "__main__":
    main()
