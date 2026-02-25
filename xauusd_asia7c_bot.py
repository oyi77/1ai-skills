#!/usr/bin/env python3
"""
XAUUSD ASIA 7-CANDLE BREAKOUT AUTOMATED TRADING
Server: 5.189.138.144
Container: mt5linux
"""

import rpyc
import pandas as pd
import time
from datetime import datetime

# RPYC connection to MT5 container
MT5_HOST = "localhost"
MT5_PORT = 18861

# Trading configuration
SYMBOL = "XAUUSD"
TIMEFRAME = 1  # H1 = 1 hour
SESSION_START = 7   # 07:00 Jakarta
SESSION_END = 15    # 15:00 Jakarta
CANDLES_COUNT = 7
RANGE_FILTER_PIPS = 5
RR_RATIO = 2.0

def connect_to_mt5_via_rpyc():
    """Connect to MT5 via RPYC"""
    try:
        conn = rpyc.classic.connect(MT5_HOST, MT5_PORT)
        print("✅ Connected to MT5 RPYC server")
        return conn
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"   MT5_HOST: {MT5_HOST}, MT5_PORT: {MT5_PORT}")
        return None

def get_hh_ll(conn, symbol, timeframe, count):
    """Get HH and LL from MT5"""
    try:
        mt5 = conn.modules['mt5linux.metatrader5']
        
        # Get rates
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None or len(rates) < count:
            return None, None
        
        df = pd.DataFrame(rates)
        hh = df['high'].max()
        ll = df['low'].min()
        
        return hh, ll
    except Exception as e:
        print(f"❌ Error getting HH/LL: {e}")
        return None, None

def place_order(conn, symbol, order_type, entry_price, sl_price, tp_price, volume):
    """Place order via MT5"""
    try:
        mt5 = conn.modules['mt5linux.metatrader5']
        order_send = None
        
        if order_type == 'BUY_STOP':
            order_send = mt5.OrderSend({
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": symbol,
                "volume": volume,
                "type": mt5.ORDER_TYPE_BUY_STOP,
                "price": entry_price,
                "sl": sl_price,
                "tp": tp_price,
                "deviation": 10,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            })
        elif order_type == 'SELL_STOP':
            order_send = mt5.OrderSend({
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": symbol,
                "volume": volume,
                "type": mt5.ORDER_TYPE_SELL_STOP,
                "price": entry_price,
                "sl": sl_price,
                "tp": tp_price,
                "deviation": 10,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            })
        
        if order_send and order_send.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"✅ Order placed: {order_send.order}")
            return True
        else:
            print(f"❌ Order failed: {order_send.retcode} - {order_send.comment}")
            return False
    except Exception as e:
        print(f"❌ Error placing order: {e}")
        return False

def is_asia_session():
    """Check if current time is within Asia session"""
    return SESSION_START <= datetime.now().hour < SESSION_END

def run_strategy(conn):
    """Main trading loop"""
    print("="*80)
    print("XAUUSD ASIA 7-CANDLE BREAKOUT - AUTOMATED TRADING")
    print("="*80)
    print()
    
    while True:
        try:
            now = datetime.now()
            hour = now.hour
            
            print(f"\n{now.strftime('%Y-%m-%d %H:%M:%S')} - Hour: {hour}")
            
            # Check if Asia session
            if is_asia_session():
                print("✅ Asia session active")
                
                # Get HH and LL
                hh, ll = get_hh_ll(conn, SYMBOL, TIMEFRAME, CANDLES_COUNT)
                
                if hh is not None and ll is not None:
                    range_val = hh - ll
                    min_range = RANGE_FILTER_PIPS / 10000
                    
                    if range_val >= min_range:
                        print(f"✅ Range filter passed: {range_val:.4f}")
                        
                        # Calculate TP and SL
                        tp_long = hh + (range_val * RR_RATIO)
                        sl_long = hh - range_val
                        
                        tp_short = ll - (range_val * RR_RATIO)
                        sl_short = ll + range_val
                        
                        print(f"📊 HH: {hh:.4f}, LL: {ll:.4f}")
                        print(f"📊 Range: {range_val:.4f}")
                        print(f"📊 Buy Stop: {hh:.4f}, TP: {tp_long:.4f}, SL: {sl_long:.4f}")
                        print(f"📊 Sell Stop: {ll:.4f}, TP: {tp_short:.4f}, SL: {sl_short:.4f}")
                        
                        # Place orders
                        place_order(conn, SYMBOL, 'BUY_STOP', hh, sl_long, tp_long, 0.01)
                        place_order(conn, SYMBOL, 'SELL_STOP', ll, sl_short, tp_short, 0.01)
                    else:
                        print(f"⚠️  Range filter failed: {range_val:.4f}")
                else:
                    print("⚠️  Not enough candles")
            else:
                print("⏸️  Outside Asia session")
            
            print()
            print("="*80)
            
            # Wait for 1 hour (H1 timeframe)
            print("⏱️  Waiting for next hour...")
            time.sleep(3600)
            
        except KeyboardInterrupt:
            print("\n❌ Bot stopped by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("⚠️  Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    conn = connect_to_mt5_via_rpyc()
    if conn:
        run_strategy(conn)
        conn.close()
    else:
        print("❌ Connection failed. Start MT5 container first.")
