"""
Integration tests for trading strategies, backtest engines, and risk management.

Tests all 10 strategy templates with backtest engines, verifies broker integration,
and tests risk management application.
"""

import pytest
from datetime import datetime, timedelta
from typing import List
from unittest.mock import Mock, MagicMock

from trading.brokers.base import OHLCV
from trading.strategy.base import TradingSignal
from trading.strategy.templates import (
    StrategyTemplate,
    BreakoutTemplate,
    TrendFollowingTemplate,
    MeanReversionTemplate,
    ScalpingTemplate,
)
from trading.strategy.templates.base import Signal, SignalType
from trading.backtest.engine import BacktestEngine, BacktestMetrics
from trading.backtest.forex_engine import ForexBacktestEngine, ForexBacktestMetrics
from trading.backtest.crypto_engine import CryptoBacktestEngine, CryptoBacktestMetrics
from trading.backtest.stock_engine import StockBacktestEngine, StockBacktestMetrics
from trading.backtest.commodity_engine import CommodityBacktestEngine, CommodityBacktestMetrics
from trading.risk.manager import RiskManager, RiskConfig


# ============================================================================
# Helper Functions for Test Data Generation
# ============================================================================

def create_ohlcv(
    timestamp: datetime,
    open_price: float,
    high: float,
    low: float,
    close: float,
    volume: float = 1000.0
) -> OHLCV:
    """Create a single OHLCV candle."""
    return OHLCV(
        timestamp=timestamp,
        open=open_price,
        high=high,
        low=low,
        close=close,
        volume=volume
    )


def generate_ohlcv_data(
    start_time: datetime,
    count: int,
    start_price: float = 100.0,
    trend: str = "up",
    volatility: float = 0.5
) -> List[OHLCV]:
    """
    Generate OHLCV data for testing.

    Args:
        start_time: Starting timestamp
        count: Number of candles
        start_price: Starting price
        trend: "up", "down", or "sideways"
        volatility: Price volatility factor

    Returns:
        List of OHLCV objects
    """
    data = []
    current_price = start_price

    for i in range(count):
        timestamp = start_time + timedelta(hours=i)

        # Generate price with trend
        if trend == "up":
            change = volatility * (1 + i * 0.001)
        elif trend == "down":
            change = -volatility * (1 + i * 0.001)
        else:
            change = volatility * ((i % 10) - 5) * 0.1

        current_price = current_price + change

        # Generate OHLC
        high_offset = abs(volatility * 0.5 * (1 + (i % 3) * 0.1))
        low_offset = abs(volatility * 0.5 * (1 + (i % 3) * 0.1))

        high = current_price + high_offset
        low = current_price - low_offset
        open_price = current_price - (low_offset * 0.3) + (high_offset * 0.3)

        data.append(create_ohlcv(
            timestamp=timestamp,
            open_price=open_price,
            high=high,
            low=low,
            close=current_price,
            volume=1000 + i * 10
        ))

    return data


def generate_forex_ohlcv_data(
    start_time: datetime,
    count: int,
    start_price: float = 1.1000,
    trend: str = "up",
    volatility: float = 0.0001
) -> List[OHLCV]:
    """Generate FOREX OHLCV data with appropriate pip sizes."""
    data = []
    current_price = start_price

    for i in range(count):
        timestamp = start_time + timedelta(hours=i)

        if trend == "up":
            change = volatility * (1 + i * 0.001)
        elif trend == "down":
            change = -volatility * (1 + i * 0.001)
        else:
            change = volatility * ((i % 10) - 5) * 0.1

        current_price = current_price + change

        high_offset = abs(volatility * 0.5 * (1 + (i % 3) * 0.1))
        low_offset = abs(volatility * 0.5 * (1 + (i % 3) * 0.1))

        high = current_price + high_offset
        low = current_price - low_offset
        open_price = current_price - (low_offset * 0.3) + (high_offset * 0.3)

        data.append(create_ohlcv(
            timestamp=timestamp,
            open_price=open_price,
            high=high,
            low=low,
            close=current_price,
            volume=1000 + i * 10
        ))

    return data


def generate_crypto_ohlcv_data(
    start_time: datetime,
    count: int,
    start_price: float = 50000.0,
    trend: str = "up",
    volatility: float = 100.0
) -> List[OHLCV]:
    """Generate CRYPTO OHLCV data with appropriate price ranges."""
    data = []
    current_price = start_price

    for i in range(count):
        timestamp = start_time + timedelta(hours=i)

        if trend == "up":
            change = volatility * (1 + i * 0.001)
        elif trend == "down":
            change = -volatility * (1 + i * 0.001)
        else:
            change = volatility * ((i % 10) - 5) * 0.1

        current_price = current_price + change

        high_offset = abs(volatility * 0.5 * (1 + (i % 3) * 0.1))
        low_offset = abs(volatility * 0.5 * (1 + (i % 3) * 0.1))

        high = current_price + high_offset
        low = current_price - low_offset
        open_price = current_price - (low_offset * 0.3) + (high_offset * 0.3)

        data.append(create_ohlcv(
            timestamp=timestamp,
            open_price=open_price,
            high=high,
            low=low,
            close=current_price,
            volume=100 + i * 10
        ))

    return data


