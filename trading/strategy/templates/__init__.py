"""
Trading Strategy Templates

Modular strategy templates with configurable hooks for entry, exit, and position sizing.
"""

from .base import StrategyTemplate
from .breakout import BreakoutTemplate
from .trend_following import TrendFollowingTemplate
from .mean_reversion import MeanReversionTemplate
from .scalping import ScalpingTemplate

__all__ = [
    "StrategyTemplate",
    "BreakoutTemplate",
    "TrendFollowingTemplate",
    "MeanReversionTemplate",
    "ScalpingTemplate",
]
