"""
Tests for Moving Averages Indicators

Tests for SMA, EMA, and WMA implementations.
"""

import pytest
from datetime import datetime, timedelta
from trading.brokers.base import OHLCV
from trading.indicators.moving_averages import SMA, EMA, WMA


def create_test_data(closes: list, start_price: float = 100.0) -> list:
    """Helper to create OHLCV data from close prices."""
    data = []
    base_time = datetime(2024, 1, 1, 0, 0, 0)
    
    for i, close in enumerate(closes):
        candle = OHLCV(
            timestamp=base_time + timedelta(hours=i),
            open=start_price,
            high=max(start_price, close) + 1,
            low=min(start_price, close) - 1,
            close=close,
            volume=1000.0
        )
        data.append(candle)
    
    return data


class TestSMA:
    """Tests for Simple Moving Average."""

    def test_sma_basic_calculation(self):
        """Test SMA calculation with known values."""
        # Simple test: 5-period SMA with prices [10, 20, 30, 40, 50]
        # SMA = (10+20+30+40+50) / 5 = 30
        closes = [10.0, 20.0, 30.0, 40.0, 50.0]
        data = create_test_data(closes)
        
        sma = SMA(period=5)
        result = sma.calculate(data)
        
        assert result[4] == 30.0
        
    def test_sma_returns_none_for_insufficient_data(self):
        """Test that SMA returns None until enough data is available."""
        closes = [10.0, 20.0, 30.0, 40.0]
        data = create_test_data(closes)
        
        sma = SMA(period=5)
        result = sma.calculate(data)
        
        # All values should be None since we only have 4 candles
        assert all(r is None for r in result)
        
    def test_sma_partial_results(self):
        """Test SMA returns correct partial results."""
        # 3-period SMA with 5 prices
        # Index 0: None (insufficient data)
        # Index 1: None (insufficient data) 
        # Index 2: (10+20+30)/3 = 20
        # Index 3: (20+30+40)/3 = 30
        # Index 4: (30+40+50)/3 = 40
        closes = [10.0, 20.0, 30.0, 40.0, 50.0]
        data = create_test_data(closes)
        
        sma = SMA(period=3)
        result = sma.calculate(data)
        
        assert result[0] is None
        assert result[1] is None
        assert result[2] == 20.0
        assert result[3] == 30.0
        assert result[4] == 40.0
        
    def test_sma_default_period(self):
        """Test SMA with default period of 20."""
        sma = SMA()
        assert sma.period == 20
        assert sma.name == "SMA_20"
        
    def test_sma_custom_period(self):
        """Test SMA with custom period."""
        sma = SMA(period=50)
        assert sma.period == 50
        assert sma.name == "SMA_50"
        
    def test_sma_empty_data_raises_error(self):
        """Test that empty data raises ValueError."""
        sma = SMA(period=5)
        
        with pytest.raises(ValueError, match="Input data is empty"):
            sma.calculate([])
            
    def test_sma_insufficient_data_raises_error(self):
        """Test that insufficient data raises ValueError."""
        closes = [10.0, 20.0]
        data = create_test_data(closes)
        
        sma = SMA(period=5)
        
        with pytest.raises(ValueError, match="Insufficient data"):
            sma.calculate(data)
            
    def test_sma_known_values(self):
        """Test SMA against manually calculated known values."""
        # Data: [100, 101, 102, 103, 104, 105]
        # Period 3:
        # Index 2: (100+101+102)/3 = 101.0
        # Index 3: (101+102+103)/3 = 102.0
        # Index 4: (102+103+104)/3 = 103.0
        # Index 5: (103+104+105)/3 = 104.0
        closes = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0]
        data = create_test_data(closes)
        
        sma = SMA(period=3)
        result = sma.calculate(data)
        
        assert result[2] == pytest.approx(101.0)
        assert result[3] == pytest.approx(102.0)
        assert result[4] == pytest.approx(103.0)
        assert result[5] == pytest.approx(104.0)
        
    def test_sma_get_required_period(self):
        """Test get_required_period returns correct value."""
        sma = SMA(period=10)
        assert sma.get_required_period() == 10