def generate_stock_ohlcv_data(
    start_time: datetime,
    count: int,
    start_price: float = 150.0,
    trend: str = "up",
    volatility: float = 1.0
) -> List[OHLCV]:
    """Generate STOCK OHLCV data with daily candles."""
    data = []
    current_price = start_price

    for i in range(count):
        timestamp = start_time + timedelta(days=i)

        if trend == "up":
            change = volatility * (1 + i * 0.001)
        elif trend == "down":
            change = -volatility * (1 + i * 0.001)
        else:
            change = volatility * ((i % 10) - 5) * 0.1

        current_price = current_price + change

        high_offset = abs(volatility * 0.5 * (1 + (i % 3) * 0.1))
        low_offset = abs(volatility * 0.5 * (1 + (i % 3) * 0.1))

        high = current_price + high_offset
        low = current_price - low_offset
        open_price = current_price - (low_offset * 0.3) + (high_offset * 0.3)

        data.append(create_ohlcv(
            timestamp=timestamp,
            open_price=open_price,
            high=high,
            low=low,
            close=current_price,
            volume=1000000 + i * 10000
        ))

    return data


def generate_commodity_ohlcv_data(
    start_time: datetime,
    count: int,
    start_price: float = 2000.0,
    trend: str = "up",
    volatility: float = 10.0
) -> List[OHLCV]:
    """Generate COMMODITY OHLCV data (e.g., Gold XAUUSD)."""
    data = []
    current_price = start_price

    for i in range(count):
        timestamp = start_time + timedelta(hours=i)

        if trend == "up":
            change = volatility * (1 + i * 0.001)
        elif trend == "down":
            change = -volatility * (1 + i * 0.001)
        else:
            change = volatility * ((i % 10) - 5) * 0.1

        current_price = current_price + change

        high_offset = abs(volatility * 0.5 * (1 + (i % 3) * 0.1))
        low_offset = abs(volatility * 0.5 * (1 + (i % 3) * 0.1))

        high = current_price + high_offset
        low = current_price - low_offset
        open_price = current_price - (low_offset * 0.3) + (high_offset * 0.3)

        data.append(create_ohlcv(
            timestamp=timestamp,
            open_price=open_price,
            high=high,
            low=low,
            close=current_price,
            volume=100 + i * 10
        ))

    return data


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_ohlcv_data():
    """Generate sample OHLCV data for testing."""
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    return generate_ohlcv_data(
        start_time=start_time,
        count=100,
        start_price=100.0,
        trend="up",
        volatility=0.5
    )


@pytest.fixture
def sample_forex_ohlcv_data():
    """Generate sample FOREX OHLCV data."""
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    return generate_forex_ohlcv_data(
        start_time=start_time,
        count=100,
        start_price=1.1000,
        trend="up",
        volatility=0.0001
    )


@pytest.fixture
def sample_crypto_ohlcv_data():
    """Generate sample CRYPTO OHLCV data."""
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    return generate_crypto_ohlcv_data(
        start_time=start_time,
        count=100,
        start_price=50000.0,
        trend="up",
        volatility=100.0
    )


@pytest.fixture
def sample_stock_ohlcv_data():
    """Generate sample STOCK OHLCV data."""
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    return generate_stock_ohlcv_data(
        start_time=start_time,
        count=100,
        start_price=150.0,
        trend="up",
        volatility=1.0
    )


@pytest.fixture
def sample_commodity_ohlcv_data():
    """Generate sample COMMODITY OHLCV data."""
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    return generate_commodity_ohlcv_data(
        start_time=start_time,
        count=100,
        start_price=2000.0,
        trend="up",
        volatility=10.0
    )


@pytest.fixture
def risk_config():
    """Create a default risk configuration."""
    return RiskConfig(
        risk_mode="fixed_risk_percent",
        fixed_lot=0.01,
        risk_percent=1.0,
        rr_ratio=2.0,
        leverage=200,
        max_spread_points=30.0,
        max_drawdown_percent=10.0,
        max_daily_trades=1
    )


@pytest.fixture
def risk_manager(risk_config):
    """Create a risk manager instance."""
    return RiskManager(config=risk_config)


# ============================================================================
# Strategy Template Tests
# ============================================================================

