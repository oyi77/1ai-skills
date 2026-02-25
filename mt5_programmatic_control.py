#!/usr/bin/env python3
"""
MT5 PROGRAMMATIC CONTROL - XAUUSD TRADING
Connect to MT5 via RPYC and control trading programmatically
"""

import rpyc
from mt5linux import MetaTrader5
import pandas as pd
import json
import time
from datetime import datetime

# Server settings
MT5_HOST = "5.189.138.144"
MT5_PORT = 18812

def connect_to_mt5_programmatic():
    """Connect to MT5 programmatically via RPYC"""
    print("="*80)
    print("MT5 PROGRAMMATIC CONTROL")
    print("="*80)
    print(f"Connecting to {MT5_HOST}:{MT5_PORT}...")
    
    try:
        # Connect via RPYC
        print("1. Establishing RPYC connection...")
        conn = rpyc.classic.connect(MT5_HOST, MT5_PORT)
        print("✅ RPYC connection established!")
        
        # Import MT5 module
        print("2. Loading MT5 module...")
        mt5 = conn.modules['mt5linux.metatrader5']
        print("✅ MT5 module loaded!")
        
        # Initialize MT5
        print("3. Initializing MT5...")
        if mt5.initialize():
            print("✅ MT5 initialized successfully!")
        else:
            print(f"❌ MT5 initialization failed: {mt5.last_error()}")
            return None
        print()
        
        # Get account info
        print("📊 ACCOUNT INFO:")
        acc = mt5.account_info()
        print(f"   Account ID: {acc.id}")
        print(f"   Balance: ${acc.balance:.2f}")
        print(f"   Equity: ${acc.equity:.2f}")
        print(f"   Margin: ${acc.margin:.2f}")
        print(f"   Free Margin: ${acc.free:.2f}")
        print()
        
        # Get terminal info
        print("📊 TERMINAL INFO:")
        ti = mt5.terminal_info()
        print(f"   Connected: {ti.connected}")
        print(f"   Server: {ti.server}")
        print(f"   Build: {ti.build}")
        print(f"   Path: {ti.path}")
        print()
        
        # Get XAUUSD symbol info
        print("📊 XAUUSD SYMBOL INFO:")
        symbol_info = mt5.symbol_info("XAUUSD")
        if symbol_info:
            print(f"   Name: {symbol_info.name}")
            print(f"   Path: {symbol_info.path}")
            print(f"   Trade allowed: {symbol_info.trade_allowed}")
            print(f"   Digits: {symbol_info.digits}")
            print(f"   Point: {symbol_info.point}")
            print(f"   Bid: {symbol_info.bid}")
            print(f"   Ask: {symbol_info.ask}")
            print(f"   Last: {symbol_info.last}")
        print()
        
        # Get recent history
        print("📊 LATEST PRICES:")
        rates = mt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_H1, 0, 5)
        if rates is not None:
            df = pd.DataFrame(rates)
            print(df.to_string(index=False))
        print()
        
        print("="*80)
        print("✅ MT5 CONTROLLABLE PROGRAMMATICALLY!")
        print("="*80)
        print()
        print("Contoh kode trading:")
        print()
        print("from mt5linux import MetaTrader5")
        print("mt5 = MetaTrader5(host='5.189.138.144', port=18812)")
        print("mt5.initialize()")
        print("mt5.symbol_subscribe('XAUUSD')")
        print("mt5.order_send({...})")
        print("mt5.shutdown()")
        print()
        print("="*80)
        
        return conn
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def run_programmatic_trading(conn):
    """Run automated trading programmatically"""
    mt5 = conn.modules['mt5linux.metatrader5']
    
    print()
    print("="*80)
    print("AUTOMATED TRADING (PROGRAMMATIC)")
    print("="*80)
    print()
    
    while True:
        try:
            now = datetime.now()
            hour = now.hour
            
            # Check if Asia session
            if 7 <= hour < 15:
                print(f"{now.strftime('%H:%M:%S')} - Asia session active")
                
                # Get market data
                rates = mt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_H1, 0, 7)
                if rates is not None:
                    df = pd.DataFrame(rates)
                    hh = df['high'].max()
                    ll = df['low'].min()
                    range_val = hh - ll
                    
                    print(f"HH: {hh:.4f}, LL: {ll:.4f}, Range: {range_val:.4f}")
                    
                    if range_val >= 0.50:
                        tp_long = hh + (range_val * 2)
                        sl_long = hh - range_val
                        
                        tp_short = ll - (range_val * 2)
                        sl_short = ll + range_val
                        
                        print(f"✅ SIGNAL: Buy @ {hh:.4f}, Sell @ {ll:.4f}")
                        print(f"   TP Long: {tp_long:.4f}, SL Long: {sl_long:.4f}")
                        print(f"   TP Short: {tp_short:.4f}, SL Short: {sl_short:.4f}")
                        
                        # Place orders programmatically
                        # (This is example code - implement actual order_send)
                        print("   [Place order code here]")
                        print()
                
                time.sleep(3600)  # Wait 1 hour
            else:
                print(f"{now.strftime('%H:%M:%S')} - Outside session")
                time.sleep(300)  # Wait 5 minutes
                
        except KeyboardInterrupt:
            print("\nStopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    conn = connect_to_mt5_programmatic()
    if conn:
        print()
        answer = input("Run automated trading? (y/n): ")
        if answer.lower() == 'y':
            run_programmatic_trading(conn)
        conn.close()
        print("✅ Done!")
