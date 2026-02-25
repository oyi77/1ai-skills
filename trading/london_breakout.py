#!/usr/bin/env python3
"""
BerkahKarya — London Session Breakout Strategy
================================================
Session  : 15:00 – 17:00 Jakarta (WIB / UTC+7)
           ≡ 08:00 – 10:00 London (UTC+1/+2)

Logic:
  1. Wait for Asia session to close (14:59 WIB).
  2. Measure the Asia range:
       Asia High = highest high during 07:00–14:59 WIB
       Asia Low  = lowest  low  during 07:00–14:59 WIB
       Range     = Asia High − Asia Low
  3. At London open (15:00 WIB) place pending orders:
       Buy  Stop = Asia High + buffer   → TP = entry + 1.5×Range, SL = entry − 0.5×Range
       Sell Stop = Asia Low  − buffer   → TP = entry − 1.5×Range, SL = entry + 0.5×Range
  4. Cancel all pending orders that haven't triggered by 17:00 WIB.

Backtest (standalone):
  python london_breakout.py --backtest --start 2025-01-01 --end 2026-01-01
"""

import argparse
import sys
from datetime import datetime, date, time, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

import pytz

# ---------------------------------------------------------------------------
# Optional: use Yahoo Finance for backtesting
# ---------------------------------------------------------------------------
try:
    import yfinance as yf
    import pandas as pd
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
JAKARTA_TZ   = pytz.timezone("Asia/Jakarta")
SYMBOL       = "XAUUSD"
YF_TICKER    = "GC=F"        # Gold futures proxy

# Session windows (WIB)
ASIA_START   = time(7, 0)
ASIA_END     = time(14, 59)
LONDON_START = time(15, 0)
LONDON_END   = time(17, 0)

TP_MULT      = 1.5           # TP = 1.5 × range
SL_MULT      = 0.5           # SL = 0.5 × range
BUFFER_PCT   = 0.0002        # 2-pip buffer above/below range edges