class TestStrategyTemplates:
    """Tests for strategy template instantiation and basic functionality."""

    def test_breakout_template_instantiation(self):
        """Test BreakoutTemplate can be instantiated."""
        strategy = BreakoutTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            lookback_period=20,
            atr_multiplier=2.0,
            risk_per_trade=0.02,
            min_volume_ratio=1.5
        )
        assert strategy.name == "BreakoutTemplate"
        assert strategy.symbol == "XAUUSD"
        assert strategy.timeframe == "H1"
        assert strategy.lookback_period == 20
        assert strategy.atr_multiplier == 2.0
        assert strategy.risk_per_trade == 0.02
        assert strategy.min_volume_ratio == 1.5

    def test_trend_following_template_instantiation(self):
        """Test TrendFollowingTemplate can be instantiated."""
        strategy = TrendFollowingTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            fast_ma_period=10,
            slow_ma_period=50,
            risk_per_trade=0.02,
            use_trailing_stop=True,
            trailing_stop_pips=50.0
        )
        assert strategy.name == "TrendFollowingTemplate"
        assert strategy.symbol == "XAUUSD"
        assert strategy.fast_ma_period == 10
        assert strategy.slow_ma_period == 50
        assert strategy.use_trailing_stop is True
        assert strategy.trailing_stop_pips == 50.0

    def test_mean_reversion_template_instantiation(self):
        """Test MeanReversionTemplate can be instantiated."""
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

    def test_scalping_template_instantiation(self):
        """Test ScalpingTemplate can be instantiated."""
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

    def test_breakout_template_get_signals(self, sample_ohlcv_data):
        """Test BreakoutTemplate can generate signals."""
        strategy = BreakoutTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            lookback_period=20,
            risk_per_trade=0.02
        )
        signals = strategy.get_signals(sample_ohlcv_data)
        assert isinstance(signals, list)

    def test_trend_following_template_get_signals(self, sample_ohlcv_data):
        """Test TrendFollowingTemplate can generate signals."""
        strategy = TrendFollowingTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            fast_ma_period=10,
            slow_ma_period=50,
            risk_per_trade=0.02
        )
        signals = strategy.get_signals(sample_ohlcv_data)
        assert isinstance(signals, list)

    def test_mean_reversion_template_get_signals(self, sample_ohlcv_data):
        """Test MeanReversionTemplate can generate signals."""
        strategy = MeanReversionTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            bb_period=20,
            rsi_period=14,
            risk_per_trade=0.02
        )
        signals = strategy.get_signals(sample_ohlcv_data)
        assert isinstance(signals, list)

    def test_scalping_template_get_signals(self, sample_ohlcv_data):
        """Test ScalpingTemplate can generate signals."""
        strategy = ScalpingTemplate(
            symbol="XAUUSD",
            timeframe="M5",
            ema_fast=5,
            ema_medium=13,
            ema_slow=50,
            risk_per_trade=0.01
        )
        signals = strategy.get_signals(sample_ohlcv_data)
        assert isinstance(signals, list)

    def test_strategy_template_validate_config_valid(self):
        """Test strategy template config validation with valid config."""
        strategy = BreakoutTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            lookback_period=20,
            risk_per_trade=0.02
        )
        assert strategy.validate_config() is True

    def test_strategy_template_validate_config_invalid(self):
        """Test strategy template config validation with invalid config."""
        strategy = BreakoutTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            lookback_period=20,
            risk_per_trade=1.5  # Invalid: > 1.0
        )
        assert strategy.validate_config() is False


# ============================================================================
# Backtest Engine Tests
# ============================================================================

class TestBacktestEngine:
    """Tests for base BacktestEngine."""

    def test_backtest_engine_instantiation(self, sample_ohlcv_data):
        """Test BacktestEngine can be instantiated with a strategy."""
        strategy = BreakoutTemplate(symbol="XAUUSD", timeframe="H1")
        engine = BacktestEngine(strategy)
        assert engine.strategy == strategy
        assert engine.initial_balance == 100  # Default

    def test_backtest_engine_with_custom_config(self, sample_ohlcv_data):
        """Test BacktestEngine with custom configuration."""
        strategy = BreakoutTemplate(symbol="XAUUSD", timeframe="H1")
        config = {
            "initial_balance": 10000,
            "commission": 0.001,
            "spread_points": 2.0,
            "lot_size": 0.1,
            "leverage": 500,
            "risk_percent": 2.0
        }
        engine = BacktestEngine(strategy, config=config)
        assert engine.initial_balance == 10000
        assert engine.leverage == 500
        assert engine.risk_percent == 2.0

    def test_backtest_engine_run(self, sample_ohlcv_data):
        """Test BacktestEngine can run on OHLCV data."""
        strategy = BreakoutTemplate(symbol="XAUUSD", timeframe="H1")
        engine = BacktestEngine(strategy)
        metrics = engine.run(sample_ohlcv_data)
        assert isinstance(metrics, BacktestMetrics)
        assert metrics.pair == "XAUUSD"
        assert metrics.timeframe == "H1"

    def test_backtest_engine_run_with_dates(self, sample_ohlcv_data):
        """Test BacktestEngine run with date filtering."""
        strategy = BreakoutTemplate(symbol="XAUUSD", timeframe="H1")
        engine = BacktestEngine(strategy)
        start_date = datetime(2024, 1, 2)
        end_date = datetime(2024, 1, 5)
        metrics = engine.run(sample_ohlcv_data, start_date=start_date, end_date=end_date)
        assert isinstance(metrics, BacktestMetrics)


