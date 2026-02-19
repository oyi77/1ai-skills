"""
Indicator Base Class

Abstract base class for all technical indicators.
"""

from abc import ABC, abstractmethod
from typing import List, Any, Optional, Dict
import logging

from ..brokers.base import OHLCV

logger = logging.getLogger(__name__)


class Indicator(ABC):
    """Abstract base class for technical indicators."""

    def __init__(self, **kwargs):
        """
        Initialize indicator with configuration parameters.

        Args:
            **kwargs: Configuration parameters (e.g., period=14, multiplier=2.0)
        """
        self.config = kwargs or {}
        self._name = self.__class__.__name__
        self.logger = logging.getLogger(f"indicator.{self._name}")

    @property
    def name(self) -> str:
        """Get indicator name."""
        return self._name

    @abstractmethod
    def calculate(self, data: List[OHLCV]) -> Any:
        """
        Calculate indicator values from OHLCV data.

        Args:
            data: List of OHLCV candlestick data

        Returns:
            Indicator calculation result (type varies by indicator)
        """
        pass

    def validate_input(self, data: List[OHLCV]) -> bool:
        """
        Validate input data before calculation.

        Args:
            data: List of OHLCV candlestick data

        Returns:
            True if data is valid, raises ValueError otherwise

        Raises:
            ValueError: If data is invalid (empty, wrong type, insufficient length)
        """
        if not data:
            raise ValueError(f"{self.name}: Input data is empty")

        if not isinstance(data, list):
            raise ValueError(f"{self.name}: Input data must be a list, got {type(data)}")

        if len(data) == 0:
            raise ValueError(f"{self.name}: Input data has no elements")

        if not all(isinstance(candle, OHLCV) for candle in data):
            raise ValueError(f"{self.name}: All elements must be OHLCV objects")

        return True

    def get_required_period(self) -> int:
        """
        Get minimum number of candles required for calculation.

        Returns:
            Minimum number of candles needed
        """
        return 1

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get configuration parameter.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)

    def __repr__(self) -> str:
        """String representation of indicator."""
        config_str = ", ".join(f"{k}={v}" for k, v in self.config.items())
        return f"{self.name}({config_str})"
