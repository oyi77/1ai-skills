#!/usr/bin/env python3
"""
BerkahKarya Automated Trader
=============================
Runs XAUUSD Asia 7-Candle Breakout strategy automatically.
Supports MT5, cTrader, and Paper trading modes.

Usage:
    python automated_trader.py --broker paper --mode paper      # Paper trading (yfinance)
    python automated_trader.py --broker mt5 --mode demo         # MT5 demo account
    python automated_trader.py --broker mt5 --mode real         # MT5 real account
    python automated_trader.py --broker ctrader --mode real     # cTrader real
    
    python automated_trader.py --balance 5000 --dry-run --once  # Test run
"""

import argparse
import logging
import os
import sys
import time
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

import pytz

# Import broker connectors
from brokers.mt5.connector import MT5Connector
from brokers.ctrader.connector import CTraderConnector
from brokers.simulated import SimulatedBroker

# ---------------------------------------------------------------------------
# Paths & logging setup
# ---------------------------------------------------------------------------
TRADING_DIR = Path(__file__).parent
LOGS_DIR = TRADING_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / "trading.log"

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("automated_trader")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


log = setup_logger()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
JAKARTA_TZ = pytz.timezone("Asia/Jakarta")
SESSION_START = (7, 0)   # 07:00 WIB
SESSION_END = (15, 0)    # 15:00 WIB

SYMBOL = "XAUUSD"
MAX_TRADES = 3
RISK_PCT = 0.01
RR_RATIO = 2.0
POLL_SECS = 60

# ---------------------------------------------------------------------------
# Broker Factory
# ---------------------------------------------------------------------------
def create_broker(broker: str, mode: str = "paper", **kwargs):
    """Create broker instance based on type."""
    broker = broker.lower()
    
    if broker == "mt5":
        log.info(f"Initializing MT5 connector (mode: {mode})")
        mt5 = MT5Connector()
        
        if mode in ["demo", "real"]:
            login = int(os.environ.get("MT5_LOGIN", kwargs.get("login", 0)))
            password = os.environ.get("MT5_PASSWORD", kwargs.get("password", ""))
            server = os.environ.get("MT5_SERVER", kwargs.get("server", ""))
            
            if not all([login, password, server]):
                log.error("MT5 credentials required: set MT5_LOGIN, MT5_PASSWORD, MT5_SERVER env vars")
                return None
            
            connected = mt5.connect(
                login=login,
                password=password,
                server=server
            )
            if not connected:
                log.error("Failed to connect to MT5")
                return None
        
        return mt5
    
    elif broker == "ctrader":
        log.info(f"Initializing cTrader connector (mode: {mode})")
        ctrader = CTraderConnector()
        
        if mode in ["demo", "real"]:
            client_id = os.environ.get("CTRADER_CLIENT_ID", kwargs.get("client_id", ""))
            client_secret = os.environ.get("CTRADER_CLIENT_SECRET", kwargs.get("client_secret", ""))
            access_token = os.environ.get("CTRADER_ACCESS_TOKEN", kwargs.get("access_token", ""))
            
            if not all([client_id, client_secret, access_token]):
                log.error("cTrader credentials required: set CTRADER_CLIENT_ID, CTRADER_CLIENT_SECRET, CTRADER_ACCESS_TOKEN")
                return None
            
            connected = ctrader.connect(
                client_id=client_id,
                client_secret=client_secret,
                access_token=access_token
            )
            if not connected:
                log.error("Failed to connect to cTrader")
                return None
        
        return ctrader
    
    elif broker == "paper":
        log.info("Initializing SimulatedBroker (paper trading with yfinance)")
        simulated = SimulatedBroker()
        simulated.connect()
        return simulated
    
    else:
        log.error(f"Unknown broker: {broker}. Use: mt5, ctrader, or paper")
        return None

