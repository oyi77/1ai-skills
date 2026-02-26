# Ostium Integration Guide

Complete guide for using Ostium (Decentralized Perpetual Exchange) with the trading framework.

## What is Ostium?

Ostium is a decentralized perpetuals exchange on Arbitrum that allows you to trade:
- **Commodities:** Gold (XAU-USD), Silver, Oil, Copper
- **FX:** EUR-USD, GBP-USD, USD-JPY, etc.
- **Indices:** S&P 500, NASDAQ, Dow Jones, Nikkei 225, FTSE, DAX
- **Stocks:** NVIDIA, Google, Amazon, Tesla, Apple, Microsoft
- **Crypto:** Bitcoin, Ethereum, Solana

**Key Advantages:**
- Self-custody (you control your funds)
- Transparent on-chain (all transactions visible)
- No account restrictions (cannot freeze funds)
- Up to 200x leverage
- Fast deposits/withdrawals in USDC

## Installation

### 1. Install Dependencies

```bash
cd /home/openclaw/.openclaw/workspace/skills/1ai-skills/trading
~/.trading-venv/bin/pip install ostium-python-sdk eth-account yfinance
```

### 2. Get Alchemy RPC URL

1. Go to https://www.alchemy.com/
2. Sign up for free account
3. Create a new app:
   - **For Testnet:** Choose "Arbitrum Sepolia"
   - **For Mainnet:** Choose "Arbitrum One"
4. Copy the RPC URL (looks like: `https://arb-sepolia.g.alchemy.com/v2/xxx`)

### 3. Get EVM Wallet Private Key

1. Open MetaMask (or your Ethereum wallet)
2. Go to Account Details → Export Private Key
3. **⚠️ WARNING:** Never share or commit this key!
4. Copy the private key (starts with `0x` or just hex)

### 4. Configure Environment

```bash
# Copy example config
cp .env.ostium.example .env.ostium

# Edit with your credentials
nano .env.ostium
```

Fill in:
```
OSTIUM_PRIVATE_KEY=0x_your_private_key_here
OSTIUM_RPC_URL=https://arb-sepolia.g.alchemy.com/v2/your_api_key
OSTIUM_TESTNET=true
```

## Testing

### Basic Connection Test

```bash
cd /home/openclaw/.openclaw/workspace/skills/1ai-skills/trading
~/.trading-venv/bin/python test_ostium_connector.py
```

This will test:
1. ✅ Connection to Ostium
2. ✅ Account info retrieval
3. ✅ Available symbols
4. ✅ OHLCV data fetching
5. ✅ Current price
6. ✅ Open positions
7. ✅ Disconnect

### Get Testnet USDC (Paper Trading)

If using testnet, get free USDC:

```python
from ostium_python_sdk import OstiumSDK, NetworkConfig
import os
from dotenv import load_dotenv

load_dotenv(".env.ostium")

config = NetworkConfig.testnet()
sdk = OstiumSDK(config, os.getenv("OSTIUM_PRIVATE_KEY"), os.getenv("OSTIUM_RPC_URL"))

# Get your address
from eth_account import Account
account = Account.from_key(os.getenv("OSTIUM_PRIVATE_KEY"))

# Request testnet USDC
if sdk.faucet.can_request_tokens(account.address):
    amount = sdk.faucet.get_token_amount()
    receipt = sdk.faucet.request_tokens()
    print(f"Got {amount} testnet USDC")
```

## Usage

### Python API

```python
from brokers.ostium.connector import OstiumConnector
import os
from dotenv import load_dotenv

load_dotenv(".env.ostium")

# Initialize connector
connector = OstiumConnector()

# Connect to testnet
connector.connect(
    private_key=os.getenv("OSTIUM_PRIVATE_KEY"),
    rpc_url=os.getenv("OSTIUM_RPC_URL"),
    testnet=True
)

# Get account info
account = connector.get_account_info()
print(f"Balance: {account.balance} USDC")

# Get XAU-USD price
price = connector.get_current_price("XAU-USD")
print(f"Gold Price: ${price}")

# Place BUY order (Long)
order = connector.place_order(
    symbol="XAU-USD",
    order_type="BUY",
    volume=100.0,  # 100 USDC collateral
    leverage=10,
    sl=price * 0.99,  # 1% SL
    tp=price * 1.02   # 2% TP
)

# Get open positions
positions = connector.get_positions()
for pos in positions:
    print(f"{pos.symbol} | {pos.order_type} | PnL: {pos.profit:.2f}")

# Close position
connector.close_position(order.ticket)

# Disconnect
connector.disconnect()
```

