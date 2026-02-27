#!/usr/bin/env python3
"""
Ostium Setup - Complete Automation Script

Runs all setup steps sequentially until 100% completion:
1. Check ETH balance
2. Request USDC from Ostium faucet (if ETH available)
3. Verify USDC balance
4. Report final status
"""

import os
import sys
import time
from dotenv import load_dotenv
from eth_account import Account

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brokers.ostium.connector import OstiumConnector
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def print_status(status, message):
    """Print formatted status."""
    icon = "✅" if status else "❌"
    print(f"{icon} {message}")

def main():
    """Run complete Ostium setup."""
    load_dotenv('.env.ostium', override=True)

    private_key = os.getenv('OSTIUM_PRIVATE_KEY')
    rpc_url = os.getenv('OSTIUM_RPC_URL')

    if not private_key:
        print_status(False, "OSTIUM_PRIVATE_KEY not found")
        return False

    # Get wallet address
    account = Account.from_key(private_key)
    wallet_address = account.address

    print_section("OSTIUM SETUP - COMPLETE AUTOMATION")
    print(f"Wallet: {wallet_address}")
    print(f"RPC URL: {rpc_url}")
    print()

    # Step 1: Initialize Ostium connector
    print_section("STEP 1: Connecting to Ostium")
    connector = OstiumConnector()

    if not connector.connect(private_key=private_key, rpc_url=rpc_url, testnet=True):
        print_status(False, "Failed to connect to Ostium")
        return False

    print_status(True, "Connected to Arbitrum Sepolia (testnet)")

    # Step 2: Check account info
    print_section("STEP 2: Checking Account Info")
    account_info = connector.get_account_info()

    if not account_info:
        print_status(False, "Failed to get account info")
        connector.disconnect()
        return False

    print(f"Balance: {account_info.balance} USDC")
    print(f"Native Balance: (checked later)")

    if account_info.balance > 0:
        print_status(True, "USDC already available! Skipping faucet.")
        connector.disconnect()
        print_section("✅ SETUP COMPLETE")
        print("You can start paper trading now!")
        return True

    # Step 3: Check ETH balance (need this for gas)
    print_section("STEP 3: Checking ETH Balance (for gas)")

    # Get native balance from account info
    # Note: AccountInfo doesn't track ETH separately, we need to check directly
    from ostium_python_sdk import OstiumSDK, NetworkConfig

    config = NetworkConfig.testnet()
    sdk = OstiumSDK(config, private_key, rpc_url)

    usdc_balance, native_balance = sdk.balance.get_balance(wallet_address)

    print(f"USDC Balance: {float(usdc_balance):.4f}")
    print(f"ETH Balance: {float(native_balance):.6f}")

    eth_balance = float(native_balance)

    if eth_balance < 0.001:  # Need at least 0.001 ETH for gas
        print_status(False, "Insufficient ETH for gas")
        print("\n" + "-" * 60)
        print("ACTION REQUIRED: Get Testnet ETH")
        print("-" * 60)
        print("\n1. Open: https://faucet.quicknode.com/arbitrum/sepolia")
        print("2. Connect your wallet (MetaMask)")
        print(f"3. Enter address: {wallet_address}")
        print("4. Claim ETH (wait 30-60 seconds)")
        print("\nAfter claiming ETH, run this script again.")
        print("-" * 60)

        connector.disconnect()
        return False

    print_status(True, f"ETH Balance: {eth_balance:.6f} (sufficient for gas)")

    # Step 4: Request USDC from Ostium faucet
    print_section("STEP 4: Requesting USDC from Ostium Faucet")

    # Check if eligible
    if not sdk.faucet.can_request_tokens(wallet_address):
        next_time = sdk.faucet.get_next_request_time(wallet_address)
        print_status(False, "Cannot request tokens yet")
        print(f"Next request available at: {next_time}")
        connector.disconnect()
        return False

    # Get faucet amount
    amount = sdk.faucet.get_token_amount()
    print(f"Available to request: {float(amount):.0f} USDC")

    try:
        print("Requesting USDC from faucet...")
        receipt = sdk.faucet.request_tokens()

        tx_hash = receipt['transactionHash'].hex()
        print_status(True, f"USDC request submitted")
        print(f"Transaction Hash: {tx_hash}")

        # Wait for transaction confirmation
        print("\nWaiting for transaction confirmation...")
        time.sleep(10)  # Wait 10 seconds for block confirmation

    except Exception as e:
        print_status(False, f"Failed to request USDC: {e}")
        connector.disconnect()
        return False

    # Step 5: Verify USDC balance
    print_section("STEP 5: Verifying USDC Balance")

    # Wait a bit more for indexer
    print("Waiting for balance update...")
    time.sleep(5)

    usdc_balance_new, native_balance_new = sdk.balance.get_balance(wallet_address)
    usdc_final = float(usdc_balance_new)

    print(f"USDC Balance (before): {account_info.balance:.4f}")
    print(f"USDC Balance (now): {usdc_final:.4f}")

    if usdc_final <= account_info.balance:
        print_status(False, "USDC balance not updated yet")
        print("\nTransaction might still be processing.")
        print("Wait 1-2 minutes and run this script again.")
        connector.disconnect()
        return False

    received = usdc_final - account_info.balance
    print_status(True, f"Received {received:.2f} USDC from faucet")

    # Step 6: Final status report
    print_section("✅ SETUP COMPLETE - 100% SUCCESS")

    print("\nWallet Configuration:")
    print(f"  - Address: {wallet_address}")
    print(f"  - USDC Balance: {usdc_final:.2f}")
    print(f"  - ETH Balance: {float(native_balance_new):.6f}")

    print("\nYou are now ready for:")
    print("  ✅ Paper Trading on Ostium Testnet")
    print("  ✅ Deploy Asia 7-Candle Strategy")
    print("  ✅ Test trades with real infrastructure")

    print("\nNext Steps:")
    print("  1. Run Asia 7-Candle backtest")
    print("  2. Deploy paper trading bot")
    print("  3. Monitor for 1-2 months")
    print("  4. If profitable → Move to mainnet")

    # Disconnect
    connector.disconnect()
    print_status(True, "Disconnected from Ostium")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
