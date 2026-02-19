"""
Unit tests for Bollinger Bands indicator.
"""

import pytest
from datetime import datetime, timedelta
from trading.brokers.base import OHLCV
from trading.indicators.bollinger_bands import BollingerBands, BollingerBandsResult


def create_ohlcv_data(closes, opens=None, highs=None, lows=None, volumes=None):
    """Helper function to create OHLCV data from closing prices."""
    data = []
    base_time = datetime(2024, 1, 1)
    
    for i, close in enumerate(closes):
        open_price = opens[i] if opens else close
        high = highs[i] if highs else close + 1.0
        low = lows[i] if lows else close - 1.0
        volume = volumes[i] if volumes else 1000 + i
        
        data.append(OHLCV(
            timestamp=base_time + timedelta(hours=i),
            open=open_price,
            high=high,
            low=low,
            close=close,
            volume=volume
        ))
    return data


class TestBollingerBandsInitialization:
    """Test BollingerBands initialization and configuration."""
    
    def test_default_initialization(self):
        """Test default period and multiplier values."""
        bb = BollingerBands()
        assert bb.period == 20
        assert bb.multiplier == 2.0
        assert bb.name == "BB_20_2.0"
    
    def test_custom_initialization(self):
        """Test custom period and multiplier values."""
        bb = BollingerBands(period=10, multiplier=1.5)
        assert bb.period == 10
        assert bb.multiplier == 1.5
        assert bb.name == "BB_10_1.5"
    
    def test_get_required_period(self):
        """Test get_required_period returns the configured period."""
        bb = BollingerBands(period=15)
        assert bb.get_required_period() == 15


class TestBollingerBandsCalculation:
    """Test Bollinger Bands calculation logic."""
    
    def test_insufficient_data_raises_error(self):
        """Test that calculation raises error with insufficient data."""
        bb = BollingerBands(period=20)
        data = create_ohlcv_data([100.0] * 10)  # Only 10 candles
        
        with pytest.raises(ValueError, match="Insufficient data"):
            bb.calculate(data)
    
    def test_empty_data_raises_error(self):
        """Test that calculation raises error with empty data."""
        bb = BollingerBands()
        
        with pytest.raises(ValueError, match="empty"):
            bb.calculate([])
    
    def test_exact_period_data(self):
        """Test calculation with exactly period candles."""
        bb = BollingerBands(period=20)
        # Constant price = no volatility
        closes = [100.0] * 20
        data = create_ohlcv_data(closes)
        
        results = bb.calculate(data)
        
        assert len(results) == 20
        # First 19 should be None (insufficient data)
        for i in range(19):
            assert results[i].upper is None
            assert results[i].middle is None
            assert results[i].lower is None
        
        # Last one should have values
        last = results[-1]
        assert last.middle == 100.0
        assert last.upper == 100.0  # No std dev with constant prices
        assert last.lower == 100.0
    
    def test_bollinger_bands_with_volatility(self):
        """Test calculation with volatile prices."""
        bb = BollingerBands(period=5, multiplier=2.0)
        # Prices with known standard deviation
        closes = [100.0, 102.0, 101.0, 103.0, 104.0]
        data = create_ohlcv_data(closes)
        
        results = bb.calculate(data)
        
        # First 4 should be None
        for i in range(4):
            assert results[i].middle is None
        
        # Last result should have calculated values
        last = results[-1]
        assert last.middle is not None
        assert last.upper > last.middle
        assert last.lower < last.middle
        assert last.upper > last.lower
    
    def test_band_width_calculation(self):
        """Test band width calculation."""
        bb = BollingerBands(period=5, multiplier=2.0)
        closes = [100.0, 102.0, 101.0, 103.0, 104.0]
        data = create_ohlcv_data(closes)
        
        results = bb.calculate(data)
        last = results[-1]
        
        # Band width = (Upper - Lower) / Middle
        expected_bandwidth = (last.upper - last.lower) / last.middle
        assert last.bandwidth == pytest.approx(expected_bandwidth, rel=1e-10)
    
    def test_percent_b_calculation(self):
        """Test %B calculation."""
        bb = BollingerBands(period=5, multiplier=2.0)
        closes = [100.0, 102.0, 101.0, 103.0, 104.0]
        data = create_ohlcv_data(closes)
        
        results = bb.calculate(data)
        last = results[-1]
        
        # %B = (Price - Lower) / (Upper - Lower)
        expected_percent_b = (104.0 - last.lower) / (last.upper - last.lower)
        assert last.percent_b == pytest.approx(expected_percent_b, rel=1e-10)
    
    def test_known_values_verification(self):
        """Test with known expected values for verification."""
        bb = BollingerBands(period=5, multiplier=2.0)
        # Simple increasing sequence: 1, 2, 3, 4, 5
        # Mean = 3.0
        # StdDev = sqrt(((4+1+0+1+4)/5)) = sqrt(2) ≈ 1.414
        # Upper = 3 + 2*1.414 ≈ 5.828
        # Lower = 3 - 2*1.414 ≈ 0.172
        closes = [1.0, 2.0, 3.0, 4.0, 5.0]
        data = create_ohlcv_data(closes)
        
        results = bb.calculate(data)
        last = results[-1]
        
        assert last.middle == pytest.approx(3.0, rel=1e-10)
        assert last.upper == pytest.approx(5.828, abs=0.001)
        assert last.lower == pytest.approx(0.172, abs=0.001)
        
        # %B at price 5.0 = (5 - 0.172) / (5.828 - 0.172) ≈ 0.853
        assert last.percent_b == pytest.approx(0.853, abs=0.001)
        
        # Band Width = (5.828 - 0.172) / 3.0 ≈ 1.885
        assert last.bandwidth == pytest.approx(1.885, abs=0.001)


