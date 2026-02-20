"""
COMMODITY Backtest Engine

COMMODITY-specific backtesting with futures contracts, contango-adjusted returns,
seasonality-adjusted performance, and MT5 broker integration.
Extends the base BacktestEngine for COMMODITY-specific requirements.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import numpy as np

from .engine import BacktestEngine, BacktestMetrics, TradeResult
from ..brokers.base import OHLCV
from ..strategy.base import TradingSignal


# Commodity futures contract specifications
# Format: {symbol: {tick_size, contract_size, point_value, exchange, currency}}
COMMODITY_CONTRACTS = {
    # Precious Metals
    "XAUUSD": {
        "tick_size": 0.01,
        "contract_size": 100,  # troy ounces
        "point_value": 1.0,  # $1 per point per ounce
        "exchange": "FX",
        "currency": "USD",
        "tick_value": 1.0,  # $1 per tick
        "trading_hours": "23:00-22:00",
        "settlement": "cash",
    },
    "XAGUSD": {
        "tick_size": 0.005,
        "contract_size": 5000,  # troy ounces
        "point_value": 0.1,  # $0.10 per point per ounce
        "exchange": "FX",
        "currency": "USD",
        "tick_value": 0.5,  # $0.50 per tick
        "trading_hours": "23:00-22:00",
        "settlement": "cash",
    },
    # Energy
    "CL": {  # Crude Oil WTI
        "tick_size": 0.01,
        "contract_size": 1000,  # barrels
        "point_value": 10.0,  # $10 per point per barrel
        "exchange": "NYMEX",
        "currency": "USD",
        "tick_value": 10.0,  # $10 per tick
        "trading_hours": "18:00-17:00",
        "settlement": "physical",
    },
    "NG": {  # Natural Gas
        "tick_size": 0.001,
        "contract_size": 10000,  # mmBtu
        "point_value": 10.0,  # $10 per point per mmBtu
        "exchange": "NYMEX",
        "currency": "USD",
        "tick_value": 10.0,  # $10 per tick
        "trading_hours": "18:00-17:00",
        "settlement": "physical",
    },
    "RB": {  # RBOB Gasoline
        "tick_size": 0.0001,
        "contract_size": 42000,  # gallons
        "point_value": 4.2,  # $4.20 per point per gallon
        "exchange": "NYMEX",
        "currency": "USD",
        "tick_value": 4.2,  # $4.20 per tick
        "trading_hours": "18:00-17:00",
        "settlement": "physical",
    },
    "HO": {  # Heating Oil
        "tick_size": 0.0001,
        "contract_size": 42000,  # gallons
        "point_value": 4.2,  # $4.20 per point per gallon
        "exchange": "NYMEX",
        "currency": "USD",
        "tick_value": 4.2,  # $4.20 per tick
        "trading_hours": "18:00-17:00",
        "settlement": "physical",
    },
    # Agricultural
    "ZC": {  # Corn
        "tick_size": 0.0025,
        "contract_size": 5000,  # bushels
        "point_value": 12.5,  # $12.50 per point per bushel
        "exchange": "CBOT",
        "currency": "USD",
        "tick_value": 12.5,  # $12.50 per tick
        "trading_hours": "20:00-14:45",
        "settlement": "physical",
    },
    "ZS": {  # Soybeans
        "tick_size": 0.0025,
        "contract_size": 5000,  # bushels
        "point_value": 12.5,  # $12.50 per point per bushel
        "exchange": "CBOT",
        "currency": "USD",
        "tick_value": 12.5,  # $12.50 per tick
        "trading_hours": "20:00-14:45",
        "settlement": "physical",
    },
    "ZW": {  # Wheat
        "tick_size": 0.0025,
        "contract_size": 5000,  # bushels
        "point_value": 12.5,  # $12.50 per point per bushel
        "exchange": "CBOT",
        "currency": "USD",
        "tick_value": 12.5,  # $12.50 per tick
        "trading_hours": "20:00-14:45",
        "settlement": "physical",
    },
    "KC": {  # Coffee
        "tick_size": 0.0005,
        "contract_size": 37500,  # pounds
        "point_value": 18.75,  # $18.75 per point per pound
        "exchange": "ICE",
        "currency": "USD",
        "tick_value": 18.75,  # $18.75 per tick
        "trading_hours": "03:15-14:30",
        "settlement": "physical",
    },
    "SB": {  # Sugar
        "tick_size": 0.0001,
        "contract_size": 112000,  # pounds
        "point_value": 11.2,  # $11.20 per point per pound
        "exchange": "ICE",
        "currency": "USD",
        "tick_value": 11.2,  # $11.20 per tick
        "trading_hours": "03:45-14:00",
        "settlement": "physical",
    },
    "CC": {  # Cocoa
        "tick_size": 1.0,
        "contract_size": 10,  # metric tons
        "point_value": 10.0,  # $10 per point per ton
        "exchange": "ICE",
        "currency": "USD",
        "tick_value": 10.0,  # $10 per tick
        "trading_hours": "04:45-14:30",
        "settlement": "physical",
    },
    "CT": {  # Cotton
        "tick_size": 0.0001,
        "contract_size": 50000,  # pounds
        "point_value": 5.0,  # $5 per point per pound
        "exchange": "ICE",
        "currency": "USD",
        "tick_value": 5.0,  # $5 per tick
        "trading_hours": "21:00-14:30",
        "settlement": "physical",
    },
    # Softs
    "OJ": {  # Orange Juice
        "tick_size": 0.0005,
        "contract_size": 15000,  # pounds
        "point_value": 7.5,  # $7.50 per point per pound
        "exchange": "ICE",
        "currency": "USD",
        "tick_value": 7.5,  # $7.50 per tick
        "trading_hours": "21:00-14:30",
        "settlement": "physical",
    },
    # Indices
    "ES": {  # E-mini S&P 500
        "tick_size": 0.25,
        "contract_size": 50,  # $50 per index point
        "point_value": 12.5,  # $12.50 per point
        "exchange": "CME",
        "currency": "USD",
        "tick_value": 12.5,  # $12.50 per tick
        "trading_hours": "18:00-17:00",
        "settlement": "cash",
    },
    "NQ": {  # E-mini Nasdaq 100
        "tick_size": 0.25,
        "contract_size": 20,  # $20 per index point
        "point_value": 5.0,  # $5 per point
        "exchange": "CME",
        "currency": "USD",
        "tick_value": 5.0,  # $5 per tick
        "trading_hours": "18:00-17:00",
        "settlement": "cash",
    },
    "YM": {  # E-mini Dow
        "tick_size": 1.0,
        "contract_size": 5,  # $5 per index point
        "point_value": 5.0,  # $5 per point
        "exchange": "CME",
        "currency": "USD",
        "tick_value": 5.0,  # $5 per tick
        "trading_hours": "18:00-17:00",
        "settlement": "cash",
    },
    # Metals
    "GC": {  # Gold
        "tick_size": 0.10,
        "contract_size": 100,  # troy ounces
        "point_value": 10.0,  # $10 per point per ounce
        "exchange": "COMEX",
        "currency": "USD",
        "tick_value": 10.0,  # $10 per tick
        "trading_hours": "18:00-17:00",
        "settlement": "physical",
    },
    "SI": {  # Silver
        "tick_size": 0.005,
        "contract_size": 5000,  # troy ounces
        "point_value": 25.0,  # $25 per point per ounce
        "exchange": "COMEX",
        "currency": "USD",
        "tick_value": 25.0,  # $25 per tick
        "trading_hours": "18:00-17:00",
        "settlement": "physical",
    },
    "HG": {  # Copper
        "tick_size": 0.0005,
        "contract_size": 25000,  # pounds
        "point_value": 12.5,  # $12.50 per point per pound
        "exchange": "COMEX",
        "currency": "USD",
        "tick_value": 12.5,  # $12.50 per tick
        "trading_hours": "18:00-17:00",
        "settlement": "physical",
    },
    "PL": {  # Platinum
        "tick_size": 0.10,
        "contract_size": 50,  # troy ounces
        "point_value": 5.0,  # $5 per point per ounce
        "exchange": "NYMEX",
        "currency": "USD",
        "tick_value": 5.0,  # $5 per tick
        "trading_hours": "18:00-17:00",
        "settlement": "physical",
    },
    "PA": {  # Palladium
        "tick_size": 0.005,
        "contract_size": 100,  # troy ounces
        "point_value": 5.0,  # $5 per point per ounce
        "exchange": "NYMEX",
        "currency": "USD",
        "tick_value": 5.0,  # $5 per tick
        "trading_hours": "18:00-17:00",
        "settlement": "physical",
    },
}

# Supported timeframes for commodities
COMMODITY_TIMEFRAMES = ["H1", "H4", "D1", "W1", "MN1"]

# Typical contract months for futures (F=G, H=J, K=M, N=Q, U=S, V=X, Z=Z)
FUTURES_MONTH_CODES = {
    "F": "January",
    "G": "February",
    "H": "March",
    "J": "April",
    "K": "May",
    "M": "June",
    "N": "July",
    "Q": "August",
    "U": "September",
    "V": "October",
    "X": "November",
    "Z": "December",
}

# Seasonality patterns for commodities
# Format: {symbol: {month: multiplier}} - higher multiplier = better performance
COMMODITY_SEASONALITY = {
    "CL": {  # Crude Oil
        1: 0.9, 2: 0.85, 3: 0.95, 4: 1.0, 5: 1.05, 6: 1.1,
        7: 1.05, 8: 1.0, 9: 0.95, 10: 0.9, 11: 0.85, 12: 0.9,
    },
    "NG": {  # Natural Gas
        1: 1.3, 2: 1.2, 3: 1.0, 4: 0.85, 5: 0.8, 6: 0.75,
        7: 0.7, 8: 0.75, 9: 0.9, 10: 1.1, 11: 1.25, 12: 1.35,
    },
    "ZC": {  # Corn
        1: 0.9, 2: 0.85, 3: 0.8, 4: 0.75, 5: 0.7, 6: 0.65,
        7: 0.6, 8: 0.65, 9: 0.75, 10: 0.9, 11: 1.0, 12: 1.05,
    },
    "ZS": {  # Soybeans
        1: 0.95, 2: 0.9, 3: 0.85, 4: 0.8, 5: 0.75, 6: 0.7,
        7: 0.65, 8: 0.7, 9: 0.8, 10: 0.95, 11: 1.05, 12: 1.1,
    },
    "ZW": {  # Wheat
        1: 1.0, 2: 0.95, 3: 0.9, 4: 0.85, 5: 0.8, 6: 0.75,
        7: 0.7, 8: 0.75, 9: 0.85, 10: 0.95, 11: 1.05, 12: 1.1,
    },
    "KC": {  # Coffee
        1: 0.95, 2: 1.0, 3: 1.05, 4: 1.1, 5: 1.05, 6: 1.0,
        7: 0.95, 8: 0.9, 9: 0.85, 10: 0.8, 11: 0.85, 12: 0.9,
    },
    "SB": {  # Sugar
        1: 0.9, 2: 0.85, 3: 0.8, 4: 0.75, 5: 0.7, 6: 0.65,
        7: 0.7, 8: 0.75, 9: 0.85, 10: 0.95, 11: 1.05, 12: 1.1,
    },
    "GC": {  # Gold
        1: 1.05, 2: 1.0, 3: 0.95, 4: 0.9, 5: 0.85, 6: 0.8,
        7: 0.85, 8: 0.9, 9: 0.95, 10: 1.0, 11: 1.05, 12: 1.1,
    },
    "SI": {  # Silver
        1: 1.05, 2: 1.0, 3: 0.95, 4: 0.9, 5: 0.85, 6: 0.8,
        7: 0.85, 8: 0.9, 9: 0.95, 10: 1.0, 11: 1.05, 12: 1.1,
    },
}

# Typical contango/backwardation spreads (as percentage of price)
# Positive = contango (futures > spot), Negative = backwardation (futures < spot)
TYPICAL_CONTANGO_SPREADS = {
    "CL": 0.02,  # ~2% contango for oil
    "NG": 0.05,  # ~5% contango for natural gas
    "GC": 0.01,  # ~1% contango for gold
    "SI": 0.015,  # ~1.5% contango for silver
    "ZC": 0.02,  # ~2% contango for corn
    "ZS": 0.02,  # ~2% contango for soybeans
    "ZW": 0.02,  # ~2% contango for wheat
}


@dataclass
class CommodityTradeResult:
    """Extended trade result with COMMODITY-specific metrics."""

    # Base fields from TradeResult
    entry_time: datetime
    exit_time: datetime
    symbol: str
    side: str  # BUY or SELL
    entry_price: float
    exit_price: float
    volume: float  # Number of contracts
    sl: float
    tp: float
    result: str  # WIN, LOSS, BREAKEVEN
    pnl_points: float
    pnl_money: float
    r_multiple: float
    reason: str

    # COMMODITY-specific fields
    contract_month: str = ""  # Futures contract month (e.g., "H25" for March 2025)
    contract_expiry: Optional[datetime] = None  # Contract expiration date
    roll_date: Optional[datetime] = None  # Date when contract was rolled
    roll_yield: float = 0.0  # PnL from rolling contracts (contango/backwardation)
    contango_adjustment: float = 0.0  # Contango-adjusted return
    seasonality_adjustment: float = 0.0  # Seasonality-adjusted return
    usd_exposure: float = 0.0  # Total USD exposure of the trade
    commission: float = 0.0  # Commission in USD
    holding_days: int = 0  # Number of days held

    def to_dict(self) -> Dict[str, Any]:
        base = {
            "entry_time": self.entry_time.isoformat(),
            "exit_time": self.exit_time.isoformat(),
            "symbol": self.symbol,
            "side": self.side,
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "volume": self.volume,
            "sl": self.sl,
            "tp": self.tp,
            "result": self.result,
            "pnl_points": self.pnl_points,
            "pnl_money": self.pnl_money,
            "r_multiple": self.r_multiple,
            "reason": self.reason,
            "contract_month": self.contract_month,
            "contract_expiry": self.contract_expiry.isoformat() if self.contract_expiry else None,
            "roll_date": self.roll_date.isoformat() if self.roll_date else None,
            "roll_yield": self.roll_yield,
            "contango_adjustment": self.contango_adjustment,
            "seasonality_adjustment": self.seasonality_adjustment,
            "usd_exposure": self.usd_exposure,
            "commission": self.commission,
            "holding_days": self.holding_days,
        }
        return base


@dataclass
class CommodityBacktestMetrics:
    """Extended metrics with COMMODITY-specific calculations."""

    # Base metrics
    symbol: str = ""
    contract: str = ""
    timeframe: str = ""
    strategy: str = ""
    start_date: str = ""
    end_date: str = ""
    leverage: int = 100
    risk_percent: float = 1.0
    avg_contracts: float = 0.0
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    total_pnl_points: float = 0.0
    total_pnl_money: float = 0.0
    avg_r: float = 0.0
    profit_factor: float = 0.0
    max_drawdown_points: float = 0.0
    max_drawdown_money: float = 0.0
    expectancy: float = 0.0
    starting_capital: float = 0.0
    ending_capital: float = 0.0
    roi_percent: float = 0.0

    # COMMODITY-specific metrics
    total_roll_yield: float = 0.0  # Total PnL from contract rolls
    avg_roll_yield: float = 0.0  # Average roll yield per trade
    contango_adjusted_return: float = 0.0  # Return adjusted for contango
    contango_impact_percent: float = 0.0  # Impact of contango on returns
    seasonality_adjusted_return: float = 0.0  # Return adjusted for seasonality
    seasonality_factor: float = 0.0  # Average seasonality factor
    total_commission: float = 0.0  # Total commission costs
    avg_commission: float = 0.0  # Average commission per trade
    avg_holding_days: float = 0.0  # Average holding period
    total_rolls: int = 0  # Number of contract rolls
    avg_usd_exposure: float = 0.0  # Average USD exposure per trade

    # Contango/Backwardation analysis
    avg_contango_spread: float = 0.0  # Average contango spread
    contango_periods: int = 0  # Number of periods in contango
    backwardation_periods: int = 0  # Number of periods in backwardation

    # Risk metrics
    volatility_percent: float = 0.0  # Annualized volatility
    sharpe_ratio: float = 0.0  # Risk-adjusted return
    sortino_ratio: float = 0.0  # Downside risk-adjusted return

    # Contract information
    contract_size: int = 0  # Size of one contract
    tick_size: float = 0.0  # Minimum price movement
    tick_value: float = 0.0  # Value of one tick
    point_value: float = 0.0  # Value of one point

    def to_dict(self) -> Dict[str, Any]:
        base = {
            "symbol": self.symbol,
            "contract": self.contract,
            "timeframe": self.timeframe,
            "strategy": self.strategy,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "leverage": self.leverage,
            "risk_percent": self.risk_percent,
            "avg_contracts": self.avg_contracts,
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": self.win_rate,
            "total_pnl_points": self.total_pnl_points,
            "total_pnl_money": self.total_pnl_money,
            "avg_r": self.avg_r,
            "profit_factor": self.profit_factor,
            "max_drawdown_points": self.max_drawdown_points,
            "max_drawdown_money": self.max_drawdown_money,
            "expectancy": self.expectancy,
            "starting_capital": self.starting_capital,
            "ending_capital": self.ending_capital,
            "roi_percent": self.roi_percent,
            "total_roll_yield": self.total_roll_yield,
            "avg_roll_yield": self.avg_roll_yield,
            "contango_adjusted_return": self.contango_adjusted_return,
            "contango_impact_percent": self.contango_impact_percent,
            "seasonality_adjusted_return": self.seasonality_adjusted_return,
            "seasonality_factor": self.seasonality_factor,
            "total_commission": self.total_commission,
            "avg_commission": self.avg_commission,
            "avg_holding_days": self.avg_holding_days,
            "total_rolls": self.total_rolls,
            "avg_usd_exposure": self.avg_usd_exposure,
            "avg_contango_spread": self.avg_contango_spread,
            "contango_periods": self.contango_periods,
            "backwardation_periods": self.backwardation_periods,
            "volatility_percent": self.volatility_percent,
            "sharpe_ratio": self.sharpe_ratio,
            "sortino_ratio": self.sortino_ratio,
            "contract_size": self.contract_size,
            "tick_size": self.tick_size,
            "tick_value": self.tick_value,
            "point_value": self.point_value,
        }
        return base


class CommodityBacktestEngine(BacktestEngine):
    """
    COMMODITY-specific backtest engine.

    Extends the base BacktestEngine with:
    - Futures contract support with expiration dates
    - Contango-adjusted returns (roll yield calculation)
    - Seasonality-adjusted performance metrics
    - Contract roll simulation
    - MT5 broker integration
    - USD exposure tracking
    - Support for multiple commodity types (metals, energy, agriculture)
    """

    def __init__(self, strategy, config: Optional[Dict[str, Any]] = None):
        # Initialize base class
        super().__init__(strategy, config)

        # Override defaults for COMMODITIES
        self._symbol = self.config.get("symbol", "GC")
        self._contract = self.config.get("contract", "H25")  # Default to March 2025
        self._timeframe = self.config.get("timeframe", "H1")

        # Validate symbol
        if self._symbol not in COMMODITY_CONTRACTS:
            raise ValueError(
                f"Unsupported commodity: {self._symbol}. "
                f"Supported: {list(COMMODITY_CONTRACTS.keys())}"
            )

        # Validate timeframe
        if self._timeframe not in COMMODITY_TIMEFRAMES:
            raise ValueError(
                f"Unsupported timeframe: {self._timeframe}. "
                f"Supported: {COMMODITY_TIMEFRAMES}"
            )

        # Get contract specifications
        contract_spec = COMMODITY_CONTRACTS[self._symbol]
        self.tick_size = contract_spec["tick_size"]
        self.contract_size = contract_spec["contract_size"]
        self.point_value = contract_spec["point_value"]
        self.tick_value = contract_spec["tick_value"]
        self.exchange = contract_spec["exchange"]
        self.currency = contract_spec["currency"]

        # Commission configuration (per contract)
        self.commission_per_contract = self.config.get("commission_per_contract", 0.0)

        # Contango configuration
        self.contango_spread = self.config.get(
            "contango_spread", TYPICAL_CONTANGO_SPREADS.get(self._symbol, 0.02)
        )
        self.auto_roll = self.config.get("auto_roll", True)
        self.roll_days_before_expiry = self.config.get("roll_days_before_expiry", 5)

        # Seasonality configuration
        self.use_seasonality = self.config.get("use_seasonality", True)
        self.seasonality_data = COMMODITY_SEASONALITY.get(self._symbol, {})

        # Contract expiry date (calculated from contract month)
        self.contract_expiry = self._calculate_contract_expiry(self._contract)

        # Store COMMODITY-specific trades
        self.commodity_trades: List[CommodityTradeResult] = []

        # Track rolls and contango periods
        self.total_rolls = 0
        self.contango_periods = 0
        self.backwardation_periods = 0
        self.total_contango_spread = 0.0

        # Store daily returns for volatility calculations
        self.daily_returns: List[float] = []

    def _calculate_contract_expiry(self, contract: str) -> datetime:
        """
        Calculate contract expiration date from contract month code.

        Args:
            contract: Contract month code (e.g., "H25" for March 2025)

        Returns:
            Expiration datetime
        """
        if len(contract) < 3:
            # Default to 3 months from now
            return datetime.now() + timedelta(days=90)

        month_code = contract[0].upper()
        year_suffix = contract[1:]

        # Parse year (assume 20xx)
        try:
            year = 2000 + int(year_suffix)
        except ValueError:
            year = datetime.now().year

        # Map month code to month number
        month_map = {
            "F": 1, "G": 2, "H": 3, "J": 4, "K": 5, "M": 6,
            "N": 7, "Q": 8, "U": 9, "V": 10, "X": 11, "Z": 12,
        }
        month = month_map.get(month_code, 3)  # Default to March

        # Calculate expiry (typically last business day of month before delivery)
        # For simplicity, use the last day of the month
        from calendar import monthrange
        last_day = monthrange(year, month)[1]
        expiry = datetime(year, month, last_day, 23, 59, 59)

        return expiry

    def _get_next_contract(self, current_contract: str) -> str:
        """Get the next contract month after current contract."""
        if len(current_contract) < 3:
            return current_contract

        month_code = current_contract[0].upper()
        year_suffix = current_contract[1:]

        # Month order
        month_order = ["F", "G", "H", "J", "K", "M", "N", "Q", "U", "V", "X", "Z"]
        try:
            current_idx = month_order.index(month_code)
        except ValueError:
            current_idx = 2  # Default to March

        # Get next month
        next_idx = (current_idx + 1) % 12
        next_month = month_order[next_idx]

        # Handle year rollover
        try:
            year = int(year_suffix)
            if next_idx <= current_idx:
                year += 1
            next_year = f"{year:02d}"
        except ValueError:
            next_year = year_suffix

        return f"{next_month}{next_year}"

    def _calculate_roll_yield(
        self, current_price: float, next_price: float, side: str
    ) -> float:
        """
        Calculate roll yield from contract roll.

        In contango (futures > spot): rolling long positions incurs negative yield
        In backwardation (futures < spot): rolling long positions incurs positive yield

        Args:
            current_price: Price of current contract
            next_price: Price of next contract
            side: Trade side (BUY or SELL)

        Returns:
            Roll yield in price points
        """
        if next_price <= 0 or current_price <= 0:
            return 0.0

        # Roll yield = (current_price - next_price) / next_price
        # Positive when current < next (backwardation for longs)
        # Negative when current > next (contango for longs)
        roll_yield_pct = (current_price - next_price) / next_price

        # Convert to price points
        roll_yield = roll_yield_pct * current_price

        # For long positions, negative roll yield in contango
        # For short positions, positive roll yield in contango
        if side == "BUY":
            return roll_yield
        else:
            return -roll_yield

    def _calculate_contango_adjustment(
        self, price: float, side: str, holding_days: int
    ) -> float:
        """
        Calculate contango adjustment for a trade.

        Args:
            price: Entry price
            side: Trade side
            holding_days: Number of days held

        Returns:
            Contango adjustment in price points
        """
        if holding_days <= 0 or self.contango_spread == 0:
            return 0.0

        # Daily contango impact
        daily_contango = self.contango_spread / 365

        # Total contango adjustment
        contango_adjustment = price * daily_contango * holding_days

        # For long positions, contango is negative
        # For short positions, contango is positive
        if side == "BUY":
            return -contango_adjustment
        else:
            return contango_adjustment

    def _calculate_seasonality_adjustment(
        self, entry_time: datetime, exit_time: datetime, pnl_money: float
    ) -> float:
        """
        Calculate seasonality adjustment for a trade.

        Args:
            entry_time: Trade entry time
            exit_time: Trade exit time
            pnl_money: Raw PnL in money terms

        Returns:
            Seasonality adjustment factor
        """
        if not self.use_seasonality or not self.seasonality_data:
            return 0.0

        # Get seasonality factor for entry month
        entry_month = entry_time.month
        seasonality_factor = self.seasonality_data.get(entry_month, 1.0)

        # Seasonality adjustment = PnL * (factor - 1)
        # Positive factor > 1 means favorable seasonality
        if seasonality_factor > 1.0:
            return pnl_money * (seasonality_factor - 1.0)
        elif seasonality_factor < 1.0:
            return pnl_money * (seasonality_factor - 1.0)
        else:
            return 0.0

    def _get_seasonality_factor(self, month: int) -> float:
        """Get seasonality factor for a given month."""
        return self.seasonality_data.get(month, 1.0)

    def _calculate_usd_exposure(
        self, price: float, contracts: float, side: str
    ) -> float:
        """
        Calculate USD exposure for a commodity position.

        Args:
            price: Current price
            contracts: Number of contracts
            side: BUY or SELL

        Returns:
            Total USD exposure
        """
        # USD exposure = price * contract_size * contracts
        exposure = price * self.contract_size * contracts

        # For short positions, exposure is still positive (magnitude)
        return abs(exposure)

    def _calculate_commission(self, contracts: float) -> float:
        """Calculate commission for a trade."""
        return self.commission_per_contract * contracts

    def _simulate_contract_roll(
        self,
        trade: CommodityTradeResult,
        current_price: float,
        next_contract_price: float,
    ) -> CommodityTradeResult:
        """
        Simulate rolling from one contract to the next.

        Args:
            trade: Current trade result
            current_price: Price of current contract at roll time
            next_contract_price: Price of next contract

        Returns:
            Updated trade result with roll information
        """
        # Calculate roll yield
        roll_yield = self._calculate_roll_yield(
            current_price, next_contract_price, trade.side
        )

        # Update trade with roll information
        trade.roll_date = datetime.now()
        trade.roll_yield = roll_yield
        trade.contract_month = self._get_next_contract(trade.contract_month)

        # Update total rolls counter
        self.total_rolls += 1

        return trade

    def _create_commodity_trade_result(
        self,
        signal: TradingSignal,
        side: str,
        entry_time: datetime,
        exit_time: datetime,
        entry_price: float,
        exit_price: float,
        reason: str,
    ) -> CommodityTradeResult:
        """Create COMMODITY-specific trade result."""
        # Get current account balance for position sizing
        current_balance = self.initial_balance
        if self.trades:
            current_balance = self.initial_balance + sum(
                t.pnl_money for t in self.trades
            )

        # Calculate number of contracts using risk manager
        sl_price = signal.buy_sl if side == "BUY" else signal.sell_sl
        lot_result = self.risk_manager.calculate_lot_size(
            account_balance=current_balance,
            entry_price=entry_price,
            sl_price=sl_price,
            risk_percent=self.risk_percent,
            leverage=self.leverage,
        )
        contracts = lot_result["lot_size"]

        # Calculate PnL in price points
        if side == "BUY":
            pnl_points = exit_price - entry_price
        else:
            pnl_points = entry_price - exit_price

        # Calculate PnL in money: contracts * pnl_points * point_value
        pnl_money = pnl_points * contracts * self.point_value

        # Calculate holding days
        holding_days = (exit_time - entry_time).days

        # Calculate contango adjustment
        contango_adj = self._calculate_contango_adjustment(
            entry_price, side, holding_days
        )

        # Calculate seasonality adjustment
        seasonality_adj = self._calculate_seasonality_adjustment(
            entry_time, exit_time, pnl_money
        )

        # Calculate USD exposure
        usd_exposure = self._calculate_usd_exposure(entry_price, contracts, side)

        # Calculate commission
        commission = self._calculate_commission(contracts)

        # Net PnL after costs
        net_pnl_money = pnl_money - commission

        # Determine result based on net PnL
        if net_pnl_money > 0:
            result = "WIN"
        elif net_pnl_money < 0:
            result = "LOSS"
        else:
            result = "BREAKEVEN"

        # Calculate R multiple
        r = signal.r_points
        r_multiple = pnl_points / r if r > 0 else 0

        return CommodityTradeResult(
            entry_time=entry_time,
            exit_time=exit_time,
            symbol=signal.symbol or self._symbol,
            side=side,
            entry_price=entry_price,
            exit_price=exit_price,
            volume=contracts,
            sl=signal.buy_sl if side == "BUY" else signal.sell_sl,
            tp=signal.buy_tp if side == "BUY" else signal.sell_tp,
            result=result,
            pnl_points=pnl_points,
            pnl_money=net_pnl_money,
            r_multiple=r_multiple,
            reason=reason,
            contract_month=self._contract,
            contract_expiry=self.contract_expiry,
            contango_adjustment=contango_adj,
            seasonality_adjustment=seasonality_adj,
            usd_exposure=usd_exposure,
            commission=commission,
            holding_days=holding_days,
        )

    def run(
        self,
        ohlcv_data: List[OHLCV],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        next_contract_price: Optional[float] = None,
    ) -> CommodityBacktestMetrics:
        """Run backtest on historical commodity data."""
        self.trades = []
        self.commodity_trades = []
        self.equity_curve = []
        self.daily_returns = []
        self.total_rolls = 0
        self.contango_periods = 0
        self.backwardation_periods = 0
        self.total_contango_spread = 0.0

        # Capture date range from data if not provided
        if ohlcv_data:
            if not start_date:
                start_date = ohlcv_data[0].timestamp
            if not end_date:
                end_date = ohlcv_data[-1].timestamp

        # Store date range
        self._start_date = start_date.strftime("%Y-%m-%d") if start_date else ""
        self._end_date = end_date.strftime("%Y-%m-%d") if end_date else ""

        # Filter by date if specified
        if start_date:
            ohlcv_data = [c for c in ohlcv_data if c.timestamp >= start_date]
        if end_date:
            ohlcv_data = [c for c in ohlcv_data if c.timestamp <= end_date]

        # Calculate daily returns from OHLCV data for volatility
        self._calculate_daily_returns(ohlcv_data)

        # Determine if in contango or backwardation
        if next_contract_price and ohlcv_data:
            current_price = ohlcv_data[-1].close
            if next_contract_price > current_price:
                self.contango_periods = 1
                self.total_contango_spread = (
                    (next_contract_price - current_price) / current_price
                )
            else:
                self.backwardation_periods = 1
                self.total_contango_spread = (
                    (current_price - next_contract_price) / current_price
                )

        # Find trading days and generate signals
        trading_dates = self._get_trading_days(ohlcv_data)

        for date in trading_dates:
            # Check if we need to roll contracts
            if self.auto_roll and self.contract_expiry:
                days_to_expiry = (self.contract_expiry - date).days
                if days_to_expiry <= self.roll_days_before_expiry:
                    # Roll to next contract
                    self._contract = self._get_next_contract(self._contract)
                    self.contract_expiry = self._calculate_contract_expiry(self._contract)

            # Get OHLCV for this day + lookforward
            day_data = self._get_day_data(ohlcv_data, date)

            if len(day_data) < 10:
                continue

            # Generate signal
            signals = self.strategy.get_signals(day_data)

            if not signals:
                continue

            signal = signals[0]

            # Simulate pending order execution
            trade = self._simulate_commodity_trade(signal, day_data)

            if trade:
                self.trades.append(trade)
                self.commodity_trades.append(trade)

                # Update equity curve
                self._update_equity()

        # Calculate COMMODITY-specific metrics
        metrics = self._calculate_commodity_metrics()

        return metrics

    def _calculate_daily_returns(self, ohlcv_data: List[OHLCV]):
        """Calculate daily returns from OHLCV data for volatility."""
        if len(ohlcv_data) < 2:
            return

        # Sort by timestamp
        sorted_data = sorted(ohlcv_data, key=lambda x: x.timestamp)

        for i in range(1, len(sorted_data)):
            prev_close = sorted_data[i - 1].close
            curr_close = sorted_data[i].close
            if prev_close > 0:
                daily_return = (curr_close - prev_close) / prev_close
                self.daily_returns.append(daily_return)

    def _simulate_commodity_trade(
        self, signal: TradingSignal, day_data: List[OHLCV]
    ) -> Optional[CommodityTradeResult]:
        """Simulate trade execution for commodities with roll simulation."""
        signal_candle_idx = len(day_data) - 4

        if signal_candle_idx >= len(day_data):
            return None

        entry_time = None
        exit_time = None
        exit_price = None
        reason = ""

        # Look for trigger in subsequent candles
        for i in range(signal_candle_idx + 1, len(day_data)):
            candle = day_data[i]
            high = candle.high
            low = candle.low

            # Check buy trigger
            if high >= signal.buy_stop:
                entry_time = candle.timestamp
                entry_price = signal.buy_stop

                # Check TP
                if high >= signal.buy_tp:
                    exit_time = candle.timestamp
                    exit_price = signal.buy_tp
                    reason = "TP hit"
                # Check SL
                elif low <= signal.buy_sl:
                    exit_time = candle.timestamp
                    exit_price = signal.buy_sl
                    reason = "SL hit"
                else:
                    # Close at end of day
                    exit_time = candle.timestamp
                    exit_price = candle.close
                    reason = "session end"

                return self._create_commodity_trade_result(
                    signal,
                    "BUY",
                    entry_time,
                    exit_time,
                    entry_price,
                    exit_price,
                    reason,
                )

            # Check sell trigger
            if low <= signal.sell_stop:
                entry_time = candle.timestamp
                entry_price = signal.sell_stop

                # Check TP
                if low <= signal.sell_tp:
                    exit_time = candle.timestamp
                    exit_price = signal.sell_tp
                    reason = "TP hit"
                # Check SL
                elif high >= signal.sell_sl:
                    exit_time = candle.timestamp
                    exit_price = signal.sell_sl
                    reason = "SL hit"
                else:
                    exit_time = candle.timestamp
                    exit_price = candle.close
                    reason = "session end"

                return self._create_commodity_trade_result(
                    signal,
                    "SELL",
                    entry_time,
                    exit_time,
                    entry_price,
                    exit_price,
                    reason,
                )

        # No trigger - cancelled
        return None

    def _calculate_commodity_metrics(self) -> CommodityBacktestMetrics:
        """Calculate COMMODITY-specific performance metrics."""
        if not self.commodity_trades:
            return CommodityBacktestMetrics(
                symbol=self._symbol,
                contract=self._contract,
                timeframe=self._timeframe,
                strategy=self._strategy_name,
                start_date=self._start_date,
                end_date=self._end_date,
                leverage=self.leverage,
                risk_percent=self.risk_percent,
                contract_size=self.contract_size,
                tick_size=self.tick_size,
                tick_value=self.tick_value,
                point_value=self.point_value,
            )

        winning = [t for t in self.commodity_trades if t.result == "WIN"]
        losing = [t for t in self.commodity_trades if t.result == "LOSS"]

        # Basic PnL calculations
        total_pnl_money = sum(t.pnl_money for t in self.commodity_trades)
        total_pnl_points = sum(t.pnl_points for t in self.commodity_trades)
        total_commission = sum(t.commission for t in self.commodity_trades)
        total_roll_yield = sum(t.roll_yield for t in self.commodity_trades)

        # Profit factor
        wins_pnl = sum(t.pnl_money for t in winning) if winning else 0
        losses_pnl = abs(sum(t.pnl_money for t in losing)) if losing else 1
        profit_factor = wins_pnl / losses_pnl if losses_pnl > 0 else 0

        # Average R
        avg_r = sum(t.r_multiple for t in self.commodity_trades) / len(self.commodity_trades)

        # Expectancy
        expectancy = total_pnl_money / len(self.commodity_trades)

        # Average contracts
        avg_contracts = (
            sum(t.volume for t in self.commodity_trades) / len(self.commodity_trades)
            if self.commodity_trades
            else 0
        )

        # Average holding days
        total_holding_days = sum(t.holding_days for t in self.commodity_trades)
        avg_holding_days = total_holding_days / len(self.commodity_trades)

        # Average commission
        avg_commission = total_commission / len(self.commodity_trades)

        # Average roll yield
        avg_roll_yield = total_roll_yield / len(self.commodity_trades) if self.commodity_trades else 0

        # Average USD exposure
        total_usd_exposure = sum(t.usd_exposure for t in self.commodity_trades)
        avg_usd_exposure = total_usd_exposure / len(self.commodity_trades)

        # Capital calculations
        starting_capital = self.initial_balance
        ending_capital = self.initial_balance + total_pnl_money
        roi_percent = (
            ((ending_capital - starting_capital) / starting_capital * 100)
            if starting_capital > 0
            else 0
        )

        # Contango-adjusted return
        contango_adjusted_return = total_pnl_money + sum(
            t.contango_adjustment for t in self.commodity_trades
        )

        # Seasonality-adjusted return
        seasonality_adjusted_return = total_pnl_money + sum(
            t.seasonality_adjustment for t in self.commodity_trades
        )

        # Contango impact percentage
        gross_pnl = abs(total_pnl_money)
        contango_impact_percent = (
            (sum(abs(t.contango_adjustment) for t in self.commodity_trades) / gross_pnl * 100)
            if gross_pnl > 0
            else 0
        )

        # Average seasonality factor
        if self.seasonality_data:
            avg_seasonality = sum(
                self._get_seasonality_factor(t.entry_time.month)
                for t in self.commodity_trades
            ) / len(self.commodity_trades)
        else:
            avg_seasonality = 1.0

        # Average contango spread
        avg_contango_spread = (
            self.total_contango_spread / max(self.contango_periods + self.backwardation_periods, 1)
        )

        # Volatility (annualized)
        volatility_percent = self._calculate_volatility()

        # Sharpe ratio
        sharpe_ratio = self._calculate_sharpe_ratio(roi_percent, volatility_percent)

        # Sortino ratio
        sortino_ratio = self._calculate_sortino_ratio()

        # Max drawdown
        max_dd = 0
        peak = self.initial_balance
        for eq in self.equity_curve:
            if eq["equity"] > peak:
                peak = eq["equity"]
            dd = (peak - eq["equity"]) / peak * 100 if peak > 0 else 0
            if dd > max_dd:
                max_dd = dd

        return CommodityBacktestMetrics(
            symbol=self._symbol,
            contract=self._contract,
            timeframe=self._timeframe,
            strategy=self._strategy_name,
            start_date=self._start_date,
            end_date=self._end_date,
            leverage=self.leverage,
            risk_percent=self.risk_percent,
            avg_contracts=avg_contracts,
            total_trades=len(self.commodity_trades),
            winning_trades=len(winning),
            losing_trades=len(losing),
            win_rate=len(winning) / len(self.commodity_trades) * 100,
            total_pnl_points=total_pnl_points,
            total_pnl_money=total_pnl_money,
            avg_r=avg_r,
            profit_factor=profit_factor,
            max_drawdown_points=max_dd,
            max_drawdown_money=max_dd,
            expectancy=expectancy,
            starting_capital=starting_capital,
            ending_capital=ending_capital,
            roi_percent=roi_percent,
            total_roll_yield=total_roll_yield,
            avg_roll_yield=avg_roll_yield,
            contango_adjusted_return=contango_adjusted_return,
            contango_impact_percent=contango_impact_percent,
            seasonality_adjusted_return=seasonality_adjusted_return,
            seasonality_factor=avg_seasonality,
            total_commission=total_commission,
            avg_commission=avg_commission,
            avg_holding_days=avg_holding_days,
            total_rolls=self.total_rolls,
            avg_usd_exposure=avg_usd_exposure,
            avg_contango_spread=avg_contango_spread,
            contango_periods=self.contango_periods,
            backwardation_periods=self.backwardation_periods,
            volatility_percent=volatility_percent,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            contract_size=self.contract_size,
            tick_size=self.tick_size,
            tick_value=self.tick_value,
            point_value=self.point_value,
        )

    def _calculate_volatility(self) -> float:
        """Calculate annualized volatility from daily returns."""
        if len(self.daily_returns) < 2:
            return 0.0

        # Calculate standard deviation of daily returns
        daily_std = np.std(self.daily_returns, ddof=1)

        # Annualize (sqrt of 252 trading days)
        annualized_vol = daily_std * np.sqrt(252) * 100  # Convert to percentage

        return annualized_vol

    def _calculate_sharpe_ratio(
        self, annual_return: float, volatility: float
    ) -> float:
        """Calculate Sharpe ratio."""
        if volatility <= 0:
            return 0.0

        risk_free_rate = 0.05  # 5% annual risk-free rate
        excess_return = annual_return / 100 - risk_free_rate
        return excess_return / (volatility / 100)

    def _calculate_sortino_ratio(self) -> float:
        """Calculate Sortino ratio (downside risk only)."""
        if len(self.daily_returns) < 2:
            return 0.0

        # Calculate downside returns (negative returns only)
        downside_returns = [r for r in self.daily_returns if r < 0]

        if not downside_returns:
            return float('inf')

        # Calculate downside deviation
        downside_std = np.std(downside_returns, ddof=1)

        # Annualize downside deviation
        annualized_downside = downside_std * np.sqrt(252)

        if annualized_downside <= 0:
            return 0.0

        # Calculate annual return from daily returns
        cumulative_return = 1.0
        for ret in self.daily_returns:
            cumulative_return *= (1 + ret)
        annual_return = (cumulative_return - 1) * 100

        risk_free_rate = 0.05
        excess_return = annual_return / 100 - risk_free_rate
        return excess_return / annualized_downside

    def run_multi_contract(
        self,
        ohlcv_data_by_contract: Dict[str, List[OHLCV]],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, CommodityBacktestMetrics]:
        """Run backtest across multiple futures contracts."""
        results = {}

        for contract, ohlcv_data in ohlcv_data_by_contract.items():
            # Update contract in config
            self.config["contract"] = contract
            self._contract = contract
            self.contract_expiry = self._calculate_contract_expiry(contract)

            # Run backtest for this contract
            metrics = self.run(ohlcv_data, start_date, end_date)
            results[contract] = metrics

        return results

    def set_contango_spread(self, spread: float):
        """Set the contango spread for roll yield calculations."""
        self.contango_spread = spread

    def set_seasonality_data(self, seasonality_data: Dict[int, float]):
        """Set custom seasonality data for the commodity."""
        self.seasonality_data = seasonality_data
        self.use_seasonality = True

    def export_trades(self, filename: str = "commodity_backtest_trades.json") -> str:
        """Export COMMODITY trades to JSON."""
        data = {
            "metrics": self._calculate_commodity_metrics().to_dict(),
            "trades": [t.to_dict() for t in self.commodity_trades],
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        return filename

    def format_summary(self, metrics: CommodityBacktestMetrics) -> str:
        """Format COMMODITY metrics as readable summary."""
        return f"""
