"""
Risk Management Module

Handles position sizing, SL/TP calculations, and risk validation.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class RiskConfig:
    """Risk management configuration."""

    risk_mode: str = "fixed_risk_percent"  # "fixed_lot" or "fixed_risk_percent"
    fixed_lot: float = 0.01
    risk_percent: float = 1.0  # Risk 1% of account per trade
    rr_ratio: float = 2.0  # Risk:Reward ratio
    leverage: int = 200  # Account leverage (e.g., 200, 500, 1000, 2000)
    max_spread_points: float = 30.0
    max_drawdown_percent: float = 10.0
    max_daily_trades: int = 1


class RiskManager:
    """Risk management for trading."""

    def __init__(self, config: Optional[RiskConfig] = None):
        self.config = config or RiskConfig()

    def calculate_position_size(
        self,
        account_balance: float,
        risk_percent: float,
        entry_price: float,
        sl_price: float,
        point_value: float = 0.01,
    ) -> float:
        """
        Calculate position size based on risk percent.

        Args:
            account_balance: Total account balance
            risk_percent: Percentage of account to risk (e.g., 1.0 for 1%)
            entry_price: Entry price
            sl_price: Stop loss price
            point_value: Value of one point (pip) for the symbol

        Returns:
            Position size in lots
        """
        risk_amount = account_balance * (risk_percent / 100)

        # Calculate SL in points
        sl_distance = abs(entry_price - sl_price)

        if sl_distance == 0:
            return self.config.fixed_lot

        # Points = SL distance / point value
        sl_points = sl_distance / point_value

        # Position size = Risk amount / (SL points * point value)
        # But since we're working with lots:
        # Risk amount = lots * SL points * point value * 100 (for standard lots)
        # Actually for MT5: Risk = lots * SL_points * contract_size * point

        # Simplified: position size = risk_amount / (sl_points * point_value * 10)
        # This assumes standard lot and varies by broker

        # More accurate: Use broker's contract size (usually 100000 for forex)
        contract_size = 100000  # Standard lot

        position_size = risk_amount / (sl_points * point_value * contract_size)

        # Round to broker's lot step (usually 0.01)
        position_size = round(position_size, 2)

        # Ensure minimum lot size
        position_size = max(position_size, 0.01)

        return position_size

    def calculate_lot_size(
        self,
        account_balance: float,
        entry_price: float,
        sl_price: float,
        risk_percent: float = None,
        leverage: int = None,
        point_value: float = 0.01,
    ) -> Dict[str, float]:
        """
        Calculate lot size with leverage support.

        Args:
            account_balance: Account balance in USD
            entry_price: Entry price
            sl_price: Stop loss price
            risk_percent: Risk percentage (default from config)
            leverage: Account leverage (default from config)
            point_value: Point value for the symbol

        Returns:
            Dict with lot_size, risk_amount, max_lot, margin_required
        """
        if risk_percent is None:
            risk_percent = self.config.risk_percent
        if leverage is None:
            leverage = self.config.leverage

        # Calculate risk amount
        risk_amount = account_balance * (risk_percent / 100)

        # Calculate SL distance in points
        sl_distance = abs(entry_price - sl_price)
        sl_points = sl_distance / point_value if point_value > 0 else 0

        # For XAUUSD: 1 lot = 100 oz
        # Point value: 1 point = $1 per 1 lot = $0.01 per 0.01 lot
        # Risk = lot_size * sl_points * point_value * 100 (for 1 lot = 100 oz)
        # Simplified: Risk = lot_size * sl_points * point_value
        if sl_points > 0 and point_value > 0:
            lot_by_risk = risk_amount / (sl_points * point_value)
        else:
            lot_by_risk = self.config.fixed_lot

        # Calculate max lot by leverage
        # Max position = account_balance * leverage
        # For XAUUSD: 1 lot = 100 oz, value = entry_price * 100
        contract_size = 100
        max_position = account_balance * leverage
        max_lot = max_position / (entry_price * contract_size)

        # Use the smaller of the two
        lot_size = min(lot_by_risk, max_lot)

        # Round to broker's lot step (0.01)
        lot_size = round(lot_size, 2)
        lot_size = max(lot_size, 0.01)  # Minimum

        # Calculate actual margin required
        margin_per_lot = entry_price * contract_size / leverage
        margin_required = lot_size * margin_per_lot

        return {
            "lot_size": lot_size,
            "risk_amount": risk_amount,
            "max_lot": round(max_lot, 2),
            "margin_required": round(margin_required, 2),
            "sl_points": sl_points,
        }

    def get_max_lot(
        self,
        account_balance: float,
        entry_price: float,
        leverage: int = None,
    ) -> float:
        """Get maximum lot size based on leverage."""
        if leverage is None:
            leverage = self.config.leverage

        contract_size = 100  # 100 oz per lot for gold
        max_position = account_balance * leverage
        max_lot = max_position / (entry_price * contract_size)

        return round(max_lot, 2)

    def calculate_sl_tp(
        self,
        entry_price: float,
        order_type: str,
        r_points: float,
        rr_ratio: float = None,
    ) -> tuple:
        """
        Calculate SL and TP based on R (range) and risk-reward ratio.

        Args:
            entry_price: Entry price
            order_type: "BUY" or "SELL"
            r_points: Range in points (SL distance)
            rr_ratio: Risk-reward ratio (default from config)

        Returns:
            (sl_price, tp_price)
        """
        if rr_ratio is None:
            rr_ratio = self.config.rr_ratio

        if order_type.upper() == "BUY":
            sl = entry_price - r_points
            tp = entry_price + (r_points * rr_ratio)
        else:  # SELL
            sl = entry_price + r_points
            tp = entry_price - (r_points * rr_ratio)

        return (sl, tp)

    def points_to_price(
        self,
        points: float,
        entry_price: float,
        order_type: str,
        point_value: float = 0.01,
    ) -> float:
        """Convert points to price."""
        if order_type.upper() == "BUY":
            return entry_price + (points * point_value)
        else:
            return entry_price - (points * point_value)

    def price_to_points(
        self, price1: float, price2: float, point_value: float = 0.01
    ) -> float:
        """Convert price difference to points."""
        return abs(price1 - price2) / point_value

    def validate_trade(
        self,
        spread: float,
        account_balance: float,
        current_drawdown: float = 0.0,
        daily_trades: int = 0,
    ) -> tuple:
        """
        Validate if trade passes risk checks.

        Returns:
            (is_valid, reason)
        """
        # Check spread
        if spread > self.config.max_spread_points:
            return (
                False,
                f"Spread {spread} exceeds max {self.config.max_spread_points}",
            )

        # Check drawdown
        if current_drawdown > self.config.max_drawdown_percent:
            return (
                False,
                f"Drawdown {current_drawdown}% exceeds max {self.config.max_drawdown_percent}%",
            )

        # Check daily trade limit
        if daily_trades >= self.config.max_daily_trades:
            return (False, f"Daily trade limit reached ({daily_trades})")

        return (True, "OK")

    def get_guardrail_summary(self, params: Dict[str, Any]) -> str:
        """Generate a human-readable guardrail summary."""
        return f"""
=== Trade Guardrail Summary ===
Symbol: {params.get("symbol", "N/A")}
Order Type: {params.get("order_type", "N/A")}
Entry Price: {params.get("entry_price", "N/A")}
Stop Loss: {params.get("sl", "N/A")}
Take Profit: {params.get("tp", "N/A")}
Risk Amount: {params.get("risk_percent", self.config.risk_percent)}%
RR Ratio: {self.config.rr_ratio}
Max Spread: {self.config.max_spread_points}
Max Daily Trades: {self.config.max_daily_trades}
=============================="""
