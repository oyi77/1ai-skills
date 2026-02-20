"""
Strategy Registry

Centralized registry for trading strategies with market type filtering.
Supports dynamic strategy registration and factory pattern for strategy creation.

Market Types:
- FOREX: Currency pairs (EUR/USD, GBP/USD, etc.)
- CRYPTO: Cryptocurrency pairs (BTC/USD, ETH/USD, etc.)
- STOCKS: Equity instruments (AAPL, MSFT, etc.)
- COMMODITIES: Physical goods (XAUUSD, XAGUSD, etc.)

Strategies (Waves 2-5):
- FOREX: holy_grail, momentum_elder, kumo_breakout
- CRYPTO: funding_reversal, volume_momentum
- STOCKS: golden_cross, rsi_divergence
- COMMODITIES: gold_silver_ratio, seasonal
"""

from enum import Enum
from typing import Dict, List, Optional, Type, Callable, Any
import logging

logger = logging.getLogger(__name__)


class MarketType(Enum):
    """Supported market types for strategy filtering."""
    FOREX = "FOREX"
    CRYPTO = "CRYPTO"
    STOCKS = "STOCKS"
    COMMODITIES = "COMMODITIES"


class StrategyRegistry:
    """
    Central registry for trading strategies.

    Provides:
    - Strategy registration and discovery
    - Market type filtering
    - Factory pattern for strategy creation
    - Dynamic strategy registration

    Usage:
        registry = StrategyRegistry()
        registry.register("my_strategy", MyStrategy, MarketType.FOREX)
        strategy = registry.get("my_strategy")(symbol="EUR/USD")
        forex_strategies = registry.get_by_market_type(MarketType.FOREX)
    """

    def __init__(self):
        self._strategies: Dict[str, Dict[str, Any]] = {}
        self._market_type_index: Dict[MarketType, List[str]] = {
            MarketType.FOREX: [],
            MarketType.CRYPTO: [],
            MarketType.STOCKS: [],
            MarketType.COMMODITIES: [],
        }

    def register(
        self,
        name: str,
        strategy_class: Type,
        market_type: MarketType,
        description: str = "",
        **kwargs
    ) -> None:
        """
        Register a strategy in the registry.

        Args:
            name: Unique strategy identifier
            strategy_class: Strategy class (must be callable)
            market_type: Market type for filtering
            description: Optional strategy description
            **kwargs: Additional metadata for the strategy

        Raises:
            ValueError: If strategy name already exists or invalid arguments
        """
        if name in self._strategies:
            logger.warning(f"Strategy '{name}' already registered. Overwriting.")
        if not callable(strategy_class):
            raise ValueError(f"Strategy class must be callable: {strategy_class}")
        if not isinstance(market_type, MarketType):
            raise ValueError(f"Invalid market type: {market_type}")

        self._strategies[name] = {
            "class": strategy_class,
            "market_type": market_type,
            "description": description,
            "kwargs": kwargs,
        }

        # Update market type index
        if name not in self._market_type_index[market_type]:
            self._market_type_index[market_type].append(name)

        logger.info(f"Registered strategy: {name} ({market_type.value})")

    def get(self, name: str) -> Optional[Type]:
        """
        Retrieve a strategy class by name.

        Args:
            name: Strategy name to retrieve

        Returns:
            Strategy class or None if not found
        """
        if name not in self._strategies:
            logger.warning(f"Strategy not found: {name}")
            return None
        return self._strategies[name]["class"]

    def get_by_market_type(self, market_type: MarketType) -> List[Dict[str, Any]]:
        """
        Get all strategies for a specific market type.

        Args:
            market_type: Market type to filter by

        Returns:
            List of strategy info dictionaries with keys:
            - name: Strategy name
            - class: Strategy class
            - description: Strategy description
            - kwargs: Additional metadata
        """
        if not isinstance(market_type, MarketType):
            logger.warning(f"Invalid market type: {market_type}")
            return []

        strategy_names = self._market_type_index.get(market_type, [])
        return [
            {
                "name": name,
                "class": self._strategies[name]["class"],
                "description": self._strategies[name]["description"],
                "kwargs": self._strategies[name]["kwargs"],
            }
            for name in strategy_names
        ]

    def list_strategies(self) -> List[Dict[str, Any]]:
        """
        List all registered strategies.

        Returns:
            List of strategy info dictionaries
        """
        return [
            {
                "name": name,
                "class": info["class"],
                "market_type": info["market_type"],
                "description": info["description"],
                "kwargs": info["kwargs"],
            }
            for name, info in self._strategies.items()
        ]

    def list_strategy_names(self) -> List[str]:
        """
        List all registered strategy names.

        Returns:
            List of strategy names
        """
        return list(self._strategies.keys())

    def create(self, name: str, **kwargs) -> Optional[Any]:
        """
        Factory method to create a strategy instance.

        Args:
            name: Strategy name to create
            **kwargs: Arguments to pass to strategy constructor

        Returns:
            Strategy instance or None if not found
        """
        strategy_class = self.get(name)
        if strategy_class is None:
            return None
        return strategy_class(**kwargs)

    def get_market_type(self, name: str) -> Optional[MarketType]:
        """
        Get the market type for a strategy.

        Args:
            name: Strategy name

        Returns:
            MarketType or None if not found
        """
        if name not in self._strategies:
            return None
        return self._strategies[name]["market_type"]

    def count(self) -> int:
        """
        Get total number of registered strategies.

        Returns:
            Number of strategies
        """
        return len(self._strategies)

    def count_by_market_type(self, market_type: MarketType) -> int:
        """
        Get number of strategies for a market type.

        Args:
            market_type: Market type to count

        Returns:
            Number of strategies for the market type
        """
        return len(self._market_type_index.get(market_type, []))