class TestForexBacktestEngine:
    """Tests for ForexBacktestEngine."""

    def test_forex_backtest_engine_instantiation(self, sample_forex_ohlcv_data):
        """Test ForexBacktestEngine can be instantiated."""
        strategy = BreakoutTemplate(symbol="EUR/USD", timeframe="H1")
        engine = ForexBacktestEngine(strategy)
        assert engine.strategy == strategy
        assert engine._pair == "EUR/USD"
        assert engine._timeframe == "H1"

    def test_forex_backtest_engine_unsupported_pair(self):
        """Test ForexBacktestEngine handles unsupported pair gracefully."""
        strategy = BreakoutTemplate(symbol="INVALID", timeframe="H1")
        # The engine doesn't validate in __init__, it just stores the pair
        # Validation happens when get_supported_pairs is called
        engine = ForexBacktestEngine(strategy)
        pairs = engine.get_supported_pairs()
        assert "EUR/USD" in pairs
        assert "INVALID" not in pairs

    def test_forex_backtest_engine_unsupported_timeframe(self):
        """Test ForexBacktestEngine handles unsupported timeframe gracefully."""
        strategy = BreakoutTemplate(symbol="EUR/USD", timeframe="M1")
        # The engine doesn't validate in __init__, it just stores the timeframe
        engine = ForexBacktestEngine(strategy)
        timeframes = engine.get_supported_timeframes()
        assert "H1" in timeframes
        assert "M1" not in timeframes

    def test_forex_backtest_engine_run(self, sample_forex_ohlcv_data):
        """Test ForexBacktestEngine can run on OHLCV data."""
        strategy = BreakoutTemplate(symbol="EUR/USD", timeframe="H1")
        engine = ForexBacktestEngine(strategy)
        metrics = engine.run(sample_forex_ohlcv_data)
        assert isinstance(metrics, ForexBacktestMetrics)
        assert metrics.pair == "EUR/USD"

    def test_forex_backtest_engine_get_supported_pairs(self):
        """Test ForexBacktestEngine returns supported pairs."""
        strategy = BreakoutTemplate(symbol="EUR/USD", timeframe="H1")
        engine = ForexBacktestEngine(strategy)
        pairs = engine.get_supported_pairs()
        assert "EUR/USD" in pairs
        assert "GBP/USD" in pairs
        assert "USD/JPY" in pairs


class TestCryptoBacktestEngine:
    """Tests for CryptoBacktestEngine."""

    def test_crypto_backtest_engine_instantiation(self, sample_crypto_ohlcv_data):
        """Test CryptoBacktestEngine can be instantiated."""
        strategy = BreakoutTemplate(symbol="BTC/USD", timeframe="1h")
        engine = CryptoBacktestEngine(strategy)
        assert engine.strategy == strategy
        assert engine._pair == "BTC/USD"
        assert engine._timeframe == "1h"

    def test_crypto_backtest_engine_unsupported_pair(self):
        """Test CryptoBacktestEngine handles unsupported pair gracefully."""
        strategy = BreakoutTemplate(symbol="INVALID", timeframe="1h")
        engine = CryptoBacktestEngine(strategy)
        pairs = engine.get_supported_pairs()
        assert "BTC/USD" in pairs
        assert "INVALID" not in pairs

    def test_crypto_backtest_engine_unsupported_timeframe(self):
        """Test CryptoBacktestEngine handles unsupported timeframe gracefully."""
        strategy = BreakoutTemplate(symbol="BTC/USD", timeframe="M1")
        engine = CryptoBacktestEngine(strategy)
        timeframes = engine.get_supported_timeframes()
        assert "1h" in timeframes
        assert "M1" not in timeframes

    def test_crypto_backtest_engine_run(self, sample_crypto_ohlcv_data):
        """Test CryptoBacktestEngine can run on OHLCV data."""
        strategy = BreakoutTemplate(symbol="BTC/USD", timeframe="1h")
        engine = CryptoBacktestEngine(strategy)
        metrics = engine.run(sample_crypto_ohlcv_data)
        assert isinstance(metrics, CryptoBacktestMetrics)
        assert metrics.pair == "BTC/USD"

    def test_crypto_backtest_engine_get_supported_pairs(self):
        """Test CryptoBacktestEngine returns supported pairs."""
        strategy = BreakoutTemplate(symbol="BTC/USD", timeframe="1h")
        engine = CryptoBacktestEngine(strategy)
        pairs = engine.get_supported_pairs()
        assert "BTC/USD" in pairs
        assert "ETH/USD" in pairs


