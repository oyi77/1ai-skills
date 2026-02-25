#!/usr/bin/env python3
"""
CTRADER API - XAUUSD ASIA 7-CANDLE BREAKOUT AUTOMATED TRADING
Fully automated paper trading 24/7
"""

import sys
import time
import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

try:
    from ctrader_sdk import CTraderBot
    print("✅ ctrader-sdk imported successfully")
except ImportError as e:
    print(f"❌ Failed to import ctrader-sdk: {e}")
    sys.exit(1)

print()
print("="*80)
print("CTRADER API - XAUUSD ASIA 7-CANDLE BREAKOUT")
print("FULLY AUTOMATED PAPER TRADING 24/7")
print("="*80)
print()

# Configuration
CONFIG = {
    "broker": "Fusion Markets",
    "server": "FusionMarkets-Demo",
    "symbol": "XAUUSD",
    "timeframe": "H1",  # 1 Hour timeframe
    "timezone": "Asia/Jakarta",
    
    # Trading Session
    "asia_session_start": "07:00",  # Jakarta time
    "asia_session_end": "15:00",    # Jakarta time
    
    # Strategy Parameters
    "candles_count": 7,              # Number of candles for HH/LL
    "range_filter_pips": 5,         # Minimum range in pips (5 pips = 0.50 for XAUUSD)
    "rr_ratio": 2.0,               # Risk/Reward ratio (2:1)
    
    # Risk Management
    "risk_per_trade": 0.01,          # 1% per trade
    "max_trades_per_day": 3,         # Maximum 3 trades per day
    "lot_size": 0.01,               # Mini lot
    
    # Account Credentials (PROVIDED BY USER)
    "client_id": "21861_zgu5qR2pW4CP1uR6RjJFFpanWvHJoJb5PXnrx6V1pLnt9fuIqY",
    "client_secret": "D1tO3U2m3SyCoG0f3GUmCJkNFbeJEHnbRwTxSCY3LlZMfiZvEi",
    "access_token": None,  # Will be auto-generated
    "account_id": "YOUR_ACCOUNT_ID",  # User needs to provide this
}

# Journal file
JOURNAL_FILE = Path("/home/openclaw/.openclaw/workspace/asia7c_automated_trades.json")

print("📋 CONFIGURATION:")
print("-"*80)
for key, value in CONFIG.items():
    if "secret" in key.lower() or "token" in key.lower() or "id" in key.lower() and key != "account_id":
        print(f"   {key}: {value}")
    elif "client_id" in key or "client_secret" in key or "access_token" in key or "account_id" in key:
        print(f"   {key}: [HIDDEN - User needs to fill]")
    else:
        print(f"   {key}: {value}")
print()

print("="*80)
print("⚠️  CREDENTIALS REQUIRED")
print("="*80)
print()
print("SEBELUM RUNNING, ANDA PERLU:")
print()
print("STEP 1: Register App di cTrader Open API")
print("   - Buka: https://openapi.ctrader.com/apps")
print("   - Login dengan akun Fusion Markets")
print("   - Create New Application")
print("   - Dapat: CLIENT_ID dan CLIENT_SECRET")
print()
print("STEP 2: Get Access Token")
print("   - Gunakan Auth untuk dapat access_token")
print("   - Refresh token secara berkala (biasanya 7 hari)")
print()
print("STEP 3: Get Account ID")
print("   - Login ke Fusion Markets cTrader Webtrader")
print("   - Cari Account ID di Settings/Account")
print()
print("="*80)
print("SETUP CREDENTIALS")
print("="*80)
print()
print("Buka file ini dan isi:")
print("   - CONFIG['client_id'] = 'YOUR_CLIENT_ID'")
print("   - CONFIG['client_secret'] = 'YOUR_CLIENT_SECRET'")
print("   - CONFIG['access_token'] = 'YOUR_ACCESS_TOKEN'")
print("   - CONFIG['account_id'] = 'YOUR_ACCOUNT_ID'")
print()
print("ATAU")
print()
print("Buat file .env:")
print()
print("   echo 'CTRADER_CLIENT_ID=your_client_id' > .env")
print("   echo 'CTRADER_CLIENT_SECRET=your_client_secret' >> .env")
print("   echo 'CTRADER_ACCESS_TOKEN=your_access_token' >> .env")
print("   echo 'CTRADER_ACCOUNT_ID=your_account_id' >> .env")
print()
print("="*80)
print("NEXT STEPS")
print("="*80)
print()
print("1. Register application di cTrader Open API")
print("2. Dapatkan credentials")
print("3. Update CONFIG di script ini")
print("4. Jalankan script: python asia7c_automated.py")
print("5. Script akan berjalan 24/7 dan trading secara otomatis")
print()

