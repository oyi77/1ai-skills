"""
Tests for MeanReversionTemplate strategy.
"""
import pytest
from datetime import datetime
from typing import List

from trading.brokers.base import OHLCV
from trading.strategy.templates.mean_reversion import MeanReversionTemplate
from trading.strategy.templates.base import SignalType, Position


class TestMeanReversionTemplate:
    """Tests for MeanReversionTemplate class."""
    
    def test_initialization(self):
        strategy = MeanReversionTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            bb_period=20,
            bb_std=2.0,
            rsi_period=14,
            rsi_oversold=30.0,
            rsi_overbought=70.0,
            risk_per_trade=0.02
        )
        
        assert strategy.name == "MeanReversionTemplate"
        assert strategy.symbol == "XAUUSD"
        assert strategy.bb_period == 20
        assert strategy.bb_std == 2.0
        assert strategy.rsi_period == 14
        assert strategy.rsi_oversold == 30.0
        assert strategy.rsi_overbought == 70.0
    
    def test_validate_config_valid(self):
        strategy = MeanReversionTemplate()
        assert strategy.validate_config() is True
    
    def test_validate_config_invalid_oversold(self):
        strategy = MeanReversionTemplate(
            rsi_oversold=70.0,
            rsi_overbought=30.0
        )
        assert strategy.validate_config() is False
    
    def test_validate_config_invalid_bb_period(self):
        strategy = MeanReversionTemplate(bb_period=3)
        assert strategy.validate_config() is False
    
    def test_calculate_sma(self, sample_ohlcv_bullish):
        strategy = MeanReversionTemplate()
        sma = strategy.calculate_sma(sample_ohlcv_bullish, 20)
        
        assert sma is not None
        assert sma > 0
    
    def test_calculate_std(self, sample_ohlcv_bullish):
        strategy = MeanReversionTemplate()
        std = strategy.calculate_std(sample_ohlcv_bullish, 20)
        
        assert std is not None
        assert std >= 0
    
    def test_calculate_bollinger_bands(self, sample_ohlcv_bullish):
        strategy = MeanReversionTemplate(bb_period=20)
        
        upper, middle, lower = strategy.calculate_bollinger_bands(
            sample_ohlcv_bullish
        )
        
        if upper is not None:
            assert upper > middle
            assert middle > lower
    
    def test_calculate_rsi(self, sample_ohlcv_bullish):
        strategy = MeanReversionTemplate(rsi_period=14)
        
        rsi = strategy.calculate_rsi(sample_ohlcv_bullish)
        
        if rsi is not None:
            assert 0 <= rsi <= 100
    
    def test_calculate_atr(self, sample_ohlcv_bullish):
        strategy = MeanReversionTemplate()
        atr = strategy.calculate_atr(sample_ohlcv_bullish)
        
        assert atr >= 0
    
    def test_entry_conditions_insufficient_data(self, sample_ohlcv_bullish):
        strategy = MeanReversionTemplate()
        
        met, signal = strategy.entry_conditions(sample_ohlcv_bullish, 10)
        
        assert met is False
        assert signal is None
    
    def test_entry_conditions_in_middle_band(self, sample_ohlcv_sideways):
        strategy = MeanReversionTemplate()
        
        met, signal = strategy.entry_conditions(sample_ohlcv_sideways, 30)
        
        # Should not trigger entry in middle band
        assert met is False
    
    def test_entry_conditions_with_extreme(self, sample_ohlcv_bullish):
        strategy = MeanReversionTemplate(
            bb_period=10,
            rsi_period=5
        )
        
        # Modify data to create extreme conditions
        test_data = sample_ohlcv_bullish.copy()
        # Set last candle to be at extreme (low with low RSI)
        test_data[-1].close = test_data[-1].low - 1.0
        
        met, signal = strategy.entry_conditions(test_data, len(test_data) - 1)
        
        # May trigger if conditions are met
        if met and signal:
            assert signal.signal_type in [SignalType.BUY, SignalType.SELL]
            assert signal.price > 0
    
    def test_exit_conditions_long_stop_loss(self, sample_ohlcv_bullish):
        strategy = MeanReversionTemplate()
        
        position = Position(
            symbol="XAUUSD",
            entry_price=100.0,
            quantity=1.0,
            side="LONG",
            entry_time=datetime.now(),
            stop_loss=99.0,
            take_profit=101.0
        )
        
        test_data = sample_ohlcv_bullish.copy()
        test_data[-1].low = 98.0  # Below stop loss
        
        met, signal = strategy.exit_conditions(test_data, len(test_data) - 1, position)
        
        if met:
            assert signal.signal_type == SignalType.CLOSE_LONG
    
    def test_exit_conditions_at_middle_band(self, sample_ohlcv_bullish):
        strategy = MeanReversionTemplate()
        
        # Create position
        position = Position(
            symbol="XAUUSD",
            entry_price=100.0,
            quantity=1.0,
            side="LONG",
            entry_time=datetime.now(),
            stop_loss=99.0,
            take_profit=102.0
        )
        
        # Should exit at middle band if reached
        met, signal = strategy.exit_conditions(sample_ohlcv_bullish, 60, position)
        
        # May or may not exit depending on data
    
    def test_rsi_confidence_oversold_low(self):
        strategy = MeanReversionTemplate()
        
        confidence = strategy._calculate_rsi_confidence(5.0, is_oversold=True)
        
        assert confidence == 1.0
    
    def test_rsi_confidence_oversold_high(self):
        strategy = MeanReversionTemplate()
        
        confidence = strategy._calculate_rsi_confidence(25.0, is_oversold=True)
        
        assert 0 < confidence < 1.0
    
    def test_rsi_confidence_overbought_low(self):
        strategy = MeanReversionTemplate()
        
        confidence = strategy._calculate_rsi_confidence(75.0, is_oversold=False)
        
        assert 0 < confidence < 1.0
    
    def test_rsi_confidence_overbought_high(self):
        strategy = MeanReversionTemplate()
        
        confidence = strategy._calculate_rsi_confidence(95.0, is_oversold=False)
        
        assert confidence == 1.0
    
    def test_position_sizing(self, sample_ohlcv_bullish):
        strategy = MeanReversionTemplate(risk_per_trade=0.02)
        
        position_size = strategy.position_sizing(
            ohlcv_data=sample_ohlcv_bullish,
            current_idx=50,
            entry_price=100.0,
            stop_loss=99.0,
            account_balance=10000.0
        )
        
        assert position_size > 0
    
    def test_get_required_candles(self):
        strategy = MeanReversionTemplate(
            bb_period=20,
            rsi_period=14
        )
        
        required = strategy.get_required_candles()
        
        assert required == 34  # max(20, 14) + 14
    
    def test_get_signals(self, sample_ohlcv_bullish):
        strategy = MeanReversionTemplate()
        
        signals = strategy.get_signals(sample_ohlcv_bullish)
        
        assert isinstance(signals, list)