## Available Symbols

| Symbol   | Description           | Pair ID |
|----------|-----------------------|----------|
| XAU-USD  | Gold                  | 5        |
| BTC-USD  | Bitcoin               | 0        |
| ETH-USD  | Ethereum              | 1        |
| EUR-USD  | Euro/USD              | 2        |
| GBP-USD  | British Pound/USD       | 3        |
| USD-JPY  | USD/Japanese Yen      | 4        |
| XAG-USD  | Silver                | 8        |
| SPX-USD  | S&P 500 Index         | 10       |
| NDX-USD  | NASDAQ-100 Index      | 12       |
| NVDA-USD | NVIDIA Stock          | 18       |
| AAPL-USD | Apple Stock           | 23       |

## Using with Asia 7-Candle Strategy

The Ostium connector is now integrated into the trading framework. You can use it for paper trading:

```python
from framework_runner import run_backtest
from brokers.ostium.connector import OstiumConnector

# Initialize Ostium connector
connector = OstiumConnector()
connector.connect(
    private_key=os.getenv("OSTIUM_PRIVATE_KEY"),
    rpc_url=os.getenv("OSTIUM_RPC_URL"),
    testnet=True
)

# Run Asia 7-Candle strategy with Ostium
results = run_backtest(
    strategy="asia-7c",
    broker=connector,
    symbol="XAU-USD",
    start_date="2025-01-01",
    end_date="2025-12-31",
    initial_balance=100
)
```

## Important Notes

### ⚠️ Paper Trading First

Always start with **TESTNET** before going to mainnet:
- Testnet USDC is free (via faucet)
- All functionality is identical to mainnet
- No real money at risk

### ⚠️ Leverage

Ostium supports up to 200x leverage, but:
- **High leverage = High risk**
- Start with 10-20x maximum
- Asia 7-Candle strategy uses 10x

### ⚠️ Fees

- **Opening fee:** 2-10 bps (0.02% - 0.10%) when opening position
- **Rollover fee:** Charged for holding positions overnight
- **No closing fee:** Manual closes are free

### ⚠️ Gas Fees

- On Arbitrum, gas fees are very low (~$0.01 per transaction)
- You need ETH (or Arbitrum ETH) in your wallet for gas
- Get testnet ETH: https://www.alchemy.com/faucets/arbitrum-sepolia

## Troubleshooting

### "Ostium SDK not installed"

```bash
~/.trading-venv/bin/pip install ostium-python-sdk
```

### "Failed to connect"

Check:
1. RPC URL is correct
2. Private key is valid (starts with `0x` if provided with prefix)
3. Network matches (testnet vs mainnet)

### "No USDC in wallet"

For testnet:
- Use the faucet to get free USDC
- See "Get Testnet USDC" section above

For mainnet:
- Deposit USDC to your wallet address
- Bridge from another chain if needed

### "Out of gas"

Get testnet ETH: https://www.alchemy.com/faucets/arbitrum-sepolia

## Next Steps

1. ✅ Test connection with `test_ostium_connector.py`
2. ✅ Get testnet USDC from faucet
3. ✅ Run Asia 7-Candle backtest
4. ✅ Deploy paper trading on Ostium testnet
5. ✅ Monitor for 1-2 months
6. ✅ If profitable → migrate to Ostium mainnet

## Resources

- **Ostium Docs:** https://ostium-labs.gitbook.io/ostium-docs
- **Ostium App:** https://ostium.app
- **GitHub SDK:** https://github.com/0xOstium/ostium-python-sdk
- **Alchemy:** https://www.alchemy.com/ (for RPC URLs)

---

*Updated: 2026-02-27*
*Author: Vilona*
