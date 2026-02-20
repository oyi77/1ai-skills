"""
CRYPTO Risk Management Module

Handles CRYPTO-specific risk management including volatility-adjusted position sizing,
wider stop losses, leverage limits per volatility regime, and liquidation prevention
for major cryptocurrency pairs.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
from enum import Enum


class CryptoPair(Enum):
    """Major cryptocurrency pairs supported."""
    BTCUSD = "BTC/USD"
    ETHUSD = "ETH/USD"


class VolatilityRegime(Enum):
    """Market volatility regimes for crypto."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


@dataclass
class CryptoConfig:
    """CRYPTO risk management configuration."""
    
    # Risk settings - more conservative than FOREX
    risk_per_trade_percent: float = 0.5  # Risk 0.5-1% per trade (lower than FOREX)
    min_rr_ratio: float = 2.0  # Minimum risk-reward ratio (1:2)
    
    # Position sizing
    min_position_size_percent: float = 0.01  # Min 1% of account
    max_position_size_percent: float = 0.25  # Max 25% of account per trade
    position_step: float = 0.01  # Position size increment
    
    # Stop loss multipliers (1.5-2x wider than traditional)
    base_stop_percent: float = 0.02  # Base 2% stop loss
    stop_multiplier_low_vol: float = 1.5  # 1.5x for low volatility
    stop_multiplier_high_vol: float = 2.0  # 2x for high volatility
    stop_multiplier_extreme_vol: float = 2.5  # 2.5x for extreme volatility
    
    # Leverage limits per volatility regime
    max_leverage_low_vol: int = 100  # Max 100x in low volatility
    max_leverage_medium_vol: int = 50  # Max 50x in medium volatility
    max_leverage_high_vol: int = 25  # Max 25x in high volatility
    max_leverage_extreme_vol: int = 10  # Max 10x in extreme volatility
    liquidation_prevention_max_leverage: int = 2  # Max 2x leverage for liquidation prevention
    
    # Loss limits - lower than FOREX
    max_daily_loss_percent: float = 2.0  # Max 2% daily loss (lower than FOREX's 3%)
    max_weekly_loss_percent: float = 4.0  # Max 4% weekly loss (lower than FOREX's 6%)
    
    # Volatility thresholds (annualized volatility %)
    vol_threshold_low: float = 0.30  # < 30% annual vol = low
    vol_threshold_medium: float = 0.60  # 30-60% annual vol = medium
    vol_threshold_high: float = 1.00  # 60-100% annual vol = high
    vol_threshold_extreme: float = 1.00  # > 100% annual vol = extreme
    
    # Supported pairs
    supported_pairs: List[str] = field(default_factory=lambda: ["BTC/USD", "ETH/USD"])
    
    # Volatility lookback period (days)
    vol_lookback_days: int = 30


