#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maybe HFT Hedging EA - OpenClaw Skill

Expert Advisor cross-platform untuk trading hedging dengan sistem
trailing stop dan pending order otomatis. Compatible dengan mt5linux Docker.

Author: Mas Imam (wa.me/6289679369219)
Converted: OpenClaw AI
License: MIT
"""

# @skill_name maybe-hft
# @skill_description Hedging EA dengan trailing stop dan pending order otomatis. Cross-platform (Windows/Linux/Mac).
# @skill_param symbol:str:GC=X:Pair yang ditrading
# @skill_param lots:float:0.10:Ukuran lot per transaksi
# @skill_param stoploss:int:1500:StopLoss dalam point
# @skill_param trailing:int:500:Jarak trailing dalam point
# @skill_param trail_start:int:1000:Profit minimal sebelum trailing aktif
# @skill_param x_distance:int:300:Jarak pending dari SL
# @skill_param start_direction:int:0:0=BUY dulu, 1=SELL dulu
# @skill_param broker:str:auto:Broker: mt5, simulated, auto
# @skill_param mode:str:paper:Mode: paper, live
# @skill_param once:bool:false:Jalan sekali aja, tidak loop

import sys
import os
import time
import signal
import argparse
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum

# Add parent paths for imports
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(0, SKILL_ROOT)
sys.path.insert(0, WORKSPACE_ROOT)
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, 'brokers'))


class OrderType(Enum):
    """Order type enum matching MQL5"""
    BUY = 0
    SELL = 1
    BUY_STOP = 2
    SELL_STOP = 3


class PositionType(Enum):
    """Position type enum matching MQL5"""
    BUY = 0
    SELL = 1


class OrderTime(Enum):
    """Order time enum matching MQL5"""
    TIME_GTC = 0


@dataclass
class EAConfig:
    """EA Configuration dengan defaults dari MQL5"""
    symbol: str = "GC=X"
    lots: float = 0.10
    stoploss: int = 1500  # dalam point
    trailing: int = 500  # jarak trailing dalam point
    trail_start: int = 1000  # profit minimal dalam point sebelum trailing aktif
    x_distance: int = 300  # jarak pending dari SL
    slippage: int = 30  # dalam point
    magic: int = 12345
    start_direction: int = 0  # 0=BUY dulu, 1=SELL dulu
    broker: str = "auto"  # mt5, simulated, auto
    mode: str = "paper"  # paper, live
    once: bool = False  # jalan sekali aja (tidak loop)
    interval: float = 1.0  # check interval dalam detik


def _get_attr(obj: Any, key: str, default: Any = None) -> Any:
    """Safely get attribute from dict or dataclass."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


