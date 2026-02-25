#!/usr/bin/env python3
"""
BerkahKarya Forward Test (Paper Trading with Live Data)
========================================================
Forward test = paper trading with REAL live data, no real money.
Uses SimulatedBroker to track positions while pulling live price
data from yfinance every poll cycle.

Supported strategies:
  asia7c   — Asia 7-Candle Breakout
  london   — London Session Breakout
  ny       — NY Open Momentum

Usage:
  python forward_test.py --strategy asia7c --balance 1000
  python forward_test.py --strategy all --balance 5000 --interval 300
  python forward_test.py --strategy asia7c --balance 1000 --once   # single poll
"""

import argparse
import json
import logging
import sys
import time as time_mod
from datetime import datetime, date, time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import pytz

try:
    import yfinance as yf
    import pandas as pd
    HAS_YFINANCE = True
except ImportError:
    print("ERROR: yfinance not installed. Run: pip install yfinance pandas")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Paths & logging
# ─────────────────────────────────────────────────────────────────────────────
TRADING_DIR = Path(__file__).parent
LOGS_DIR    = TRADING_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

DATA_DIR    = TRADING_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

FWD_STATE_FILE = DATA_DIR / "forward_test_state.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOGS_DIR / "forward_test.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("forward_test")

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────
JAKARTA_TZ = pytz.timezone("Asia/Jakarta")
YF_TICKER  = "GC=F"

ASIA_START   = time(7, 0)
ASIA_END     = time(15, 0)
LONDON_START = time(15, 0)
LONDON_END   = time(17, 0)
NY_START     = time(20, 30)
NY_END       = time(22, 0)


# ─────────────────────────────────────────────────────────────────────────────
# State persistence
# ─────────────────────────────────────────────────────────────────────────────

class ForwardTestState:
    """Persistent state across forward test sessions."""

    def __init__(self, initial_balance: float = 1000.0):
        self._file = FWD_STATE_FILE
        self._state = self._load(initial_balance)

    def _load(self, initial_balance: float) -> Dict[str, Any]:
        if self._file.exists():
            try:
                with open(self._file) as f:
                    s = json.load(f)
                log.info(f"Loaded forward test state: {len(s.get('trades', []))} trades, "
                         f"balance=${s.get('balance', initial_balance):,.2f}")
                return s
            except Exception as e:
                log.warning(f"Could not load state: {e}. Starting fresh.")
        return {
            "balance":       initial_balance,
            "initial":       initial_balance,
            "trades":        [],
            "open_trades":   {},
            "signal_today":  {},
            "last_run":      None,
        }

    def save(self):
        with open(self._file, "w") as f:
            json.dump(self._state, f, indent=2, default=str)

    # Balance
    @property
    def balance(self) -> float:
        return self._state["balance"]

    @balance.setter
    def balance(self, v: float):
        self._state["balance"] = v

    # Open trades
    def add_trade(self, trade_id: str, trade: Dict):
        self._state["open_trades"][trade_id] = trade
        self.save()

    def close_trade(self, trade_id: str, close_price: float, close_time: str):
        trade = self._state["open_trades"].pop(trade_id, None)
        if trade is None:
            return None
        direction = 1 if trade["direction"] == "BUY" else -1
        pnl_pts   = direction * (close_price - trade["entry"])
        lot       = trade["lot"]
        pnl_usd   = round(pnl_pts * 100 * lot, 2)
        win       = pnl_pts > 0

        record = {
            **trade,
            "close_price": close_price,
            "close_time":  close_time,
            "pnl_pts":     round(pnl_pts, 2),
            "pnl_usd":     pnl_usd,
            "win":         win,
        }
        self._state["trades"].append(record)
        self._state["balance"] = round(self._state["balance"] + pnl_usd, 2)
        self.save()

        result_str = "WIN ✓" if win else "LOSS ✗"
        log.info(
            f"[{result_str}] {trade['direction']} {trade['symbol']} "
            f"entry={trade['entry']:.2f} close={close_price:.2f} "
            f"P/L=${pnl_usd:+.2f}  (bal=${self._state['balance']:,.2f})"
        )
        return record

    def get_open_trades(self) -> Dict:
        return self._state["open_trades"]

    def get_signal_today(self, strategy: str, today: str) -> Optional[Dict]:
        key = f"{strategy}_{today}"
        return self._state["signal_today"].get(key)

    def set_signal_today(self, strategy: str, today: str, signal: Dict):
        key = f"{strategy}_{today}"
        self._state["signal_today"][key] = signal
        self.save()

    def summary(self) -> Dict[str, Any]:
        trades  = self._state["trades"]
        if not trades:
            return {
                "total": 0, "wins": 0, "losses": 0, "win_rate": 0.0,
                "net_pnl": 0.0, "balance": self.balance,
                "initial": self._state["initial"], "return": 0.0,
            }
        wins    = [t for t in trades if t["win"]]
        losses  = [t for t in trades if not t["win"]]
        net_pnl = sum(t["pnl_usd"] for t in trades)
        return {
            "total":    len(trades),
            "wins":     len(wins),
            "losses":   len(losses),
            "win_rate": round(len(wins) / len(trades) * 100, 1) if trades else 0,
            "net_pnl":  round(net_pnl, 2),
            "balance":  self.balance,
            "initial":  self._state["initial"],
            "return":   round((self.balance - self._state["initial"]) / self._state["initial"] * 100, 2),
        }


