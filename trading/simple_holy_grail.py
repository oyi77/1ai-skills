#!/usr/bin/env python3
"""
VILONA SIMPLIFIED STRATEGY RUNNER
Bypass trading framework - langsung pakai yfinance
"""

import sys
import argparse
import json
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

class SimpleHolyGrail:
    """Simplified Holy Grail strategy (no trading framework dependency)."""

    def __init__(self, config):
        self.config = config
        self.pair = config.get('symbol', 'GBPUSD')
        self.ema_period = config.get('ema_period', 200)
        self.adx_period = config.get('adx_period', 14)
        self.rsi_period = config.get('rsi_period', 14)
        self.adx_threshold = config.get('adx_threshold', 25)
        self.rsi_buy_min = config.get('rsi_buy_min', 30)
        self.rsi_buy_max = config.get('rsi_buy_max', 40)
        self.rsi_sell_min = config.get('rsi_sell_min', 70)
        self.rsi_sell_max = config.get('rsi_sell_max', 80)

    def calculate_ema(self, series, period):
        """Calculate EMA."""
        return series.ewm(span=period, adjust=False).mean()

    def calculate_adx(self, df, period):
        """Calculate ADX."""
        high = df['high']
        low = df['low']
        close = df['close']

        plus_dm = high.diff()
        minus_dm = low.diff()

        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm > 0] = 0

        tr = pd.DataFrame({
            'high': high,
            'low': low
        }).assign(tr=lambda x: x['high'] - x['low'])

        atr = tr['tr'].rolling(window=period).mean()

        plus_di = (plus_dm.rolling(window=period).mean() / atr).fillna(0) * 100
        minus_di = (minus_dm.rolling(window=period).mean() / atr).fillna(0) * 100

        dx = pd.DataFrame({
            'plus_di': plus_di,
            'minus_di': minus_di
        })

        di_diff = abs(dx['plus_di'] - dx['minus_di'])
        di_sum = dx['plus_di'] + dx['minus_di']
        dx = (di_diff / di_sum).fillna(0) * 100

        adx = dx.rolling(window=period).mean()

        return adx

    def calculate_rsi(self, series, period):
        """Calculate RSI."""
        delta = series.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def download_data(self, start_date, end_date):
        """Download data."""
        symbol_map = {
            'GBPUSD': 'GBPUSD=X',
            'EURUSD': 'EURUSD=X',
            'USDJPY': 'USDJPY=X',
            'BTCUSDT': 'BTC-USD',
            'ETHUSDT': 'ETH-USD',
            'SOLUSDT': 'SOL-USD',
            'XAUUSD': 'GC=F',
        }

        yf_symbol = symbol_map.get(self.pair, self.pair)

        print(f"Downloading {self.pair} data...")

        try:
            ticker = yf.Ticker(yf_symbol)
            df = ticker.history(start=start_date, end=end_date, interval="1d")
            print(f"Downloaded {len(df)} bars")

            df = df.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })

            return df

        except Exception as e:
            print(f"Error: {e}")
            return None

    def backtest(self, start_date, end_date, df):
        """Run backtest."""
        if df is None or len(df) == 0:
            return {'error': 'No data available'}

        initial_balance = self.config.get('initial_balance', 100)
        balance = initial_balance
        trades = []

        # Calculate indicators
        df = df.copy()
        df['ema'] = self.calculate_ema(df['close'], self.ema_period)
        df['adx'] = self.calculate_adx(df, self.adx_period)
        df['rsi'] = self.calculate_rsi(df['close'], self.rsi_period)

        # Drop NaN rows
        df = df.dropna()

        for idx, row in df.iterrows():
            if row['adx'] < self.adx_threshold:
                continue

            if self.rsi_buy_min <= row['rsi'] <= self.rsi_buy_max:
                # Buy signal
                entry = row['close']
                stop_loss = entry * 0.99
                take_profit = entry * 1.02

                for future_idx in range(idx + 1, min(idx + 10, len(df))):
                    future_row = df.iloc[future_idx]

                    if future_row['low'] <= stop_loss:
                        pnl = -(entry - stop_loss) * 100
                        balance += pnl
                        trades.append({
                            'type': 'BUY',
                            'entry': entry,
                            'exit': stop_loss,
                            'pnl': pnl,
                            'balance': balance
                        })
                        break

                    elif future_row['high'] >= take_profit:
                        pnl = (take_profit - entry) * 100
                        balance += pnl
                        trades.append({
                            'type': 'BUY',
                            'entry': entry,
                            'exit': take_profit,
                            'pnl': pnl,
                            'balance': balance
                        })
                        break

            elif self.rsi_sell_min <= row['rsi'] <= self.rsi_sell_max:
                # Sell signal
                entry = row['close']
                stop_loss = entry * 1.01
                take_profit = entry * 0.98

                for future_idx in range(idx + 1, min(idx + 10, len(df))):
                    future_row = df.iloc[future_idx]

                    if future_row['high'] >= stop_loss:
                        pnl = -(stop_loss - entry) * 100
                        balance += pnl
                        trades.append({
                            'type': 'SELL',
                            'entry': entry,
                            'exit': stop_loss,
                            'pnl': pnl,
                            'balance': balance
                        })
                        break

                    elif future_row['low'] <= take_profit:
                        pnl = (entry - take_profit) * 100
                        balance += pnl
                        trades.append({
                            'type': 'SELL',
                            'entry': entry,
                            'exit': take_profit,
                            'pnl': pnl,
                            'balance': balance
                        })
                        break

        # Calculate stats
        wins = [t for t in trades if t['pnl'] > 0]
        losses = [t for t in trades if t['pnl'] < 0]

        win_rate = len(wins) / len(trades) * 100 if trades else 0
        total_pnl = sum(t['pnl'] for t in trades)
        gross_profit = sum(t['pnl'] for t in wins)
        gross_loss = abs(sum(t['pnl'] for t in losses))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0

        return {
            'pair': self.pair,
            'period': f"{start_date} to {end_date}",
            'total_trades': len(trades),
            'wins': len(wins),
            'losses': len(losses),
            'win_rate': win_rate,
            'pnl': {
                'points': total_pnl,
                'usd': total_pnl
            },
            'profit_factor': profit_factor,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'final_balance': balance
        }

def main():
    parser = argparse.ArgumentParser(description='Vilona Simplified Strategy Runner')
    parser.add_argument('symbol', help='Trading symbol')
    parser.add_argument('command', choices=['backtest'], help='Command')
    parser.add_argument('start_date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('end_date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--initial-balance', type=float, default=100.0, help='Initial balance')

    args = parser.parse_args()

    print("="*80)
    print(f"VILONA SIMPLIFIED RUNNER - {args.symbol}")
    print("="*80)

    strategy = SimpleHolyGrail({
        'symbol': args.symbol,
        'initial_balance': args.initial_balance
    })

    result = strategy.backtest(args.start_date, args.end_date, None)

    print()
    print("="*80)
    print("RESULTS")
    print("="*80)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
