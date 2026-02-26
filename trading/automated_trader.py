#!/usr/bin/env python3
"""
BerkahKarya Automated Trader
=============================
Runs XAUUSD trading strategies automatically.
Supports MT5 (via mt5linux), cTrader, and Paper trading modes.

Strategies:
    - asia7c  : Asia 7-Candle Breakout (default)
    - maybe_hft: Maybe HFT Hedging EA (main + hedge with trailing)
    - london  : London Breakout strategy
    - ny_momentum : NY Momentum strategy

Usage:
    python automated_trader.py --strategy asia7c --broker paper --mode paper --once
    python automated_trader.py --strategy maybe_hft --broker mt5 --mode demo
    python automated_trader.py --strategy london --broker mt5 --mode real
    python automated_trader.py --strategy ny_momentum --broker paper --dry-run --once

MT5 env vars:
    MT5_LOGIN    — account number (integer)
    MT5_PASSWORD — account password
    MT5_SERVER   — broker server name

Maybe HFT EA parameters:
    --lots 0.05 --stoploss 1000 --trailing 300 --x-distance 300
"""

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

import pytz

# ─────────────────────────────────────────────────────────────────────────────
# Sys-path: allow running from any directory
# ─────────────────────────────────────────────────────────────────────────────
_TRADING_DIR = Path(__file__).resolve().parent
if str(_TRADING_DIR) not in sys.path:
    sys.path.insert(0, str(_TRADING_DIR))

# ─────────────────────────────────────────────────────────────────────────────
# Imports
# ─────────────────────────────────────────────────────────────────────────────
from brokers.simulated import SimulatedBroker

# Maybe HFT EA import
try:
    from EA.maybe_hft import MaybeHFT, EAConfig
    MAYBE_HFT_AVAILABLE = True
except ImportError:
    MAYBE_HFT_AVAILABLE = False
    print("⚠️ Maybe HFT EA not available (EA/maybe_hft.py not found)")

# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────
LOGS_DIR = _TRADING_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE  = LOGS_DIR / "trading.log"


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("automated_trader")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
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

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────
JAKARTA_TZ   = pytz.timezone("Asia/Jakarta")
SESSION_START = (7, 0)    # 07:00 WIB
SESSION_END   = (15, 0)   # 15:00 WIB

SYMBOL    = "XAUUSD"
MAX_TRADES = 3
RISK_PCT   = 0.01   # 1% per trade
RR_RATIO   = 2.0
POLL_SECS  = 60


# ─────────────────────────────────────────────────────────────────────────────
# Broker factory
# ─────────────────────────────────────────────────────────────────────────────

def create_broker(broker_type: str, mode: str = "paper", **kwargs):
    """
    Create and connect a broker instance.

    broker_type: 'mt5' | 'ctrader' | 'paper'
    mode:        'paper' | 'demo' | 'real'
    """
    broker_type = broker_type.lower()

    # ── Paper / Simulated ──────────────────────────────────────────────────
    if broker_type == "paper":
        log.info("Initializing SimulatedBroker (paper trading)")
        sim = SimulatedBroker()
        sim.connect()
        return sim

    # ── MetaTrader 5 via mt5linux ──────────────────────────────────────────
    elif broker_type == "mt5":
        log.info(f"Initializing MT5 connector (mode={mode}) via mt5linux @ 5.189.138.144:18812")
        try:
            from brokers.mt5.connector import MT5Connector
        except ImportError as e:
            log.warning(f"MT5Connector not available: {e} — falling back to paper")
            sim = SimulatedBroker(); sim.connect(); return sim

        try:
            mt5 = MT5Connector(host="5.189.138.144", port=18812)
        except (ConnectionError, Exception) as e:
            log.warning(f"MT5 server unreachable: {e} — falling back to paper")
            sim = SimulatedBroker(); sim.connect(); return sim

        if mode in ("demo", "real"):
            login    = int(os.environ.get("MT5_LOGIN", kwargs.get("login", 0)))
            password = os.environ.get("MT5_PASSWORD", kwargs.get("password", ""))
            server   = os.environ.get("MT5_SERVER",   kwargs.get("server",   ""))

            if not login:
                log.error(
                    "MT5 login required. Set env vars: MT5_LOGIN, MT5_PASSWORD, MT5_SERVER"
                )
                return None

            ok = mt5.connect(login=login, password=password, server=server)
        else:
            # paper mode with MT5 connector — just initialize, no login
            ok = mt5.connect()

        if not ok:
            log.warning("Failed to connect to MT5 — falling back to SimulatedBroker (paper mode)")
            sim = SimulatedBroker()
            sim.connect()
            return sim

        log.info("MT5 connected successfully")
        return mt5

    # ── cTrader ───────────────────────────────────────────────────────────
    elif broker_type == "ctrader":
        log.info(f"Initializing cTrader connector (mode={mode})")
        try:
            from brokers.ctrader.connector import CTraderConnector
        except ImportError as e:
            log.error(f"Could not import CTraderConnector: {e}")
            return None

        ctrader = CTraderConnector()

        if mode in ("demo", "real"):
            client_id     = os.environ.get("CTRADER_CLIENT_ID",     kwargs.get("client_id", ""))
            client_secret = os.environ.get("CTRADER_CLIENT_SECRET",  kwargs.get("client_secret", ""))
            access_token  = os.environ.get("CTRADER_ACCESS_TOKEN",   kwargs.get("access_token", ""))

            if not all([client_id, client_secret, access_token]):
                log.error(
                    "cTrader credentials required. Set: CTRADER_CLIENT_ID, "
                    "CTRADER_CLIENT_SECRET, CTRADER_ACCESS_TOKEN"
                )
                return None

            ok = ctrader.connect(
                client_id=client_id,
                client_secret=client_secret,
                access_token=access_token,
            )
            if not ok:
                log.error("Failed to connect to cTrader")
                return None

        return ctrader

    else:
        log.error(f"Unknown broker: '{broker_type}'. Use: mt5, ctrader, paper")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Asia 7-Candle Signal Calculator
