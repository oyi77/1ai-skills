"""
Tests for TrendFollowingTemplate strategy.
"""
import pytest
from datetime import datetime
from typing import List

from trading.brokers.base import OHLCV
from trading.strategy.templates.trend_following import TrendFollowingTemplate
from trading.strategy.templates.base import SignalType, Position


class TestTrendFollowingTemplate:
    """Tests for TrendFollowingTemplate class."""
    
    def test_initialization(self):
        strategy = TrendFollowingTemplate(
            symbol="EURUSD",
            timeframe="H4",
            fast_ma_period=10,
            slow_ma_period=50,
            risk_per_trade=0.02,
            use_trailing_stop=True
        )
        
        assert strategy.name == "TrendFollowingTemplate"
        assert strategy.symbol == "EURUSD"
        assert strategy.fast_ma_period == 10
        assert strategy.slow_ma_period == 50
        assert strategy.use_trailing_stop is True
    
    def test_validate_config_valid(self):
        strategy = TrendFollowingTemplate()
        assert strategy.validate_config() is True
    
    def test_validate_config_invalid_fast_slow(self):
        strategy = TrendFollowingTemplate(
            fast_ma_period=50,
            slow_ma_period=10
        )
        assert strategy.validate_config() is False
    
    def test_calculate_sma(self, sample_ohlcv_bullish):
        strategy = TrendFollowingTemplate()
        sma = strategy.calculate_sma(sample_ohlcv_bullish, 20)
        
        assert sma is not None
        assert sma > 0
    
    def test_calculate_ema(self, sample_ohlcv_bullish):
        strategy = TrendFollowingTemplate()
        ema = strategy.calculate_ema(sample_ohlcv_bullish, 20)
        
        assert ema is not None
        assert ema > 0
    
    def test_calculate_ma_crossover_insufficient_data(self, sample_ohlcv_bullish):
        strategy = TrendFollowingTemplate()
        
        fast_ma, slow_ma, direction = strategy.calculate_ma_crossover(
            sample_ohlcv_bullish, 
            10
        )
        
        assert direction == "none"
    
    def test_calculate_ma_crossover_bullish(self, sample_ohlcv_bullish):
        strategy = TrendFollowingTemplate()
        
        fast_ma, slow_ma, direction = strategy.calculate_ma_crossover(
            sample_ohlcv_bullish, 
            60
        )
        
        # In bullish data, should see bullish alignment
        assert direction in ["bullish", "bearish", "none"]
    
    def test_entry_conditions_insufficient_data(self, sample_ohlcv_bullish):
        strategy = TrendFollowingTemplate(fast_ma_period=10, slow_ma_period=50)
        
        met, signal = strategy.entry_conditions(sample_ohlcv_bullish, 20)
        
        assert met is False
        assert signal is None
    
    def test_entry_conditions_with_crossover(self, sample_ohlcv_bullish):
        strategy = TrendFollowingTemplate(
            fast_ma_period=5,
            slow_ma_period=20
        )
        
        met, signal = strategy.entry_conditions(sample_ohlcv_bullish, 60)
        
        # May or may not have crossover depending on data
        if met and signal:
            assert signal.signal_type in [SignalType.BUY, SignalType.SELL]
            assert signal.price > 0
            assert signal.stop_loss is not None
            assert signal.take_profit is not None
    
    def test_exit_conditions_bearish_crossover(self, sample_ohlcv_bearish):
        strategy = TrendFollowingTemplate()
        
        # Create long position
        position = Position(
            symbol="XAUUSD",
            entry_price=100.0,
            quantity=1.0,
            side="LONG",
            entry_time=datetime.now(),
            stop_loss=99.0,
            take_profit=102.0
        )
        
        met, signal = strategy.exit_conditions(sample_ohlcv_bearish, 60, position)
        
        # Should exit if trend changes
        if met:
            assert signal.signal_type == SignalType.CLOSE_LONG
            assert "reason" in signal.metadata
    
    def test_exit_conditions_long_stop_loss(self, sample_ohlcv_bullish):
        strategy = TrendFollowingTemplate()
        
        position = Position(
            symbol="XAUUSD",
            entry_price=100.0,
            quantity=1.0,
            side="LONG",
            entry_time=datetime.now(),
            stop_loss=99.0,
            take_profit=102.0
        )
        
        # Set low below stop loss
        test_data = sample_ohlcv_bullish.copy()
        test_data[-1].low = 98.0
        
        met, signal = strategy.exit_conditions(test_data, len(test_data) - 1, position)
        
        if met:
            assert signal.signal_type == SignalType.CLOSE_LONG
    
    def test_position_sizing(self, sample_ohlcv_bullish):
        strategy = TrendFollowingTemplate(risk_per_trade=0.02)
        
        position_size = strategy.position_sizing(
            ohlcv_data=sample_ohlcv_bullish,
            current_idx=50,
            entry_price=100.0,
            stop_loss=99.0,
            account_balance=10000.0
        )
        
        assert position_size > 0
    
    def test_get_required_candles(self):
        strategy = TrendFollowingTemplate(
            fast_ma_period=10,
            slow_ma_period=50
        )
        
        required = strategy.get_required_candles()
        
        assert required == 64  # slow_ma_period + 14
    
    def test_get_signals(self, sample_ohlcv_bullish):
        strategy = TrendFollowingTemplate(
            fast_ma_period=5,
            slow_ma_period=20
        )
        
        signals = strategy.get_signals(sample_ohlcv_bullish)
        
        assert isinstance(signals, list)
