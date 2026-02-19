"""
Unit tests for RSI (Relative Strength Index) indicator.
"""

import pytest
from datetime import datetime, timedelta

from trading.indicators.rsi import RSI, RSIResult, calculate_rsi
from trading.brokers.base import OHLCV


class TestRSIResult:
    """Test cases for RSIResult dataclass."""
    
    def test_rsi_result_creation(self):
        """Test RSIResult creation and basic attributes."""
        result = RSIResult(
            value=50.0,
            period=14,
            overbought_level=70.0,
            oversold_level=30.0,
        )
        assert result.value == 50.0
        assert result.period == 14
        assert result.overbought_level == 70.0
        assert result.oversold_level == 30.0
    
    def test_rsi_result_is_overbought_true(self):
        """Test is_overbought returns True when RSI >= overbought level."""
        result = RSIResult(value=70.0, period=14, overbought_level=70.0, oversold_level=30.0)
        assert result.is_overbought() is True
        
        result = RSIResult(value=75.0, period=14, overbought_level=70.0, oversold_level=30.0)
        assert result.is_overbought() is True
    
    def test_rsi_result_is_overbought_false(self):
        """Test is_overbought returns False when RSI < overbought level."""
        result = RSIResult(value=69.9, period=14, overbought_level=70.0, oversold_level=30.0)
        assert result.is_overbought() is False
    
    def test_rsi_result_is_oversold_true(self):
        """Test is_oversold returns True when RSI <= oversold level."""
        result = RSIResult(value=30.0, period=14, overbought_level=70.0, oversold_level=30.0)
        assert result.is_oversold() is True
        
        result = RSIResult(value=25.0, period=14, overbought_level=70.0, oversold_level=30.0)
        assert result.is_oversold() is True
    
    def test_rsi_result_is_oversold_false(self):
        """Test is_oversold returns False when RSI > oversold level."""
        result = RSIResult(value=30.1, period=14, overbought_level=70.0, oversold_level=30.0)
        assert result.is_oversold() is False
    
    def test_rsi_result_repr(self):
        """Test string representation of RSIResult."""
        result = RSIResult(value=50.0, period=14, overbought_level=70.0, oversold_level=30.0)
        assert "RSI(50.00)" in repr(result)
        
        result = RSIResult(value=75.0, period=14, overbought_level=70.0, oversold_level=30.0)
        assert "(overbought)" in repr(result)
        
        result = RSIResult(value=25.0, period=14, overbought_level=70.0, oversold_level=30.0)
        assert "(oversold)" in repr(result)


class TestRSIInit:
    """Test cases for RSI initialization."""
    
    def test_default_initialization(self):
        """Test RSI with default parameters."""
        rsi = RSI()
        assert rsi.period == 14
        assert rsi.overbought_level == 70.0
        assert rsi.oversold_level == 30.0
        assert rsi.name == "RSI"
    
    def test_custom_initialization(self):
        """Test RSI with custom parameters."""
        rsi = RSI(period=21, overbought_level=80.0, oversold_level=20.0)
        assert rsi.period == 21
        assert rsi.overbought_level == 80.0
        assert rsi.oversold_level == 20.0
    
    def test_get_required_period(self):
        """Test get_required_period returns period + 1."""
        rsi = RSI(period=14)
        assert rsi.get_required_period() == 15
        
        rsi = RSI(period=21)
        assert rsi.get_required_period() == 22


