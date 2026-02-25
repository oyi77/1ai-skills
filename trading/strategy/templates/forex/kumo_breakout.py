"""
Kumo Breakout FOREX Strategy

Strategy based on Ichimoku Kumo (Cloud) breakouts combined with Awesome Oscillator
for momentum confirmation. Optimized for FOREX pairs.

Entry BUY: Breakdown of upper Kumo boundary; AO histogram reversal from bottom up
Entry SELL: Breakdown of lower Kumo boundary; AO histogram reversal from top to bottom

Timeframe: M15 for entry signals, H1+ for trend tracking
Parameters: Ichimoku (8, 29, 34) - forex-optimized
"""

from datetime import datetime
from typing import List, Optional, Tuple

from ....brokers.base import OHLCV
from ..base import StrategyTemplate, Signal, SignalType
from ....indicators.ichimoku import Ichimoku, IchimokuResult
from ....indicators.macd import MACD


class AwesomeOscillator:
    """
    Awesome Oscillator (AO) Indicator

    Bill Williams' Awesome Oscillator is a momentum indicator that measures
    the relationship between simple moving averages.

    Formula:
    - AO = SMA(median_price, 5) - SMA(median_price, 34)
    - Where median_price = (high + low) / 2

    The histogram represents the difference between these two SMAs.
    """

    def __init__(self, fast_period: int = 5, slow_period: int = 34):
        """
        Initialize Awesome Oscillator.

        Args:
            fast_period: Fast SMA period (default: 5)
            slow_period: Slow SMA period (default: 34)
        """
        self.fast_period = fast_period
        self.slow_period = slow_period

    def calculate(self, ohlcv_data: List[OHLCV]) -> List[Optional[float]]:
        """
        Calculate Awesome Oscillator histogram values.

        Args:
            ohlcv_data: List of OHLCV candlestick data

        Returns:
            List of AO histogram values (can contain None for insufficient data)
        """
        if len(ohlcv_data) < self.slow_period:
            return [None] * len(ohlcv_data)

        # Calculate median prices
        median_prices = [(c.high + c.low) / 2 for c in ohlcv_data]

        # Calculate fast and slow SMAs
        fast_sma = self._calculate_sma(median_prices, self.fast_period)
        slow_sma = self._calculate_sma(median_prices, self.slow_period)

        # Calculate AO histogram
        ao_histogram: List[Optional[float]] = []
        for i in range(len(ohlcv_data)):
            if fast_sma[i] is None or slow_sma[i] is None:
                ao_histogram.append(None)
            else:
                ao_histogram.append(fast_sma[i] - slow_sma[i])

        return ao_histogram

    def _calculate_sma(
        self, values: List[float], period: int
    ) -> List[Optional[float]]:
        """
        Calculate Simple Moving Average for a list of values.

        Args:
            values: List of numeric values
            period: SMA period

        Returns:
            List of SMA values (None for insufficient data)
        """
        sma: List[Optional[float]] = []

        for i in range(len(values)):
            if i < period - 1:
                sma.append(None)
            else:
                window = values[i - period + 1 : i + 1]
                sma.append(sum(window) / period)

        return sma

    def get_histogram_reversal(
        self,
        ao_histogram: List[Optional[float]],
        current_idx: int,
        direction: str
    ) -> bool:
        """
        Check if AO histogram shows reversal in specified direction.

        Args:
            ao_histogram: List of AO histogram values
            current_idx: Current candle index
            direction: "up" for bullish reversal, "down" for bearish reversal

        Returns:
            True if reversal pattern detected
        """
        if current_idx < 2 or current_idx >= len(ao_histogram):
            return False

        # Get current and previous histogram values
        curr = ao_histogram[current_idx]
        prev1 = ao_histogram[current_idx - 1]
        prev2 = ao_histogram[current_idx - 2]

        if any(v is None for v in [curr, prev1, prev2]):
            return False

        if direction == "up":
            # Bullish reversal: histogram turning from bottom (negative) up
            # Pattern: prev2 < prev1 < curr and prev2 < 0
            return prev2 < prev1 < curr and prev2 < 0
        elif direction == "down":
            # Bearish reversal: histogram turning from top (positive) down
            # Pattern: prev2 > prev1 > curr and prev2 > 0
            return prev2 > prev1 > curr and prev2 > 0

        return False