# ---------------------------------------------------------------------------
# Core strategy class
# ---------------------------------------------------------------------------
class LondonBreakoutStrategy:
    """London-open range breakout on XAUUSD (or any instrument)."""

    def __init__(self, tp_mult: float = TP_MULT, sl_mult: float = SL_MULT,
                 buffer_pct: float = BUFFER_PCT):
        self.tp_mult    = tp_mult
        self.sl_mult    = sl_mult
        self.buffer_pct = buffer_pct

    # ------------------------------------------------------------------
    # Signal generation
    # ------------------------------------------------------------------
    def generate_signal(
        self,
        asia_high: float,
        asia_low:  float,
        last_price: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Generate London breakout pending orders from the Asia range.

        Returns dict with order levels.
        """
        range_pts = asia_high - asia_low
        if range_pts <= 0:
            raise ValueError(f"Invalid Asia range: {range_pts}")

        buffer    = asia_high * self.buffer_pct
        buy_stop  = round(asia_high + buffer, 2)
        sell_stop = round(asia_low  - buffer, 2)

        buy_tp  = round(buy_stop  + self.tp_mult * range_pts, 2)
        buy_sl  = round(buy_stop  - self.sl_mult * range_pts, 2)
        sell_tp = round(sell_stop - self.tp_mult * range_pts, 2)
        sell_sl = round(sell_stop + self.sl_mult * range_pts, 2)

        return {
            "symbol":     SYMBOL,
            "strategy":   "london_breakout",
            "session":    "15:00-17:00 WIB",
            "asia_high":  round(asia_high, 2),
            "asia_low":   round(asia_low,  2),
            "range":      round(range_pts, 2),
            "buffer":     round(buffer, 2),
            "buy_stop":   buy_stop,
            "buy_tp":     buy_tp,
            "buy_sl":     buy_sl,
            "sell_stop":  sell_stop,
            "sell_tp":    sell_tp,
            "sell_sl":    sell_sl,
            "rr_long":    round(self.tp_mult / self.sl_mult, 2),
            "rr_short":   round(self.tp_mult / self.sl_mult, 2),
        }

    def format_signal(self, sig: Dict[str, Any]) -> str:
        return (
            f"\n{'='*60}\n"
            f"  LONDON BREAKOUT SIGNAL — {sig['symbol']}\n"
            f"{'='*60}\n"
            f"  Session   : {sig['session']}\n"
            f"  Asia High : {sig['asia_high']}\n"
            f"  Asia Low  : {sig['asia_low']}\n"
            f"  Range     : {sig['range']} pts\n"
            f"  Buffer    : {sig['buffer']} pts\n"
            f"\n  BUY  Stop : {sig['buy_stop']}\n"
            f"       TP   : {sig['buy_tp']}  (+{round(sig['tp_mult']*sig['range'] if 'tp_mult' in sig else sig['range']*TP_MULT, 2)})\n"
            f"       SL   : {sig['buy_sl']}\n"
            f"\n  SELL Stop : {sig['sell_stop']}\n"
            f"       TP   : {sig['sell_tp']}\n"
            f"       SL   : {sig['sell_sl']}\n"
            f"\n  R:R       : 1:{sig['rr_long']}\n"
            f"{'='*60}\n"
        )


# ---------------------------------------------------------------------------
# Backtester (uses yfinance hourly data)
# ---------------------------------------------------------------------------

def _localize_index(df):
    """Ensure DataFrame index is tz-aware in Jakarta time."""
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    df.index = df.index.tz_convert(JAKARTA_TZ)
    return df


def backtest(start: str = "2025-01-01", end: str = "2026-01-01",
             tp_mult: float = TP_MULT, sl_mult: float = SL_MULT,
             initial_balance: float = 1000.0) -> Dict[str, Any]:
    """
    Backtest London Breakout on GC=F (Gold Futures) hourly data.

    Strategy simulation on daily data:
      - Asia range approximated as day's open range (Low of 07-14h, High of 07-14h)
      - For daily data we approximate: Asia_High = Open + 0.3*(High-Open)
                                        Asia_Low  = Open - 0.3*(Open-Low)
    Returns a metrics dict.
    """
    if not HAS_YFINANCE:
        print("yfinance not installed. Run: pip install yfinance pandas")
        sys.exit(1)

    print(f"[London Breakout Backtest] Downloading {YF_TICKER} {start} → {end} ...")
    ticker = yf.Ticker(YF_TICKER)
    df = ticker.history(start=start, end=end, interval="1h")

    if df.empty:
        print("No data downloaded!")
        sys.exit(1)

    df = _localize_index(df)
    print(f"Downloaded {len(df)} hourly bars")

    strat    = LondonBreakoutStrategy(tp_mult=tp_mult, sl_mult=sl_mult)
    trades   = []
    balance  = initial_balance
    peak_bal = initial_balance

    # Group by date
    dates = sorted(set(df.index.date))

    for day in dates:
        day_data = df[df.index.date == day]

        # --- Asia range (07:00–15:00 WIB bars) ---
        asia = day_data[
            (day_data.index.time >= ASIA_START) &
            (day_data.index.time < LONDON_START)
        ]
        if asia.empty:
            continue

        asia_high = float(asia["High"].max())
        asia_low  = float(asia["Low"].min())
        range_pts = asia_high - asia_low
        if range_pts <= 0:
            continue

        sig = strat.generate_signal(asia_high, asia_low)

        # --- London session bars (15:00–17:00 WIB) ---
        london = day_data[
            (day_data.index.time >= LONDON_START) &
            (day_data.index.time < LONDON_END)
        ]
        if london.empty:
            continue

        # Simulate: check if buy_stop or sell_stop triggered
        triggered = None
        entry_price = None
        direction   = None

        for _, bar in london.iterrows():
            if triggered is None:
                if bar["High"] >= sig["buy_stop"]:
                    triggered   = "BUY"
                    entry_price = sig["buy_stop"]
                    tp_price    = sig["buy_tp"]
                    sl_price    = sig["buy_sl"]
                    direction   = 1
                elif bar["Low"] <= sig["sell_stop"]:
                    triggered   = "SELL"
                    entry_price = sig["sell_stop"]
                    tp_price    = sig["sell_tp"]
                    sl_price    = sig["sell_sl"]
                    direction   = -1
                continue

            # Check TP/SL
            if direction == 1:
                if bar["High"] >= tp_price:
                    pnl_pts = tp_price - entry_price
                    win     = True
                    break
                elif bar["Low"] <= sl_price:
                    pnl_pts = sl_price - entry_price
                    win     = False
                    break
            else:
                if bar["Low"] <= tp_price:
                    pnl_pts = entry_price - tp_price
                    win     = True
                    break
                elif bar["High"] >= sl_price:
                    pnl_pts = entry_price - sl_price
                    win     = False
                    break
        else:
            if triggered and entry_price:
                # Session ended — exit at last close
                last_close = float(london.iloc[-1]["Close"])
                pnl_pts    = direction * (last_close - entry_price)
                win        = pnl_pts > 0
            else:
                continue   # No trigger today

        # PnL in USD (1 lot XAUUSD = $100/pt, using 0.01 lot → $1/pt for $1k account)
        lot_size = balance * 0.01 / (sl_mult * range_pts * 100 + 1e-9)
        lot_size = max(0.01, round(lot_size, 2))
        pnl_usd  = round(pnl_pts * 100 * lot_size, 2)  # rough P&L

        balance  += pnl_usd
        peak_bal  = max(peak_bal, balance)

        trades.append({
            "date":        day.isoformat(),
            "direction":   triggered,
            "entry":       round(entry_price, 2),
            "range":       round(range_pts, 2),
            "pnl_usd":     pnl_usd,
            "win":         win,
        })

    return _calc_metrics(trades, initial_balance, balance, peak_bal,
                         "London Breakout (15:00-17:00 WIB)")


def _calc_metrics(trades, initial_balance, final_balance, peak_bal, label):
    if not trades:
        return {"label": label, "total_trades": 0}

    wins   = [t for t in trades if t["win"]]
    losses = [t for t in trades if not t["win"]]
    pnls   = [t["pnl_usd"] for t in trades]
    gross_profit = sum(p for p in pnls if p > 0)
    gross_loss   = abs(sum(p for p in pnls if p < 0))
    pf = gross_profit / gross_loss if gross_loss > 0 else float("inf")
    max_dd = round(peak_bal - final_balance, 2)
    max_dd_pct = round(max_dd / initial_balance * 100, 2)

    return {
        "label":           label,
        "total_trades":    len(trades),
        "wins":            len(wins),
        "losses":          len(losses),
        "win_rate":        round(len(wins) / len(trades) * 100, 1),
        "net_pnl":         round(sum(pnls), 2),
        "gross_profit":    round(gross_profit, 2),
        "gross_loss":      round(-gross_loss, 2),
        "profit_factor":   round(pf, 2),
        "avg_win":         round(gross_profit / len(wins), 2) if wins else 0,
        "avg_loss":        round(-gross_loss / len(losses), 2) if losses else 0,
        "max_drawdown":    max_dd,
        "max_drawdown_pct": max_dd_pct,
        "initial_balance": initial_balance,
        "final_balance":   round(final_balance, 2),
        "return_pct":      round((final_balance - initial_balance) / initial_balance * 100, 2),
    }


def print_metrics(m: Dict[str, Any]):
    print()
    print("=" * 60)
    print(f"  {m['label']}")
    print("=" * 60)
    print(f"  Total Trades    : {m['total_trades']}")
    print(f"  Win Rate        : {m.get('win_rate', 0):.1f}%  ({m.get('wins',0)}W / {m.get('losses',0)}L)")
    print(f"  Profit Factor   : {m.get('profit_factor', 0):.2f}")
    print("-" * 60)
    print(f"  Initial Balance : ${m.get('initial_balance', 0):,.2f}")
    print(f"  Final Balance   : ${m.get('final_balance', 0):,.2f}")
    print(f"  Net PnL         : ${m.get('net_pnl', 0):,.2f}  ({m.get('return_pct', 0):+.2f}%)")
    print(f"  Max Drawdown    : ${m.get('max_drawdown', 0):,.2f}  ({m.get('max_drawdown_pct', 0):.2f}%)")
    print(f"  Avg Win         : ${m.get('avg_win', 0):,.2f}")
    print(f"  Avg Loss        : ${m.get('avg_loss', 0):,.2f}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="London Breakout Strategy")
    parser.add_argument("--backtest",   action="store_true")
    parser.add_argument("--start",      default="2025-01-01")
    parser.add_argument("--end",        default="2026-01-01")
    parser.add_argument("--balance",    type=float, default=1000.0)
    parser.add_argument("--tp",         type=float, default=TP_MULT,
                        help="TP multiplier of range (default 1.5)")
    parser.add_argument("--sl",         type=float, default=SL_MULT,
                        help="SL multiplier of range (default 0.5)")
    args = parser.parse_args()

    if args.backtest:
        metrics = backtest(args.start, args.end, args.tp, args.sl, args.balance)
        print_metrics(metrics)
        return metrics

    # Interactive signal preview
    print("London Breakout — signal preview mode")
    print("Provide Asia session high/low:")
    try:
        asia_high = float(input("  Asia High: "))
        asia_low  = float(input("  Asia Low : "))
    except (ValueError, EOFError):
        print("Invalid input")
        sys.exit(1)

    strat = LondonBreakoutStrategy()
    sig   = strat.generate_signal(asia_high, asia_low)
    print(strat.format_signal(sig))


if __name__ == "__main__":
    main()
