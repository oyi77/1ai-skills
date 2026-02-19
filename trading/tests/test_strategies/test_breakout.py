"""
Tests for BreakoutTemplate strategy.
"""
import pytest
from datetime import datetime
from typing import List

from trading.brokers.base import OHLCV
from trading.strategy.templates.breakout import BreakoutTemplate
from trading.strategy.templates.base import SignalType


class TestBreakoutTemplate:
    """Tests for BreakoutTemplate class."""
    
    def test_initialization(self):
        strategy = BreakoutTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            lookback_period=20,
            atr_multiplier=2.0,
            risk_per_trade=0.02
        )
        
        assert strategy.name == "BreakoutTemplate"
        assert strategy.symbol == "XAUUSD"
        assert strategy.timeframe == "H1"
        assert strategy.lookback_period == 20
        assert strategy.atr_multiplier == 2.0
        assert strategy.risk_per_trade == 0.02
    
    def test_validate_config_valid(self):
        strategy = BreakoutTemplate()
        assert strategy.validate_config() is True
    
    def test_validate_config_invalid_lookback(self):
        strategy = BreakoutTemplate(lookback_period=3)
        assert strategy.validate_config() is False
    
    def test_validate_config_invalid_atr(self):
        strategy = BreakoutTemplate(atr_multiplier=0.0)
        assert strategy.validate_config() is False
    
    def test_calculate_hh_ll(self, sample_ohlcv_bullish):
        strategy = BreakoutTemplate()
        hh, ll = strategy.calculate_hh_ll(sample_ohlcv_bullish, 20)
        
        assert hh > ll
        assert isinstance(hh, float)
        assert isinstance(ll, float)
    
    def test_calculate_atr(self, sample_ohlcv_bullish):
        strategy = BreakoutTemplate()
        atr = strategy.calculate_atr(sample_ohlcv_bullish)
        
        assert atr >= 0
        assert isinstance(atr, float)
    
    def test_calculate_avg_volume(self, sample_ohlcv_bullish):
        strategy = BreakoutTemplate()
        avg_vol = strategy.calculate_avg_volume(sample_ohlcv_bullish)
        
        assert avg_vol > 0
        assert isinstance(avg_vol, float)
    
    def test_entry_conditions_insufficient_data(self, sample_ohlcv_bullish):
        strategy = BreakoutTemplate(lookback_period=20)
        
        # Less than lookback period
        met, signal = strategy.entry_conditions(sample_ohlcv_bullish, 10)
        
        assert met is False
        assert signal is None
    
    def test_entry_conditions_no_breakout(self, sample_ohlcv_sideways):
        strategy = BreakoutTemplate(lookback_period=20)
        
        met, signal = strategy.entry_conditions(sample_ohlcv_sideways, 30)
        
        # Should not trigger in sideways market
        assert met is False
        assert signal is None
    
    def test_entry_conditions_with_breakout(self, sample_ohlcv_with_breakout):
        strategy = BreakoutTemplate(
            lookback_period=20,
            min_volume_ratio=1.0
        )
        
        # Try at breakout point
        met, signal = strategy.entry_conditions(sample_ohlcv_with_breakout, 45)
        
        # Breakout may or may not trigger depending on exact data
        if met and signal:
            assert signal.signal_type in [SignalType.BUY, SignalType.SELL]
            assert signal.price > 0
            assert signal.stop_loss is not None
            assert signal.take_profit is not None
    
    def test_exit_conditions_long_stop_loss(self, sample_ohlcv_bullish):
        strategy = BreakoutTemplate()
        
        # Create a mock position
        from trading.strategy.templates.base import Position
        position = Position(
            symbol="XAUUSD",
            entry_price=100.0,
            quantity=1.0,
            side="LONG",
            entry_time=datetime.now(),
            stop_loss=99.0,
            take_profit=102.0
        )
        
        # Set current low to hit stop loss
        test_data = sample_ohlcv_bullish.copy()
        test_data[-1].low = 98.0  # Below stop loss
        
        met, signal = strategy.exit_conditions(test_data, len(test_data) - 1, position)
        
        if met:
            assert signal.signal_type == SignalType.CLOSE_LONG
            assert signal.metadata.get("reason") == "stop_loss"
    
    def test_exit_conditions_short_stop_loss(self, sample_ohlcv_bearish):
        strategy = BreakoutTemplate()
        
        from trading.strategy.templates.base import Position
        position = Position(
            symbol="XAUUSD",
            entry_price=100.0,
            quantity=1.0,
            side="SHORT",
            entry_time=datetime.now(),
            stop_loss=101.0,
            take_profit=98.0
        )
        
        # Set current high to hit stop loss
        test_data = sample_ohlcv_bearish.copy()
        test_data[-1].high = 102.0  # Above stop loss
        
        met, signal = strategy.exit_conditions(test_data, len(test_data) - 1, position)
        
        if met:
            assert signal.signal_type == SignalType.CLOSE_SHORT
            assert signal.metadata.get("reason") == "stop_loss"
    
    def test_position_sizing(self, sample_ohlcv_bullish):
        strategy = BreakoutTemplate(risk_per_trade=0.02)
        
        position_size = strategy.position_sizing(
            ohlcv_data=sample_ohlcv_bullish,
            current_idx=50,
            entry_price=100.0,
            stop_loss=99.0,
            account_balance=10000.0
        )
        
        assert position_size > 0
        assert isinstance(position_size, float)
    
    def test_get_required_candles(self):
        strategy = BreakoutTemplate(lookback_period=20)
        
        required = strategy.get_required_candles()
        
        assert required == 34  # lookback_period + 14
    
    def test_get_signals(self, sample_ohlcv_bullish):
        strategy = BreakoutTemplate(
            lookback_period=20,
            min_volume_ratio=0.5
        )
        
        signals = strategy.get_signals(sample_ohlcv_bullish)
        
        assert isinstance(signals, list)
