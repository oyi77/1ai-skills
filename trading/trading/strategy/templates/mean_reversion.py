"""
Mean Reversion Strategy Template

Strategy based on price returning to mean (Bollinger Bands + RSI).
Entry when price touches extreme band and RSI indicates reversal.
Exit when price returns to middle band or RSI normalizes.
"""

from datetime import datetime
from typing import List, Optional, Tuple

from trading.brokers.base import OHLCV
from trading.strategy.templates.base import StrategyTemplate, Signal, SignalType


class MeanReversionTemplate(StrategyTemplate):
    """
    Mean reversion strategy template using RSI and Bollinger Bands.
    
    Entry: Price at extreme Bollinger Band + RSI overbought/oversold
    Exit: Price returns to middle band or RSI returns to neutral
    """
    
    def __init__(
        self,
        symbol: str = "XAUUSD",
        timeframe: str = "H1",
        bb_period: int = 20,
        bb_std: float = 2.0,
        rsi_period: int = 14,
        rsi_oversold: float = 30.0,
        rsi_overbought: float = 70.0,
        risk_per_trade: float = 0.02,
        config: Optional[dict] = None,
    ):
        super().__init__(
            name="MeanReversionTemplate",
            symbol=symbol,
            timeframe=timeframe,
            risk_per_trade=risk_per_trade,
            config=config or {},
        )
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
    
    def calculate_sma(self, ohlcv_data: List[OHLCV], period: int) -> Optional[float]:
        """Calculate Simple Moving Average."""
        if len(ohlcv_data) < period:
            return None
        
        closes = [c.close for c in ohlcv_data[-period:]]
        return sum(closes) / period
    
    def calculate_std(self, ohlcv_data: List[OHLCV], period: int) -> Optional[float]:
        """Calculate standard deviation."""
        if len(ohlcv_data) < period:
            return None
        
        closes = [c.close for c in ohlcv_data[-period:]]
        mean = sum(closes) / period
        variance = sum((x - mean) ** 2 for x in closes) / period
        return variance ** 0.5
    
    def calculate_bollinger_bands(
        self, 
        ohlcv_data: List[OHLCV]
    ) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """
        Calculate Bollinger Bands.
        
        Returns:
            (upper_band, middle_band, lower_band)
        """
        if len(ohlcv_data) < self.bb_period:
            return None, None, None
        
        middle = self.calculate_sma(ohlcv_data, self.bb_period)
        std = self.calculate_std(ohlcv_data, self.bb_period)
        
        if middle is None or std is None:
            return None, None, None
        
        upper = middle + (std * self.bb_std)
        lower = middle - (std * self.bb_std)
        
        return upper, middle, lower
    
    def calculate_rsi(
        self, 
        ohlcv_data: List[OHLCV], 
        period: int = None
    ) -> Optional[float]:
        """
        Calculate Relative Strength Index.
        
        Returns:
            RSI value (0-100)
        """
        period = period or self.rsi_period
        
        if len(ohlcv_data) < period + 1:
            return None
        
        # Calculate price changes
        gains = []
        losses = []
        
        for i in range(1, len(ohlcv_data)):
            change = ohlcv_data[i].close - ohlcv_data[i-1].close
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        # Use last 'period' values
        recent_gains = gains[-period:]
        recent_losses = losses[-period:]
        
        avg_gain = sum(recent_gains) / period
        avg_loss = sum(recent_losses) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
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
        Check if mean reversion entry criteria are met.
        
        Entry signals:
        - Bullish: Price at lower BB + RSI oversold
        - Bearish: Price at upper BB + RSI overbought
        """
        if current_idx < max(self.bb_period, self.rsi_period) + 1:
            return False, None
        
        current = ohlcv_data[current_idx]
        
        # Calculate Bollinger Bands
        upper, middle, lower = self.calculate_bollinger_bands(
            ohlcv_data[:current_idx+1]
        )
        
        if upper is None or middle is None or lower is None:
            return False, None
        
        # Calculate RSI
        rsi = self.calculate_rsi(ohlcv_data[:current_idx+1])
        
        if rsi is None:
            return False, None
        
        # Calculate ATR for stops
        atr = self.calculate_atr(ohlcv_data[:current_idx+1])
        
        # Bullish: Price at lower band + RSI oversold
        if current.close <= lower and rsi <= self.rsi_oversold:
            entry_price = current.close
            stop_loss = current.low - (atr * 1.5)
            # Target: middle band or slight profit
            take_profit = middle
            
            return True, Signal(
                timestamp=current.time,
                symbol=self.symbol,
                timeframe=self.timeframe,
                signal_type=SignalType.BUY,
                price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                confidence=self._calculate_rsi_confidence(rsi, is_oversold=True),
                metadata={
                    "type": "bullish_reversion",
                    "lower_band": lower,
                    "middle_band": middle,
                    "upper_band": upper,
                    "rsi": rsi,
                    "atr": atr,
                }
            )
        
        # Bearish: Price at upper band + RSI overbought
        if current.close >= upper and rsi >= self.rsi_overbought:
            entry_price = current.close
            stop_loss = current.high + (atr * 1.5)
            take_profit = middle
            
            return True, Signal(
                timestamp=current.time,
                symbol=self.symbol,
                timeframe=self.timeframe,
                signal_type=SignalType.SELL,
                price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                confidence=self._calculate_rsi_confidence(rsi, is_oversold=False),
                metadata={
                    "type": "bearish_reversion",
                    "lower_band": lower,
                    "middle_band": middle,
                    "upper_band": upper,
                    "rsi": rsi,
                    "atr": atr,
                }
            )
        
        return False, None
    
    def _calculate_rsi_confidence(self, rsi: float, is_oversold: bool = True) -> float:
        """
        Calculate confidence based on RSI extremity.
        
        More extreme RSI = higher confidence.
        """
        if is_oversold:
            # Lower RSI = higher confidence (down to 10)
            if rsi <= 10:
                return 1.0
            return 1.0 - ((rsi - 10) / 20)
        else:
            # Higher RSI = higher confidence (up to 90)
            if rsi >= 90:
                return 1.0
            return 1.0 - ((90 - rsi) / 20)
    
    def exit_conditions(
        self, 
        ohlcv_data: List[OHLCV], 
        current_idx: int,
        position
    ) -> Tuple[bool, Optional[Signal]]:
        """
        Check if exit criteria are met.
        
        Exit signals:
        - Price reaches middle band (mean reversion complete)
        - RSI returns to neutral zone
        - Stop loss hit
        """
        if current_idx < 1:
            return False, None
        
        current = ohlcv_data[current_idx]
        
        # Get current Bollinger Bands
        upper, middle, lower = self.calculate_bollinger_bands(
            ohlcv_data[:current_idx+1]
        )
        
        if upper is None or middle is None:
            return False, None
        
        # Get current RSI
        rsi = self.calculate_rsi(ohlcv_data[:current_idx+1])
        
        if position.side == "LONG":
            # Check stop loss
            if current.low <= position.stop_loss:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=position.stop_loss,
                    confidence=1.0,
                    metadata={"reason": "stop_loss"}
                )
            
            # Exit at middle band (mean reversion complete)
            if current.close >= middle:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.9,
                    metadata={"reason": "mean_reversion_complete", "middle_band": middle}
                )
            
            # Exit if RSI returns to neutral
            if rsi is not None and self.rsi_oversold < rsi < (100 - self.rsi_overbought):
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_LONG,
                    price=current.close,
                    confidence=0.7,
                    metadata={"reason": "rsi_neutral"}
                )
        
        elif position.side == "SHORT":
            # Check stop loss
            if current.high >= position.stop_loss:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=position.stop_loss,
                    confidence=1.0,
                    metadata={"reason": "stop_loss"}
                )
            
            # Exit at middle band
            if current.close <= middle:
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.9,
                    metadata={"reason": "mean_reversion_complete", "middle_band": middle}
                )
            
            # Exit if RSI returns to neutral
            if rsi is not None and self.rsi_oversold < rsi < (100 - self.rsi_overbought):
                return True, Signal(
                    timestamp=current.time,
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    signal_type=SignalType.CLOSE_SHORT,
                    price=current.close,
                    confidence=0.7,
                    metadata={"reason": "rsi_neutral"}
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
        return max(self.bb_period, self.rsi_period) + 14
    
    def validate_config(self) -> bool:
        """Validate strategy configuration."""
        if not super().validate_config():
            return False
        
        if self.rsi_oversold >= self.rsi_overbought:
            self.logger.error(
                f"rsi_oversold ({self.rsi_oversold}) must be less than "
                f"rsi_overbought ({self.rsi_overbought})"
            )
            return False
        
        if self.bb_period < 5:
            self.logger.error(f"bb_period too small: {self.bb_period}")
            return False
        
        return True
