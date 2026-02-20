"""
STOCKS Backtest Engine

STOCKS-specific backtesting with percentage returns, alpha/beta metrics,
sector-adjusted returns, and support for stock screening.
Extends the base BacktestEngine for STOCKS-specific requirements.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import numpy as np

from .engine import BacktestEngine, BacktestMetrics, TradeResult
from ..brokers.base import OHLCV
from ..strategy.base import TradingSignal


# Supported timeframes for stocks
STOCKS_TIMEFRAMES = ["D1", "W1", "MN1"]  # Daily, Weekly, Monthly

# Common stock sectors for sector-adjusted analysis
STOCK_SECTORS = {
    # Technology
    "AAPL": "Technology", "MSFT": "Technology", "GOOGL": "Technology",
    "GOOG": "Technology", "NVDA": "Technology", "META": "Technology",
    "TSLA": "Technology", "AMD": "Technology", "INTC": "Technology",
    "CRM": "Technology", "ADBE": "Technology", "CSCO": "Technology",
    # Healthcare
    "JNJ": "Healthcare", "PFE": "Healthcare", "UNH": "Healthcare",
    "MRK": "Healthcare", "ABBV": "Healthcare", "LLY": "Healthcare",
    "TMO": "Healthcare", "ABT": "Healthcare", "DHR": "Healthcare",
    # Financials
    "JPM": "Financials", "BAC": "Financials", "WFC": "Financials",
    "V": "Financials", "MA": "Financials", "GS": "Financials",
    "MS": "Financials", "C": "Financials", "BLK": "Financials",
    # Consumer Discretionary
    "AMZN": "Consumer Discretionary", "TSLA": "Consumer Discretionary",
    "HD": "Consumer Discretionary", "MCD": "Consumer Discretionary",
    "NKE": "Consumer Discretionary", "SBUX": "Consumer Discretionary",
    "LOW": "Consumer Discretionary", "TJX": "Consumer Discretionary",
    # Consumer Staples
    "PG": "Consumer Staples", "KO": "Consumer Staples", "PEP": "Consumer Staples",
    "WMT": "Consumer Staples", "COST": "Consumer Staples", "PM": "Consumer Staples",
    "CL": "Consumer Staples", "KMB": "Consumer Staples", "GIS": "Consumer Staples",
    # Energy
    "XOM": "Energy", "CVX": "Energy", "COP": "Energy",
    "SLB": "Energy", "EOG": "Energy", "MPC": "Energy",
    # Industrials
    "BA": "Industrials", "CAT": "Industrials", "GE": "Industrials",
    "MMM": "Industrials", "HON": "Industrials", "UPS": "Industrials",
    # Utilities
    "NEE": "Utilities", "DUK": "Utilities", "SO": "Utilities",
    "D": "Utilities", "AEP": "Utilities", "EXC": "Utilities",
    # Real Estate
    "AMT": "Real Estate", "PLD": "Real Estate", "CCI": "Real Estate",
    "EQIX": "Real Estate", "PSA": "Real Estate", "SPG": "Real Estate",
    # Materials
    "LIN": "Materials", "APD": "Materials", "ECL": "Materials",
    "NEM": "Materials", "FCX": "Materials", "NUE": "Materials",
    # Communication Services
    "DIS": "Communication Services", "CMCSA": "Communication Services",
    "VZ": "Communication Services", "T": "Communication Services",
    "NFLX": "Communication Services", "CHTR": "Communication Services",
}

# Sector benchmark tickers (simplified - in production would use actual sector ETFs)
SECTOR_BENCHMARKS = {
    "Technology": "^XLK",      # Technology Select Sector SPDR
    "Healthcare": "^XLV",      # Healthcare Select Sector SPDR
    "Financials": "^XLF",      # Financial Select Sector SPDR
    "Consumer Discretionary": "^XLY",
    "Consumer Staples": "^XLP",
    "Energy": "^XLE",
    "Industrials": "^XLI",
    "Utilities": "^XLU",
    "Real Estate": "^XLRE",
    "Materials": "^XLB",
    "Communication Services": "^XLC",
}

# Default risk-free rate for Sharpe ratio (annual)
DEFAULT_RISK_FREE_RATE = 0.05  # 5% annual


@dataclass
class StockTradeResult:
    """Extended trade result with STOCKS-specific metrics."""

    # Base fields from TradeResult
    entry_time: datetime
    exit_time: datetime
    symbol: str
    side: str  # BUY or SELL
    entry_price: float
    exit_price: float
    volume: float  # Number of shares
    sl: float
    tp: float
    result: str  # WIN, LOSS, BREAKEVEN
    pnl_points: float
    pnl_money: float
    r_multiple: float
    reason: str

    # STOCKS-specific fields
    pnl_percent: float = 0.0  # Return as percentage
    dividend_adj_pnl: float = 0.0  # PnL adjusted for dividends
    split_adj_pnl: float = 0.0  # PnL adjusted for stock splits
    sector: str = ""  # Stock sector classification
    holding_days: int = 0  # Number of days held
    annual_return: float = 0.0  # Annualized return
    transaction_cost: float = 0.0  # Commission and fees

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
            "pnl_percent": self.pnl_percent,
            "dividend_adj_pnl": self.dividend_adj_pnl,
            "split_adj_pnl": self.split_adj_pnl,
            "sector": self.sector,
            "holding_days": self.holding_days,
            "annual_return": self.annual_return,
            "transaction_cost": self.transaction_cost,
        }
        return base


@dataclass
class StockBacktestMetrics:
    """Extended metrics with STOCKS-specific calculations."""

    # Base metrics
    symbol: str = ""
    sector: str = ""
    timeframe: str = ""
    strategy: str = ""
    start_date: str = ""
    end_date: str = ""
    leverage: int = 1  # Stocks typically don't use leverage
    risk_percent: float = 1.0
    avg_shares: float = 0.0
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

    # STOCKS-specific metrics
    total_return_percent: float = 0.0  # Total return as percentage
    annual_return_percent: float = 0.0  # Annualized return
    volatility_percent: float = 0.0  # Annualized volatility
    sharpe_ratio: float = 0.0  # Risk-adjusted return
    sortino_ratio: float = 0.0  # Downside risk-adjusted return
    alpha: float = 0.0  # Excess return vs benchmark
    beta: float = 0.0  # Market sensitivity
    max_drawdown_percent: float = 0.0  # Max drawdown as percentage
    avg_holding_days: float = 0.0  # Average holding period
    total_commission: float = 0.0  # Total transaction costs
    avg_commission: float = 0.0  # Average commission per trade

    # Sector-adjusted metrics
    sector_benchmark_return: float = 0.0  # Sector benchmark return
    sector_alpha: float = 0.0  # Alpha vs sector benchmark
    sector_relative_return: float = 0.0  # Return relative to sector

    # Benchmark comparison
    benchmark_symbol: str = "SPY"  # Default benchmark (S&P 500)
    benchmark_return: float = 0.0  # Benchmark return over same period
    alpha_vs_benchmark: float = 0.0  # Alpha vs benchmark
    beta_to_benchmark: float = 0.0  # Beta to benchmark

    # Screening results
    screening_criteria: Dict[str, Any] = field(default_factory=dict)
    screened_symbols: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        base = {
            "symbol": self.symbol,
            "sector": self.sector,
            "timeframe": self.timeframe,
            "strategy": self.strategy,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "leverage": self.leverage,
            "risk_percent": self.risk_percent,
            "avg_shares": self.avg_shares,
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
            "total_return_percent": self.total_return_percent,
            "annual_return_percent": self.annual_return_percent,
            "volatility_percent": self.volatility_percent,
            "sharpe_ratio": self.sharpe_ratio,
            "sortino_ratio": self.sortino_ratio,
            "alpha": self.alpha,
            "beta": self.beta,
            "max_drawdown_percent": self.max_drawdown_percent,
            "avg_holding_days": self.avg_holding_days,
            "total_commission": self.total_commission,
            "avg_commission": self.avg_commission,
            "sector_benchmark_return": self.sector_benchmark_return,
            "sector_alpha": self.sector_alpha,
            "sector_relative_return": self.sector_relative_return,
            "benchmark_symbol": self.benchmark_symbol,
            "benchmark_return": self.benchmark_return,
            "alpha_vs_benchmark": self.alpha_vs_benchmark,
            "beta_to_benchmark": self.beta_to_benchmark,
            "screening_criteria": self.screening_criteria,
            "screened_symbols": self.screened_symbols,
        }
        return base


class StockBacktestEngine(BacktestEngine):
    """
    STOCKS-specific backtest engine.

    Extends the base BacktestEngine with:
    - Percentage-based calculations and metrics
    - Alpha/Beta calculations against benchmark
    - Sharpe and Sortino ratios
    - Sector-adjusted returns
    - Stock screening support
    - Stock split and dividend handling (basic)
    - Support for multiple stocks
    """

    def __init__(self, strategy, config: Optional[Dict[str, Any]] = None):
        # Initialize base class
        super().__init__(strategy, config)

        # Override defaults for STOCKS
        self._symbol = self.config.get("symbol", "AAPL")
        self._timeframe = self.config.get("timeframe", "D1")
        self._sector = self.config.get("sector", STOCK_SECTORS.get(self._symbol, "Unknown"))

        # Validate timeframe
        if self._timeframe not in STOCKS_TIMEFRAMES:
            raise ValueError(
                f"Unsupported timeframe: {self._timeframe}. "
                f"Supported: {STOCKS_TIMEFRAMES}"
            )

        # STOCKS-specific configuration
        self.commission_per_share = self.config.get("commission_per_share", 0.0)
        self.min_commission = self.config.get("min_commission", 0.0)
        self.slippage_percent = self.config.get("slippage_percent", 0.0)

        # Benchmark configuration
        self.benchmark_symbol = self.config.get("benchmark_symbol", "SPY")
        self.benchmark_returns = self.config.get("benchmark_returns", [])  # List of benchmark returns

        # Sector configuration
        self.sector = self._sector
        self.sector_benchmark_return = self.config.get("sector_benchmark_return", 0.0)

        # Dividend configuration (simplified - in production would use actual dividend data)
        self.annual_dividend_yield = self.config.get("annual_dividend_yield", 0.0)

        # Stock split configuration (simplified - in production would use actual split data)
        self.split_adjustment_factor = self.config.get("split_adjustment_factor", 1.0)

        # Screening configuration
        self.screening_criteria = self.config.get("screening_criteria", {})
        self.screened_symbols = self.config.get("screened_symbols", [])

        # Risk-free rate for Sharpe ratio (annual)
        self.risk_free_rate = self.config.get("risk_free_rate", DEFAULT_RISK_FREE_RATE)

        # Store STOCKS-specific trades
        self.stock_trades: List[StockTradeResult] = []

        # Store daily returns for volatility calculations
        self.daily_returns: List[float] = []

    def _calculate_pnl_percent(self, entry_price: float, exit_price: float) -> float:
        """Calculate PnL as percentage."""
        if entry_price <= 0:
            return 0.0
        return ((exit_price - entry_price) / entry_price) * 100

    def _calculate_annualized_return(
        self, total_return: float, days_held: int
    ) -> float:
        """Annualize return based on holding period."""
        if days_held <= 0:
            return 0.0
        # Annualize using 252 trading days
        years = days_held / 252.0
        if years <= 0:
            return 0.0
        # Compound annual growth rate formula
        return ((1 + total_return / 100) ** (1 / years) - 1) * 100

    def _calculate_transaction_cost(self, shares: float, price: float) -> float:
        """Calculate transaction cost (commission)."""
        commission = shares * self.commission_per_share
        if self.min_commission > 0 and commission < self.min_commission:
            commission = self.min_commission
        return commission

    def _apply_slippage(self, price: float, side: str) -> float:
        """Apply slippage to price."""
        if self.slippage_percent <= 0:
            return price
        slippage = price * (self.slippage_percent / 100)
        if side == "BUY":
            return price + slippage
        else:
            return price - slippage

    def _calculate_dividend_adjustment(
        self, shares: float, holding_days: int
    ) -> float:
        """Calculate dividend adjustment (simplified)."""
        if self.annual_dividend_yield <= 0 or holding_days <= 0:
            return 0.0
        # Pro-rated dividend based on holding period
        daily_yield = self.annual_dividend_yield / 252.0
        return shares * daily_yield * holding_days

    def _calculate_split_adjustment(
        self, pnl_money: float, split_factor: float
    ) -> float:
        """Apply stock split adjustment to PnL."""
        return pnl_money * split_factor

    def _create_stock_trade_result(
        self,
        signal: TradingSignal,
        side: str,
        entry_time: datetime,
        exit_time: datetime,
        entry_price: float,
        exit_price: float,
        reason: str,
    ) -> StockTradeResult:
        """Create STOCKS-specific trade result."""
        # Get current account balance for position sizing
        current_balance = self.initial_balance
        if self.trades:
            current_balance = self.initial_balance + sum(
                t.pnl_money for t in self.trades
            )

        # Calculate shares using risk manager
        sl_price = signal.buy_sl if side == "BUY" else signal.sell_sl
        lot_result = self.risk_manager.calculate_lot_size(
            account_balance=current_balance,
            entry_price=entry_price,
            sl_price=sl_price,
            risk_percent=self.risk_percent,
            leverage=self.leverage,
        )
        shares = lot_result["lot_size"]  # In stocks, lot_size represents shares

        # Apply slippage
        entry_price_adj = self._apply_slippage(entry_price, side)
        exit_price_adj = self._apply_slippage(exit_price, side)

        # Calculate PnL in price points
        if side == "BUY":
            pnl_points = exit_price_adj - entry_price_adj
        else:
            pnl_points = entry_price_adj - exit_price_adj

        # Calculate PnL in money
        pnl_money = pnl_points * shares

        # Calculate PnL percentage
        pnl_percent = self._calculate_pnl_percent(entry_price_adj, exit_price_adj)

        # Calculate holding days
        holding_days = (exit_time - entry_time).days

        # Calculate dividend adjustment
        dividend_adj = self._calculate_dividend_adjustment(shares, holding_days)

        # Calculate split adjustment
        split_adj = self._calculate_split_adjustment(pnl_money, self.split_adjustment_factor)

        # Calculate transaction cost
        transaction_cost = self._calculate_transaction_cost(shares, entry_price_adj)

        # Net PnL after costs
        net_pnl_money = pnl_money - transaction_cost + dividend_adj

        # Calculate annual return
        annual_return = self._calculate_annualized_return(pnl_percent, holding_days)

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

        # Get sector
        symbol = signal.symbol or self._symbol
        sector = STOCK_SECTORS.get(symbol, "Unknown")

        return StockTradeResult(
            entry_time=entry_time,
            exit_time=exit_time,
            symbol=symbol,
            side=side,
            entry_price=entry_price_adj,
            exit_price=exit_price_adj,
            volume=shares,
            sl=signal.buy_sl if side == "BUY" else signal.sell_sl,
            tp=signal.buy_tp if side == "BUY" else signal.sell_tp,
            result=result,
            pnl_points=pnl_points,
            pnl_money=net_pnl_money,
            r_multiple=r_multiple,
            reason=reason,
            pnl_percent=pnl_percent,
            dividend_adj_pnl=dividend_adj,
            split_adj_pnl=split_adj,
            sector=sector,
            holding_days=holding_days,
            annual_return=annual_return,
            transaction_cost=transaction_cost,
        )

    def run(
        self,
        ohlcv_data: List[OHLCV],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        benchmark_returns: Optional[List[float]] = None,
    ) -> StockBacktestMetrics:
        """Run backtest on historical stock data."""
        self.trades = []
        self.stock_trades = []
        self.equity_curve = []
        self.daily_returns = []

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

        # Find trading days and generate signals
        trading_dates = self._get_trading_days(ohlcv_data)

        for date in trading_dates:
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
            trade = self._simulate_stock_trade(signal, day_data)

            if trade:
                self.trades.append(trade)
                self.stock_trades.append(trade)

                # Update equity curve
                self._update_equity()

        # Use provided benchmark returns or calculate from config
        if benchmark_returns is not None:
            self.benchmark_returns = benchmark_returns

        # Calculate STOCKS-specific metrics
        metrics = self._calculate_stock_metrics()

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

    def _simulate_stock_trade(
        self, signal: TradingSignal, day_data: List[OHLCV]
    ) -> Optional[StockTradeResult]:
        """Simulate trade execution for stocks with slippage modeling."""
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

                return self._create_stock_trade_result(
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
                    # Close at end of day
                    exit_time = candle.timestamp
                    exit_price = candle.close
                    reason = "session end"

                return self._create_stock_trade_result(
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

    def _calculate_stock_metrics(self) -> StockBacktestMetrics:
        """Calculate STOCKS-specific performance metrics."""
        if not self.stock_trades:
            return StockBacktestMetrics(
                symbol=self._symbol,
                sector=self.sector,
                timeframe=self._timeframe,
                strategy=self._strategy_name,
                start_date=self._start_date,
                end_date=self._end_date,
                leverage=self.leverage,
                risk_percent=self.risk_percent,
                screening_criteria=self.screening_criteria,
                screened_symbols=self.screened_symbols,
            )

        winning = [t for t in self.stock_trades if t.result == "WIN"]
        losing = [t for t in self.stock_trades if t.result == "LOSS"]

        # Basic PnL calculations
        total_pnl_money = sum(t.pnl_money for t in self.stock_trades)
        total_pnl_points = sum(t.pnl_points for t in self.stock_trades)
        total_commission = sum(t.transaction_cost for t in self.stock_trades)

        # Profit factor
        wins_pnl = sum(t.pnl_money for t in winning) if winning else 0
        losses_pnl = abs(sum(t.pnl_money for t in losing)) if losing else 1
        profit_factor = wins_pnl / losses_pnl if losses_pnl > 0 else 0

        # Average R
        avg_r = sum(t.r_multiple for t in self.stock_trades) / len(self.stock_trades)

        # Expectancy
        expectancy = total_pnl_money / len(self.stock_trades)

        # Average shares
        avg_shares = (
            sum(t.volume for t in self.stock_trades) / len(self.stock_trades)
            if self.stock_trades
            else 0
        )

        # Average holding days
        total_holding_days = sum(t.holding_days for t in self.stock_trades)
        avg_holding_days = total_holding_days / len(self.stock_trades)

        # Average commission
        avg_commission = total_commission / len(self.stock_trades)

        # Capital calculations
        starting_capital = self.initial_balance
        ending_capital = self.initial_balance + total_pnl_money
        roi_percent = (
            ((ending_capital - starting_capital) / starting_capital * 100)
            if starting_capital > 0
            else 0
        )

        # Total return percentage
        total_return_percent = (
            ((ending_capital - starting_capital) / starting_capital * 100)
            if starting_capital > 0
            else 0
        )

        # Annualized return
        # Calculate days between start and end
        days_in_period = 1
        if self._start_date and self._end_date:
            try:
                start = datetime.strptime(self._start_date, "%Y-%m-%d")
                end = datetime.strptime(self._end_date, "%Y-%m-%d")
                days_in_period = max(1, (end - start).days)
            except ValueError:
                days_in_period = 1

        annual_return_percent = self._calculate_annualized_return(
            total_return_percent, days_in_period
        )

        # Volatility (annualized)
        volatility_percent = self._calculate_volatility()

        # Sharpe ratio
        sharpe_ratio = self._calculate_sharpe_ratio(annual_return_percent, volatility_percent)

        # Sortino ratio
        sortino_ratio = self._calculate_sortino_ratio(annual_return_percent)

        # Alpha and Beta calculations
        alpha, beta = self._calculate_alpha_beta(sharpe_ratio)

        # Max drawdown
        max_dd = 0
        peak = self.initial_balance
        for eq in self.equity_curve:
            if eq["equity"] > peak:
                peak = eq["equity"]
            dd = (peak - eq["equity"]) / peak * 100 if peak > 0 else 0
            if dd > max_dd:
                max_dd = dd

        # Sector-adjusted metrics
        sector_alpha = total_return_percent - self.sector_benchmark_return
        sector_relative_return = total_return_percent - self.sector_benchmark_return

        # Benchmark comparison
        benchmark_return = self._calculate_benchmark_return()
        alpha_vs_benchmark = total_return_percent - benchmark_return

        return StockBacktestMetrics(
            symbol=self._symbol,
            sector=self.sector,
            timeframe=self._timeframe,
            strategy=self._strategy_name,
            start_date=self._start_date,
            end_date=self._end_date,
            leverage=self.leverage,
            risk_percent=self.risk_percent,
            avg_shares=avg_shares,
            total_trades=len(self.stock_trades),
            winning_trades=len(winning),
            losing_trades=len(losing),
            win_rate=len(winning) / len(self.stock_trades) * 100,
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
            total_return_percent=total_return_percent,
            annual_return_percent=annual_return_percent,
            volatility_percent=volatility_percent,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            alpha=alpha,
            beta=beta,
            max_drawdown_percent=max_dd,
            avg_holding_days=avg_holding_days,
            total_commission=total_commission,
            avg_commission=avg_commission,
            sector_benchmark_return=self.sector_benchmark_return,
            sector_alpha=sector_alpha,
            sector_relative_return=sector_relative_return,
            benchmark_symbol=self.benchmark_symbol,
            benchmark_return=benchmark_return,
            alpha_vs_benchmark=alpha_vs_benchmark,
            beta_to_benchmark=beta,
            screening_criteria=self.screening_criteria,
            screened_symbols=self.screened_symbols,
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

        excess_return = annual_return / 100 - self.risk_free_rate
        return excess_return / (volatility / 100)

    def _calculate_sortino_ratio(self, annual_return: float) -> float:
        """Calculate Sortino ratio (downside risk only)."""
        if len(self.daily_returns) < 2:
            return 0.0

        # Calculate downside returns (negative returns only)
        downside_returns = [r for r in self.daily_returns if r < 0]

        if not downside_returns:
            return float('inf') if annual_return > 0 else 0.0

        # Calculate downside deviation
        downside_std = np.std(downside_returns, ddof=1)

        # Annualize downside deviation
        annualized_downside = downside_std * np.sqrt(252)

        if annualized_downside <= 0:
            return 0.0

        excess_return = annual_return / 100 - self.risk_free_rate
        return excess_return / annualized_downside

    def _calculate_alpha_beta(self, sharpe_ratio: float) -> tuple:
        """Calculate alpha and beta against benchmark."""
        # Simplified alpha/beta calculation
        # In production, would use regression against benchmark returns

        if len(self.benchmark_returns) < 2:
            # Estimate beta from Sharpe ratio (simplified)
            # Higher Sharpe typically indicates lower beta in this simplified model
            estimated_beta = 1.0 - (sharpe_ratio - 1.0) * 0.1
            estimated_beta = max(0.5, min(2.0, estimated_beta))  # Bound between 0.5 and 2.0

            # Alpha is excess return over what beta would predict
            # Simplified: assume market return of 10% annually
            market_return = 10.0
            strategy_return = self._calculate_stock_metrics().annual_return_percent
            alpha = strategy_return - (estimated_beta * market_return)

            return alpha, estimated_beta

        # Use actual benchmark returns for calculation
        strategy_returns = self.daily_returns

        if len(strategy_returns) != len(self.benchmark_returns):
            return 0.0, 1.0

        # Calculate beta using covariance/variance
        strategy_arr = np.array(strategy_returns)
        benchmark_arr = np.array(self.benchmark_returns)

        covariance = np.cov(strategy_arr, benchmark_arr)[0][1]
        benchmark_variance = np.var(benchmark_arr)

        if benchmark_variance == 0:
            beta = 1.0
        else:
            beta = covariance / benchmark_variance

        # Calculate alpha (intercept from regression)
        strategy_mean = np.mean(strategy_arr)
        benchmark_mean = np.mean(benchmark_arr)
        alpha_daily = strategy_mean - beta * benchmark_mean

        # Annualize alpha
        alpha_annual = alpha_daily * 252 * 100

        return alpha_annual, beta

    def _calculate_benchmark_return(self) -> float:
        """Calculate benchmark return from provided returns or config."""
        if self.benchmark_returns:
            # Calculate cumulative return from daily returns
            cumulative = 1.0
            for ret in self.benchmark_returns:
                cumulative *= (1 + ret)
            return (cumulative - 1) * 100

        # Default: assume 10% annual return if no benchmark data
        return 10.0

    def run_multi_stock(
        self,
        ohlcv_data_by_symbol: Dict[str, List[OHLCV]],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, StockBacktestMetrics]:
        """Run backtest across multiple stocks."""
        results = {}

        for symbol, ohlcv_data in ohlcv_data_by_symbol.items():
            # Update symbol in config
            self.config["symbol"] = symbol
            self._symbol = symbol
            self._sector = STOCK_SECTORS.get(symbol, "Unknown")
            self.sector = self._sector

            # Run backtest for this symbol
            metrics = self.run(ohlcv_data, start_date, end_date)
            results[symbol] = metrics

        return results

    def screen_stocks(
        self,
        symbols: List[str],
        criteria: Dict[str, Any],
    ) -> List[str]:
        """
        Screen stocks based on criteria.

        Args:
            symbols: List of symbols to screen
            criteria: Screening criteria (e.g., min_market_cap, max_pe, etc.)

        Returns:
            List of symbols that pass screening
        """
        screened = []

        for symbol in symbols:
            # Check sector
            if "sector" in criteria:
                if STOCK_SECTORS.get(symbol) != criteria["sector"]:
                    continue

            # Add symbol to screened list (simplified - in production would check actual data)
            screened.append(symbol)

        self.screened_symbols = screened
        self.screening_criteria = criteria

        return screened

    def export_trades(self, filename: str = "stock_backtest_trades.json") -> str:
        """Export STOCKS trades to JSON."""
        data = {
            "metrics": self._calculate_stock_metrics().to_dict(),
            "trades": [t.to_dict() for t in self.stock_trades],
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        return filename

    def format_summary(self, metrics: StockBacktestMetrics) -> str:
        """Format STOCKS metrics as readable summary."""
        return f"""
