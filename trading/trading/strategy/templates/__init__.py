"""
Trading Strategy Templates

Modular strategy templates with configurable hooks for entry, exit, and position sizing.
"""

from trading.strategy.templates.base import StrategyTemplate
from trading.strategy.templates.breakout import BreakoutTemplate
from trading.strategy.templates.trend_following import TrendFollowingTemplate
from trading.strategy.templates.mean_reversion import MeanReversionTemplate
from trading.strategy.templates.scalping import ScalpingTemplate

__all__ = [
    "StrategyTemplate",
    "BreakoutTemplate",
    "TrendFollowingTemplate",
    "MeanReversionTemplate",
    "ScalpingTemplate",
]
