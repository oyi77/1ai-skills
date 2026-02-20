"""
CRYPTO Backtest Engine

CRYPTO-specific backtesting with 24/7 trading, funding-adjusted returns,
and volatility-adjusted performance. Extends the base BacktestEngine for
CRYPTO-specific requirements.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json

from .engine import BacktestEngine, BacktestMetrics, TradeResult
from ..brokers.base import OHLCV
from ..strategy.base import TradingSignal


# CRYPTO pair configurations (spot and perpetual futures)
CRYPTO_PAIRS = {
    # Spot pairs
    "BTC/USD": {
        "tick_size": 0.01,
        "contract_size": 1.0,  # 1 BTC per unit
        "quote_currency": "USD",
        "min_lot": 0.001,  # Minimum 0.001 BTC
        "price_precision": 2,
        "quantity_precision": 6,
    },
    "ETH/USD": {
        "tick_size": 0.01,
        "contract_size": 1.0,  # 1 ETH per unit
        "quote_currency": "USD",
        "min_lot": 0.001,  # Minimum 0.001 ETH
        "price_precision": 2,
        "quantity_precision": 6,
    },
    # Perpetual futures pairs
    "BTC/USDT": {
        "tick_size": 0.01,
        "contract_size": 1.0,  # 1 BTC per contract
        "quote_currency": "USDT",
        "min_lot": 1.0,  # Minimum 1 contract
        "price_precision": 2,
        "quantity_precision": 0,
    },
    "ETH/USDT": {
        "tick_size": 0.01,
        "contract_size": 1.0,  # 1 ETH per contract
        "quote_currency": "USDT",
        "min_lot": 1.0,  # Minimum 1 contract
        "price_precision": 2,
        "quantity_precision": 0,
    },
}

# Supported timeframes (crypto uses more granular timeframes)
CRYPTO_TIMEFRAMES = ["1m", "5m", "15m", "30m", "1h", "4h", "6h", "12h", "1d", "1w"]

# Typical funding rates (per 8 hours for perpetuals) - approximate values
TYPICAL_FUNDING_RATES = {
    "BTC/USD": 0.0001,  # 0.01% per 8h
    "ETH/USD": 0.0001,  # 0.01% per 8h
    "BTC/USDT": 0.0001,
    "ETH/USDT": 0.0001,
}

# Average funding intervals (in hours)
FUNDING_INTERVAL_HOURS = 8

# Typical maker/taker fees for major exchanges
TYPICAL_FEES = {
    "binance": {"maker": 0.0001, "taker": 0.0002},  # 0.01% / 0.02%
    "bybit": {"maker": 0.0001, "taker": 0.0002},
    "okx": {"maker": 0.0001, "taker": 0.0002},
    "default": {"maker": 0.0002, "taker": 0.0004},
}

# Historical volatility lookback periods (in hours)
VOLATILITY_PERIODS = {
    "short": 24,    # 24-hour volatility
    "medium": 168,  # 1-week volatility
    "long": 720,    # 30-day volatility
}


@dataclass
class CryptoTradeResult:
    """Extended trade result with CRYPTO-specific metrics."""

    # Base fields from TradeResult
    entry_time: datetime
    exit_time: datetime
    symbol: str
    side: str  # BUY or SELL
    entry_price: float
    exit_price: float
    volume: float  # In units (BTC, ETH, etc.)
    sl: float
    tp: float
    result: str  # WIN, LOSS, BREAKEVEN
    pnl_points: float
    pnl_money: float
    r_multiple: float
    reason: str

    # CRYPTO-specific fields
    funding_cost: float = 0.0  # Funding payments during hold
    funding_adjusted_pnl: float = 0.0  # PnL after funding
    fees: float = 0.0  # Trading fees (maker/taker)
    volatility: float = 0.0  # Realized volatility during trade
    sharpe_contribution: float = 0.0  # Trade's contribution to Sharpe
    max_favorable_excursion: float = 0.0  # MFE
    max_adverse_excursion: float = 0.0  # MAE
    hold_time_hours: float = 0.0  # Duration in hours

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
            "funding_cost": self.funding_cost,
            "funding_adjusted_pnl": self.funding_adjusted_pnl,
            "fees": self.fees,
            "volatility": self.volatility,
            "sharpe_contribution": self.sharpe_contribution,
            "max_favorable_excursion": self.max_favorable_excursion,
            "max_adverse_excursion": self.max_adverse_excursion,
            "hold_time_hours": self.hold_time_hours,
        }
        return base


@dataclass
class CryptoBacktestMetrics:
    """Extended metrics with CRYPTO-specific calculations."""

    # Base metrics
    pair: str = ""
    timeframe: str = ""
    strategy: str = ""
    start_date: str = ""
    end_date: str = ""
    leverage: int = 10
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

    # CRYPTO-specific metrics
    total_funding_cost: float = 0.0
    funding_adjusted_pnl: float = 0.0
    total_fees: float = 0.0
    avg_funding_cost: float = 0.0
    avg_fees: float = 0.0
    avg_volatility: float = 0.0
    avg_hold_time_hours: float = 0.0

    # Volatility-adjusted metrics
    volatility_adjusted_return: float = 0.0  # Return / Volatility
    sortino_ratio: float = 0.0  # Similar to Sharpe but downside deviation
    calmar_ratio: float = 0.0  # Annualized return / Max drawdown

    # Funding-adjusted metrics
    funding_impact_percent: float = 0.0  # How much funding affects returns
    net_funding_yield: float = 0.0  # Annualized funding yield

    # Trade quality metrics
    avg_mfe: float = 0.0  # Average max favorable excursion
    avg_mae: float = 0.0  # Average max adverse excursion
    mfe_ma_ratio: float = 0.0  # MFE/MAE ratio (trade quality)
    avg_sharpe_contribution: float = 0.0

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
            "total_funding_cost": self.total_funding_cost,
            "funding_adjusted_pnl": self.funding_adjusted_pnl,
            "total_fees": self.total_fees,
            "avg_funding_cost": self.avg_funding_cost,
            "avg_fees": self.avg_fees,
            "avg_volatility": self.avg_volatility,
            "avg_hold_time_hours": self.avg_hold_time_hours,
            "volatility_adjusted_return": self.volatility_adjusted_return,
            "sortino_ratio": self.sortino_ratio,
            "calmar_ratio": self.calmar_ratio,
            "funding_impact_percent": self.funding_impact_percent,
            "net_funding_yield": self.net_funding_yield,
            "avg_mfe": self.avg_mfe,
            "avg_mae": self.avg_mae,
            "mfe_ma_ratio": self.mfe_ma_ratio,
            "avg_sharpe_contribution": self.avg_sharpe_contribution,
        }
        return base


class CryptoBacktestEngine(BacktestEngine):
    """
    CRYPTO-specific backtest engine.

    Extends the base BacktestEngine with:
    - 24/7 trading support (continuous markets)
    - Funding rate calculations (for perpetual futures)
    - Volatility-adjusted performance metrics
    - Support for major crypto pairs (BTC/USD, ETH/USD)
    - Integration with CCXT broker
    - Higher leverage support
    - Fee modeling (maker/taker)
    """

    def __init__(self, strategy, config: Optional[Dict[str, Any]] = None):
        # Initialize base class
        super().__init__(strategy, config)

        # Override defaults for CRYPTO
        self._pair = self.config.get("pair", "BTC/USD")
        self._timeframe = self.config.get("timeframe", "1h")

        # Validate pair
        if self._pair not in CRYPTO_PAIRS:
            raise ValueError(
                f"Unsupported CRYPTO pair: {self._pair}. "
                f"Supported: {list(CRYPTO_PAIRS.keys())}"
            )

        # Validate timeframe
        if self._timeframe not in CRYPTO_TIMEFRAMES:
            raise ValueError(
                f"Unsupported timeframe: {self._timeframe}. "
                f"Supported: {CRYPTO_TIMEFRAMES}"
            )

        # CRYPTO-specific configuration
        pair_config = CRYPTO_PAIRS[self._pair]
        self.tick_size = pair_config["tick_size"]
        self.contract_size = pair_config["contract_size"]
        self.quote_currency = pair_config["quote_currency"]
        self.min_lot = pair_config["min_lot"]
        self.price_precision = pair_config["price_precision"]
        self.quantity_precision = pair_config["quantity_precision"]

        # Funding rate (per 8 hours, for perpetuals)
        self.funding_rate = self.config.get(
            "funding_rate", TYPICAL_FUNDING_RATES.get(self._pair, 0.0001)
        )
        self.funding_interval = self.config.get("funding_interval_hours", FUNDING_INTERVAL_HOURS)

        # Fee configuration
        exchange_id = self.config.get("exchange_id", "default")
        self.fees = TYPICAL_FEES.get(exchange_id, TYPICAL_FEES["default"])
        self.maker_fee = self.config.get("maker_fee", self.fees["maker"])
        self.taker_fee = self.config.get("taker_fee", self.fees["taker"])

        # Volatility calculation settings
        self.volatility_lookback = self.config.get("volatility_lookback", 24)

        # Store CRYPTO-specific trades
        self.crypto_trades: List[CryptoTradeResult] = []

    def _calculate_funding_cost(
        self, entry_time: datetime, exit_time: datetime, position_value: float, side: str
    ) -> float:
        """Calculate funding cost for holding position."""
        # Funding only applies to perpetual futures
        if "USD" not in self._pair and "USDT" not in self._pair:
            return 0.0

        # Calculate hours held
        hours_held = (exit_time - entry_time).total_seconds() / 3600

        # Number of funding periods
        num_funding_periods = max(0, int(hours_held / self.funding_interval))

        if num_funding_periods == 0:
            return 0.0

        # Funding rate sign depends on position side
        # Long positions pay/receive based on funding rate sign
        funding_cost = position_value * self.funding_rate * num_funding_periods

        # For simplicity, assume long pays, short receives (typical for crypto)
        # This can be adjusted based on actual funding rate sign
        if side == "BUY":
            return -funding_cost  # Long pays funding
        else:
            return funding_cost  # Short receives funding

    def _calculate_fees(self, volume: float, entry_price: float, exit_price: float) -> float:
        """Calculate trading fees."""
        # Calculate notional value for each trade
        entry_notional = volume * entry_price
        exit_notional = volume * exit_price

        # Assume taker fee for market orders (most common in backtesting)
        entry_fee = entry_notional * self.taker_fee
        exit_fee = exit_notional * self.taker_fee

        return entry_fee + exit_fee

    def _calculate_volatility(self, ohlcv_data: List[OHLCV], lookback: Optional[int] = None) -> float:
        """Calculate realized volatility from OHLCV data."""
        if not ohlcv_data:
            return 0.0

        lookback = lookback or self.volatility_lookback
        data_slice = ohlcv_data[-lookback:] if len(ohlcv_data) > lookback else ohlcv_data

        if len(data_slice) < 2:
            return 0.0

        # Calculate returns
        returns = []
        for i in range(1, len(data_slice)):
            if data_slice[i-1].close > 0:
                ret = (data_slice[i].close - data_slice[i-1].close) / data_slice[i-1].close
                returns.append(ret)

        if not returns:
            return 0.0

        # Calculate standard deviation of returns (annualized)
        import statistics
        std_dev = statistics.stdev(returns) if len(returns) > 1 else 0.0

        # Annualize volatility (assuming hourly data = 8760 periods/year)
        periods_per_year = {
            "1m": 525600,
            "5m": 105120,
            "15m": 35040,
            "30m": 17520,
            "1h": 8760,
            "4h": 2190,
            "6h": 1460,
            "12h": 730,
            "1d": 365,
            "1w": 52,
        }
        periods = periods_per_year.get(self._timeframe, 8760)
        annualized_vol = std_dev * (periods ** 0.5)

        return annualized_vol

    def _calculate_mfe_mae(
        self, signal: TradingSignal, day_data: List[OHLCV], side: str
    ) -> tuple:
        """Calculate Max Favorable and Max Adverse Excursion."""
        signal_candle_idx = len(day_data) - 4

        mfe = 0.0  # Max Favorable Excursion
        mae = 0.0  # Max Adverse Excursion

        # Find entry price
        entry_price = signal.buy_stop if side == "BUY" else signal.sell_stop

        for i in range(signal_candle_idx + 1, len(day_data)):
            candle = day_data[i]

            if side == "BUY":
                # Favorable: price goes up
                favorable = candle.high - entry_price
                # Adverse: price goes down
                adverse = entry_price - candle.low
            else:
                # Favorable: price goes down
                favorable = entry_price - candle.low
                # Adverse: price goes up
                adverse = candle.high - entry_price

            mfe = max(mfe, favorable)
            mae = max(mae, adverse)

        return mfe, mae

    def _create_crypto_trade_result(
        self,
        signal: TradingSignal,
        side: str,
        entry_time: datetime,
        exit_time: datetime,
        entry_price: float,
        exit_price: float,
        reason: str,
        ohlcv_data: List[OHLCV],
    ) -> CryptoTradeResult:
        """Create CRYPTO-specific trade result."""
        # Get current account balance for position sizing
        current_balance = self.initial_balance
        if self.trades:
            last_trade = self.trades[-1]
            current_balance = self.initial_balance + sum(
                t.pnl_money for t in self.trades
            )

        # Calculate position size using risk manager
        sl_price = signal.buy_sl if side == "BUY" else signal.sell_sl
        lot_result = self.risk_manager.calculate_lot_size(
            account_balance=current_balance,
            entry_price=entry_price,
            sl_price=sl_price,
            risk_percent=self.risk_percent,
            leverage=self.leverage,
        )
        position_size = lot_result["lot_size"]

        # Ensure minimum lot size
        position_size = max(position_size, self.min_lot)

        # Calculate PnL in price points
        if side == "BUY":
            pnl_points = exit_price - entry_price
        else:
            pnl_points = entry_price - exit_price

        # Convert to money
        pnl_money = pnl_points * position_size

        # Calculate funding cost
        position_value = position_size * entry_price
        funding_cost = self._calculate_funding_cost(
            entry_time, exit_time, position_value, side
        )

        # Calculate fees
        fees = self._calculate_fees(position_size, entry_price, exit_price)

        # Funding-adjusted PnL
        funding_adjusted_pnl = pnl_money + funding_cost - fees

        # Calculate hold time
        hold_time_hours = (exit_time - entry_time).total_seconds() / 3600

        # Calculate volatility during trade
        volatility = self._calculate_volatility(ohlcv_data)

        # Calculate MFE/MAE
        mfe, mae = self._calculate_mfe_mae(signal, ohlcv_data, side)

        # Determine result based on funding-adjusted PnL
        if funding_adjusted_pnl > 0:
            result = "WIN"
        elif funding_adjusted_pnl < 0:
            result = "LOSS"
        else:
            result = "BREAKEVEN"

        # Calculate R multiple
        r = signal.r_points
        r_multiple = pnl_points / r if r > 0 else 0

        # Calculate Sharpe contribution (simplified)
        sharpe_contribution = (
            funding_adjusted_pnl / volatility if volatility > 0 else 0
        )

        return CryptoTradeResult(
            entry_time=entry_time,
            exit_time=exit_time,
            symbol=signal.symbol or self._pair,
            side=side,
            entry_price=entry_price,
            exit_price=exit_price,
            volume=position_size,
            sl=signal.buy_sl if side == "BUY" else signal.sell_sl,
            tp=signal.buy_tp if side == "BUY" else signal.sell_tp,
            result=result,
            pnl_points=pnl_points,
            pnl_money=pnl_money,
            r_multiple=r_multiple,
            reason=reason,
            funding_cost=funding_cost,
            funding_adjusted_pnl=funding_adjusted_pnl,
            fees=fees,
            volatility=volatility,
            sharpe_contribution=sharpe_contribution,
            max_favorable_excursion=mfe,
            max_adverse_excursion=mae,
            hold_time_hours=hold_time_hours,
        )

    def run(
        self,
        ohlcv_data: List[OHLCV],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> CryptoBacktestMetrics:
        """Run backtest on historical CRYPTO data."""
        self.trades = []
        self.crypto_trades = []
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

        # For crypto, we process all data continuously (24/7 market)
        # No need to group by trading days like forex
        trading_hours = self._get_trading_hours(ohlcv_data)

        for hour in trading_hours:
            # Get OHLCV for this hour + lookforward
            hour_data = self._get_hour_data(ohlcv_data, hour)

            if len(hour_data) < 10:
                continue

            # Generate signal
            signals = self.strategy.get_signals(hour_data)

            if not signals:
                continue

            signal = signals[0]

            # Simulate trade execution
            trade = self._simulate_crypto_trade(signal, hour_data, ohlcv_data)

            if trade:
                self.trades.append(trade)
                self.crypto_trades.append(trade)

                # Update equity curve
                self._update_equity()

        # Calculate CRYPTO-specific metrics
        metrics = self._calculate_crypto_metrics()

        return metrics

    def _get_trading_hours(self, ohlcv_data: List[OHLCV]) -> List[datetime]:
        """Get unique trading hours from OHLCV data (24/7 support)."""
        hours = set()
        for candle in ohlcv_data:
            ts = candle.timestamp
            if ts.tzinfo is None:
                import pytz
                ts = ts.replace(tzinfo=pytz.utc)
            # Round to hour
            hour_ts = ts.replace(minute=0, second=0, microsecond=0)
            hours.add(hour_ts)

        first_ts = ohlcv_data[0].timestamp if ohlcv_data else None
        if first_ts and first_ts.tzinfo:
            tz = first_ts.tzinfo
            return sorted(
                [
                    datetime.combine(h, datetime.min.time()).replace(tzinfo=tz)
                    for h in hours
                ]
            )
        return sorted([datetime.combine(h, datetime.min.time()) for h in hours])

    def _get_hour_data(self, ohlcv_data: List[OHLCV], hour: datetime) -> List[OHLCV]:
        """Get OHLCV data for a specific hour plus lookback for strategy."""
        # Get data from 5 hours before to ensure we have enough lookback candles
        if hour.tzinfo is None:
            start = hour - timedelta(hours=5)
            end = hour + timedelta(hours=1)
        else:
            start = hour.replace(minute=0, second=0) - timedelta(hours=5)
            end = hour.replace(minute=0, second=0) + timedelta(hours=1)

        return [c for c in ohlcv_data if start <= c.timestamp <= end]

    def _simulate_crypto_trade(
        self, signal: TradingSignal, hour_data: List[OHLCV], ohlcv_data: List[OHLCV]
    ) -> Optional[CryptoTradeResult]:
        """Simulate trade execution for CRYPTO with 24/7 support."""
        signal_candle_idx = len(hour_data) - 4

        if signal_candle_idx >= len(hour_data):
            return None

        entry_time = None
        exit_time = None
        exit_price = None
        reason = ""

        # Look for trigger in subsequent candles (continuous market)
        for i in range(signal_candle_idx + 1, len(hour_data)):
            candle = hour_data[i]
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
                    # Close at end of candle
                    exit_time = candle.timestamp
                    exit_price = candle.close
                    reason = "candle close"

                return self._create_crypto_trade_result(
                    signal,
                    "BUY",
                    entry_time,
                    exit_time,
                    entry_price,
                    exit_price,
                    reason,
                    ohlcv_data,
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
                    reason = "candle close"

                return self._create_crypto_trade_result(
                    signal,
                    "SELL",
                    entry_time,
                    exit_time,
                    entry_price,
                    exit_price,
                    reason,
                    ohlcv_data,
                )

        # No trigger - cancelled
        return None

    def _calculate_crypto_metrics(self) -> CryptoBacktestMetrics:
        """Calculate CRYPTO-specific performance metrics."""
        if not self.crypto_trades:
            return CryptoBacktestMetrics(
                pair=self._pair,
                timeframe=self._timeframe,
                strategy=self._strategy_name,
                start_date=self._start_date,
                end_date=self._end_date,
                leverage=self.leverage,
                risk_percent=self.risk_percent,
            )

        winning = [t for t in self.crypto_trades if t.result == "WIN"]
        losing = [t for t in self.crypto_trades if t.result == "LOSS"]

        # Basic PnL calculations
        total_pnl_money = sum(t.pnl_money for t in self.crypto_trades)
        total_pnl_points = sum(t.pnl_points for t in self.crypto_trades)

        # Funding and fees
        total_funding_cost = sum(t.funding_cost for t in self.crypto_trades)
        total_fees = sum(t.fees for t in self.crypto_trades)

        # Funding-adjusted PnL
        funding_adjusted_pnl = sum(t.funding_adjusted_pnl for t in self.crypto_trades)

        # Profit factor
        wins_pnl = sum(t.pnl_money for t in winning) if winning else 0
        losses_pnl = abs(sum(t.pnl_money for t in losing)) if losing else 1
        profit_factor = wins_pnl / losses_pnl if losses_pnl > 0 else 0

        # Average R
        avg_r = sum(t.r_multiple for t in self.crypto_trades) / len(self.crypto_trades)

        # Expectancy
        expectancy = total_pnl_money / len(self.crypto_trades)

        # Average position size
        avg_lot = (
            sum(t.volume for t in self.crypto_trades) / len(self.crypto_trades)
            if self.crypto_trades
            else 0
        )

        # Average funding cost and fees
        avg_funding_cost = total_funding_cost / len(self.crypto_trades) if self.crypto_trades else 0
        avg_fees = total_fees / len(self.crypto_trades) if self.crypto_trades else 0

        # Average volatility
        avg_volatility = sum(t.volatility for t in self.crypto_trades) / len(self.crypto_trades) if self.crypto_trades else 0

        # Average hold time
        total_hours = sum(t.hold_time_hours for t in self.crypto_trades)
        avg_hold_time_hours = total_hours / len(self.crypto_trades) if self.crypto_trades else 0

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

        # Volatility-adjusted return
        volatility_adjusted_return = (
            (roi_percent / avg_volatility) if avg_volatility > 0 else 0
        )

        # Sortino ratio (using downside deviation)
        if losing:
            downside_returns = [t.funding_adjusted_pnl for t in self.crypto_trades if t.funding_adjusted_pnl < 0]
            if downside_returns:
                import statistics
                downside_std = statistics.stdev(downside_returns) if len(downside_returns) > 1 else abs(sum(downside_returns))
                sortino_ratio = (funding_adjusted_pnl / downside_std) if downside_std > 0 else 0
            else:
                sortino_ratio = 0
        else:
            sortino_ratio = 0

        # Calmar ratio (annualized return / max drawdown)
        # Annualize the return based on the backtest period
        if self._start_date and self._end_date:
            try:
                start = datetime.strptime(self._start_date, "%Y-%m-%d")
                end = datetime.strptime(self._end_date, "%Y-%m-%d")
                days = max(1, (end - start).days)
                annualized_return = (roi_percent * 365) / days
                calmar_ratio = (annualized_return / max_dd) if max_dd > 0 else 0
            except:
                calmar_ratio = 0
        else:
            calmar_ratio = 0

        # Funding impact
        gross_pnl = abs(total_pnl_money)
        funding_impact_percent = (
            (total_funding_cost / gross_pnl * 100) if gross_pnl > 0 else 0
        )

        # Net funding yield (annualized)
        if starting_capital > 0 and total_hours > 0:
            # Annualize funding cost
            hours_per_year = 8760
            annualized_funding = (total_funding_cost / total_hours) * hours_per_year
            net_funding_yield = (annualized_funding / starting_capital) * 100
        else:
            net_funding_yield = 0

        # Trade quality metrics
        avg_mfe = sum(t.max_favorable_excursion for t in self.crypto_trades) / len(self.crypto_trades) if self.crypto_trades else 0
        avg_mae = sum(t.max_adverse_excursion for t in self.crypto_trades) / len(self.crypto_trades) if self.crypto_trades else 0
        mfe_ma_ratio = (avg_mfe / avg_mae) if avg_mae > 0 else 0

        # Average Sharpe contribution
        avg_sharpe_contribution = (
            sum(t.sharpe_contribution for t in self.crypto_trades) / len(self.crypto_trades)
            if self.crypto_trades
            else 0
        )

        return CryptoBacktestMetrics(
            pair=self._pair,
            timeframe=self._timeframe,
            strategy=self._strategy_name,
            start_date=self._start_date,
            end_date=self._end_date,
            leverage=self.leverage,
            risk_percent=self.risk_percent,
            avg_lot_size=avg_lot,
            total_trades=len(self.crypto_trades),
            winning_trades=len(winning),
            losing_trades=len(losing),
            win_rate=len(winning) / len(self.crypto_trades) * 100,
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
            total_funding_cost=total_funding_cost,
            funding_adjusted_pnl=funding_adjusted_pnl,
            total_fees=total_fees,
            avg_funding_cost=avg_funding_cost,
            avg_fees=avg_fees,
            avg_volatility=avg_volatility,
            avg_hold_time_hours=avg_hold_time_hours,
            volatility_adjusted_return=volatility_adjusted_return,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            funding_impact_percent=funding_impact_percent,
            net_funding_yield=net_funding_yield,
            avg_mfe=avg_mfe,
            avg_mae=avg_mae,
            mfe_ma_ratio=mfe_ma_ratio,
            avg_sharpe_contribution=avg_sharpe_contribution,
        )

    def export_trades(self, filename: str = "crypto_backtest_trades.json") -> str:
        """Export CRYPTO trades to JSON."""
        data = {
            "metrics": self._calculate_crypto_metrics().to_dict(),
            "trades": [t.to_dict() for t in self.crypto_trades],
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        return filename

    def format_summary(self, metrics: CryptoBacktestMetrics) -> str:
        """Format CRYPTO metrics as readable summary."""
        return f"""