class MaybeHFT:
    """
    Maybe HFT Hedging EA Implementation
    
    Fitur utama:
    - Buka order utama (BUY/SELL) berdasarkan start_direction
    - Buat pending hedge order saat SL aktif
    - Trailing stop dengan threshold
    - Modify pending orders untuk track perubahan SL
    """
    
    def __init__(self, config: EAConfig):
        self.config = config
        self.broker = None
        self.running = True
        self.trade_count = 0
        
        # Setup signal handlers untuk graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Shutting down EA...")
        self.running = False
    
    def _convert_symbol(self, symbol: str) -> str:
        """Convert trading symbol to broker symbol."""
        symbol_map = {
            "GC=X": "GC=F",  # Yahoo Finance gold
            "XAUUSD": "GC=F",
            "GOLD": "GC=F",
        }
        return symbol_map.get(symbol, symbol)
    
    def initialize_broker(self) -> bool:
        """Initialize broker connection dengan fallback"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Initializing broker: {self.config.broker}")
        
        if self.config.broker == "auto":
            # Coba mt5 dulu, fallback ke simulated
            try:
                from brokers.mt5.connector import MT5Connector
                self.broker = MT5Connector()
                if self.broker.connect():
                    print(f"✅ Connected to mt5linux ({self.broker.host}:{self.broker.port})")
                    return True
            except Exception as e:
                print(f"⚠️ MT5 connection failed: {e}")
            
            # Fallback ke simulated
            try:
                from brokers.simulated import SimulatedBroker
                broker_symbol = self._convert_symbol(self.config.symbol)
                self.broker = SimulatedBroker(symbol=broker_symbol)
                print(f"✅ Connected to simulated broker (yfinance)")
                return True
            except Exception as e:
                print(f"❌ Simulated broker failed: {e}")
                return False
        
        elif self.config.broker == "mt5":
            try:
                from brokers.mt5.connector import MT5Connector
                self.broker = MT5Connector()
                if self.broker.connect():
                    print(f"✅ Connected to mt5linux ({self.broker.host}:{self.broker.port})")
                    return True
                else:
                    print("❌ Failed to connect to mt5linux")
                    return False
            except Exception as e:
                print(f"❌ MT5 error: {e}")
                return False
        
        elif self.config.broker == "simulated":
            try:
                from brokers.simulated import SimulatedBroker
                broker_symbol = self._convert_symbol(self.config.symbol)
                self.broker = SimulatedBroker(symbol=broker_symbol)
                print(f"✅ Connected to simulated broker (yfinance)")
                return True
            except Exception as e:
                print(f"❌ Simulated broker error: {e}")
                return False
        else:
            print(f"❌ Unknown broker: {self.config.broker}")
            return False
    
    def get_point(self) -> float:
        """Get symbol point size"""
        return self.broker.get_point()
    
    def get_ask(self) -> float:
        """Get current ask price"""
        return self.broker.get_ask()
    
    def get_bid(self) -> float:
        """Get current bid price"""
        return self.broker.get_bid()
    
    def count_main_orders(self) -> int:
        """Count active positions dengan magic number ini"""
        count = 0
        for pos in self.broker.positions:
            pos_symbol = _get_attr(pos, 'symbol')
            pos_magic = _get_attr(pos, 'magic')
            if pos_symbol == self.config.symbol and pos_magic == self.config.magic:
                count += 1
        return count
    
    def count_pending_orders(self) -> int:
        """Count pending STOP orders dengan magic number ini"""
        count = 0
        for order in self.broker.orders:
            order_symbol = _get_attr(order, 'symbol')
            order_magic = _get_attr(order, 'magic')
            order_type = _get_attr(order, 'type')
            if (order_symbol == self.config.symbol and 
                order_magic == self.config.magic and
                order_type in [OrderType.BUY_STOP.value, OrderType.SELL_STOP.value]):
                count += 1
        return count
    
    def open_main_order(self, direction: int) -> bool:
        """Buka order utama (BUY atau SELL)"""
        point = self.get_point()
        ask = self.get_ask()
        bid = self.get_bid()
        
        try:
            if direction == OrderType.BUY.value:
                price = ask
                sl = price - self.config.stoploss * point
                self.trade_count += 1
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📈 Opening MAIN BUY: "
                      f"Lots={self.config.lots}, Price={price:.5f}, SL={sl:.5f}")
                success = self.broker.buy(
                    volume=self.config.lots,
                    symbol=self.config.symbol,
                    price=price,
                    sl=sl,
                    tp=0,
                    magic=self.config.magic,
                    comment="Main BUY"
                )
            else:
                price = bid
                sl = price + self.config.stoploss * point
                self.trade_count += 1
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📉 Opening MAIN SELL: "
                      f"Lots={self.config.lots}, Price={price:.5f}, SL={sl:.5f}")
                success = self.broker.sell(
                    volume=self.config.lots,
                    symbol=self.config.symbol,
                    price=price,
                    sl=sl,
                    tp=0,
                    magic=self.config.magic,
                    comment="Main SELL"
                )
            return success
        except Exception as e:
            print(f"❌ Error opening main order: {e}")
            return False
    
    def trail_orders(self) -> None:
        """Terapkan trailing stop jika profit melebihi threshold"""
        point = self.get_point()
        ask = self.get_ask()
        bid = self.get_bid()
        
        for pos in self.broker.positions:
            pos_symbol = _get_attr(pos, 'symbol')
            pos_magic = _get_attr(pos, 'magic')
            if pos_symbol != self.config.symbol or pos_magic != self.config.magic:
                continue
            
            pos_type = _get_attr(pos, 'type')
            open_price = _get_attr(pos, 'open_price')
            sl = _get_attr(pos, 'sl', 0)
            ticket = _get_attr(pos, 'ticket')
            
            if pos_type == PositionType.BUY.value:
                # Hitung profit dalam point
                profit_points = (bid - open_price) / point
                if profit_points > self.config.trail_start:
                    new_sl = bid - self.config.trailing * point
                    if new_sl > sl:
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔧 Modifying BUY SL: "
                              f"{sl:.5f} → {new_sl:.5f} (Profit: {profit_points:.1f} pts)")
                        self.broker.position_modify(ticket, sl=new_sl, tp=0)
                        
            elif pos_type == PositionType.SELL.value:
                # Hitung profit dalam point
                profit_points = (open_price - ask) / point
                if profit_points > self.config.trail_start:
                    new_sl = ask + self.config.trailing * point
                    if sl == 0 or new_sl < sl:
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔧 Modifying SELL SL: "
                              f"{sl:.5f} → {new_sl:.5f} (Profit: {profit_points:.1f} pts)")
                        self.broker.position_modify(ticket, sl=new_sl, tp=0)
    
    def handle_pending(self) -> None:
        """Buat atau modify pending hedge orders"""
        point = self.get_point()
        
        # Cari posisi utama
        main_type = None
        main_sl = 0
        
        for pos in self.broker.positions:
            pos_symbol = _get_attr(pos, 'symbol')
            pos_magic = _get_attr(pos, 'magic')
            if pos_symbol == self.config.symbol and pos_magic == self.config.magic:
                main_type = _get_attr(pos, 'type')
                main_sl = _get_attr(pos, 'sl', 0)
                break
                
        if main_type is None:
            return  # Tidak ada posisi utama
            
        if self.count_main_orders() >= 2:
            return  # Udah ada 2 posisi (main + hedge)
            
        # Cari pending order yang ada
        pending_ticket = None
        pending_type = None
        pending_price = None
        pending_sl = None
        
        for order in self.broker.orders:
            order_symbol = _get_attr(order, 'symbol')
            order_magic = _get_attr(order, 'magic')
            order_type = _get_attr(order, 'type')
            if (order_symbol == self.config.symbol and 
                order_magic == self.config.magic and
                order_type in [OrderType.BUY_STOP.value, OrderType.SELL_STOP.value]):
                pending_ticket = _get_attr(order, 'ticket')
                pending_type = order_type
                pending_price = _get_attr(order, 'price_open')
                pending_sl = _get_attr(order, 'sl', 0)
                break
        
        # Hitung parameter pending baru
        new_price = 0
        new_sl = 0
        
        if main_type == PositionType.BUY.value and main_sl > 0:
            new_price = main_sl + self.config.x_distance * point
            new_sl = new_price + self.config.stoploss * point
            
            if pending_ticket is None:
                # Buat SELL STOP hedge baru
                self.trade_count += 1
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🛡️ Creating HEDGE SELL STOP: "
                      f"Lots={self.config.lots}, Price={new_price:.5f}, SL={new_sl:.5f}")
                self.broker.sell_stop(
                    volume=self.config.lots,
                    symbol=self.config.symbol,
                    price=new_price,
                    sl=new_sl,
                    tp=0,
                    magic=self.config.magic,
                    comment="Hedge SELL STOP"
                )
            elif pending_type == OrderType.SELL_STOP.value:
                # Modify pending yang ada
                price_diff = abs(pending_price - new_price)
                sl_diff = abs(pending_sl - new_sl)
                if price_diff > point * 2 or sl_diff > point * 2:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔧 Modifying HEDGE SELL STOP: "
                          f"Price={pending_price:.5f}→{new_price:.5f}, SL={pending_sl:.5f}→{new_sl:.5f}")
                    self.broker.order_modify(
                        ticket=pending_ticket,
                        price=new_price,
                        sl=new_sl,
                        tp=0
                    )
                    
        elif main_type == PositionType.SELL.value and main_sl > 0:
            new_price = main_sl - self.config.x_distance * point
            new_sl = new_price - self.config.stoploss * point
            
            if pending_ticket is None:
                # Buat BUY STOP hedge baru
                self.trade_count += 1
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🛡️ Creating HEDGE BUY STOP: "
                      f"Lots={self.config.lots}, Price={new_price:.5f}, SL={new_sl:.5f}")
                self.broker.buy_stop(
                    volume=self.config.lots,
                    symbol=self.config.symbol,
                    price=new_price,
                    sl=new_sl,
                    tp=0,
                    magic=self.config.magic,
                    comment="Hedge BUY STOP"
                )
            elif pending_type == OrderType.BUY_STOP.value:
                # Modify pending yang ada
                price_diff = abs(pending_price - new_price)
                sl_diff = abs(pending_sl - new_sl)
                if price_diff > point * 2 or sl_diff > point * 2:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔧 Modifying HEDGE BUY STOP: "
                          f"Price={pending_price:.5f}→{new_price:.5f}, SL={pending_sl:.5f}→{new_sl:.5f}")
                    self.broker.order_modify(
                        ticket=pending_ticket,
                        price=new_price,
                        sl=new_sl,
                        tp=0
                    )
    
    def print_status(self) -> None:
        """Print status EA saat ini"""
        positions = []
        for p in self.broker.positions:
            pos_symbol = _get_attr(p, 'symbol')
            pos_magic = _get_attr(p, 'magic')
            if pos_symbol == self.config.symbol and pos_magic == self.config.magic:
                positions.append(p)
        
        orders = []
        for o in self.broker.orders:
            order_symbol = _get_attr(o, 'symbol')
            order_magic = _get_attr(o, 'magic')
            if order_symbol == self.config.symbol and order_magic == self.config.magic:
                orders.append(o)
        
        print(f"\n{'='*60}")
        print(f" MAYBE HFT EA STATUS")
        print(f" {'='*60}")
        print(f" Symbol: {self.config.symbol}")
        print(f" Broker: {self.config.broker} | Mode: {self.config.mode}")
        print(f" Ask: {self.get_ask():.5f} | Bid: {self.get_bid():.5f}")
        print(f" Point: {self.get_point()}")
        print(f" -" * 30)
        print(f" Main Orders: {len(positions)}")
        print(f" Pending Orders: {len(orders)}")
        print(f" -" * 30)
        
        for pos in positions:
            pos_type = _get_attr(pos, 'type')
            pos_type_str = "BUY" if pos_type == 0 else "SELL"
            open_price = _get_attr(pos, 'open_price')
            sl = _get_attr(pos, 'sl', 0)
            tp = _get_attr(pos, 'tp', 0)
            profit = _get_attr(pos, 'profit', 0)
            ticket = _get_attr(pos, 'ticket')
            print(f"  📊 {pos_type_str} #{ticket}: "
                  f"Open={open_price:.5f}, SL={sl:.5f}, TP={tp:.5f}, Profit={profit:.2f}")
            
        for order in orders:
            order_type = _get_attr(order, 'type')
            order_type_str = "BUY_STOP" if order_type == 2 else "SELL_STOP"
            price = _get_attr(order, 'price_open')
            sl = _get_attr(order, 'sl', 0)
            ticket = _get_attr(order, 'ticket')
            print(f"  ⏳ {order_type_str} #{ticket}: "
                  f"Price={price:.5f}, SL={sl:.5f}")
        
        print(f"{'='*60}\n")
    
    def run(self) -> None:
        """Main EA loop"""
        print(f"\n{'#'*60}")
        print(f"# MAYBE HFT HEDGING EA")
        print(f"# Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*60}")
        
        # Initialize broker
        if not self.initialize_broker():
            print("❌ Failed to initialize broker. Exiting.")
            return
        
        # Subscribe to symbol
        broker_symbol = self._convert_symbol(self.config.symbol)
        self.broker.subscribe(broker_symbol)
        
        print(f"\n📋 EA Configuration:")
        print(f"   Symbol: {self.config.symbol}")
        print(f"   Lots: {self.config.lots}")
        print(f"   StopLoss: {self.config.stoploss} pts")
        print(f"   Trailing: {self.config.trailing} pts")
        print(f"   TrailStart: {self.config.trail_start} pts")
        print(f"   X-Distance: {self.config.x_distance} pts")
        print(f"   StartDirection: {'BUY' if self.config.start_direction == 0 else 'SELL'}")
        print(f"   Magic: {self.config.magic}")
        print(f"   Mode: {self.config.mode}")
        print()
        
        loop_count = 0
        
        while self.running:
            try:
                loop_count += 1
                
                # Refresh data
                self.broker.refresh()
                
                # Execute EA logic
                self.trail_orders()
                self.handle_pending()
                
                # Open main order if none exists
                if self.count_main_orders() == 0 and self.count_pending_orders() == 0:
                    self.open_main_order(self.config.start_direction)
                
                # Print status every 10 loops
                if loop_count % 10 == 0:
                    self.print_status()
                    
                # Sleep between checks
                time.sleep(self.config.interval)
                
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(5)
                
        # Cleanup
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Cleaning up...")
        if self.broker:
            self.broker.disconnect()
        print(f"✅ EA stopped successfully.")


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Maybe HFT Hedging EA - Cross-platform Expert Advisor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Run dengan defaults
  %(prog)s --lots 0.05 --stoploss 1000       # Custom lot dan SL
  %(prog)s --broker mt5 --mode paper          # Pakai mt5linux, paper mode
  %(prog)s --once                             # Run sekali dan exit
  %(prog)s --config config.yaml               # Load config dari file
        """
    )
    
    # Trading parameters
    parser.add_argument("--symbol", type=str, default="GC=X",
                       help="Trading symbol (default: GC=X untuk XAUUSD)")
    parser.add_argument("--lots", type=float, default=0.10,
                       help="Lot size (default: 0.10)")
    parser.add_argument("--stoploss", type=int, default=1500,
                       help="StopLoss dalam point (default: 1500)")
    parser.add_argument("--trailing", type=int, default=500,
                       help="Trailing distance dalam point (default: 500)")
    parser.add_argument("--trail-start", type=int, default=1000,
                       help="Min profit dalam point sebelum trailing (default: 1000)")
    parser.add_argument("--x-distance", type=int, default=300,
                       help="Pending order distance dari SL (default: 300)")
    parser.add_argument("--slippage", type=int, default=30,
                       help="Slippage dalam point (default: 30)")
    parser.add_argument("--magic", type=int, default=12345,
                       help="Magic number (default: 12345)")
    parser.add_argument("--start-direction", type=int, default=0, choices=[0, 1],
                       help="0=BUY dulu, 1=SELL dulu (default: 0)")
    
    # Broker/Mode parameters
    parser.add_argument("--broker", type=str, default="auto", 
                       choices=["auto", "mt5", "simulated"],
                       help="Broker yang dipakai (default: auto)")
    parser.add_argument("--mode", type=str, default="paper",
                       choices=["paper", "live"],
                       help="Trading mode (default: paper)")
    parser.add_argument("--interval", type=float, default=1.0,
                       help="Check interval dalam detik (default: 1.0)")
    parser.add_argument("--once", action="store_true",
                       help="Run sekali dan exit (tidak loop)")
    
    # Config file
    parser.add_argument("--config", type=str, default=None,
                       help="Path ke config.yaml file")
    
    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_args()
    
    # Load config dari file jika specified
    config_dict = {}
    if args.config:
        config_dict = load_config(args.config)
        print(f"📄 Loaded config dari {args.config}")
    
    # Merge command line args dengan defaults, lalu config
    config = EAConfig(
        symbol=getattr(args, 'symbol', None) or config_dict.get('symbol', 'GC=X'),
        lots=getattr(args, 'lots', None) or config_dict.get('lots', 0.10),
        stoploss=getattr(args, 'stoploss', None) or config_dict.get('stoploss', 1500),
        trailing=getattr(args, 'trailing', None) or config_dict.get('trailing', 500),
        trail_start=getattr(args, 'trail_start', None) or config_dict.get('trail_start', 1000),
        x_distance=getattr(args, 'x_distance', None) or config_dict.get('x_distance', 300),
        slippage=getattr(args, 'slippage', None) or config_dict.get('slippage', 30),
        magic=getattr(args, 'magic', None) or config_dict.get('magic', 12345),
        start_direction=getattr(args, 'start_direction', None) or config_dict.get('start_direction', 0),
        broker=getattr(args, 'broker', None) or config_dict.get('broker', 'auto'),
        mode=getattr(args, 'mode', None) or config_dict.get('mode', 'paper'),
        interval=getattr(args, 'interval', None) or config_dict.get('interval', 1.0),
        once=getattr(args, 'once', False)
    )
    
    # Print warning untuk live mode
    if config.mode == "live":
        print("\n⚠️⚠️⚠️ WARNING: LIVE TRADING MODE ⚠️⚠️⚠️")
        print("Ini akan trading dengan UANG SEJATI!")
        print("Pastikan Anda memahami resikonya.")
        print("Press Ctrl+C untuk membatalkan dalam 5 detik...")
        time.sleep(5)
    
    # Create dan run EA
    ea = MaybeHFT(config)
    
    if config.once:
        # Run once mode
        if ea.initialize_broker():
            broker_symbol = ea._convert_symbol(config.symbol)
            ea.broker.subscribe(broker_symbol)
            ea.broker.refresh()
            ea.trail_orders()
            ea.handle_pending()
            if ea.count_main_orders() == 0 and ea.count_pending_orders() == 0:
                ea.open_main_order(config.start_direction)
            ea.print_status()
            ea.broker.disconnect()
            print(f"✅ Single run completed.")
        else:
            print("❌ Gagal initialize broker untuk single run.")
    else:
        # Continuous mode
        ea.run()


if __name__ == "__main__":
    main()
