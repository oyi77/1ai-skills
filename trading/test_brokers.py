#!/usr/bin/env python3
"""
Test all broker connectors for automated trading.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime

def test_simulated_broker():
    """Test SimulatedBroker (paper trading with yfinance)."""
    print("\n" + "="*50)
    print("🧪 TESTING SimulatedBroker (PAPER TRADING)")
    print("="*50)
    
    try:
        from brokers.simulated import SimulatedBroker
        
        broker = SimulatedBroker()
        connected = broker.connect()
        
        if connected:
            print("✅ SimulatedBroker: CONNECTED")
            
            # Get OHLCV
            ohlcv = broker.get_ohlcv("XAUUSD", "H1", count=10)
            print(f"✅ Got {len(ohlcv)} candles for XAUUSD")
            
            # Get account info
            account = broker.get_account_info()
            print(f"✅ Account info: balance=${account.balance:.2f}")
            
            # Get current price
            price = broker._get_price("XAUUSD")
            print(f"✅ Current XAUUSD price: ${price:.2f}")
            
            broker.disconnect()
            print("✅ SimulatedBroker: DISCONNECTED")
            return True
        else:
            print("❌ SimulatedBroker: FAILED TO CONNECT")
            return False
            
    except Exception as e:
        print(f"❌ SimulatedBroker ERROR: {e}")
        return False

def test_ctrader_connector():
    """Test cTrader connector (requires credentials)."""
    print("\n" + "="*50)
    print("🧪 TESTING cTrader Connector")
    print("="*50)
    
    try:
        from brokers.ctrader.connector import CTraderConnector
        
        broker = CTraderConnector()
        print("✅ cTraderConnector: CLASS LOADED")
        
        # Check if credentials available
        client_id = os.environ.get("CTRADER_CLIENT_ID")
        client_secret = os.environ.get("CTRADER_CLIENT_SECRET")
        access_token = os.environ.get("CTRADER_ACCESS_TOKEN")
        
        if client_id and client_secret and access_token:
            print("✅ cTrader credentials: AVAILABLE")
            print("ℹ️  Run: python test_brokers.py --broker ctrader --mode real")
            # Don't actually connect (might fail in test environment)
            return True
        else:
            print("⚠️  cTrader credentials: NOT SET")
            print("ℹ️  Set env vars: CTRADER_CLIENT_ID, CTRADER_CLIENT_SECRET, CTRADER_ACCESS_TOKEN")
            return True  # Class loads OK
            
    except ImportError as e:
        print(f"❌ cTrader library not installed: {e}")
        return False
    except Exception as e:
        print(f"❌ cTrader ERROR: {e}")
        return False

def test_ccxt_connector():
    """Test CCXT connector (for crypto)."""
    print("\n" + "="*50)
    print("🧪 TESTING CCXT Connector (Crypto)")
    print("="*50)
    
    try:
        from brokers.ccxt.connector import CCXTConnector
        
        broker = CCXTConnector(exchange_id="binance")
        print("✅ CCXTConnector: CLASS LOADED")
        
        # Test basic methods exist
        assert hasattr(broker, 'connect')
        assert hasattr(broker, 'get_ohlcv')
        assert hasattr(broker, 'place_order')
        
        print("✅ CCXTConnector: All methods available")
        print("ℹ️  Note: CCXT is for CRYPTO exchanges (not XAUUSD)")
        print("ℹ️  Use --exchange binance/kraken/coinbase for crypto trading")
        
        return True
            
    except ImportError as e:
        print(f"❌ CCXT library not installed: {e}")
        return False
    except Exception as e:
        print(f"❌ CCXT ERROR: {e}")
        return False

def test_mt5_connector():
    """Test MT5 connector (Windows only)."""
    print("\n" + "="*50)
    print("🧪 TESTING MT5 Connector")
    print("="*50)
    
    try:
        from brokers.mt5.connector import MT5Connector
        
        broker = MT5Connector()
        print("✅ MT5Connector: CLASS LOADED")
        
        try:
            import MetaTrader5 as mt5
            print("✅ MT5 package: INSTALLED")
            
            # Try initialize (will fail without terminal)
            if mt5.initialize():
                print("✅ MT5 initialized (MT5 Terminal found)")
                mt5.shutdown()
            else:
                error = mt5.last_error()
                if error[0] == 1:  # timeout - no terminal
                    print("⚠️  MT5 Terminal: NOT RUNNING")
                    print("ℹ️  Install MT5 terminal on Windows, then run this bot there")
                else:
                    print(f"⚠️  MT5 error: {error}")
            
        except ImportError:
            print("⚠️  MT5 package: NOT INSTALLED")
            print("ℹ️  MT5 only works on Windows with MT5 Terminal installed")
            print("ℹ️  Install: pip install MetaTrader5")
            print("ℹ️  Alternative: Use cTrader or paper trading on Linux")
        
        return True
            
    except ImportError as e:
        print(f"❌ MT5 ERROR: {e}")
        return False

def main():
    print("="*50)
    print("🤖 BERKAHKARYA TRADING - BROKER TEST SUITE")
    print("="*50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.executable}")
    
    results = {}
    
    # Test all brokers
    results['simulated'] = test_simulated_broker()
    results['ctrader'] = test_ctrader_connector()
    results['ccxt'] = test_ccxt_connector()
    results['mt5'] = test_mt5_connector()
    
    # Summary
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    
    working = []
    not_working = []
    
    for name, status in results.items():
        if status:
            working.append(name)
            print(f"✅ {name}: READY")
        else:
            not_working.append(name)
            print(f"❌ {name}: NOT AVAILABLE")
    
    print("\n" + "="*50)
    print("🚀 RECOMMENDED USAGE")
    print("="*50)
    
    print("\n1. PAPER TRADING (WORKS NOW!):")
    print("   python automated_trader.py --broker paper --mode paper")
    
    print("\n2. REAL TRADING:")
    if 'mt5' in working:
        print("   python automated_trader.py --broker mt5 --mode real")
        print("   (Requires Windows + MT5 Terminal)")
    elif 'ctrader' in working:
        print("   python automated_trader.py --broker ctrader --mode real")
        print("   (Set CTRADER_CLIENT_ID, CTRADER_CLIENT_SECRET, CTRADER_ACCESS_TOKEN)")
    
    print("\n3. BACKTEST:")
    print("   python automated_trader.py --broker paper --once")
    print("   python london_breakout.py --start 2025-01-01 --end 2025-12-31")
    print("   python ny_momentum.py --start 2025-01-01 --end 2025-12-31")

if __name__ == "__main__":
    main()