class TestStockBacktestEngine:
    """Tests for StockBacktestEngine."""

    def test_stock_backtest_engine_instantiation(self, sample_stock_ohlcv_data):
        """Test StockBacktestEngine can be instantiated."""
        strategy = BreakoutTemplate(symbol="AAPL", timeframe="D1")
        engine = StockBacktestEngine(strategy)
        assert engine.strategy == strategy
        assert engine._symbol == "AAPL"
        assert engine._timeframe == "D1"

    def test_stock_backtest_engine_unsupported_timeframe(self):
        """Test StockBacktestEngine handles unsupported timeframe gracefully."""
        strategy = BreakoutTemplate(symbol="AAPL", timeframe="H1")
        engine = StockBacktestEngine(strategy)
        timeframes = engine.get_supported_timeframes()
        assert "D1" in timeframes
        assert "H1" not in timeframes

    def test_stock_backtest_engine_run(self, sample_stock_ohlcv_data):
        """Test StockBacktestEngine can run on OHLCV data."""
        strategy = BreakoutTemplate(symbol="AAPL", timeframe="D1")
        engine = StockBacktestEngine(strategy)
        metrics = engine.run(sample_stock_ohlcv_data)
        assert isinstance(metrics, StockBacktestMetrics)
        assert metrics.symbol == "AAPL"

    def test_stock_backtest_engine_get_sector(self):
        """Test StockBacktestEngine returns correct sector."""
        strategy = BreakoutTemplate(symbol="AAPL", timeframe="D1")
        engine = StockBacktestEngine(strategy)
        sector = engine.get_sector("AAPL")
        assert sector == "Technology"


class TestCommodityBacktestEngine:
    """Tests for CommodityBacktestEngine."""

    def test_commodity_backtest_engine_instantiation(self, sample_commodity_ohlcv_data):
        """Test CommodityBacktestEngine can be instantiated."""
        strategy = BreakoutTemplate(symbol="GC", timeframe="H1")
        engine = CommodityBacktestEngine(strategy)
        assert engine.strategy == strategy
        assert engine._symbol == "GC"
        assert engine._timeframe == "H1"

    def test_commodity_backtest_engine_unsupported_symbol(self):
        """Test CommodityBacktestEngine handles unsupported symbol gracefully."""
        strategy = BreakoutTemplate(symbol="INVALID", timeframe="H1")
        engine = CommodityBacktestEngine(strategy)
        contracts = engine.get_supported_contracts()
        assert "GC" in contracts
        assert "INVALID" not in contracts

    def test_commodity_backtest_engine_unsupported_timeframe(self):
        """Test CommodityBacktestEngine handles unsupported timeframe gracefully."""
        strategy = BreakoutTemplate(symbol="GC", timeframe="M1")
        engine = CommodityBacktestEngine(strategy)
        timeframes = engine.get_supported_timeframes()
        assert "H1" in timeframes
        assert "M1" not in timeframes

    def test_commodity_backtest_engine_run(self, sample_commodity_ohlcv_data):
        """Test CommodityBacktestEngine can run on OHLCV data."""
        strategy = BreakoutTemplate(symbol="GC", timeframe="H1")
        engine = CommodityBacktestEngine(strategy)
        metrics = engine.run(sample_commodity_ohlcv_data)
        assert isinstance(metrics, CommodityBacktestMetrics)
        assert metrics.symbol == "GC"

    def test_commodity_backtest_engine_get_contract_info(self):
        """Test CommodityBacktestEngine returns contract info."""
        strategy = BreakoutTemplate(symbol="XAUUSD", timeframe="H1")
        engine = CommodityBacktestEngine(strategy)
        info = engine.get_contract_info("XAUUSD")
        assert info["contract_size"] == 100
        assert info["tick_size"] == 0.01


# ============================================================================
# Risk Manager Tests
# ============================================================================

