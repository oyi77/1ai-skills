"""
Quick test - just connection and account info
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brokers.ostium.connector import OstiumConnector
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv('/home/openclaw/.openclaw/workspace/skills/1ai-skills/trading/.env.ostium', override=True)

connector = OstiumConnector()

print("="*60)
print("QUICK TEST: Connection + Account Info")
print("="*60)

print("\nConnecting...")
if connector.connect(
    private_key=os.getenv('OSTIUM_PRIVATE_KEY'),
    rpc_url=os.getenv('OSTIUM_RPC_URL'),
    testnet=True
):
    print("✅ Connected")
else:
    print("❌ Connection failed")
    sys.exit(1)

print("\nGetting account info...")
account = connector.get_account_info()
if account:
    print(f"✅ Account Info:")
    print(f"   - Balance: {account.balance} USDC")
    print(f"   - Server: {account.server}")
    print(f"   - Login: {account.login}")
else:
    print("❌ Failed to get account info")
    sys.exit(1)

connector.disconnect()
print("\n✅ SUCCESS")