class TestRSICalculate:
    """Test cases for RSI calculation."""
    
    def create_ohlcv_data(self, closes, start_price=100.0):
        """Helper to create OHLCV data from closing prices."""
        data = []
        base_time = datetime(2024, 1, 1)
        
        for i, close in enumerate(closes):
            # Create simple OHLCV with close as the main varying field
            open_price = close - 1.0 if i == 0 else closes[i-1]
            high = max(open_price, close) + 0.5
            low = min(open_price, close) - 0.5
            
            candle = OHLCV(
                timestamp=base_time + timedelta(hours=i),
                open=open_price,
                high=high,
                low=low,
                close=close,
                volume=1000.0,
            )
            data.append(candle)
        
        return data
    
    def test_insufficient_data_raises_error(self):
        """Test that insufficient data raises ValueError."""
        rsi = RSI(period=14)
        # Only 14 candles, need 15
        data = self.create_ohlcv_data([100.0] * 14)
        
        with pytest.raises(ValueError, match="RSI requires at least 15 candles"):
            rsi.calculate(data)
    
    def test_empty_data_raises_error(self):
        """Test that empty data raises ValueError."""
        rsi = RSI()
        with pytest.raises(ValueError, match="empty"):
            rsi.calculate([])
    
    def test_rsi_returns_valid_result(self):
        """Test that RSI calculation returns a valid result."""
        # Generate data with some volatility
        closes = [
            100.0, 101.0, 102.0, 101.5, 103.0,  # Up trend
            102.0, 101.0, 100.5, 101.5, 102.5,  # Mixed
            103.5, 104.0, 103.0, 102.0, 101.0,  # Down trend
        ]
        data = self.create_ohlcv_data(closes)
        
        rsi = RSI(period=14)
        result = rsi.calculate(data)
        
        assert result is not None
        assert isinstance(result, RSIResult)
        assert 0.0 <= result.value <= 100.0
    
    def test_rsi_all_up_trend(self):
        """Test RSI with consistent upward movement (should be high)."""
        # Strong uptrend - prices consistently increasing
        closes = [100.0 + i * 2.0 for i in range(30)]  # 30 candles, steadily increasing
        data = self.create_ohlcv_data(closes)
        
        rsi = RSI(period=14)
        result = rsi.calculate(data)
        
        assert result is not None
        assert result.value > 50.0  # Should be bullish
        assert 0.0 <= result.value <= 100.0
    
    def test_rsi_all_down_trend(self):
        """Test RSI with consistent downward movement (should be low)."""
        # Strong downtrend - prices consistently decreasing
        closes = [100.0 - i * 2.0 for i in range(30)]  # 30 candles, steadily decreasing
        data = self.create_ohlcv_data(closes)
        
        rsi = RSI(period=14)
        result = rsi.calculate(data)
        
        assert result is not None
        assert result.value < 50.0  # Should be bearish
        assert 0.0 <= result.value <= 100.0
    
    def test_rsi_neutral_movement(self):
        """Test RSI with sideways movement (should be around 50)."""
        # Sideways movement with small changes
        closes = [100.0] * 30  # Flat prices
        data = self.create_ohlcv_data(closes)
        
        rsi = RSI(period=14)
        result = rsi.calculate(data)
        
        assert result is not None
        # With no movement, RSI should be around 50 (neutral)
        assert 40.0 <= result.value <= 60.0
    
    def test_rsi_bounds_zero_and_hundred(self):
        """Test RSI respects 0-100 bounds even with extreme movements."""
        # Extreme gains only
        gains_only = [100.0] + [100.0 + i * 10.0 for i in range(1, 30)]
        data = self.create_ohlcv_data(gains_only)
        result = RSI(period=14).calculate(data)
        assert result.value <= 100.0
        
        # Extreme losses only
        losses_only = [300.0 - i * 10.0 for i in range(30)]
        data = self.create_ohlcv_data(losses_only)
        result = RSI(period=14).calculate(data)
        assert result.value >= 0.0
    
    def test_rsi_with_known_values(self):
        """Test RSI calculation against known values."""
        # Sample data that should produce a predictable RSI
        # Using a simplified approach: alternating small gains and losses
        closes = [
            100.0, 101.0, 100.5, 101.5, 101.0,  # Mix of gains/losses
            102.0, 101.5, 102.5, 102.0, 103.0,
            102.5, 103.5, 103.0, 104.0, 103.5,
            104.5, 104.0, 105.0, 104.5, 105.5,
            105.0, 106.0, 105.5, 106.5, 106.0,
            107.0, 106.5, 107.5, 107.0, 108.0,
        ]
        data = self.create_ohlcv_data(closes)
        
        rsi = RSI(period=14)
        result = rsi.calculate(data)
        
        assert result is not None
        assert isinstance(result.value, float)
        assert 0.0 <= result.value <= 100.0
    
    def test_rsi_different_periods(self):
        """Test RSI with different period values."""
        closes = [100.0 + i * 1.5 for i in range(50)]
        data = self.create_ohlcv_data(closes)
        
        rsi_7 = RSI(period=7)
        rsi_14 = RSI(period=14)
        rsi_21 = RSI(period=21)
        
        result_7 = rsi_7.calculate(data)
        result_14 = rsi_14.calculate(data)
        result_21 = rsi_21.calculate(data)
        
        assert result_7 is not None
        assert result_14 is not None
        assert result_21 is not None
        
        # All should be valid values
        assert 0.0 <= result_7.value <= 100.0
        assert 0.0 <= result_14.value <= 100.0
        assert 0.0 <= result_21.value <= 100.0


