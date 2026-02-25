#!/usr/bin/env python3
"""
FUSION MARKETS CTRADER API - FULL CONNECTION
Using direct WebSocket connections
"""

import asyncio
import json
from datetime import datetime

# Try to import cTrader API
try:
    import ctrader_openapi as ctrader
    CTRADER_AVAILABLE = True
except ImportError:
    CTRADER_AVAILABLE = False

    # Try alternative imports
    try:
        import cTrader
        CTRADER_AVAILABLE = True
    except ImportError:
        CTRADER_AVAILABLE = False

class FusionMarketsAPI:
    """Full cTrader API connection to Fusion Markets"""

    def __init__(self):
        self.credentials = {
            'username': 'Openclaw@12',
            'password': '10100262',
            'server': 'FusionMarkets-Demo'
        }
        self.client_id = None
        self.access_token = None
        self.account_id = None

    async def connect(self):
        """Connect ke Fusion Markets via cTrader OpenAPI"""
        if not CTRADER_AVAILABLE:
            print("❌ cTrader OpenAPI not available")
            return False

        print("🔗 Connecting to Fusion Markets cTrader OpenAPI...")

        try:
            # Create OpenAPI client
            config = ctrader.OpenApiConfig(
                client_id="OpenclawBot",
                client_secret="OpenclawBotSecret",
                access_token=None,
                token_type="Public"
            )

            self.client_id = config.client_id
            self.access_token = config.access_token

            # Connect to server
            socket_client = ctrader.OpenApiClient(
                host="demo.ctrader.com",
                token=config.access_token
            )

            # Get accounts
            accounts = await socket_client.get_accounts_async()
            self.account_id = accounts[0]["id"]
            print(f"✅ Connected! Account ID: {self.account_id}")
            print(f"   Broker: Fusion Markets Demo")
            print(f"   Account Type: Demo")
            print(f"   Balance: {accounts[0]['balance']}")

            return True

        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print(f"   This is expected - cTrader API may need special credentials")
            return False

    async def subscribe_symbols(self, symbols=["XAUUSD"]):
        """Subscribe to XAUUSD quotes"""
        if not self.client:
            print("❌ Not connected")
            return

        print(f"📊 Subscribing to symbols: {symbols}")

        try:
            # Get symbol information
            symbol_info = await self.client.get_symbol_async(symbol=symbols[0])
            print(f"✅ Symbol info: {symbol_info}")
            print(f"   Ask: {symbol_info['Ask']}")
            print(f"   Bid: {symbol_info['Bid']}")
            print(f"   Spread: {symbol_info['Spread']}")

            return True

        except Exception as e:
            print(f"❌ Subscription failed: {e}")
            return False

    async def place_order(self, symbol="XAUUSD", trade_type="Buy", volume=0.01, price=None,
                     stop_loss=None, take_profit=None):
        """Place order via API"""
        if not self.client:
            print("❌ Not connected")
            return False

        print(f"📝 Placing order: {trade_type} {symbol} @ {volume} lots")

        try:
            # Create order request
            order = ctrader.OrderRequest(
                symbol_id=symbol,
                order_type=trade_type,  # Buy or Sell
                volume=volume,
                price=price,
                stop_loss=stop_loss,
                take_profit=take_profit
                label="XAUUSD Asia 7-Candle"
            )

            # Place order
            result = await self.client.place_order_async(order)
            print(f"✅ Order placed: {result['order_id']}")
            print(f"   Status: {result['status']}")

            return True

        except Exception as e:
            print(f"❌ Order failed: {e}")
            return False

    def get_account_info(self):
        """Get account information"""
        if self.client:
            print(f"\n💰 Account Info:")
            print(f"   Account ID: {self.account_id}")
            print(f"   Balance: Available")
            return True
        return False

async def main():
    api = FusionMarketsAPI()

    # Try to connect
    await api.connect()

    # If connected, get symbol info
    if api.client:
        await api.subscribe_symbols(["XAUUSD"])
        api.get_account_info()

if __name__ == "__main__":
    asyncio.run(main())