# ─────────────────────────────────────────────────────────────────────────────
# Live data helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_live_price() -> Optional[float]:
    """Fetch current XAUUSD (GC=F) bid price from yfinance."""
    try:
        ticker = yf.Ticker(YF_TICKER)
        info   = ticker.info
        price  = (
            info.get("regularMarketPrice")
            or info.get("currentPrice")
            or info.get("previousClose")
        )
        if price:
            return float(price)
    except Exception as e:
        log.warning(f"Live price fetch failed: {e}")
    return None


def get_recent_bars(interval: str = "1h", period: str = "5d") -> pd.DataFrame:
    """Fetch recent OHLCV bars for session analysis."""
    try:
        ticker = yf.Ticker(YF_TICKER)
        df     = ticker.history(period=period, interval=interval)
        if df.empty:
            return df
        if df.index.tz is None:
            df.index = df.index.tz_localize("UTC")
        df.index = df.index.tz_convert(JAKARTA_TZ)
        return df
    except Exception as e:
        log.warning(f"Bar fetch failed: {e}")
        return pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# Signal generators (reuse logic from backtest)
# ─────────────────────────────────────────────────────────────────────────────

def check_asia7c_signal(df: pd.DataFrame, today: date) -> Optional[Dict]:
    """Check Asia 7-Candle signal for today."""
    today_data = df[df.index.date == today]
    window = today_data[
        (today_data.index.time >= ASIA_START) &
        (today_data.index.time < time(14, 0))
    ].head(7)

    if len(window) < 4:
        return None

    hh = float(window["High"].max())
    ll = float(window["Low"].min())
    r  = hh - ll

    if r <= 0:
        return None

    buffer    = min(0.5, r * 0.01)
    buy_stop  = round(hh + buffer, 2)
    sell_stop = round(ll - buffer, 2)

    return {
        "strategy":   "asia7c",
        "hh":         hh,
        "ll":         ll,
        "range":      round(r, 2),
        "buy_stop":   buy_stop,
        "sell_stop":  sell_stop,
        "buy_tp":     round(buy_stop  + r * 2.0, 2),
        "buy_sl":     round(buy_stop  - r,        2),
        "sell_tp":    round(sell_stop - r * 2.0,  2),
        "sell_sl":    round(sell_stop + r,         2),
        "risk_r":     round(r, 2),
    }


def check_london_signal(df: pd.DataFrame, today: date) -> Optional[Dict]:
    """Check London Breakout signal for today."""
    today_data = df[df.index.date == today]
    asia = today_data[
        (today_data.index.time >= ASIA_START) &
        (today_data.index.time < LONDON_START)
    ]

    if asia.empty:
        return None

    asia_high = float(asia["High"].max())
    asia_low  = float(asia["Low"].min())
    r         = asia_high - asia_low

    if r <= 0:
        return None

    buffer    = asia_high * 0.0002
    buy_stop  = round(asia_high + buffer, 2)
    sell_stop = round(asia_low  - buffer, 2)

    return {
        "strategy":   "london",
        "asia_high":  round(asia_high, 2),
        "asia_low":   round(asia_low,  2),
        "range":      round(r, 2),
        "buy_stop":   buy_stop,
        "sell_stop":  sell_stop,
        "buy_tp":     round(buy_stop  + 1.5 * r, 2),
        "buy_sl":     round(buy_stop  - 0.5 * r, 2),
        "sell_tp":    round(sell_stop - 1.5 * r, 2),
        "sell_sl":    round(sell_stop + 0.5 * r, 2),
        "risk_r":     round(0.5 * r, 2),
    }


