"""
Scalping Strategy Template

Short-term trading strategy for quick trades.
Uses tight stops and quick profit targets on low timeframe.
Entry based on EMA alignment and momentum.
"""

from datetime import datetime
from typing import List, Optional, Tuple

from trading.brokers.base import OHLCV
from trading.strategy.templates.base import StrategyTemplate, Signal, SignalType


class ScalpingTemplate(StrategyTemplate):
    """
    Scalping strategy template for short-term trades.
    
    Entry: EMA alignment + momentum confirmation
    Exit: Quick profit target or tight stop loss
    """
    
    def __init__(
        self,
        symbol: str = "XAUUSD",
        timeframe: str = "M5",
        ema_fast: int = 5,
        ema_medium: int = 13,
        ema_slow: int = 50,
        risk_per_trade: float = 0.01,
        profit_target_pips: float = 10.0,
        stop_loss_pips: float = 8.0,
        config: Optional[dict] = None,
    ):
        super().__init__(
            name="ScalpingTemplate",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )
        self.ema_fast = ema_fast
        self.ema_medium = ema_medium
        self.ema_slow = ema_slow
        self.profit_target_pips = profit_target_pips
        self.stop_loss_pips = stop_loss_pips
    
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
    
    def calculate_ema_stack(
        self, 
        ohlcv_data: List[OHLCV], 
        current_idx: int
    ) -> Tuple[Optional[float], Optional[float], Optional[float], str]:
        """Calculate EMA stack and determine trend."""
        if current_idx < self.ema_slow:
            return None, None, None, "neutral"
        
        ema_fast = self.calculate_ema(
            ohlcv_data[:current_idx+1], 
            self.ema_fast
        )
        ema_medium = self.calculate_ema(
            ohlcv_data[:current_idx+1], 
            self.ema_medium
        )
        ema_slow = self.calculate_ema(
            ohlcv_data[:current_idx+1], 
            self.ema_slow
        )
        
        if ema_fast is None or ema_medium is None or ema_slow is None:
            return None, None, None, "neutral"
        
        if ema_fast > ema_medium > ema_slow:
            return ema_fast, ema_medium, ema_slow, "bullish"
        elif ema_fast < ema_medium < ema_slow:
            return ema_fast, ema_medium, ema_slow, "bearish"
        
        return ema_fast, ema_medium, ema_slow, "neutral"
    
    def calculate_momentum(
        self, 
        ohlcv_data: List[OHLCV], 
        current_idx: int,
        period: int = 5
    ) -> float:
        """Calculate momentum (rate of change)."""
        if current_idx < period:
            return 0.0
        
        current_price = ohlcv_data[current_idx].close
        past_price = ohlcv_data[current_idx - period].close
        
        if past_price == 0:
            return 0.0
        
        return ((current_price - past_price) / past_price) * 100
    
    def calculate_volatility(
        self, 
        ohlcv_data: List[OHLCV], 
        current_idx: int,
        period: int = 20
    ) -> float:
        """Calculate price volatility (standard deviation)."""
        if current_idx < period:
            return 0.0
        
        closes = [c.close for c in ohlcv_data[current_idx-period:current_idx+1]]
        mean = sum(closes) / len(closes)
        variance = sum((x - mean) ** 2 for x in closes) / len(closes)
        
        return variance ** 0.5
    
    def entry_conditions(
        self, 
        ohlcv_data: List[OHLCV], 
        current_idx: int
    ) -> Tuple[bool, Optional[Signal]]:
        """Check if scalping entry criteria are met."""
        if current_idx < self.ema_slow:
            return False, None
        
        current = ohlcv_data[current_idx]
        
        ema_fast, ema_medium, ema_slow, trend = self.calculate_ema_stack(
            ohlcv_data, 
            current_idx
        )
        
        if trend == "neutral":
            return False, None
        
        momentum = self.calculate_momentum(ohlcv_data, current_idx)
        
        pip_value = self.calculate_pip_value(self.symbol)
        profit_target = self.profit_target_pips * pip_value
        stop_loss = self.stop_loss_pips * pip_value
        
        if trend == "bullish" and momentum > 0:
            entry_price = current.close
            tp = entry_price + profit_target
            sl = entry_price - stop_loss
            
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
                    "type": "scalp_long",
                    "ema_fast": ema_fast,
                    "ema_medium": ema_medium,
                    "ema_slow": ema_slow,
                    "momentum": momentum,
                }
            )
        
        if trend == "bearish" and momentum < 0:
            entry_price = current.close
            tp = entry_price - profit_target
            sl = entry_price + stop_loss
            
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
                    "type": "scalp_short",
                    "ema_fast": ema_fast,
                    "ema_medium": ema_medium,
                    "ema_slow": ema_slow,
                    "momentum": momentum,
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
        
        ema_fast, ema_medium, ema_slow, trend = self.calculate_ema_stack(
            ohlcv_data, 
            current_idx
        )
        
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
            
            if trend != "bullish":
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.8,
                    metadata={"reason": "trend_change", "new_trend": trend}
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
            
            if trend != "bearish":
                return True, Signal(
                    timestamp=current.timestamp,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.8,
                    metadata={"reason": "trend_change", "new_trend": trend}
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
        return self.ema_slow + 10
    
    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        if not super().validate_config():
            return False
        
        if self.profit_target_pips <= 0:
            self.logger.error(f"Invalid profit_target_pips: {self.profit_target_pips}")
            return False
        
        if self.stop_loss_pips <= 0:
            self.logger.error(f"Invalid stop_loss_pips: {self.stop_loss_pips}")
            return False
        
        return True