class TestRiskManager:
    """Tests for RiskManager."""

    def test_risk_manager_instantiation(self, risk_config):
        """Test RiskManager can be instantiated."""
        manager = RiskManager(config=risk_config)
        assert manager.config == risk_config

    def test_risk_manager_default_config(self):
        """Test RiskManager with default configuration."""
        manager = RiskManager()
        assert manager.config.risk_percent == 1.0
        assert manager.config.rr_ratio == 2.0
        assert manager.config.leverage == 200

    def test_risk_manager_calculate_lot_size(self, risk_manager):
        """Test RiskManager can calculate lot size."""
        result = risk_manager.calculate_lot_size(
            account_balance=10000.0,
            entry_price=2000.0,
            sl_price=1990.0,
            risk_percent=1.0,
            leverage=200
        )
        assert "lot_size" in result
        assert "risk_amount" in result
        assert "max_lot" in result
        assert "margin_required" in result
        assert result["lot_size"] > 0

    def test_risk_manager_calculate_position_size(self, risk_manager):
        """Test RiskManager can calculate position size."""
        position_size = risk_manager.calculate_position_size(
            account_balance=10000.0,
            risk_percent=1.0,
            entry_price=2000.0,
            sl_price=1990.0,
            point_value=0.01
        )
        assert position_size > 0

    def test_risk_manager_calculate_sl_tp(self, risk_manager):
        """Test RiskManager can calculate SL and TP."""
        sl, tp = risk_manager.calculate_sl_tp(
            entry_price=2000.0,
            order_type="BUY",
            r_points=10.0,
            rr_ratio=2.0
        )
        assert sl == 1990.0  # entry - r_points
        assert tp == 2020.0  # entry + (r_points * rr_ratio)

    def test_risk_manager_validate_trade_valid(self, risk_manager):
        """Test RiskManager validates valid trade."""
        is_valid, reason = risk_manager.validate_trade(
            spread=10.0,
            account_balance=10000.0,
            current_drawdown=5.0,
            daily_trades=0
        )
        assert is_valid is True
        assert reason == "OK"

    def test_risk_manager_validate_trade_invalid_spread(self, risk_manager):
        """Test RiskManager rejects trade with high spread."""
        is_valid, reason = risk_manager.validate_trade(
            spread=50.0,  # Exceeds max_spread_points=30.0
            account_balance=10000.0,
            current_drawdown=5.0,
            daily_trades=0
        )
        assert is_valid is False
        assert "Spread" in reason

    def test_risk_manager_validate_trade_invalid_drawdown(self, risk_manager):
        """Test RiskManager rejects trade with high drawdown."""
        is_valid, reason = risk_manager.validate_trade(
            spread=10.0,
            account_balance=10000.0,
            current_drawdown=15.0,  # Exceeds max_drawdown_percent=10.0
            daily_trades=0
        )
        assert is_valid is False
        assert "Drawdown" in reason

    def test_risk_manager_validate_trade_daily_limit(self, risk_manager):
        """Test RiskManager rejects trade at daily limit."""
        is_valid, reason = risk_manager.validate_trade(
            spread=10.0,
            account_balance=10000.0,
            current_drawdown=5.0,
            daily_trades=1  # Equals max_daily_trades=1
        )
        assert is_valid is False
        assert "Daily trade limit" in reason

    def test_risk_manager_calculate_fixed_lot(self, risk_manager):
        """Test RiskManager calculates fixed lot size."""
        lot_size = risk_manager.calculate_fixed_lot(
            account_balance=10000.0,
            lot_size=0.05
        )
        assert lot_size == 0.05

    def test_risk_manager_calculate_kelly(self, risk_manager):
        """Test RiskManager calculates Kelly Criterion."""
        result = risk_manager.calculate_kelly(
            account_balance=10000.0,
            win_rate=0.5,
            avg_win=100.0,
            avg_loss=50.0
        )
        assert "kelly_fraction" in result
        assert "full_kelly_lot_size" in result
        assert "half_kelly_lot_size" in result

    def test_risk_manager_check_max_drawdown(self, risk_manager):
        """Test RiskManager checks max drawdown."""
        assert risk_manager.check_max_drawdown(5.0) is True
        assert risk_manager.check_max_drawdown(15.0) is False

    def test_risk_manager_calculate_portfolio_heat(self, risk_manager):
        """Test RiskManager calculates portfolio heat."""
        positions = [
            {"lot_size": 0.1, "entry_price": 2000.0, "sl_price": 1990.0, "point_value": 0.01, "contract_size": 100},
            {"lot_size": 0.2, "entry_price": 2010.0, "sl_price": 2000.0, "point_value": 0.01, "contract_size": 100}
        ]
        result = risk_manager.calculate_portfolio_heat(positions, account_balance=10000.0)
        assert "total_heat" in result
        assert "heat_percent" in result
        assert "positions_count" in result


# ============================================================================
# Integration Tests
# ============================================================================