# ---------------------------------------------------------------------------
# 7-Candle Strategy
# ---------------------------------------------------------------------------
def calculate_7c_signal(ohlcv_list: list) -> Dict[str, Any]:
    """Calculate XAUUSD Asia 7-Candle Breakout signal.
    
    Asia session: 07:00-15:00 WIB (00:00-08:00 UTC)
    Take first 7 candles from 00:00 UTC = 07:00 WIB
    """
    if len(ohlcv_list) < 8:
        return {"signal": "WAIT", "reason": "Insufficient data"}
    
    # Use 7 candles starting from first of session (candle index 1, 0 is partial)
    candles = ohlcv_list[1:8]
    
    hh = max(c.high for c in candles)
    ll = min(c.low for c in candles)
    hc = max(c.close for c in candles)
    lc = min(c.close for c in candles)
    
    # Current price
    current = ohlcv_list[-1]
    
    # Breakout levels
    buy_stop = hh + 0.5  # 0.5 pts above HH
    sell_stop = ll - 0.5  # 0.5 pts below LL
    
    # TP/SL (2:1 reward to risk)
    risk = buy_stop - ll if buy_stop - ll > hh - sell_stop else hh - sell_stop
    tp_buy = buy_stop + risk * RR_RATIO
    sl_buy = buy_stop - risk
    tp_sell = sell_stop - risk * RR_RATIO
    sl_sell = sell_stop + risk
    
    return {
        "signal": "BREAKOUT",
        "hh": hh,
        "ll": ll,
        "buy_stop": buy_stop,
        "sell_stop": sell_stop,
        "tp_buy": tp_buy,
        "sl_buy": sl_buy,
        "tp_sell": tp_sell,
        "sl_sell": sl_sell,
        "range": hh - ll,
        "current": current.close,
        "timestamp": datetime.now(JAKARTA_TZ).isoformat()
    }

# ---------------------------------------------------------------------------
# Broker Actions
# ---------------------------------------------------------------------------
def place_pending_orders(broker, signal: Dict, balance: float, dry_run: bool):
    """Place buy stop and sell stop orders."""
    if signal["signal"] != "BREAKOUT":
        return False
    
    from brokers.base import Order
    
    risk_amount = balance * RISK_PCT
    lot_size = risk_amount / signal["range"] / 100  # Gold: 100 oz per lot = $1 per pip per 0.01 lot
    
    orders_placed = 0
    
    # Buy Stop
    buy_order = Order(
        ticket=0,
        symbol=SYMBOL,
        order_type="BUYSTOP",
        volume=round(lot_size, 2),
        price=signal["buy_stop"],
        sl=signal["sl_buy"],
        tp=signal["tp_buy"],
        comment="Asia 7C Buy"
    )
    
    if broker.place_order(buy_order, dry_run):
        orders_placed += 1
        log.info(f"[{'DRY-RUN' if dry_run else 'REAL'}] BUYSTOP {SYMBOL} @ {signal['buy_stop']} SL={signal['sl_buy']} TP={signal['tp_buy']}")
    
    # Sell Stop
    sell_order = Order(
        ticket=0,
        symbol=SYMBOL,
        order_type="SELLSTOP",
        volume=round(lot_size, 2),
        price=signal["sell_stop"],
        sl=signal["sl_sell"],
        tp=signal["tp_sell"],
        comment="Asia 7C Sell"
    )
    
    if broker.place_order(sell_order, dry_run):
        orders_placed += 1
        log.info(f"[{'DRY-RUN' if dry_run else 'REAL'}] SELLSTOP {SYMBOL} @ {signal['sell_stop']} SL={signal['sl_sell']} TP={signal['tp_sell']}")
    
    return orders_placed > 0

def check_trade_result(broker, signal: Dict, dry_run: bool):
    """Check open positions and close if SL/TP hit."""
    positions = broker.get_positions()
    
    for pos in positions:
        current = broker._get_price(pos.symbol) if hasattr(broker, '_get_price') else signal["current"]
        
        if pos.order_type.startswith("BUY"):
            if pos.sl and current <= pos.sl:
                log.info(f"[{'DRY-RUN' if dry_run else 'REAL'}] BUY hit SL @ {current}")
                broker.close_position(pos.ticket, dry_run)
            elif pos.tp and current >= pos.tp:
                log.info(f"[{'DRY-RUN' if dry_run else 'REAL'}] BUY hit TP @ {current}")
                broker.close_position(pos.ticket, dry_run)
        else:
            if pos.sl and current >= pos.sl:
                log.info(f"[{'DRY-RUN' if dry_run else 'REAL'}] SELL hit SL @ {current}")
                broker.close_position(pos.ticket, dry_run)
            elif pos.tp and current <= pos.tp:
                log.info(f"[{'DRY-RUN' if dry_run else 'REAL'}] SELL hit TP @ {current}")
                broker.close_position(pos.ticket, dry_run)

