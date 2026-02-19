"""
Tests for StrategyTemplate base class.
"""
import pytest
from datetime import datetime
from typing import List

from trading.brokers.base import OHLCV
from trading.strategy.templates.base import (
    StrategyTemplate, 
    Signal, 
    SignalType,
    Position
)


class ConcreteStrategyTemplate(StrategyTemplate):
    """Concrete implementation for testing."""
    
    def __init__(self, **kwargs):
        super().__init__(name="TestStrategy", **kwargs)
        self.entry_called = False
        self.exit_called = False
    
    def entry_conditions(
        self, 
        ohlcv_data: List[OHLCV], 
        current_idx: int
    ):
        self.entry_called = True
        return False, None
    
    def exit_conditions(
        self, 
        ohlcv_data: List[OHLCV], 
        current_idx: int,
        position: Position
    ):
        self.exit_called = True
        return False, None
    
    def position_sizing(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int,
        entry_price: float,
        stop_loss: float,
        account_balance: float
    ) -> float:
        return 1.0


class TestSignalType:
    """Tests for SignalType enum."""
    
    def test_signal_type_values(self):
        assert SignalType.BUY.value == "BUY"
        assert SignalType.SELL.value == "SELL"
        assert SignalType.NEUTRAL.value == "NEUTRAL"
        assert SignalType.CLOSE_LONG.value == "CLOSE_LONG"
        assert SignalType.CLOSE_SHORT.value == "CLOSE_SHORT"


class TestSignal:
    """Tests for Signal dataclass."""
    
    def test_signal_creation(self):
        signal = Signal(
            timestamp=datetime.now(),
            symbol="XAUUSD",
            timeframe="H1",
            signal_type=SignalType.BUY,
            price=100.0,
            stop_loss=99.0,
            take_profit=102.0,
            confidence=0.8
        )
        
        assert signal.symbol == "XAUUSD"
        assert signal.signal_type == SignalType.BUY
        assert signal.price == 100.0
        assert signal.confidence == 0.8
    
    def test_signal_to_dict(self):
        signal = Signal(
            timestamp=datetime(2024, 1, 1, 0, 0, 0),
            symbol="XAUUSD",
            timeframe="H1",
            signal_type=SignalType.BUY,
            price=100.0,
            stop_loss=99.0,
            take_profit=102.0,
            confidence=0.8
        )
        
        signal_dict = signal.to_dict()
        
        assert signal_dict["symbol"] == "XAUUSD"
        assert signal_dict["signal_type"] == "BUY"
        assert signal_dict["price"] == 100.0
        assert signal_dict["confidence"] == 0.8


class TestStrategyTemplate:
    """Tests for StrategyTemplate base class."""
    
    def test_strategy_initialization(self):
        strategy = ConcreteStrategyTemplate(
            symbol="EURUSD",
            timeframe="M15",
            risk_per_trade=0.03
        )
        
        assert strategy.name == "TestStrategy"
        assert strategy.symbol == "EURUSD"
        assert strategy.timeframe == "M15"
        assert strategy.risk_per_trade == 0.03
    
    def test_validate_config_valid(self):
        strategy = ConcreteStrategyTemplate(risk_per_trade=0.02)
        assert strategy.validate_config() is True
    
    def test_validate_config_invalid(self):
        strategy = ConcreteStrategyTemplate(risk_per_trade=0.0)
        assert strategy.validate_config() is False
    
    def test_validate_config_invalid_high_risk(self):
        strategy = ConcreteStrategyTemplate(risk_per_trade=1.5)
        assert strategy.validate_config() is False
    
    def test_calculate_pip_value_xauusd(self):
        strategy = ConcreteStrategyTemplate()
        pip_value = strategy.calculate_pip_value("XAUUSD")
        assert pip_value == 0.01
    
    def test_calculate_pip_value_eurusd(self):
        strategy = ConcreteStrategyTemplate()
        pip_value = strategy.calculate_pip_value("EURUSD")
        assert pip_value == 0.0001
    
    def test_calculate_pip_value_unknown(self):
        strategy = ConcreteStrategyTemplate()
        pip_value = strategy.calculate_pip_value("UNKNOWN")
        assert pip_value == 0.0001  # Default
    
    def test_calculate_stop_loss_pips_long(self):
        strategy = ConcreteStrategyTemplate()
        pips = strategy.calculate_stop_loss_pips(
            entry_price=100.0,
            stop_loss=99.0,
            is_long=True
        )
        assert pips == 100.0  # 1.0 / 0.01 = 100 pips for XAUUSD
    
    def test_calculate_position_size_from_risk(self):
        strategy = ConcreteStrategyTemplate(risk_per_trade=0.02)
        
        position_size = strategy.calculate_position_size_from_risk(
            account_balance=10000.0,
            stop_loss_pips=100.0
        )
        
        # Risk = 10000 * 0.02 = 200
        # Position size = 200 / (100 * 0.01) = 200 lots
        assert position_size == 200.0
    
    def test_get_required_candles(self):
        strategy = ConcreteStrategyTemplate()
        assert strategy.get_required_candles() == 50
    
    def test_get_signals(self, sample_ohlcv_bullish):
        strategy = ConcreteStrategyTemplate()
        signals = strategy.get_signals(sample_ohlcv_bullish)
        
        assert strategy.entry_called is True
        assert isinstance(signals, list)
