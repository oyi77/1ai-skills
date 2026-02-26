"""
Test Ostium Connector

Test script to verify Ostium connector functionality.
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brokers.ostium.connector import OstiumConnector
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_ostium_connector():
    """Test Ostium connector basic functionality."""
    # Load .env.ostium with full path
    load_dotenv('/home/openclaw/.openclaw/workspace/skills/1ai-skills/trading/.env.ostium', override=True)

    # Get credentials from environment
    private_key = os.getenv("OSTIUM_PRIVATE_KEY")
    rpc_url = os.getenv("OSTIUM_RPC_URL")

    if not private_key:
        logger.error("OSTIUM_PRIVATE_KEY not found in environment")
        return False

    if not rpc_url:
        logger.error("OSTIUM_RPC_URL not found in environment")
        return False

    # Initialize connector
    connector = OstiumConnector()

    # Test connection
    logger.info("=" * 60)
    logger.info("TEST 1: Connecting to Ostium")
    logger.info("=" * 60)

    if not connector.connect(
        private_key=private_key,
        rpc_url=rpc_url,
        testnet=True  # Use testnet for paper trading
    ):
        logger.error("❌ Connection failed")
        return False

    logger.info("✅ Connection successful")

    # Test account info
    logger.info("\n" + "=" * 60)
    logger.info("TEST 2: Getting Account Info")
    logger.info("=" * 60)

    account_info = connector.get_account_info()
    if account_info:
        logger.info(f"✅ Account Info:")
        logger.info(f"   - Wallet: {connector._wallet_address}")
        logger.info(f"   - Balance: {account_info.balance} USDC")
        logger.info(f"   - Server: {account_info.server}")
    else:
        logger.error("❌ Failed to get account info")
        return False

    # Test available symbols
    logger.info("\n" + "=" * 60)
    logger.info("TEST 3: Getting Available Symbols")
    logger.info("=" * 60)

    symbols = connector.get_available_symbols()
    if symbols:
        logger.info(f"✅ Available symbols ({len(symbols)}):")
        for symbol in symbols[:10]:  # Show first 10
            logger.info(f"   - {symbol}")
    else:
        logger.error("❌ Failed to get symbols")
        return False

    # Test OHLCV data (XAU-USD)
    logger.info("\n" + "=" * 60)
    logger.info("TEST 4: Getting OHLCV Data (XAU-USD)")
    logger.info("=" * 60)

    ohlcv = connector.get_ohlcv(
        symbol="XAU-USD",
        timeframe="1h",
        count=10
    )
    if ohlcv:
        logger.info(f"✅ OHLCV Data ({len(ohlcv)} candles):")
        for candle in ohlcv[-3:]:  # Show last 3
            logger.info(f"   - {candle.timestamp} | O:{candle.open} H:{candle.high} L:{candle.low} C:{candle.close} V:{candle.volume}")
    else:
        logger.error("❌ Failed to get OHLCV data")
        return False

    # Test current price
    logger.info("\n" + "=" * 60)
    logger.info("TEST 5: Getting Current Price (XAU-USD)")
    logger.info("=" * 60)

    price = connector.get_current_price("XAU-USD")
    if price:
        logger.info(f"✅ Current XAU-USD Price: ${price:.2f}")
    else:
        logger.error("❌ Failed to get current price")
        return False

    # Test getting open positions
    logger.info("\n" + "=" * 60)
    logger.info("TEST 6: Getting Open Positions")
    logger.info("=" * 60)

    positions = connector.get_positions()
    if positions:
        logger.info(f"✅ Open Positions ({len(positions)}):")
        for pos in positions:
            logger.info(f"   - {pos.symbol} | {pos.order_type} | Vol: {pos.volume} | PnL: {pos.profit:.2f}")
    else:
        logger.info("✅ No open positions (as expected for test)")

    # Test placing a small order (TESTNET ONLY!)
    logger.info("\n" + "=" * 60)
    logger.info("TEST 7: Placing Test Order (TESTNET)")
    logger.info("=" * 60)
    logger.info("⚠️  Skipping order placement test to avoid unintended trades")
    logger.info("⚠️  To test order placement, uncomment the code below")

    # Uncomment to test order placement (TESTNET ONLY!)
    """
    order = connector.place_order(
        symbol="XAU-USD",
        order_type="BUY",
        volume=10.0,  # 10 USDC collateral
        leverage=10,
    )

    if order:
        logger.info(f"✅ Order placed:")
        logger.info(f"   - Ticket: {order.ticket}")
        logger.info(f"   - Symbol: {order.symbol}")
        logger.info(f"   - Type: {order.order_type}")
        logger.info(f"   - Volume: {order.volume}")
        logger.info(f"   - Price: {order.price}")

        # Sleep for a few seconds, then close the position
        import time
        time.sleep(5)

        logger.info(f"\nClosing test order...")
        if connector.close_position(order.ticket):
            logger.info(f"✅ Position closed successfully")
    else:
        logger.error("❌ Failed to place order")
    """

    # Disconnect
    logger.info("\n" + "=" * 60)
    logger.info("TEST 8: Disconnecting")
    logger.info("=" * 60)

    if connector.disconnect():
        logger.info("✅ Disconnected successfully")
    else:
        logger.error("❌ Failed to disconnect")
        return False

    logger.info("\n" + "=" * 60)
    logger.info("✅ ALL TESTS PASSED")
    logger.info("=" * 60)

    return True


if __name__ == "__main__":
    try:
        success = test_ostium_connector()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
