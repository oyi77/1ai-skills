"""
Volume Momentum Crypto Strategy

Scalping strategy for cryptocurrency markets using volume surges
and momentum indicators for entry confirmation.

Entry: Volume surge (150-200%+ of average) + momentum confirmation
Exit: SL hit or TP hit

Indicators:
- MACD(12, 26, 9) for momentum direction
- RSI(14) for overbought/oversold confirmation (60-80 bullish, 20-40 bearish)
- Volume confirmation (150-200%+ of 20-period average)

Timeframe: 5M-15M scalping
Supported pairs: BTC/USD, ETH/USD
"""

from datetime import datetime
from typing import List, Optional, Tuple

from ....brokers.base import OHLCV
from ..base import StrategyTemplate, Signal, SignalType


class VolumeMomentumStrategy(StrategyTemplate):
    """
    Volume Momentum strategy for crypto scalping.

    Combines volume surge detection with MACD and RSI momentum confirmation
    for high-probability short-term entries.

    Entry Conditions:
    - BUY: Volume 150-200%+ of average + MACD bullish + RSI 60-80
    - SELL: Volume 150-200%+ of average + MACD bearish + RSI 20-40

    Exit Conditions:
    - Stop loss hit
    - Take profit hit
    """

    def __init__(
        self,
        symbol: str = "BTCUSD",
        timeframe: str = "M5",
        macd_fast: int = 12,
        macd_slow: int = 26,
        macd_signal: int = 9,
        rsi_period: int = 14,
        rsi_buy_min: float = 60.0,
        rsi_buy_max: float = 80.0,
        rsi_sell_min: float = 20.0,
        rsi_sell_max: float = 40.0,
        volume_surge_min: float = 1.5,  # 150% of average
        volume_surge_max: float = 2.0,  # 200% of average
        volume_period: int = 20,
        risk_per_trade: float = 0.02,
        profit_target_pct: float = 0.5,  # 0.5% profit target
        stop_loss_pct: float = 0.3,  # 0.3% stop loss
        config: Optional[dict] = None,
    ):
        super().__init__(
            name="VolumeMomentumStrategy",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )
        # MACD parameters
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal

        # RSI parameters
        self.rsi_period = rsi_period
        self.rsi_buy_min = rsi_buy_min
        self.rsi_buy_max = rsi_buy_max
        self.rsi_sell_min = rsi_sell_min
        self.rsi_sell_max = rsi_sell_max

        # Volume parameters
        self.volume_surge_min = volume_surge_min
        self.volume_surge_max = volume_surge_max
        self.volume_period = volume_period

        # Risk management
        self.profit_target_pct = profit_target_pct
        self.stop_loss_pct = stop_loss_pct

    def calculate_ema(
        self,
        ohlcv_data: List[OHLCV],
        period: int,
        smoothing: float = 2.0
    ) -> Optional[float]:
        """Calculate Exponential Moving Average."""
        if len(ohlcv_data) < period:
            return None

        closes = [c.close for c in ohlcv_data[-period:]]
        multiplier = smoothing / (period + 1)

        ema = sum(closes) / period

        for price in closes[1:]:
            ema = (price - ema) * multiplier + ema

        return ema

    def calculate_macd(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int
    ) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """
        Calculate MACD values (MACD line, Signal line, Histogram).

        Returns:
            Tuple of (macd_line, signal_line, histogram)
        """
        required_period = max(self.macd_fast, self.macd_slow) + self.macd_signal
        if current_idx < required_period:
            return None, None, None

        # Calculate EMAs for MACD
        ema_fast = self.calculate_ema(
            ohlcv_data[:current_idx + 1],
            self.macd_fast
        )
        ema_slow = self.calculate_ema(
            ohlcv_data[:current_idx + 1],
            self.macd_slow
        )

        if ema_fast is None or ema_slow is None:
            return None, None, None

        macd_line = ema_fast - ema_slow

        # Calculate signal line (EMA of MACD line)
        macd_history = []
        for i in range(max(0, current_idx - self.macd_signal + 1), current_idx + 1):
            prev_ema_fast = self.calculate_ema(
                ohlcv_data[:i + 1],
                self.macd_fast
            )
            prev_ema_slow = self.calculate_ema(
                ohlcv_data[:i + 1],
                self.macd_slow
            )
            if prev_ema_fast is not None and prev_ema_slow is not None:
                macd_history.append(prev_ema_fast - prev_ema_slow)

        if len(macd_history) < self.macd_signal:
            return None, None, None

        signal_line = self.calculate_ema(
            [OHLCV(close=v, **{'timestamp': None, 'open': v, 'high': v, 'low': v, 'volume': 0}) for v in macd_history],
            self.macd_signal
        )

        if signal_line is None:
            return None, None, None

        histogram = macd_line - signal_line

        return macd_line, signal_line, histogram

    def calculate_rsi(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int
    ) -> Optional[float]:
        """Calculate RSI value."""
        if current_idx < self.rsi_period + 1:
            return None

        closes = [c.close for c in ohlcv_data[current_idx - self.rsi_period:current_idx + 1]]

        gains = []
        losses = []

        for i in range(1, len(closes)):
            change = closes[i] - closes[i - 1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        if len(gains) == 0:
            return None

        avg_gain = sum(gains) / len(gains)
        avg_loss = sum(losses) / len(losses)

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))

        return rsi

    def calculate_average_volume(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int,
        period: int = None
    ) -> Optional[float]:
        """Calculate average volume over specified period."""
        if period is None:
            period = self.volume_period

        if current_idx < period:
            return None

        volumes = [c.volume for c in ohlcv_data[current_idx - period:current_idx + 1]]
        return sum(volumes) / len(volumes)

    def calculate_volume_surge_ratio(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int
    ) -> Optional[float]:
        """Calculate current volume as ratio of average volume."""
        avg_volume = self.calculate_average_volume(ohlcv_data, current_idx)
        if avg_volume is None or avg_volume == 0:
            return None

        current_volume = ohlcv_data[current_idx].volume
        return current_volume / avg_volume

    def is_volume_surge(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int
    ) -> bool:
        """Check if current volume is a surge (150-200%+ of average)."""
        ratio = self.calculate_volume_surge_ratio(ohlcv_data, current_idx)
        if ratio is None:
            return False

        return self.volume_surge_min <= ratio <= self.volume_surge_max

    def entry_conditions(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """Check if volume momentum entry criteria are met."""
        required_candles = max(
            self.macd_slow + self.macd_signal,
            self.rsi_period + 1,
            self.volume_period
        )
        if current_idx < required_candles:
            return False, None

        current = ohlcv_data[current_idx]

        # Check volume surge first (mandatory)
        if not self.is_volume_surge(ohlcv_data, current_idx):
            return False, None

        # Calculate indicators
        macd_line, signal_line, histogram = self.calculate_macd(ohlcv_data, current_idx)
        rsi = self.calculate_rsi(ohlcv_data, current_idx)

        if macd_line is None or signal_line is None or rsi is None:
            return False, None

        # MACD momentum direction
        macd_bullish = macd_line > signal_line
        macd_bearish = macd_line < signal_line

        # RSI momentum confirmation
        rsi_bullish = self.rsi_buy_min <= rsi <= self.rsi_buy_max
        rsi_bearish = self.rsi_sell_min <= rsi <= self.rsi_sell_max

        # Calculate SL/TP
        entry_price = current.close
        profit_target = self.profit_target_pct / 100.0
        stop_loss = self.stop_loss_pct / 100.0

        # BUY signal: Volume surge + MACD bullish + RSI bullish
        if macd_bullish and rsi_bullish:
            tp = entry_price * (1 + profit_target)
            sl = entry_price * (1 - stop_loss)

            return True, Signal(
                timestamp=current.timestamp,
                symbol=self.symbol,
                timeframe=self.timeframe,
                signal_type=SignalType.BUY,
                price=entry_price,
                stop_loss=sl,
                take_profit=tp,
                confidence=0.75,
                metadata={
                    "type": "volume_momentum_long",
                    "macd_line": macd_line,
                    "signal_line": signal_line,
                    "histogram": histogram,
                    "rsi": rsi,
                    "volume_ratio": self.calculate_volume_surge_ratio(ohlcv_data, current_idx),
                }
            )

        # SELL signal: Volume surge + MACD bearish + RSI bearish
        if macd_bearish and rsi_bearish:
            tp = entry_price * (1 - profit_target)
            sl = entry_price * (1 + stop_loss)

            return True, Signal(
                timestamp=current.timestamp,
                symbol=self.symbol,
                timeframe=self.timeframe,
                signal_type=SignalType.SELL,
                price=entry_price,
                stop_loss=sl,
                take_profit=tp,
                confidence=0.75,
                metadata={
                    "type": "volume_momentum_short",
                    "macd_line": macd_line,
                    "signal_line": signal_line,
                    "histogram": histogram,
                    "rsi": rsi,
                    "volume_ratio": self.calculate_volume_surge_ratio(ohlcv_data, current_idx),
                }
            )

        return False, None

    def exit_conditions(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int,
        position
    ) -> Tuple[bool, Optional[Signal]]:
        """Check if exit criteria are met."""
        if current_idx < 1:
            return False, None

        current = ohlcv_data[current_idx]

        if position.side == "LONG":
            # Stop loss hit
            if current.low <= position.stop_loss:
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=position.stop_loss,
                    confidence=1.0,
                    metadata={"reason": "stop_loss"}
                )

            # Take profit hit
            if current.high >= position.take_profit:
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=position.take_profit,
                    confidence=1.0,
                    metadata={"reason": "take_profit"}
                )

        elif position.side == "SHORT":
            # Stop loss hit
            if current.high >= position.stop_loss:
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=position.stop_loss,
                    confidence=1.0,
                    metadata={"reason": "stop_loss"}
                )

            # Take profit hit
            if current.low <= position.take_profit:
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=position.take_profit,
                    confidence=1.0,
                    metadata={"reason": "take_profit"}
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
        """Calculate position size based on risk management."""
        if stop_loss == entry_price:
            return 0.0

        stop_loss_pct = abs(entry_price - stop_loss) / entry_price
        stop_loss_pips = stop_loss_pct * 10000  # Convert to "pips" for consistency

        return self.calculate_position_size_from_risk(
            account_balance=account_balance,
            stop_loss_pips=stop_loss_pips,
        )

    def get_required_candles(self) -> int:
        """Get number of candles required for signal generation."""
        return max(
            self.macd_slow + self.macd_signal + 10,
            self.rsi_period + 10,
            self.volume_period + 10
        )

    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        if not super().validate_config():
            return False

        if self.profit_target_pct <= 0:
            self.logger.error(f"Invalid profit_target_pct: {self.profit_target_pct}")
            return False

        if self.stop_loss_pct <= 0:
            self.logger.error(f"Invalid stop_loss_pct: {self.stop_loss_pct}")
            return False

        if self.volume_surge_min < 1.0:
            self.logger.error(f"Invalid volume_surge_min: {self.volume_surge_min}")
            return False

        if self.volume_surge_max < self.volume_surge_min:
            self.logger.error(f"volume_surge_max ({self.volume_surge_max}) must be >= volume_surge_min ({self.volume_surge_min})")
            return False

        # Validate symbol
        supported_symbols = ["BTCUSD", "BTC/USDT", "ETHUSD", "ETH/USDT", "XBTUSD"]
        if self.symbol not in supported_symbols:
            self.logger.warning(f"Symbol {self.symbol} may not be optimized. Supported: {supported_symbols}")

        return True


    def backtest(self, start_date, end_date, initial_balance=100):
        """
        Run backtest for Volume Momentum strategy.

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
            'strategy': 'Volume Momentum',
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
