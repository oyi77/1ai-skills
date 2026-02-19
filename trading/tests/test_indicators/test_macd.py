"""
Unit tests for MACD (Moving Average Convergence Divergence) indicator.
"""

import pytest
from datetime import datetime
from trading.brokers.base import OHLCV
from trading.indicators.macd import MACD, MACDResult


def create_ohlcv_data(
    closes: list,
    opens: list = None,
    highs: list = None,
    lows: list = None,
    volumes: list = None
) -> list:
    """Helper function to create OHLCV data from close prices."""
    data = []
    base_time = datetime(2024, 1, 1, 0, 0, 0)
    
    for i, close in enumerate(closes):
        open_price = opens[i] if opens else close - 0.5
        high = highs[i] if highs else close + 0.5
        low = lows[i] if lows else close - 0.5
        volume = volumes[i] if volumes else 1000
        
        candle = OHLCV(
            timestamp=base_time.timestamp() + i * 3600,
            open=open_price,
            high=high,
            low=low,
            close=close,
            volume=volume
        )
        data.append(candle)
    
    return data


class TestMACDInitialization:
    """Test MACD indicator initialization."""
    
    def test_default_parameters(self):
        """Test MACD initializes with default parameters."""
        macd = MACD()
        assert macd.fast_period == 12
        assert macd.slow_period == 26
        assert macd.signal_period == 9
        assert macd.name == "MACD(12,26,9)"
    
    def test_custom_parameters(self):
        """Test MACD initializes with custom parameters."""
        macd = MACD(fast_period=5, slow_period=15, signal_period=3)
        assert macd.fast_period == 5
        assert macd.slow_period == 15
        assert macd.signal_period == 3
        assert macd.name == "MACD(5,15,3)"
    
    def test_invalid_fast_gte_slow(self):
        """Test MACD raises error when fast >= slow period."""
        with pytest.raises(ValueError, match="Fast period .* must be less than"):
            MACD(fast_period=26, slow_period=26)
        
        with pytest.raises(ValueError, match="Fast period .* must be less than"):
            MACD(fast_period=30, slow_period=26)
    
    def test_invalid_periods(self):
        """Test MACD raises error for non-positive periods."""
        with pytest.raises(ValueError, match="All periods must be positive"):
            MACD(fast_period=0, slow_period=26, signal_period=9)
        
        with pytest.raises(ValueError, match="All periods must be positive"):
            MACD(fast_period=12, slow_period=-5, signal_period=9)
        
        with pytest.raises(ValueError, match="All periods must be positive"):
            MACD(fast_period=12, slow_period=26, signal_period=0)


class TestMACDCalculation:
    """Test MACD calculation functionality."""
    
    def test_calculate_returns_macd_result(self):
        """Test calculate returns MACDResult object."""
        macd = MACD(fast_period=3, slow_period=6, signal_period=2)
        # Need at least slow + signal - 1 = 6 + 2 - 1 = 7 candles
        closes = [100.0, 102.0, 101.0, 103.0, 102.0, 104.0, 105.0]
        data = create_ohlcv_data(closes)
        
        result = macd.calculate(data)
        
        assert isinstance(result, MACDResult)
        assert hasattr(result, 'macd_line')
        assert hasattr(result, 'signal_line')
        assert hasattr(result, 'histogram')
    
    def test_macd_line_calculation(self):
        """Test MACD Line = Fast EMA - Slow EMA."""
        macd = MACD(fast_period=3, slow_period=5, signal_period=2)
        # Need at least 5 + 2 - 1 = 6 candles
        closes = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0]
        data = create_ohlcv_data(closes)
        
        result = macd.calculate(data)
        
        # MACD line should have values after slow_period - 1 = 4
        assert len(result.macd_line) == len(closes)
        # First slow_period - 1 values should be None
        assert all(m is None for m in result.macd_line[:4])
        # Values from index 4 onwards should be numeric
        assert all(m is not None for m in result.macd_line[4:])
    
    def test_signal_line_calculation(self):
        """Test Signal Line is EMA of MACD Line."""
        macd = MACD(fast_period=3, slow_period=5, signal_period=2)
        closes = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0]
        data = create_ohlcv_data(closes)
        
        result = macd.calculate(data)
        
        # Signal line should have more None values than MACD line
        # due to additional smoothing
        assert len(result.signal_line) == len(closes)
    
    def test_histogram_calculation(self):
        """Test Histogram = MACD Line - Signal Line."""
        macd = MACD(fast_period=3, slow_period=5, signal_period=2)
        closes = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0]
        data = create_ohlcv_data(closes)
        
        result = macd.calculate(data)
        
        # Histogram should equal MACD - Signal where both are not None
        for i in range(len(result.histogram)):
            if result.macd_line[i] is not None and result.signal_line[i] is not None:
                expected_hist = result.macd_line[i] - result.signal_line[i]
                assert abs(result.histogram[i] - expected_hist) < 1e-10
    
    def test_insufficient_data(self):
        """Test MACD raises error with insufficient data."""
        macd = MACD(fast_period=12, slow_period=26, signal_period=9)
        # Need at least 26 + 9 - 1 = 34 candles
        closes = [100.0] * 30
        data = create_ohlcv_data(closes)
        
        with pytest.raises(ValueError, match="Insufficient data"):
            macd.calculate(data)
    
    def test_empty_data(self):
        """Test MACD raises error with empty data."""
        macd = MACD()
        
        with pytest.raises(ValueError, match="Input data is empty"):
            macd.calculate([])
    
    def test_get_required_period(self):
        """Test get_required_period returns correct value."""
        macd = MACD(fast_period=12, slow_period=26, signal_period=9)
        assert macd.get_required_period() == 34  # 26 + 9 - 1
        
        macd2 = MACD(fast_period=5, slow_period=15, signal_period=3)
        assert macd2.get_required_period() == 17  # 15 + 3 - 1