# ─────────────────────────────────────────────────────────────────────────────

def calculate_7c_signal(ohlcv_list: list) -> Dict[str, Any]:
    """
    Calculate XAUUSD Asia 7-Candle Breakout signal.

    Takes the 7 most recent candles from the Asia session window,
    finds HH/LL, and sets pending order levels.
    """
    if len(ohlcv_list) < 8:
        return {"signal": "WAIT", "reason": "Insufficient data"}

    # Use candles 1..7 (skip candle[0] which may be partial)
    candles = ohlcv_list[1:8]

    hh = max(c.high for c in candles)
    ll = min(c.low  for c in candles)
    r  = hh - ll

    if r <= 0:
        return {"signal": "WAIT", "reason": "Zero range"}

    buffer    = min(0.5, r * 0.01)
    buy_stop  = hh + buffer
    sell_stop = ll - buffer

    buy_tp   = buy_stop  + r * RR_RATIO
    buy_sl   = buy_stop  - r
    sell_tp  = sell_stop - r * RR_RATIO
    sell_sl  = sell_stop + r

    current = ohlcv_list[-1]

    return {
        "signal":     "BREAKOUT",
        "hh":         hh,
        "ll":         ll,
        "range":      r,
        "buy_stop":   buy_stop,
        "sell_stop":  sell_stop,
        "buy_tp":     buy_tp,
        "buy_sl":     buy_sl,
        "sell_tp":    sell_tp,
        "sell_sl":    sell_sl,
        "current":    current.close,
        "timestamp":  datetime.now(JAKARTA_TZ).isoformat(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Order helpers
# ─────────────────────────────────────────────────────────────────────────────

def place_pending_orders(broker, signal: Dict, balance: float, dry_run: bool) -> bool:
    """Place BUY_STOP and SELL_STOP orders via the broker's unified interface."""
    if signal.get("signal") != "BREAKOUT":
        return False

    r        = signal["range"]
    lot_size = (balance * RISK_PCT) / (r * 100 + 1e-9)
    lot_size = max(0.01, round(lot_size, 2))

    prefix   = "[DRY-RUN] " if dry_run else "[REAL] "
    placed   = 0

    for direction, entry, tp, sl, label in [
        ("BUY_STOP",  signal["buy_stop"],  signal["buy_tp"],  signal["buy_sl"],  "Asia 7C Buy"),
        ("SELL_STOP", signal["sell_stop"], signal["sell_tp"], signal["sell_sl"], "Asia 7C Sell"),
    ]:
        try:
            order = broker.place_order(
                symbol=SYMBOL,
                order_type=direction,
                volume=lot_size,
                price=entry,
                sl=sl,
                tp=tp,
                comment=label,
                dry_run=dry_run,
            )
            if order is not None:
                placed += 1
                log.info(
                    f"{prefix}{direction} {SYMBOL} lot={lot_size} "
                    f"@ {entry:.2f}  SL={sl:.2f}  TP={tp:.2f}"
                )
        except Exception as e:
            log.error(f"Failed to place {direction} order: {e}")

    return placed > 0


def check_trade_result(broker, signal: Dict, dry_run: bool):
    """Check open positions; close if SL/TP hit."""
    try:
        positions = broker.get_positions()
    except Exception as e:
        log.warning(f"get_positions failed: {e}")
        return

    current_price = signal.get("current", 0.0)

    for pos in positions:
        # Try to get live price if broker supports it
        if hasattr(broker, "_get_price"):
            try:
                current_price = broker._get_price(pos.symbol)
            except Exception:
                pass

        hit = None
        if pos.order_type.startswith("BUY"):
            if pos.sl and current_price <= pos.sl:
                hit = ("SL", pos.sl)
            elif pos.tp and current_price >= pos.tp:
                hit = ("TP", pos.tp)
        else:
            if pos.sl and current_price >= pos.sl:
                hit = ("SL", pos.sl)
            elif pos.tp and current_price <= pos.tp:
                hit = ("TP", pos.tp)

        if hit:
            log.info(
                f"[{'DRY-RUN' if dry_run else 'REAL'}] "
                f"{pos.order_type} {pos.symbol} hit {hit[0]} @ {current_price:.2f}"
            )
            try:
                broker.close_position(pos.ticket, dry_run=dry_run)
            except Exception as e:
                log.error(f"close_position failed: {e}")


def cancel_all_pending(broker, dry_run: bool):
    """Cancel all pending orders at session end."""
    log.info(f"[{'DRY-RUN' if dry_run else 'REAL'}] Cancelling pending orders at session end")
    if hasattr(broker, "cancel_all_pending_orders"):
        try:
            n = broker.cancel_all_pending_orders(SYMBOL)
            log.info(f"Cancelled {n} pending orders")
        except Exception as e:
            log.warning(f"cancel_all_pending_orders failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Day state
# ─────────────────────────────────────────────────────────────────────────────

class DayState:
    def __init__(self):
        self.signal_placed = False
        self.trades_today  = 0

    def can_trade(self) -> bool:
        return self.trades_today < MAX_TRADES


# ─────────────────────────────────────────────────────────────────────────────
# Main loop
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# Maybe HFT EA Strategy Runner
# ─────────────────────────────────────────────────────────────────────────────

def run_maybe_hft_ea(
    balance: float,
    dry_run: bool,
    once: bool,
    broker_type: str,
    mode: str,
    lots: float,
    stoploss: int,
    trailing: int,
    trail_start: int,
    x_distance: int,
    start_direction: int,
    magic: int,
    symbol: str,
    interval: float,
):
    """
    Run Maybe HFT Hedging EA as a strategy.
    
    Args:
        balance: Account balance (for lot sizing if needed)
        dry_run: If True, only log (EA uses broker's dry_run internally)
        once: Run once and exit
        broker_type: mt5, paper, ctrader
        mode: paper, demo, real
        lots: Position size in lots
        stoploss: StopLoss in points
        trailing: Trailing stop distance
        trail_start: Min profit before trailing
        x_distance: Hedge pending distance from SL
        start_direction: 0=BUY first, 1=SELL first
        magic: Magic number
        symbol: Trading symbol
        interval: Check interval in seconds
    """
    if not MAYBE_HFT_AVAILABLE:
        log.error("Maybe HFT EA not available. Please check EA/maybe_hft.py")
        return
    
    log.info(
        f"Maybe HFT EA | broker={broker_type} | mode={mode} | "
        f"symbol={symbol} | lots={lots} | SL={stoploss}pts | "
        f"Trail={trailing}pts | StartDir={'BUY' if start_direction == 0 else 'SELL'}"
    )
    
    # Determine effective broker type (EA handles its own broker choice)
    ea_broker = broker_type
    
    # Create EA configuration
    config = EAConfig(
        symbol=symbol,
        lots=lots,
        stoploss=stoploss,
        trailing=trailing,
        trail_start=trail_start,
        x_distance=x_distance,
        magic=magic,
        start_direction=start_direction,
        broker=ea_broker,
        mode=mode if not dry_run else "paper",
        once=once,
        interval=interval,
    )
    
    # Create and run EA
    ea = MaybeHFT(config)
    
    if mode == "live" and not dry_run:
        log.warning("⚠️⚠️⚠️ LIVE TRADING MODE - REAL MONEY ⚠️⚠️⚠️")
        log.warning("Press Ctrl+C to cancel within 10 seconds...")
        time.sleep(10)
    
    try:
        if once:
            # Single run mode
            if ea.initialize_broker():
                ea.broker.subscribe(symbol)
                ea.broker.refresh()
                ea.trail_orders()
                ea.handle_pending()
                if ea.count_main_orders() == 0 and ea.count_pending_orders() == 0:
                    ea.open_main_order(start_direction)
                log.info("✅ Maybe HFT EA single run completed")
                ea.broker.disconnect()
            else:
                log.error("Failed to initialize broker for Maybe HFT EA")
        else:
            # Continuous mode
            ea.run()
    except KeyboardInterrupt:
        log.info("Maybe HFT EA interrupted by user")
    except Exception as e:
        log.error(f"Maybe HFT EA error: {e}")
    finally:
        log.info("Maybe HFT EA stopped")
    log.info(
        f"BerkahKarya Automated Trader | broker={broker_type} | mode={mode} | "
        f"balance=${balance:,.2f} | dry_run={dry_run}"
    )
    log.info(f"Strategy: XAUUSD Asia 7-Candle Breakout | Risk={RISK_PCT*100:.0f}%/trade | RR=1:{RR_RATIO}")

    broker = create_broker(broker_type, mode)
    if broker is None:
        log.error("Broker init failed. Exiting.")
        return

    # Attempt account info
    try:
        info = broker.get_account_info()
        if info:
            log.info(f"Account: login={info.login} balance=${info.balance:.2f} equity=${info.equity:.2f}")
    except Exception as e:
        log.warning(f"get_account_info failed: {e}")

    state = DayState()
    signal = {}

    try:
        while True:
            now = datetime.now(JAKARTA_TZ)
            h, m = now.hour, now.minute

            in_session = SESSION_START[0] <= h < SESSION_END[0]

            # ── New session: generate signal ────────────────────────────────
            if in_session and not state.signal_placed:
                log.info(f"=== Session open: {now.strftime('%Y-%m-%d %H:%M WIB')} ===")

                try:
                    ohlcv = broker.get_ohlcv(SYMBOL, "H1", count=15)
                except Exception as e:
                    log.error(f"get_ohlcv failed: {e}")
                    ohlcv = []

                if ohlcv:
                    signal = calculate_7c_signal(ohlcv)

                    if signal.get("signal") == "BREAKOUT" and state.can_trade():
                        log.info(
                            f"Signal: HH={signal['hh']:.2f} LL={signal['ll']:.2f} "
                            f"Range={signal['range']:.2f}  "
                            f"BUY@{signal['buy_stop']:.2f}  SELL@{signal['sell_stop']:.2f}"
                        )
                        if place_pending_orders(broker, signal, balance, dry_run):
                            state.signal_placed = True
                            state.trades_today += 1
                    else:
                        log.info(
                            f"Signal: {signal.get('signal')} — {signal.get('reason', 'N/A')}"
                        )
                else:
                    log.warning("No OHLCV data available")

            # ── Check SL/TP on open positions ───────────────────────────────
            if state.signal_placed and signal:
                check_trade_result(broker, signal, dry_run)

            # ── Session closed: reset for next day ──────────────────────────
            if not in_session and state.signal_placed:
                log.info("Session ended — cancelling pending, resetting state")
                cancel_all_pending(broker, dry_run)
                state = DayState()
                signal = {}

            if once:
                log.info("--once flag set, exiting after single poll")
                break

            time.sleep(POLL_SECS)

    except KeyboardInterrupt:
        log.info("Received interrupt, shutting down...")
    finally:
        try:
            broker.disconnect()
        except Exception:
            pass
        log.info("Automated trader stopped")


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="BerkahKarya Automated Trader — Multi-strategy XAUUSD trading"
    )
    parser.add_argument(
        "--strategy", type=str, default="asia7c",
        choices=["asia7c", "maybe_hft", "london", "ny_momentum"],
        help="Trading strategy: asia7c (default), maybe_hft, london, ny_momentum"
    )
    parser.add_argument(
        "--balance", type=float, default=1000.0,
        help="Account balance in USD (default: 1000)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Log orders without executing them"
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Run one poll cycle and exit (testing)"
    )
    parser.add_argument(
        "--broker", type=str, default="paper",
        choices=["mt5", "ctrader", "paper"],
        help="Broker: mt5, ctrader, paper (default: paper)"
    )
    parser.add_argument(
        "--mode", type=str, default="paper",
        choices=["paper", "demo", "real"],
        help="Mode: paper, demo, real (default: paper)"
    )
    
    # Maybe HFT EA parameters
    parser.add_argument(
        "--lots", type=float, default=0.10,
        help="Lot size for Maybe HFT EA (default: 0.10)"
    )
    parser.add_argument(
        "--stoploss", type=int, default=1500,
        help="StopLoss in points for Maybe HFT EA (default: 1500)"
    )
    parser.add_argument(
        "--trailing", type=int, default=500,
        help="Trailing distance in points for Maybe HFT EA (default: 500)"
    )
    parser.add_argument(
        "--trail-start", type=int, default=1000,
        help="Min profit before trailing for Maybe HFT EA (default: 1000)"
    )
    parser.add_argument(
        "--x-distance", type=int, default=300,
        help="Hedge pending distance from SL for Maybe HFT EA (default: 300)"
    )
    parser.add_argument(
        "--start-direction", type=int, default=0, choices=[0, 1],
        help="0=BUY first, 1=SELL first for Maybe HFT EA (default: 0)"
    )
    parser.add_argument(
        "--magic", type=int, default=12345,
        help="Magic number for order identification (default: 12345)"
    )
    parser.add_argument(
        "--symbol", type=str, default="GC=X",
        help="Trading symbol (default: GC=X for XAUUSD)"
    )
    parser.add_argument(
        "--interval", type=float, default=1.0,
        help="Check interval in seconds (default: 1.0)"
    )

    args = parser.parse_args()
    
    strategy = args.strategy
    
    log.info(f"=" * 60)
    log.info(f"BerkahKarya Automated Trader v2.0")
    log.info(f"Strategy: {strategy.upper()}")
    log.info(f"=" * 60)
    
    # Route to appropriate strategy
    if strategy == "maybe_hft":
        run_maybe_hft_ea(
            balance=args.balance,
            dry_run=args.dry_run,
            once=args.once,
            broker_type=args.broker,
            mode=args.mode,
            lots=args.lots,
            stoploss=args.stoploss,
            trailing=args.trailing,
            trail_start=args.trail_start,
            x_distance=args.x_distance,
            start_direction=args.start_direction,
            magic=args.magic,
            symbol=args.symbol,
            interval=args.interval,
        )
    elif strategy == "london":
        log.info("London Breakout strategy - Use: python london_breakout.py")
        log.info("Importing and running London Breakout EA...")
        try:
            from london_breakout import LondonBreakoutEA
            ea = LondonBreakoutEA(
                broker_type=args.broker,
                mode=args.mode,
                symbol=args.symbol,
                lots=args.lots,
                stoploss=args.stoploss,
                takeprofit=args.stoploss * 2,  # 1:2 RR default
                dry_run=args.dry_run,
            )
            if args.once:
                ea.run_once()
            else:
                ea.run()
        except ImportError:
            log.error("London Breakout EA not found: london_breakout.py")
            
    elif strategy == "ny_momentum":
        log.info("NY Momentum strategy - Use: python ny_momentum.py")
        log.info("Importing and running NY Momentum EA...")
        try:
            from ny_momentum import NYMomentumEA
            ea = NYMomentumEA(
                broker_type=args.broker,
                mode=args.mode,
                symbol=args.symbol,
                lots=args.lots,
                stoploss=args.stoploss,
                takeprofit=args.stoploss * 2,
                dry_run=args.dry_run,
            )
            if args.once:
                ea.run_once()
            else:
                ea.run()
        except ImportError:
            log.error("NY Momentum EA not found: ny_momentum.py")
            
    else:
        # Default: Asia 7-Candle strategy
        run_loop(
            balance=args.balance,
            dry_run=args.dry_run,
            once=args.once,
            broker_type=args.broker,
            mode=args.mode,
        )


if __name__ == "__main__":
    main()
