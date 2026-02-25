"""
Momentum Elder FOREX Strategy

Strategy based on the Momentum Elder method from ForexTester.
Combines EMA(19) for trend direction and Momentum(18, close, 100) for signal generation.

Entry BUY:
- Closing price above EMA(19) (uptrend)
- Momentum crosses 100 from bottom up

Entry SELL:
- Closing price below EMA(19) (downtrend)
- Momentum crosses 100 from top to bottom

Exit:
- Opposite momentum crossover
- Price closes beyond EMA in opposite direction

Timeframe: H1 minimum
Support major pairs: EUR/USD, GBP/USD, USD/JPY (configurable)
"""

from datetime import datetime
from typing import List, Optional, Tuple

from ....brokers.base import OHLCV
from ..base import StrategyTemplate, Signal, SignalType
from ....indicators.moving_averages import EMA


class MomentumElderStrategy(StrategyTemplate):
    """
    Momentum Elder FOREX strategy implementation.

    Combines EMA(19) for trend direction and Momentum(18, close, 100) for signal generation.

    Attributes:
        ema_period: Period for EMA (default: 19)
        momentum_period: Period for Momentum calculation (default: 18)
        momentum_baseline: Baseline level for Momentum (default: 100)
        min_timeframe: Minimum timeframe (default: H1)
    """

    # Valid timeframes for this strategy (H1 minimum)
    VALID_TIMEFRAMES = ["H1", "H4", "D1", "W1"]

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
        timeframe: str = "H1",
        ema_period: int = 19,
        momentum_period: int = 18,
        momentum_baseline: float = 100.0,
        risk_per_trade: float = 0.02,
        config: Optional[dict] = None,
    ):
        """
        Initialize Momentum Elder strategy.

        Args:
            symbol: Trading symbol (default: EUR/USD)
            timeframe: Chart timeframe (default: H1)
            ema_period: EMA period (default: 19)
            momentum_period: Period for Momentum calculation (default: 18)
            momentum_baseline: Baseline level for Momentum (default: 100)
            risk_per_trade: Risk per trade as fraction (default: 0.02 = 2%)
            config: Additional configuration dictionary
        """
        super().__init__(
            name="MomentumElderStrategy",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )

        # Indicator parameters
        self.ema_period = ema_period
        self.momentum_period = momentum_period
        self.momentum_baseline = momentum_baseline

        # Initialize EMA indicator
        self.ema_indicator = EMA(period=ema_period)

    def calculate_momentum(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Optional[float]:
        """
        Calculate Momentum value.

        Momentum formula: (Current Close - Close N periods ago) / Close N periods ago * 100

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            Momentum value or None if insufficient data
        """
        if current_idx < self.momentum_period:
            return None

        current_close = ohlcv_data[current_idx].close
        past_close = ohlcv_data[current_idx - self.momentum_period].close

        if past_close == 0:
            return None

        momentum = ((current_close - past_close) / past_close) * 100
        return momentum

    def calculate_momentum_previous(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Optional[float]:
        """
        Calculate previous Momentum value (for crossover detection).

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            Previous Momentum value or None if insufficient data
        """
        if current_idx < self.momentum_period + 1:
            return None

        prev_close = ohlcv_data[current_idx - 1].close
        past_close = ohlcv_data[current_idx - 1 - self.momentum_period].close

        if past_close == 0:
            return None

        momentum = ((prev_close - past_close) / past_close) * 100
        return momentum

    def _get_ema_values(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Tuple[Optional[float], Optional[float]]:
        """
        Get EMA values for current and previous candle.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            Tuple of (current_ema, prev_ema)
        """
        if current_idx < self.ema_period:
            return None, None

        # Get all EMA values up to current index
        ema_values = self.ema_indicator.calculate(ohlcv_data[: current_idx + 1])

        if ema_values[-1] is None:
            return None, None

        current_ema = ema_values[-1]
        prev_ema = ema_values[-2] if len(ema_values) > 1 else None

        return current_ema, prev_ema

    def _is_uptrend(self, ohlcv_data: List[OHLCV], current_idx: int) -> bool:
        """
        Check if market is in uptrend based on EMA position.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index

        Returns:
            True if price is above EMA (uptrend)
        """
        current_ema, _ = self._get_ema_values(ohlcv_data, current_idx)
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
        current_ema, _ = self._get_ema_values(ohlcv_data, current_idx)
        if current_ema is None:
            return False

        current_price = ohlcv_data[current_idx].close
        return current_price < current_ema

    def _detect_momentum_crossover(
        self, ohlcv_data: List[OHLCV], current_idx: int, direction: str
    ) -> bool:
        """
        Detect Momentum crossover of baseline.

        Args:
            ohlcv_data: OHLCV data
            current_idx: Current candle index
            direction: "up" for bullish crossover, "down" for bearish crossover

        Returns:
            True if crossover detected
        """
        current_momentum = self.calculate_momentum(ohlcv_data, current_idx)
        prev_momentum = self.calculate_momentum_previous(ohlcv_data, current_idx)

        if current_momentum is None or prev_momentum is None:
            return False

        if direction == "up":
            # Bullish crossover: Momentum crosses 100 from bottom up
            return prev_momentum <= self.momentum_baseline and current_momentum > self.momentum_baseline
        elif direction == "down":
            # Bearish crossover: Momentum crosses 100 from top to bottom
            return prev_momentum >= self.momentum_baseline and current_momentum < self.momentum_baseline

        return False

    def _calculate_atr(
        self, ohlcv_data: List[OHLCV], period: int = 14
    ) -> float:
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
            prev_close = ohlcv_data[i - 1].close

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            true_ranges.append(tr)

        return sum(true_ranges[-period:]) / period if true_ranges else 0.0

    def entry_conditions(
        self, ohlcv_data: List[OHLCV], current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if entry criteria are met for Momentum Elder strategy.

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        current = ohlcv_data[current_idx]

        # Check minimum index requirements
        min_required = max(self.ema_period, self.momentum_period + 1) + 5
        if current_idx < min_required:
            return False, None

        # Check for BUY entry
        if self._is_uptrend(ohlcv_data, current_idx):
            if self._detect_momentum_crossover(ohlcv_data, current_idx, direction="up"):
                # Calculate stop loss and take profit
                current_ema, _ = self._get_ema_values(ohlcv_data, current_idx)
                atr = self._calculate_atr(ohlcv_data)

                entry_price = current.close
                stop_loss = current.low - (atr * 2) if atr > 0 else current.close * 0.02
                risk = entry_price - stop_loss
                take_profit = entry_price + (risk * 2)

                current_momentum = self.calculate_momentum(ohlcv_data, current_idx)

                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.BUY,
                    price=entry_price,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    confidence=0.8,
                    metadata={
                        "type": "momentum_elder_buy",
                        "ema_period": self.ema_period,
                        "momentum_period": self.momentum_period,
                        "momentum_baseline": self.momentum_baseline,
                        "ema_value": current_ema,
                        "momentum_value": current_momentum,
                    }
                )

        # Check for SELL entry
        if self._is_downtrend(ohlcv_data, current_idx):
            if self._detect_momentum_crossover(ohlcv_data, current_idx, direction="down"):
                # Calculate stop loss and take profit
                current_ema, _ = self._get_ema_values(ohlcv_data, current_idx)
                atr = self._calculate_atr(ohlcv_data)

                entry_price = current.close
                stop_loss = current.high + (atr * 2) if atr > 0 else current.close * 0.02
                risk = stop_loss - entry_price
                take_profit = entry_price - (risk * 2)

                current_momentum = self.calculate_momentum(ohlcv_data, current_idx)

                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.SELL,
                    price=entry_price,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    confidence=0.8,
                    metadata={
                        "type": "momentum_elder_sell",
                        "ema_period": self.ema_period,
                        "momentum_period": self.momentum_period,
                        "momentum_baseline": self.momentum_baseline,
                        "ema_value": current_ema,
                        "momentum_value": current_momentum,
                    }
                )

        return False, None

    def exit_conditions(
        self, ohlcv_data: List[OHLCV], current_idx: int, position
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if exit criteria are met for Momentum Elder strategy.

        Exit when:
        - Opposite momentum crossover occurs
        - Price closes beyond EMA in opposite direction

        Args:
            ohlcv_data: Historical OHLCV data
            current_idx: Current candle index
            position: Current position to check

        Returns:
            Tuple of (conditions_met, signal_or_none)
        """
        current = ohlcv_data[current_idx]

        # Check for opposite momentum crossover
        if position.side == "LONG":
            # Check for bearish momentum crossover (exit long)
            if self._detect_momentum_crossover(ohlcv_data, current_idx, direction="down"):
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.85,
                    metadata={"reason": "momentum_bearish_crossover"}
                )

            # Check if price closed below EMA (trend reversal)
            current_ema, _ = self._get_ema_values(ohlcv_data, current_idx)
            if current_ema is not None and current.close < current_ema:
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.75,
                    metadata={"reason": "price_below_ema"}
                )

        elif position.side == "SHORT":
            # Check for bullish momentum crossover (exit short)
            if self._detect_momentum_crossover(ohlcv_data, current_idx, direction="up"):
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.85,
                    metadata={"reason": "momentum_bullish_crossover"}
                )

            # Check if price closed above EMA (trend reversal)
            current_ema, _ = self._get_ema_values(ohlcv_data, current_idx)
            if current_ema is not None and current.close > current_ema:
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.75,
                    metadata={"reason": "price_above_ema"}
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
        # Need enough candles for EMA and Momentum calculations
        return max(self.ema_period, self.momentum_period + 1) + 20

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
                f"Timeframe {self.timeframe} is below minimum H1. "
                f"Strategy may not perform optimally."
            )

        # Validate EMA period
        if self.ema_period <= 0:
            self.logger.error(f"Invalid ema_period: {self.ema_period}")
            return False

        # Validate momentum period
        if self.momentum_period <= 0:
            self.logger.error(f"Invalid momentum_period: {self.momentum_period}")
            return False

        # Validate momentum baseline
        if self.momentum_baseline <= 0:
            self.logger.error(f"Invalid momentum_baseline: {self.momentum_baseline}")
            return False

        return True

    def backtest(self, start_date, end_date, initial_balance=100):
        """
        Run backtest for Momentum Elder strategy.

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
            'strategy': 'Momentum Elder',
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
