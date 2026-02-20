"""
FOREX Backtest Engine

FOREX-specific backtesting with pips, spread cost, and correlation-adjusted returns.
Extends the base BacktestEngine for FOREX-specific requirements.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

from .engine import BacktestEngine, BacktestMetrics, TradeResult
from ..brokers.base import OHLCV
from ..strategy.base import TradingSignal


# FOREX pair configurations
FOREX_PAIRS = {
    "EUR/USD": {
        "pip_size": 0.0001,
        "tick_size": 0.00001,
        "standard_lot_units": 100000,
        "exchange_rate": 1.0,  # USD quote currency
    },
    "GBP/USD": {
        "pip_size": 0.0001,
        "tick_size": 0.00001,
        "standard_lot_units": 100000,
        "exchange_rate": 1.0,
    },
    "USD/JPY": {
        "pip_size": 0.01,
        "tick_size": 0.001,
        "standard_lot_units": 100000,
        "exchange_rate": 1.0,
    },
    "USD/CHF": {
        "pip_size": 0.0001,
        "tick_size": 0.00001,
        "standard_lot_units": 100000,
        "exchange_rate": 1.0,
    },
    "AUD/USD": {
        "pip_size": 0.0001,
        "tick_size": 0.00001,
        "standard_lot_units": 100000,
        "exchange_rate": 1.0,
    },
    "USD/CAD": {
        "pip_size": 0.0001,
        "tick_size": 0.00001,
        "standard_lot_units": 100000,
        "exchange_rate": 1.0,
    },
    "NZD/USD": {
        "pip_size": 0.0001,
        "tick_size": 0.00001,
        "standard_lot_units": 100000,
        "exchange_rate": 1.0,
    },
}

# Supported timeframes
FOREX_TIMEFRAMES = ["H1", "H4", "D1", "W1", "MN1"]

# Typical spreads in pips for major pairs (can be overridden in config)
TYPICAL_SPREADS = {
    "EUR/USD": 1.0,
    "GBP/USD": 1.5,
    "USD/JPY": 1.0,
    "USD/CHF": 1.5,
    "AUD/USD": 1.2,
    "USD/CAD": 1.5,
    "NZD/USD": 1.5,
}

# Correlation coefficients between major pairs (approximate)
PAIR_CORRELATIONS = {
    ("EUR/USD", "GBP/USD"): 0.89,
    ("EUR/USD", "AUD/USD"): 0.81,
    ("EUR/USD", "NZD/USD"): 0.78,
    ("GBP/USD", "AUD/USD"): 0.75,
    ("GBP/USD", "NZD/USD"): 0.72,
    ("USD/JPY", "USD/CHF"): -0.74,
    ("USD/JPY", "USD/CAD"): 0.68,
    ("EUR/USD", "USD/JPY"): -0.52,
}


@dataclass
class ForexTradeResult:
    """Extended trade result with FOREX-specific metrics."""

    # Base fields from TradeResult
    entry_time: datetime
    exit_time: datetime
    symbol: str
    side: str  # BUY or SELL
    entry_price: float
    exit_price: float
    volume: float  # In lots
    sl: float
    tp: float
    result: str  # WIN, LOSS, BREAKEVEN
    pnl_points: float
    pnl_money: float
    r_multiple: float
    reason: str

    # FOREX-specific fields
    pnl_pips: float = 0.0
    spread_cost_pips: float = 0.0
    spread_cost_money: float = 0.0
    net_pnl_pips: float = 0.0
    net_pnl_money: float = 0.0
    swap: float = 0.0  # Overnight swap/rollover
    commission: float = 0.0  # Commission in account currency

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
            "pnl_pips": self.pnl_pips,
            "spread_cost_pips": self.spread_cost_pips,
            "spread_cost_money": self.spread_cost_money,
            "net_pnl_pips": self.net_pnl_pips,
            "net_pnl_money": self.net_pnl_money,
            "swap": self.swap,
            "commission": self.commission,
        }
        return base


@dataclass
class ForexBacktestMetrics:
    """Extended metrics with FOREX-specific calculations."""

    # Base metrics
    pair: str = ""
    timeframe: str = ""
    strategy: str = ""
    start_date: str = ""
    end_date: str = ""
    leverage: int = 100
    risk_percent: float = 1.0
    avg_lot_size: float = 0.0
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

    # FOREX-specific metrics
    total_pnl_pips: float = 0.0
    avg_pnl_pips: float = 0.0
    total_spread_cost_pips: float = 0.0
    total_spread_cost_money: float = 0.0
    net_pnl_pips: float = 0.0
    net_pnl_money: float = 0.0
    avg_spread_cost_pips: float = 0.0
    spread_impact_percent: float = 0.0  # How much spread reduces returns
    avg_trade_duration_hours: float = 0.0
    total_swap: float = 0.0
    total_commission: float = 0.0

    # Correlation-adjusted metrics
    correlation_adjustment: float = 0.0
    risk_adjusted_return: float = 0.0  # Sharpe-like ratio using pips
    sharpe_ratio: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        base = {
            "pair": self.pair,
            "timeframe": self.timeframe,
            "strategy": self.strategy,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "leverage": self.leverage,
            "risk_percent": self.risk_percent,
            "avg_lot_size": self.avg_lot_size,
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
            "total_pnl_pips": self.total_pnl_pips,
            "avg_pnl_pips": self.avg_pnl_pips,
            "total_spread_cost_pips": self.total_spread_cost_pips,
            "total_spread_cost_money": self.total_spread_cost_money,
            "net_pnl_pips": self.net_pnl_pips,
            "net_pnl_money": self.net_pnl_money,
            "avg_spread_cost_pips": self.avg_spread_cost_pips,
            "spread_impact_percent": self.spread_impact_percent,
            "avg_trade_duration_hours": self.avg_trade_duration_hours,
            "total_swap": self.total_swap,
            "total_commission": self.total_commission,
            "correlation_adjustment": self.correlation_adjustment,
            "risk_adjusted_return": self.risk_adjusted_return,
            "sharpe_ratio": self.sharpe_ratio,
        }
        return base


class ForexBacktestEngine(BacktestEngine):
    """
    FOREX-specific backtest engine.

    Extends the base BacktestEngine with:
    - Pip-based calculations and metrics
    - Spread cost modeling
    - Correlation-adjusted returns
    - Support for major FOREX pairs
    - Multiple timeframe support
    """

    def __init__(self, strategy, config: Optional[Dict[str, Any]] = None):
        # Initialize base class
        super().__init__(strategy, config)

        # Override defaults for FOREX
        self._pair = self.config.get("pair", "EUR/USD")
        self._timeframe = self.config.get("timeframe", "H1")

        # Validate pair
        if self._pair not in FOREX_PAIRS:
            raise ValueError(
                f"Unsupported FOREX pair: {self._pair}. "
                f"Supported: {list(FOREX_PAIRS.keys())}"
            )

        # Validate timeframe
        if self._timeframe not in FOREX_TIMEFRAMES:
            raise ValueError(
                f"Unsupported timeframe: {self._timeframe}. "
                f"Supported: {FOREX_TIMEFRAMES}"
            )

        # FOREX-specific configuration
        pair_config = FOREX_PAIRS[self._pair]
        self.pip_size = pair_config["pip_size"]
        self.tick_size = pair_config["tick_size"]
        self.standard_lot_units = pair_config["standard_lot_units"]

        # Spread configuration (in pips)
        self.spread_pips = self.config.get("spread_pips", TYPICAL_SPREADS.get(self._pair, 1.5))

        # Commission (per lot, in account currency)
        self.commission_per_lot = self.config.get("commission_per_lot", 0.0)

        # Swap configuration (per lot per night)
        self.swap_rate = self.config.get("swap_rate", 0.0)

        # Correlation pairs for multi-pair analysis
        self.correlation_pairs = self.config.get("correlation_pairs", [])

        # Store FOREX-specific trades
        self.forex_trades: List[ForexTradeResult] = []

    def _calculate_pips(self, price_change: float) -> float:
        """Convert price change to pips."""
        return price_change / self.pip_size

    def _calculate_spread_cost(
        self, lot_size: float, spread_pips: Optional[float] = None
    ) -> tuple:
        """Calculate spread cost in pips and money."""
        spread = spread_pips if spread_pips is not None else self.spread_pips

        # Spread cost in pips (fixed per trade regardless of direction)
        spread_cost_pips = spread

        # Spread cost in money: spread_pips * pip_value_per_lot * lots
        # Pip value per standard lot = 10 units of quote currency (for most pairs)
        pip_value_per_lot = 10.0  # Standard for pairs with USD as quote
        spread_cost_money = spread * pip_value_per_lot * lot_size

        return spread_cost_pips, spread_cost_money

    def _calculate_swap(
        self, lot_size: float, hours_held: int, side: str
    ) -> float:
        """Calculate overnight swap."""
        if hours_held < 24:
            return 0.0

        # Calculate number of nights
        nights = hours_held // 24

        # Swap is typically charged per lot per night
        # Positive for long (BUY), negative for short (SELL) depending on pair
        swap_per_night = self.swap_rate
        if side == "SELL":
            swap_per_night = -swap_per_night

        return swap_per_night * lot_size * nights

    def _create_forex_trade_result(
        self,
        signal: TradingSignal,
        side: str,
        entry_time: datetime,
        exit_time: datetime,
        entry_price: float,
        exit_price: float,
        reason: str,
    ) -> ForexTradeResult:
        """Create FOREX-specific trade result."""
        # Get current account balance for lot sizing
        current_balance = self.initial_balance
        if self.trades:
            last_trade = self.trades[-1]
            current_balance = self.initial_balance + sum(
                t.pnl_money for t in self.trades
            )

        # Calculate lot size using risk manager
        sl_price = signal.buy_sl if side == "BUY" else signal.sell_sl
        lot_result = self.risk_manager.calculate_lot_size(
            account_balance=current_balance,
            entry_price=entry_price,
            sl_price=sl_price,
            risk_percent=self.risk_percent,
            leverage=self.leverage,
        )
        lot_size = lot_result["lot_size"]

        # Calculate PnL in price points
        if side == "BUY":
            pnl_points = exit_price - entry_price
        else:
            pnl_points = entry_price - exit_price

        # Convert to pips
        pnl_pips = self._calculate_pips(pnl_points)

        # Calculate spread cost
        spread_cost_pips, spread_cost_money = self._calculate_spread_cost(lot_size)

        # Net PnL after spread
        net_pnl_pips = pnl_pips - spread_cost_pips

        # Convert to money
        # Pip value per lot = 10 for most pairs, adjust for JPY
        if "JPY" in self._pair:
            pip_value_per_lot = 1000.0  # JPY pairs have different pip value
        else:
            pip_value_per_lot = 10.0

        pnl_money = pnl_pips * pip_value_per_lot * lot_size
        net_pnl_money = net_pnl_pips * pip_value_per_lot * lot_size

        # Calculate commission
        commission = self.commission_per_lot * lot_size

        # Calculate swap (overnight charges)
        hours_held = int((exit_time - entry_time).total_seconds() / 3600)
        swap = self._calculate_swap(lot_size, hours_held, side)

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

        return ForexTradeResult(
            entry_time=entry_time,
            exit_time=exit_time,
            symbol=signal.symbol or self._pair,
            side=side,
            entry_price=entry_price,
            exit_price=exit_price,
            volume=lot_size,
            sl=signal.buy_sl if side == "BUY" else signal.sell_sl,
            tp=signal.buy_tp if side == "BUY" else signal.sell_tp,
            result=result,
            pnl_points=pnl_points,
            pnl_money=pnl_money,
            r_multiple=r_multiple,
            reason=reason,
            pnl_pips=pnl_pips,
            spread_cost_pips=spread_cost_pips,
            spread_cost_money=spread_cost_money,
            net_pnl_pips=net_pnl_pips,
            net_pnl_money=net_pnl_money,
            swap=swap,
            commission=commission,
        )

    def run(
        self,
        ohlcv_data: List[OHLCV],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> ForexBacktestMetrics:
        """Run backtest on historical FOREX data."""
        self.trades = []
        self.forex_trades = []
        self.equity_curve = []

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
            trade = self._simulate_forex_trade(signal, day_data)

            if trade:
                self.trades.append(trade)
                self.forex_trades.append(trade)

                # Update equity curve
                self._update_equity()

        # Calculate FOREX-specific metrics
        metrics = self._calculate_forex_metrics()

        return metrics

    def _simulate_forex_trade(
        self, signal: TradingSignal, day_data: List[OHLCV]
    ) -> Optional[ForexTradeResult]:
        """Simulate trade execution for FOREX with spread modeling."""
        signal_candle_idx = len(day_data) - 4

        if signal_candle_idx >= len(day_data):
            return None

        entry_time = None
        exit_time = None
        exit_price = None
        reason = ""

        # Account for spread in entry price
        # For BUY: entry at ask (higher), for SELL: entry at bid (lower)
        for i in range(signal_candle_idx + 1, len(day_data)):
            candle = day_data[i]
            high = candle.high
            low = candle.low

            # Check buy trigger (buy stop above current price)
            if high >= signal.buy_stop:
                entry_time = candle.timestamp
                # Entry at buy stop + spread adjustment
                entry_price = signal.buy_stop + (self.spread_pips * self.pip_size)

                # Check TP (adjusted for spread)
                tp_with_spread = signal.buy_tp - (self.spread_pips * self.pip_size)
                if high >= tp_with_spread:
                    exit_time = candle.timestamp
                    exit_price = tp_with_spread
                    reason = "TP hit"
                # Check SL
                elif low <= signal.buy_sl:
                    exit_time = candle.timestamp
                    exit_price = signal.buy_sl
                    reason = "SL hit"
                else:
                    exit_time = candle.timestamp
                    exit_price = candle.close - (self.spread_pips * self.pip_size)
                    reason = "session end"

                return self._create_forex_trade_result(
                    signal,
                    "BUY",
                    entry_time,
                    exit_time,
                    entry_price,
                    exit_price,
                    reason,
                )

            # Check sell trigger (sell stop below current price)
            if low <= signal.sell_stop:
                entry_time = candle.timestamp
                # Entry at sell stop - spread adjustment
                entry_price = signal.sell_stop - (self.spread_pips * self.pip_size)

                # Check TP (adjusted for spread)
                tp_with_spread = signal.sell_tp + (self.spread_pips * self.pip_size)
                if low <= tp_with_spread:
                    exit_time = candle.timestamp
                    exit_price = tp_with_spread
                    reason = "TP hit"
                # Check SL
                elif high >= signal.sell_sl:
                    exit_time = candle.timestamp
                    exit_price = signal.sell_sl
                    reason = "SL hit"
                else:
                    exit_time = candle.timestamp
                    exit_price = candle.close + (self.spread_pips * self.pip_size)
                    reason = "session end"

                return self._create_forex_trade_result(
                    signal,
                    "SELL",
                    entry_time,
                    exit_time,
                    entry_price,
                    exit_price,
                    reason,
                )

        return None

    def _calculate_forex_metrics(self) -> ForexBacktestMetrics:
        """Calculate FOREX-specific performance metrics."""
        if not self.forex_trades:
            return ForexBacktestMetrics(
                pair=self._pair,
                timeframe=self._timeframe,
                strategy=self._strategy_name,
                start_date=self._start_date,
                end_date=self._end_date,
                leverage=self.leverage,
                risk_percent=self.risk_percent,
            )

        winning = [t for t in self.forex_trades if t.result == "WIN"]
        losing = [t for t in self.forex_trades if t.result == "LOSS"]

        # Basic PnL calculations
        total_pnl_money = sum(t.pnl_money for t in self.forex_trades)
        total_pnl_points = sum(t.pnl_points for t in self.forex_trades)
        total_pnl_pips = sum(t.pnl_pips for t in self.forex_trades)

        # Spread costs
        total_spread_cost_pips = sum(t.spread_cost_pips for t in self.forex_trades)
        total_spread_cost_money = sum(t.spread_cost_money for t in self.forex_trades)

        # Net PnL after spread
        net_pnl_pips = total_pnl_pips - total_spread_cost_pips
        net_pnl_money = total_pnl_money - total_spread_cost_money

        # Other costs
        total_swap = sum(t.swap for t in self.forex_trades)
        total_commission = sum(t.commission for t in self.forex_trades)

        # Profit factor
        wins_pnl = sum(t.pnl_money for t in winning) if winning else 0
        losses_pnl = abs(sum(t.pnl_money for t in losing)) if losing else 1
        profit_factor = wins_pnl / losses_pnl if losses_pnl > 0 else 0

        # Average R
        avg_r = sum(t.r_multiple for t in self.forex_trades) / len(self.forex_trades)

        # Expectancy
        expectancy = total_pnl_money / len(self.forex_trades)

        # Average lot size
        avg_lot = (
            sum(t.volume for t in self.forex_trades) / len(self.forex_trades)
            if self.forex_trades
            else 0
        )

        # Average spread cost
        avg_spread_cost_pips = (
            total_spread_cost_pips / len(self.forex_trades)
            if self.forex_trades
            else 0
        )

        # Spread impact (percentage of gross PnL lost to spread)
        gross_pnl = abs(total_pnl_money)
        spread_impact_percent = (
            (total_spread_cost_money / gross_pnl * 100) if gross_pnl > 0 else 0
        )

        # Average trade duration
        total_hours = sum(
            (t.exit_time - t.entry_time).total_seconds() / 3600
            for t in self.forex_trades
        )
        avg_trade_duration_hours = total_hours / len(self.forex_trades)

        # Capital calculations
        starting_capital = self.initial_balance
        ending_capital = self.initial_balance + total_pnl_money
        roi_percent = (
            ((ending_capital - starting_capital) / starting_capital * 100)
            if starting_capital > 0
            else 0
        )

        # Max drawdown
        max_dd = 0
        peak = self.initial_balance
        for eq in self.equity_curve:
            if eq["equity"] > peak:
                peak = eq["equity"]
            dd = (peak - eq["equity"]) / peak * 100 if peak > 0 else 0
            if dd > max_dd:
                max_dd = dd

        # Correlation adjustment
        correlation_adjustment = self._calculate_correlation_adjustment()

        # Risk-adjusted return (similar to Sharpe using pips)
        if len(self.forex_trades) > 1:
            pips_returns = [t.net_pnl_pips for t in self.forex_trades]
            avg_return = sum(pips_returns) / len(pips_returns)
            variance = sum((r - avg_return) ** 2 for r in pips_returns) / len(pips_returns)
            std_dev = variance ** 0.5
            risk_adjusted_return = avg_return / std_dev if std_dev > 0 else 0
        else:
            risk_adjusted_return = 0

        # Sharpe ratio (using money returns)
        if len(self.forex_trades) > 1:
            money_returns = [t.net_pnl_money for t in self.forex_trades]
            avg_money = sum(money_returns) / len(money_returns)
            money_variance = sum((r - avg_money) ** 2 for r in money_returns) / len(money_returns)
            money_std = money_variance ** 0.5
            sharpe_ratio = (avg_money / money_std) if money_std > 0 else 0
        else:
            sharpe_ratio = 0

        return ForexBacktestMetrics(
            pair=self._pair,
            timeframe=self._timeframe,
            strategy=self._strategy_name,
            start_date=self._start_date,
            end_date=self._end_date,
            leverage=self.leverage,
            risk_percent=self.risk_percent,
            avg_lot_size=avg_lot,
            total_trades=len(self.forex_trades),
            winning_trades=len(winning),
            losing_trades=len(losing),
            win_rate=len(winning) / len(self.forex_trades) * 100,
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
            total_pnl_pips=total_pnl_pips,
            avg_pnl_pips=total_pnl_pips / len(self.forex_trades) if self.forex_trades else 0,
            total_spread_cost_pips=total_spread_cost_pips,
            total_spread_cost_money=total_spread_cost_money,
            net_pnl_pips=net_pnl_pips,
            net_pnl_money=net_pnl_money,
            avg_spread_cost_pips=avg_spread_cost_pips,
            spread_impact_percent=spread_impact_percent,
            avg_trade_duration_hours=avg_trade_duration_hours,
            total_swap=total_swap,
            total_commission=total_commission,
            correlation_adjustment=correlation_adjustment,
            risk_adjusted_return=risk_adjusted_return,
            sharpe_ratio=sharpe_ratio,
        )

    def _calculate_correlation_adjustment(self) -> float:
        """Calculate correlation adjustment for multi-pair strategies."""
        if not self.correlation_pairs or len(self.correlation_pairs) < 2:
            return 0.0

        # Calculate average correlation with configured pairs
        total_corr = 0.0
        count = 0

        for pair in self.correlation_pairs:
            # Check both directions of pair tuple
            key1 = (self._pair, pair)
            key2 = (pair, self._pair)

            if key1 in PAIR_CORRELATIONS:
                total_corr += PAIR_CORRELATIONS[key1]
                count += 1
            elif key2 in PAIR_CORRELATIONS:
                total_corr += PAIR_CORRELATIONS[key2]
                count += 1

        if count > 0:
            return total_corr / count
        return 0.0

    def export_trades(self, filename: str = "forex_backtest_trades.json") -> str:
        """Export FOREX trades to JSON."""
        data = {
            "metrics": self._calculate_forex_metrics().to_dict(),
            "trades": [t.to_dict() for t in self.forex_trades],
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        return filename

    def format_summary(self, metrics: ForexBacktestMetrics) -> str:
        """Format FOREX metrics as readable summary."""
        return f"""
