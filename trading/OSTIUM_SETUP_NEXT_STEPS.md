# 🚀 Ostium Setup - Next Steps

## Status
✅ Wallet generated: `0x6bC9d7Da87a72B524de4a1900663B3b220223119`
✅ Ostium connector: FULLY WORKING
✅ Connection test: SUCCESS
✅ .env.ostium: Configured
❌ Balance: 0.0 USDC (butuh top up)

## Next Steps (Quick Guide)

### Step 1: Get Testnet ETH for Gas
**Pilih salah satu:**

**Option A: QuickNode Faucet (Web - Paling Gampang)**
1. Buka browser: https://faucet.quicknode.com/arbitrum/sepolia
2. Klik "Connect Wallet" (MetaMask/other wallet)
3. Paste address: `0x6bC9d7Da87a72B524de4a1900663B3b220223119`
4. Select "Arbitrum" → "Sepolia"
5. Pilih token: ETH
6. Claim faucet (1 drip per 12 hours)

**Option B: Alchemy Faucet (CURL)**
```bash
curl -X POST https://sepolia-faucet.polygon.technology/api/v1/faucet \
  -H "Content-Type: application/json" \
  -d '{"address":"0x6bC9d7Da87a72B524de4a1900663B3b220223119","token":"ETH"}'
```

### Step 2: Get Testnet USDC (via Ostium SDK)
Setelah dapat ETH, jalankan:
```bash
cd /home/openclaw/.openclaw/workspace/skills/1ai-skills/trading
~/.trading-venv/bin/python << 'EOF'
from ostium_python_sdk import OstiumSDK, NetworkConfig
from dotenv import load_dotenv
import os

load_dotenv('.env.ostium')

config = NetworkConfig.testnet()
sdk = OstiumSDK(config, os.getenv('OSTIUM_PRIVATE_KEY'), os.getenv('OSTIUM_RPC_URL'))

from eth_account import Account
acct = Account.from_key(os.getenv('OSTIUM_PRIVATE_KEY'))

print(f"Wallet: {acct.address}")

if sdk.faucet.can_request_tokens(acct.address):
    amount = sdk.faucet.get_token_amount()
    print(f"Requesting {amount} USDC...")
    try:
        receipt = sdk.faucet.request_tokens()
        print(f"✅ SUCCESS!")
        print(f"TX: {receipt['transactionHash'].hex()}")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("❌ Cannot request yet")
EOF
```

### Step 3: Verify Balance
```bash
~/.trading-venv/bin/python test_quick.py
```

Akan menunjukkan balance USDC setelah faucet.

### Step 4: Start Paper Trading
Deploy Asia 7-Candle strategy ke Ostium testnet:
```bash
# (akan dibuat setelah USDC didapat)
```

## Files Reference
- `.env.ostium` - Credential config
- `test_quick.py` - Connection + balance test
- `test_ostium_connector.py` - Full connector test
- `OSTIUM_README.md` - Complete documentation

## Quick Commands
```bash
# Test connection
~/.trading-venv/bin/python test_quick.py

# Get USDC (setelah ada ETH)
~/.trading-venv/bin/python get_usdc.py

# Backtest Asia 7-Candle
~/.trading-venv/bin/python framework_runner.py backtest --strategy asia-7c --symbol GC=F --start-date 2025-01-01 --end-date 2025-12-31
```

---

**Mau saya otomatisasi Step 1 (QuickNode faucet) dengan browser automation?**

Perlu:
1. Klik extension OpenClaw di Chrome tab
2. Buka https://faucet.quicknode.com/arbitrum/sepolia

Atau kamu mau manual via browser sendiri?
