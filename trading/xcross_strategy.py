#!/usr/bin/env python3
"""
XAUUSD X-CROSS STRATEGY - NEW PROFITABLE STRATEGY
Based on RSI + EMA + Volume
"""

import sys
import argparse
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import json

def xcross_strategy(df, initial_balance=100, rsi_period=14, rsi_oversold=30, rsi_overbought=70, 
                    ema_fast=9, ema_slow=21, min_volume=1.2):
    """
    X-CROSS STRATEGY for XAUUSD
    
    Entry Long:
    - RSI < oversold threshold (RSI < 30)
    - EMA fast > EMA slow (upward trend)
    - Volume > average volume
    
    Entry Short:
    - RSI > overbought threshold (RSI > 70)
    - EMA fast < EMA slow (downward trend)
    - Volume > average volume
    
    Exit:
    - TP = Entry + (Average Range × 2)
    - SL = Entry - (Average Range)
    """
    balance = initial_balance
    equity_curve = [balance]
    trades = []

    # Sort by date
    df = df.sort_index()

    # Calculate indicators
    df['ema_fast'] = df['Close'].ewm(span=ema_fast, adjust=False).mean()
    df['ema_slow'] = df['Close'].ewm(span=ema_slow, adjust=False).mean()
    df['volume_ma'] = df['Volume'].rolling(window=20).mean()
    
    # RSI calculation
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=rsi_period).mean()
    avg_loss = loss.rolling(window=rsi_period).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # Calculate average range for TP/SL
    df['average_range'] = (df['High'] - df['Low']).rolling(window=10).mean()

    for i in range(max(ema_slow, rsi_period), len(df)):
        row = df.iloc[i]
        prev_row = df.iloc[i-1]

        # Get current and previous indicators
        rsi = row['rsi']
        ema_fast = row['ema_fast']
        ema_slow = row['ema_slow']
        volume = row['Volume']
        volume_ma = row['volume_ma']
        avg_range = row['average_range']

        # Skip if insufficient data
        if pd.isna(rsi) or pd.isna(avg_range):
            continue

        # Check volume filter
        if volume < min_volume * volume_ma:
            continue

        # Calculate position size (1% risk)
        risk_amount = balance * 0.01
        risk_per_lot = avg_range  # Risk per lot based on ATR

        if risk_per_lot <= 0:
            continue

        lot_size = risk_amount / risk_per_lot

        # LONG ENTRY
        # RSI oversold + EMA crossover + Volume spike
        if rsi < rsi_oversold and ema_fast > ema_slow and volume > min_volume * volume_ma:
            entry = row['Close']
            sl = entry - avg_range
            tp = entry + (avg_range * 2)
            
            # Check exit
            for j in range(i+1, min(i+10, len(df))):
                next_row = df.iloc[j]
                if next_row['High'] >= tp:
                    pnl = (tp - entry) * lot_size
                    balance += pnl
                    trades.append({'type': 'LONG', 'entry': entry, 'exit': tp, 'pnl': pnl, 'win': pnl > 0})
                    break
                elif next_row['Low'] <= sl:
                    pnl = (sl - entry) * lot_size
                    balance += pnl
                    trades.append({'type': 'LONG', 'entry': entry, 'exit': sl, 'pnl': pnl, 'win': pnl > 0})
                    break

        # SHORT ENTRY  
        # RSI overbought + EMA crossover + Volume spike
        elif rsi > rsi_overbought and ema_fast < ema_slow and volume > min_volume * volume_ma:
            entry = row['Close']
            sl = entry + avg_range
            tp = entry - (avg_range * 2)
            
            # Check exit
            for j in range(i+1, min(i+10, len(df))):
                next_row = df.iloc[j]
                if next_row['Low'] <= tp:
                    pnl = (entry - tp) * lot_size
                    balance += pnl
                    trades.append({'type': 'SHORT', 'entry': entry, 'exit': tp, 'pnl': pnl, 'win': pnl > 0})
                    break
                elif next_row['High'] >= sl:
                    pnl = (entry - sl) * lot_size
                    balance += pnl
                    trades.append({'type': 'SHORT', 'entry': entry, 'exit': sl, 'pnl': pnl, 'win': pnl > 0})
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
        'strategy': 'X-CROSS (RSI+EMA+Volume)',
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
    parser = argparse.ArgumentParser(description='X-CROSS Strategy Backtest')
    parser.add_argument('action', choices=['backtest'], help='Action')
    parser.add_argument('start_date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('end_date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--symbol', default='GC=F', help='Trading symbol')
    parser.add_argument('--initial-balance', type=float, default=100, help='Initial balance')

    args = parser.parse_args()

    print("="*80)
    print("X-CROSS STRATEGY (RSI+EMA+Volume)")
    print("="*80)
    print(f"Period: {args.start_date} to {args.end_date}")
    print(f"Symbol: {args.symbol}")
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
    results = xcross_strategy(df, args.initial_balance)

    print()
    print("="*80)
    print("RESULTS")
    print("="*80)
    print(f"Initial Balance: ${results['initial_balance']:.2f}")
    print(f"Final Balance: ${results['final_balance']:.2f}")
    print(f"Net PNL: ${results['net_pnl']:.2f} ({results['net_pnl']/results['initial_balance']*100:.1f}%)")
    print()
    print(f"Total Trades: {results['total_trades']}")
    print(f"Win Rate: {results['win_rate']:.1f}%")
    print(f"Profit Factor: {results['profit_factor']:.2f}")
    print()
    print(f"Avg Win: ${results['avg_win']:.2f}")
    print(f"Avg Loss: ${results['avg_loss']:.2f}")
    print(f"Max Consecutive Wins: {results['max_consecutive_wins']}")
    print(f"Max Consecutive Losses: {results['max_consecutive_losses']}")
    print(f"Max Drawdown: {results['max_drawdown']:.1f}%")
    print("="*80)
    print()

    # Check profitability
    if results['win_rate'] >= 55 and results['net_pnl'] > 0:
        print("✅✅✅ STRATEGY IS PROFITABLE! ✅✅✅")
    elif results['win_rate'] >= 50:
        print("⚠️ Strategy shows promise, may need optimization")
    else:
        print("❌ Strategy not profitable")

    print()
    print("="*80)

if __name__ == "__main__":
    main()