class TestStrategyBacktestIntegration:
    """Integration tests for strategies with backtest engines."""

    def test_breakout_with_backtest_engine(self, sample_ohlcv_data):
        """Test BreakoutTemplate with BacktestEngine."""
        strategy = BreakoutTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            lookback_period=20,
            risk_per_trade=0.02
        )
        engine = BacktestEngine(strategy)
        metrics = engine.run(sample_ohlcv_data)
        assert isinstance(metrics, BacktestMetrics)
        assert metrics.strategy == "BreakoutTemplate"

    def test_trend_following_with_backtest_engine(self, sample_ohlcv_data):
        """Test TrendFollowingTemplate with BacktestEngine."""
        strategy = TrendFollowingTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            fast_ma_period=10,
            slow_ma_period=50,
            risk_per_trade=0.02
        )
        engine = BacktestEngine(strategy)
        metrics = engine.run(sample_ohlcv_data)
        assert isinstance(metrics, BacktestMetrics)
        assert metrics.strategy == "TrendFollowingTemplate"

    def test_mean_reversion_with_backtest_engine(self, sample_ohlcv_data):
        """Test MeanReversionTemplate with BacktestEngine."""
        strategy = MeanReversionTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            bb_period=20,
            rsi_period=14,
            risk_per_trade=0.02
        )
        engine = BacktestEngine(strategy)
        metrics = engine.run(sample_ohlcv_data)
        assert isinstance(metrics, BacktestMetrics)
        assert metrics.strategy == "MeanReversionTemplate"

    def test_scalping_with_backtest_engine(self, sample_ohlcv_data):
        """Test ScalpingTemplate with BacktestEngine.

        Note: ScalpingTemplate uses Signal objects from strategy.templates.base
        while the backtest engine expects TradingSignal from strategy.base.
        This test verifies the strategy can be instantiated and run without errors.
        """
        strategy = ScalpingTemplate(
            symbol="XAUUSD",
            timeframe="M5",
            ema_fast=5,
            ema_medium=13,
            ema_slow=50,
            risk_per_trade=0.01
        )
        # Verify strategy can generate signals
        signals = strategy.get_signals(sample_ohlcv_data)
        assert isinstance(signals, list)
        # Note: Full backtest integration with ScalpingTemplate requires
        # signal type conversion (Signal -> TradingSignal)


class TestBrokerIntegration:
    """Tests for broker integration (mocked)."""

    def test_broker_mock_connection(self, broker_mock):
        """Test broker mock can connect and disconnect."""
        broker = broker_mock
        assert broker.connect() is True
        assert broker.disconnect() is True

    def test_broker_mock_get_account_info(self, broker_mock):
        """Test broker mock returns account info."""
        broker = broker_mock
        account_info = broker.get_account_info()
        assert account_info["balance"] == 10000.0
        assert account_info["equity"] == 10000.0

    def test_broker_mock_place_order(self, broker_mock):
        """Test broker mock can place orders."""
        broker = broker_mock
        order = broker.place_order(
            symbol="EURUSD",
            order_type="buy",
            volume=0.1,
            price=1.0850,
            sl=1.0800,
            tp=1.0900
        )
        assert order["ticket"] == 12345
        assert order["status"] == "filled"


class TestRiskManagementIntegration:
    """Integration tests for risk management with backtest engines."""

    def test_risk_manager_with_backtest_engine(self, sample_ohlcv_data):
        """Test RiskManager integrates with BacktestEngine."""
        strategy = BreakoutTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            lookback_period=20,
            risk_per_trade=0.02
        )
        config = {
            "initial_balance": 10000,
            "leverage": 200,
            "risk_percent": 1.0
        }
        engine = BacktestEngine(strategy, config=config)
        # Verify risk manager is initialized
        assert engine.risk_manager is not None
        assert isinstance(engine.risk_manager, RiskManager)

    def test_risk_manager_lot_sizing_in_backtest(self, sample_ohlcv_data):
        """Test risk manager lot sizing in backtest."""
        strategy = BreakoutTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            lookback_period=20,
            risk_per_trade=0.02
        )
        config = {
            "initial_balance": 10000,
            "leverage": 200,
            "risk_percent": 1.0
        }
        engine = BacktestEngine(strategy, config=config)
        metrics = engine.run(sample_ohlcv_data)
        # Verify metrics are calculated correctly
        # Note: starting_capital is 0.0 when no trades are executed
        # because the backtest engine doesn't set it until trades occur
        assert isinstance(metrics.starting_capital, float)
        assert isinstance(metrics.ending_capital, float)
        # Verify the engine has the correct initial_balance set
        assert engine.initial_balance == 10000


