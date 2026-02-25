#!/usr/bin/env python3
"""
PAPER TRADING BOT V2 - SIMPLIFIED
XAUUSD Asia 7-Candle Breakout
"""

import yfinance as yf
import pandas as pd
import json
import time
from datetime import datetime
from pathlib import Path
import os

# Set timezone to Asia/Jakarta
os.environ['TZ'] = 'Asia/Jakarta'

# Config
SYMBOL = 'GC=F'
SESSION_START = 7   # 07:00 Jakarta
SESSION_END = 15    # 15:00 Jakarta

def main():
    print('='*80)
    print('PAPER TRADING BOT - XAUUSD Asia 7-Candle Breakout')
    print('='*80)
    print()
    
    while True:
        try:
            now = datetime.now()
            hour = now.hour
            
            print(f'{now.strftime("%Y-%m-%d %H:%M:%S")} - Hour: {hour:02d}', end=' ')
            
            if SESSION_START <= hour < SESSION_END:
                print('✅ Asia session')
                
                # Fetch data
                ticker = yf.Ticker(SYMBOL)
                df = ticker.history(period="5d", interval="1h")
                
                if not df.empty:
                    # Get last 7 candles
                    candles = df.tail(7)
                    hh = candles['High'].max()
                    ll = candles['Low'].min()
                    range_val = hh - ll
                    
                    if range_val >= 0.50:  # 5 pips
                        print(f'Range: {range_val:.4f}, HH: {hh:.4f}, LL: {ll:.4f}')
                        print(f'📊 SIGNAL: Buy @ {hh:.4f}, Sell @ {ll:.4f}')
                    else:
                        print(f'Range too small: {range_val:.4f}')
                else:
                    print('No data')
            else:
                print('⏸️ Outside session')
            
            print()
            time.sleep(3600)  # 1 hour
            
        except Exception as e:
            print(f'Error: {e}')
            time.sleep(60)

if __name__ == '__main__':
    main()