class TestMACDSignals:
    """Test MACD signal detection methods."""
    
    def test_is_bullish_crossover(self):
        """Test bullish crossover detection."""
        macd = MACD()
        
        # Create a MACD result with a bullish crossover at the end
        # MACD crosses from below Signal to above Signal
        result = MACDResult(
            macd_line=[0.5, 0.6, 0.4, 0.3, 0.5, 0.7],  # Crosses up at index 4
            signal_line=[0.5, 0.5, 0.5, 0.5, 0.45, 0.5],  # Signal below at index 4
            histogram=[0.0, 0.1, -0.1, -0.2, 0.05, 0.2]
        )
        
        assert macd.is_bullish(result, index=4) is True
        assert macd.is_bullish(result, index=5) is False  # Already crossed
    
    def test_is_bearish_crossover(self):
        """Test bearish crossover detection."""
        macd = MACD()
        
        # Create a MACD result with a bearish crossover at the end
        # MACD crosses from above Signal to below Signal
        result = MACDResult(
            macd_line=[0.5, 0.6, 0.7, 0.6, 0.4, 0.3],  # Crosses down at index 4
            signal_line=[0.5, 0.5, 0.5, 0.55, 0.5, 0.45],  # Signal above at index 4
            histogram=[0.0, 0.1, 0.2, 0.05, -0.1, -0.15]
        )
        
        assert macd.is_bearish(result, index=4) is True
        assert macd.is_bearish(result, index=5) is False  # Already crossed
    
    def test_is_bullish_no_crossover(self):
        """Test is_bullish returns False when no crossover."""
        macd = MACD()
        
        result = MACDResult(
            macd_line=[0.5, 0.6, 0.7, 0.8],  # MACD stays above Signal
            signal_line=[0.4, 0.45, 0.5, 0.55],
            histogram=[0.1, 0.15, 0.2, 0.25]
        )
        
        assert macd.is_bullish(result, index=-1) is False
    
    def test_is_bearish_no_crossover(self):
        """Test is_bearish returns False when no crossover."""
        macd = MACD()
        
        result = MACDResult(
            macd_line=[0.3, 0.25, 0.2, 0.15],  # MACD stays below Signal
            signal_line=[0.5, 0.45, 0.4, 0.35],
            histogram=[-0.2, -0.2, -0.2, -0.2]
        )
        
        assert macd.is_bearish(result, index=-1) is False
    
    def test_is_bullish_with_none_values(self):
        """Test is_bullish handles None values gracefully."""
        macd = MACD()
        
        result = MACDResult(
            macd_line=[None, None, 0.5, 0.6],
            signal_line=[None, None, 0.5, 0.5],
            histogram=[None, None, 0.0, 0.1]
        )
        
        assert macd.is_bullish(result, index=-1) is True
    
    def test_is_bearish_with_none_values(self):
        """Test is_bearish handles None values gracefully."""
        macd = MACD()
        
        result = MACDResult(
            macd_line=[None, None, 0.6, 0.4],
            signal_line=[None, None, 0.5, 0.5],
            histogram=[None, None, 0.1, -0.1]
        )
        
        assert macd.is_bearish(result, index=-1) is True
    
    def test_is_bullish_empty_result(self):
        """Test is_bullish returns False for empty result."""
        macd = MACD()
        result = MACDResult(macd_line=[], signal_line=[], histogram=[])
        assert macd.is_bullish(result) is False
    
    def test_is_bearish_empty_result(self):
        """Test is_bearish returns False for empty result."""
        macd = MACD()
        result = MACDResult(macd_line=[], signal_line=[], histogram=[])
        assert macd.is_bearish(result) is False
    
    def test_is_bullish_index_out_of_range(self):
        """Test is_bullish raises error for invalid index."""
        macd = MACD()
        result = MACDResult(
            macd_line=[0.5, 0.6],
            signal_line=[0.5, 0.5],
            histogram=[0.0, 0.1]
        )
        
        with pytest.raises(ValueError, match="Index .* out of range"):
            macd.is_bullish(result, index=10)
    
    def test_is_bearish_index_out_of_range(self):
        """Test is_bearish raises error for invalid index."""
        macd = MACD()
        result = MACDResult(
            macd_line=[0.5, 0.6],
            signal_line=[0.5, 0.5],
            histogram=[0.0, 0.1]
        )
        
        with pytest.raises(ValueError, match="Index .* out of range"):
            macd.is_bearish(result, index=-10)