=== CRYPTO Backtest Results ===

Strategy:  {metrics.strategy}
Pair:      {metrics.pair}
Timeframe: {metrics.timeframe}
Period:    {metrics.start_date} to {metrics.end_date}

Capital:
  Starting:           ${metrics.starting_capital:,.2f}
  Ending:             ${metrics.ending_capital:,.2f}
  Gross PnL:          ${metrics.total_pnl_money:,.2f}
  Funding-Adj PnL:    ${metrics.funding_adjusted_pnl:,.2f}
  ROI:                {metrics.roi_percent:.2f}%

Funding & Fees:
  Total Funding:      ${metrics.total_funding_cost:,.2f}
  Total Fees:         ${metrics.total_fees:,.2f}
  Avg Funding/Trade:  ${metrics.avg_funding_cost:,.2f}
  Avg Fees/Trade:     ${metrics.avg_fees:,.2f}
  Funding Impact:     {metrics.funding_impact_percent:.1f}%
  Net Funding Yield:  {metrics.net_funding_yield:.2f}%

Volatility:
  Avg Volatility:     {metrics.avg_volatility:.2f}
  Vol-Adj Return:     {metrics.volatility_adjusted_return:.2f}

Trades:
  Total:              {metrics.total_trades}
  Wins:               {metrics.winning_trades}
  Losses:             {metrics.losing_trades}
  Win Rate:           {metrics.win_rate:.1f}%
  Avg Hold Time:      {metrics.avg_hold_time_hours:.1f} hours

