#!/usr/bin/env python3
"""
MT5 Connection Test Script - Enhanced
Tests connection to mt5linux server with better error handling
"""

import sys
import os

# Add trading to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mt5linux import MetaTrader5
from datetime import datetime


def test_connection():
    print("=" * 60)
    print("MT5 Connection Test - Enhanced")
    print("=" * 60)

    # Create connection
    host = "5.189.138.144"
    port = 18812

    print(f"\n[1] Connecting to {host}:{port}...")
    try:
        mt5 = MetaTrader5(host=host, port=port)
        print(f"✓ Connected to MT5")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

    print("\n[2] Initializing MT5...")
    try:
        result = mt5.initialize()
        print(f"  Initialize result: {result}")
        if not result:
            print(f"  Last error: {mt5.last_error()}")
    except Exception as e:
        print(f"✗ Initialize failed: {e}")
        return False

    print("\n[3] Getting terminal info...")
    try:
        terminal = mt5.terminal_info()
        print(f"✓ Terminal info:")
        for key, value in terminal._asdict().items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"✗ Terminal info failed: {e}")

    print("\n[4] Getting account info...")
    try:
        account = mt5.account_info()
        if account:
            print(f"✓ Logged in to account:")
            print(f"  Login: {account.login}")
            print(f"  Server: {account.server}")
            print(f"  Balance: ${account.balance}")
            print(f"  Equity: ${account.equity}")
            print(f"  Currency: {account.currency}")
            print(f"  Leverage: {account.leverage}")
        else:
            print("✗ Not logged in - account_info is None")
            print(f"  Last error: {mt5.last_error()}")
    except Exception as e:
        print(f"✗ Account info failed: {e}")

    print("\n[5] Getting symbols list...")
    try:
        symbols = mt5.symbols_get()
        print(f"✓ Total symbols: {len(symbols)}")

        # Look for XAUUSD
        xauusd = mt5.symbol_info("XAUUSD")
        if xauusd:
            print(f"✓ XAUUSD found:")
            print(f"  Bid: {xauusd.bid}")
            print(f"  Ask: {xauusd.ask}")
            print(f"  Digits: {xauusd.digits}")
        else:
            print("✗ XAUUSD not found")
            # Try to find gold symbols
            gold_symbols = [
                s.name
                for s in symbols
                if "GOLD" in s.name.upper() or "XAU" in s.name.upper()
            ]
            print(f"  Available gold symbols: {gold_symbols[:5]}")
    except Exception as e:
        print(f"✗ Symbols failed: {e}")

    print("\n[6] Getting OHLCV data for XAUUSD...")
    try:
        rates = mt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_H1, 0, 10)
        if rates is not None and len(rates) > 0:
            print(f"✓ Got {len(rates)} candles:")
            for rate in rates[-5:]:
                dt = datetime.fromtimestamp(rate[0])
                print(
                    f"  {dt} O:{rate[1]:.2} H:{rate[2]:.2} L:{rate[3]:.2} C:{rate[4]:.2}"
                )
        else:
            print("✗ No data returned")
    except Exception as e:
        print(f"✗ OHLCV failed: {e}")

    print("\n[7] Getting open positions...")
    try:
        positions = mt5.positions_get()
        if positions:
            print(f"✓ {len(positions)} open positions:")
            for pos in positions:
                print(
                    f"  {pos.symbol} {'BUY' if pos.type == 0 else 'SELL'} {pos.volume} @ {pos.price_open}"
                )
        else:
            print("✓ No open positions")
    except Exception as e:
        print(f"✗ Positions failed: {e}")

    print("\n[8] Trying manual login...")
    try:
        # Try to login with the credentials
        login_result = mt5.login(
            login=5046812779, password="PiUk_5Ql", server="MetaQuotes-Demo"
        )
        print(f"  Login result: {login_result}")
        if login_result:
            account = mt5.account_info()
            print(f"  ✓ Logged in after manual login!")
            print(f"    Balance: ${account.balance}")
    except Exception as e:
        print(f"  ✗ Manual login failed: {e}")

    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

    # Cleanup
    try:
        mt5.shutdown()
        print("\nDisconnected cleanly")
    except:
        pass

    return True


if __name__ == "__main__":
    test_connection()
