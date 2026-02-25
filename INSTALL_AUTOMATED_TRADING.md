# AUTOMATED TRADING SYSTEM - INSTALLATION GUIDE

## Server Info
- **IP:** 5.189.138.144
- **VNC:** http://5.189.138.144:6081/vnc.html
- **VNC Password:** raimuasu
- **RPYC Port:** 18812

## Step 1: Access MT5 via VNC

1. Open browser: http://5.189.138.144:6081/vnc.html
2. Enter password: `raimuasu`
3. You should see MT5 Windows desktop
4. **Login to Fusion Markets:**
   - Username: Openclaw@12
   - Password: 10100262
   - Server: FusionMarkets-Demo

## Step 2: Install Required Packages on Local Computer

```bash
pip3 install rpyc pandas numpy mt5linux
```

## Step 3: Create Trading Bot

Create file: `xauusd_asia7c_bot.py`

```python
#!/usr/bin/env python3
"""
XAUUSD ASIA 7-CANDLE BREAKOUT - AUTOMATED TRADING
Connects to MT5 via RPYC on server 5.189.138.144:18812
"""

from mt5linux import MetaTrader5
import pandas as pd
import time
from datetime import datetime

# Server connection
MT5_HOST = "5.189.138.144"
MT5_PORT = 18812

# Trading configuration
SYMBOL = "XAUUSD"
TIMEFRAME = 1  # H1
SESSION_START = 7   # 07:00 Jakarta
SESSION_END = 15    # 15:00 Jakarta
CANDLES_COUNT = 7
RANGE_FILTER_PIPS = 5
RR_RATIO = 2.0

def connect_to_mt5():
    """Connect to MT5 via RPYC"""
    print(f"Connecting to {MT5_HOST}:{MT5_PORT}...")
    mt5 = MetaTrader5(host=MT5_HOST, port=MT5_PORT)
    
    if mt5.initialize():
        print("✅ Connected to MT5!")
        acc = mt5.account_info()
        print(f"📊 Account ID: {acc.id}")
        print(f"📊 Balance: ${acc.balance:.2f}")
        return mt5
    else:
        print(f"❌ Connection failed")
        return None

def get_hh_ll(mt5, symbol, timeframe, count):
    """Get Highest High and Lowest Low"""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) < count:
        return None, None
    
    df = pd.DataFrame(rates)
    return df['high'].max(), df['low'].min()

def is_asia_session():
    """Check if Asia session"""
    return SESSION_START <= datetime.now().hour < SESSION_END

def run_strategy(mt5):
    """Main trading loop"""
    print("\n" + "="*80)
    print("XAUUSD ASIA 7-CANDLE BREAKOUT - AUTOMATED TRADING")
    print("="*80 + "\n")
    
    while True:
        try:
            now = datetime.now()
            print(f"{now.strftime('%Y-%m-%d %H:%M:%S')}", end=" ")
            
            if is_asia_session():
                print("✅ Asia session")
                hh, ll = get_hh_ll(mt5, SYMBOL, TIMEFRAME, CANDLES_COUNT)
                
                if hh and ll:
                    range_val = hh - ll
                    if range_val >= RANGE_FILTER_PIPS/10000:
                        print(f"HH: {hh:.4f}, LL: {ll:.4f}, Range: {range_val:.4f}")
                        # Implement your trading logic here
                    else:
                        print(f"Range too small: {range_val:.4f}")
                else:
                    print("No data")
            else:
                print("⏸️ Outside session")
            
            time.sleep(3600)  # Wait 1 hour
            
        except KeyboardInterrupt:
            print("\n❌ Stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)
    
    mt5.shutdown()

if __name__ == "__main__":
    mt5 = connect_to_mt5()
    if mt5:
        run_strategy(mt5)
    else:
        print("Failed to connect")
```

## Step 4: Run Trading Bot

```bash
python3 xauusd_asia7c_bot.py
```

## Quick Test

Before running the bot, test the connection:

```python
from mt5linux import MetaTrader5

mt5 = MetaTrader5(host="5.189.138.144", port=18812)
if mt5.initialize():
    print("✅ Connected!")
    acc = mt5.account_info()
    print(f"Account: {acc.id}")
    print(f"Balance: ${acc.balance}")
    mt5.shutdown()
else:
    print("❌ Failed")
```

## Troubleshooting

If connection fails:
1. Check if container running: `docker ps | grep mt5linux`
2. Check RPYC port: Make sure port 18812 is exposed
3. Check VNC: http://5.189.138.144:6081/vnc.html
4. Restart container if needed
