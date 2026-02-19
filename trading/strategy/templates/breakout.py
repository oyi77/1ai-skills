"""
Breakout Strategy Template

Strategy based on breaking HH (Higher High) / LL (Lower Low) levels.
Entry when price breaks recent high/low with volume confirmation.
"""

from datetime import datetime
from typing import List, Optional, Tuple

from trading.brokers.base import OHLCV
from trading.strategy.templates.base import StrategyTemplate, Signal, SignalType


class BreakoutTemplate(StrategyTemplate):
    """
    Breakout strategy template.
    
    Entry: Price breaks above HH (bullish) or below LL (bearish)
    Exit: Price reaches take profit or stops out at SL
    """
    
    def __init__(
        self,
        symbol: str = "XAUUSD",
        timeframe: str = "H1",
        lookback_period: int = 20,
        atr_multiplier: float = 2.0,
        risk_per_trade: float = 0.02,
        min_volume_ratio: float = 1.5,
        config: Optional[dict] = None,
    ):
        super().__init__(
            name="BreakoutTemplate",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )
        self.lookback_period = lookback_period
        self.atr_multiplier = atr_multiplier
        self.min_volume_ratio = min_volume_ratio
    
    def calculate_hh_ll(self, ohlcv_data: List[OHLCV], period: int) -> Tuple[float, float]:
        """Calculate Highest High and Lowest Low over the period."""
        if len(ohlcv_data) < period:
            return 0.0, 0.0
        
        highs = [c.high for c in ohlcv_data[-period:]]
        lows = [c.low for c in ohlcv_data[-period:]]
        
        return max(highs), min(lows)
    
    def calculate_atr(self, ohlcv_data: List[OHLCV], period: int = 14) -> float:
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
    
    def calculate_avg_volume(self, ohlcv_data: List[OHLCV], period: int = 20) -> float:
        """Calculate average volume over period."""
        if len(ohlcv_data) < period:
            return 0.0
        
        volumes = [c.volume for c in ohlcv_data[-period:]]
        return sum(volumes) / period
    
    def entry_conditions(
        self, 
        ohlcv_data: List[OHLCV], 
        current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """Check if breakout entry criteria are met."""
        if current_idx < self.lookback_period:
            return False, None
        
        current = ohlcv_data[current_idx]
        prev = ohlcv_data[current_idx - 1]
        
        # Get HH/LL
        hh, ll = self.calculate_hh_ll(ohlcv_data, self.lookback_period)
        
        # Calculate ATR for stop loss
        atr = self.calculate_atr(ohlcv_data)
        
        # Calculate average volume
        avg_volume = self.calculate_avg_volume(ohlcv_data)
        volume_ratio = current.volume / avg_volume if avg_volume > 0 else 0
        
        # Bullish breakout: price breaks above HH
        if current.close > hh and prev.close <= hh:
            if volume_ratio >= self.min_volume_ratio:
                entry_price = hh
                stop_loss = current.low - (atr * self.atr_multiplier * 0.5)
                take_profit = entry_price + (entry_price - stop_loss) * 2
                
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.BUY,
                    price=entry_price,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    confidence=min(volume_ratio / 2.0, 1.0),
                    metadata={
                        "type": "bullish_breakout",
                        "hh": hh,
                        "ll": ll,
                        "atr": atr,
                        "volume_ratio": volume_ratio,
                    }
                )
        
        # Bearish breakout: price breaks below LL
        if current.close < ll and prev.close >= ll:
            if volume_ratio >= self.min_volume_ratio:
                entry_price = ll
                stop_loss = current.high + (atr * self.atr_multiplier * 0.5)
                take_profit = entry_price - (stop_loss - entry_price) * 2
                
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.SELL,
                    price=entry_price,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    confidence=min(volume_ratio / 2.0, 1.0),
                    metadata={
                        "type": "bearish_breakout",
                        "hh": hh,
                        "ll": ll,
                        "atr": atr,
                        "volume_ratio": volume_ratio,
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
        
        stop_loss_pips = self.calculate_stop_loss_pips(entry_price, stop_loss)
        
        return self.calculate_position_size_from_risk(
            account_balance=account_balance,
            stop_loss_pips=stop_loss_pips,
        )
    
    def get_required_candles(self) -> int:
        """Get number of candles required."""
        return self.lookback_period + 14
    
    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        if not super().validate_config():
            return False
        
        if self.lookback_period < 5:
            self.logger.error(f"lookback_period too small: {self.lookback_period}")
            return False
        
        if self.atr_multiplier <= 0:
            self.logger.error(f"Invalid atr_multiplier: {self.atr_multiplier}")
            return False
        
        return True
