#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Volatility Expansion Strategy - Trading Strategy

Berbasis pada ekspansi volatilitas untuk entry point.
Breakout high/low setelah ATR threshold terlewati.

Inspired from: Volatility Breakout strategies
Base-kan pada: Asia 7-Candle framework
"""

import sys
import os
import argparse
from datetime import datetime, timedelta
from typing import List, Optional
from dataclasses import dataclass

# Add parent paths for imports
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(0, SKILL_ROOT)
sys.path.insert(0, WORKSPACE_ROOT)


@dataclass
class VolConfig:
    """Configuration untuk Volatility Expansion Strategy"""
    symbol: str = "GC=X"
    lots: float = 0.10
    atr_period: int = 14  # ATR period untuk volatilitas
    atr_multiplier: float = 2.0  # Multiplier ATR untuk threshold
    stoploss_atr: float = 1.5  # SL = 1.5 * ATR
    tp_atr: float = 2.0  # TP = 2.0 * ATR
    trail_atr: bool = True  # Trailing dengan ATR
    min_atr: float = 5.0  # Minimum ATR untuk trade
    max_spread: float = 0.0  # Maximum spread (point)
    session_start: str = "07:00"  # WIB (Asia session start)
    session_end: str = "15:00"  # WIB (Asia session end)
    magic: int = 54321
    risk_per_trade: float = 1.0  # 1% per trade
    max_trades: int = 3  # Max trades per session


class VolatilityExpansion:
    """
    Volatility Expansion Strategy
    
    Logika:
    1. Hitung ATR (Average True Range) dari candle
    2. Breakout entry kalau harga high/low melewati threshold
    3. Trailing stop berdasarkan ATR
    4. Take profit berdasarkan ekspansi (2x ATR)
    """
    
    def __init__(self, config: VolConfig):
        self.config = config
        self.running = True
        self.trade_count = 0
        self.positions = []
    
    def parse_time(self, time_str: str) -> int:
        """Parse HH:MM format ke menit"""
        parts = time_str.split(':')
        return int(parts[0]) * 60 + int(parts[1])
    
    def in_session(self, current_time: datetime) -> bool:
        """Cek apakah time dalam trading session"""
        start = self.parse_time(self.config.session_start)
        end = self.parse_time(self.config.session_end)
        current = current_time.hour * 60 + current_time.minute
        
        if end < start:  # Cross midnight (15:00 ke 07:00 next day)
            return current >= start or current <= end
        else:
            return start <= current <= end
    
    def print_signal(self, signal_type: str, price: float, atr: float, details: str = ""):
        """Print trading signal"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔔 {signal_type.upper()} Signal")
        print(f"   Price: {price:.5f}")
        print(f"   ATR({self.config.atr_period}): {atr:.5f} pts")
        print(f"   Details: {details}")
        print(f"   Session: {self.config.session_start}-{self.config.session_end} WIB")
    
    def print_trade(self, action: str, details: dict):
        """Print trade information"""
        direction = details.get('direction', 'BUY')
        entry = details.get('entry', 0)
        sl = details.get('sl', 0)
        tp = details.get('tp', 0)
        lots = details.get('lots', 0)
        atr = details.get('atr', 0)
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📊 {action} Trade")
        print(f"   {direction} {self.config.symbol} @ {entry:.5f}")
        print(f"   Lots: {lots}")
        if atr > 0:
            print(f"   SL: {sl:.5f} ({abs((sl-entry)/atr):.1f}x ATR)")
            print(f"   TP: {tp:.5f} ({abs((tp-entry)/atr):.1f}x ATR)")
        else:
            print(f"   SL: {sl:.5f}")
            print(f"   TP: {tp:.5f}")
    
    def backtest(self, ohlcv_data: List) -> dict:
        """
        Run backtest pada data OHLCV
        
        Returns:
        {
            'trades': list,
            'total_trades': int,
            'win_rate': float,
            'net_profit': float,
            'profit_factor': float,
            'max_drawdown': float
        }
        """
        trades = []
        balance = 10000.0
        current_positions = []
        max_balance = balance
        max_drawdown = 0.0
        
        for i, candle in enumerate(ohlcv_data):
            if i < self.config.atr_period:
                continue  # Butuh cukup data buat ATR
            
            # Hitung ATR
            atr_candles = ohlcv_data[max(0, i - self.config.atr_period):i]
            atr = self.calculate_atr(atr_candles)
            
            current_price = candle.close
            high = candle.high
            low = candle.low
            
            # Cek breakout
            upper_threshold = current_price + (atr * self.config.atr_multiplier)
            lower_threshold = current_price - (atr * self.config.atr_multiplier)
            
            # Cek entry signal
            signal_type = None
            entry_price = None
            sl = None
            tp = None
            
            if high > upper_threshold:
                signal_type = "BOUGHT (High Breakout)"
                entry_price = upper_threshold
                sl = entry_price - (atr * self.config.stoploss_atr)
                tp = entry_price + (atr * self.config.tp_atr)
                
            elif low < lower_threshold:
                signal_type = "BOUGHT (Low Breakout)"
                entry_price = lower_threshold
                sl = entry_price - (atr * self.config.stoploss_atr)
                tp = entry_price + (atr * self.config.tp_atr)
            
            # Eksekusi trade
            if signal_type and atr >= self.config.min_atr:
                # Cek apakah sudah ada posisi yang sama
                has_position = False
                for pos in current_positions:
                    if pos['direction'] == 'BUY' and signal_type.startswith('BOUGHT'):
                        has_position = True
                        break
                
                if not has_position and len(current_positions) < self.config.max_trades:
                    # Tentukan direction berdasarkan signal
                    direction = 'BUY' if signal_type.startswith('BOUGHT') else 'SELL'
                    
                    trade = {
                        'direction': direction,
                        'entry': entry_price,
                        'sl': sl,
                        'tp': tp,
                        'lots': self.config.lots,
                        'atr': atr,
                        'time': candle.timestamp,
                        'signal_type': signal_type
                    }
                    
                    trades.append(trade)
                    current_positions.append(trade)
                    
                    # Update balance
                    if direction == 'BUY':
                        balance += (tp - entry_price) * 100 * self.config.lots
                    else:
                        balance += (entry_price - tp) * 100 * self.config.lots
                    
                    if balance > max_balance:
                        max_balance = balance
                    
                    drawdown = (max_balance - balance) / max_balance * 100
                    if drawdown > max_drawdown:
                        max_drawdown = drawdown
                    
                    self.print_trade("Entry", trade)
            
            # Cek exit untuk posisi yang ada
            for pos in current_positions[:]:
                candle_price = candle.close
                
                # Check SL
                if direction == 'BUY':
                    if candle_price <= pos['sl']:
                        profit = (pos['sl'] - pos['entry']) * 100 * self.config.lots
                        trades[-1]['exit_price'] = pos['sl']
                        trades[-1]['exit_reason'] = 'SL'
                        trades[-1]['profit'] = profit
                        balance += profit
                        current_positions.remove(pos)
                        self.print_trade("SL Hit", {
                            'exit_price': pos['sl'],
                            'profit': profit
                        })
                    
                    # Check TP
                    elif candle_price >= pos['tp']:
                        profit = (pos['tp'] - pos['entry']) * 100 * self.config.lots
                        trades[-1]['exit_price'] = pos['tp']
                        trades[-1]['exit_reason'] = 'TP'
                        trades[-1]['profit'] = profit
                        balance += profit
                        current_positions.remove(pos)
                        self.print_trade("TP Hit", {
                            'exit_price': pos['tp'],
                            'profit': profit
                        })
                
                else:  # SELL position
                    if candle_price >= pos['sl']:
                        profit = (pos['entry'] - pos['sl']) * 100 * self.config.lots
                        trades[-1]['exit_price'] = pos['sl']
                        trades[-1]['exit_reason'] = 'SL'
                        trades[-1]['profit'] = profit
                        balance += profit
                        current_positions.remove(pos)
                        self.print_trade("SL Hit", {
                            'exit_price': pos['sl'],
                            'profit': profit
                        })
                    
                    # Check TP
                    elif candle_price <= pos['tp']:
                        profit = (pos['entry'] - pos['tp']) * 100 * self.config.lots
                        trades[-1]['exit_price'] = pos['tp']
                        trades[-1]['exit_reason'] = 'TP'
                        trades[-1]['profit'] = profit
                        balance += profit
                        current_positions.remove(pos)
                        self.print_trade("TP Hit", {
                            'exit_price': pos['tp'],
                            'profit': profit
                        })
        
        # Hitung statistik
        total_trades = len(trades)
        if total_trades == 0:
            return {
                'trades': [],
                'total_trades': 0,
                'win_rate': 0.0,
                'net_profit': 0.0,
                'profit_factor': 0.0,
                'max_drawdown': 0.0
            }
        
        wins = sum(1 for t in trades if t.get('profit', 0) > 0)
        net_profit = sum(t.get('profit', 0) for t in trades)
        profit_factor = sum(t.get('profit', 0) for t in trades if t.get('profit', 0) > 0) / abs(sum(t.get('profit', 0) for t in trades if t.get('profit', 0) < 0))
        
        win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0.0
        
        return {
            'trades': trades,
            'total_trades': total_trades,
            'win_rate': win_rate,
            'net_profit': net_profit,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown
        }
    
    def calculate_atr(self, candles: List) -> float:
        """
        Hitung Average True Range (ATR)
        
        Menggunakan metode standar:
        - Hitung true range untuk setiap candle
        - Rata-ratakan untuk atr_period
        """
        if len(candles) < 2:
            return 0.0
        
        true_ranges = []
        for i in range(1, len(candles)):
            tr = abs(candles[i].high - candles[i].low)
            true_ranges.append(tr)
        
        atr = sum(true_ranges) / len(true_ranges)
        return atr
    
    def print_results(self, results: dict):
        """Print backtest results"""
        print(f"\n{'='*60}")
        print(f" VOLATILITY EXPANSION STRATEGY - BACKTEST RESULTS")
        print(f" {'='*60}")
        print(f" Symbol: {self.config.symbol}")
        print(f" Period: Asia Session ({self.config.session_start}-{self.config.session_end} WIB)")
        print(f" Initial Balance: $10,000")
        print(f" -" * 60)
        print(f" Total Trades: {results['total_trades']}")
        print(f" Win Rate: {results['win_rate']:.1f}%")
        print(f" Net Profit: ${results['net_profit']:.2f}")
        print(f" Profit Factor: {results['profit_factor']:.2f}")
        print(f" Max Drawdown: {results['max_drawdown']:.1f}%")
        print(f" -" * 60)
        
        if results['profit_factor'] > 1.0:
            print(f" ✅ STRATEGY PROFITABLE! PF > 1")
        elif results['profit_factor'] > 0.5:
            print(f" ⚠️  Strategy moderate (PF > 0.5)")
        else:
            print(f" ❌ STRATEGY UNPROFITABLE (PF < 0.5)")
        
        print(f"{'='*60}\n")


