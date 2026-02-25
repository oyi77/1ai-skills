#!/usr/bin/env python3
"""
XAUUSD PURE PRICE ACTION STRATEGY - Simplified & Robust
Focus on profitable chart patterns - no complex indicators
"""

import sys
import argparse
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import json

def price_action_strategy(df, initial_balance=100, risk_per_trade=0.01, 
                           range_filter_pips=5, rr_ratio=2.0):
    """
    Pure Price Action Strategy - Chart Patterns
    
    Patterns:
    1. Engulfing (Bullish/Bearish)
    2. Pin Bar (Hammer/Shooting Star)
    3. Inside Bar Breakout
    4. Outside Bar Reversal
    5. Morning/Evening Star
    
    Filters:
    - Range filter (minimum volatility)
    - Trend filter (EMA 50)
    - Time filter (Asia session)
    
    Risk:
    - 1% per trade
    - 2:1 R/R ratio
    - Max 3 trades/day
    """
    balance = initial_balance
    equity_curve = [balance]
    trades = []
    daily_trades = 0
    last_date = None

    # Sort by date
    df = df.sort_index()

    # Calculate EMA for trend filter
    df['ema_50'] = df['Close'].ewm(span=50, adjust=False).mean()

    for i in range(2, len(df)):
        row = df.iloc[i]
        prev_row = df.iloc[i-1]
        prev2_row = df.iloc[i-2]

        # Date tracking
        current_date = row.name.date()
        if last_date != current_date:
            daily_trades = 0
            last_date = current_date

        # Daily trade limit
        if daily_trades >= 3:
            continue

        # Get candles for pattern recognition
        candles = df.iloc[i-3:i+1]  # 4 candles
        
        # Time filter: Asia session (00:00-08:00 UTC = 07:00-15:00 Jakarta)
        if current_date.hour() < 0 or current_date.hour() >= 8:
            continue  # Skip non-Asia session

        # Calculate range for volatility filter
        high = candles['High'].max()
        low = candles['Low'].min()
        range_val = high - low

        # Filter: Minimum range (avoid choppy market)
        if range_val < range_filter_pips / 10000:  # 5 pips = 0.0050 for XAUUSD
            continue

        # Trend filter (only trade with trend)
        trend_up = prev_row['Close'] > prev_row['ema_50']
        trend_down = prev_row['Close'] < prev_row['ema_50']

        # PATTERN RECOGNITION
        pattern = None
        signal_type = None
        entry_price = None

        # 1. ENGFING PATTERN (Bullish)
        if (candles.iloc[1]['Close'] > candles.iloc[0]['Open'] and  # Bullish
            candles.iloc[1]['Open'] < candles.iloc[0]['Close'] and  # Bearish body
            candles.iloc[1]['Close'] > candles.iloc[0]['Close']):  # Body fully engulfing
            
            pattern = 'BULLISH_ENGULFING'
            signal_type = 'LONG'
            entry_price = candles.iloc[0]['Open']

        # 2. ENGFING PATTERN (Bearish)
        elif (candles.iloc[1]['Open'] < candles.iloc[0]['Open'] and  # Bearish
              candles.iloc[1]['Open'] > candles.iloc[0]['Close'] and  # Bullish body
              candles.iloc[1]['Close'] < candles.iloc[0]['Close']):  # Body fully engulfing
            
            pattern = 'BEARISH_ENGULFING'
            signal_type = 'SHORT'
            entry_price = candles.iloc[0]['Open']

        # 3. PIN BAR (Hammer - Bullish Reversal)
        elif (candles.iloc[1]['Close'] > candles.iloc[0]['Open'] and  # Bearish body
              abs(candles.iloc[1]['Close'] - candles.iloc[0]['Close']) < abs(candles.iloc[0]['Open'] - candles.iloc[0]['Close']) and  # Small body
              candles.iloc[1]['High'] < candles.iloc[0]['High'] and  # No upper wick
              candles.iloc[1]['Close'] > candles.iloc[0]['Close']):  # Lower wick > body
              prev2_row['Close'] < candles.iloc[0]['Close']):  # Previous candle bearish
            
            pattern = 'HAMMER_BULLISH'
            signal_type = 'LONG'
            entry_price = candles.iloc[0]['Open']

        # 4. PIN BAR (Shooting Star - Bearish Reversal)
        elif (candles.iloc[1]['Open'] > candles.iloc[0]['Open'] and  # Bullish body
              abs(candles.iloc[1]['Close'] - candles.iloc[0]['Close']) < abs(candles.iloc[0]['Open'] - candles.iloc[0]['Close']) and  # Small body
              candles.iloc[1]['Low'] > candles.iloc[0]['Low'] and  # No lower wick
              candles.iloc[1]['Close'] < candles.iloc[0]['Close']):  # Upper wick > body
              prev2_row['Close'] > candles.iloc[0]['Close']):  # Previous candle bullish
            
            pattern = 'SHOOTING_STAR_BEARISH'
            signal_type = 'SHORT'
            entry_price = candles.iloc[0]['Open']

        # 5. INSIDE BAR BREAKOUT (Trend Continuation)
        elif (candles.iloc[1]['High'] < candles.iloc[0]['High'] and  # Lower high
              candles.iloc[1]['Low'] > candles.iloc[0]['Low'] and  # Higher low
              candles.iloc[1]['Close'] < candles.iloc[0]['Close'] and  # Close lower
              candles.iloc[1]['Close'] > candles.iloc[0]['Open']):  # No gap
            
            pattern = 'INSIDE_BAR_BREAKOUT'
            signal_type = 'LONG'
            entry_price = candles.iloc[0]['High']

        # 6. OUTSIDE BAR REVERSAL (Trend Change)
        elif (candles.iloc[1]['High'] > candles.iloc[0]['High'] and  # Higher high
              candles.iloc[1]['Low'] < candles.iloc[0]['Low'] and  # Lower low
              candles.iloc[1]['Close'] > candles.iloc[0]['Open']):  # Bullish
            
            pattern = 'OUTSIDE_BAR_REVERSAL'
            signal_type = 'LONG'
            entry_price = candles.iloc[0]['Close']

        # 7. MORNING STAR (Bullish Trend)
        elif (candles.iloc[1]['Open'] < candles.iloc[0]['Close'] and  # Small body
              candles.iloc[1]['Close'] > candles.iloc[0]['Open'] and  # Bullish
              candles.iloc[1]['High'] < candles.iloc[0]['High'] and  # Lower wick
              prev2_row['Close'] < prev_row['Close']):  # Previous 2 candles bearish
            
            pattern = 'MORNING_STAR'
            signal_type = 'LONG'
            entry_price = candles.iloc[0]['Open']

        # If no pattern, skip
        if not pattern:
            continue

        # Trend filter: Only trade with trend
        if signal_type == 'LONG' and not trend_up:
            continue  # Don't buy in downtrend
        if signal_type == 'SHORT' and not trend_down:
            continue  # Don't sell in uptrend

        # Risk management
        risk_amount = balance * risk_per_trade
        lot_size = 0.01

        # Backtest
        if signal_type in ['LONG', 'SHORT']:
            tp = entry_price + (range_val * rr_ratio)
            sl = entry_price - (range_val if signal_type == 'LONG' else -range_val)

            # Check exit
            pnl = 0
            win = False
            exit_reason = None

            for j in range(i, min(i+10, len(df))):
                future_row = df.iloc[j]

                if signal_type == 'LONG':
                    if future_row['Low'] <= sl:
                        pnl = (sl - entry_price) * lot_size
                        exit_reason = 'SL_HIT'
                        win = False
                        break
                    elif future_row['High'] >= tp:
                        pnl = (tp - entry_price) * lot_size
                        exit_reason = 'TP_HIT'
                        win = True
                        break
                    elif j == i + 9:  # Timeout after 10 candles
                        pnl = (future_row['Close'] - entry_price) * lot_size
                        exit_reason = 'TIMEOUT'
                        win = pnl > 0
                        break

                elif signal_type == 'SHORT':
                    if future_row['High'] >= sl:
                        pnl = (entry_price - sl) * lot_size
                        exit_reason = 'SL_HIT'
                        win = False
                        break
                    elif future_row['Low'] <= tp:
                        pnl = (tp - future_row['Close']) * lot_size
                        exit_reason = 'TP_HIT'
                        win = True
                        break
                    elif j == i + 9:  # Timeout after 10 candles
                        pnl = (entry_price - future_row['Close']) * lot_size
                        exit_reason = 'TIMEOUT'
                        win = pnl > 0
                        break

            balance += pnl
            trades.append({
                'date': str(current_date),
                'pattern': pattern,
                'type': signal_type,
                'entry': entry_price,
                'tp': tp if signal_type == 'LONG' else sl if signal_type == 'SHORT' else None,
                'sl': sl if signal_type == 'LONG' else tp if signal_type == 'SHORT' else None,
                'pnl': pnl,
                'win': win,
                'exit_reason': exit_reason
            })
            daily_trades += 1

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

    # Pattern statistics
    pattern_stats = {}
    for t in trades:
        pattern = t['pattern']
        if pattern not in pattern_stats:
            pattern_stats[pattern] = {'wins': 0, 'losses': 0, 'pnl': 0}
        pattern_stats[pattern]['pnl'] += t['pnl']
        if t['win']:
            pattern_stats[pattern]['wins'] += 1
        else:
            pattern_stats[pattern]['losses'] += 1

    # Calculate WR per pattern
    for pattern in pattern_stats:
        wins = pattern_stats[pattern]['wins']
        losses = pattern_stats[pattern]['losses']
        pattern_stats[pattern]['total'] = wins + losses
        pattern_stats[pattern]['wr'] = (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0

    return {
        'pair': 'XAUUSD',
        'strategy': 'Pure Price Action',
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
        'max_consecutive_wins': max([t['win'] for t in trades if t['win']] + [t['win'] for t in trades if t['win']] + [t['win'] for t in trades if t['win']] + [t['win'] for t in trades if t['win']]) if total_wins >= 4 else max([t['win'] for t in trades if t['win']]),  # Max 4 consecutive
        'max_consecutive_losses': max([not t['win'] for t in trades] + [not t['win'] for t in trades] + [not t['win'] for t in trades]),
        'max_drawdown': max_drawdown,
        'pattern_stats': pattern_stats
        'parameters': {
            'range_filter_pips': range_filter_pips,
            'rr_ratio': rr_ratio,
            'risk_per_trade': risk_per_trade
        }
    }

def main():
    parser = argparse.ArgumentParser(description='XAUUSD Pure Price Action Strategy')
    parser.add_argument('action', choices=['backtest'], help='Action')
    parser.add_argument('--symbol', default='GC=F', help='Trading symbol')
    parser.add_argument('--start-date', default='2025-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', default='2025-12-31', help='End date (YYYY-MM-DD)')
    parser.add_argument('--initial-balance', type=float, default=100, help='Initial balance')
    parser.add_argument('--range-filter', type=int, default=5, help='Range filter in pips')

    args = parser.parse_args()

    print("="*80)
    print("XAUUSD PURE PRICE ACTION STRATEGY")
    print("="*80)
    print(f"Pattern Recognition: Engulfing, Pin Bar, Inside/Outside Bar, Morning/Evening Star")
    print(f"Filter: EMA 50 Trend + Range Filter ({args.range_filter} pips)")
    print(f"R/R Ratio: {args.rr_ratio}:1")
    print(f"Risk: 1% per trade")
    print("="*80)
    print()

    # Download data
    print("Downloading XAUUSD data...")
    ticker = yf.Ticker(args.symbol)
    df = ticker.history(start=args.start_date, end=args.end_date, interval="1d")

    if df.empty:
        print("❌ No data downloaded!")
        return

    print(f"✅ Downloaded {len(df)} candles")
    print()

    # Run backtest
    print("Backtesting...")
    results = price_action_strategy(df, args.initial_balance, args.range_filter, args.rr_ratio)

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
    print(f"Profit Factor: {results['profit_factor']:.2f}")
    print()
    print(f"Max Drawdown: {results['max_drawdown']:.1f}%")
    print()
    print("PATTERN STATISTICS:")
    print("-"*80)
    sorted_patterns = sorted(results['pattern_stats'].items(), 
                              key=lambda x: x[1]['wr'], 
                              reverse=True)
    for pattern, stats in sorted_patterns:
        print(f"{pattern}:")
        print(f"  Trades: {stats['total']}")
        print(f"  Win Rate: {stats['wr']:.1f}%")
        print(f"  PNL: ${stats['pnl']:.2f}")
        print(f"  Wins: {stats['wins']}")
        print(f"  Losses: {stats['losses']}")
        print()
    print("="*80)

    # Check profitability
    if results['win_rate'] >= 65 and results['net_pnl'] > 0:
        print("🎯🎯🎯 RECOMMENDATION: STRATEGY IS PROFITABLE! 🎯🎯🎯")
        print("   Pure Price Action beats Asia 7-Candle!")
        print(f"   Win Rate: {results['win_rate']:.1f}% (Target: ≥ 65%)")
        print(f"   Net PNL: ${results['net_pnl']:.2f} (Target: positive)")
        print(f"   Consider for paper trading!")
    elif results['win_rate'] >= 60:
        print("⚠️  Strategy shows promise. Optimize parameters.")
    else:
        print("❌ Strategy not profitable. Reconsider approach.")

    print()
    print("="*80)
    print("COMPLETE")
    print("="*80)

    # Save results
    output_file = "/tmp/price_action_backtest.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"✅ Results saved to: {output_file}")
    print()

if __name__ == "__main__":
    main()
