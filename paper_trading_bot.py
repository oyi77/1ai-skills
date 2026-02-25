#!/usr/bin/env python3
"""
PAPER TRADING BOT - XAUUSD ASIA 7-CANDLE BREAKOUT
Fully automated 24/7 paper trading simulation
"""

import yfinance as yf
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import signal
import sys

# Configuration
CONFIG = {
    'symbol': 'GC=F',  # XAUUSD futures
    'timeframe': '1h',
    'initial_balance': 10000.0,
    'risk_per_trade': 0.01,  # 1%
    'max_trades_per_day': 3,
    'lot_size': 0.01,
    'pip_value': 0.10,  # $0.10 per pip for 0.01 lot
    'session_start': 7,  # 07:00 Jakarta
    'session_end': 15,   # 15:00 Jakarta
    'candles_count': 7,
    'range_filter_pips': 5,
    'rr_ratio': 2.0,
}

# Journal file
JOURNAL_FILE = Path('/tmp/paper_trading_journal.json')

class PaperTradingBot:
    def __init__(self):
        self.running = True
        self.balance = CONFIG['initial_balance']
        self.equity = CONFIG['initial_balance']
        self.daily_trades = 0
        self.last_trade_date = None
        self.positions = []
        self.trades_history = []
        
        # Load existing journal
        if JOURNAL_FILE.exists():
            with open(JOURNAL_FILE, 'r') as f:
                data = json.load(f)
                self.trades_history = data.get('trades', [])
                self.balance = data.get('final_balance', CONFIG['initial_balance'])
        
        # Setup signal handlers
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)
    
    def shutdown(self, signum, frame):
        print('\n🔴 Shutting down bot...')
        self.running = False
        self.save_journal()
    
    def save_journal(self):
        """Save trading journal"""
        data = {
            'start_date': self.trades_history[0]['date'] if self.trades_history else str(datetime.now().date()),
            'end_date': str(datetime.now().date()),
            'initial_balance': CONFIG['initial_balance'],
            'final_balance': self.balance,
            'total_trades': len(self.trades_history),
            'trades': self.trades_history
        }
        with open(JOURNAL_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f'💾 Journal saved: {JOURNAL_FILE}')
    
    def is_asia_session(self):
        """Check if current time is within Asia session"""
        now = datetime.now()
        return CONFIG['session_start'] <= now.hour < CONFIG['session_end']
    
    def get_market_data(self):
        """Fetch XAUUSD data from yfinance"""
        try:
            ticker = yf.Ticker(CONFIG['symbol'])
            df = ticker.history(period="5d", interval=CONFIG['timeframe'])
            return df
        except Exception as e:
            print(f'❌ Error fetching data: {e}')
            return None
    
    def get_hh_ll(self, df):
        """Get Highest High and Lowest Low"""
        if df is None or len(df) < CONFIG['candles_count']:
            return None, None
        
        candles = df.tail(CONFIG['candles_count'])
        hh = candles['High'].max()
        ll = candles['Low'].min()
        return hh, ll
    
    def check_range_filter(self, hh, ll):
        """Check if range meets minimum filter"""
        range_val = hh - ll
        min_range = CONFIG['range_filter_pips'] / 10000
        return range_val >= min_range, range_val
    
    def simulate_trade(self, trade_type, entry, tp, sl, timestamp):
        """Simulate a trade and track result"""
        lot_size = CONFIG['lot_size']
        pip_value = CONFIG['pip_value']
        
        # Calculate pips
        if trade_type == 'BUY':
            pips_tp = (tp - entry) * 10000  # Convert to pips
            pips_sl = (entry - sl) * 10000
        else:
            pips_tp = (entry - tp) * 10000
            pips_sl = (sl - entry) * 10000
        
        # Calculate potential PnL
        potential_profit = pips_tp * pip_value * lot_size
        potential_loss = pips_sl * pip_value * lot_size
        
        trade = {
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'type': trade_type,
            'entry': round(entry, 4),
            'tp': round(tp, 4),
            'sl': round(sl, 4),
            'lot_size': lot_size,
            'potential_profit': round(potential_profit, 2),
            'potential_loss': round(potential_loss, 2),
            'status': 'OPEN'
        }
        
        return trade
    
    def run(self):
        """Main trading loop"""
        print('='*80)
        print('PAPER TRADING BOT - XAUUSD ASIA 7-CANDLE BREAKOUT')
        print('='*80)
        print(f'Initial Balance: ${CONFIG["initial_balance"]:.2f}')
        print(f'Session: {CONFIG["session_start"]:02d}:00 - {CONFIG["session_end"]:02d}:00 Jakarta')
        print('='*80)
        print()
        
        while self.running:
            try:
                now = datetime.now()
                current_time = now.strftime('%Y-%m-%d %H:%M:%S')
                hour = now.hour
                
                print(f'\n{current_time} - Hour: {hour:02d}', end=' ')
                
                # Check if Asia session
                if self.is_asia_session():
                    print('✅ Asia session')
                    
                    # Reset daily trades
                    today = now.date()
                    if self.last_trade_date != today:
                        self.daily_trades = 0
                        self.last_trade_date = today
                        print(f'📅 New day - Reset trade count')
                    
                    # Fetch market data
                    df = self.get_market_data()
                    
                    if df is not None and not df.empty:
                        # Get HH and LL
                        hh, ll = self.get_hh_ll(df)
                        
                        if hh is not None and ll is not None:
                            passes_filter, range_val = self.check_range_filter(hh, ll)
                            
                            if passes_filter:
                                print(f'✅ Range: {range_val:.4f}')
                                
                                # Calculate TP and SL
                                tp_long = hh + (range_val * CONFIG['rr_ratio'])
                                sl_long = hh - range_val
                                
                                tp_short = ll - (range_val * CONFIG['rr_ratio'])
                                sl_short = ll + range_val
                                
                                print(f'📊 HH: {hh:.4f}, LL: {ll:.4f}')
                                print(f'📊 Buy Stop: {hh:.4f} -> TP: {tp_long:.4f}, SL: {sl_long:.4f}')
                                print(f'📊 Sell Stop: {ll:.4f} -> TP: {tp_short:.4f}, SL: {sl_short:.4f}')
                                
                                # Simulate trades
                                if self.daily_trades < CONFIG['max_trades_per_day']:
                                    # Buy Stop
                                    trade_buy = self.simulate_trade('BUY_STOP', hh, tp_long, sl_long, now)
                                    self.trades_history.append(trade_buy)
                                    
                                    # Sell Stop
                                    trade_sell = self.simulate_trade('SELL_STOP', ll, tp_short, sl_short, now)
                                    self.trades_history.append(trade_sell)
                                    
                                    self.daily_trades += 2