=== STOCKS Backtest Results ===

Symbol:     {metrics.symbol}
Sector:     {metrics.sector}
Timeframe:  {metrics.timeframe}
Strategy:   {metrics.strategy}
Period:     {metrics.start_date} to {metrics.end_date}

Capital:
  Starting:      ${metrics.starting_capital:,.2f}
  Ending:        ${metrics.ending_capital:,.2f}
  Gross PnL:     ${metrics.total_pnl_money:,.2f}
  ROI:           {metrics.roi_percent:.2f}%

Returns:
  Total Return:  {metrics.total_return_percent:.2f}%
  Annual Return: {metrics.annual_return_percent:.2f}%
  Volatility:    {metrics.volatility_percent:.2f}%

Risk-Adjusted:
  Sharpe Ratio:  {metrics.sharpe_ratio:.2f}
  Sortino Ratio: {metrics.sortino_ratio:.2f}
  Alpha:         {metrics.alpha:.2f}%
  Beta:          {metrics.beta:.2f}

Sector Performance:
  Sector Return: {metrics.sector_benchmark_return:.2f}%
  Sector Alpha:  {metrics.sector_alpha:.2f}%
  Relative:      {metrics.sector_relative_return:.2f}%

Benchmark Comparison:
  Benchmark:     {metrics.benchmark_symbol}
  Benchmark Ret: {metrics.benchmark_return:.2f}%
  Alpha vs BM:   {metrics.alpha_vs_benchmark:.2f}%
  Beta to BM:    {metrics.beta_to_benchmark:.2f}