# Global registry instance
registry = StrategyRegistry()

# =============================================================================
# Register Strategies from Waves 2-5
# =============================================================================

def _register_all_strategies():
    """Register all strategies from Waves 2-5."""

    # FOREX Strategies (Wave 2)
    from trading.strategy.templates.forex.holy_grail import HolyGrailStrategy
    from trading.strategy.templates.forex.momentum_elder import MomentumElderStrategy
    from trading.strategy.templates.forex.kumo_breakout import KumoBreakoutStrategy

    registry.register(
        name="holy_grail",
        strategy_class=HolyGrailStrategy,
        market_type=MarketType.FOREX,
        description="EMA(20) + ADX(14) + RSI(14) trend-following strategy for major FOREX pairs"
    )

    registry.register(
        name="momentum_elder",
        strategy_class=MomentumElderStrategy,
        market_type=MarketType.FOREX,
        description="Dr. Elder's triple screen system combining momentum and trend filters"
    )

    registry.register(
        name="kumo_breakout",
        strategy_class=KumoBreakoutStrategy,
        market_type=MarketType.FOREX,
        description="Ichimoku Kumo breakout strategy for FOREX markets"
    )

    # CRYPTO Strategies (Wave 3)
    from trading.strategy.templates.crypto.funding_reversal import FundingReversalStrategy
    from trading.strategy.templates.crypto.volume_momentum import VolumeMomentumStrategy

    registry.register(
        name="funding_reversal",
        strategy_class=FundingReversalStrategy,
        market_type=MarketType.CRYPTO,
        description="Funding rate reversal strategy for cryptocurrency markets"
    )

    registry.register(
        name="volume_momentum",
        strategy_class=VolumeMomentumStrategy,
        market_type=MarketType.CRYPTO,
        description="Volume-weighted momentum strategy for crypto assets"
    )

    # STOCKS Strategies (Wave 4)
    from trading.strategy.templates.stocks.golden_cross import GoldenCrossStrategy
    from trading.strategy.templates.stocks.rsi_divergence import RSIDivergenceStrategy

    registry.register(
        name="golden_cross",
        strategy_class=GoldenCrossStrategy,
        market_type=MarketType.STOCKS,
        description="Classic 50/200 SMA crossover strategy for equities"
    )

    registry.register(
        name="rsi_divergence",
        strategy_class=RSIDivergenceStrategy,
        market_type=MarketType.STOCKS,
        description="RSI divergence detection for stock trading"
    )

    # COMMODITIES Strategies (Wave 5)
    from trading.strategy.templates.commodities.gold_silver_ratio import GoldSilverRatioStrategy
    from trading.strategy.templates.commodities.seasonal import SeasonalStrategy

    registry.register(
        name="gold_silver_ratio",
        strategy_class=GoldSilverRatioStrategy,
        market_type=MarketType.COMMODITIES,
        description="Gold/Silver ratio spread trading strategy"
    )

    registry.register(
        name="seasonal",
        strategy_class=SeasonalStrategy,
        market_type=MarketType.COMMODITIES,
        description="Seasonal pattern strategy for commodities"
    )


# Initialize registry with all strategies
_register_all_strategies()
