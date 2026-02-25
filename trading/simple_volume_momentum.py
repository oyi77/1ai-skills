#!/usr/bin/env python3
"""
VOLUME MOMENTUM STRATEGY - Simplified Version
Volume-based momentum strategy with volume spikes
"""

import sys
import argparse
import pandas as pd
import yfinance as yf
from datetime import datetime
import json
import numpy as np

def calculate_volume_momentum(df, ema_period=20):
    """Calculate volume momentum指标."""
    # Volume EMA
    df['volume_ema'] = df['Volume'].ewm(span=ema_period, adjust=False).mean()

    # Volume momentum: ratio of current volume to EMA
    df['volume_ratio'] = df['Volume'] / df['volume_ema']

    # Price momentum
    df['price_momentum'] = df['Close'].pct_change(periods=3)

    return df

def volume_momentum_strategy(df, initial_balance=100, min_volume_ratio=1.5, min_price_momentum=0.0005, rr_ratio=2.0):
    """
    Volume Momentum Strategy:
    - Entry: High volume spike (volume_ratio >= min) + price momentum in same direction
    - Filter: Only trade if volume ratio and price momentum are strong enough
    - Exit: TP = Entry + (Price Range × RR), SL = Entry - Price Range
    - Risk: 1% per trade, max 3 trades/day
    """
    balance = initial_balance
    equity_curve = [balance]
    trades = []
    daily_trades_count = 0
    last_date = None

    # Calculate volume momentum
    df = calculate_volume_momentum(df)

    # Sort by date
    df = df.sort_index()

    # Drop NaN values
    df = df.dropna()

    for i in range(3, len(df)):
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

        # Current momentum
        volume_ratio = current_candle['volume_ratio']
        price_momentum = current_candle['price_momentum']

        # Filter: Minimum volume and price momentum
        if volume_ratio < min_volume_ratio:
            continue

        # Calculate price range (ATR-like)
        high_low = current_candle['High'] - current_candle['Low']
        range_size = high_low

        if range_size < 0.0001:
            continue

        # Calculate risk amount (1% of balance)
        risk_amount = balance * 0.01

        # Check for long entry (volume up + price up)
        if volume_ratio >= min_volume_ratio and price_momentum > min_price_momentum:
            entry = current_candle['Close']
            stop_loss = entry - range_size
            take_profit = entry + (range_size * rr_ratio)
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

        # Check for short entry (volume up + price down)
        elif volume_ratio >= min_volume_ratio and price_momentum < -min_price_momentum:
            entry = current_candle['Close']
            stop_loss = entry + range_size
            take_profit = entry - (range_size * rr_ratio)
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
        'strategy': 'Volume Momentum',
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
    parser = argparse.ArgumentParser(description='Volume Momentum Strategy Backtest')
    parser.add_argument('action', choices=['backtest'], help='Action')
    parser.add_argument('start_date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('end_date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--symbol', default='GC=F', help='Trading symbol (default: Gold)')
    parser.add_argument('--initial-balance', type=float, default=100, help='Initial balance')
    parser.add_argument('--min-volume-ratio', type=float, default=1.5, help='Minimum volume ratio')
    parser.add_argument('--min-price-momentum', type=float, default=0.0005, help='Minimum price momentum')
    parser.add_argument('--rr-ratio', type=float, default=2.0, help='Risk/Reward ratio')

    args = parser.parse_args()

    if args.action == 'backtest':
        print("="*80)
        print("VOLUME MOMENTUM STRATEGY BACKTEST")
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
        results = volume_momentum_strategy(
            df=df,
            initial_balance=args.initial_balance,
            min_volume_ratio=args.min_volume_ratio,
            min_price_momentum=args.min_price_momentum,
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
        output_file = "/tmp/volume_momentum_backtest.json"
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