class TestBollingerBandsHelperMethods:
    """Test helper methods for position checking."""
    
    @pytest.fixture
    def sample_result(self):
        """Create a sample BollingerBandsResult for testing."""
        return BollingerBandsResult(
            upper=110.0,
            middle=100.0,
            lower=90.0,
            bandwidth=0.2,
            percent_b=0.5
        )
    
    def test_is_price_above_upper_true(self, sample_result):
        """Test price above upper band detection."""
        bb = BollingerBands()
        assert bb.is_price_above_upper(sample_result, 115.0) is True
    
    def test_is_price_above_upper_false(self, sample_result):
        """Test price above upper band detection when false."""
        bb = BollingerBands()
        assert bb.is_price_above_upper(sample_result, 105.0) is False
    
    def test_is_price_below_lower_true(self, sample_result):
        """Test price below lower band detection."""
        bb = BollingerBands()
        assert bb.is_price_below_lower(sample_result, 85.0) is True
    
    def test_is_price_below_lower_false(self, sample_result):
        """Test price below lower band detection when false."""
        bb = BollingerBands()
        assert bb.is_price_below_lower(sample_result, 95.0) is False
    
    def test_is_price_inside_bands(self, sample_result):
        """Test price inside bands detection."""
        bb = BollingerBands()
        assert bb.is_price_inside_bands(sample_result, 100.0) is True
        assert bb.is_price_inside_bands(sample_result, 90.0) is True  # At lower
        assert bb.is_price_inside_bands(sample_result, 110.0) is True  # At upper
    
    def test_is_price_inside_bands_false(self, sample_result):
        """Test price inside bands detection when false."""
        bb = BollingerBands()
        assert bb.is_price_inside_bands(sample_result, 85.0) is False
        assert bb.is_price_inside_bands(sample_result, 115.0) is False
    
    def test_get_position_within_bands(self, sample_result):
        """Test relative position calculation."""
        bb = BollingerBands()
        
        # At lower band
        assert bb.get_position_within_bands(sample_result, 90.0) == 0.0
        
        # At middle band (100 is midway between 90 and 110)
        assert bb.get_position_within_bands(sample_result, 100.0) == 0.5
        
        # At upper band
        assert bb.get_position_within_bands(sample_result, 110.0) == 1.0
        
        # Quarter way up
        assert bb.get_position_within_bands(sample_result, 95.0) == 0.25
    
    def test_get_position_clamping(self, sample_result):
        """Test position clamping outside bands."""
        bb = BollingerBands()
        
        # Below lower should clamp to 0
        assert bb.get_position_within_bands(sample_result, 80.0) == 0.0
        
        # Above upper should clamp to 1
        assert bb.get_position_within_bands(sample_result, 120.0) == 1.0
    
    def test_get_position_none_result(self):
        """Test position with None result values."""
        bb = BollingerBands()
        empty_result = BollingerBandsResult()
        
        assert bb.get_position_within_bands(empty_result, 100.0) is None
        assert bb.is_price_above_upper(empty_result, 100.0) is False
        assert bb.is_price_below_lower(empty_result, 100.0) is False
        assert bb.is_price_inside_bands(empty_result, 100.0) is False