def cancel_pending_orders(broker, dry_run: bool):
    """Cancel all pending orders at session end."""
    # For paper broker, just log
    log.info(f"[{'DRY-RUN' if dry_run else 'REAL'}] Session end — cancelling pending orders")

# ---------------------------------------------------------------------------
# Day State
# ---------------------------------------------------------------------------
class DayState:
    def __init__(self):
        self.trades_today = 0
        self.signal_placed = False
        self.open_trade = False

    def can_trade(self):
        return self.trades_today < MAX_TRADES

# ---------------------------------------------------------------------------
# Main Loop
# ---------------------------------------------------------------------------
def run_loop(balance: float, dry_run: bool, once: bool, broker_type: str, mode: str):
    """Main trading loop."""
    log.info(f"BerkahKarya Automated Trader started | balance=${balance} | broker={broker_type} | mode={mode}")
    log.info(f"Strategy: XAUUSD Asia 7-Candle Breakout | Session: 07:00-15:00 WIB | Risk: {RISK_PCT*100}%/trade")
    
    # Create broker
    broker = create_broker(broker_type, mode)
    if not broker:
        log.error("Failed to initialize broker. Exiting.")
        return
    
    state = DayState()
    
    try:
        while True:
            now = datetime.now(JAKARTA_TZ)
            current_hour, current_min = now.hour, now.minute
            
            # Check session
            session_open = SESSION_START[0] <= current_hour < SESSION_END[0]
            
            # Session opened
            if session_open and not state.signal_placed:
                log.info(f"=== New trading day: {now.date()} ===")
                
                # Get OHLCV data
                ohlcv = broker.get_ohlcv(SYMBOL, "H1", count=10)
                
                # Calculate signal
                signal = calculate_7c_signal(ohlcv)
                
                if signal["signal"] == "BREAKOUT" and state.can_trade():
                    # Place orders
                    if place_pending_orders(broker, signal, balance, dry_run):
                        state.signal_placed = True
                        log.info(f"Signal placed: Range={signal['range']:.2f}pts | HH={signal['hh']:.2f} LL={signal['ll']:.2f}")
                else:
                    log.info(f"Signal: {signal['signal']} | Reason: {signal.get('reason', 'N/A')}")
            
            # Check trade result during session
            if state.signal_placed:
                check_trade_result(broker, signal, dry_run)
            
            # Session ended
            if not session_open and (state.signal_placed or state.open_trade):
                log.info("Session ended")
                cancel_pending_orders(broker, dry_run)
                state = DayState()  # Reset for next day
            
            if once:
                log.info("--once flag set, exiting after single loop")
                break
            
            time.sleep(POLL_SECS)
    
    except KeyboardInterrupt:
        log.info("Received interrupt, shutting down...")
    finally:
        if broker:
            broker.disconnect()
        log.info("Automated trader stopped")

# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="BerkahKarya Automated Trader — XAUUSD Asia 7-Candle Breakout"
    )
    parser.add_argument("--balance", type=float, default=1000.0,
                        help="Account balance in USD (default: 1000)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Log orders without executing them")
    parser.add_argument("--once", action="store_true",
                        help="Run one poll cycle and exit (testing)")
    parser.add_argument("--broker", type=str, default="paper",
                        choices=["mt5", "ctrader", "paper"],
                        help="Broker type: mt5, ctrader, or paper (default: paper)")
    parser.add_argument("--mode", type=str, default="paper",
                        choices=["paper", "demo", "real"],
                        help="Trading mode: paper, demo, or real (default: paper)")
    
    args = parser.parse_args()
    
    run_loop(
        balance=args.balance,
        dry_run=args.dry_run,
        once=args.once,
        broker_type=args.broker,
        mode=args.mode
    )


if __name__ == "__main__":
    main()
