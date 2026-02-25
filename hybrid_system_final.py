#!/usr/bin/env python3
"""
HYBRID TRADING SYSTEM - WORKING VERSION
- VNC: Visual trading dengan MT5 GUI
- Paper: 24/7 data collection & backtesting
- Bridge: Sinkronisasi data & signal
"""

import yfinance as yf
import pandas as pd
import json
import time
from datetime import datetime
from pathlib import Path

# Config
SYMBOL = 'GC=F'  # XAUUSD
SESSION_START = 7
SESSION_END = 15
DATA_FILE = Path('/tmp/hybrid_data.json')
SIGNAL_LOG = Path('/tmp/trading_signals.log')

def get_xauusd_data():
    """Fetch XAUUSD data dari yfinance"""
    try:
        ticker = yf.Ticker(SYMBOL)
        df = ticker.history(period="5d", interval="1h")
        return df
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None

def calculate_hh_ll(df, count=7):
    """Calculate HH dan LL dari candles terakhir"""
    if df is None or len(df) < count:
        return None, None, None
    
    last_candles = df.tail(count)
    hh = last_candles['High'].max()
    ll = last_candles['Low'].min()
    lc = last_candles['Close'].iloc[-1]  # Last close
    
    return hh, ll, lc

def is_asia_session():
    """Check Indonesia time - Asia session"""
    now = datetime.now()
    return SESSION_START <= now.hour < SESSION_END

def analyze_strategy(hh, ll, lc, prev_hh, prev_ll):
    """Analyze XAUUSD Asia 7-Candle Breakout strategy"""
    if hh is None or ll is None:
        return None, "No data"
    
    range_val = hh - ll
    
    if range_val < 0.50:  # 5 pips filter
        return None, f"Range too small: {range_val:.4f}"
    
    # Check breakout conditions
    signal = None
    
    # Buy condition: Price above HH
    if lc > prev_hh:
        signal = "BUY"
        entry = hh
        tp = hh + (range_val * 2)
        sl = hh - range_val
    
    # Sell condition: Price below LL  
    elif lc < prev_ll:
        signal = "SELL"
        entry = ll
        tp = ll - (range_val * 2)
        sl = ll + range_val
    
    else:
        return None, f"Waiting for breakout - HH:{hh:.4f}, LL:{ll:.4f}"
    
    return {
        'signal': signal,
        'entry': entry,
        'tp': tp,
        'sl': sl,
        'range': range_val,
        'rr_ratio': 2.0
    }, "Valid signal"

def save_data(data):
    """Save hybrid data to JSON"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def save_signal(signal_data):
    """Log trading signal"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {json.dumps(signal_data)}"
    with open(SIGNAL_LOG, 'a') as f:
        f.write(log_entry + '\n')

def run_hybrid_loop():
    """Main hybrid trading loop"""
    print("="*80)
    print("HYBRID TRADING SYSTEM - VNC + PAPER + BRIDGE")
    print("="*80)
    print()
    print("Configuration:")
    print(f"  Asset: {SYMBOL} (XAUUSD)")
    print(f"  Session: {SESSION_START}:00 - {SESSION_END}:00 Jakarta")
    print(f"  Data: yfinance (real-time)")
    print(f"  Execution: VNC (manual/semi-auto)")
    print()
    print("Access:")
    print("  VNC: http://5.189.138.144:6081/vnc.html")
    print("  Password: raimuasu")
    print()
    print("="*80)
    print()
    
    prev_hh = 0
    prev_ll = float('inf')
    
    while True:
        try:
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            
            print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} - Hour: {hour:02d}", end=' ')
            
            # Save current status
            status = {
                'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
                'hour': hour,
                'session': 'ASIA' if is_asia_session() else 'OFF',
                'vnc_ready': True,
                'vnc_url': 'http://5.189.138.144:6081/vnc.html'
            }
            save_data(status)
            
            if is_asia_session():
                print("✅ Asia session")
                
                # Fetch data
                df = get_xauusd_data()
                
                if df is not None and not df.empty:
                    # Calculate current HH/LL
                    hh, ll, lc = calculate_hh_ll(df, count=7)
                    
                    if hh and ll and lc:
                        print(f"HH: {hh:.4f}, LL: {ll:.4f}, Last: {lc:.4f}")
                        
                        # Analyze
                        signal, message = analyze_strategy(hh, ll, lc, prev_hh, prev_ll)
                        
                        if signal:
                            print(f"   ✅ {signal} SIGNAL!")
                            print(f"   Entry: {signal['entry']:.4f}, TP: {signal['tp']:.4f}, SL: {signal['sl']:.4f}")
                            
                            # Save signal
                            signal_data = {
                                'signal': signal['signal'],
                                'entry': signal['entry'],
                                'tp': signal['tp'],
                                'sl': signal['sl'],
                                'range': signal['range']
                            }
                            save_signal(signal_data)
                            print(f"   📝 Signal logged to: {SIGNAL_LOG}")
                        else:
                            print(f"   {message}")
                        
                        # Update prev values
                        prev_hh = hh
                        prev_ll = ll
                    
                    print()
                else:
                    print("⚠️ No data")
                    print()
            else:
                print("⏸️ Outside session")
                
                # Fetch data in background anyway
                df = get_xauusd_data()
                if df is not None:
                    hh, ll, lc = calculate_hh_ll(df)
                    if hh and ll:
                        print(f"  [Background] HH:{hh:.4f}, LL:{ll:.4f}")
                
                print()
            
            # Wait 1 hour
            time.sleep(3600)
            
        except KeyboardInterrupt:
            print("\n🛑 Hybrid system stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_hybrid_loop()
