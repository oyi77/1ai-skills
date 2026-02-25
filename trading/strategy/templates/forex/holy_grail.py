"""
Holy Grail FOREX Strategy

Strategy based on the Holy Grail trading method from ForexTester.
Combines EMA(20) for trend direction, ADX(14) for trend strength,
and RSI(14) for momentum confirmation.

Entry BUY:
- Uptrend by EMA(20): price above EMA(20)
- ADX rises above 30 (trend strengthening)
- Breakdown of EMA with rollback: price crosses below EMA then retraces back above

Entry SELL:
- Bearish trend by EMA(20): price below EMA(20)
- ADX grows above 30 (trend strengthening)
- Breakdown from bottom up with rollback: price crosses above EMA then retraces back below

Exit:
- ADX line reversal down from upper zone (ADX starts declining from high levels)

Timeframe: H4 minimum
Support major pairs: EUR/USD, GBP/USD, USD/JPY (configurable)
"""

from datetime import datetime
from typing import List, Optional, Tuple

from ....brokers.base import OHLCV
from ..base import StrategyTemplate, Signal, SignalType
from ....indicators.moving_averages import EMA
from ....indicators.adx import ADX, calculate_adx
from ....indicators.rsi import RSI, calculate_rsi


class HolyGrailStrategy(StrategyTemplate):
    """
    Holy Grail FOREX strategy implementation.

    Combines EMA(20) for trend direction, ADX(14) for trend strength,
    and RSI(14) for momentum confirmation.

    Attributes:
        ema_period: Period for EMA (default: 20)
        adx_period: Period for ADX (default: 14)
        adx_threshold: ADX level to confirm trend (default: 30)
        rsi_period: Period for RSI (default: 14)
        rsi_buy_zone: RSI range for BUY confirmation (default: 40-60)
        rsi_sell_zone: RSI range for SELL confirmation (default: 40-60)
        min_timeframe: Minimum timeframe (default: H4)
    """

    # Valid timeframes for this strategy (H4 minimum)
    VALID_TIMEFRAMES = ["H4", "D1", "W1"]

    # Major FOREX pairs supported
    MAJOR_PAIRS = [
        "EUR/USD",
        "GBP/USD",
        "USD/JPY",
        "USD/CHF",
        "AUD/USD",
        "USD/CAD",
        "NZD/USD",
        "EUR/GBP",
        "EUR/JPY",
        "GBP/JPY",
    ]

    def __init__(
        self,
        symbol: str = "EUR/USD",
        timeframe: str = "H4",
        ema_period: int = 20,
        adx_period: int = 14,
        adx_threshold: float = 30.0,
        rsi_period: int = 14,
        rsi_buy_min: float = 40.0,
        rsi_buy_max: float = 60.0,
        rsi_sell_min: float = 40.0,
        rsi_sell_max: float = 60.0,
        risk_per_trade: float = 0.02,
        config: Optional[dict] = None,
    ):
        """
        Initialize Holy Grail strategy.

        Args:
            symbol: Trading symbol (default: EUR/USD)
            timeframe: Chart timeframe (default: H4)
            ema_period: EMA period (default: 20)
            adx_period: ADX period (default: 14)
            adx_threshold: ADX level to confirm trend (default: 30)
            rsi_period: RSI period (default: 14)
            rsi_buy_min: Minimum RSI for BUY confirmation (default: 40)
            rsi_buy_max: Maximum RSI for BUY confirmation (default: 60)
            rsi_sell_min: Minimum RSI for SELL confirmation (default: 40)
            rsi_sell_max: Maximum RSI for SELL confirmation (default: 60)
            risk_per_trade: Risk per trade as fraction (default: 0.02 = 2%)
            config: Additional configuration dictionary
        """
        super().__init__(
            name="HolyGrailStrategy",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )

        # Indicator parameters
        self.ema_period = ema_period
        self.adx_period = adx_period
        self.adx_threshold = adx_threshold
        self.rsi_period = rsi_period
        self.rsi_buy_min = rsi_buy_min
        self.rsi_buy_max = rsi_buy_max
        self.rsi_sell_min = rsi_sell_min
        self.rsi_sell_max = rsi_sell_max

        # Initialize indicators
        self.ema_indicator = EMA(period=ema_period)
        self.adx_indicator = ADX(
            period=adx_period,
            weak_level=adx_threshold,
            strong_level=adx_threshold + 10,
            very_strong_level=adx_threshold + 20,
        )
        self.rsi_indicator = RSI(period=rsi_period)

        # Track ADX state for exit detection
        self._adx_history: List[float] = []
        self._adx_peak: Optional[float] = None

    def _get_ema_values(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """
        Get EMA values for current and previous candle.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            Tuple of (current_ema, prev_ema, prev_prev_ema)
        """
        if current_idx < self.ema_period:
            return None, None, None

        # Get all EMA values up to current index
        ema_values = self.ema_indicator.calculate(ohlcv_data[: current_idx + 1])

        if ema_values[-1] is None:
            return None, None, None

        current_ema = ema_values[-1]
        prev_ema = ema_values[-2] if len(ema_values) > 1 else None
        prev_prev_ema = ema_values[-3] if len(ema_values) > 2 else None

        return current_ema, prev_ema, prev_prev_ema

    def _get_adx_result(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ):
        """
        Get ADX result for current candle.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            ADXResult or None
        """
        if current_idx < self.adx_period + 1:
            return None

        try:
            adx_result = self.adx_indicator.calculate(ohlcv_data[: current_idx + 1])
            return adx_result
        except ValueError:
            return None

    def _get_rsi_value(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Optional[float]:
        """
        Get RSI value for current candle.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            RSI value or None
        """
        if current_idx < self.rsi_period + 1:
            return None

        try:
            rsi_result = self.rsi_indicator.calculate(ohlcv_data[: current_idx + 1])
            return rsi_result.value if rsi_result else None
        except ValueError:
            return None

    def _is_uptrend(self, ohlcv_data: List[OHLCV], current_idx: int) -> bool:
        """
        Check if market is in uptrend based on EMA position.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            True if price is above EMA (uptrend)
        """
        current_ema, _, _ = self._get_ema_values(ohlcv_data, current_idx)
        if current_ema is None:
            return False

        current_price = ohlcv_data[current_idx].close
        return current_price > current_ema

    def _is_downtrend(self, ohlcv_data: List[OHLCV], current_idx: int) -> bool:
        """
        Check if market is in downtrend based on EMA position.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            True if price is below EMA (downtrend)
        """
        current_ema, _, _ = self._get_ema_values(ohlcv_data, current_idx)
        if current_ema is None:
            return False

        current_price = ohlcv_data[current_idx].close
        return current_price < current_ema

    def _detect_ema_breakdown_with_rollback(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> bool:
        """
        Detect EMA breakdown with rollback (for BUY entry).

        Pattern: Price crosses below EMA, then retraces back above EMA.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            True if breakdown with rollback pattern detected
        """
        if current_idx < 3:
            return False

        current_ema, prev_ema, prev_prev_ema = self._get_ema_values(
            ohlcv_data, current_idx
        )
        if current_ema is None or prev_ema is None or prev_prev_ema is None:
            return False

        current_price = ohlcv_data[current_idx].close
        prev_price = ohlcv_data[current_idx - 1].close
        prev_prev_price = ohlcv_data[current_idx - 2].close

        # Check for rollback pattern:
        # Previous candle: price was below EMA
        # Current candle: price crosses back above EMA
        prev_was_below = prev_price < prev_ema
        curr_is_above = current_price > current_ema

        # Also check that 2 candles ago price was above EMA (confirms breakdown)
        prev_prev_was_above = prev_prev_price > prev_prev_ema

        return prev_was_below and curr_is_above and prev_prev_was_above

    def _detect_ema_breakout_with_rollback(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> bool:
        """
        Detect EMA breakout with rollback (for SELL entry).

        Pattern: Price crosses above EMA, then retraces back below EMA.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            True if breakout with rollback pattern detected
        """
        if current_idx < 3:
            return False

        current_ema, prev_ema, prev_prev_ema = self._get_ema_values(
            ohlcv_data, current_idx
        )
        if current_ema is None or prev_ema is None or prev_prev_ema is None:
            return False

        current_price = ohlcv_data[current_idx].close
        prev_price = ohlcv_data[current_idx - 1].close
        prev_prev_price = ohlcv_data[current_idx - 2].close

        # Check for rollback pattern:
        # Previous candle: price was above EMA
        # Current candle: price crosses back below EMA
        prev_was_above = prev_price > prev_ema
        curr_is_below = current_price < current_ema

        # Also check that 2 candles ago price was below EMA (confirms breakout)
        prev_prev_was_below = prev_prev_price < prev_prev_ema

        return prev_was_above and curr_is_below and prev_prev_was_below

    def _is_adx_rising(self, ohlcv_data: List[OHLCV], current_idx: int) -> bool:
        """
        Check if ADX is rising (trend strengthening).

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            True if ADX is rising and above threshold
        """
        if current_idx < self.adx_period + 5:
            return False

        current_adx = self._get_adx_result(ohlcv_data, current_idx)
        prev_adx = self._get_adx_result(ohlcv_data, current_idx - 1)

        if current_adx is None or prev_adx is None:
            return False

        # ADX must be above threshold and rising
        return (
            current_adx.adx > self.adx_threshold
            and current_adx.adx > prev_adx.adx
        )

    def _is_adx_reversing_down(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> bool:
        """
        Check if ADX is reversing down from upper zone (exit signal).

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            True if ADX is reversing down from upper zone
        """
        if current_idx < self.adx_period + 10:
            return False

        current_adx = self._get_adx_result(ohlcv_data, current_idx)
        prev_adx = self._get_adx_result(ohlcv_data, current_idx - 1)
        prev_prev_adx = self._get_adx_result(ohlcv_data, current_idx - 2)

        if current_adx is None or prev_adx is None or prev_prev_adx is None:
            return False

        # ADX must be in upper zone (above strong level) and starting to decline
        upper_zone = self.adx_threshold + 10  # e.g., 40

        return (
            prev_prev_adx.adx > upper_zone
            and prev_adx.adx > upper_zone
            and current_adx.adx < prev_adx.adx
            and current_adx.adx < prev_prev_adx.adx
        )

    def _check_rsi_confirmation(
        self, ohlcv_data: List[OHLCV], current_idx: int, is_buy: bool
    ) -> bool:
        """
        Check if RSI confirms the entry signal.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index
            is_buy: True for BUY signal, False for SELL

        Returns:
            True if RSI confirms the signal
        """
        rsi_value = self._get_rsi_value(ohlcv_data, current_idx)
        if rsi_value is None:
            return True  # Allow entry if RSI not available

        if is_buy:
            return self.rsi_buy_min <= rsi_value <= self.rsi_buy_max
        else:
            return self.rsi_sell_min <= rsi_value <= self.rsi_sell_max

    def entry_conditions(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if entry criteria are met for Holy Grail strategy.

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        current = ohlcv_data[current_idx]

        # Check minimum index requirements
        min_required = max(
            self.ema_period, self.adx_period + 1, self.rsi_period + 1
        ) + 5
        if current_idx < min_required:
            return False, None

        # Check for BUY entry
        if self._is_uptrend(ohlcv_data, current_idx):
            if self._is_adx_rising(ohlcv_data, current_idx):
                if self._detect_ema_breakdown_with_rollback(ohlcv_data, current_idx):
                    if self._check_rsi_confirmation(ohlcv_data, current_idx, is_buy=True):
                        # Calculate stop loss and take profit
                        ema_value, _, _ = self._get_ema_values(ohlcv_data, current_idx)
                        atr = self._calculate_atr(ohlcv_data)

                        entry_price = current.close
                        stop_loss = ema_value - (atr * 2) if ema_value else current.low - (atr * 2)
                        risk = entry_price - stop_loss
                        take_profit = entry_price + (risk * 2)

                        return True, Signal(
                            timestamp=current.timestamp,
                            symbol=self.symbol,
                            timeframe=self.timeframe,
                            signal_type=SignalType.BUY,
                            price=entry_price,
                            stop_loss=stop_loss,
                            take_profit=take_profit,
                            confidence=0.85,
                            metadata={
                                "type": "holy_grail_buy",
                                "ema_period": self.ema_period,
                                "adx_period": self.adx_period,
                                "adx_threshold": self.adx_threshold,
                                "rsi_period": self.rsi_period,
                                "ema_value": ema_value,
                            }
                        )

        # Check for SELL entry
        if self._is_downtrend(ohlcv_data, current_idx):
            if self._is_adx_rising(ohlcv_data, current_idx):
                if self._detect_ema_breakout_with_rollback(ohlcv_data, current_idx):
                    if self._check_rsi_confirmation(ohlcv_data, current_idx, is_buy=False):
                        # Calculate stop loss and take profit
                        ema_value, _, _ = self._get_ema_values(ohlcv_data, current_idx)
                        atr = self._calculate_atr(ohlcv_data)

                        entry_price = current.close
                        stop_loss = ema_value + (atr * 2) if ema_value else current.high + (atr * 2)
                        risk = stop_loss - entry_price
                        take_profit = entry_price - (risk * 2)

                        return True, Signal(
                            timestamp=current.timestamp,
                            symbol=self.symbol,
                            timeframe=self.timeframe,
                            signal_type=SignalType.SELL,
                            price=entry_price,
                            stop_loss=stop_loss,
                            take_profit=take_profit,
                            confidence=0.85,
                            metadata={
                                "type": "holy_grail_sell",
                                "ema_period": self.ema_period,
                                "adx_period": self.adx_period,
                                "adx_threshold": self.adx_threshold,
                                "rsi_period": self.rsi_period,
                                "ema_value": ema_value,
                            }
                        )

        return False, None

    def exit_conditions(
        self, ohlcv_data: List[OHLCV], current_idx: int, position
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if exit criteria are met for Holy Grail strategy.

        Exit when ADX reverses down from upper zone.

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            position: Current position to check

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        current = ohlcv_data[current_idx]

        # Check for ADX reversal (exit signal)
        if self._is_adx_reversing_down(ohlcv_data, current_idx):
            if position.side == "LONG":
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.9,
                    metadata={"reason": "adx_reversal_down"}
                )
            elif position.side == "SHORT":
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.9,
                    metadata={"reason": "adx_reversal_down"}
                )

        return False, None

    def position_sizing(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int,
        entry_price: float,
        stop_loss: float,
        account_balance: float
    ) -> float:
        """
        Calculate position size based on risk management.

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            entry_price: Planned entry price
            stop_loss: Stop loss price
            account_balance: Current account balance

        Returns:
            Position size (units/lots)
        """
        if stop_loss == entry_price:
            return 0.0

        stop_loss_pips = self.calculate_stop_loss_pips(entry_price, stop_loss)

        return self.calculate_position_size_from_risk(
            account_balance=account_balance,
            stop_loss_pips=stop_loss_pips,
        )

    def _calculate_atr(self, ohlcv_data: List[OHLCV], period: int = 14) -> float:
        """
        Calculate Average True Range for stop loss placement.

        Args:
            ohlcv_data: OHLCV data
            period: ATR period (default: 14)

        Returns:
            ATR value
        """
        if len(ohlcv_data) < period + 1:
            return 0.0

        true_ranges = []
        for i in range(1, len(ohlcv_data)):
            high = ohlcv_data[i].high
            low = ohlcv_data[i].low
            prev_close = ohlcv_data[i-1].close

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            true_ranges.append(tr)

        return sum(true_ranges[-period:]) / period if true_ranges else 0.0

    def get_required_candles(self) -> int:
        """
        Get number of candles required for signal generation.

        Returns:
            Minimum number of candles needed
        """
        # Need enough candles for EMA, ADX, and ATR calculations
        return max(
            self.ema_period,
            self.adx_period + 1,
            self.rsi_period + 1
        ) + 20  # Extra buffer for pattern detection

    def validate_config(self) -> bool:
        """
        Validate strategy configuration.

        Returns:
            True if configuration is valid
        """
        if not super().validate_config():
            return False

        # Validate timeframe
        if self.timeframe not in self.VALID_TIMEFRAMES:
            self.logger.warning(
                f"Timeframe {self.timeframe} is below minimum H4. "
                f"Strategy may not perform optimally."
            )

        # Validate periods
        if self.ema_period <= 0:
            self.logger.error(f"Invalid ema_period: {self.ema_period}")
            return False

        if self.adx_period <= 0:
            self.logger.error(f"Invalid adx_period: {self.adx_period}")
            return False

        if self.rsi_period <= 0:
            self.logger.error(f"Invalid rsi_period: {self.rsi_period}")
            return False

        # Validate ADX threshold
        if self.adx_threshold <= 0 or self.adx_threshold > 100:
            self.logger.error(f"Invalid adx_threshold: {self.adx_threshold}")
            return False

        # Validate RSI zones
        if not (0 <= self.rsi_buy_min <= self.rsi_buy_max <= 100):
            self.logger.error(f"Invalid RSI buy zone: {self.rsi_buy_min}-{self.rsi_buy_max}")
            return False

        if not (0 <= self.rsi_sell_min <= self.rsi_sell_max <= 100):
            self.logger.error(f"Invalid RSI sell zone: {self.rsi_sell_min}-{self.rsi_sell_max}")
            return False

        return True

    def backtest(self, start_date, end_date, initial_balance=100):
        """
        Run backtest for Holy Grail strategy.

        Args:
            start_date: Start date string (YYYY-MM-DD)
            end_date: End date string (YYYY-MM-DD)
            initial_balance: Starting balance (default: 100)

        Returns:
            Dictionary with backtest results
        """
        import yfinance as yf
        import pandas as pd
        from datetime import datetime
        import json

        # Download data
        symbol_ticker = self.symbol.replace('/', '-')
        if 'XAUUSD' in symbol_ticker:
            symbol_ticker = 'GC=F'
        elif 'USDJPY' in symbol_ticker:
            symbol_ticker = 'JPY=X'
        else:
            symbol_ticker += '=X'

        print(f"Downloading {{symbol_ticker}} data from {{start_date}} to {{end_date}}...")
        ticker = yf.Ticker(symbol_ticker)
        df = ticker.history(start=start_date, end=end_date, interval="1d")

        if df.empty:
            return {{'error': f'No data for {{symbol_ticker}}'}}

        print(f"Downloaded {{len(df)}} candles")

        # Remove timezone
        if df.index.tz is not None:
            df = df.tz_localize(None)

        # Initialize backtest
        balance = initial_balance
        trades = []
        signals = []

        # Calculate indicators
        print("Calculating indicators...")
        for i in range(len(df)):
            current_candle = df.iloc[i:i+1]
            timestamp = current_candle.index[0]
            ohlcv = self.OHLCV(
                timestamp=timestamp,
                open=current_candle['Open'].iloc[0],
                high=current_candle['High'].iloc[0],
                low=current_candle['Low'].iloc[0],
                close=current_candle['Close'].iloc[0],
                volume=current_candle['Volume'].iloc[0]
            )

            signals.append(ohlcv)

        # Generate trading signals
        print("Generating trading signals...")
        try:
            for i in range(len(signals)):
                if i < len(signals) - 1:
                    # Get signals for current candle
                    signal = self.generate_signals(signals[:i+1])

                    if signal:
                        # Simulate trade
                        entry = signals[i].close
                        sl = signals[i].low
                        tp = signals[i].high

                        # Simple 1:1 R/R for now
                        risk = entry - sl
                        if risk <= 0:
                            continue

                        if risk > 0:
                            # Long trade
                            tp_price = entry + abs(risk)
                            sl_price = sl
                        else:
                            # Short trade
                            tp_price = entry - abs(risk)
                            sl_price = high

                        # Risk 1% of balance
                        risk_amount = balance * 0.01
                        lot_size = risk_amount / abs(risk)

                        # Simulate exit
                        pnl = 0
                        if i < len(signals) - 1:
                            next_candles = signals[i+1:min(i+10, len(signals))]

                            # Check if TP hit
                            for c in next_candles:
                                if risk > 0 and c.high >= tp_price:
                                    pnl = (tp_price - entry) * lot_size
                                    break
                                elif risk < 0 and c.low <= tp_price:
                                    pnl = (entry - tp_price) * lot_size
                                    break
                                elif risk > 0 and c.low <= sl_price:
                                    pnl = (sl_price - entry) * lot_size
                                    break
                                elif risk < 0 and c.high >= sl_price:
                                    pnl = (entry - sl_price) * lot_size
                                    break

                        balance += pnl
                        trades.append({{
                            'date': str(signals[i].timestamp),
                            'type': 'BUY' if risk > 0 else 'SELL',
                            'entry': entry,
                            'sl': sl_price,
                            'tp': tp_price,
                            'pnl': pnl,
                            'win': pnl > 0
                        }})

        except Exception as e:
            print(f"Signal generation error: {{e}}")
            return {{'error': str(e)}}

        # Calculate metrics
        wins = [t for t in trades if t['win']]
        losses = [t for t in trades if not t['win']]

        total_trades = len(trades)
        total_wins = len(wins)
        total_losses = len(losses)
        win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0

        net_pnl = balance - initial_balance

        total_profit = sum(t['pnl'] for t in wins)
        total_loss = abs(sum(t['pnl'] for t in losses))
        profit_factor = (total_profit / total_loss) if total_loss > 0 else 0

        avg_win = (total_profit / total_wins) if total_wins > 0 else 0
        avg_loss = (total_loss / total_losses) if total_losses > 0 else 0

        # Max drawdown
        peak = initial_balance
        trough = initial_balance
        for t in trades:
            balance_after = peak + sum(t['pnl'] for t in trades[:trades.index(t)+1])
            peak = max(peak, balance_after)
            trough = min(trough, balance_after)

        max_drawdown = ((peak - trough) / peak * 100) if peak > 0 else 0

        # Consecutive wins/losses
        max_consecutive_wins = 0
        max_consecutive_losses = 0
        current_consecutive_wins = 0
        current_consecutive_losses = 0

        for t in trades:
            if t['win']:
                current_consecutive_wins += 1
                current_consecutive_losses = 0
                max_consecutive_wins = max(max_consecutive_wins, current_consecutive_wins)
            else:
                current_consecutive_losses += 1
                current_consecutive_wins = 0
                max_consecutive_losses = max(max_consecutive_losses, current_consecutive_losses)

        return {{
            'pair': self.symbol,
            'strategy': 'Holy Grail',
            'initial_balance': initial_balance,
            'final_balance': balance,
            'net_pnl': net_pnl,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_trades': total_trades,
            'wins': total_wins,
            'losses': total_losses,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'max_consecutive_wins': max_consecutive_wins,
            'max_consecutive_losses': max_consecutive_losses,
            'max_drawdown': max_drawdown
        }}



    def get_supported_symbols(self) -> List[str]:
        """
        Get list of supported trading symbols.

        Returns:
            List of supported symbol strings
        """
        return self.MAJOR_PAIRS.copy()
