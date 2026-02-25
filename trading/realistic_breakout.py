#!/usr/bin/env python3
"""
XAUUSD REALISTIC BREAKOUT STRATEGY
Versi yang lebih realistis dengan proper SL dan risk management
"""

import sys
import argparse
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import json

def realistic_breakout_strategy(df, initial_balance=100, min_range=5, rr_ratio=1.5, 
                                   risk_per_trade=0.01, max_trades_per_day=3):
    """
    Realistic Breakout Strategy
    
    Entry: Previous day's High/Low break
    Filter: Min range + Trend filter + Volatility filter
    Exit: TP = Entry + (Range × RR), SL = Entry - Range
    Risk: 1% per trade, max 3 trades/day
    Proper SL: Always set, stop loss is inevitable
    """
    balance = initial_balance
    equity_curve = [balance]
    trades = []
    daily_trades = 0
    last_date = None

    # Sort by date
    df = df.sort_index()

    # Calculate indicators
    df['ema_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['ema_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['volatility'] = df['Close'].rolling(window=14).std()

    for i in range(1, len(df)):
        row = df.iloc[i]
        current_date = row.name.date()

        # Date tracking for daily trade limit
        if last_date != current_date:
            daily_trades = 0
            last_date = current_date

        # Check daily trade limit
        if daily_trades >= max_trades_per_day:
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
        vol = row['Volatility']

        # FILTERS
        # 1. Min range filter
        if range_val < min_range / 10000:  # Convert pips to price
            continue

        # 2. Trend filter (only trade with trend)
        # Check EMA 20 vs EMA 50 to determine trend
        trend_up = row['ema_20'] > row['ema_50']
        trend_down = row['ema_20'] < row['ema_50']

        # 3. Volatility filter (avoid choppy market)
        avg_vol = df['volatility'].iloc[max(0, i-14):i]
        if vol > avg_vol * 2:  # Too volatile, avoid
            continue

        # Entry points
        buy_stop = high
        sell_stop = low

        # Entry conditions
        long_entry = (row['Open'] > buy_stop) and trend_up and (vol < avg_vol * 2)
        short_entry = (row['Open'] < sell_stop) and trend_down and (vol < avg_vol * 2)

        # Risk management
        risk_amount = balance * risk_per_trade
        lot_size = risk_amount / range_val

        # Backtest
        if long_entry:
            entry = buy_stop
            tp = entry + (range_val * rr_ratio)
            sl = entry - range_val

            # Check exit
            for j in range(i, min(i+20, len(df))):
                future_row = df.iloc[j]

                if future_row['Low'] <= sl:
                    pnl = (sl - entry) * lot_size
                    balance += pnl
                    trades.append({
                        'date': str(current_date),
                        'type': 'LONG',
                        'entry': entry,
                        'exit': sl,
                        'pnl': pnl,
                        'win': False
                    })
                    daily_trades += 1
                    break
                elif future_row['High'] >= tp:
                    pnl = (tp - entry) * lot_size
                    balance += pnl
                    trades.append({
                        'date': str(current_date),
                        'type': 'LONG',
                        'entry': entry,
                        'exit': tp,
                        'pnl': pnl,
                        'win': True
                    })
                    daily_trades += 1
                    break

        elif short_entry:
            entry = sell_stop
            tp = entry - (range_val * rr_ratio)
            sl = entry + range_val

            # Check exit
            for j in range(i, min(i+20, len(df))):
                future_row = df.iloc[j]

                if future_row['High'] >= sl:
                    pnl = (entry - sl) * lot_size
                    balance += pnl
                    trades.append({
                        'date': str(current_date),
                        'type': 'SHORT',
                        'entry': entry,
                        'exit': sl,
                        'pnl': pnl,
                        'win': False
                    })
                    daily_trades += 1
                    break
                elif future_row['Low'] <= tp:
                    pnl = (tp - entry) * lot_size
                    balance += pnl
                    trades.append({
                        'date': str(current_date),
                        'type': 'SHORT',
                        'entry': entry,
                        'exit': tp,
                        'pnl': pnl,
                        'win': True
                    })
                    daily_trades += 1
                    break

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

    avg_win = (total_profit / total_wins) if total_wins > 0 else 0
    avg_loss = (total_loss / total_losses) if total_losses > 0 else 0

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

    return {
        'pair': 'XAUUSD',
        'strategy': 'Realistic Breakout',
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
        'max_drawdown': max_drawdown,
        'parameters': {
            'min_range_pips': min_range,
            'rr_ratio': rr_ratio,
            'risk_per_trade': risk_per_trade,
            'max_trades_per_day': max_trades_per_day
        }
    }

def main():
    parser = argparse.ArgumentParser(description='XAUUSD Realistic Breakout Strategy Backtest')
    parser.add_argument('action', choices=['backtest', 'optimize'], help='Action')
    parser.add_argument('--symbol', default='GC=F', help='Trading symbol')
    parser.add_argument('--start-date', default='2025-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', default='2025-12-31', help='End date (YYYY-MM-DD)')
    parser.add_argument('--initial-balance', type=float, default=100, help='Initial balance')

    args = parser.parse_args()

    if args.action == 'backtest':
        print("="*80)
        print("XAUUSD REALISTIC BREAKOUT STRATEGY BACKTEST")
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
        results = realistic_breakout_strategy(df, args.initial_balance)

        # Print results
        print()
        print("="*80)
        print("BACKTEST RESULTS")
        print("="*80)
        print(f"Initial Balance: ${results['initial_balance']:.2f}")
        print(f"Final Balance: ${results['final_balance']:.2f}")
        print(f"Net PNL: ${results['net_pnl']:.2f}")
        print(f"Return: {results['net_pnl']/results['initial_balance']*100:.2f}%")
        print()
        print(f"Total Trades: {results['total_trades']}")
        print(f"Wins: {results['wins']}")
        print(f"Losses: {results['losses']}")
        print(f"Win Rate: {results['win_rate']:.2f}%")
        print()
        print(f"Avg Win: ${results['avg_win']:.2f}")
        print(f"Avg Loss: ${results['avg_loss']:.2f}")
        print(f"Profit Factor: {results['profit_factor']:.2f}")
        print()
        print(f"Max Consecutive Wins: {results['max_consecutive_wins']}")
        print(f"Max Consecutive Losses: {results['max_consecutive_losses']}")
        print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
        print()
        print("Parameters:")
        print(f"  Min Range: {results['parameters']['min_range_pips']} pips")
        print(f"  R/R Ratio: {results['parameters']['rr_ratio']}")
        print(f"  Risk/Trade: {results['parameters']['risk_per_trade']*100}%")
        print(f"  Max Trades/Day: {results['parameters']['max_trades_per_day']}")
        print("="*80)
        print()

        # Check profitability
        if results['win_rate'] >= 55 and results['net_pnl'] > 0:
            print("🎯 RECOMMENDATION: Strategy is profitable!")
            print("   This is more realistic than the 100% version")
        elif results['win_rate'] >= 50:
            print("⚠️ Strategy shows promise. Optimize parameters.")
        else:
            print("❌ Strategy not profitable. Reconsider approach.")

        print()
        print("="*80)
        print("COMPLETE")
        print("="*80)

        # Save results
        output_file = "/tmp/realistic_breakout.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"✅ Results saved to: {output_file}")
        print()

if __name__ == "__main__":
    main()