class TestBollingerBandsResult:
    """Test BollingerBandsResult dataclass."""
    
    def test_result_creation(self):
        """Test creating a BollingerBandsResult."""
        result = BollingerBandsResult(
            upper=110.0,
            middle=100.0,
            lower=90.0,
            bandwidth=0.2,
            percent_b=0.5
        )
        
        assert result.upper == 110.0
        assert result.middle == 100.0
        assert result.lower == 90.0
        assert result.bandwidth == 0.2
        assert result.percent_b == 0.5
    
    def test_result_to_dict(self):
        """Test conversion to dictionary."""
        result = BollingerBandsResult(
            upper=110.0,
            middle=100.0,
            lower=90.0,
            bandwidth=0.2,
            percent_b=0.5
        )
        
        d = result.to_dict()
        assert d['upper'] == 110.0
        assert d['middle'] == 100.0
        assert d['lower'] == 90.0
        assert d['bandwidth'] == 0.2
        assert d['percent_b'] == 0.5
    
    def test_empty_result(self):
        """Test empty result with default None values."""
        result = BollingerBandsResult()
        
        assert result.upper is None
        assert result.middle is None
        assert result.lower is None
        assert result.bandwidth is None
        assert result.percent_b is None


class TestBollingerBandsIntegration:
    """Integration tests with real-world-like scenarios."""
    
    def test_trending_market(self):
        """Test Bollinger Bands in trending market."""
        bb = BollingerBands(period=20)
        # Strong uptrend
        closes = [100.0 + i * 0.5 for i in range(30)]
        data = create_ohlcv_data(closes)
        
        results = bb.calculate(data)
        
        # Check that bands expand with trend
        valid_results = [r for r in results if r.middle is not None]
        assert len(valid_results) == 11  # 30 - 20 + 1
        
        # All results should have upper > middle > lower
        for r in valid_results:
            assert r.upper > r.middle > r.lower
    
    def test_sideways_market(self):
        """Test Bollinger Bands in sideways/ranging market."""
        bb = BollingerBands(period=10)
        # Oscillating prices
        closes = [100.0, 101.0, 100.0, 99.0, 100.0] * 5
        data = create_ohlcv_data(closes)
        
        results = bb.calculate(data)
        valid_results = [r for r in results if r.middle is not None]
        
        # Should have valid calculations
        assert len(valid_results) > 0
        
        for r in valid_results:
            assert r.upper is not None
            assert r.lower is not None
            # Bandwidth should be non-zero
            assert r.bandwidth > 0
    
    def test_result_length_matches_input(self):
        """Test that result length matches input data length."""
        bb = BollingerBands(period=20)
        closes = [100.0] * 50
        data = create_ohlcv_data(closes)
        
        results = bb.calculate(data)
        
        assert len(results) == len(data)


class TestBollingerBandsDifferentMultipliers:
    """Test Bollinger Bands with different standard deviation multipliers."""
    
    def test_multiplier_1_0(self):
        """Test with multiplier of 1.0."""
        bb = BollingerBands(period=5, multiplier=1.0)
        closes = [100.0, 102.0, 101.0, 103.0, 104.0]
        data = create_ohlcv_data(closes)
        
        results = bb.calculate(data)
        last = results[-1]
        
        band_width = last.upper - last.lower
        # With multiplier 1.0, bands should be tighter
        assert band_width > 0
    
    def test_multiplier_3_0(self):
        """Test with multiplier of 3.0."""
        bb = BollingerBands(period=5, multiplier=3.0)
        closes = [100.0, 102.0, 101.0, 103.0, 104.0]
        data = create_ohlcv_data(closes)
        
        results = bb.calculate(data)
        last = results[-1]
        
        band_width = last.upper - last.lower
        # With multiplier 3.0, bands should be wider
        assert band_width > 0
    
    def test_multiplier_comparison(self):
        """Compare bands with different multipliers."""
        closes = [100.0, 102.0, 101.0, 103.0, 104.0]
        data = create_ohlcv_data(closes)
        
        bb_1 = BollingerBands(period=5, multiplier=1.0)
        bb_2 = BollingerBands(period=5, multiplier=2.0)
        bb_3 = BollingerBands(period=5, multiplier=3.0)
        
        results_1 = bb_1.calculate(data)
        results_2 = bb_2.calculate(data)
        results_3 = bb_3.calculate(data)
        
        width_1 = results_1[-1].upper - results_1[-1].lower
        width_2 = results_2[-1].upper - results_2[-1].lower
        width_3 = results_3[-1].upper - results_3[-1].lower
        
        # Wider multiplier = wider bands
        assert width_1 < width_2 < width_3