=== COMMODITY Backtest Results ===

Symbol:     {metrics.symbol}
Contract:   {metrics.contract}
Timeframe:  {metrics.timeframe}
Strategy:   {metrics.strategy}
Period:     {metrics.start_date} to {metrics.end_date}

Capital:
  Starting:          ${metrics.starting_capital:,.2f}
  Ending:            ${metrics.ending_capital:,.2f}
  Gross PnL:         ${metrics.total_pnl_money:,.2f}
  ROI:               {metrics.roi_percent:.2f}%

Contract Info:
  Contract Size:     {metrics.contract_size}
  Tick Size:         {metrics.tick_size}
  Tick Value:        ${metrics.tick_value:.2f}
  Point Value:       ${metrics.point_value:.2f}

Contango Analysis:
  Total Roll Yield:  ${metrics.total_roll_yield:,.2f}
  Avg Roll Yield:    ${metrics.avg_roll_yield:.2f}
  Contango Adj Ret:  ${metrics.contango_adjusted_return:,.2f}
  Contango Impact:   {metrics.contango_impact_percent:.1f}%
  Avg Contango:      {metrics.avg_contango_spread:.2%}
  Contango Periods:  {metrics.contango_periods}
  Backward Periods:  {metrics.backwardation_periods}

Seasonality:
  Seasonality Adj:   ${metrics.seasonality_adjusted_return:,.2f}
  Avg Seasonality:   {metrics.seasonality_factor:.2f}

