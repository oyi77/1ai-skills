#!/usr/bin/env python3
"""
XAUUSD CONSERVATIVE TREND STRATEGY
Fokus pada risk management ketat dan win rate tinggi
"""

import sys
import argparse
import yfinance as yf
import json
from datetime import datetime

def conservative_trend_strategy(df, initial_balance=100, risk_per_trade=0.005, max_trades_per_day=2):
    """
    Conservative Trend Strategy - Ketat Risk Management
    
    Strategy: Trend following dengan tight stops
    Entry: EMA crossover confirmation
    Exit: TP 1.5x range, SL at swing low
    Risk: 0.5% per trade (lebih konservatif)
    """
    balance = initial_balance
    equity_curve = [balance]
    trades = []
    daily_trades = 0
    last_date = None

    # Sort by date
    df = df.sort_index()

    # Calculate EMA untuk trend following
    df['ema_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['ema_50'] = df['Close'].ewm(span=50, adjust=False).mean()

    for i in range(max(50, 2), len(df)):  # Mulai dari candle 50 untuk data cukup
        row = df.iloc[i]
        current_date = row.name.date()

        # Date tracking
        if last_date != current_date:
            daily_trades = 0
            last_date = current_date

        # Daily trade limit (konservatif: hanya 2 trade/hari)
        if daily_trades >= max_trades_per_day:
            continue

        # Trend following: EMA 20 > EMA 50 = uptrend
        if row['ema_20'] <= row['ema_50']:
            continue  # Downtrend atau sideways, skip

        # Range filter (minimal 10 pips untuk mengurangi noise)
        prev_row = df.iloc[i-1]
        range_val = prev_row['High'] - prev_row['Low']

        if range_val < 0.0010:  # 10 pips minimum
            continue

        # Entry: Buy stop di previous high (breakout setup)
        entry = prev_row['High']

        # Risk ketat: 0.5% dari balance
        risk_amount = balance * risk_per_trade

        # Lot size berdasarkan risk
        risk_per_lot = range_val

        if risk_per_lot <= 0:
            continue

        lot_size = risk_amount / risk_per_lot

        # TP dan SL yang konservatif
        # R/R 1.5:1 (lebih kecil dari 2:1 biasanya)
        tp = entry + (range_val * 1.5)
        sl = entry - range_val  # SL dekat (quick exit)

        # Backtest
        for j in range(i, min(i+20, len(df))):
            future_row = df.iloc[j]

            # Check if TP hit
            if future_row['High'] >= tp:
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

            # Check if SL hit
            elif future_row['Low'] <= sl:
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

            # Jika 20 candle tidak hit TP/SL, exit at close
            elif j == i + 19:
                pnl = (future_row['Close'] - entry) * lot_size
                balance += pnl
                trades.append({
                    'date': str(current_date),
                    'type': 'LONG',
                    'entry': entry,
                    'exit': future_row['Close'],
                    'pnl': pnl,
                    'win': pnl > 0
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

    max_drawdown = 0
    peak = max(equity_curve)
    trough = min(equity_curve)
    max_drawdown = ((peak - trough) / peak * 100) if peak > 0 else 0

    return {
        'pair': 'XAUUSD',
        'strategy': 'Conservative Trend',
        'initial_balance': initial_balance,
        'final_balance': balance,
        'net_pnl': net_pnl,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'total_trades': total_trades,
        'wins': total_wins,
        'losses': total_losses,
        'max_drawdown': max_drawdown
    }

def main():
    parser = argparse.ArgumentParser(description='XAUUSD Conservative Trend Strategy')
    parser.add_argument('action', choices=['backtest'], help='Action')
    parser.add_argument('--symbol', default='GC=F', help='Trading symbol')
    parser.add_argument('--start-date', default='2025-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', default='2025-12-31', help='End date (YYYY-MM-DD)')
    parser.add_argument('--initial-balance', type=float, default=100, help='Initial balance')

    args = parser.parse_args()

    print("="*80)
    print("XAUUSD CONSERVATIVE TREND STRATEGY")
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
    results = conservative_trend_strategy(df, args.initial_balance)

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
    print(f"Profit Factor: {results['profit_factor']:.2f}")
    print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
    print("="*80)
    print()

    # Check profitability
    if results['win_rate'] >= 55 and results['net_pnl'] > 0:
        print("✅✅✅ STRATEGY IS PROFITABLE! ✅✅✅")
        print("   Target: WR ≥ 55%, PNL positive")
        print("   Result: Both criteria met!")
        print()
        print("🎯 RECOMMENDATION:")
        print("   Consider this strategy for live trading!")
        print("   Conservative approach with tight risk management.")
    elif results['win_rate'] >= 50:
        print("⚠️ Strategy shows promise. Optimize parameters.")
        print("   Current WR ≥ 50%, but not yet profitable.")
    else:
        print("❌ Strategy not profitable. Reconsider approach.")

    print()
    print("="*80)
    print("COMPLETE")
    print("="*80)

    # Save results
    output_file = "/tmp/conservative_trend.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"✅ Results saved to: {output_file}")
    print()

if __name__ == "__main__":
    main()