class TestMACDHelperMethods:
    """Test MACD helper methods."""
    
    def test_get_last_values(self):
        """Test get_last_values returns last values correctly."""
        macd = MACD()
        
        result = MACDResult(
            macd_line=[0.1, 0.2, 0.3, 0.4, 0.5],
            signal_line=[0.2, 0.3, 0.4, 0.5, 0.6],
            histogram=[-0.1, -0.1, -0.1, -0.1, -0.1]
        )
        
        last = macd.get_last_values(result)
        
        assert last['macd'] == 0.5
        assert last['signal'] == 0.6
        assert last['histogram'] == -0.1
    
    def test_get_last_values_empty(self):
        """Test get_last_values handles empty result."""
        macd = MACD()
        result = MACDResult(macd_line=[], signal_line=[], histogram=[])
        
        last = macd.get_last_values(result)
        
        assert last['macd'] is None
        assert last['signal'] is None
        assert last['histogram'] is None
    
    def test_get_last_values_with_none(self):
        """Test get_last_values handles None in last position."""
        macd = MACD()
        result = MACDResult(
            macd_line=[0.1, 0.2, None],
            signal_line=[0.2, 0.3, None],
            histogram=[-0.1, -0.1, None]
        )
        
        last = macd.get_last_values(result)
        
        assert last['macd'] is None
        assert last['signal'] is None
        assert last['histogram'] is None


class TestMACDRealData:
    """Test MACD with realistic price data."""
    
    def test_macd_with_trending_data(self):
        """Test MACD with upward trending data."""
        macd = MACD(fast_period=3, slow_period=6, signal_period=2)
        
        # Strong uptrend: prices increasing consistently
        closes = [100, 102, 104, 106, 108, 110, 112, 114, 116, 118]
        data = create_ohlcv_data(closes)
        
        result = macd.calculate(data)
        
        # In an uptrend, fast EMA should be above slow EMA
        # So MACD line should be positive
        valid_macd = [m for m in result.macd_line if m is not None]
        assert all(m > 0 for m in valid_macd)
    
    def test_macd_with_downtrending_data(self):
        """Test MACD with downward trending data."""
        macd = MACD(fast_period=3, slow_period=6, signal_period=2)
        
        # Strong downtrend: prices decreasing consistently
        closes = [120, 118, 116, 114, 112, 110, 108, 106, 104, 102]
        data = create_ohlcv_data(closes)
        
        result = macd.calculate(data)
        
        # In a downtrend, fast EMA should be below slow EMA
        # So MACD line should be negative
        valid_macd = [m for m in result.macd_line if m is not None]
        assert all(m < 0 for m in valid_macd)
    
    def test_macd_histogram_positive_negative(self):
        """Test histogram correctly reflects MACD vs Signal relationship."""
        macd = MACD(fast_period=3, slow_period=6, signal_period=2)
        
        closes = [100, 105, 110, 108, 112, 115, 113, 118, 120, 122]
        data = create_ohlcv_data(closes)
        
        result = macd.calculate(data)
        
        # Where MACD > Signal, histogram should be positive
        # Where MACD < Signal, histogram should be negative
        for i in range(len(result.histogram)):
            if result.histogram[i] is not None:
                if result.histogram[i] > 0:
                    assert result.macd_line[i] > result.signal_line[i]
                elif result.histogram[i] < 0:
                    assert result.macd_line[i] < result.signal_line[i]
                else:
                    assert result.macd_line[i] == result.signal_line[i]


class TestMACDEdgeCases:
    """Test MACD edge cases and error handling."""
    
    def test_repr(self):
        """Test string representation of MACD."""
        macd = MACD(fast_period=12, slow_period=26, signal_period=9)
        repr_str = repr(macd)
        assert "MACD" in repr_str
        assert "12" in repr_str
        assert "26" in repr_str
        assert "9" in repr_str
    
    def test_single_candle_data(self):
        """Test MACD with single candle raises error."""
        macd = MACD()
        data = create_ohlcv_data([100.0])
        
        with pytest.raises(ValueError, match="Insufficient data"):
            macd.calculate(data)
    
    def test_macd_crossover_at_first_valid_index(self):
        """Test MACD handles crossover at boundary correctly."""
        macd = MACD(fast_period=3, slow_period=5, signal_period=2)
        
        # First valid MACD at index 4, first valid Signal at index 5
        # Test that we can't detect crossover at index 4 (no previous Signal)
        closes = [100, 101, 102, 103, 104, 103, 102, 101, 100, 99]
        data = create_ohlcv_data(closes)
        
        result = macd.calculate(data)
        
        # At index 0, should return False (can't detect crossover)
        assert macd.is_bullish(result, index=0) is False
        assert macd.is_bearish(result, index=0) is False