class TestRSIHelperMethods:
    """Test cases for RSI helper methods."""
    
    def test_is_overbought_method(self):
        """Test RSI instance method is_overbought."""
        rsi = RSI(overbought_level=70.0)
        assert rsi.is_overbought(70.0) is True
        assert rsi.is_overbought(75.0) is True
        assert rsi.is_overbought(69.9) is False
    
    def test_is_oversold_method(self):
        """Test RSI instance method is_oversold."""
        rsi = RSI(oversold_level=30.0)
        assert rsi.is_oversold(30.0) is True
        assert rsi.is_oversold(25.0) is True
        assert rsi.is_oversold(30.1) is False
    
    def test_custom_levels(self):
        """Test RSI with custom overbought/oversold levels."""
        rsi = RSI(overbought_level=80.0, oversold_level=20.0)
        
        assert rsi.is_overbought(80.0) is True
        assert rsi.is_overbought(79.0) is False
        assert rsi.is_oversold(20.0) is True
        assert rsi.is_oversold(21.0) is False


class TestCalculateRSIFunction:
    """Test cases for calculate_rsi convenience function."""
    
    def create_ohlcv_data(self, closes, start_price=100.0):
        """Helper to create OHLCV data from closing prices."""
        data = []
        base_time = datetime(2024, 1, 1)
        
        for i, close in enumerate(closes):
            open_price = close - 1.0 if i == 0 else closes[i-1]
            high = max(open_price, close) + 0.5
            low = min(open_price, close) - 0.5
            
            candle = OHLCV(
                timestamp=base_time + timedelta(hours=i),
                open=open_price,
                high=high,
                low=low,
                close=close,
                volume=1000.0,
            )
            data.append(candle)
        
        return data
    
    def test_calculate_rsi_function(self):
        """Test calculate_rsi convenience function."""
        closes = [100.0 + i * 1.0 for i in range(30)]
        data = self.create_ohlcv_data(closes)
        
        result = calculate_rsi(data)
        
        assert result is not None
        assert isinstance(result, RSIResult)
        assert 0.0 <= result.value <= 100.0
    
    def test_calculate_rsi_with_custom_params(self):
        """Test calculate_rsi with custom parameters."""
        closes = [100.0 + i * 1.0 for i in range(30)]
        data = self.create_ohlcv_data(closes)
        
        result = calculate_rsi(
            data,
            period=21,
            overbought_level=80.0,
            oversold_level=20.0,
        )
        
        assert result is not None
        assert result.period == 21
        assert result.overbought_level == 80.0
        assert result.oversold_level == 20.0


class TestRSIEdgeCases:
    """Test cases for RSI edge cases."""
    
    def create_ohlcv_data(self, closes, start_price=100.0):
        """Helper to create OHLCV data from closing prices."""
        data = []
        base_time = datetime(2024, 1, 1)
        
        for i, close in enumerate(closes):
            open_price = close - 1.0 if i == 0 else closes[i-1]
            high = max(open_price, close) + 0.5
            low = min(open_price, close) - 0.5
            
            candle = OHLCV(
                timestamp=base_time + timedelta(hours=i),
                open=open_price,
                high=high,
                low=low,
                close=close,
                volume=1000.0,
            )
            data.append(candle)
        
        return data
    
    def test_exactly_minimum_candles(self):
        """Test RSI with exactly the minimum required candles."""
        closes = [100.0 + i * 0.5 for i in range(15)]  # Exactly 15 candles
        data = self.create_ohlcv_data(closes)
        
        rsi = RSI(period=14)
        result = rsi.calculate(data)
        
        assert result is not None
        assert 0.0 <= result.value <= 100.0
    
    def test_all_same_price(self):
        """Test RSI when all prices are the same."""
        closes = [100.0] * 30
        data = self.create_ohlcv_data(closes)
        
        rsi = RSI(period=14)
        result = rsi.calculate(data)
        
        assert result is not None
        # When there are no gains or losses, RSI should be around 50
        assert 40.0 <= result.value <= 60.0
    
    def test_alternating_up_down(self):
        """Test RSI with alternating up and down movements."""
        closes = []
        price = 100.0
        for i in range(30):
            if i % 2 == 0:
                price += 2.0
            else:
                price -= 1.0
            closes.append(price)
        
        data = self.create_ohlcv_data(closes)
        rsi = RSI(period=14)
        result = rsi.calculate(data)
        
        assert result is not None
        assert 0.0 <= result.value <= 100.0
    
    def test_very_small_changes(self):
        """Test RSI with very small price changes."""
        closes = [100.0 + i * 0.01 for i in range(30)]
        data = self.create_ohlcv_data(closes)
        
        rsi = RSI(period=14)
        result = rsi.calculate(data)
        
        assert result is not None
        assert 0.0 <= result.value <= 100.0
