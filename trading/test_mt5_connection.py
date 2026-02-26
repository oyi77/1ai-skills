#!/usr/bin/env python3
"""
MT5 Connection Test Script
Tests connection to mt5linux server
"""

import sys
import os

# Add trading to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the connector
from trading.brokers.mt5.connector import MT5Connector


def test_connection():
    print("=" * 60)
    print("MT5 Connection Test")
    print("=" * 60)

    # Create connector
    connector = MT5Connector(host="5.189.138.144", port=18812)

    # Test 1: Check if server is reachable
    print("\n[1] Testing server reachability...")
    if connector._check_server(timeout=10):
        print("✓ Server is reachable at 5.189.138.144:18812")
    else:
        print("✗ Server is NOT reachable")
        print("  Possible causes:")
        print("  - MT5 Docker container not running on server")
        print("  - Firewall blocking the port")
        print("  - Wrong IP/Port")
        return False

    # Test 2: Initialize MT5
    print("\n[2] Initializing MT5 connection...")
    try:
        mt5 = connector._import_mt5(timeout=30)
        print(f"✓ MT5 initialized: {mt5}")
    except Exception as e:
        print(f"✗ MT5 initialization failed: {e}")
        return False

    # Test 3: Get account info (no login required for demo account)
    print("\n[3] Getting account info...")
    try:
        account = mt5.account_info()
        if account:
            print(f"✓ Connected to account:")
            print(f"  Login: {account.login}")
            print(f"  Server: {account.server}")
            print(f"  Balance: ${account.balance}")
            print(f"  Equity: ${account.equity}")
            print(f"  Margin: ${account.margin}")
            print(f"  Free Margin: ${account.margin_free}")
            print(f"  Currency: {account.currency}")
        else:
            print("✗ No account info (need login credentials)")
    except Exception as e:
        print(f"✗ Failed to get account info: {e}")

    # Test 4: Get symbol info
    print("\n[4] Getting symbol info for XAUUSD...")
    try:
        symbol_info = mt5.symbol_info("XAUUSD")
        if symbol_info:
            print(f"✓ XAUUSD info:")
            print(f"  Name: {symbol_info.name}")
            print(f"  Digits: {symbol_info.digits}")
            print(f"  Point: {symbol_info.point}")
            print(f"  Volume Min: {symbol_info.volume_min}")
            print(f"  Volume Max: {symbol_info.volume_max}")
        else:
            print("✗ XAUUSD not available")
    except Exception as e:
        print(f"✗ Failed to get symbol info: {e}")

    # Test 5: Get OHLCV data
    print("\n[5] Getting OHLCV data for XAUUSD H1...")
    try:
        rates = mt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_H1, 0, 10)
        if rates is not None and len(rates) > 0:
            print(f"✓ Got {len(rates)} candles:")
            for rate in rates[-5:]:
                from datetime import datetime

                dt = datetime.fromtimestamp(rate[0])
                print(
                    f"  {dt} O:{rate[1]:.2} H:{rate[2]:.2} L:{rate[3]:.2} C:{rate[4]:.2} V:{rate[5]}"
                )
        else:
            print("✗ No data returned")
    except Exception as e:
        print(f"✗ Failed to get OHLCV: {e}")

    # Test 6: Get open positions
    print("\n[6] Getting open positions...")
    try:
        positions = mt5.positions_get()
        if positions:
            print(f"✓ {len(positions)} open positions:")
            for pos in positions:
                print(
                    f"  {pos.symbol} {'BUY' if pos.type == 0 else 'SELL'} {pos.volume} @ {pos.price_open} (profit: ${pos.profit})"
                )
        else:
            print("✓ No open positions")
    except Exception as e:
        print(f"✗ Failed to get positions: {e}")

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
