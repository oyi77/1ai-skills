#!/usr/bin/env python3
"""
MT5 RPYC TEST - PROGRAMMATIC CONTROL
Test koneksi MT5 via RPYC server
"""

import rpyc

# Server settings
MT5_HOST = "5.189.138.144"
MT5_PORT = 18812

print("="*80)
print("MT5 PROGRAMMATIC CONTROL TEST")
print("="*80)
print(f"Server: {MT5_HOST}:{MT5_PORT}")
print()

try:
    # Connect via RPYC
    print("Connecting to MT5...")
    conn = rpyc.classic.connect(MT5_HOST, MT5_PORT)
    print("✅ Connected!")
    print()
    
    # List available modules
    print("Available modules:")
    for mod in dir(conn.modules):
        print(f"  - {mod}")
    print()
    
    # Try to import mt5linux
    print("Trying mt5linux...")
    mt5 = conn.modules.mt5linux
    print(f"mt5linux module: {mt5}")
    print()
    
    # List mt5linux attributes
    print("mt5linux attributes:")
    for attr in dir(mt5):
        if not attr.startswith('__'):
            print(f"  - {attr}")
    print()
    
    # Try to use MetaTrader5
    print("Trying MetaTrader5...")
    mt5_class = mt5.MetaTrader5
    print("MetaTrader5 class obtained")
    
    # Create instance
    print("Creating MT5 instance...")
    instance = mt5_class()
    print("Instance created")
    
    # Try initialize
    print("Calling initialize...")
    result = instance.initialize()
    print(f"Initialize result: {result}")
    
    # Get account info
    print("Getting account info...")
    acc = instance.account_info()
    print(f"Account ID: {acc.id}")
    print(f"Balance: ${acc.balance:.2f}")
    
    conn.close()
    print()
    print("="*80)
    print("✅ MT5 BISA DIKONTROL SECARA PROGRAMMATIC!")
    print("="*80)
    print()
    print("Koneksi successfully established!")
    print("Anda bisa sekarang control MT5 dari Python!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