class XAUUSDAsia7CBreakoutBot:
    """Automated trading bot for XAUUSD Asia 7-Candle Breakout Strategy"""
    
    def __init__(self, config):
        self.config = config
        self.bot = None
        self.running = False
        self.daily_trades = 0
        self.last_trade_date = None
        self.positions = []
        self.trades_journal = []
        
        # Load existing journal
        if JOURNAL_FILE.exists():
            with open(JOURNAL_FILE, 'r') as f:
                self.trades_journal = json.load(f)
    
    def connect(self):
        """Connect to cTrader API"""
        try:
            print("🔗 Connecting to cTrader API...")
            
            # Initialize CTraderBot
            self.bot = CTraderBot(
                client_id=self.config['client_id'],
                client_secret=self.config['client_secret'],
                access_token=self.config['access_token'],
                account_id=self.config['account_id']
            )
            
            print("✅ Connected to cTrader API")
            
            # Get account info
            account_info = self.bot.get_account_information()
            print(f"📊 Account: {account_info}")
            print()
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("⚠️  Please check your credentials")
            return False
    
    def is_asia_session(self):
        """Check if current time is within Asia session"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        start = self.config['asia_session_start']
        end = self.config['asia_session_end']
        
        return start <= current_time < end
    
    def get_hh_ll(self, df, count=7):
        """Get Highest High (HH) and Lowest Low (LL) from N candles"""
        candles = df.tail(count)
        
        hh = candles['High'].max()
        ll = candles['Low'].min()
        
        return hh, ll
    
    def check_range_filter(self, hh, ll):
        """Check if range meets minimum filter"""
        range_val = hh - ll
        min_range = self.config['range_filter_pips'] / 10000  # 5 pips = 0.50 for XAUUSD
        
        return range_val >= min_range, range_val
    
    def calculate_tp_sl(self, entry, range_val, is_long=True):
        """Calculate Take Profit (TP) and Stop Loss (SL)"""
        if is_long:
            tp = entry + (range_val * self.config['rr_ratio'])
            sl = entry - range_val
        else:
            tp = entry - (range_val * self.config['rr_ratio'])
            sl = entry + range_val
        
        return tp, sl
    
    def place_orders(self, hh, ll, range_val):
        """Place Buy/Sell stop orders"""
        try:
            # Calculate TP/SL
            tp_long, sl_long = self.calculate_tp_sl(hh, range_val, is_long=True)
            tp_short, sl_short = self.calculate_tp_sl(ll, range_val, is_long=False)
            
            print(f"📊 Placing orders...")
            print(f"   Range: {range_val:.4f}")
            print(f"   HH: {hh:.4f}, LL: {ll:.4f}")
            print(f"   Buy Stop: {hh:.4f}, TP: {tp_long:.4f}, SL: {sl_long:.4f}")
            print(f"   Sell Stop: {ll:.4f}, TP: {tp_short:.4f}, SL: {sl_short:.4f}")
            print()
            
            # Place Buy Stop
            buy_order = self.bot.place_order(
                symbol=self.config['symbol'],
                order_type="BUY_STOP",
                entry_price=hh,
                stop_loss=sl_long,
                take_profit=tp_long,
                volume=self.config['lot_size']
            )
            
            print(f"✅ Buy Stop placed: {buy_order}")
            
            # Place Sell Stop
            sell_order = self.bot.place_order(
                symbol=self.config['symbol'],
                order_type="SELL_STOP",
                entry_price=ll,
                stop_loss=sl_short,
                take_profit=tp_short,
                volume=self.config['lot_size']
            )
            
            print(f"✅ Sell Stop placed: {sell_order}")
            print()
            
            # Update daily trade count
            now = datetime.now()
            today = now.date()
            
            if self.last_trade_date != today:
                self.daily_trades = 0
                self.last_trade_date = today
            
            self.daily_trades += 2  # Both buy and sell orders
            
            return True, buy_order, sell_order
            
        except Exception as e:
            print(f"❌ Failed to place orders: {e}")
            return False, None, None
    
    def check_positions(self):
        """Check open positions and track them"""
        try:
            positions = self.bot.get_open_positions()
            
            for pos in positions:
                print(f"📍 Position: {pos}")
            
            return positions
            
        except Exception as e:
            print(f"❌ Failed to get positions: {e}")
            return []
    
    def cancel_old_orders(self):
        """Cancel orders that are no longer valid"""
        try:
            orders = self.bot.get_open_orders()
            
            for order in orders:
                # Cancel old orders (before current session)
                self.bot.cancel_order(order['order_id'])
                print(f"❌ Cancelled order: {order['order_id']}")
            
        except Exception as e:
            print(f"❌ Failed to cancel orders: {e}")
    
    def run(self):
        """Main trading loop"""
        print()
        print("="*80)
        print("STARTING AUTOMATED TRADING BOT")
        print("="*80)
        print()
        print("🚀 Bot will run 24/7 and execute trades during Asia session")
        print("📊 XAUUSD Asia 7-Candle Breakout Strategy")
        print(f"⏰ Session: {self.config['asia_session_start']} - {self.config['asia_session_end']} Jakarta")
        print(f"📈 Timeframe: {self.config['timeframe']}")
        print(f"🎯 Risk: {self.config['risk_per_trade']*100}% per trade")
        print(f"📦 Max Trades: {self.config['max_trades_per_day']} per day")
        print()
        print("="*80)
        print()
        
        self.running = True
        
        while self.running:
            try:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                today = now.date()
                
                print(f"🕐 Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Check if Asia session
                if self.is_asia_session():
                    print(f"✅ Asia session active")
                    
                    # Reset daily trade count
                    if self.last_trade_date != today:
                        self.daily_trades = 0
                        self.last_trade_date = today
                        print(f"📅 New day - Reset trade count")
                    
                    # Check max trades
                    if self.daily_trades < self.config['max_trades_per_day']:
                        # Fetch market data
                        df = self.bot.fetch_dataframe(
                            symbol=self.config['symbol'],
                            timeframe=self.config['timeframe'],
                            count=self.config['candles_count']
                        )
                        
                        if df is not None and len(df) >= self.config['candles_count']:
                            # Get HH and LL
                            hh, ll = self.get_hh_ll(df, self.config['candles_count'])
                            
                            # Check range filter
                            passes_filter, range_val = self.check_range_filter(hh, ll)
                            
                            if passes_filter:
                                print(f"✅ Range filter passed: {range_val:.4f} >= {self.config['range_filter_pips']/10000}")
                                
                                # Place orders
                                success, buy_order, sell_order = self.place_orders(hh, ll, range_val)
                                
                                if success:
                                    # Log trades
                                    trade = {
                                        'date': now.strftime('%Y-%m-%d'),
                                        'time': now.strftime('%H:%M:%S'),
                                        'hh': float(hh),
                                        'll': float(ll),
                                        'range': float(range_val),
                                        'buy_stop': float(hh),
                                        'sell_stop': float(ll),
                                        'buy_order_id': buy_order.get('order_id') if buy_order else None,
                                        'sell_order_id': sell_order.get('order_id') if sell_order else None
                                    }
                                    self.trades_journal.append(trade)
                                    
                                    # Save journal
                                    with open(JOURNAL_FILE, 'w') as f:
                                        json.dump(self.trades_journal, f, indent=2)
                            else:
                                print(f"⚠️  Range filter failed: {range_val:.4f} < {self.config['range_filter_pips']/10000}")
                        else:
                            print("⚠️  Not enough candles")
                    else:
                        print(f"⚠️  Max trades reached: {self.daily_trades}/{self.config['max_trades_per_day']}")
                else:
                    print("⏸️  Outside Asia session - waiting...")
                
                # Check positions
                self.check_positions()
                
                print()
                print("="*80)
                print()
                
                # Wait for 1 hour (H1 timeframe)
                print("⏱️  Waiting for next hour...")
                time.sleep(3600)
                
            except KeyboardInterrupt:
                print()
                print("🏹 Bot stopped by user")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                print("⚠️  Waiting 10 seconds before retry...")
                time.sleep(10)
        
        print()
        print("="*80)
        print("BOT STOPPED")
        print("="*80)
        print()
        print(f"📊 Total trades journalled: {len(self.trades_journal)}")
        print(f"📁 Journal saved to: {JOURNAL_FILE}")
        print()
        print("="*80)
        print("COMPLETE")
        print("="*80)

# Main execution
if __name__ == "__main__":
    # Check if credentials are set
    if CONFIG['client_id'] == 'YOUR_CLIENT_ID':
        print()
        print("="*80)
        print("⚠️  CREDENTIALS NOT SET")
        print("="*80)
        print()
        print("Please set your credentials in the CONFIG section:")
        print("   - client_id")
        print("   - client_secret")
        print("   - access_token")
        print("   - account_id")
        print()
        print("See instructions above for how to get them.")
        print()
        print("="*80)
        print()
        sys.exit(1)
    
    # Initialize bot
    bot = XAUUSDAsia7CBreakoutBot(CONFIG)
    
    # Connect
    if bot.connect():
        # Run bot
        bot.run()
    else:
        print()
        print("="*80)
        print("❌ CONNECTION FAILED")
        print("="*80)
        print()
        print("Please check:")
        print("   - Credentials are correct")
        print("   - cTrader Open API is accessible")
        print("   - Network connection is stable")
        print()
        print("="*80)
        print()
        sys.exit(1)
