#!/usr/bin/env python3
"""
MT5 Connection Test with Explicit Login
"""

import sys
import os

# Add trading to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trading.brokers.mt5.connector import MT5Connector


def test_with_login():
    print("=" * 60)
    print("MT5 Connection Test with Explicit Login")
    print("=" * 60)

    # Create connector
    connector = MT5Connector(host="5.189.138.144", port=18812)

    # Test with explicit login credentials
    login = 5046812779
    password = "PiUk_5Ql"
    server = "MetaQuotes-Demo"

    print(f"\n[1] Connecting to {server} with login {login}...")

    try:
        connected = connector.connect(login=login, password=password, server=server)

        if connected:
            print("✓ Connected successfully!")
        else:
            print("✗ Connection failed")
            return

    except Exception as e:
        print(f"✗ Connection error: {e}")
        return

    # Get account info
    print("\n[2] Getting account info...")
    account = connector.get_account_info()
    if account:
        print(f"✓ Account info:")
        print(f"  Login: {account.login}")
        print(f"  Server: {account.server}")
        print(f"  Balance: ${account.balance}")
        print(f"  Equity: ${account.equity}")
        print(f"  Currency: {account.currency}")
    else:
        print("✗ No account info")

    # Get symbol info
    print("\n[3] Getting symbol info for XAUUSD...")
    symbol_info = connector.get_symbol_info("XAUUSD")
    if symbol_info:
        print(f"✓ XAUUSD available")
    else:
        print("✗ XAUUSD not available")

    # Get OHLCV
    print("\n[4] Getting OHLCV data for XAUUSD H1...")
    from datetime import datetime, timedelta

    ohlcv = connector.get_ohlcv("XAUUSD", "H1", count=5)
    if ohlcv:
        print(f"✓ Got {len(ohlcv)} candles:")
        for candle in ohlcv:
            print(
                f"  {candle.timestamp} O:{candle.open} H:{candle.high} L:{candle.low} C:{candle.close}"
            )
    else:
        print("✗ No data")

    # Get positions
    print("\n[5] Getting open positions...")
    positions = connector.get_positions()
    print(f"✓ {len(positions)} open positions")

    # Disconnect
    connector.disconnect()
    print("\n✓ Test complete!")


if __name__ == "__main__":
    test_with_login()