Risk-Adjusted:
  Volatility:        {metrics.volatility_percent:.2f}%
  Sharpe Ratio:      {metrics.sharpe_ratio:.2f}
  Sortino Ratio:     {metrics.sortino_ratio:.2f}

Trades:
  Total:             {metrics.total_trades}
  Wins:              {metrics.winning_trades}
  Losses:            {metrics.losing_trades}
  Win Rate:          {metrics.win_rate:.1f}%
  Avg Holding:       {metrics.avg_holding_days:.1f} days
  Total Rolls:       {metrics.total_rolls}

Costs:
  Total Commission:  ${metrics.total_commission:,.2f}
  Avg Commission:    ${metrics.avg_commission:.2f}

Performance:
  Profit Factor:     {metrics.profit_factor:.2f}
  Average R:         {metrics.avg_r:.2f}
  Expectancy:        ${metrics.expectancy:.2f}
  Max Drawdown:      {metrics.max_drawdown_points:.1f}%

Exposure:
  Avg USD Exposure:  ${metrics.avg_usd_exposure:,.2f}
"""

    def get_supported_contracts(self) -> List[str]:
        """Get list of supported commodity contracts."""
        return list(COMMODITY_CONTRACTS.keys())

    def get_supported_timeframes(self) -> List[str]:
        """Get list of supported timeframes."""
        return COMMODITY_TIMEFRAMES.copy()

    def get_contract_info(self, symbol: str) -> Dict[str, Any]:
        """Get contract specifications for a commodity."""
        if symbol not in COMMODITY_CONTRACTS:
            raise ValueError(f"Unknown commodity: {symbol}")
        return COMMODITY_CONTRACTS[symbol]

    def get_seasonality_info(self, symbol: str) -> Dict[int, float]:
        """Get seasonality data for a commodity."""
        return COMMODITY_SEASONALITY.get(symbol, {})

    def get_contract_month_name(self, contract: str) -> str:
        """Get full month name from contract month code."""
        if len(contract) < 1:
            return "Unknown"
        month_code = contract[0].upper()
        month_name = FUTURES_MONTH_CODES.get(month_code, "Unknown")
        year_suffix = contract[1:] if len(contract) > 1 else ""
        return f"{month_name} 20{year_suffix}" if year_suffix else month_name
