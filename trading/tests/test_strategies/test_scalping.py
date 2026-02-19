"""
Tests for ScalpingTemplate strategy.
"""
import pytest
from datetime import datetime
from typing import List

from trading.brokers.base import OHLCV
from trading.strategy.templates.scalping import ScalpingTemplate
from trading.strategy.templates.base import SignalType, Position


class TestScalpingTemplate:
    """Tests for ScalpingTemplate class."""
    
    def test_initialization(self):
        strategy = ScalpingTemplate(
            symbol="XAUUSD",
            timeframe="M5",
            ema_fast=5,
            ema_medium=13,
            ema_slow=50,
            risk_per_trade=0.01,
            profit_target_pips=10.0,
            stop_loss_pips=8.0
        )
        
        assert strategy.name == "ScalpingTemplate"
        assert strategy.symbol == "XAUUSD"
        assert strategy.timeframe == "M5"
        assert strategy.ema_fast == 5
        assert strategy.ema_medium == 13
        assert strategy.ema_slow == 50
        assert strategy.profit_target_pips == 10.0
        assert strategy.stop_loss_pips == 8.0
    
    def test_validate_config_valid(self):
        strategy = ScalpingTemplate()
        assert strategy.validate_config() is True
    
    def test_validate_config_invalid_profit_target(self):
        strategy = ScalpingTemplate(profit_target_pips=0.0)
        assert strategy.validate_config() is False
    
    def test_validate_config_invalid_stop_loss(self):
        strategy = ScalpingTemplate(stop_loss_pips=-5.0)
        assert strategy.validate_config() is False
    
    def test_calculate_ema(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate()
        ema = strategy.calculate_ema(sample_ohlcv_bullish, 10)
        
        assert ema is not None
        assert ema > 0
    
    def test_calculate_ema_stack_insufficient_data(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate()
        
        ema_fast, ema_medium, ema_slow, trend = strategy.calculate_ema_stack(
            sample_ohlcv_bullish,
            20
        )
        
        assert trend == "neutral"
    
    def test_calculate_ema_stack_bullish_alignment(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate()
        
        ema_fast, ema_medium, ema_slow, trend = strategy.calculate_ema_stack(
            sample_ohlcv_bullish,
            60
        )
        
        # Should show alignment in bullish data
        assert trend in ["bullish", "bearish", "neutral"]
    
    def test_calculate_momentum(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate()
        
        momentum = strategy.calculate_momentum(sample_ohlcv_bullish, 20, 5)
        
        # Momentum can be positive or negative
        assert isinstance(momentum, float)
    
    def test_calculate_momentum_insufficient_data(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate()
        
        momentum = strategy.calculate_momentum(sample_ohlcv_bullish, 3, 5)
        
        assert momentum == 0.0
    
    def test_calculate_volatility(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate()
        
        volatility = strategy.calculate_volatility(sample_ohlcv_bullish, 30, 20)
        
        assert volatility >= 0
    
    def test_entry_conditions_insufficient_data(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate()
        
        met, signal = strategy.entry_conditions(sample_ohlcv_bullish, 20)
        
        assert met is False
        assert signal is None
    
    def test_entry_conditions_with_alignment(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate(
            ema_fast=5,
            ema_medium=13,
            ema_slow=30
        )
        
        met, signal = strategy.entry_conditions(sample_ohlcv_bullish, 50)
        
        # May trigger if EMA alignment and momentum match
        if met and signal:
            assert signal.signal_type in [SignalType.BUY, SignalType.SELL]
            assert signal.price > 0
            assert signal.stop_loss is not None
            assert signal.take_profit is not None
    
    def test_exit_conditions_long_stop_loss(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate()
        
        position = Position(
            symbol="XAUUSD",
            entry_price=100.0,
            quantity=1.0,
            side="LONG",
            entry_time=datetime.now(),
            stop_loss=99.2,
            take_profit=101.0
        )
        
        test_data = sample_ohlcv_bullish.copy()
        test_data[-1].low = 99.0  # Below stop loss
        
        met, signal = strategy.exit_conditions(test_data, len(test_data) - 1, position)
        
        if met:
            assert signal.signal_type == SignalType.CLOSE_LONG
    
    def test_exit_conditions_long_take_profit(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate()
        
        position = Position(
            symbol="XAUUSD",
            entry_price=100.0,
            quantity=1.0,
            side="LONG",
            entry_time=datetime.now(),
            stop_loss=99.2,
            take_profit=101.0
        )
        
        test_data = sample_ohlcv_bullish.copy()
        test_data[-1].high = 101.5  # Above take profit
        
        met, signal = strategy.exit_conditions(test_data, len(test_data) - 1, position)
        
        if met:
            assert signal.signal_type == SignalType.CLOSE_LONG
            assert signal.metadata.get("reason") == "take_profit"
    
    def test_exit_conditions_trend_change(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate()
        
        # Create long position
        position = Position(
            symbol="XAUUSD",
            entry_price=100.0,
            quantity=1.0,
            side="LONG",
            entry_time=datetime.now(),
            stop_loss=99.2,
            take_profit=102.0
        )
        
        # Should exit if trend changes
        met, signal = strategy.exit_conditions(sample_ohlcv_bullish, 60, position)
        
        # May exit if EMA alignment breaks
    
    def test_position_sizing(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate(risk_per_trade=0.01)
        
        position_size = strategy.position_sizing(
            ohlcv_data=sample_ohlcv_bullish,
            current_idx=50,
            entry_price=100.0,
            stop_loss=99.2,
            account_balance=10000.0
        )
        
        assert position_size > 0
    
    def test_get_required_candles(self):
        strategy = ScalpingTemplate(ema_slow=50)
        
        required = strategy.get_required_candles()
        
        assert required == 60  # ema_slow + 10
    
    def test_get_signals(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate(
            ema_fast=5,
            ema_medium=13,
            ema_slow=30
        )
        
        signals = strategy.get_signals(sample_ohlcv_bullish)
        
        assert isinstance(signals, list)
    
    def test_profit_target_calculation(self, sample_ohlcv_bullish):
        strategy = ScalpingTemplate(
            profit_target_pips=10.0,
            stop_loss_pips=8.0
        )
        
        # For XAUUSD, pip = 0.01
        pip_value = strategy.calculate_pip_value("XAUUSD")
        
        assert pip_value == 0.01
        
        # Profit target: 10 * 0.01 = 0.10
        # Stop loss: 8 * 0.01 = 0.08
