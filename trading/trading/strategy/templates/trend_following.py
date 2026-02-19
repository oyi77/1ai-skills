"""
Trend Following Strategy Template

Strategy based on Moving Average crossovers.
Entry when fast MA crosses above/below slow MA.
Exit on opposite crossover or trailing stop.
"""

from datetime import datetime
from typing import List, Optional, Tuple

from trading.brokers.base import OHLCV
from trading.strategy.templates.base import StrategyTemplate, Signal, SignalType


class TrendFollowingTemplate(StrategyTemplate):
    """
    Trend following strategy template using MA crossovers.
    
    Entry: Fast MA crosses above slow MA (bullish) or below (bearish)
    Exit: Opposite crossover, or price closes beyond MA
    """
    
    def __init__(
        self,
        symbol: str = "XAUUSD",
        timeframe: str = "H1",
        fast_ma_period: int = 10,
        slow_ma_period: int = 50,
        risk_per_trade: float = 0.02,
        use_trailing_stop: bool = True,
        trailing_stop_pips: float = 50.0,
        config: Optional[dict] = None,
    ):
        super().__init__(
            name="TrendFollowingTemplate",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )
        self.fast_ma_period = fast_ma_period
        self.slow_ma_period = slow_ma_period
        self.use_trailing_stop = use_trailing_stop
        self.trailing_stop_pips = trailing_stop_pips
    
    def calculate_sma(self, ohlcv_data: List[OHLCV], period: int) -> Optional[float]:
        """Calculate Simple Moving Average."""
        if len(ohlcv_data) < period:
            return None
        
        closes = [c.close for c in ohlcv_data[-period:]]
        return sum(closes) / period
    
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
        
        # Start with SMA
        ema = sum(closes) / period
        
        # Calculate EMA
        for price in closes[1:]:
            ema = (price - ema) * multiplier + ema
        
        return ema
    
    def calculate_ma_crossover(
        self,
        ohlcv_data: List[OHLCV],
        current_idx: int
    ) -> Tuple[Optional[float], Optional[float], str]:
        """
        Calculate MA values and detect crossover.
        
        Returns:
            (fast_ma, slow_ma, crossover_direction)
            direction: "bullish", "bearish", "none"
        """
        if current_idx < self.slow_ma_period:
            return None, None, "none"
        
        # Calculate current MAs
        fast_ma_curr = self.calculate_ema(
            ohlcv_data[:current_idx+1], 
            self.fast_ma_period
        )
        slow_ma_curr = self.calculate_ema(
            ohlcv_data[:current_idx+1], 
            self.slow_ma_period
        )
        
        # Calculate previous MAs
        fast_ma_prev = self.calculate_ema(
            ohlcv_data[:current_idx], 
            self.fast_ma_period
        )
        slow_ma_prev = self.calculate_ema(
            ohlcv_data[:current_idx], 
            self.slow_ma_period
        )
        
        if fast_ma_curr is None or slow_ma_curr is None:
            return None, None, "none"
        
        # Detect crossover
        if fast_ma_prev is not None and slow_ma_prev is not None:
            # Bullish: Fast crosses above slow
            if fast_ma_prev <= slow_ma_prev and fast_ma_curr > slow_ma_curr:
                return fast_ma_curr, slow_ma_curr, "bullish"
            # Bearish: Fast crosses below slow
            elif fast_ma_prev >= slow_ma_prev and fast_ma_curr < slow_ma_curr:
                return fast_ma_curr, slow_ma_curr, "bearish"
        
        return fast_ma_curr, slow_ma_curr, "none"
    
    def calculate_atr(
        self, 
        ohlcv_data: List[OHLCV], 
        period: int = 14
    ) -> float:
        """Calculate Average True Range."""
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
    
    def entry_conditions(
        self, 
        ohlcv_data: List[OHLCV], 
        current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if MA crossover entry criteria are met.
        
        Entry signals:
        - Bullish: Fast MA crosses above Slow MA
        - Bearish: Fast MA crosses below Slow MA
        """
        if current_idx < self.slow_ma_period:
            return False, None
        
        current = ohlcv_data[current_idx]
        fast_ma, slow_ma, direction = self.calculate_ma_crossover(
            ohlcv_data, 
            current_idx
        )
        
        if direction == "none" or fast_ma is None or slow_ma is None:
            return False, None
        
        # Calculate ATR for stops
        atr = self.calculate_atr(ohlcv_data)
        pip_value = self.calculate_pip_value(self.symbol)
        
        if direction == "bullish":
            # Entry at current close or market
            entry_price = current.close
            stop_loss = current.low - (atr * 2)
            # Risk-reward 1:2
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
                confidence=0.8,
                metadata={
                    "type": "bullish_crossover",
                    "fast_ma": fast_ma,
                    "slow_ma": slow_ma,
                    "atr": atr,
                }
            )
        
        elif direction == "bearish":
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
                confidence=0.8,
                metadata={
                    "type": "bearish_crossover",
                    "fast_ma": fast_ma,
                    "slow_ma": slow_ma,
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
        Check if exit criteria are met.
        
        Exit signals:
        - Opposite MA crossover
        - Price closes below/below MA (trend change)
        """
        if current_idx < self.slow_ma_period:
            return False, None
        
        current = ohlcv_data[current_idx]
        
        # Get current MA values
        fast_ma, slow_ma, direction = self.calculate_ma_crossover(
            ohlcv_data, 
            current_idx
        )
        
        if fast_ma is None or slow_ma is None:
            return False, None
        
        if position.side == "LONG":
            # Exit on bearish crossover
            if direction == "bearish":
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.9,
                    metadata={"reason": "bearish_crossover_exit"}
                )
            
            # Exit if price closes below slow MA
            if current.close < slow_ma:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.7,
                    metadata={"reason": "below_sma_exit"}
                )
            
            # Trailing stop check
            if self.use_trailing_stop:
                trailing_stop = position.entry_price + (
                    (position.entry_price - position.stop_loss) * 1.5
                )
                if current.close > trailing_stop:
                    new_stop = position.entry_price + (
                        (current.close - position.entry_price) * 0.5
                    )
                    if current.low <= new_stop:
                        return True, Signal(
                            timestamp=current.time,
                            symbol=self.symbol,
                            timeframe=self.timeframe,
                            signal_type=SignalType.CLOSE_LONG,
                            price=new_stop,
                            confidence=1.0,
                            metadata={"reason": "trailing_stop"}
                        )
        
        elif position.side == "SHORT":
            # Exit on bullish crossover
            if direction == "bullish":
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.9,
                    metadata={"reason": "bullish_crossover_exit"}
                )
            
            # Exit if price closes above slow MA
            if current.close > slow_ma:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.7,
                    metadata={"reason": "above_sma_exit"}
                )
            
            # Trailing stop check
            if self.use_trailing_stop:
                trailing_stop = position.entry_price - (
                    (position.stop_loss - position.entry_price) * 1.5
                )
                if current.close < trailing_stop:
                    new_stop = position.entry_price - (
                        (position.entry_price - current.close) * 0.5
                    )
                    if current.high >= new_stop:
                        return True, Signal(
                            timestamp=current.time,
                            symbol=self.symbol,
                            timeframe=self.timeframe,
                            signal_type=SignalType.CLOSE_SHORT,
                            price=new_stop,
                            confidence=1.0,
                            metadata={"reason": "trailing_stop"}
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
        
        stop_loss_pips = self.calculate_stop_loss_pips(entry_price, stop_loss)
        
        return self.calculate_position_size_from_risk(
            account_balance=account_balance,
            stop_loss_pips=stop_loss_pips,
        )
    
    def get_required_candles(self) -> int:
        """Get number of candles required."""
        return self.slow_ma_period + 14
    
    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        if not super().validate_config():
            return False
        
        if self.fast_ma_period >= self.slow_ma_period:
            self.logger.error(
                f"fast_ma_period ({self.fast_ma_period}) must be "
                f"less than slow_ma_period ({self.slow_ma_period})"
            )
            return False
        
        return True
