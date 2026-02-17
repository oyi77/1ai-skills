"""
Backtest Engine

Historical strategy testing with detailed metrics.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json

from ..brokers.base import OHLCV
from ..strategy.base import TradingSignal
from ..strategy.tradfi.commodities.xauusd_asia_7c_breakout.strategy import (
    XAUUSDAsia7CBreakout,
)


@dataclass
class TradeResult:
    """Result of a single trade."""

    entry_time: datetime
    exit_time: datetime
    symbol: str
    side: str  # BUY or SELL
    entry_price: float
    exit_price: float
    volume: float
    sl: float
    tp: float
    result: str  # WIN, LOSS, BREAKEVEN
    pnl_points: float
    pnl_money: float
    r_multiple: float  # R ratio
    reason: str  # TP hit, SL hit, cancelled

    def to_dict(self) -> Dict[str, Any]:
        return {
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
        }


@dataclass
class BacktestMetrics:
    """Backtest performance metrics."""

    pair: str = ""
    timeframe: str = ""
    strategy: str = ""
    start_date: str = ""
    end_date: str = ""
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pair": self.pair,
            "timeframe": self.timeframe,
            "strategy": self.strategy,
            "start_date": self.start_date,
            "end_date": self.end_date,
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
        }


class BacktestEngine:
    """Backtest engine for strategy testing."""

    def __init__(self, strategy, config: Optional[Dict[str, Any]] = None):
        self.strategy = strategy
        self.config = config or {}
        self.trades: List[TradeResult] = []
        self.equity_curve: List[Dict[str, Any]] = []

        # Default config
        self.initial_balance = self.config.get("initial_balance", 100)
        self.commission = self.config.get("commission", 0)
        self.spread_points = self.config.get("spread_points", 0)
        self.lot_size = self.config.get("lot_size", 0.01)
        self.leverage = self.config.get("leverage", 200)
        self.risk_percent = self.config.get("risk_percent", 1.0)

        # Metadata
        self._pair = self.config.get("pair", "XAUUSD")
        self._timeframe = self.config.get("timeframe", "H1")
        self._strategy_name = strategy.name if hasattr(strategy, "name") else "Strategy"
        self._start_date = ""
        self._end_date = ""

        # Risk manager for lot sizing
        from ..risk.manager import RiskManager, RiskConfig

        self.risk_manager = RiskManager(
            RiskConfig(leverage=self.leverage, risk_percent=self.risk_percent)
        )

    def run(
        self,
        ohlcv_data: List[OHLCV],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> BacktestMetrics:
        """Run backtest on historical data."""
        self.trades = []
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

            if len(day_data) < 10:  # Need enough candles
                continue

            # Generate signal
            signals = self.strategy.get_signals(day_data)

            if not signals:
                continue

            signal = signals[0]

            # Simulate pending order execution
            trade = self._simulate_trade(signal, day_data)

            if trade:
                self.trades.append(trade)

                # Update equity curve
                self._update_equity()

        # Calculate metrics
        metrics = self._calculate_metrics()

        return metrics

    def _get_trading_days(self, ohlcv_data: List[OHLCV]) -> List[datetime]:
        """Get unique trading dates from OHLCV data."""
        dates = set()
        for candle in ohlcv_data:
            # Get the timestamp, making it timezone-aware if needed
            ts = candle.timestamp
            if ts.tzinfo is None:
                # If naive, assume UTC
                import pytz

                ts = ts.replace(tzinfo=pytz.utc)
            dates.add(ts.date())

        # Return sorted dates, preserving timezone info from first candle if available
        first_ts = ohlcv_data[0].timestamp if ohlcv_data else None
        if first_ts and first_ts.tzinfo:
            tz = first_ts.tzinfo
            return sorted(
                [
                    datetime.combine(d, datetime.min.time()).replace(tzinfo=tz)
                    for d in dates
                ]
            )
        return sorted([datetime.combine(d, datetime.min.time()) for d in dates])

    def _get_day_data(self, ohlcv_data: List[OHLCV], date: datetime) -> List[OHLCV]:
        """Get OHLCV data for a specific day plus lookback for strategy."""
        # Get data from 5 days before to ensure we have enough lookback candles
        # (handles gaps in hourly data from weekends/holidays)
        if date.tzinfo is None:
            start = date.replace(hour=0, minute=0) - timedelta(days=5)
            end = date.replace(hour=23, minute=59, second=59)
        else:
            start = date.replace(hour=0, minute=0, second=0) - timedelta(days=5)
            end = date.replace(hour=23, minute=59, second=59)

        return [c for c in ohlcv_data if start <= c.timestamp <= end]

    def _simulate_trade(
        self, signal: TradingSignal, day_data: List[OHLCV]
    ) -> Optional[TradeResult]:
        """Simulate trade execution for a signal."""
        # Skip candles before signal generation (COA+3 must close)
        # Find index after COA+3
        signal_candle_idx = len(day_data) - 4  # Assume signal generated at last candle

        if signal_candle_idx >= len(day_data):
            return None

        # Simulate pending order execution
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
                exit_price = signal.buy_stop

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

                return self._create_trade_result(
                    signal,
                    "BUY",
                    entry_time,
                    exit_time,
                    signal.buy_stop,
                    exit_price,
                    reason,
                )

            # Check sell trigger
            if low <= signal.sell_stop:
                entry_time = candle.timestamp
                exit_price = signal.sell_stop

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

                return self._create_trade_result(
                    signal,
                    "SELL",
                    entry_time,
                    exit_time,
                    signal.sell_stop,
                    exit_price,
                    reason,
                )

        # No trigger - cancelled
        return None

    def _create_trade_result(
        self,
        signal: TradingSignal,
        side: str,
        entry_time: datetime,
        exit_time: datetime,
        entry_price: float,
        exit_price: float,
        reason: str,
    ) -> TradeResult:
        """Create trade result from execution."""
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

        # Calculate PnL
        if side == "BUY":
            pnl_points = exit_price - entry_price
        else:
            pnl_points = entry_price - exit_price

        # Convert to money: lot_size * pnl_points * point_value
        # For XAUUSD: point_value = 0.01, so 1 point = $0.01 per 0.01 lot
        pnl_money = pnl_points * lot_size

        # Determine result
        if pnl_points > 0:
            result = "WIN"
        elif pnl_points < 0:
            result = "LOSS"
        else:
            result = "BREAKEVEN"

        # Calculate R multiple
        r = signal.r_points
        r_multiple = pnl_points / r if r > 0 else 0

        return TradeResult(
            entry_time=entry_time,
            exit_time=exit_time,
            symbol=signal.symbol,
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
        )

    def _update_equity(self):
        """Update equity curve."""
        if not self.equity_curve:
            self.equity_curve.append(
                {
                    "time": datetime.now(),
                    "balance": self.initial_balance,
                    "equity": self.initial_balance,
                }
            )

        last_equity = self.equity_curve[-1]["equity"]
        last_trade = self.trades[-1]

        new_equity = last_equity + last_trade.pnl_money

        self.equity_curve.append(
            {"time": last_trade.exit_time, "balance": new_equity, "equity": new_equity}
        )

    def _calculate_metrics(self) -> BacktestMetrics:
        """Calculate performance metrics."""
        if not self.trades:
            return BacktestMetrics(
                pair=self._pair,
                timeframe=self._timeframe,
                strategy=self._strategy_name,
                start_date=self._start_date,
                end_date=self._end_date,
            )

        winning = [t for t in self.trades if t.result == "WIN"]
        losing = [t for t in self.trades if t.result == "LOSS"]

        total_pnl_money = sum(t.pnl_money for t in self.trades)
        total_pnl_points = sum(t.pnl_points for t in self.trades)

        wins_pnl = sum(t.pnl_money for t in winning) if winning else 0
        losses_pnl = abs(sum(t.pnl_money for t in losing)) if losing else 1

        profit_factor = wins_pnl / losses_pnl if losses_pnl > 0 else 0

        avg_r = sum(t.r_multiple for t in self.trades) / len(self.trades)

        expectancy = total_pnl_money / len(self.trades)

        # Capital calculations
        starting_capital = self.initial_balance
        ending_capital = self.initial_balance + total_pnl_money
        roi_percent = (
            ((ending_capital - starting_capital) / starting_capital) * 100
            if starting_capital > 0
            else 0
        )

        # Max drawdown
        max_dd = 0
        peak = self.initial_balance
        for eq in self.equity_curve:
            if eq["equity"] > peak:
                peak = eq["equity"]
            dd = (peak - eq["equity"]) / peak * 100
            if dd > max_dd:
                max_dd = dd

        return BacktestMetrics(
            pair=self._pair,
            timeframe=self._timeframe,
            strategy=self._strategy_name,
            start_date=self._start_date,
            end_date=self._end_date,
            total_trades=len(self.trades),
            winning_trades=len(winning),
            losing_trades=len(losing),
            win_rate=len(winning) / len(self.trades) * 100,
            total_pnl_points=total_pnl_points,
            total_pnl_money=total_pnl_money,
            avg_r=avg_r,
            profit_factor=profit_factor,
            max_drawdown_points=max_dd,
            expectancy=expectancy,
            starting_capital=starting_capital,
            ending_capital=ending_capital,
            roi_percent=roi_percent,
        )

    def export_trades(self, filename: str = "backtest_trades.json"):
        """Export trades to JSON."""
        data = {
            "metrics": self._calculate_metrics().to_dict(),
            "trades": [t.to_dict() for t in self.trades],
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        return filename

    def format_summary(self, metrics: BacktestMetrics) -> str:
        """Format metrics as readable summary."""
        return f"""
=== Backtest Results ===

Strategy: {metrics.strategy}
Pair:     {metrics.pair}
Timeframe: {metrics.timeframe}
Period:   {metrics.start_date} to {metrics.end_date}

Capital:
  Starting: ${metrics.starting_capital:,.2f}
  Ending:   ${metrics.ending_capital:,.2f}
  PnL:      ${metrics.total_pnl_money:,.2f}
  ROI:      {metrics.roi_percent:.2f}%

Trades:
  Total:    {metrics.total_trades}
  Wins:     {metrics.winning_trades}
  Losses:   {metrics.losing_trades}
  Win Rate: {metrics.win_rate:.1f}%

Performance:
  Total PnL (Points): {metrics.total_pnl_points:.1f}
  Average R: {metrics.avg_r:.2f}
  Profit Factor: {metrics.profit_factor:.2f}
  Expectancy: ${metrics.expectancy:.2f}
  Max Drawdown: {metrics.max_drawdown_points:.1f}%
"""
