"""
Funding Rate Data Module

Handles funding rate data fetching, persistence calculation, and 
crowded positioning signal detection for CRYPTO strategies.

Funding Rate Concepts:
- Positive funding = longs pay shorts (bullish sentiment)
- Negative funding = shorts pay longs (bearish sentiment)
- 14+ consecutive days elevated = crowded positioning warning
- Extreme readings (>5-6% annualized) indicate crowded positioning
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class FundingRate:
    """Represents a single funding rate observation."""
    symbol: str
    rate: float  # Funding rate as decimal (e.g., 0.001 = 0.1%)
    timestamp: datetime
    annualized_rate: float  # Annualized rate for comparison
    
    def is_elevated(self, threshold: float = 0.0005) -> bool:
        """Check if funding rate is elevated (above threshold)."""
        return abs(self.rate) > threshold
    
    def is_extreme(self, threshold: float = 0.0005) -> bool:
        """Check if funding rate is extreme (>5-6% annualized)."""
        return abs(self.annualized_rate) > threshold


@dataclass
class PersistenceData:
    """Represents funding rate persistence analysis."""
    symbol: str
    consecutive_days_elevated: int
    current_funding_rate: float
    direction: str  # "positive" or "negative"
    is_warning: bool  # True if 14+ consecutive days
    severity: str  # "low", "medium", "high", "extreme"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "symbol": self.symbol,
            "consecutive_days_elevated": self.consecutive_days_elevated,
            "current_funding_rate": self.current_funding_rate,
            "direction": self.direction,
            "is_warning": self.is_warning,
            "severity": self.severity,
            "timestamp": datetime.now().isoformat()
        }


class FundingRateData:
    """
    Handles funding rate data for crypto trading strategies.
    
    Supports:
    - Major pairs: BTC/USD, ETH/USD
    - Funding rate persistence calculation
    - Crowded positioning signal detection
    - 14+ consecutive days elevated = reversal warning
    """
    
    # Supported trading pairs
    SUPPORTED_PAIRS = ["BTC/USD", "ETH/USD"]
    
    # Thresholds
    ELEVATED_THRESHOLD = 0.0005  # 0.05% per funding period
    EXTREME_THRESHOLD = 0.0005   # >5-6% annualized
    PERSISTENCE_WARNING_DAYS = 14
    
    def __init__(self, base_path: str = "./trading_data"):
        """
        Initialize funding rate data module.
        
        Args:
            base_path: Base path for data storage
        """
        self.base_path = Path(base_path)
        self.funding_path = self.base_path / "funding"
        self._ensure_directories()
        
        # In-memory cache for funding rates
        self._funding_cache: Dict[str, List[FundingRate]] = {}
        
    def _ensure_directories(self):
        """Create directories if they don't exist."""
        self.funding_path.mkdir(parents=True, exist_ok=True)
    
    def _get_funding_filename(self, symbol: str) -> Path:
        """Get filename for funding rate data."""
        # Normalize symbol for filename (BTC/USD -> BTC_USD)
        normalized_symbol = symbol.replace("/", "_")
        return self.funding_path / f"funding_{normalized_symbol}.json"
    
    def fetch_funding_rates(self, symbol: str) -> List[FundingRate]:
        """
        Fetch funding rates for a symbol from exchange.
        
        This is a placeholder that would integrate with CCXT or exchange APIs.
        For now, it loads from local storage or returns empty list.
        
        Args:
            symbol: Trading pair (e.g., "BTC/USD", "ETH/USD")
            
        Returns:
            List of FundingRate objects
        """
        if symbol not in self.SUPPORTED_PAIRS:
            raise ValueError(f"Unsupported symbol: {symbol}. Supported: {self.SUPPORTED_PAIRS}")
        
        # Check cache first
        if symbol in self._funding_cache:
            return self._funding_cache[symbol]
        
        # Try to load from storage
        funding_rates = self._load_funding_from_storage(symbol)
        
        if not funding_rates:
            # Return empty list if no data available
            # In production, this would call exchange API
            funding_rates = []
        
        # Cache the results
        self._funding_cache[symbol] = funding_rates
        
        return funding_rates
    
    def _load_funding_from_storage(self, symbol: str) -> List[FundingRate]:
        """Load funding rates from local storage."""
        filepath = self._get_funding_filename(symbol)
        
        if not filepath.exists():
            return []
        
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                
            funding_rates = []
            for item in data:
                funding_rates.append(FundingRate(
                    symbol=item["symbol"],
                    rate=item["rate"],
                    timestamp=datetime.fromisoformat(item["timestamp"]),
                    annualized_rate=item["annualized_rate"]
                ))
                
            return funding_rates
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading funding data for {symbol}: {e}")
            return []
    
    def save_funding_rates(self, symbol: str, funding_rates: List[FundingRate]):
        """
        Save funding rates to local storage.
        
        Args:
            symbol: Trading pair
            funding_rates: List of FundingRate objects
        """
        filepath = self._get_funding_filename(symbol)
        
        data = []
        for rate in funding_rates:
            data.append({
                "symbol": rate.symbol,
                "rate": rate.rate,
                "timestamp": rate.timestamp.isoformat(),
                "annualized_rate": rate.annualized_rate
            })
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        
        # Update cache
        self._funding_cache[symbol] = funding_rates
    
    def calculate_persistence(self, symbol: str, days: int = 30) -> PersistenceData:
        """
        Calculate funding rate persistence for a symbol.
        
        Persistence measures how many consecutive days the funding rate
        has been elevated, indicating crowded positioning.
        
        Args:
            symbol: Trading pair
            days: Number of days to analyze
            
        Returns:
            PersistenceData with analysis results
        """
        funding_rates = self.fetch_funding_rates(symbol)
        
        if not funding_rates:
            return PersistenceData(
                symbol=symbol,
                consecutive_days_elevated=0,
                current_funding_rate=0.0,
                direction="neutral",
                is_warning=False,
                severity="low"
            )
        
        # Sort by timestamp (most recent first)
        sorted_rates = sorted(funding_rates, key=lambda x: x.timestamp, reverse=True)
        
        # Get rates from the last 'days' days
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_rates = [r for r in sorted_rates if r.timestamp >= cutoff_date]
        
        if not recent_rates:
            return PersistenceData(
                symbol=symbol,
                consecutive_days_elevated=0,
                current_funding_rate=0.0,
                direction="neutral",
                is_warning=False,
                severity="low"
            )
        
        # Calculate consecutive days elevated
        consecutive_days = 0
        current_direction = "neutral"
        
        for rate in recent_rates:
            if rate.is_elevated(self.ELEVATED_THRESHOLD):
                consecutive_days += 1
                if rate.rate > 0:
                    current_direction = "positive"
                else:
                    current_direction = "negative"
            else:
                break  # Stop counting when we hit a non-elevated rate
        
        # Get current funding rate
        current_rate = recent_rates[0] if recent_rates else None
        current_funding_rate = current_rate.rate if current_rate else 0.0
        
        # Determine if this is a warning (14+ consecutive days)
        is_warning = consecutive_days >= self.PERSISTENCE_WARNING_DAYS
        
        # Determine severity
        severity = self._calculate_severity(consecutive_days, current_rate)
        
        return PersistenceData(
            symbol=symbol,
            consecutive_days_elevated=consecutive_days,
            current_funding_rate=current_funding_rate,
            direction=current_direction,
            is_warning=is_warning,
            severity=severity
        )
    
    def _calculate_severity(self, consecutive_days: int, rate: Optional[FundingRate]) -> str:
        """
        Calculate severity level based on persistence and rate magnitude.
        
        Args:
            consecutive_days: Number of consecutive elevated days
            rate: Current FundingRate object
            
        Returns:
            Severity level: "low", "medium", "high", "extreme"
        """
        if consecutive_days >= 21:
            return "extreme"
        elif consecutive_days >= 14:
            return "high"
        elif consecutive_days >= 7:
            return "medium"
        elif consecutive_days >= 3:
            return "low"
        else:
            return "low"
    
    def get_crowded_positioning_signal(self, symbol: str) -> Dict[str, Any]:
        """
        Identify crowded positioning signals.
        
        Crowded positioning occurs when many traders have similar positions,
        often leading to reversals when funding persists elevated.
        
        Args:
            symbol: Trading pair
            
        Returns:
            Dictionary with signal information
        """
        persistence = self.calculate_persistence(symbol)
        
        signal = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "crowded_positioning": False,
            "warning": False,
            "direction": persistence.direction,
            "consecutive_days": persistence.consecutive_days_elevated,
            "current_rate": persistence.current_funding_rate,
            "severity": persistence.severity,
            "signal_type": "none",
            "recommendation": "normal"
        }
        
        # Check for crowded positioning
        if persistence.consecutive_days_elevated >= 3:
            signal["crowded_positioning"] = True
            
            # Generate signal based on direction and persistence
            if persistence.direction == "positive":
                # Positive funding persisting = crowded long positions
                if persistence.consecutive_days_elevated >= 14:
                    signal["warning"] = True
                    signal["signal_type"] = "reversal_short"
                    signal["recommendation"] = "Consider short positions or reduce long exposure"
                elif persistence.consecutive_days_elevated >= 7:
                    signal["signal_type"] = "caution_long"
                    signal["recommendation"] = "Long positions may be crowded, monitor for reversal"
                else:
                    signal["signal_type"] = "watch"
                    signal["recommendation"] = "Monitor funding persistence"
                    
            elif persistence.direction == "negative":
                # Negative funding persisting = crowded short positions
                if persistence.consecutive_days_elevated >= 14:
                    signal["warning"] = True
                    signal["signal_type"] = "reversal_long"
                    signal["recommendation"] = "Consider long positions or reduce short exposure"
                elif persistence.consecutive_days_elevated >= 7:
                    signal["signal_type"] = "caution_short"
                    signal["recommendation"] = "Short positions may be crowded, monitor for reversal"
                else:
                    signal["signal_type"] = "watch"
                    signal["recommendation"] = "Monitor funding persistence"
        
        return signal
    
    def get_all_signals(self) -> Dict[str, Dict[str, Any]]:
        """
        Get crowded positioning signals for all supported pairs.
        
        Returns:
            Dictionary mapping symbols to their signals
        """
        signals = {}
        
        for symbol in self.SUPPORTED_PAIRS:
            signals[symbol] = self.get_crowded_positioning_signal(symbol)
        
        return signals
    
    def add_funding_rate(self, symbol: str, rate: float, timestamp: Optional[datetime] = None):
        """
        Add a new funding rate observation.
        
        Args:
            symbol: Trading pair
            rate: Funding rate as decimal
            timestamp: Observation timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Calculate annualized rate (assuming 8 funding periods per day)
        # Funding rates are typically expressed per 8 hours
        periods_per_day = 3  # 8 hours * 3 = 24 hours
        periods_per_year = periods_per_day * 365
        annualized_rate = rate * periods_per_year
        
        funding_rate = FundingRate(
            symbol=symbol,
            rate=rate,
            timestamp=timestamp,
            annualized_rate=annualized_rate
        )
        
        # Add to cache
        if symbol not in self._funding_cache:
            self._funding_cache[symbol] = []
        
        self._funding_cache[symbol].append(funding_rate)
        
        # Save to storage
        self.save_funding_rates(symbol, self._funding_cache[symbol])
    
    def clear_cache(self, symbol: Optional[str] = None):
        """
        Clear the funding rate cache.
        
        Args:
            symbol: Specific symbol to clear, or None for all
        """
        if symbol:
            if symbol in self._funding_cache:
                del self._funding_cache[symbol]
        else:
            self._funding_cache.clear()
    
    def get_funding_summary(self, symbol: str) -> Dict[str, Any]:
        """
        Get a summary of funding rate data for a symbol.
        
        Args:
            symbol: Trading pair
            
        Returns:
            Summary dictionary
        """
        funding_rates = self.fetch_funding_rates(symbol)
        persistence = self.calculate_persistence(symbol)
        signal = self.get_crowded_positioning_signal(symbol)
        
        return {
            "symbol": symbol,
            "total_observations": len(funding_rates),
            "current_rate": persistence.current_funding_rate,
            "annualized_rate": funding_rates[0].annualized_rate if funding_rates else 0.0,
            "direction": persistence.direction,
            "consecutive_days_elevated": persistence.consecutive_days_elevated,
            "is_warning": persistence.is_warning,
            "severity": persistence.severity,
            "signal": signal["signal_type"],
            "recommendation": signal["recommendation"]
        }