class CRYPTORiskManager:
    """CRYPTO-specific risk management."""
    
    # Typical volatility ranges for major crypto pairs (annualized)
    VOLATILITY_RANGES = {
        "BTC/USD": {"low": 0.40, "medium": 0.70, "high": 1.00, "extreme": 1.50},
        "ETH/USD": {"low": 0.50, "medium": 0.80, "high": 1.20, "extreme": 1.80},
    }
    
    def __init__(self, config: Optional[CryptoConfig] = None):
        self.config = config or CryptoConfig()
        self.daily_loss = 0.0
        self.weekly_loss = 0.0
        self.daily_trades = 0
        self.weekly_trades = 0
        self.current_positions: Dict[str, Dict] = {}
        self.volatility_cache: Dict[str, float] = {}
    
    def calculate_volatility_adjusted_position_size(
        self,
        account_balance: float,
        entry_price: float,
        sl_price: float,
        pair: str,
        current_volatility: float = None,
        risk_percent: float = None,
    ) -> Dict[str, float]:
        """
        Calculate position size adjusted for crypto volatility.
        
        Args:
            account_balance: Total account balance
            entry_price: Entry price
            sl_price: Stop loss price
            pair: Cryptocurrency pair (e.g., "BTC/USD")
            current_volatility: Current annualized volatility (calculated if not provided)
            risk_percent: Risk percentage (default from config)
        
        Returns:
            Dict with position_size_percent, risk_amount, sl_percent, etc.
        """
        if risk_percent is None:
            risk_percent = self.config.risk_per_trade_percent
        
        # Calculate SL distance as percentage
        sl_percent = abs(entry_price - sl_price) / entry_price
        
        if sl_percent == 0:
            return {
                "position_size_percent": self.config.min_position_size_percent,
                "risk_amount": 0.0,
                "sl_percent": 0,
                "error": "Zero SL distance"
            }
        
        # Determine volatility regime
        if current_volatility is None:
            current_volatility = self._get_typical_volatility(pair)
        
        regime = self._get_volatility_regime(current_volatility)
        
        # Adjust stop loss for volatility (wider stops for crypto)
        adjusted_sl_percent = sl_percent * self._get_stop_multiplier(regime)
        
        # Calculate risk amount in account currency
        risk_amount = account_balance * (risk_percent / 100)
        
        # Position size = Risk amount / (SL percentage * entry price)
        # This gives us the dollar amount to risk
        risk_per_unit = entry_price * adjusted_sl_percent
        position_value = risk_amount / adjusted_sl_percent if adjusted_sl_percent > 0 else 0
        position_size_percent = position_value / account_balance if account_balance > 0 else 0
        
        # Round to position step
        position_size_percent = round(position_size_percent / self.config.position_step) * self.config.position_step
        position_size_percent = max(position_size_percent, self.config.min_position_size_percent)
        position_size_percent = min(position_size_percent, self.config.max_position_size_percent)
        
        # Calculate actual risk
        actual_risk = position_size_percent * account_balance
        
        return {
            "position_size_percent": round(position_size_percent, 4),
            "risk_amount": round(actual_risk, 2),
            "sl_percent": round(adjusted_sl_percent, 4),
            "sl_price": sl_price,
            "risk_percent": risk_percent,
            "volatility": current_volatility,
            "regime": regime.value,
            "entry_price": entry_price,
        }
    
    def _get_stop_multiplier(self, regime: VolatilityRegime) -> float:
        """Get stop loss multiplier based on volatility regime."""
        multipliers = {
            VolatilityRegime.LOW: self.config.stop_multiplier_low_vol,
            VolatilityRegime.MEDIUM: 1.0,  # Base multiplier
            VolatilityRegime.HIGH: self.config.stop_multiplier_high_vol,
            VolatilityRegime.EXTREME: self.config.stop_multiplier_extreme_vol,
        }
        return multipliers.get(regime, 1.0)
    
    def _get_volatility_regime(self, volatility: float) -> VolatilityRegime:
        """Determine volatility regime from annualized volatility."""
        if volatility < self.config.vol_threshold_low:
            return VolatilityRegime.LOW
        elif volatility < self.config.vol_threshold_medium:
            return VolatilityRegime.MEDIUM
        elif volatility < self.config.vol_threshold_high:
            return VolatilityRegime.HIGH
        else:
            return VolatilityRegime.EXTREME
    
    def _get_typical_volatility(self, pair: str) -> float:
        """Get typical volatility for a pair (from cache or defaults)."""
        if pair in self.volatility_cache:
            return self.volatility_cache[pair]
        
        if pair in self.VOLATILITY_RANGES:
            # Use medium volatility as default
            typical_vol = self.VOLATILITY_RANGES[pair]["medium"]
            self.volatility_cache[pair] = typical_vol
            return typical_vol
        
        return 0.70  # Default to medium volatility
    
    def check_leverage_limits(
        self,
        leverage: int,
        pair: str,
        current_volatility: float = None,
    ) -> Tuple[bool, str]:
        """
        Check leverage limits based on volatility regime.
        
        Args:
            leverage: Proposed leverage ratio
            pair: Cryptocurrency pair
            current_volatility: Current annualized volatility
        
        Returns:
            (is_safe, warning_message)
        """
        if current_volatility is None:
            current_volatility = self._get_typical_volatility(pair)
        
        regime = self._get_volatility_regime(current_volatility)
        
        # Get max leverage for this regime
        max_leverage = self._get_max_leverage_for_regime(regime)
        
        # Check liquidation prevention (max 50% leverage in high vol = max 2x)
        if regime in [VolatilityRegime.HIGH, VolatilityRegime.EXTREME]:
            if leverage > self.config.liquidation_prevention_max_leverage:
                return (False, f"Liquidation prevention: {leverage}x leverage exceeds max {self.config.liquidation_prevention_max_leverage}x for {regime.value} volatility")
        
        # Check regime-specific limits
        if leverage > max_leverage:
            return (False, f"Leverage {leverage}x exceeds max {max_leverage}x for {regime.value} volatility regime")
        
        # Warning if approaching limit
        if leverage > max_leverage * 0.8:
            return (True, f"Warning: {leverage}x leverage is {leverage/max_leverage*100:.0f}% of max {max_leverage}x for {regime.value} volatility")
        
        return (True, f"Leverage {leverage}x is acceptable for {regime.value} volatility")
    
    def _get_max_leverage_for_regime(self, regime: VolatilityRegime) -> int:
        """Get maximum leverage for a volatility regime."""
        leverage_limits = {
            VolatilityRegime.LOW: self.config.max_leverage_low_vol,
            VolatilityRegime.MEDIUM: self.config.max_leverage_medium_vol,
            VolatilityRegime.HIGH: self.config.max_leverage_high_vol,
            VolatilityRegime.EXTREME: self.config.max_leverage_extreme_vol,
        }
        return leverage_limits.get(regime, self.config.max_leverage_medium_vol)
    
    def check_loss_limits(
        self,
        account_balance: float,
        daily_loss: float = None,
        weekly_loss: float = None,
    ) -> Tuple[bool, str]:
        """
        Check if daily/weekly loss limits are exceeded (lower limits than FOREX).
        
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
        
        # Check daily limit (lower than FOREX)
        if daily_loss_percent >= self.config.max_daily_loss_percent:
            return (False, f"Daily loss limit exceeded: {daily_loss_percent:.1f}% (max: {self.config.max_daily_loss_percent}%)")
        
        # Check weekly limit (lower than FOREX)
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
        pair: str,
    ) -> float:
        """
        Calculate risk-reward ratio for a crypto trade.
        
        Args:
            entry_price: Entry price
            sl_price: Stop loss price
            tp_price: Take profit price
            pair: Cryptocurrency pair
        
        Returns:
            Risk-reward ratio
        """
        sl_percent = abs(entry_price - sl_price) / entry_price
        tp_percent = abs(tp_price - entry_price) / entry_price
        
        if sl_percent == 0:
            return 0.0
        
        return tp_percent / sl_percent
    
    def validate_trade(
        self,
        pair: str,
        entry_price: float,
        sl_price: float,
        tp_price: float,
        position_size_percent: float,
        leverage: int,
        account_balance: float,
        current_volatility: float = None,
        current_positions: Dict[str, Dict] = None,
    ) -> Tuple[bool, str]:
        """
        Comprehensive trade validation for CRYPTO.
        
        Args:
            pair: Cryptocurrency pair
            entry_price: Entry price
            sl_price: Stop loss price
            tp_price: Take profit price
            position_size_percent: Position size as percentage of account
            leverage: Account leverage
            account_balance: Account balance
            current_volatility: Current annualized volatility
            current_positions: Current open positions
        
        Returns:
            (is_valid, validation_message)
        """
        # Check if pair is supported
        if pair not in self.config.supported_pairs:
            return (False, f"Unsupported pair: {pair}")
        
        # Check position size limits
        if position_size_percent > self.config.max_position_size_percent:
            return (False, f"Position size {position_size_percent*100:.1f}% exceeds max {self.config.max_position_size_percent*100:.1f}%")
        
        # Check RR ratio
        rr_ratio = self.calculate_rr_ratio(entry_price, sl_price, tp_price, pair)
        if rr_ratio < self.config.min_rr_ratio:
            return (False, f"RR ratio {rr_ratio:.2f} below minimum {self.config.min_rr_ratio}")
        
        # Check leverage limits
        lev_ok, lev_msg = self.check_leverage_limits(leverage, pair, current_volatility)
        if not lev_ok:
            return (lev_ok, lev_msg)
        
        # Check loss limits
        limits_ok, limits_msg = self.check_loss_limits(account_balance)
        if not limits_ok:
            return (limits_ok, limits_msg)
        
        # All checks passed
        messages = [lev_msg, limits_msg]
        valid_messages = [msg for msg in messages if msg and msg != "OK"]
        
        return (True, f"Trade validated. {'; '.join(valid_messages)}" if valid_messages else "All checks passed")
    
    def get_position_summary(
        self,
        pair: str,
        position_size_percent: float,
        entry_price: float,
        sl_price: float,
        account_balance: float,
    ) -> Dict:
        """Get summary of a proposed crypto position."""
        sl_percent = abs(entry_price - sl_price) / entry_price
        
        return {
            "pair": pair,
            "position_size_percent": round(position_size_percent, 4),
            "entry_price": entry_price,
            "sl_price": sl_price,
            "sl_percent": round(sl_percent, 4),
            "position_value": position_size_percent * account_balance,
            "risk_amount": position_size_percent * sl_percent * account_balance,
            "volatility_regime": self._get_volatility_regime(
                self._get_typical_volatility(pair)
            ).value,
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
    
    def add_position(self, pair: str, position_size_percent: float, entry_price: float, sl_price: float):
        """Add a position to tracking."""
        self.current_positions[pair] = {
            "position_size_percent": position_size_percent,
            "entry_price": entry_price,
            "sl_price": sl_price,
        }
    
    def remove_position(self, pair: str):
        """Remove a position from tracking."""
        if pair in self.current_positions:
            del self.current_positions[pair]
    
    def get_total_exposure(self) -> Dict[str, float]:
        """Get total exposure across all crypto positions."""
        total_value = sum(
            pos["position_size_percent"] * 100  # Convert to percentage
            for pos in self.current_positions.values()
        )
        
        # Group by major pairs
        btc_exposure = 0.0
        eth_exposure = 0.0
        
        if "BTC/USD" in self.current_positions:
            btc_exposure = self.current_positions["BTC/USD"]["position_size_percent"] * 100
        if "ETH/USD" in self.current_positions:
            eth_exposure = self.current_positions["ETH/USD"]["position_size_percent"] * 100
        
        return {
            "total_exposure_percent": round(total_value, 2),
            "btc_usd_exposure": round(btc_exposure, 2),
            "eth_usd_exposure": round(eth_exposure, 2),
            "positions_count": len(self.current_positions),
        }
    
    def update_volatility(self, pair: str, volatility: float):
        """Update cached volatility for a pair."""
        self.volatility_cache[pair] = volatility
    
    def get_volatility_regime_info(self, pair: str) -> Dict:
        """Get volatility regime information for a pair."""
        volatility = self._get_typical_volatility(pair)
        regime = self._get_volatility_regime(volatility)
        max_leverage = self._get_max_leverage_for_regime(regime)
        
        return {
            "pair": pair,
            "volatility": volatility,
            "regime": regime.value,
            "max_leverage": max_leverage,
            "stop_multiplier": self._get_stop_multiplier(regime),
        }
