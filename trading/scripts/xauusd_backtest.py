#!/usr/bin/env python3
"""
XAUUSD Backtest Script
Period: 2025-01-01 to 2026-01-01 (or today if future)
Initial Balance: $100
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import sys

# Configuration
SYMBOL = "XAUUSD"
INITIAL_BALANCE = 100.0
START_DATE = "2025-01-01"
END_DATE = "2026-01-01"

def download_data():
    """Download XAUUSD historical data."""
    print(f"Downloading {SYMBOL} data from {START_DATE} to {END_DATE}...")
    
    # XAUUSD di yfinance = ^XAUUSD atau GC=F (Gold Futures)
    ticker = yf.Ticker("GC=F")
    
    # Download daily data
    df = ticker.history(start=START_DATE, end=END_DATE, interval="1d")
    
    if df.empty:
        print("No data downloaded!")
        return None
    
    print(f"Downloaded {len(df)} bars")
    return df

def simple_breakout_strategy(df, lookback=20, tp_pct=0.02, sl_pct=0.01):
    """
    Simple breakout strategy:
    - Buy when price breaks above high of last 'lookback' days
    - Sell when price breaks below low of last 'lookback' days
    - TP: 2%, SL: 1%
    """
    trades = []
    position = None
    entry_price = 0
    entry_time = None
    
    for i, (idx, row) in enumerate(df.iterrows()):
        high = row['High']
        low = row['Low']
        close = row['Close']
        volume = row['Volume']
        
        if i < lookback:
            continue
        
        # Calculate lookback levels
        lookback_high = df['High'].iloc[i-lookback:i].max()
        lookback_low = df['Low'].iloc[i-lookback:i].min()
        
        # Entry signals
        if position is None:
            # Long signal: price breaks above lookback high
            if close > lookback_high:
                position = 'long'
                entry_price = close
                entry_time = idx
                trades.append({
                    'pair': SYMBOL,
                    'entry_time': str(idx),
                    'exit_time': None,
                    'entry_price': entry_price,
                    'exit_price': None,
                    'pnl_usd': None,
                    'pnl_points': None,
                    'win': None
                })
        
        # Exit signals
        elif position == 'long':
            # TP or SL hit
            if close >= entry_price * (1 + tp_pct):
                pnl_pct = tp_pct
                win = True
            elif close <= entry_price * (1 - sl_pct):
                pnl_pct = -sl_pct
                win = False
            elif close < lookback_low:
                # Exit on breakdown
                pnl_pct = (close - entry_price) / entry_price
                win = pnl_pct > 0
            else:
                continue  # Still in position
            
            pnl_usd = INITIAL_BALANCE * pnl_pct
            pnl_points = (close - entry_price) / 0.01  # Gold point = $0.01 per 0.01 move
            
            # Update last trade
            trades[-1]['exit_time'] = str(idx)
            trades[-1]['exit_price'] = close
            trades[-1]['pnl_usd'] = round(pnl_usd, 2)
            trades[-1]['pnl_points'] = round(pnl_points, 2)
            trades[-1]['win'] = win
            
            position = None
            entry_price = 0
    
    # Close any open position at end
    if position is not None and len(trades) > 0:
        last_close = df.iloc[-1]['Close']
        pnl_pct = (last_close - entry_price) / entry_price
        pnl_usd = INITIAL_BALANCE * pnl_pct
        pnl_points = (last_close - entry_price) / 0.01
        
        trades[-1]['exit_time'] = str(df.index[-1])
        trades[-1]['exit_price'] = last_close
        trades[-1]['pnl_usd'] = round(pnl_usd, 2)
        trades[-1]['pnl_points'] = round(pnl_points, 2)
        trades[-1]['win'] = pnl_usd > 0
    
    return trades

def analyze_trades(trades):
    """Analyze trading results."""
    if not trades:
        return None
    
    total_trades = len(trades)
    win_count = sum(1 for t in trades if t.get('win', False))
    loss_count = total_trades - win_count
    
    pnl_usd_list = [t['pnl_usd'] for t in trades if t['pnl_usd'] is not None]
    pnl_points_list = [t['pnl_points'] for t in trades if t['pnl_points'] is not None]
    
    gross_profit = sum(p for p in pnl_usd_list if p > 0)
    gross_loss = sum(abs(p) for p in pnl_usd_list if p < 0)
    net_pnl = sum(pnl_usd_list)
    
    wins = [p for p in pnl_usd_list if p > 0]
    losses = [p for p in pnl_usd_list if p < 0]
    
    avg_win = gross_profit / len(wins) if wins else 0
    avg_loss = gross_loss / len(losses) if losses else 0
    
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf') if gross_profit > 0 else 0
    
    # Calculate drawdown
    equity = INITIAL_BALANCE
    peak = INITIAL_BALANCE
    max_drawdown = 0
    
    for t in pnl_usd_list:
        equity += t
        if equity > peak:
            peak = equity
        drawdown = peak - equity
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    return {
        'total_trades': total_trades,
        'win_count': win_count,
        'loss_count': loss_count,
        'win_rate': (win_count / total_trades * 100) if total_trades > 0 else 0,
        'gross_profit': round(gross_profit, 2),
        'gross_loss': round(-gross_loss, 2),
        'net_pnl': round(net_pnl, 2),
        'avg_win': round(avg_win, 2),
        'avg_loss': round(-avg_loss, 2),
        'profit_factor': round(profit_factor, 2),
        'max_drawdown': round(max_drawdown, 2),
        'max_drawdown_pct': round((max_drawdown / INITIAL_BALANCE) * 100, 2) if INITIAL_BALANCE > 0 else 0,
        'initial_balance': INITIAL_BALANCE,
        'ending_balance': round(INITIAL_BALANCE + net_pnl, 2),
        'pairs': [SYMBOL]
    }

def print_summary(metrics):
    """Print formatted summary."""
    if not metrics:
        print("No trades to summarize!")
        return
    
    return_pct = ((metrics['ending_balance'] - metrics['initial_balance']) / metrics['initial_balance'] * 100)
    
    print()
    print("=" * 60)
    print(f"{'XAUUSD BACKTEST SUMMARY':^60}")
    print("=" * 60)
    print(f"PERIOD            : {START_DATE} to 2026-01-01")
    print(f"STRATEGY          : Breakout (lookback=20, TP=2%, SL=1%)")
    print("-" * 60)
    print(f"PAIR              : {SYMBOL}")
    print(f"Total Trades      : {metrics['total_trades']}")
    print(f"Win Rate          : {metrics['win_rate']:.2f}%")
    print("-" * 60)
    print("BALANCE")
    print(f"  Initial Balance : ${metrics['initial_balance']:,.2f}")
    print(f"  Ending Balance  : ${metrics['ending_balance']:,.2f}")
    print(f"  Net PNL         : ${metrics['net_pnl']:,.2f} ({return_pct:+.2f}%)")
    print("-" * 60)
    print("DRAWDOWN")
    print(f"  Max Drawdown    : ${metrics['max_drawdown']:,.2f} ({metrics['max_drawdown_pct']:.2f}%)")
    print("-" * 60)
    print("PNL (USD)")
    print(f"  Gross Profit    : ${metrics['gross_profit']:,.2f}")
    print(f"  Gross Loss      : ${metrics['gross_loss']:,.2f}")
    print(f"  Avg Win         : ${metrics['avg_win']:,.2f}")
    print(f"  Avg Loss        : ${metrics['avg_loss']:,.2f}")
    print("-" * 60)
    print(f"PROFIT FACTOR     : {metrics['profit_factor']:.2f}")
    print("=" * 60)

def main():
    print(f"\nXAUUSD Backtest")
    print(f"Period: {START_DATE} to 2026-01-01")
    print(f"Initial Balance: ${INITIAL_BALANCE}")
    
    # Download data
    df = download_data()
    if df is None:
        print("Failed to download data!")
        sys.exit(1)
    
    # Show data info
    print(f"\nData range: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")
    print(f"Price range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
    
    # Run backtest
    print("\nRunning breakout strategy backtest...")
    trades = simple_breakout_strategy(df)
    
    if not trades:
        print("No trades generated!")
        sys.exit(0)
    
    print(f"Generated {len(trades)} trades")
    
    # Analyze results
    metrics = analyze_trades(trades)
    
    # Print summary
    print_summary(metrics)
    
    return metrics, trades

if __name__ == "__main__":
    main()