class KumoBreakoutStrategy(StrategyTemplate):
    """
    Kumo Breakout Strategy for FOREX trading.

    Combines Ichimoku Cloud (Kumo) breakouts with Awesome Oscillator
    for momentum confirmation. Uses forex-optimized parameters (8, 29, 34).

    Entry Conditions:
        BUY: Price breaks above upper Kumo boundary AND AO histogram reverses upward
        SELL: Price breaks below lower Kumo boundary AND AO histogram reverses downward

    Exit Conditions:
        - Opposite Kumo boundary break
        - Tenkan-Kijun cross in opposite direction
        - Price closes beyond cloud in opposite direction

    Timeframe:
        - M15: Primary entry signals
        - H1+: Trend tracking and confirmation

    Risk Management:
        - Stop loss: Beyond opposite Kumo boundary or ATR-based
        - Take profit: 2:1 risk-reward ratio
    """

    def __init__(
        self,
        symbol: str = "EURUSD",
        timeframe: str = "M15",
        risk_per_trade: float = 0.02,
        use_trailing_stop: bool = True,
        trailing_stop_pips: float = 30.0,
        config: Optional[dict] = None,
    ):
        """
        Initialize Kumo Breakout Strategy.

        Args:
            symbol: Trading symbol (default: EURUSD)
            timeframe: Primary timeframe for signals (default: M15)
            risk_per_trade: Risk percentage per trade (default: 2%)
            use_trailing_stop: Use trailing stop loss (default: True)
            trailing_stop_pips: Trailing stop distance in pips (default: 30)
            config: Additional configuration options
        """
        super().__init__(
            name="KumoBreakoutStrategy",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )
        self.use_trailing_stop = use_trailing_stop
        self.trailing_stop_pips = trailing_stop_pips

        # Initialize Ichimoku with forex-optimized parameters (8, 29, 34)
        self.ichimoku = Ichimoku(
            tenkan_period=8,
            kijun_period=29,
            senkou_b_period=34,
            cloud_future=26,
            forex_mode=True,
        )

        # Initialize Awesome Oscillator
        self.awesome_oscillator = AwesomeOscillator(fast_period=5, slow_period=34)

    def calculate_ichimoku(
        self, ohlcv_data: List[OHLCV], idx: int
    ) -> Optional[IchimokuResult]:
        """
        Calculate Ichimoku values at specific index.

        Args:
            ohlcv_data: List of OHLCV data
            idx: Current index

        Returns:
            IchimokuResult or None if insufficient data
        """
        required = self.ichimoku.get_required_period()
        if idx < required:
            return None

        # Use data up to current index for calculation
        data_slice = ohlcv_data[: idx + 1]
        return self.ichimoku.calculate(data_slice)

    def get_kumo_boundaries(
        self, ichimoku_result: Optional[IchimokuResult]
    ) -> Tuple[Optional[float], Optional[float]]:
        """
        Get current Kumo (cloud) boundaries.

        Args:
            ichimoku_result: Ichimoku calculation result

        Returns:
            Tuple of (upper_boundary, lower_boundary)
            Upper = max(senkou_a, senkou_b)
            Lower = min(senkou_a, senkou_b)
        """
        if ichimoku_result is None:
            return None, None

        upper = max(ichimoku_result.senkou_a, ichimoku_result.senkou_b)
        lower = min(ichimoku_result.senkou_a, ichimoku_result.senkou_b)

        return upper, lower

    def is_kumo_breakout(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int,
        direction: str
    ) -> bool:
        """
        Check if price is breaking out of Kumo in specified direction.

        Args:
            ohlcv_data: List of OHLCV data
            current_idx: Current candle index
            direction: "up" for bullish breakout, "down" for bearish

        Returns:
            True if breakout detected
        """
        if current_idx < 1:
            return False

        current = ohlcv_data[current_idx]
        previous = ohlcv_data[current_idx - 1]

        ichimoku = self.calculate_ichimoku(ohlcv_data, current_idx)
        if ichimoku is None:
            return False

        upper, lower = self.get_kumo_boundaries(ichimoku)

        if upper is None or lower is None:
            return False

        if direction == "up":
            # Bullish breakout: price breaks above upper Kumo boundary
            # Current close above upper, previous close at or below upper
            return (
                current.close > upper
                and previous.close <= upper
            )
        elif direction == "down":
            # Bearish breakout: price breaks below lower Kumo boundary
            # Current close below lower, previous close at or above lower
            return (
                current.close < lower
                and previous.close >= lower
            )

        return False

    def calculate_atr(
        self,
        ohlcv_data: List[OHLCV],
        period: int = 14
    ) -> float:
        """
        Calculate Average True Range for stop loss placement.

        Args:
            ohlcv_data: List of OHLCV data
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
            prev_close = ohlcv_data[i - 1].close

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            true_ranges.append(tr)

        return sum(true_ranges[-period:]) / period if true_ranges else 0.0

    def entry_conditions(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if entry criteria are met.

        BUY: Upper Kumo breakout + AO histogram reversal from bottom up
        SELL: Lower Kumo breakout + AO histogram reversal from top to bottom

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        if current_idx < self.get_required_candles():
            return False, None

        current = ohlcv_data[current_idx]

        # Calculate Awesome Oscillator histogram
        ao_histogram = self.awesome_oscillator.calculate(ohlcv_data)

        # Check for BUY signal
        if self.is_kumo_breakout(ohlcv_data, current_idx, "up"):
            ao_reversal_up = self.awesome_oscillator.get_histogram_reversal(
                ao_histogram, current_idx, "up"
            )

            if ao_reversal_up:
                atr = self.calculate_atr(ohlcv_data)
                entry_price = current.close
                stop_loss = current.low - (atr * 2)
                risk = entry_price - stop_loss
                take_profit = entry_price + (risk * 2)

                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.BUY,
                    price=entry_price,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    confidence=0.75,
                    metadata={
                        "type": "kumo_breakout_buy",
                        "reason": "Upper Kumo breakout with AO bullish reversal",
                        "atr": atr,
                    }
                )

        # Check for SELL signal
        if self.is_kumo_breakout(ohlcv_data, current_idx, "down"):
            ao_reversal_down = self.awesome_oscillator.get_histogram_reversal(
                ao_histogram, current_idx, "down"
            )

            if ao_reversal_down:
                atr = self.calculate_atr(ohlcv_data)
                entry_price = current.close
                stop_loss = current.high + (atr * 2)
                risk = stop_loss - entry_price
                take_profit = entry_price - (risk * 2)

                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.SELL,
                    price=entry_price,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    confidence=0.75,
                    metadata={
                        "type": "kumo_breakout_sell",
                        "reason": "Lower Kumo breakout with AO bearish reversal",
                        "atr": atr,
                    }
                )

        return False, None

    def exit_conditions(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int,
        position
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if exit criteria are met for existing position.

        Exit conditions:
        - Opposite Kumo boundary break
        - Tenkan-Kijun cross in opposite direction
        - Price closes beyond cloud in opposite direction

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            position: Current position to check

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        if current_idx < 1:
            return False, None

        current = ohlcv_data[current_idx]
        ichimoku = self.calculate_ichimoku(ohlcv_data, current_idx)

        if ichimoku is None:
            return False, None

        upper, lower = self.get_kumo_boundaries(ichimoku)

        if position.side == "LONG":
            # Exit long if price breaks below lower Kumo boundary
            if current.close < lower:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.8,
                    metadata={"reason": "price_below_lower_kumo"}
                )

            # Exit if Tenkan crosses below Kijun (momentum reversal)
            if ichimoku.tenkan < ichimoku.kijun:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.7,
                    metadata={"reason": "tenkan_kijun_bearish_cross"}
                )

        elif position.side == "SHORT":
            # Exit short if price breaks above upper Kumo boundary
            if current.close > upper:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.8,
                    metadata={"reason": "price_above_upper_kumo"}
                )

            # Exit if Tenkan crosses above Kijun (momentum reversal)
            if ichimoku.tenkan > ichimoku.kijun:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.7,
                    metadata={"reason": "tenkan_kijun_bullish_cross"}
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

    def get_required_candles(self) -> int:
        """
        Get number of candles required for signal generation.

        Returns:
            Minimum number of candles needed
        """
        # Ichimoku requires: max(8, 29, 34) + 26 = 60
        # Awesome Oscillator requires: 34
        return max(
            self.ichimoku.get_required_period(),
            self.awesome_oscillator.slow_period
        ) + 10  # Buffer for calculations

    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        if not super().validate_config():
            return False

        if self.trailing_stop_pips < 0:
            self.logger.error(f"Invalid trailing_stop_pips: {self.trailing_stop_pips}")
            return False

        return True


    def backtest(self, start_date, end_date, initial_balance=100):
        """
        Run backtest for Kumo Breakout strategy.

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
                            sl_price = signals[i].high

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
            'strategy': 'Kumo Breakout',
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
