#!/usr/bin/env python3
"""
MT5 LINUX - KONEKSI RPYC TEST
Test koneksi ke MT5 via RPYC server di server jarak jauh
"""

from mt5linux import MetaTrader5
import sys

# Server settings
MT5_HOST = "5.189.138.144"
MT5_PORT = 18812
TIMEOUT = 30000  # 30 detik

print("="*80)
print("MT5 LINUX - KONEKSI RPYC TEST")
print("="*80)
print()
print(f"Server: {MT5_HOST}:{MT5_PORT}")
print()

try:
    # Initialize MT5 connection
    print(f"Connecting to {MT5_HOST}:{MT5_PORT}...")
    mt5 = MetaTrader5(host=MT5_HOST, port=MT5_PORT, timeout=TIMEOUT)
    
    # Initialize connection
    print("Initializing MT5...")
    if mt5.initialize():
        print("✅ KONEKSI BERHASIL!")
        print()
        
        # Get account info
        acc = mt5.account_info()
        print("📊 ACCOUNT INFO:")
        print(f"   Account ID: {acc.id}")
        print(f"   Balance: ${acc.balance:.2f}")
        print(f"   Equity: ${acc.equity:.2f}")
        print(f"   Margin: ${acc.margin:.2f}")
        print()
        
        # Get terminal info
        ti = mt5.terminal_info()
        print("📊 TERMINAL INFO:")
        print(f"   Connected: {ti.connected}")
        print(f"   Server: {ti.server}")
        print(f"   Build: {ti.build}")
        print()
        
        # Get symbol info
        print("📊 SYMBOL INFO (XAUUSD):")
        symbol_info = mt5.symbol_info("XAUUSD")
        if symbol_info:
            print(f"   Name: {symbol_info.name}")
            print(f"   Path: {symbol_info.path}")
            print(f"   Trade allowed: {symbol_info.trade_allowed}")
            print(f"   Session volume: {symbol_info.session_volume}")
        print()
        
        mt5.shutdown()
        print("="*80)
        print("✅ TEST SELESAI - KONEKSI MT5 BERHASIL!")
        print("="*80)
        print()
        print("MT5 dapat diakses dari komputer lokal!")
        print("Siap untuk automated trading 24/7.")
        print()
        print("Untuk menjalankan bot:")
        print("  python3 xauusd_asia7c_bot.py")
        
    else:
        print(f"❌ GAGAL: {mt5.last_error()}")
        sys.exit(1)

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