Trades:
  Total:         {metrics.total_trades}
  Wins:          {metrics.winning_trades}
  Losses:        {metrics.losing_trades}
  Win Rate:      {metrics.win_rate:.1f}%
  Avg Holding:   {metrics.avg_holding_days:.1f} days

Costs:
  Total Comm:    ${metrics.total_commission:,.2f}
  Avg Comm:      ${metrics.avg_commission:.2f}

Performance:
  Profit Factor: {metrics.profit_factor:.2f}
  Average R:     {metrics.avg_r:.2f}
  Expectancy:    ${metrics.expectancy:.2f}
  Max Drawdown:  {metrics.max_drawdown_percent:.1f}%
"""

    def get_supported_timeframes(self) -> List[str]:
        """Get list of supported timeframes."""
        return STOCKS_TIMEFRAMES.copy()

    def get_sector(self, symbol: str) -> str:
        """Get sector for a symbol."""
        return STOCK_SECTORS.get(symbol, "Unknown")

    def get_sector_benchmark(self, sector: str) -> str:
        """Get benchmark ticker for a sector."""
        return SECTOR_BENCHMARKS.get(sector, "")

    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get information for a stock symbol."""
        return {
            "symbol": symbol,
            "sector": self.get_sector(symbol),
            "benchmark": self.get_sector_benchmark(self.get_sector(symbol)),
        }
