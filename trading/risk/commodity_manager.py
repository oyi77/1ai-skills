"""
Commodity Risk Management Module

Handles COMMODITY-specific risk management including contract-specific position limits,
contango/backwardation awareness (futures), seasonality risk (unusual patterns),
supply/demand event risk, and currency exposure (commodities priced in USD).
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta
from enum import Enum


class CommodityType(Enum):
    """Types of commodities."""
    PRECIOUS_METALS = "Precious Metals"
    ENERGY = "Energy"
    AGRICULTURAL = "Agricultural"
    INDUSTRIAL_METALS = "Industrial Metals"
    SOFTS = "Softs"


class Commodity(Enum):
    """Commodities supported for trading."""
    # Precious Metals
    GOLD = "XAUUSD"
    SILVER = "XAGUSD"
    PLATINUM = "XPTUSD"
    PALLADIUM = "XPDUSD"
    
    # Energy
    CRUDE_OIL = "CL"
    BRENT_CRUDE = "BRN"
    NATURAL_GAS = "NG"
    HEATING_OIL = "HO"
    GASOLINE = "RB"
    
    # Agricultural
    CORN = "ZC"
    WHEAT = "ZW"
    SOYBEANS = "ZS"
    COTTON = "CT"
    COFFEE = "KC"
    SUGAR = "SB"
    COCOA = "CC"
    OATS = "ZO"
    
    # Industrial Metals
    COPPER = "HG"
    ALUMINUM = "ALI"
    ZINC = "ZS"
    NICKEL = "NI"
    LEAD = "LL"
    
    # Softs
    ORANGE_JUICE = "OJ"
    LIVE_CATTLE = "LC"
    LEAN_HOGS = "LH"
    FEEDER_CATTLE = "FC"


@dataclass
class CommodityConfig:
    """Commodity risk management configuration."""
    
    # Risk settings
    risk_per_trade_percent: float = 1.0  # Risk 1-2% per trade
    min_rr_ratio: float = 2.0  # Minimum risk-reward ratio (1:2)
    
    # Contract specifications (standard futures contracts)
    contract_specs: Dict[str, Dict] = field(default_factory=lambda: {
        # Precious Metals
        "XAUUSD": {"contract_size": 100, "unit": "oz", "tick_size": 0.01, "tick_value": 1.0},
        "XAGUSD": {"contract_size": 5000, "unit": "oz", "tick_size": 0.005, "tick_value": 25.0},
        "XPTUSD": {"contract_size": 100, "unit": "oz", "tick_size": 0.1, "tick_value": 10.0},
        "XPDUSD": {"contract_size": 100, "unit": "oz", "tick_size": 0.1, "tick_value": 10.0},
        
        # Energy
        "CL": {"contract_size": 1000, "unit": "barrels", "tick_size": 0.01, "tick_value": 10.0},
        "BRN": {"contract_size": 1000, "unit": "barrels", "tick_size": 0.01, "tick_value": 10.0},
        "NG": {"contract_size": 10000, "unit": "mmBtu", "tick_size": 0.001, "tick_value": 10.0},
        "HO": {"contract_size": 42000, "unit": "gallons", "tick_size": 0.0001, "tick_value": 4.2},
        "RB": {"contract_size": 42000, "unit": "gallons", "tick_size": 0.0001, "tick_value": 4.2},
        
        # Agricultural
        "ZC": {"contract_size": 5000, "unit": "bushels", "tick_size": 0.0025, "tick_value": 12.5},
        "ZW": {"contract_size": 5000, "unit": "bushels", "tick_size": 0.0025, "tick_value": 12.5},
        "ZS": {"contract_size": 5000, "unit": "bushels", "tick_size": 0.0025, "tick_value": 12.5},
        "CT": {"contract_size": 500, "unit": "lbs", "tick_size": 0.0001, "tick_value": 0.05},
        "KC": {"contract_size": 37500, "unit": "lbs", "tick_size": 0.0005, "tick_value": 18.75},
        "SB": {"contract_size": 112000, "unit": "lbs", "tick_size": 0.0001, "tick_value": 11.2},
        "CC": {"contract_size": 10, "unit": "tons", "tick_size": 1.0, "tick_value": 10.0},
        "ZO": {"contract_size": 5000, "unit": "bushels", "tick_size": 0.0025, "tick_value": 12.5},
        
        # Industrial Metals
        "HG": {"contract_size": 25000, "unit": "lbs", "tick_size": 0.0005, "tick_value": 12.5},
        "ALI": {"contract_size": 20000, "unit": "kg", "tick_size": 0.5, "tick_value": 10.0},
        "ZS": {"contract_size": 25, "unit": "tons", "tick_size": 0.5, "tick_value": 12.5},
        "NI": {"contract_size": 1, "unit": "tons", "tick_size": 10.0, "tick_value": 10.0},
        "LL": {"contract_size": 25, "unit": "tons", "tick_size": 0.5, "tick_value": 12.5},
        
        # Softs
        "OJ": {"contract_size": 15000, "unit": "lbs", "tick_size": 0.0005, "tick_value": 7.5},
        "LC": {"contract_size": 40000, "unit": "lbs", "tick_size": 0.00025, "tick_value": 10.0},
        "LH": {"contract_size": 20000, "unit": "lbs", "tick_size": 0.00025, "tick_value": 5.0},
        "FC": {"contract_size": 50000, "unit": "lbs", "tick_size": 0.00025, "tick_value": 12.5},
    })
    
    # Position limits
    max_position_percent: float = 10.0  # Max 10% per commodity
    min_position_percent: float = 5.0  # Min 5% per commodity (recommended)
    max_single_contract_exposure: float = 5.0  # Max 5% for single contract
    
    # Contango/Backwardation settings
    max_contango_percent: float = 5.0  # Max contango before warning
    max_backwardation_percent: float = 5.0  # Max backwardation before warning
    roll_cost_warning_threshold: float = 2.0  # Warn if roll cost > 2% annually
    
    # Seasonality settings
    seasonality_warning_threshold: float = 1.5  # Std dev threshold for seasonality warning
    
    # Supply/Demand event settings
    supply_event_risk_days: int = 5  # Days to avoid trading before/after supply events
    supply_event_warning_days: int = 10  # Days for supply event warning
    
    # Currency exposure (commodities priced in USD)
    max_non_usd_exposure_percent: float = 20.0  # Max 20% in non-USD denominated commodities
    
    # Loss limits
    max_daily_loss_percent: float = 3.0  # Max 3% daily loss
    max_weekly_loss_percent: float = 6.0  # Max 6% weekly loss
    
    # Supported commodities
    supported_commodities: List[str] = field(default_factory=lambda: [
        "XAUUSD", "XAGUSD", "XPTUSD", "XPDUSD",  # Precious Metals
        "CL", "BRN", "NG", "HO", "RB",  # Energy
        "ZC", "ZW", "ZS", "CT", "KC", "SB", "CC", "ZO",  # Agricultural
        "HG", "ALI", "ZS", "NI", "LL",  # Industrial Metals
        "OJ", "LC", "LH", "FC",  # Softs
    ])


@dataclass
class SupplyDemandEvent:
    """Supply/demand event data."""
    commodity: str
    event_date: datetime
    event_type: str  # e.g., "OPEC Meeting", "USDA Report", "Weather Event"
    impact: str  # "High", "Medium", "Low"
    description: str = ""


@dataclass
class SeasonalityPattern:
    """Seasonality pattern data for a commodity."""
    commodity: str
    month: int  # 1-12
    avg_return: float
    std_deviation: float
    sample_size: int


class COMMODITYRiskManager:
    """Commodity-specific risk management."""
    
    # Commodity type mapping
    COMMODITY_TYPES = {
        "XAUUSD": CommodityType.PRECIOUS_METALS,
        "XAGUSD": CommodityType.PRECIOUS_METALS,
        "XPTUSD": CommodityType.PRECIOUS_METALS,
        "XPDUSD": CommodityType.PRECIOUS_METALS,
        "CL": CommodityType.ENERGY,
        "BRN": CommodityType.ENERGY,
        "NG": CommodityType.ENERGY,
        "HO": CommodityType.ENERGY,
        "RB": CommodityType.ENERGY,
        "ZC": CommodityType.AGRICULTURAL,
        "ZW": CommodityType.AGRICULTURAL,
        "ZS": CommodityType.AGRICULTURAL,
        "CT": CommodityType.AGRICULTURAL,
        "KC": CommodityType.AGRICULTURAL,
        "SB": CommodityType.AGRICULTURAL,
        "CC": CommodityType.AGRICULTURAL,
        "ZO": CommodityType.AGRICULTURAL,
        "HG": CommodityType.INDUSTRIAL_METALS,
        "ALI": CommodityType.INDUSTRIAL_METALS,
        "ZS": CommodityType.INDUSTRIAL_METALS,
        "NI": CommodityType.INDUSTRIAL_METALS,
        "LL": CommodityType.INDUSTRIAL_METALS,
        "OJ": CommodityType.SOFTS,
        "LC": CommodityType.SOFTS,
        "LH": CommodityType.SOFTS,
        "FC": CommodityType.SOFTS,
    }
    
    # Common seasonality patterns (simplified)
    SEASONALITY_PATTERNS = {
        "NG": {  # Natural Gas - higher in winter
            1: {"avg_return": 0.02, "std_deviation": 0.08},
            2: {"avg_return": 0.015, "std_deviation": 0.07},
            3: {"avg_return": -0.01, "std_deviation": 0.06},
            4: {"avg_return": -0.015, "std_deviation": 0.05},
            5: {"avg_return": -0.02, "std_deviation": 0.05},
            6: {"avg_return": -0.015, "std_deviation": 0.05},
            7: {"avg_return": -0.01, "std_deviation": 0.05},
            8: {"avg_return": 0.0, "std_deviation": 0.05},
            9: {"avg_return": 0.005, "std_deviation": 0.05},
            10: {"avg_return": 0.015, "std_deviation": 0.06},
            11: {"avg_return": 0.025, "std_deviation": 0.07},
            12: {"avg_return": 0.03, "std_deviation": 0.08},
        },
        "CL": {  # Crude Oil - seasonal demand patterns
            1: {"avg_return": 0.01, "std_deviation": 0.06},
            2: {"avg_return": 0.005, "std_deviation": 0.05},
            3: {"avg_return": 0.0, "std_deviation": 0.05},
            4: {"avg_return": -0.005, "std_deviation": 0.05},
            5: {"avg_return": -0.01, "std_deviation": 0.05},
            6: {"avg_return": 0.0, "std_deviation": 0.05},
            7: {"avg_return": 0.005, "std_deviation": 0.05},
            8: {"avg_return": 0.01, "std_deviation": 0.05},
            9: {"avg_return": 0.015, "std_deviation": 0.05},
            10: {"avg_return": 0.01, "std_deviation": 0.05},
            11: {"avg_return": 0.005, "std_deviation": 0.05},
            12: {"avg_return": 0.01, "std_deviation": 0.06},
        },
        "ZC": {  # Corn - harvest pressure in fall
            1: {"avg_return": 0.005, "std_deviation": 0.05},
            2: {"avg_return": 0.01, "std_deviation": 0.05},
            3: {"avg_return": 0.005, "std_deviation": 0.05},
            4: {"avg_return": 0.0, "std_deviation": 0.05},
            5: {"avg_return": -0.005, "std_deviation": 0.05},
            6: {"avg_return": 0.0, "std_deviation": 0.05},
            7: {"avg_return": 0.005, "std_deviation": 0.05},
            8: {"avg_return": 0.01, "std_deviation": 0.05},
            9: {"avg_return": 0.005, "std_deviation": 0.05},
            10: {"avg_return": -0.01, "std_deviation": 0.06},
            11: {"avg_return": -0.015, "std_deviation": 0.07},
            12: {"avg_return": -0.01, "std_deviation": 0.06},
        },
        "ZW": {  # Wheat - similar to corn
            1: {"avg_return": 0.005, "std_deviation": 0.05},
            2: {"avg_return": 0.01, "std_deviation": 0.05},
            3: {"avg_return": 0.005, "std_deviation": 0.05},
            4: {"avg_return": 0.0, "std_deviation": 0.05},
            5: {"avg_return": -0.005, "std_deviation": 0.05},
            6: {"avg_return": 0.0, "std_deviation": 0.05},
            7: {"avg_return": 0.005, "std_deviation": 0.05},
            8: {"avg_return": 0.01, "std_deviation": 0.05},
            9: {"avg_return": 0.005, "std_deviation": 0.05},
            10: {"avg_return": -0.01, "std_deviation": 0.06},
            11: {"avg_return": -0.015, "std_deviation": 0.07},
            12: {"avg_return": -0.01, "std_deviation": 0.06},
        },
        "XAUUSD": {  # Gold - safe haven flows
            1: {"avg_return": 0.01, "std_deviation": 0.04},
            2: {"avg_return": 0.005, "std_deviation": 0.04},
            3: {"avg_return": 0.0, "std_deviation": 0.04},
            4: {"avg_return": -0.005, "std_deviation": 0.04},
            5: {"avg_return": 0.0, "std_deviation": 0.04},
            6: {"avg_return": 0.005, "std_deviation": 0.04},
            7: {"avg_return": 0.01, "std_deviation": 0.04},
            8: {"avg_return": 0.005, "std_deviation": 0.04},
            9: {"avg_return": 0.0, "std_deviation": 0.04},
            10: {"avg_return": 0.005, "std_deviation": 0.04},
            11: {"avg_return": 0.01, "std_deviation": 0.04},
            12: {"avg_return": 0.015, "std_deviation": 0.04},
        },
    }
    
    def __init__(self, config: Optional[CommodityConfig] = None):
        self.config = config or CommodityConfig()
        self.daily_loss = 0.0
        self.weekly_loss = 0.0
        self.daily_trades = 0
        self.weekly_trades = 0
        self.current_positions: Dict[str, Dict] = {}
        self.supply_demand_calendar: Dict[str, SupplyDemandEvent] = {}
    
    def calculate_position_size(
        self,
        account_balance: float,
        entry_price: float,
        sl_price: float,
        commodity: str,
        risk_percent: float = None,
    ) -> Dict[str, float]:
        """
        Calculate position size using contract-specific method (COMMODITY-specific).
        
        Args:
            account_balance: Total account balance
            entry_price: Entry price
            sl_price: Stop loss price
            commodity: Commodity symbol (e.g., "XAUUSD", "CL")
            risk_percent: Risk percentage (default from config)
        
        Returns:
            Dict with contracts, risk_amount, contract_value, etc.
        """
        if risk_percent is None:
            risk_percent = self.config.risk_per_trade_percent
        
        # Get contract specifications
        contract_spec = self._get_contract_spec(commodity)
        if contract_spec is None:
            return {
                "contracts": 0,
                "risk_amount": 0.0,
                "error": f"Unknown commodity: {commodity}"
            }
        
        # Calculate SL distance in price terms
        sl_distance = abs(entry_price - sl_price)
        
        if sl_distance == 0:
            return {
                "contracts": 0,
                "risk_amount": 0.0,
                "error": "Zero SL distance"
            }
        
        # Calculate risk amount in account currency
        risk_amount = account_balance * (risk_percent / 100)
        
        # Calculate tick value and contract value
        tick_size = contract_spec["tick_size"]
        tick_value = contract_spec["tick_value"]
        contract_size = contract_spec["contract_size"]
        
        # Calculate number of ticks for SL
        sl_ticks = sl_distance / tick_size
        
        # Risk per contract = SL ticks * tick value
        risk_per_contract = sl_ticks * tick_value
        
        if risk_per_contract == 0:
            return {
                "contracts": 0,
                "risk_amount": 0.0,
                "error": "Zero risk per contract"
            }
        
        # Number of contracts = Risk amount / Risk per contract
        contracts = risk_amount / risk_per_contract
        
        # Round to reasonable precision (typically 0.01 for most contracts)
        contracts = round(contracts * 100) / 100
        contracts = max(contracts, 0.01)
        
        # Calculate actual risk
        actual_risk = contracts * risk_per_contract
        
        # Calculate contract value
        contract_value = entry_price * contract_size
        
        return {
            "contracts": contracts,
            "risk_amount": round(actual_risk, 2),
            "risk_percent": risk_percent,
            "contract_value": round(contract_value, 2),
            "sl_distance": sl_distance,
            "sl_ticks": sl_ticks,
            "tick_size": tick_size,
            "tick_value": tick_value,
            "contract_size": contract_size,
            "unit": contract_spec["unit"],
            "entry_price": entry_price,
            "sl_price": sl_price,
        }
    
    def _get_contract_spec(self, commodity: str) -> Optional[Dict]:
        """Get contract specifications for a commodity."""
        commodity_upper = commodity.upper()
        return self.config.contract_specs.get(commodity_upper)
    
    def _get_commodity_type(self, commodity: str) -> CommodityType:
        """Get commodity type."""
        commodity_upper = commodity.upper()
        return self.COMMODITY_TYPES.get(commodity_upper, CommodityType.OTHER)
    
    def contango_check(
        self,
        commodity: str,
        spot_price: float,
        futures_price: float,
        days_to_expiry: int = 30,
    ) -> Tuple[bool, str]:
        """
        Check contango/backwardation conditions for futures.
        
        Args:
            commodity: Commodity symbol
            spot_price: Current spot price
            futures_price: Futures contract price
            days_to_expiry: Days until futures contract expiry
        
        Returns:
            (is_safe, message)
        """
        if spot_price == 0:
            return (False, "Spot price cannot be zero")
        
        # Calculate percentage difference
        price_diff = (futures_price - spot_price) / spot_price * 100
        
        # Annualize the premium/discount
        if days_to_expiry > 0:
            annualized_diff = (price_diff / days_to_expiry) * 365
        else:
            annualized_diff = price_diff
        
        # Check for contango (futures > spot)
        if price_diff > 0:
            max_contango = self.config.max_contango_percent
            if price_diff > max_contango:
                return (False, f"Contango {price_diff:.2f}% exceeds max {max_contango}% - negative roll yield expected")
            
            # Calculate roll cost estimate
            roll_cost_annual = annualized_diff
            roll_cost_warning = self.config.roll_cost_warning_threshold
            
            if roll_cost_annual > roll_cost_warning:
                return (True, f"Contango {price_diff:.2f}% - roll cost ~{roll_cost_annual:.1f}% annually (warning threshold: {roll_cost_warning}%)")
            
            return (True, f"Contango {price_diff:.2f}% is acceptable")
        
        # Check for backwardation (futures < spot)
        else:
            max_backwardation = self.config.max_backwardation_percent
            if abs(price_diff) > max_backwardation:
                return (False, f"Backwardation {abs(price_diff):.2f}% exceeds max {max_backwardation}% - unusual backwardation")
            
            # Backwardation is generally positive for roll returns
            roll_benefit_annual = abs(annualized_diff)
            
            return (True, f"Backwardation {abs(price_diff):.2f}% - positive roll yield ~{roll_benefit_annual:.1f}% annually")
    
    def seasonality_risk_check(
        self,
        commodity: str,
        current_date: datetime = None,
    ) -> Tuple[bool, str]:
        """
        Check seasonality risk for a commodity.
        
        Args:
            commodity: Commodity symbol
            current_date: Current date (default: now)
        
        Returns:
            (is_safe, message)
        """
        if current_date is None:
            current_date = datetime.now()
        
        commodity_upper = commodity.upper()
        
        # Check if we have seasonality data
        if commodity_upper not in self.SEASONALITY_PATTERNS:
            return (True, f"No seasonality data for {commodity}")
        
        seasonality_data = self.SEASONALITY_PATTERNS[commodity_upper]
        current_month = current_date.month
        
        # Get current month's pattern
        if current_month not in seasonality_data:
            return (True, f"No seasonality data for {commodity} in month {current_month}")
        
        month_pattern = seasonality_data[current_month]
        avg_return = month_pattern["avg_return"]
        std_deviation = month_pattern["std_deviation"]
        
        # Check if current return is unusual (beyond threshold std dev)
        threshold = self.config.seasonality_warning_threshold
        
        # Calculate z-score (how many std deviations from mean)
        if std_deviation > 0:
            z_score = avg_return / std_deviation
        else:
            z_score = 0
        
        if abs(z_score) > threshold:
            return (True, f"Seasonality alert: {commodity} in month {current_month} has unusual pattern (z-score: {z_score:.2f})")
        
        # Check for strong seasonal patterns
        if avg_return > 0.02:  # > 2% average return
            return (True, f"Strong seasonal uptrend: {commodity} in month {current_month} (avg: {avg_return*100:.1f}%)")
        elif avg_return < -0.02:  # < -2% average return
            return (True, f"Strong seasonal downtrend: {commodity} in month {current_month} (avg: {avg_return*100:.1f}%)")
        
        return (True, f"Seasonality normal for {commodity} in month {current_month}")
    
    def supply_demand_check(
        self,
        commodity: str,
        current_date: datetime = None,
    ) -> Tuple[bool, str]:
        """
        Check supply/demand event risk.
        
        Args:
            commodity: Commodity symbol
            current_date: Current date (default: now)
        
        Returns:
            (is_safe, message)
        """
        if current_date is None:
            current_date = datetime.now()
        
        commodity_upper = commodity.upper()
        
        if commodity_upper not in self.supply_demand_calendar:
            return (True, "No supply/demand events on record")
        
        event = self.supply_demand_calendar[commodity_upper]
        days_to_event = (event.event_date - current_date).days
        
        # Check if within risk period
        risk_days = self.config.supply_event_risk_days
        warning_days = self.config.supply_event_warning_days
        
        if abs(days_to_event) <= risk_days:
            return (False, f"{event.event_type} in {days_to_event} days ({event.impact} impact) - high risk period")
        
        if abs(days_to_event) <= warning_days:
            return (True, f"Warning: {event.event_type} in {days_to_event} days ({event.impact} impact)")
        
        return (True, f"{event.event_type} in {days_to_event} days - acceptable")
    
    def add_supply_demand_event(self, event: SupplyDemandEvent):
        """Add a supply/demand event to the calendar."""
        self.supply_demand_calendar[event.commodity.upper()] = event
    
    def check_position_limits(
        self,
        commodity: str,
        position_percent: float,
        account_balance: float,
    ) -> Tuple[bool, str]:
        """
        Check if position size is within limits.
        
        Args:
            commodity: Commodity symbol
            position_percent: Proposed position as percentage of account
            account_balance: Total account balance
        
        Returns:
            (is_safe, warning_message)
        """
        max_percent = self.config.max_position_percent
        min_percent = self.config.min_position_percent
        
        if position_percent > max_percent:
            return (False, f"Position size {position_percent:.1f}% exceeds max {max_percent}% for {commodity}")
        
        if position_percent < min_percent:
            return (True, f"Position size {position_percent:.1f}% is below recommended {min_percent}% for {commodity}")
        
        return (True, f"Position size {position_percent:.1f}% is acceptable")
    
    def check_usd_exposure(
        self,
        commodity: str,
        proposed_position_value: float,
        current_positions: Dict[str, Dict] = None,
    ) -> Tuple[bool, str]:
        """
        Check USD exposure (commodities are typically priced in USD).
        
        Args:
            commodity: Commodity symbol
            proposed_position_value: Value of proposed position
            current_positions: Current open positions
        
        Returns:
            (is_safe, message)
        """
        if current_positions is None:
            current_positions = self.current_positions
        
        # All commodities in our config are USD-denominated
        # This check is for non-USD denominated commodities if added later
        commodity_type = self._get_commodity_type(commodity)
        
        # For now, all supported commodities are USD-denominated
        # This method can be extended for non-USD commodities
        return (True, f"{commodity} ({commodity_type.value}) is USD-denominated")
    
    def check_loss_limits(
        self,
        account_balance: float,
        daily_loss: float = None,
        weekly_loss: float = None,
    ) -> Tuple[bool, str]:
        """
        Check if daily/weekly loss limits are exceeded.
        
        Args:
            account_balance: Current account balance
            daily_loss: Current daily loss (uses internal tracking if not provided)
            weekly_loss: Current weekly loss (uses internal tracking if not provided)
        
        Returns:
            (is_within_limits, message)
        """
        if daily_loss is None:
            daily_loss = self.daily_loss
        if weekly_loss is None:
            weekly_loss = self.weekly_loss
        
        daily_loss_percent = (daily_loss / account_balance) * 100 if account_balance > 0 else 0
        weekly_loss_percent = (weekly_loss / account_balance) * 100 if account_balance > 0 else 0
        
        # Check daily limit
        if daily_loss_percent >= self.config.max_daily_loss_percent:
            return (False, f"Daily loss limit exceeded: {daily_loss_percent:.1f}% (max: {self.config.max_daily_loss_percent}%)")
        
        # Check weekly limit
        if weekly_loss_percent >= self.config.max_weekly_loss_percent:
            return (False, f"Weekly loss limit exceeded: {weekly_loss_percent:.1f}% (max: {self.config.max_weekly_loss_percent}%)")
        
        # Warnings
        messages = []
        if daily_loss_percent >= self.config.max_daily_loss_percent * 0.8:
            messages.append(f"Daily loss at {daily_loss_percent:.1f}% (warning threshold)")
        if weekly_loss_percent >= self.config.max_weekly_loss_percent * 0.8:
            messages.append(f"Weekly loss at {weekly_loss_percent:.1f}% (warning threshold)")
        
        if messages:
            return (True, "; ".join(messages))
        
        return (True, "Within loss limits")
    
    def calculate_rr_ratio(
        self,
        entry_price: float,
        sl_price: float,
        tp_price: float,
    ) -> float:
        """
        Calculate risk-reward ratio for a trade.
        
        Args:
            entry_price: Entry price
            sl_price: Stop loss price
            tp_price: Take profit price
        
        Returns:
            Risk-reward ratio
        """
        sl_distance = abs(entry_price - sl_price)
        tp_distance = abs(tp_price - entry_price)
        
        if sl_distance == 0:
            return 0.0
        
        return tp_distance / sl_distance
    
    def validate_trade(
        self,
        commodity: str,
        entry_price: float,
        sl_price: float,
        tp_price: float,
        position_percent: float,
        account_balance: float,
        spot_price: float = None,
        futures_price: float = None,
        days_to_expiry: int = 30,
        current_positions: Dict[str, Dict] = None,
        current_date: datetime = None,
    ) -> Tuple[bool, str]:
        """
        Comprehensive trade validation for commodities.
        
        Args:
            commodity: Commodity symbol
            entry_price: Entry price
            sl_price: Stop loss price
            tp_price: Take profit price
            position_percent: Position as percentage of account
            account_balance: Account balance
            spot_price: Current spot price (for contango check)
            futures_price: Futures price (for contango check)
            days_to_expiry: Days until futures expiry
            current_positions: Current open positions
            current_date: Current date
        
        Returns:
            (is_valid, validation_message)
        """
        # Check if commodity is supported
        if commodity not in self.config.supported_commodities:
            return (False, f"Unsupported commodity: {commodity}")
        
        # Check position limits
        position_ok, position_msg = self.check_position_limits(
            commodity, position_percent, account_balance
        )
        if not position_ok:
            return (position_ok, position_msg)
        
        # Check contango/backwardation if futures data provided
        if spot_price is not None and futures_price is not None:
            contango_ok, contango_msg = self.contango_check(
                commodity, spot_price, futures_price, days_to_expiry
            )
            if not contango_ok:
                return (contango_ok, contango_msg)
        
        # Check seasonality risk
        seasonality_ok, seasonality_msg = self.seasonality_risk_check(
            commodity, current_date
        )
        
        # Check supply/demand events
        supply_ok, supply_msg = self.supply_demand_check(
            commodity, current_date
        )
        if not supply_ok:
            return (supply_ok, supply_msg)
        
        # Check RR ratio
        rr_ratio = self.calculate_rr_ratio(entry_price, sl_price, tp_price)
        if rr_ratio < self.config.min_rr_ratio:
            return (False, f"RR ratio {rr_ratio:.2f} below minimum {self.config.min_rr_ratio}")
        
        # Check loss limits
        limits_ok, limits_msg = self.check_loss_limits(account_balance)
        if not limits_ok:
            return (limits_ok, limits_msg)
        
        # All checks passed
        messages = [position_msg]
        if spot_price is not None and futures_price is not None:
            messages.append(contango_msg)
        messages.append(seasonality_msg)
        messages.append(supply_msg)
        messages.append(limits_msg)
        valid_messages = [msg for msg in messages if msg and msg != "OK"]
        
        return (True, f"Trade validated. {'; '.join(valid_messages)}" if valid_messages else "All checks passed")
    
    def get_position_summary(
        self,
        commodity: str,
        contracts: float,
        entry_price: float,
        sl_price: float,
    ) -> Dict:
        """Get summary of a proposed position."""
        contract_spec = self._get_contract_spec(commodity)
        if contract_spec is None:
            return {"error": f"Unknown commodity: {commodity}"}
        
        contract_value = entry_price * contract_spec["contract_size"]
        sl_distance = abs(entry_price - sl_price)
        
        return {
            "commodity": commodity,
            "contracts": contracts,
            "contract_value": round(contract_value, 2),
            "total_value": round(contracts * contract_value, 2),
            "entry_price": entry_price,
            "sl_price": sl_price,
            "sl_distance": sl_distance,
            "unit": contract_spec["unit"],
            "commodity_type": self._get_commodity_type(commodity).value,
        }
    
    def update_daily_stats(self, pnl: float):
        """Update daily statistics after a trade."""
        self.daily_loss += abs(min(pnl, 0))  # Only track losses
        self.daily_trades += 1
    
    def update_weekly_stats(self, pnl: float):
        """Update weekly statistics after a trade."""
        self.weekly_loss += abs(min(pnl, 0))  # Only track losses
        self.weekly_trades += 1
    
    def reset_daily_stats(self):
        """Reset daily statistics (call at start of trading day)."""
        self.daily_loss = 0.0
        self.daily_trades = 0
    
    def reset_weekly_stats(self):
        """Reset weekly statistics (call at start of trading week)."""
        self.weekly_loss = 0.0
        self.weekly_trades = 0
    
    def add_position(self, commodity: str, contracts: float, entry_price: float, sl_price: float):
        """Add a position to tracking."""
        contract_spec = self._get_contract_spec(commodity)
        if contract_spec is None:
            return
        
        contract_value = entry_price * contract_spec["contract_size"]
        position_value = contracts * contract_value
        
        self.current_positions[commodity.upper()] = {
            "contracts": contracts,
            "contract_value": contract_value,
            "position_value": position_value,
            "entry_price": entry_price,
            "sl_price": sl_price,
        }
    
    def remove_position(self, commodity: str):
        """Remove a position from tracking."""
        commodity_upper = commodity.upper()
        if commodity_upper in self.current_positions:
            del self.current_positions[commodity_upper]
    
    def get_portfolio_summary(self) -> Dict[str, any]:
        """Get summary of current portfolio."""
        total_value = 0.0
        commodity_type_exposure = {}
        
        for commodity, position in self.current_positions.items():
            position_value = position.get("position_value", 0)
            total_value += position_value
            
            # Commodity type exposure
            commodity_type = self._get_commodity_type(commodity)
            if commodity_type not in commodity_type_exposure:
                commodity_type_exposure[commodity_type] = 0.0
            commodity_type_exposure[commodity_type] += position_value
        
        # Convert to percentages
        type_percentages = {}
        for commodity_type, value in commodity_type_exposure.items():
            type_percentages[commodity_type.value] = round((value / total_value) * 100, 2) if total_value > 0 else 0
        
        return {
            "total_value": round(total_value, 2),
            "positions_count": len(self.current_positions),
            "commodity_type_exposure": type_percentages,
        }