Performance:
  Profit Factor:      {metrics.profit_factor:.2f}
  Average R:          {metrics.avg_r:.2f}
  Expectancy:         ${metrics.expectancy:.2f}
  Max Drawdown:       {metrics.max_drawdown_points:.1f}%

Risk-Adjusted:
  Sharpe Contrib:     {metrics.avg_sharpe_contribution:.2f}
  Sortino Ratio:      {metrics.sortino_ratio:.2f}
  Calmar Ratio:       {metrics.calmar_ratio:.2f}

Trade Quality:
  Avg MFE:            {metrics.avg_mfe:.2f}
  Avg MAE:            {metrics.avg_mae:.2f}
  MFE/MAE Ratio:      {metrics.mfe_ma_ratio:.2f}
"""

    def get_supported_pairs(self) -> List[str]:
        """Get list of supported CRYPTO pairs."""
        return list(CRYPTO_PAIRS.keys())

    def get_supported_timeframes(self) -> List[str]:
        """Get list of supported timeframes."""
        return CRYPTO_TIMEFRAMES.copy()

    def get_pair_info(self, pair: str) -> Dict[str, Any]:
        """Get configuration info for a CRYPTO pair."""
        if pair not in CRYPTO_PAIRS:
            raise ValueError(f"Unknown pair: {pair}")
        return CRYPTO_PAIRS[pair]
