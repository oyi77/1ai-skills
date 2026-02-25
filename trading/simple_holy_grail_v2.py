#!/usr/bin/env python3
"""
HOLY GRAIL STRATEGY - Simplified Version
Breakout strategy based on high/low of previous day
"""

import sys
import argparse
import pandas as pd
import yfinance as yf
from datetime import datetime
import json

def holy_grail_strategy(df, initial_balance=100, min_range_pips=5, rr_ratio=2.0):
    """
    Holy Grail Strategy:
    - Entry: Buy stop at yesterday's high, Sell stop at yesterday's low
    - Filter: Only trade if daily range >= min_range_pips
    - Exit: TP = Entry + (Range × RR), SL = Entry - Range
    - Risk: 1% per trade, max 3 trades/day
    """
    balance = initial_balance
    equity_curve = [balance]
    trades = []
    daily_trades_count = 0
    last_date = None

    # Sort by date
    df = df.sort_index()

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

        # Calculate range
        high = prev_candle['High']
        low = prev_candle['Low']
        close = prev_candle['Close']
        daily_range = high - low

        # Filter: Minimum range
        if daily_range < min_range_pips / 10000:  # Convert pips to price (assuming 5-decimal pairs)
            continue

        # Calculate risk amount (1% of balance)
        risk_amount = balance * 0.01

        # Entry points
        buy_stop = high
        sell_stop = low

        # Check for long entry
        if current_candle['High'] >= buy_stop:
            entry = buy_stop
            stop_loss = low
            take_profit = entry + (daily_range * rr_ratio)
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

        # Check for short entry
        elif current_candle['Low'] <= sell_stop:
            entry = sell_stop
            stop_loss = high
            take_profit = entry - (daily_range * rr_ratio)
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
        'pair': 'GBPUSD',  # Default
        'strategy': 'Holy Grail',
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
    parser = argparse.ArgumentParser(description='Holy Grail Strategy Backtest')
    parser.add_argument('action', choices=['backtest'], help='Action')
    parser.add_argument('start_date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('end_date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--symbol', default='GBPUSD=X', help='Trading symbol')
    parser.add_argument('--initial-balance', type=float, default=100, help='Initial balance')
    parser.add_argument('--min-range-pips', type=int, default=5, help='Minimum range in pips')
    parser.add_argument('--rr-ratio', type=float, default=2.0, help='Risk/Reward ratio')

    args = parser.parse_args()

    if args.action == 'backtest':
        print("="*80)
        print("HOLY GRAIL STRATEGY BACKTEST")
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
        results = holy_grail_strategy(
            df=df,
            initial_balance=args.initial_balance,
            min_range_pips=args.min_range_pips,
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
        output_file = "/tmp/holy_grail_backtest.json"
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