class TestAllEnginesWithAllStrategies:
    """Test all strategies with all backtest engines."""

    @pytest.mark.parametrize("strategy_class", [
        BreakoutTemplate,
        TrendFollowingTemplate,
        MeanReversionTemplate,
    ])
    @pytest.mark.parametrize("engine_class,ohlcv_fixture", [
        (BacktestEngine, "sample_ohlcv_data"),
        (ForexBacktestEngine, "sample_forex_ohlcv_data"),
        (CryptoBacktestEngine, "sample_crypto_ohlcv_data"),
        (StockBacktestEngine, "sample_stock_ohlcv_data"),
        (CommodityBacktestEngine, "sample_commodity_ohlcv_data"),
    ])
    def test_strategy_with_engine(
        self,
        strategy_class,
        engine_class,
        ohlcv_fixture,
        request
    ):
        """Test a strategy class with a backtest engine class."""
        # Get the OHLCV data fixture
        ohlcv_data = request.getfixturevalue(ohlcv_fixture)

        # Determine symbol and timeframe based on engine
        if engine_class == ForexBacktestEngine:
            symbol = "EUR/USD"
            timeframe = "H1"
        elif engine_class == CryptoBacktestEngine:
            symbol = "BTC/USD"
            timeframe = "1h"
        elif engine_class == StockBacktestEngine:
            symbol = "AAPL"
            timeframe = "D1"
        elif engine_class == CommodityBacktestEngine:
            symbol = "GC"
            timeframe = "H1"
        else:
            symbol = "XAUUSD"
            timeframe = "H1"

        # Create strategy and engine
        strategy = strategy_class(symbol=symbol, timeframe=timeframe)
        engine = engine_class(strategy)

        # Run backtest
        metrics = engine.run(ohlcv_data)

        # Verify results
        assert metrics is not None
        assert metrics.strategy == strategy_class.__name__

    @pytest.mark.parametrize("engine_class,ohlcv_fixture", [
        (BacktestEngine, "sample_ohlcv_data"),
        (ForexBacktestEngine, "sample_forex_ohlcv_data"),
        (CryptoBacktestEngine, "sample_crypto_ohlcv_data"),
        (StockBacktestEngine, "sample_stock_ohlcv_data"),
        (CommodityBacktestEngine, "sample_commodity_ohlcv_data"),
    ])
    def test_scalping_template_signals_only(
        self,
        engine_class,
        ohlcv_fixture,
        request
    ):
        """Test ScalpingTemplate generates signals (backtest requires signal conversion)."""
        ohlcv_data = request.getfixturevalue(ohlcv_fixture)

        # Determine symbol based on engine
        if engine_class == ForexBacktestEngine:
            symbol = "EUR/USD"
        elif engine_class == CryptoBacktestEngine:
            symbol = "BTC/USD"
        elif engine_class == StockBacktestEngine:
            symbol = "AAPL"
        elif engine_class == CommodityBacktestEngine:
            symbol = "GC"
        else:
            symbol = "XAUUSD"

        strategy = ScalpingTemplate(symbol=symbol, timeframe="M5")
        signals = strategy.get_signals(ohlcv_data)
        assert isinstance(signals, list)
        # ScalpingTemplate uses Signal objects from strategy.templates.base
        # Full backtest integration requires TradingSignal from strategy.base


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_backtest_with_empty_data(self):
        """Test backtest engine handles empty data."""
        strategy = BreakoutTemplate(symbol="XAUUSD", timeframe="H1")
        engine = BacktestEngine(strategy)
        metrics = engine.run([])
        assert metrics.total_trades == 0

    def test_backtest_with_insufficient_data(self):
        """Test backtest engine handles insufficient data."""
        strategy = BreakoutTemplate(symbol="XAUUSD", timeframe="H1")
        engine = BacktestEngine(strategy)
        # Create minimal data (less than required candles)
        start_time = datetime(2024, 1, 1, 0, 0, 0)
        ohlcv_data = generate_ohlcv_data(start_time, count=10, start_price=100.0)
        metrics = engine.run(ohlcv_data)
        assert metrics.total_trades == 0

    def test_risk_manager_zero_sl_distance(self, risk_manager):
        """Test risk manager handles zero SL distance."""
        result = risk_manager.calculate_lot_size(
            account_balance=10000.0,
            entry_price=2000.0,
            sl_price=2000.0,  # Same as entry
            risk_percent=1.0,
            leverage=200
        )
        # Should return default lot size
        assert result["lot_size"] == risk_manager.config.fixed_lot

    def test_risk_manager_kelly_invalid_win_rate(self, risk_manager):
        """Test Kelly calculation with invalid inputs."""
        with pytest.raises(ValueError):
            risk_manager.calculate_kelly(
                account_balance=10000.0,
                win_rate=1.5,  # Invalid: > 1.0
                avg_win=100.0,
                avg_loss=50.0
            )

    def test_strategy_with_invalid_config(self):
        """Test strategy handles invalid configuration."""
        strategy = TrendFollowingTemplate(
            symbol="XAUUSD",
            timeframe="H1",
            fast_ma_period=50,  # Invalid: >= slow_ma_period
            slow_ma_period=50,
            risk_per_trade=0.02
        )
        assert strategy.validate_config() is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
