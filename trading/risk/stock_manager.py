"""
Stock Risk Management Module

Handles STOCKS-specific risk management including position limits,
sector exposure, earnings event risk, correlation risk (beta), and
dividend/earnings calendar awareness.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta
from enum import Enum


class Sector(Enum):
    """Stock sectors for exposure tracking."""
    TECHNOLOGY = "Technology"
    HEALTHCARE = "Healthcare"
    FINANCIAL = "Financial"
    CONSUMER_DISCRETIONARY = "Consumer Discretionary"
    CONSUMER_STAPLES = "Consumer Staples"
    ENERGY = "Energy"
    INDUSTRIALS = "Industrials"
    MATERIALS = "Materials"
    REAL_ESTATE = "Real Estate"
    UTILITIES = "Utilities"
    COMMUNICATION_SERVICES = "Communication Services"
    OTHER = "Other"


@dataclass
class StockConfig:
    """Stock risk management configuration."""

    # Risk settings
    risk_per_trade_percent: float = 1.0  # Risk 1-2% per trade
    min_rr_ratio: float = 2.0  # Minimum risk-reward ratio (1:2)

    # Position limits
    max_position_percent: float = 10.0  # Max 10% per stock
    min_position_percent: float = 5.0  # Min 5% per stock (recommended)

    # Sector exposure limits
    max_sector_exposure_percent: float = 30.0  # Max 30% per sector
    min_sector_exposure_percent: float = 25.0  # Min 25% per sector (recommended)

    # Earnings event settings
    earnings_risk_days: int = 5  # Days to avoid trading before/after earnings
    earnings_warning_days: int = 10  # Days for earnings warning

    # Correlation/Beta settings
    max_portfolio_beta: float = 1.2  # Max portfolio beta
    max_single_stock_beta: float = 1.5  # Max beta for single stock
    correlation_threshold: float = 0.7  # Correlation threshold for warning

    # Loss limits
    max_daily_loss_percent: float = 3.0  # Max 3% daily loss
    max_weekly_loss_percent: float = 6.0  # Max 6% weekly loss

    # Dividend settings
    dividend_ex_date_warning_days: int = 5  # Days before ex-date to warn
    dividend_yield_threshold: float = 5.0  # High dividend yield threshold (%)

    # Supported sectors
    supported_sectors: List[str] = field(default_factory=lambda: [
        "Technology", "Healthcare", "Financial", "Consumer Discretionary",
        "Consumer Staples", "Energy", "Industrials", "Materials",
        "Real Estate", "Utilities", "Communication Services", "Other"
    ])


@dataclass
class EarningsEvent:
    """Earnings event data."""
    ticker: str
    earnings_date: datetime
    estimated_eps: float
    previous_eps: float
    sector: str = "Other"


@dataclass
class DividendEvent:
    """Dividend event data."""
    ticker: str
    ex_date: datetime
    pay_date: datetime
    dividend_amount: float
    dividend_yield: float


class STOCKSRiskManager:
    """Stock-specific risk management."""

    # Market beta reference (S&P 500 = 1.0)
    BETA_REFERENCE = {
        "SPY": 1.0,
        "QQQ": 1.2,
        "DIA": 1.0,
        "IWM": 1.1,
    }

    # Sector classification for common stocks
    SECTOR_CLASSIFICATION = {
        # Technology
        "AAPL": Sector.TECHNOLOGY,
        "MSFT": Sector.TECHNOLOGY,
        "GOOGL": Sector.TECHNOLOGY,
        "GOOG": Sector.TECHNOLOGY,
        "AMZN": Sector.TECHNOLOGY,
        "META": Sector.TECHNOLOGY,
        "NVDA": Sector.TECHNOLOGY,
        "TSLA": Sector.TECHNOLOGY,
        "AMD": Sector.TECHNOLOGY,
        "INTC": Sector.TECHNOLOGY,
        "CRM": Sector.TECHNOLOGY,
        "ORCL": Sector.TECHNOLOGY,
        "CSCO": Sector.TECHNOLOGY,
        "ADBE": Sector.TECHNOLOGY,
        "NFLX": Sector.TECHNOLOGY,
        "PYPL": Sector.TECHNOLOGY,
        "SQ": Sector.TECHNOLOGY,
        "SHOP": Sector.TECHNOLOGY,
        "UBER": Sector.TECHNOLOGY,
        "LYFT": Sector.TECHNOLOGY,
        # Healthcare
        "JNJ": Sector.HEALTHCARE,
        "PFE": Sector.HEALTHCARE,
        "UNH": Sector.HEALTHCARE,
        "MRK": Sector.HEALTHCARE,
        "ABBV": Sector.HEALTHCARE,
        "LLY": Sector.HEALTHCARE,
        "TMO": Sector.HEALTHCARE,
        "ABT": Sector.HEALTHCARE,
        "DHR": Sector.HEALTHCARE,
        "BMY": Sector.HEALTHCARE,
        "AMGN": Sector.HEALTHCARE,
        "GILD": Sector.HEALTHCARE,
        "BIIB": Sector.HEALTHCARE,
        "REGN": Sector.HEALTHCARE,
        "VRTX": Sector.HEALTHCARE,
        # Financial
        "JPM": Sector.FINANCIAL,
        "BAC": Sector.FINANCIAL,
        "WFC": Sector.FINANCIAL,
        "C": Sector.FINANCIAL,
        "GS": Sector.FINANCIAL,
        "MS": Sector.FINANCIAL,
        "BLK": Sector.FINANCIAL,
        "SCHW": Sector.FINANCIAL,
        "AXP": Sector.FINANCIAL,
        "V": Sector.FINANCIAL,
        "MA": Sector.FINANCIAL,
        "COF": Sector.FINANCIAL,
        "USB": Sector.FINANCIAL,
        "PNC": Sector.FINANCIAL,
        "TFC": Sector.FINANCIAL,
        # Consumer Discretionary
        "HD": Sector.CONSUMER_DISCRETIONARY,
        "LOW": Sector.CONSUMER_DISCRETIONARY,
        "NKE": Sector.CONSUMER_DISCRETIONARY,
        "SBUX": Sector.CONSUMER_DISCRETIONARY,
        "MCD": Sector.CONSUMER_DISCRETIONARY,
        "KO": Sector.CONSUMER_STAPLES,
        "PEP": Sector.CONSUMER_STAPLES,
        "COST": Sector.CONSUMER_STAPLES,
        "WMT": Sector.CONSUMER_STAPLES,
        "TGT": Sector.CONSUMER_DISCRETIONARY,
        "AMZN": Sector.CONSUMER_DISCRETIONARY,
        "EBAY": Sector.CONSUMER_DISCRETIONARY,
        "ETSY": Sector.CONSUMER_DISCRETIONARY,
        # Energy
        "XOM": Sector.ENERGY,
        "CVX": Sector.ENERGY,
        "COP": Sector.ENERGY,
        "SLB": Sector.ENERGY,
        "EOG": Sector.ENERGY,
        "MPC": Sector.ENERGY,
        "PSX": Sector.ENERGY,
        "VLO": Sector.ENERGY,
        # Industrials
        "BA": Sector.INDUSTRIALS,
        "CAT": Sector.INDUSTRIALS,
        "GE": Sector.INDUSTRIALS,
        "MMM": Sector.INDUSTRIALS,
        "HON": Sector.INDUSTRIALS,
        "UPS": Sector.INDUSTRIALS,
        "FDX": Sector.INDUSTRIALS,
        "LMT": Sector.INDUSTRIALS,
        "RTX": Sector.INDUSTRIALS,
        "GD": Sector.INDUSTRIALS,
        # Materials
        "LIN": Sector.MATERIALS,
        "APD": Sector.MATERIALS,
        "ECL": Sector.MATERIALS,
        "NEM": Sector.MATERIALS,
        "FCX": Sector.MATERIALS,
        "NUE": Sector.MATERIALS,
        "DOW": Sector.MATERIALS,
        "DD": Sector.MATERIALS,
        # Real Estate
        "AMT": Sector.REAL_ESTATE,
        "PLD": Sector.REAL_ESTATE,
        "CCI": Sector.REAL_ESTATE,
        "EQIX": Sector.REAL_ESTATE,
        "PSA": Sector.REAL_ESTATE,
        "SPG": Sector.REAL_ESTATE,
        "O": Sector.REAL_ESTATE,
        "WELL": Sector.REAL_ESTATE,
        # Utilities
        "NEE": Sector.UTILITIES,
        "DUK": Sector.UTILITIES,
        "SO": Sector.UTILITIES,
        "D": Sector.UTILITIES,
        "AEP": Sector.UTILITIES,
        "EXC": Sector.UTILITIES,
        "XEL": Sector.UTILITIES,
        "ED": Sector.UTILITIES,
        # Communication Services
        "DIS": Sector.COMMUNICATION_SERVICES,
        "CMCSA": Sector.COMMUNICATION_SERVICES,
        "VZ": Sector.COMMUNICATION_SERVICES,
        "T": Sector.COMMUNICATION_SERVICES,
        "EA": Sector.COMMUNICATION_SERVICES,
        "ATVI": Sector.COMMUNICATION_SERVICES,
        "TTWO": Sector.COMMUNICATION_SERVICES,
        "OMC": Sector.COMMUNICATION_SERVICES,
    }

    # Correlation matrix for major stocks (simplified)
    CORRELATION_MATRIX = {
        "AAPL": {"MSFT": 0.85, "GOOGL": 0.75, "AMZN": 0.65, "META": 0.70, "NVDA": 0.80},
        "MSFT": {"AAPL": 0.85, "GOOGL": 0.80, "AMZN": 0.70, "META": 0.65, "NVDA": 0.75},
        "GOOGL": {"AAPL": 0.75, "MSFT": 0.80, "AMZN": 0.75, "META": 0.70, "NVDA": 0.65},
        "AMZN": {"AAPL": 0.65, "MSFT": 0.70, "GOOGL": 0.75, "META": 0.60, "NVDA": 0.70},
        "META": {"AAPL": 0.70, "MSFT": 0.65, "GOOGL": 0.70, "AMZN": 0.60, "NVDA": 0.65},
        "NVDA": {"AAPL": 0.80, "MSFT": 0.75, "GOOGL": 0.65, "AMZN": 0.70, "META": 0.65},
        "JPM": {"BAC": 0.90, "WFC": 0.85, "C": 0.80, "GS": 0.75, "MS": 0.70},
        "BAC": {"JPM": 0.90, "WFC": 0.85, "C": 0.80, "GS": 0.70, "MS": 0.70},
        "WFC": {"JPM": 0.85, "BAC": 0.85, "C": 0.75, "GS": 0.65, "MS": 0.65},
        "XOM": {"CVX": 0.85, "COP": 0.80, "SLB": 0.70, "EOG": 0.75},
        "CVX": {"XOM": 0.85, "COP": 0.80, "SLB": 0.70, "EOG": 0.75},
    }

    def __init__(self, config: Optional[StockConfig] = None):
        self.config = config or StockConfig()
        self.daily_loss = 0.0
        self.weekly_loss = 0.0
        self.daily_trades = 0
        self.weekly_trades = 0
        self.current_positions: Dict[str, Dict] = {}
        self.earnings_calendar: Dict[str, EarningsEvent] = {}
        self.dividend_calendar: Dict[str, DividendEvent] = {}

    def calculate_position_size(
        self,
        account_balance: float,
        entry_price: float,
        sl_price: float,
        ticker: str,
        risk_percent: float = None,
    ) -> Dict[str, float]:
        """
        Calculate position size using percentage-based method (STOCKS-specific).

        Args:
            account_balance: Total account balance
            entry_price: Entry price
            sl_price: Stop loss price
            ticker: Stock ticker symbol
            risk_percent: Risk percentage (default from config)

        Returns:
            Dict with position_size, risk_amount, risk_percent, etc.
        """
        if risk_percent is None:
            risk_percent = self.config.risk_per_trade_percent

        # Calculate SL distance in price terms
        sl_distance = abs(entry_price - sl_price)

        if sl_distance == 0:
            return {
                "position_size": 0,
                "risk_amount": 0.0,
                "shares": 0,
                "error": "Zero SL distance"
            }

        # Calculate risk amount in account currency
        risk_amount = account_balance * (risk_percent / 100)

        # Position size = Risk amount / SL distance
        position_value = risk_amount / (sl_distance / entry_price)
        shares = int(position_value / entry_price)

        if shares == 0:
            return {
                "position_size": 0,
                "risk_amount": 0.0,
                "shares": 0,
                "error": "Position too small"
            }

        # Calculate actual position value and risk
        actual_position_value = shares * entry_price
        actual_risk = shares * sl_distance

        # Calculate position as percentage of account
        position_percent = (actual_position_value / account_balance) * 100

        return {
            "position_size": shares,
            "position_value": round(actual_position_value, 2),
            "risk_amount": round(actual_risk, 2),
            "risk_percent": risk_percent,
            "position_percent": round(position_percent, 2),
            "entry_price": entry_price,
            "sl_price": sl_price,
            "sl_distance": sl_distance,
            "shares": shares,
        }

    def check_position_limits(
        self,
        ticker: str,
        position_percent: float,
        account_balance: float,
    ) -> Tuple[bool, str]:
        """
        Check if position size is within limits.

        Args:
            ticker: Stock ticker symbol
            position_percent: Proposed position as percentage of account
            account_balance: Total account balance

        Returns:
            (is_safe, warning_message)
        """
        max_percent = self.config.max_position_percent
        min_percent = self.config.min_position_percent

        if position_percent > max_percent:
            return (False, f"Position size {position_percent:.1f}% exceeds max {max_percent}% for {ticker}")

        if position_percent < min_percent:
            return (True, f"Position size {position_percent:.1f}% is below recommended {min_percent}% for {ticker}")

        return (True, f"Position size {position_percent:.1f}% is acceptable")

    def sector_exposure_check(
        self,
        ticker: str,
        proposed_position_value: float,
        current_positions: Dict[str, Dict] = None,
    ) -> Tuple[bool, str]:
        """
        Check sector exposure limits.

        Args:
            ticker: Stock ticker symbol
            proposed_position_value: Value of proposed position
            current_positions: Current open positions

        Returns:
            (is_safe, warning_message)
        """
        if current_positions is None:
            current_positions = self.current_positions

        # Get sector for ticker
        sector = self._get_sector(ticker)

        # Calculate current sector exposure
        sector_exposure = proposed_position_value
        total_portfolio_value = proposed_position_value

        for existing_ticker, position in current_positions.items():
            existing_sector = self._get_sector(existing_ticker)
            position_value = position.get("position_value", 0)
            total_portfolio_value += position_value

            if existing_sector == sector:
                sector_exposure += position_value

        # Calculate exposure percentages
        if total_portfolio_value == 0:
            sector_percent = 0
        else:
            sector_percent = (sector_exposure / total_portfolio_value) * 100

        max_sector = self.config.max_sector_exposure_percent
        min_sector = self.config.min_sector_exposure_percent

        if sector_percent > max_sector:
            return (False, f"Sector exposure {sector_percent:.1f}% exceeds max {max_sector}% for {sector.value}")

        if sector_percent < min_sector:
            return (True, f"Sector exposure {sector_percent:.1f}% is below recommended {min_sector}% for {sector.value}")

        return (True, f"Sector exposure {sector_percent:.1f}% is acceptable for {sector.value}")

    def _get_sector(self, ticker: str) -> Sector:
        """Get sector for a ticker."""
        return self.SECTOR_CLASSIFICATION.get(ticker.upper(), Sector.OTHER)

    def correlation_risk_check(
        self,
        ticker: str,
        proposed_position_value: float,
        beta: float = None,
        current_positions: Dict[str, Dict] = None,
    ) -> Tuple[bool, str]:
        """
        Check correlation and beta risk.

        Args:
            ticker: Stock ticker symbol
            proposed_position_value: Value of proposed position
            beta: Market beta for the stock (default from reference)
            current_positions: Current open positions

        Returns:
            (is_safe, warning_message)
        """
        if current_positions is None:
            current_positions = self.current_positions

        # Get beta
        if beta is None:
            beta = self._get_beta(ticker)

        # Check single stock beta limit
        max_beta = self.config.max_single_stock_beta
        if beta > max_beta:
            return (False, f"Beta {beta:.2f} exceeds max {max_beta} for {ticker}")

        # Calculate portfolio beta
        portfolio_beta = self._calculate_portfolio_beta(
            ticker, proposed_position_value, beta, current_positions
        )

        max_portfolio_beta = self.config.max_portfolio_beta
        if portfolio_beta > max_portfolio_beta:
            return (False, f"Portfolio beta {portfolio_beta:.2f} exceeds max {max_portfolio_beta}")

        # Check correlation with existing positions
        correlated_stocks = self._get_correlated_stocks(ticker, current_positions)

        if correlated_stocks:
            warning_parts = [f"High correlation with: "]
            for stock, correlation in correlated_stocks:
                warning_parts.append(f"{stock} ({correlation:.2f})")

            return (True, " ".join(warning_parts))

        return (True, f"Beta {beta:.2f} is acceptable")

    def _get_beta(self, ticker: str) -> float:
        """Get market beta for a ticker."""
        ticker_upper = ticker.upper()

        # Check reference dictionary
        if ticker_upper in self.BETA_REFERENCE:
            return self.BETA_REFERENCE[ticker_upper]

        # Default beta for unknown stocks
        return 1.0

    def _calculate_portfolio_beta(
        self,
        ticker: str,
        proposed_value: float,
        beta: float,
        current_positions: Dict[str, Dict],
    ) -> float:
        """Calculate weighted portfolio beta."""
        total_value = proposed_value
        weighted_beta = proposed_value * beta

        for existing_ticker, position in current_positions.items():
            position_value = position.get("position_value", 0)
            total_value += position_value

            if existing_ticker != ticker:
                existing_beta = self._get_beta(existing_ticker)
                weighted_beta += position_value * existing_beta

        if total_value == 0:
            return 0

        return weighted_beta / total_value

    def _get_correlated_stocks(
        self,
        ticker: str,
        current_positions: Dict[str, Dict],
    ) -> List[Tuple[str, float]]:
        """Get list of correlated stocks in portfolio."""
        correlated = []

        ticker_upper = ticker.upper()

        for existing_ticker in current_positions.keys():
            if existing_ticker.upper() == ticker_upper:
                continue

            correlation = self._get_correlation(ticker_upper, existing_ticker.upper())
            if abs(correlation) >= self.config.correlation_threshold:
                correlated.append((existing_ticker, correlation))

        return correlated

    def _get_correlation(self, ticker1: str, ticker2: str) -> float:
        """Get correlation coefficient between two stocks."""
        ticker1_upper = ticker1.upper()
        ticker2_upper = ticker2.upper()

        if ticker1_upper not in self.CORRELATION_MATRIX:
            return 0.0

        correlations = self.CORRELATION_MATRIX[ticker1_upper]
        return correlations.get(ticker2_upper, 0.0)

    def earnings_risk_check(
        self,
        ticker: str,
        current_date: datetime = None,
    ) -> Tuple[bool, str]:
        """
        Check earnings event risk.

        Args:
            ticker: Stock ticker symbol
            current_date: Current date (default: now)

        Returns:
            (is_safe, warning_message)
        """
        if current_date is None:
            current_date = datetime.now()

        ticker_upper = ticker.upper()

        if ticker_upper not in self.earnings_calendar:
            return (True, "No earnings date on record")

        earnings_event = self.earnings_calendar[ticker_upper]
        days_to_earnings = (earnings_event.earnings_date - current_date).days

        # Check if within risk period
        risk_days = self.config.earnings_risk_days
        warning_days = self.config.earnings_warning_days

        if abs(days_to_earnings) <= risk_days:
            return (False, f"Earnings in {days_to_earnings} days - high risk period")

        if abs(days_to_earnings) <= warning_days:
            return (True, f"Warning: Earnings in {days_to_earnings} days")

        return (True, f"Earnings in {days_to_earnings} days - acceptable")

    def add_earnings_event(self, earnings_event: EarningsEvent):
        """Add an earnings event to the calendar."""
        self.earnings_calendar[earnings_event.ticker.upper()] = earnings_event

    def dividend_risk_check(
        self,
        ticker: str,
        current_date: datetime = None,
    ) -> Tuple[bool, str]:
        """
        Check dividend event risk.

        Args:
            ticker: Stock ticker symbol
            current_date: Current date (default: now)

        Returns:
            (is_safe, warning_message)
        """
        if current_date is None:
            current_date = datetime.now()

        ticker_upper = ticker.upper()

        if ticker_upper not in self.dividend_calendar:
            return (True, "No dividend event on record")

        dividend_event = self.dividend_calendar[ticker_upper]
        days_to_ex_date = (dividend_event.ex_date - current_date).days

        # Check if within warning period
        warning_days = self.config.dividend_ex_date_warning_days

        if days_to_ex_date <= 0:
            return (True, "Ex-date has passed")

        if days_to_ex_date <= warning_days:
            return (True, f"Ex-date in {days_to_ex_date} days - dividend capture possible")

        # Check dividend yield
        if dividend_event.dividend_yield > self.config.dividend_yield_threshold:
            return (True, f"High dividend yield {dividend_event.dividend_yield:.1f}%")

        return (True, f"Ex-date in {days_to_ex_date} days")

    def add_dividend_event(self, dividend_event: DividendEvent):
        """Add a dividend event to the calendar."""
        self.dividend_calendar[dividend_event.ticker.upper()] = dividend_event

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
        ticker: str,
        entry_price: float,
        sl_price: float,
        tp_price: float,
        position_percent: float,
        account_balance: float,
        beta: float = None,
        current_positions: Dict[str, Dict] = None,
        current_date: datetime = None,
    ) -> Tuple[bool, str]:
        """
        Comprehensive trade validation for stocks.

        Args:
            ticker: Stock ticker symbol
            entry_price: Entry price
            sl_price: Stop loss price
            tp_price: Take profit price
            position_percent: Position as percentage of account
            account_balance: Account balance
            beta: Market beta for the stock
            current_positions: Current open positions
            current_date: Current date

        Returns:
            (is_valid, validation_message)
        """
        # Check position limits
        position_ok, position_msg = self.check_position_limits(
            ticker, position_percent, account_balance
        )
        if not position_ok:
            return (position_ok, position_msg)

        # Calculate position value
        position_value = account_balance * (position_percent / 100)

        # Check sector exposure
        sector_ok, sector_msg = self.sector_exposure_check(
            ticker, position_value, current_positions
        )
        if not sector_ok:
            return (sector_ok, sector_msg)

        # Check correlation risk
        corr_ok, corr_msg = self.correlation_risk_check(
            ticker, position_value, beta, current_positions
        )
        if not corr_ok:
            return (corr_ok, corr_msg)

        # Check earnings risk
        earnings_ok, earnings_msg = self.earnings_risk_check(ticker, current_date)
        if not earnings_ok:
            return (earnings_ok, earnings_msg)

        # Check RR ratio
        rr_ratio = self.calculate_rr_ratio(entry_price, sl_price, tp_price)
        if rr_ratio < self.config.min_rr_ratio:
            return (False, f"RR ratio {rr_ratio:.2f} below minimum {self.config.min_rr_ratio}")

        # Check loss limits
        limits_ok, limits_msg = self.check_loss_limits(account_balance)
        if not limits_ok:
            return (limits_ok, limits_msg)

        # All checks passed
        messages = [position_msg, sector_msg, corr_msg, earnings_msg, limits_msg]
        valid_messages = [msg for msg in messages if msg and msg != "OK"]

        return (True, f"Trade validated. {'; '.join(valid_messages)}" if valid_messages else "All checks passed")

    def get_position_summary(
        self,
        ticker: str,
        position_size: int,
        entry_price: float,
        sl_price: float,
    ) -> Dict:
        """Get summary of a proposed position."""
        position_value = position_size * entry_price
        sl_distance = abs(entry_price - sl_price)

        return {
            "ticker": ticker,
            "position_size": position_size,
            "position_value": position_value,
            "entry_price": entry_price,
            "sl_price": sl_price,
            "sl_distance": sl_distance,
            "sector": self._get_sector(ticker).value,
            "beta": self._get_beta(ticker),
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

    def add_position(self, ticker: str, position_size: int, entry_price: float, sl_price: float):
        """Add a position to tracking."""
        position_value = position_size * entry_price
        self.current_positions[ticker.upper()] = {
            "position_size": position_size,
            "position_value": position_value,
            "entry_price": entry_price,
            "sl_price": sl_price,
        }

    def remove_position(self, ticker: str):
        """Remove a position from tracking."""
        ticker_upper = ticker.upper()
        if ticker_upper in self.current_positions:
            del self.current_positions[ticker_upper]

    def get_portfolio_summary(self) -> Dict[str, any]:
        """Get summary of current portfolio."""
        total_value = 0.0
        sector_exposure = {}
        portfolio_beta = 0.0

        for ticker, position in self.current_positions.items():
            position_value = position.get("position_value", 0)
            total_value += position_value

            # Sector exposure
            sector = self._get_sector(ticker)
            if sector not in sector_exposure:
                sector_exposure[sector] = 0.0
            sector_exposure[sector] += position_value

            # Portfolio beta
            beta = self._get_beta(ticker)
            portfolio_beta += position_value * beta

        # Calculate weighted beta
        if total_value > 0:
            portfolio_beta = portfolio_beta / total_value
        else:
            portfolio_beta = 0

        # Convert sector exposure to percentages
        sector_percentages = {}
        for sector, value in sector_exposure.items():
            sector_percentages[sector.value] = round((value / total_value) * 100, 2) if total_value > 0 else 0

        return {
            "total_value": round(total_value, 2),
            "positions_count": len(self.current_positions),
            "portfolio_beta": round(portfolio_beta, 2),
            "sector_exposure": sector_percentages,
        }