=== FOREX Backtest Results ===

Strategy:  {metrics.strategy}
Pair:      {metrics.pair}
Timeframe: {metrics.timeframe}
Period:    {metrics.start_date} to {metrics.end_date}

Capital:
  Starting:      ${metrics.starting_capital:,.2f}
  Ending:        ${metrics.ending_capital:,.2f}
  Gross PnL:     ${metrics.total_pnl_money:,.2f}
  Net PnL:       ${metrics.net_pnl_money:,.2f}
  ROI:           {metrics.roi_percent:.2f}%

Pips Analysis:
  Gross PnL:     {metrics.total_pnl_pips:.1f} pips
  Net PnL:       {metrics.net_pnl_pips:.1f} pips
  Avg PnL/Trade: {metrics.avg_pnl_pips:.2f} pips

Spread Impact:
  Total Cost:    {metrics.total_spread_cost_pips:.1f} pips (${metrics.total_spread_cost_money:,.2f})
  Avg Cost:      {metrics.avg_spread_cost_pips:.2f} pips/trade
  Impact:        {metrics.spread_impact_percent:.1f}% of gross PnL

Costs:
  Commission:    ${metrics.total_commission:,.2f}
  Swap:          ${metrics.total_swap:,.2f}

Trades:
  Total:         {metrics.total_trades}
  Wins:          {metrics.winning_trades}
  Losses:        {metrics.losing_trades}
  Win Rate:      {metrics.win_rate:.1f}%
  Avg Duration:  {metrics.avg_trade_duration_hours:.1f} hours

Performance:
  Profit Factor: {metrics.profit_factor:.2f}
  Average R:     {metrics.avg_r:.2f}
  Expectancy:    ${metrics.expectancy:.2f}
  Max Drawdown:  {metrics.max_drawdown_points:.1f}%

Risk-Adjusted:
  Sharpe Ratio:  {metrics.sharpe_ratio:.2f}
  Risk-Adj Ret:  {metrics.risk_adjusted_return:.2f}
  Correlation:   {metrics.correlation_adjustment:.2f}
"""

    def get_supported_pairs(self) -> List[str]:
        """Get list of supported FOREX pairs."""
        return list(FOREX_PAIRS.keys())

    def get_supported_timeframes(self) -> List[str]:
        """Get list of supported timeframes."""
        return FOREX_TIMEFRAMES.copy()

    def get_pair_info(self, pair: str) -> Dict[str, Any]:
        """Get configuration info for a FOREX pair."""
        if pair not in FOREX_PAIRS:
            raise ValueError(f"Unknown pair: {pair}")
        return FOREX_PAIRS[pair]