class TestEMA:
    """Tests for Exponential Moving Average."""

    def test_ema_basic_calculation(self):
        """Test EMA calculation with known values."""
        # First EMA = SMA of first period
        # Then: EMA = (Price * k) + (PrevEMA * (1-k))
        # k = 2/(3+1) = 0.5
        # Prices: [10, 20, 30]
        # Index 2 (first EMA): SMA = (10+20+30)/3 = 20
        closes = [10.0, 20.0, 30.0]
        data = create_test_data(closes)
        
        ema = EMA(period=3)
        result = ema.calculate(data)
        
        # First EMA is SMA of first 3 prices
        assert result[2] == 20.0
        
    def test_ema_with_more_data(self):
        """Test EMA with extended data."""
        # Period 3, k = 0.5
        # Prices: [10, 20, 30, 40]
        # EMA[2] = SMA = (10+20+30)/3 = 20
        # EMA[3] = (40 * 0.5) + (20 * 0.5) = 20 + 10 = 30
        closes = [10.0, 20.0, 30.0, 40.0]
        data = create_test_data(closes)
        
        ema = EMA(period=3)
        result = ema.calculate(data)
        
        assert result[2] == 20.0
        assert result[3] == 30.0
        
    def test_ema_partial_results(self):
        """Test EMA returns correct partial results."""
        closes = [10.0, 20.0, 30.0, 40.0, 50.0]
        data = create_test_data(closes)
        
        ema = EMA(period=3)
        result = ema.calculate(data)
        
        # First 2 should be None
        assert result[0] is None
        assert result[1] is None
        # Index 2 is first EMA (SMA)
        assert result[2] is not None
        # Remaining should have values
        assert result[3] is not None
        assert result[4] is not None
        
    def test_ema_default_period(self):
        """Test EMA with default period of 20."""
        ema = EMA()
        assert ema.period == 20
        assert ema.name == "EMA_20"
        assert ema.multiplier == 2 / (20 + 1)
        
    def test_ema_custom_period(self):
        """Test EMA with custom period."""
        ema = EMA(period=10)
        assert ema.period == 10
        assert ema.name == "EMA_10"
        assert ema.multiplier == 2 / (10 + 1)
        
    def test_ema_empty_data_raises_error(self):
        """Test that empty data raises ValueError."""
        ema = EMA(period=5)
        
        with pytest.raises(ValueError, match="Input data is empty"):
            ema.calculate([])
            
    def test_ema_insufficient_data_raises_error(self):
        """Test that insufficient data raises ValueError."""
        closes = [10.0, 20.0]
        data = create_test_data(closes)
        
        ema = EMA(period=5)
        
        with pytest.raises(ValueError, match="Insufficient data"):
            ema.calculate(data)
            
    def test_ema_known_values_period_3(self):
        """Test EMA against manually calculated known values for period 3."""
        # Period 3, k = 2/(3+1) = 0.5
        # Prices: [100, 102, 101, 103, 105]
        # Index 2: SMA = (100+102+101)/3 = 101.0
        # Index 3: (103 * 0.5) + (101 * 0.5) = 51.5 + 50.5 = 102.0
        # Index 4: (105 * 0.5) + (102 * 0.5) = 52.5 + 51.0 = 103.5
        closes = [100.0, 102.0, 101.0, 103.0, 105.0]
        data = create_test_data(closes)
        
        ema = EMA(period=3)
        result = ema.calculate(data)
        
        assert result[2] == pytest.approx(101.0)
        assert result[3] == pytest.approx(102.0)
        assert result[4] == pytest.approx(103.5)
        
    def test_ema_get_required_period(self):
        """Test get_required_period returns correct value."""
        ema = EMA(period=15)
        assert ema.get_required_period() == 15
        
    def test_ema_responds_faster_than_sma(self):
        """Test that EMA responds faster to price changes than SMA."""
        # Create data with a sudden jump
        closes = [10.0, 10.0, 10.0, 10.0, 50.0]  # Sudden jump at end
        data = create_test_data(closes)
        
        sma = SMA(period=5)
        ema = EMA(period=5)
        
        sma_result = sma.calculate(data)
        ema_result = ema.calculate(data)
        
        # Both should have a value at index 4
        # EMA should be higher (more weight to recent 50.0 price)
        assert ema_result[4] > sma_result[4]