def check_ny_signal(df: pd.DataFrame, today: date) -> Optional[Dict]:
    """Check NY Momentum signal for today."""
    today_data = df[df.index.date == today]
    ny_bars    = today_data[today_data.index.time >= NY_START]

    if ny_bars.empty:
        return None

    first = ny_bars.iloc[0]
    o = float(first["Open"])
    h = float(first["High"])
    l = float(first["Low"])
    c = float(first["Close"])

    if c == o:
        return None   # doji

    bullish = c > o
    sl      = l if bullish else h
    risk    = abs(c - sl)

    if risk <= 0:
        return None

    tp = c + 2.0 * risk if bullish else c - 2.0 * risk

    return {
        "strategy":   "ny",
        "direction":  "BUY" if bullish else "SELL",
        "entry":      round(c, 2),
        "sl":         round(sl, 2),
        "tp":         round(tp, 2),
        "risk_r":     round(risk, 2),
        # For pending-order-style tracking
        "buy_stop":   round(c, 2) if bullish else None,
        "sell_stop":  round(c, 2) if not bullish else None,
        "buy_sl":     round(sl, 2) if bullish else None,
        "buy_tp":     round(tp, 2) if bullish else None,
        "sell_sl":    round(sl, 2) if not bullish else None,
        "sell_tp":    round(tp, 2) if not bullish else None,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Forward Test engine
# ─────────────────────────────────────────────────────────────────────────────

class ForwardTestEngine:
    """Manages forward test state and executes strategy logic."""

    def __init__(self, strategies: List[str], balance: float, risk_pct: float = 0.01):
        self.strategies = strategies
        self.risk_pct   = risk_pct
        self.state      = ForwardTestState(balance)

    def _lot_size(self, balance: float, risk_r: float) -> float:
        """Calculate lot size: 1% risk, gold = $100/pt per lot."""
        lot = (balance * self.risk_pct) / (risk_r * 100 + 1e-9)
        return max(0.01, round(lot, 2))

    def _now_wib(self) -> datetime:
        return datetime.now(JAKARTA_TZ)

    def poll(self):
        """One poll cycle: check signals and manage open trades."""
        now   = self._now_wib()
        today = now.date()
        t     = now.time()

        log.info(f"── Poll at {now.strftime('%Y-%m-%d %H:%M:%S %Z')} ──")

        # Fetch bars
        df = get_recent_bars("1h", "5d")
        if df.empty:
            log.warning("No bar data available. Skipping poll.")
            return

        # Live price
        live_price = get_live_price()
        if live_price is None:
            live_price = float(df.iloc[-1]["Close"])
        log.info(f"Live price: {live_price:.2f}")

        # ── Check / update open trades ──
        self._update_open_trades(live_price, now)

        # ── Generate signals per strategy ──
        for strategy in self.strategies:
            self._process_strategy(strategy, df, today, t, live_price, now)

        # Print running summary
        s = self.state.summary()
        log.info(
            f"[Summary] Trades={s['total']} W/L={s.get('wins',0)}/{s.get('losses',0)} "
            f"WR={s.get('win_rate',0.0)}% Net=${s.get('net_pnl',0.0):+.2f} Bal=${s['balance']:,.2f}"
        )

    def _update_open_trades(self, price: float, now: datetime):
        """Check TP/SL on open trades."""
        to_close = []
        for tid, trade in self.state.get_open_trades().items():
            tp = trade.get("tp")
            sl = trade.get("sl")
            direction = trade["direction"]

            hit = None
            if direction == "BUY":
                if tp and price >= tp:
                    hit = ("TP", tp)
                elif sl and price <= sl:
                    hit = ("SL", sl)
            else:
                if tp and price <= tp:
                    hit = ("TP", tp)
                elif sl and price >= sl:
                    hit = ("SL", sl)

            if hit:
                log.info(f"Trade {tid}: {hit[0]} hit at {hit[1]:.2f} (price={price:.2f})")
                to_close.append((tid, hit[1]))

        for tid, close_px in to_close:
            self.state.close_trade(tid, close_px, now.isoformat())

    def _process_strategy(
        self,
        strategy: str,
        df: pd.DataFrame,
        today: date,
        t: time,
        price: float,
        now: datetime,
    ):
        """Process one strategy: generate signal and open trade if needed."""
        today_str = today.isoformat()

        # Already signalled today?
        existing = self.state.get_signal_today(strategy, today_str)

        if strategy == "asia7c":
            self._handle_asia7c(df, today, today_str, t, price, now, existing)
        elif strategy == "london":
            self._handle_london(df, today, today_str, t, price, now, existing)
        elif strategy == "ny":
            self._handle_ny(df, today, today_str, t, price, now, existing)

    def _handle_asia7c(self, df, today, today_str, t, price, now, existing):
        in_session = ASIA_END <= t < time(23, 59)  # post-Asia breakout window

        if existing is not None:
            return  # Signal already processed today

        if not in_session:
            return  # Wait for Asia session to close

        sig = check_asia7c_signal(df, today)
        if sig is None:
            log.info("[Asia7C] No signal today (insufficient bars)")
            self.state.set_signal_today("asia7c", today_str, {"none": True})
            return

        log.info(
            f"[Asia7C] Signal: HH={sig['hh']:.2f} LL={sig['ll']:.2f} "
            f"Range={sig['range']:.2f}  "
            f"BUY@{sig['buy_stop']} TP={sig['buy_tp']} SL={sig['buy_sl']}  |  "
            f"SELL@{sig['sell_stop']} TP={sig['sell_tp']} SL={sig['sell_sl']}"
        )

        lot = self._lot_size(self.state.balance, sig["range"])

        # Check if price already triggered
        for direction, entry, tp, sl in [
            ("BUY",  sig["buy_stop"],  sig["buy_tp"],  sig["buy_sl"]),
            ("SELL", sig["sell_stop"], sig["sell_tp"], sig["sell_sl"]),
        ]:
            triggered = (
                (direction == "BUY"  and price >= entry) or
                (direction == "SELL" and price <= entry)
            )
            if triggered:
                tid = f"asia7c_{today_str}_{direction.lower()}"
                self.state.add_trade(tid, {
                    "strategy":  "asia7c",
                    "symbol":    "XAUUSD",
                    "direction": direction,
                    "entry":     entry,
                    "tp":        tp,
                    "sl":        sl,
                    "lot":       lot,
                    "open_time": now.isoformat(),
                })
                log.info(
                    f"[Asia7C] ENTRY {direction} @ {entry:.2f}  "
                    f"TP={tp:.2f}  SL={sl:.2f}  lot={lot}"
                )

        self.state.set_signal_today("asia7c", today_str, sig)

    def _handle_london(self, df, today, today_str, t, price, now, existing):
        in_session = LONDON_START <= t < LONDON_END

        if existing is not None:
            return

        if not in_session:
            return

        sig = check_london_signal(df, today)
        if sig is None:
            log.info("[London] No signal today")
            self.state.set_signal_today("london", today_str, {"none": True})
            return

        log.info(
            f"[London] Signal: Asia range [{sig['asia_low']:.2f} - {sig['asia_high']:.2f}] "
            f"= {sig['range']:.2f} pts  "
            f"BUY@{sig['buy_stop']}  SELL@{sig['sell_stop']}"
        )

        lot = self._lot_size(self.state.balance, sig["range"] * 0.5)

        for direction, entry, tp, sl in [
            ("BUY",  sig["buy_stop"],  sig["buy_tp"],  sig["buy_sl"]),
            ("SELL", sig["sell_stop"], sig["sell_tp"], sig["sell_sl"]),
        ]:
            triggered = (
                (direction == "BUY"  and price >= entry) or
                (direction == "SELL" and price <= entry)
            )
            if triggered:
                tid = f"london_{today_str}_{direction.lower()}"
                self.state.add_trade(tid, {
                    "strategy":  "london",
                    "symbol":    "XAUUSD",
                    "direction": direction,
                    "entry":     entry,
                    "tp":        tp,
                    "sl":        sl,
                    "lot":       lot,
                    "open_time": now.isoformat(),
                })
                log.info(
                    f"[London] ENTRY {direction} @ {entry:.2f}  "
                    f"TP={tp:.2f}  SL={sl:.2f}  lot={lot}"
                )

        self.state.set_signal_today("london", today_str, sig)

    def _handle_ny(self, df, today, today_str, t, price, now, existing):
        in_session = NY_START <= t < NY_END

        if existing is not None:
            return

        if not in_session:
            return

        sig = check_ny_signal(df, today)
        if sig is None:
            log.info("[NY] No signal today (doji or no bars)")
            self.state.set_signal_today("ny", today_str, {"none": True})
            return

        log.info(
            f"[NY] Signal: {sig['direction']}  entry={sig['entry']:.2f}  "
            f"TP={sig['tp']:.2f}  SL={sig['sl']:.2f}  risk={sig['risk_r']:.2f}"
        )

        lot = self._lot_size(self.state.balance, sig["risk_r"])
        tid = f"ny_{today_str}_{sig['direction'].lower()}"

        if not self.state.get_open_trades().get(tid):
            self.state.add_trade(tid, {
                "strategy":  "ny",
                "symbol":    "XAUUSD",
                "direction": sig["direction"],
                "entry":     sig["entry"],
                "tp":        sig["tp"],
                "sl":        sig["sl"],
                "lot":       lot,
                "open_time": now.isoformat(),
            })
            log.info(
                f"[NY] ENTRY {sig['direction']} @ {sig['entry']:.2f}  "
                f"TP={sig['tp']:.2f}  SL={sig['sl']:.2f}  lot={lot}"
            )

        self.state.set_signal_today("ny", today_str, sig)

    def print_summary(self):
        s = self.state.summary()
        print()
        print("=" * 64)
        print("  FORWARD TEST SUMMARY")
        print("=" * 64)
        print(f"  Strategies      : {', '.join(self.strategies)}")
        print(f"  Initial Balance : ${s['initial']:>10,.2f}")
        print(f"  Current Balance : ${s['balance']:>10,.2f}")
        print(f"  Return          : {s['return']:>+10.2f}%")
        print(f"  Total Trades    : {s['total']}")
        print(f"  Win / Loss      : {s['wins']}W / {s['losses']}L  ({s['win_rate']}%)")
        print(f"  Net PnL         : ${s['net_pnl']:>+10,.2f}")
        print(f"  Open Trades     : {len(self.state.get_open_trades())}")
        print("=" * 64)

        open_trades = self.state.get_open_trades()
        if open_trades:
            print("\n  Open Positions:")
            for tid, t in open_trades.items():
                print(f"    {tid}: {t['direction']} entry={t['entry']:.2f} "
                      f"SL={t['sl']:.2f} TP={t['tp']:.2f} lot={t['lot']}")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="BerkahKarya Forward Test — paper trading with live yfinance data"
    )
    parser.add_argument(
        "--strategy", "-s",
        default="asia7c",
        help="Strategy: asia7c, london, ny, or comma-separated list (default: asia7c)"
    )
    parser.add_argument(
        "--balance", "-b",
        type=float,
        default=1000.0,
        help="Starting balance in USD (default: 1000)"
    )
    parser.add_argument(
        "--risk",
        type=float,
        default=0.01,
        help="Risk per trade as fraction (default: 0.01 = 1%%)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Poll interval in seconds (default: 300 = 5 min)"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one poll cycle and exit (testing)"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset all forward test state (start fresh)"
    )
    args = parser.parse_args()

    if args.reset:
        if FWD_STATE_FILE.exists():
            FWD_STATE_FILE.unlink()
            print("Forward test state reset.")
        else:
            print("No state file found.")
        return

    # Parse strategies
    if args.strategy == "all":
        strategies = ["asia7c", "london", "ny"]
    else:
        strategies = [s.strip() for s in args.strategy.split(",")]

    valid = {"asia7c", "london", "ny"}
    for s in strategies:
        if s not in valid:
            print(f"ERROR: Unknown strategy '{s}'. Valid: asia7c, london, ny, all")
            sys.exit(1)

    engine = ForwardTestEngine(strategies, args.balance, args.risk)

    log.info(f"Forward Test started | strategies={strategies} | "
             f"balance=${args.balance:,.2f} | risk={args.risk*100:.1f}%")

    if args.once:
        engine.poll()
        engine.print_summary()
        return

    try:
        while True:
            engine.poll()
            engine.print_summary()
            log.info(f"Next poll in {args.interval}s...")
            time_mod.sleep(args.interval)
    except KeyboardInterrupt:
        log.info("Forward test interrupted by user.")
        engine.print_summary()


if __name__ == "__main__":
    main()
