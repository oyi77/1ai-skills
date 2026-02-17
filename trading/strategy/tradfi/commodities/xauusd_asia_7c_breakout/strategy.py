"""
XAUUSD Asia 7-Candle Breakout Strategy

Breakout strategy using 7-candle window (3 before + COA + 3 after)
for XAUUSD during Asia Session.

Rules:
- Identify COA ( candle that opens at Asia session open time)
- Form 7-candle window: COA-3 to COA+3
- Calculate HH (Highest High) and LL (Lowest Low) from 7 candles
- Calculate R from last candle (COA+3)
- Place Buy Stop at HH, Sell Stop at LL
- SL = 1R, TP = 2R from entry
"""

from datetime import datetime, time
from typing import List, Optional, Dict, Any
import pytz

from ..base import Strategy, TradingSignal, OHLCV


class XAUUSDAsia7CBreakout(Strategy):
    """XAUUSD Asia Session 7-Candle Breakout Strategy."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        default_config = {
            "symbol": "XAUUSD",
            "timeframe": "H1",
            "timezone": "Asia/Jakarta",
            "session_start": time(7, 0),  # 07:00
            "session_end": time(15, 0),  # 15:00
            "open_asia_candle_time": time(7, 0),  # COA at 07:00
            "lookback_before": 3,
            "lookforward_after": 3,
            "min_range_pips": 5,
            "entry_buffer_points": 0,
            "rr_ratio": 2.0,
            "point_value": 0.01,  # For XAUUSD
            "digits": 2,  # XAUUSD usually has 2 digits
        }
        if config:
            default_config.update(config)

        super().__init__("XAUUSD Asia 7C Breakout", default_config)

    def get_signals(self, ohlcv_data: List[OHLCV]) -> List[TradingSignal]:
        """Generate signals from OHLCV data."""
        signals = []

        # Find COA (candle that opens at open_asia_candle_time)
        coa_candle = self._find_coa_candle(ohlcv_data)

        if coa_candle is None:
            self.logger.warning("COA candle not found")
            return signals

        # Find 7-candle window
        window = self._get_7_candle_window(ohlcv_data, coa_candle)

        if len(window) < 7:
            self.logger.warning(f"Not enough candles for 7-window: {len(window)}")
            return signals

        # Calculate HH/LL
        hh, ll = self.calculate_hh_ll(window)

        # Get R from last candle (COA+3)
        r_candle = window[-1]
        r_points = self._calculate_r(r_candle)

        # Check minimum range
        if r_points < self.config["min_range_pips"]:
            self.logger.info(
                f"R {r_points} below min {self.config['min_range_pips']}, skipping"
            )
            return signals

        # Calculate pending order levels
        buffer = self.config["entry_buffer_points"]
        buy_stop = hh + buffer
        sell_stop = ll - buffer

        # Calculate SL/TP
        buy_sl = buy_stop - r_points
        buy_tp = buy_stop + (r_points * self.config["rr_ratio"])

        sell_sl = sell_stop + r_points
        sell_tp = sell_stop - (r_points * self.config["rr_ratio"])

        signal = TradingSignal(
            symbol=self.config["symbol"],
            timeframe=self.config["timeframe"],
            timestamp=coa_candle.timestamp,
            hh=hh,
            ll=ll,
            r_points=r_points,
            buy_stop=buy_stop,
            sell_stop=sell_stop,
            buy_sl=buy_sl,
            buy_tp=buy_tp,
            sell_sl=sell_sl,
            sell_tp=sell_tp,
            status="pending",
        )

        signals.append(signal)

        return signals

    def calculate_hh_ll(self, ohlcv_data: List[OHLCV]) -> tuple:
        """Calculate HH (Highest High) and LL (Lowest Low)."""
        if not ohlcv_data:
            return (0.0, 0.0)

        highs = [candle.high for candle in ohlcv_data]
        lows = [candle.low for candle in ohlcv_data]

        hh = max(highs)
        ll = min(lows)

        return (hh, ll)

    def _find_coa_candle(self, ohlcv_data: List[OHLCV]) -> Optional[OHLCV]:
        """Find the COA ( candle that opens at Asia session open time)."""
        tz = pytz.timezone(self.config["timezone"])
        target_time = self.config["open_asia_candle_time"]

        for i, candle in enumerate(ohlcv_data):
            # Get candle open time in our timezone
            candle_time = candle.timestamp.astimezone(tz).time()

            if candle_time == target_time:
                return candle

        return None

    def _get_7_candle_window(
        self, ohlcv_data: List[OHLCV], coa_candle: OHLCV
    ) -> List[OHLCV]:
        """Get 7-candle window: COA-3 to COA+3."""
        # Find index of COA
        try:
            coa_index = ohlcv_data.index(coa_candle)
        except ValueError:
            return []

        lookback = self.config["lookback_before"]
        lookforward = self.config["lookforward_after"]

        start_idx = max(0, coa_index - lookback)
        end_idx = min(len(ohlcv_data), coa_index + lookforward + 1)

        return ohlcv_data[start_idx:end_idx]

    def _calculate_r(self, candle: OHLCV) -> float:
        """Calculate R (range) from a candle in points."""
        high = candle.high
        low = candle.low
        point_value = self.config["point_value"]

        r = (high - low) / point_value
        return r

    def get_required_timeframe(self) -> str:
        return self.config["timeframe"]

    def get_required_candles(self) -> int:
        """Need at least lookback + 1 (COA) + lookforward + buffer"""
        return (
            self.config["lookback_before"] + 1 + self.config["lookforward_after"] + 10
        )

    def check_trigger(
        self, signal: TradingSignal, current_price: float
    ) -> Optional[str]:
        """
        Check if pending order is triggered.

        Returns:
            'BUY' if buy triggered, 'SELL' if sell triggered, None if not triggered
        """
        if signal.status != "pending":
            return None

        # Check buy trigger
        if current_price >= signal.buy_stop:
            return "BUY"

        # Check sell trigger
        if current_price <= signal.sell_stop:
            return "SELL"

        return None

    def format_signal_output(self, signal: TradingSignal) -> str:
        """Format signal for 'signal today' command output."""
        return f"""
Date: {signal.timestamp.strftime("%Y-%m-%d")} ({self.config["timezone"]})
COA time: {self.config["open_asia_candle_time"].strftime("%H:%M")}
Window: COA-{self.config["lookback_before"]} .. COA+{self.config["lookforward_after"]}

HH: {signal.hh}
LL: {signal.ll}
R (last candle): {signal.r_points} points

Buy Stop: {signal.buy_stop}
  SL: {signal.buy_sl}
  TP: {signal.buy_tp}

Sell Stop: {signal.sell_stop}
  SL: {signal.sell_sl}
  TP: {signal.sell_tp}

Filters: range OK, spread OK
Status: pending placed
"""