class TestWMA:
    """Tests for Weighted Moving Average."""

    def test_wma_basic_calculation(self):
        """Test WMA calculation with known values."""
        # Period 3, weights: [1, 2, 3], sum = 6
        # Prices: [10, 20, 30]
        # WMA = (10*1 + 20*2 + 30*3) / 6 = (10 + 40 + 90) / 6 = 140 / 6 = 23.333...
        closes = [10.0, 20.0, 30.0]
        data = create_test_data(closes)
        
        wma = WMA(period=3)
        result = wma.calculate(data)
        
        assert result[2] == pytest.approx(23.333333, rel=1e-5)
        
    def test_wma_partial_results(self):
        """Test WMA returns correct partial results."""
        # Period 3 with 5 prices
        # Index 0, 1: None (insufficient data)
        # Index 2: (p0*1 + p1*2 + p2*3)/6
        # Index 3: (p1*1 + p2*2 + p3*3)/6
        # Index 4: (p2*1 + p3*2 + p4*3)/6
        closes = [10.0, 20.0, 30.0, 40.0, 50.0]
        data = create_test_data(closes)
        
        wma = WMA(period=3)
        result = wma.calculate(data)
        
        assert result[0] is None
        assert result[1] is None
        # (10*1 + 20*2 + 30*3)/6 = 140/6 = 23.333
        assert result[2] == pytest.approx(23.333333, rel=1e-5)
        # (20*1 + 30*2 + 40*3)/6 = 200/6 = 33.333
        assert result[3] == pytest.approx(33.333333, rel=1e-5)
        # (30*1 + 40*2 + 50*3)/6 = 260/6 = 43.333
        assert result[4] == pytest.approx(43.333333, rel=1e-5)
        
    def test_wma_default_period(self):
        """Test WMA with default period of 20."""
        wma = WMA()
        assert wma.period == 20
        assert wma.name == "WMA_20"
        assert wma.weights == list(range(1, 21))
        assert wma.weight_sum == sum(range(1, 21))
        
    def test_wma_custom_period(self):
        """Test WMA with custom period."""
        wma = WMA(period=5)
        assert wma.period == 5
        assert wma.name == "WMA_5"
        assert wma.weights == [1, 2, 3, 4, 5]
        assert wma.weight_sum == 15
        
    def test_wma_empty_data_raises_error(self):
        """Test that empty data raises ValueError."""
        wma = WMA(period=5)
        
        with pytest.raises(ValueError, match="Input data is empty"):
            wma.calculate([])
            
    def test_wma_insufficient_data_raises_error(self):
        """Test that insufficient data raises ValueError."""
        closes = [10.0, 20.0]
        data = create_test_data(closes)
        
        wma = WMA(period=5)
        
        with pytest.raises(ValueError, match="Insufficient data"):
            wma.calculate(data)
            
    def test_wma_known_values_period_4(self):
        """Test WMA against manually calculated known values for period 4."""
        # Period 4, weights: [1, 2, 3, 4], sum = 10
        # Prices: [10, 20, 30, 40]
        # WMA = (10*1 + 20*2 + 30*3 + 40*4) / 10 = (10 + 40 + 90 + 160) / 10 = 300/10 = 30
        closes = [10.0, 20.0, 30.0, 40.0]
        data = create_test_data(closes)
        
        wma = WMA(period=4)
        result = wma.calculate(data)
        
        assert result[3] == 30.0
        
    def test_wma_get_required_period(self):
        """Test get_required_period returns correct value."""
        wma = WMA(period=12)
        assert wma.get_required_period() == 12
        
    def test_wma_weights_increasing(self):
        """Test that WMA gives more weight to recent prices."""
        # Create data where older prices are higher
        closes = [50.0, 40.0, 30.0, 20.0, 10.0]  # Decreasing
        data = create_test_data(closes)
        
        wma = WMA(period=5)
        sma = SMA(period=5)
        
        wma_result = wma.calculate(data)
        sma_result = sma.calculate(data)
        
        # WMA should be lower than SMA because more weight is on recent lower prices
        assert wma_result[4] < sma_result[4]


class TestMovingAveragesComparison:
    """Tests comparing the three moving average types."""

    def test_all_ma_same_period_same_name_format(self):
        """Test that all MAs follow the same naming convention."""
        sma = SMA(period=10)
        ema = EMA(period=10)
        wma = WMA(period=10)
        
        assert sma.name == "SMA_10"
        assert ema.name == "EMA_10"
        assert wma.name == "WMA_10"
        
    def test_all_ma_same_required_period(self):
        """Test that all MAs report the same required period."""
        sma = SMA(period=10)
        ema = EMA(period=10)
        wma = WMA(period=10)
        
        assert sma.get_required_period() == 10
        assert ema.get_required_period() == 10
        assert wma.get_required_period() == 10
        
    def test_all_ma_with_same_data(self):
        """Test all MAs produce results with the same data."""
        closes = [float(i) for i in range(1, 26)]  # 25 prices
        data = create_test_data(closes)
        
        sma = SMA(period=20)
        ema = EMA(period=20)
        wma = WMA(period=20)
        
        sma_result = sma.calculate(data)
        ema_result = ema.calculate(data)
        wma_result = wma.calculate(data)
        
        # All should have same length
        assert len(sma_result) == len(ema_result) == len(wma_result) == 25
        
        # First 19 should be None for all
        for i in range(19):
            assert sma_result[i] is None
            assert ema_result[i] is None
            assert wma_result[i] is None
            
        # Last 6 should have values
        for i in range(19, 25):
            assert sma_result[i] is not None
            assert ema_result[i] is not None
            assert wma_result[i] is not None