def run_backtest(symbol: str = "GC=X", start_date: str = "2025-01-01", end_date: str = "2025-12-31"):
    """Run backtest dengan yfinance"""
    print(f"\n{'#'*60}")
    print(f"# Volatility Expansion Strategy - Backtest")
    print(f"# Symbol: {symbol} | Period: {start_date} to {end_date}")
    print(f"{'#'*60}\n")
    
    # Import brokers
    try:
        from brokers.simulated import SimulatedBroker
    except ImportError as e:
        print(f"❌ Error importing broker: {e}")
        return
    
    # Create broker dan fetch data
    broker = SimulatedBroker(symbol=symbol)
    broker.connect()
    
    print(f"Fetching OHLCV data for {symbol}...")
    ohlcv_data = broker.get_ohlcv(
        symbol=symbol,
        timeframe="H1",
        start=datetime.strptime(start_date, "%Y-%m-%d"),
        end=datetime.strptime(end_date, "%Y-%m-%d")
    )
    
    if not ohlcv_data:
        print(f"❌ No data found for {symbol}")
        return
    
    print(f"✅ Fetched {len(ohlcv_data)} candles")
    
    # Create strategy dan run backtest
    config = VolConfig(symbol=symbol)
    strategy = VolatilityExpansion(config=config)
    
    # Run backtest
    results = strategy.backtest(ohlcv_data)
    
    # Print results
    strategy.print_results(results)
    
    broker.disconnect()


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Volatility Expansion Strategy - Breakout trading berdasarkan volatilitas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Run backtest dengan defaults
  %(prog)s --atr-period 20 --atr-multiplier 2.5    # Custom ATR settings
  %(prog)s --lots 0.05 --risk 0.5             # Smaller position size
        """
    )
    
    parser.add_argument("--symbol", type=str, default="GC=X",
                       help="Trading symbol (default: GC=X untuk XAUUSD)")
    parser.add_argument("--lots", type=float, default=0.10,
                       help="Lot size (default: 0.10)")
    parser.add_argument("--atr-period", type=int, default=14,
                       help="ATR period (default: 14)")
    parser.add_argument("--atr-multiplier", type=float, default=2.0,
                       help="ATR multiplier untuk threshold (default: 2.0)")
    parser.add_argument("--stoploss-atr", type=float, default=1.5,
                       help="SL = multiplier ATR (default: 1.5)")
    parser.add_argument("--tp-atr", type=float, default=2.0,
                       help="TP = multiplier ATR (default: 2.0)")
    parser.add_argument("--trail-atr", action="store_true",
                       help="Enable trailing stop berdasarkan ATR")
    parser.add_argument("--min-atr", type=float, default=5.0,
                       help="Minimum ATR untuk trade (default: 5.0)")
    parser.add_argument("--max-spread", type=float, default=0.0,
                       help="Maximum spread dalam point (default: 0)")
    parser.add_argument("--session-start", type=str, default="07:00",
                       help="Session start HH:MM WIB (default: 07:00)")
    parser.add_argument("--session-end", type=str, default="15:00",
                       help="Session end HH:MM WIB (default: 15:00)")
    parser.add_argument("--magic", type=int, default=54321,
                       help="Magic number (default: 54321)")
    parser.add_argument("--risk", type=float, default=1.0,
                       help="Risk per trade %% (default: 1.0)")
    parser.add_argument("--max-trades", type=int, default=3,
                       help="Max trades per session (default: 3)")
    
    parser.add_argument("--start-date", type=str, default="2025-01-01",
                       help="Start date YYYY-MM-DD (default: 2025-01-01)")
    parser.add_argument("--end-date", type=str, default="2025-12-31",
                       help="End date YYYY-MM-DD (default: 2025-12-31)")
    
    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_args()
    
    # Create config
    config = VolConfig(
        symbol=args.symbol,
        lots=args.lots,
        atr_period=args.atr_period,
        atr_multiplier=args.atr_multiplier,
        stoploss_atr=args.stoploss_atr,
        tp_atr=args.tp_atr,
        trail_atr=args.trail_atr,
        min_atr=args.min_atr,
        max_spread=args.max_spread,
        session_start=args.session_start,
        session_end=args.session_end,
        magic=args.magic,
        risk_per_trade=args.risk,
        max_trades=args.max_trades
    )
    
    # Run backtest
    run_backtest(
        symbol=config.symbol,
        start_date=args.start_date,
        end_date=args.end_date
    )


if __name__ == "__main__":
    main()
