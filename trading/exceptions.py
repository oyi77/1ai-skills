"""
Custom exception classes for the trading system.

This module defines all custom exceptions used throughout the trading platform
for proper error handling and categorization.
"""

from typing import Optional


class TradingError(Exception):
    """Base exception for all trading-related errors."""
    pass


class BrokerConnectionError(TradingError):
    """Raised when connection to a broker fails or times out.
    
    Attributes:
        broker_name (str): Name of the broker that failed to connect
        message (str): Detailed error message
    """
    def __init__(self, broker_name: str, message: str = "Failed to connect to broker"):
        self.broker_name = broker_name
        self.message = message
        super().__init__(f"{message}: {broker_name}")


class IndicatorCalculationError(TradingError):
    """Raised when technical indicator calculation fails.
    
    Attributes:
        indicator_name (str): Name of the indicator that failed
        symbol (str): Trading symbol being processed
        message (str): Detailed error message
    """
    def __init__(self, indicator_name: str, symbol: str = "", message: str = "Indicator calculation failed"):
        self.indicator_name = indicator_name
        self.symbol = symbol
        self.message = message
        error_msg = f"{message}: {indicator_name}"
        if symbol:
            error_msg += f" for {symbol}"
        super().__init__(error_msg)


class StrategyValidationError(TradingError):
    """Raised when a trading strategy validation fails.
    
    Attributes:
        strategy_name (str): Name of the invalid strategy
        validation_errors (list): List of specific validation errors
        message (str): Detailed error message
    """
    def __init__(self, strategy_name: str, validation_errors: Optional[list] = None, message: str = "Strategy validation failed"):
        self.strategy_name = strategy_name
        self.validation_errors = validation_errors or []
        self.message = message
        error_msg = f"{message}: {strategy_name}"
        if self.validation_errors:
            error_msg += f" - Errors: {'; '.join(self.validation_errors)}"
        super().__init__(error_msg)


class RiskManagerError(TradingError):
    """Raised when risk management rules are violated or calculations fail.
    
    Attributes:
        rule_name (str): Name of the risk rule that triggered the error
        details (dict): Additional details about the risk violation
        message (str): Detailed error message
    """
    def __init__(self, rule_name: str, details: Optional[dict] = None, message: str = "Risk management error"):
        self.rule_name = rule_name
        self.details = details or {}
        self.message = message
        error_msg = f"{message}: {rule_name}"
        if self.details:
            error_msg += f" - Details: {self.details}"
        super().__init__(error_msg)
