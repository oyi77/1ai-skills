"""
Tests for CCXT broker connector with retry behavior.
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestCCXTConnectorRetry(unittest.TestCase):
    """Test cases for CCXT connector retry behavior."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock the ccxt module before importing connector
        self.mock_ccxt = MagicMock()
        self.mock_exchange = MagicMock()
        self.mock_ccxt.binance.return_value = self.mock_exchange
        
        # Patch the import of ccxt
        self.ccxt_patcher = patch.dict('sys.modules', {'ccxt': self.mock_ccxt})
        self.ccxt_patcher.start()
        
        # Need to reload the module to get fresh import
        if 'trading.brokers.ccxt.connector' in sys.modules:
            del sys.modules['trading.brokers.ccxt.connector']
        
        from trading.brokers.ccxt.connector import CCXTConnector
        
        # Create a subclass that implements abstract methods
        class TestableConnector(CCXTConnector):
            def connect(self, **kwargs):
                return True
            def disconnect(self):
                return True
        
        self.connector = TestableConnector(exchange_id="binance")
        self.connector._exchange = self.mock_exchange
        self.connector.connected = True

    def tearDown(self):
        """Clean up after tests."""
        self.ccxt_patcher.stop()

    def test_get_ohlcv_retry_on_failure(self):
        """Test that get_ohlcv retries on failure."""
        # Mock exchange to fail twice then succeed
        self.mock_exchange.fetch_ohlcv.side_effect = [
            Exception("Network error"),
            Exception("Network error"),
            [(1700000000000, 100.0, 105.0, 99.0, 102.0, 1000.0)]
        ]
        
        # Should succeed after retries
        result = self.connector.get_ohlcv("BTC/USDT", "1h", count=10)
        
        # Should have called fetch_ohlcv 3 times (2 failures + 1 success)
        self.assertEqual(self.mock_exchange.fetch_ohlcv.call_count, 3)
        self.assertEqual(len(result), 1)

    def test_get_ohlcv_max_retries_exceeded(self):
        """Test that get_ohlcv raises exception after max retries."""
        # Mock exchange to always fail
        self.mock_exchange.fetch_ohlcv.side_effect = Exception("Permanent error")
        
        # Should raise exception after max attempts (retry re-raises)
        with self.assertRaises(Exception) as context:
            self.connector.get_ohlcv("BTC/USDT", "1h", count=10)
        
        self.assertEqual(str(context.exception), "Permanent error")
        # Should have called fetch_ohlcv 3 times (max_attempts)
        self.assertEqual(self.mock_exchange.fetch_ohlcv.call_count, 3)

    def test_place_order_retry_on_failure(self):
        """Test that place_order retries on failure."""
        # Mock exchange to fail once then succeed
        self.mock_exchange.create_order.side_effect = [
            Exception("Connection error"),
            {"id": "order123", "price": 100.0}
        ]
        
        result = self.connector.place_order("BTC/USDT", "BUY", 0.01, price=100.0)
        
        # Should have called create_order 2 times
        self.assertEqual(self.mock_exchange.create_order.call_count, 2)
        self.assertIsNotNone(result)

    def test_get_positions_retry_on_failure(self):
        """Test that get_positions retries on failure."""
        # Mock exchange to fail twice then succeed
        self.mock_exchange.fetch_positions.side_effect = [
            Exception("API error"),
            Exception("API error"),
            [{"id": "1", "symbol": "BTC/USDT", "contracts": 1.0, "side": "long",
              "entryPrice": 100.0, "markPrice": 105.0, "unrealizedPnl": 5.0}]
        ]
        
        result = self.connector.get_positions()
        
        # Should have called fetch_positions 3 times
        self.assertEqual(self.mock_exchange.fetch_positions.call_count, 3)
        self.assertEqual(len(result), 1)

    def test_get_account_info_retry_on_failure(self):
        """Test that get_account_info retries on failure."""
        # Mock exchange to fail once then succeed
        self.mock_exchange.fetch_balance.side_effect = [
            Exception("Auth error"),
            {"total": {"USDT": 1000.0}, "free": {"USDT": 800.0}}
        ]
        
        result = self.connector.get_account_info()
        
        # Should have called fetch_balance 2 times
        self.assertEqual(self.mock_exchange.fetch_balance.call_count, 2)
        self.assertIsNotNone(result)
        self.assertEqual(result.balance, 1000.0)

    def test_health_check_success(self):
        """Test health_check returns True on success."""
        self.mock_exchange.fetch_time.return_value = 1700000000000
        
        result = self.connector.health_check()
        
        self.assertTrue(result)
        self.assertTrue(self.connector.is_healthy)
        self.mock_exchange.fetch_time.assert_called_once()

    def test_health_check_failure(self):
        """Test health_check returns False on failure."""
        self.mock_exchange.fetch_time.side_effect = Exception("Connection failed")
        
        result = self.connector.health_check()
        
        self.assertFalse(result)
        self.assertFalse(self.connector.is_healthy)

    def test_is_healthy_property(self):
        """Test is_healthy property returns correct status."""
        # Initially should be False
        self.assertFalse(self.connector.is_healthy)
        
        # After successful health check should be True
        self.mock_exchange.fetch_time.return_value = 1700000000000
        self.connector.health_check()
        self.assertTrue(self.connector.is_healthy)

    def test_retry_config_attached(self):
        """Test that retry config is attached to decorated methods."""
        from trading.brokers.ccxt.connector import CCXTConnector
        
        # Check get_ohlcv has retry config
        self.assertTrue(hasattr(self.connector.get_ohlcv, '_retry_config'))
        config = self.connector.get_ohlcv._retry_config
        self.assertEqual(config['max_attempts'], 3)
        self.assertEqual(config['backoff'], 1.0)


class TestCCXTConnectorRetryWithCustomParams(unittest.TestCase):
    """Test retry with custom parameters."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_ccxt = MagicMock()
        self.mock_exchange = MagicMock()
        self.mock_ccxt.binance.return_value = self.mock_exchange
        
        self.ccxt_patcher = patch.dict('sys.modules', {'ccxt': self.mock_ccxt})
        self.ccxt_patcher.start()
        
        # Need to reload the module to get fresh import
        if 'trading.brokers.ccxt.connector' in sys.modules:
            del sys.modules['trading.brokers.ccxt.connector']
        
        from trading.brokers.ccxt.connector import CCXTConnector
        
        # Create a subclass that implements abstract methods
        class TestableConnector(CCXTConnector):
            def connect(self, **kwargs):
                return True
            def disconnect(self):
                return True
        
        self.connector = TestableConnector(exchange_id="binance")
        self.connector._exchange = self.mock_exchange
        self.connector.connected = True

    def tearDown(self):
        """Clean up after tests."""
        self.ccxt_patcher.stop()

    def test_retry_respects_max_attempts(self):
        """Test that retry respects max_attempts parameter."""
        call_count = 0
        
        def always_fail(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise Exception("Test error")
        
        # Mock to call a function that always fails
        self.mock_exchange.fetch_ohlcv.side_effect = always_fail
        
        # Should raise exception after max attempts
        with self.assertRaises(Exception):
            self.connector.get_ohlcv("BTC/USDT", "1h")
        
        # Should attempt exactly max_attempts (3) times
        self.assertEqual(call_count, 3)


if __name__ == '__main__':
    unittest.main()
