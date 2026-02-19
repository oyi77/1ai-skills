"""
Symbol Configuration Module

Defines symbol configurations for trading instruments.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SymbolConfig:
    """Configuration for a trading symbol."""

    symbol: str
    yahoo_ticker: str
    point_value: float
    pip_digits: int
    contract_size: float
    description: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "symbol": self.symbol,
            "yahoo_ticker": self.yahoo_ticker,
            "point_value": self.point_value,
            "pip_digits": self.pip_digits,
            "contract_size": self.contract_size,
            "description": self.description,
        }


# Forex symbol configurations
FOREX_SYMBOLS = {
    "EURUSD": SymbolConfig(
        symbol="EURUSD",
        yahoo_ticker="EURUSD=X",
        point_value=0.0001,
        pip_digits=4,
        contract_size=100000,
        description="Euro / US Dollar",
    ),
    "GBPUSD": SymbolConfig(
        symbol="GBPUSD",
        yahoo_ticker="GBPUSD=X",
        point_value=0.0001,
        pip_digits=4,
        contract_size=100000,
        description="British Pound / US Dollar",
    ),
    "USDJPY": SymbolConfig(
        symbol="USDJPY",
        yahoo_ticker="JPY=X",
        point_value=0.01,
        pip_digits=2,
        contract_size=100000,
        description="US Dollar / Japanese Yen",
    ),
}

# Commodity symbol configurations
COMMODITY_SYMBOLS = {
    "XAUUSD": SymbolConfig(
        symbol="XAUUSD",
        yahoo_ticker="GC=F",
        point_value=0.01,
        pip_digits=2,
        contract_size=100,
        description="Gold / US Dollar",
    ),
    "XAUUSD.D": SymbolConfig(
        symbol="XAUUSD.D",
        yahoo_ticker="GC=F",
        point_value=0.01,
        pip_digits=2,
        contract_size=100,
        description="Gold / US Dollar (Daily)",
    ),
}

# Combined symbol registry
SYMBOL_REGISTRY = {**FOREX_SYMBOLS, **COMMODITY_SYMBOLS}


def get_symbol_config(symbol: str) -> Optional[SymbolConfig]:
    """
    Get configuration for a symbol.

    Args:
        symbol: Trading symbol (e.g., "EURUSD")

    Returns:
        SymbolConfig if found, None otherwise
    """
    return SYMBOL_REGISTRY.get(symbol)


def get_yahoo_ticker(symbol: str) -> str:
    """
    Get Yahoo Finance ticker for a symbol.

    Args:
        symbol: Trading symbol (e.g., "EURUSD")

    Returns:
        Yahoo Finance ticker string, or the symbol itself if not found
    """
    config = get_symbol_config(symbol)
    if config:
        return config.yahoo_ticker
    return symbol


def list_available_symbols() -> list[str]:
    """
    List all available symbols.

    Returns:
        List of symbol strings
    """
    return list(SYMBOL_REGISTRY.keys())


def add_symbol_config(config: SymbolConfig) -> None:
    """
    Add a new symbol configuration to the registry.

    Args:
        config: SymbolConfig to add
    """
    SYMBOL_REGISTRY[config.symbol] = config
