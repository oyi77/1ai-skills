"""
FOREX Risk Management Module

Handles FOREX-specific risk management including pip-based position sizing,
correlation risk, spread checks, and leverage warnings for major currency pairs.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
from enum import Enum


class FOREXPair(Enum):
    """Major FOREX pairs supported."""
    EURUSD = "EUR/USD"
    GBPUSD = "GBP/USD"
    USDJPY = "USD/JPY"
    AUDUSD = "AUD/USD"
    USDCAD = "USD/CAD"
    USDCHF = "USD/CHF"
    NZDUSD = "NZD/USD"
    EURGBP = "EUR/GBP"


@dataclass
class FOREXConfig:
    """FOREX risk management configuration."""
    
    # Risk settings
    risk_per_trade_percent: float = 1.0  # Risk 1-2% per trade
    min_rr_ratio: float = 2.0  # Minimum risk-reward ratio (1:2)
    
    # Position sizing
    pip_value: float = 10.0  # Value of 1 pip per standard lot (for USD pairs)
    standard_lot_size: int = 100000  # Standard lot = 100,000 units
    min_lot_size: float = 0.01
    lot_step: float = 0.01
    
    # Spread limits (in pips)
    max_eurusd_spread: float = 2.0
    max_gbpusd_spread: float = 3.0
    max_usdjpy_spread: float = 3.0
    max_other_spread: float = 4.0
    
    # Correlation limits
    max_correlated_exposure_percent: float = 50.0  # Max 50% in correlated pairs
    
    # Loss limits
    max_daily_loss_percent: float = 3.0  # Max 3% daily loss
    max_weekly_loss_percent: float = 6.0  # Max 6% weekly loss
    
    # Leverage warnings
    leverage_warning_threshold: int = 500  # Warn above 500:1
    max_recommended_leverage: int = 200  # Max recommended leverage
    
    # Supported pairs
    supported_pairs: List[str] = field(default_factory=lambda: [
        "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", 
        "USD/CHF", "NZD/USD", "EUR/GBP"
    ])


class FOREXRiskManager:
    """FOREX-specific risk management."""
    
    # Correlation matrix for major pairs (simplified)
    CORRELATION_MATRIX = {
        "EUR/USD": {"GBP/USD": 0.85, "AUD/USD": 0.65, "USD/JPY": -0.72, "USD/CAD": -0.45},
        "GBP/USD": {"EUR/USD": 0.85, "AUD/USD": 0.70, "USD/JPY": -0.55, "USD/CAD": -0.40},
        "USD/JPY": {"EUR/USD": -0.72, "GBP/USD": -0.55, "USD/CAD": 0.50, "USD/CHF": 0.68},
        "AUD/USD": {"EUR/USD": 0.65, "GBP/USD": 0.70, "USD/CAD": -0.35, "NZD/USD": 0.85},
        "USD/CAD": {"EUR/USD": -0.45, "GBP/USD": -0.40, "USD/JPY": 0.50, "USD/CHF": 0.55},
        "USD/CHF": {"USD/JPY": 0.68, "USD/CAD": 0.55, "EUR/USD": -0.68, "GBP/USD": -0.55},
        "NZD/USD": {"AUD/USD": 0.85, "EUR/USD": 0.55, "GBP/USD": 0.60},
        "EUR/GBP": {"EUR/USD": 0.45, "GBP/USD": 0.55, "USD/JPY": -0.25},
    }
    
    def __init__(self, config: Optional[FOREXConfig] = None):
        self.config = config or FOREXConfig()
        self.daily_loss = 0.0
        self.weekly_loss = 0.0
        self.daily_trades = 0
        self.weekly_trades = 0
        self.current_positions: Dict[str, Dict] = {}
    
    def calculate_pip_based_position_size(
        self,
        account_balance: float,
        entry_price: float,
        sl_price: float,
        pair: str,
        risk_percent: float = None,
    ) -> Dict[str, float]:
        """
        Calculate position size using pip-based method (FOREX-specific).
        
        Args:
            account_balance: Total account balance
            entry_price: Entry price
            sl_price: Stop loss price
            pair: Currency pair (e.g., "EUR/USD")
            risk_percent: Risk percentage (default from config)
        
        Returns:
            Dict with lot_size, risk_amount, sl_pips, etc.
        """
        if risk_percent is None:
            risk_percent = self.config.risk_per_trade_percent
        
        # Calculate SL distance in pips
        sl_pips = self._calculate_pip_distance(entry_price, sl_price, pair)
        
        if sl_pips == 0:
            return {
                "lot_size": self.config.min_lot_size,
                "risk_amount": 0.0,
                "sl_pips": 0,
                "error": "Zero SL distance"
            }
        
        # Calculate risk amount in account currency
        risk_amount = account_balance * (risk_percent / 100)
        
        # Calculate pip value for the pair
        pip_value = self._get_pip_value(pair, account_balance)
        
        # Position size = Risk amount / (SL pips * pip value per lot)
        # For standard lot: risk = lots * sl_pips * pip_value
        lots_by_risk = risk_amount / (sl_pips * pip_value)
        
        # Round to lot step
        lot_size = round(lots_by_risk / self.config.lot_step) * self.config.lot_step
        lot_size = max(lot_size, self.config.min_lot_size)
        
        # Calculate actual risk
        actual_risk = lot_size * sl_pips * pip_value
        
        return {
            "lot_size": lot_size,
            "risk_amount": round(actual_risk, 2),
            "sl_pips": sl_pips,
            "risk_percent": risk_percent,
            "pip_value": pip_value,
            "entry_price": entry_price,
            "sl_price": sl_price,
        }
    
    def _calculate_pip_distance(self, entry_price: float, sl_price: float, pair: str) -> float:
        """Calculate stop loss distance in pips."""
        if pair == "USD/JPY":
            # JPY pairs: 1 pip = 0.01
            return abs(entry_price - sl_price) / 0.01
        else:
            # Other pairs: 1 pip = 0.0001
            return abs(entry_price - sl_price) / 0.0001
    
    def _get_pip_value(self, pair: str, account_balance: float) -> float:
        """
        Get pip value per standard lot for a currency pair.
        
        For USD pairs: ~$10 per pip per standard lot
        For non-USD pairs: more complex calculation needed
        """
        if pair.endswith("/USD"):
            # Direct USD pairs: pip value is constant
            return self.config.pip_value
        elif pair.startswith("USD/"):
            # Inverse USD pairs: pip value varies with price
            base_pair = pair.split("/")[1]  # e.g., "JPY" from "USD/JPY"
            # Simplified: assume pip value around $8-10 for inverse pairs
            return self.config.pip_value * 0.85
        else:
            # Cross pairs: more complex, use average
            return self.config.pip_value * 0.90
    
    def check_correlation_risk(
        self,
        pair: str,
        proposed_lot_size: float,
        current_positions: Dict[str, Dict] = None,
    ) -> Tuple[bool, str]:
        """
        Check correlation risk for proposed trade.
        
        Args:
            pair: Currency pair to trade
            proposed_lot_size: Proposed position size in lots
            current_positions: Current open positions
        
        Returns:
            (is_safe, warning_message)
        """
        if current_positions is None:
            current_positions = self.current_positions
        
        if not current_positions:
            return (True, "No correlated positions")
        
        # Calculate total exposure for correlated pairs
        correlated_exposure = 0.0
        correlated_pairs = []
        
        for existing_pair, position in current_positions.items():
            if existing_pair == pair:
                continue
            
            correlation = self._get_correlation(pair, existing_pair)
            if abs(correlation) >= 0.7:  # Significant correlation
                exposure = position.get("lot_size", 0) * abs(correlation)
                correlated_exposure += exposure
                correlated_pairs.append((existing_pair, exposure, correlation))
        
        # Calculate proposed exposure as percentage
        total_exposure = proposed_lot_size + correlated_exposure
        if total_exposure > 0:
            proposed_percent = (proposed_lot_size / total_exposure) * 100
        else:
            proposed_percent = 100.0
        
        # Check against limits
        max_correlated = self.config.max_correlated_exposure_percent
        
        if proposed_percent > max_correlated:
            return (False, f"Correlation risk: {pair} would be {proposed_percent:.1f}% of total correlated exposure (max: {max_correlated}%)")
        
        # Generate warning if correlated exposure is high
        if correlated_pairs:
            warning_parts = [f"Correlated pairs: "]
            for cp, exposure, corr in correlated_pairs:
                warning_parts.append(f"{cp} ({exposure:.2f} lots, {corr:.2f} correlation)")
            
            return (True, " ".join(warning_parts))
        
        return (True, "Correlation risk acceptable")
    
    def _get_correlation(self, pair1: str, pair2: str) -> float:
        """Get correlation coefficient between two pairs."""
        if pair1 not in self.CORRELATION_MATRIX:
            return 0.0
        
        correlations = self.CORRELATION_MATRIX[pair1]
        return correlations.get(pair2, 0.0)
    
    def check_spread(self, pair: str, current_spread: float) -> Tuple[bool, str]:
        """
        Check if spread is acceptable for trading.
        
        Args:
            pair: Currency pair
            current_spread: Current spread in pips
        
        Returns:
            (is_acceptable, message)
        """
        max_spread = self._get_max_spread(pair)
        
        if current_spread > max_spread:
            return (False, f"Spread {current_spread:.1f} pips exceeds max {max_spread} for {pair}")
        
        if current_spread > max_spread * 0.8:
            return (True, f"Warning: Spread {current_spread:.1f} pips is high (max: {max_spread})")
        
        return (True, f"Spread {current_spread:.1f} pips is acceptable")
    
    def _get_max_spread(self, pair: str) -> float:
        """Get maximum allowed spread for a pair."""
        spread_limits = {
            "EUR/USD": self.config.max_eurusd_spread,
            "GBP/USD": self.config.max_gbpusd_spread,
            "USD/JPY": self.config.max_usdjpy_spread,
        }
        return spread_limits.get(pair, self.config.max_other_spread)
    
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
    
    def check_leverage_warning(self, leverage: int) -> Tuple[bool, str]:
        """
        Check leverage and provide warnings.
        
        Args:
            leverage: Account leverage ratio
        
        Returns:
            (is_safe, warning_message)
        """
        if leverage > self.config.leverage_warning_threshold:
            return (False, f"High leverage warning: {leverage}:1 exceeds threshold {self.config.leverage_warning_threshold}:1")
        
        if leverage > self.config.max_recommended_leverage:
            return (True, f"Leverage {leverage}:1 exceeds recommended {self.config.max_recommended_leverage}:1 - trade with caution")
        
        return (True, f"Leverage {leverage}:1 is acceptable")
    
    def calculate_rr_ratio(
        self,
        entry_price: float,
        sl_price: float,
        tp_price: float,
        pair: str,
    ) -> float:
        """
        Calculate risk-reward ratio for a trade.
        
        Args:
            entry_price: Entry price
            sl_price: Stop loss price
            tp_price: Take profit price
            pair: Currency pair
        
        Returns:
            Risk-reward ratio
        """
        sl_pips = self._calculate_pip_distance(entry_price, sl_price, pair)
        tp_pips = self._calculate_pip_distance(entry_price, tp_price, pair)
        
        if sl_pips == 0:
            return 0.0
        
        return tp_pips / sl_pips
    
    def validate_trade(
        self,
        pair: str,
        entry_price: float,
        sl_price: float,
        tp_price: float,
        lot_size: float,
        spread: float,
        account_balance: float,
        leverage: int,
        current_positions: Dict[str, Dict] = None,
    ) -> Tuple[bool, str]:
        """
        Comprehensive trade validation for FOREX.
        
        Args:
            pair: Currency pair
            entry_price: Entry price
            sl_price: Stop loss price
            tp_price: Take profit price
            lot_size: Position size in lots
            spread: Current spread in pips
            account_balance: Account balance
            leverage: Account leverage
            current_positions: Current open positions
        
        Returns:
            (is_valid, validation_message)
        """
        # Check if pair is supported
        if pair not in self.config.supported_pairs:
            return (False, f"Unsupported pair: {pair}")
        
        # Check spread
        spread_ok, spread_msg = self.check_spread(pair, spread)
        if not spread_ok:
            return (spread_ok, spread_msg)
        
        # Check RR ratio
        rr_ratio = self.calculate_rr_ratio(entry_price, sl_price, tp_price, pair)
        if rr_ratio < self.config.min_rr_ratio:
            return (False, f"RR ratio {rr_ratio:.2f} below minimum {self.config.min_rr_ratio}")
        
        # Check correlation risk
        corr_ok, corr_msg = self.check_correlation_risk(pair, lot_size, current_positions)
        if not corr_ok:
            return (corr_ok, corr_msg)
        
        # Check loss limits
        limits_ok, limits_msg = self.check_loss_limits(account_balance)
        if not limits_ok:
            return (limits_ok, limits_msg)
        
        # Check leverage
        lev_ok, lev_msg = self.check_leverage_warning(leverage)
        if not lev_ok:
            return (lev_ok, lev_msg)
        
        # All checks passed
        messages = [spread_msg, corr_msg, limits_msg, lev_msg]
        valid_messages = [msg for msg in messages if msg and msg != "OK"]
        
        return (True, f"Trade validated. {'; '.join(valid_messages)}" if valid_messages else "All checks passed")
    
    def get_position_summary(self, pair: str, lot_size: float, entry_price: float, sl_price: float) -> Dict:
        """Get summary of a proposed position."""
        sl_pips = self._calculate_pip_distance(entry_price, sl_price, pair)
        pip_value = self._get_pip_value(pair, 10000)  # Assume $10k account for calculation
        
        return {
            "pair": pair,
            "lot_size": lot_size,
            "entry_price": entry_price,
            "sl_price": sl_price,
            "sl_pips": sl_pips,
            "pip_value_estimate": pip_value,
            "risk_per_pip": lot_size * pip_value,
            "total_risk": lot_size * sl_pips * pip_value,
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
    
    def add_position(self, pair: str, lot_size: float, entry_price: float, sl_price: float):
        """Add a position to tracking."""
        self.current_positions[pair] = {
            "lot_size": lot_size,
            "entry_price": entry_price,
            "sl_price": sl_price,
        }
    
    def remove_position(self, pair: str):
        """Remove a position from tracking."""
        if pair in self.current_positions:
            del self.current_positions[pair]
    
    def get_total_exposure(self) -> Dict[str, float]:
        """Get total exposure across all positions."""
        total_lots = sum(pos["lot_size"] for pos in self.current_positions.values())
        
        # Group by USD exposure
        usd_pairs = ["EUR/USD", "GBP/USD", "AUD/USD", "NZD/USD"]
        jpy_pairs = ["USD/JPY"]
        other_pairs = ["USD/CAD", "USD/CHF", "EUR/GBP"]
        
        usd_exposure = sum(
            self.current_positions[p]["lot_size"] 
            for p in usd_pairs if p in self.current_positions
        )
        jpy_exposure = sum(
            self.current_positions[p]["lot_size"] 
            for p in jpy_pairs if p in self.current_positions
        )
        
        return {
            "total_lots": total_lots,
            "usd_pairs_exposure": usd_exposure,
            "jpy_pairs_exposure": jpy_exposure,
            "positions_count": len(self.current_positions),
        }
