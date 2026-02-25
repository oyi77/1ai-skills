#!/usr/bin/env python3
"""
MT5 RPYC - SLOW START WORKAROUND
Workaround untuk MT5 initialize timeout
"""

import rpyc
import time

print("Connecting to MT5 RPYC server...")
conn = rpyc.classic.connect('5.189.138.144', 18812)
print("✅ Connected to RPYC!")

# Get modules
mt5_mod = conn.modules.mt5linux
print("✅ MT5 module loaded")

# Create instance
instance = mt5_mod.MetaTrader5()
print("✅ MT5 instance created")

# Small delay before initialize
print("Waiting 5 seconds for MT5 to initialize...")
time.sleep(5)

# Try initialize
print("Calling initialize...")
result = instance.initialize()
print(f"✅ Initialize result: {result}")

# Get account
print("Getting account info...")
acc = instance.account_info()
print(f"Account ID: {acc.id}")
print(f"Balance: ${acc.balance:.2f}")

conn.close()
print("✅ MT5 CONTROLLABLE!")
