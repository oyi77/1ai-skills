#!/usr/bin/env python3
"""
BerkahKarya — New York Open Momentum Strategy
==============================================
Session  : 20:30 – 22:00 Jakarta (WIB / UTC+7)
           ≡ 13:30 – 15:00 New York (ET)

Logic:
  1. Wait for the NY open at 20:30 WIB.
  2. Observe the FIRST 15-minute candle that CLOSES after 20:30 WIB
     (i.e. the 20:30 candle).
  3. Determine direction from the candle body:
       Bullish (close > open)  → Long
       Bearish (close < open)  → Short
  4. Entry = close of that first candle.
  5. SL    = opposite end of the candle (low for long / high for short).
  6. TP    = entry ± 2 × (entry − SL)   →  R:R = 2:1
  7. Cancel any untriggered/still-open trade at 22:00 WIB.

Backtest (standalone):
  python ny_momentum.py --backtest --start 2025-01-01 --end 2026-01-01
"""

import argparse
import sys
from datetime import datetime, date, time, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

import pytz

# ---------------------------------------------------------------------------
# Optional: yfinance for backtesting
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
JAKARTA_TZ = pytz.timezone("Asia/Jakarta")
SYMBOL     = "XAUUSD"
YF_TICKER  = "GC=F"

# Session windows (WIB)
NY_OPEN  = time(20, 30)
NY_CLOSE = time(22, 0)

TP_MULT = 2.0    # TP = 2 × (entry-SL)
SL_MULT = 1.0    # SL = 1 × first-candle range


# ---------------------------------------------------------------------------
# Core strategy class
# ---------------------------------------------------------------------------
class NYMomentumStrategy:
    """NY Open Momentum — entry on first 15-min candle direction."""

    def __init__(self, tp_mult: float = TP_MULT, sl_mult: float = SL_MULT):
        self.tp_mult = tp_mult
        self.sl_mult = sl_mult

    def generate_signal(
        self,
        candle_open:  float,
        candle_high:  float,
        candle_low:   float,
        candle_close: float,
        candle_time:  Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Generate NY momentum signal from the first 15-min candle.

        Returns signal dict or None if candle is a doji (no clear direction).
        """
        if candle_close == candle_open:
            return None   # doji — skip

        bullish = candle_close > candle_open
        direction = "LONG" if bullish else "SHORT"

        entry = candle_close

        if bullish:
            sl   = round(candle_low  * self.sl_mult if self.sl_mult == 1.0
                         else candle_low,  2)
            risk = round(entry - sl, 2)
            tp   = round(entry + self.tp_mult * risk, 2)
        else:
            sl   = round(candle_high, 2)
            risk = round(sl - entry, 2)
            tp   = round(entry - self.tp_mult * risk, 2)

        candle_range = round(candle_high - candle_low, 2)

        return {
            "symbol":        SYMBOL,
            "strategy":      "ny_momentum",
            "session":       "20:30-22:00 WIB",
            "candle_time":   candle_time or "20:30 WIB",
            "direction":     direction,
            "candle_open":   round(candle_open,  2),
            "candle_high":   round(candle_high,  2),
            "candle_low":    round(candle_low,   2),
            "candle_close":  round(candle_close, 2),
            "candle_range":  candle_range,
            "entry":         round(entry, 2),
            "sl":            sl,
            "tp":            tp,
            "risk_pts":      round(risk, 2),
            "rr":            round(self.tp_mult / self.sl_mult, 1),
        }

    def format_signal(self, sig: Dict[str, Any]) -> str:
        arrow = "▲ LONG" if sig["direction"] == "LONG" else "▼ SHORT"
        return (
            f"\n{'='*60}\n"
            f"  NY MOMENTUM SIGNAL — {sig['symbol']} {arrow}\n"
            f"{'='*60}\n"
            f"  Session      : {sig['session']}\n"
            f"  Candle Time  : {sig['candle_time']}\n"
            f"  Candle OHLC  : O={sig['candle_open']} H={sig['candle_high']} "
            f"L={sig['candle_low']} C={sig['candle_close']}\n"
            f"  Candle Range : {sig['candle_range']} pts\n"
            f"\n  Entry        : {sig['entry']}\n"
            f"  Stop Loss    : {sig['sl']}  (−{sig['risk_pts']} pts)\n"
            f"  Take Profit  : {sig['tp']}  (+{round(sig['tp_mult'] * sig['risk_pts'] if 'tp_mult' not in sig else sig['rr'] * sig['risk_pts'], 2)} pts)\n"
            f"\n  R:R          : 1:{sig['rr']}\n"
            f"{'='*60}\n"
        )


# ---------------------------------------------------------------------------
# Backtester
# ---------------------------------------------------------------------------

def _localize_index(df):
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    df.index = df.index.tz_convert(JAKARTA_TZ)
    return df


def backtest(start: str = "2025-01-01", end: str = "2026-01-01",
             tp_mult: float = TP_MULT, sl_mult: float = SL_MULT,
             initial_balance: float = 1000.0) -> Dict[str, Any]:
    """
    Backtest NY Momentum on GC=F (Gold Futures) 15-minute data.
    Falls back to hourly if 15m is unavailable.
    """
    if not HAS_YFINANCE:
        print("yfinance not installed. Run: pip install yfinance pandas")
        sys.exit(1)

    ticker = yf.Ticker(YF_TICKER)

    # Try 15-minute bars (yfinance limit: last 60 days for free)
    # For 2025 we use 1h as closest available resolution
    print(f"[NY Momentum Backtest] Downloading {YF_TICKER} {start} → {end} (1h) ...")
    df = ticker.history(start=start, end=end, interval="1h")

    if df.empty:
        print("No data downloaded!")
        sys.exit(1)

    df = _localize_index(df)
    print(f"Downloaded {len(df)} hourly bars (using as 1h candle ≈ first NY hour)")

    strat    = NYMomentumStrategy(tp_mult=tp_mult, sl_mult=sl_mult)
    trades   = []
    balance  = initial_balance
    peak_bal = initial_balance

    dates = sorted(set(df.index.date))

    for day in dates:
        day_data = df[df.index.date == day]

        # --- Find the first candle at/after 20:30 WIB ---
        ny_bars = day_data[day_data.index.time >= NY_OPEN]
        if ny_bars.empty:
            continue

        first_bar = ny_bars.iloc[0]
        o = float(first_bar["Open"])
        h = float(first_bar["High"])
        l = float(first_bar["Low"])
        c = float(first_bar["Close"])

        sig = strat.generate_signal(o, h, l, c,
                                    candle_time=str(first_bar.name.time()))
        if sig is None:
            continue   # doji

        entry  = sig["entry"]
        sl     = sig["sl"]
        tp     = sig["tp"]
        risk   = sig["risk_pts"]
        is_long = sig["direction"] == "LONG"

        if risk <= 0:
            continue

        # Position sizing: 1% risk
        lot_size = (balance * 0.01) / (risk * 100 + 1e-9)
        lot_size = max(0.01, round(lot_size, 2))

        # --- Simulate trade on remaining NY bars ---
        ny_remaining = ny_bars[
            ny_bars.index.time < NY_CLOSE
        ].iloc[1:]   # skip first bar (entry candle)

        win     = None
        pnl_pts = None

        for _, bar in ny_remaining.iterrows():
            b_h = float(bar["High"])
            b_l = float(bar["Low"])

            if is_long:
                if b_h >= tp:
                    pnl_pts = tp - entry
                    win     = True
                    break
                elif b_l <= sl:
                    pnl_pts = sl - entry  # negative
                    win     = False
                    break
            else:
                if b_l <= tp:
                    pnl_pts = entry - tp
                    win     = True
                    break
                elif b_h >= sl:
                    pnl_pts = entry - sl  # negative
                    win     = False
                    break

        if win is None:
            # Session end — exit at last bar's close
            if len(ny_remaining) == 0:
                last_close = c
            else:
                last_close = float(ny_remaining.iloc[-1]["Close"])
            pnl_pts = (last_close - entry) if is_long else (entry - last_close)
            win     = pnl_pts > 0

        pnl_usd = round(pnl_pts * 100 * lot_size, 2)
        balance  += pnl_usd
        peak_bal  = max(peak_bal, balance)

        trades.append({
            "date":      day.isoformat(),
            "direction": sig["direction"],
            "entry":     round(entry, 2),
            "sl":        sl,
            "tp":        tp,
            "pnl_usd":   pnl_usd,
            "win":       win,
        })

    return _calc_metrics(trades, initial_balance, balance, peak_bal,
                         "NY Open Momentum (20:30-22:00 WIB)")


def _calc_metrics(trades, initial_balance, final_balance, peak_bal, label):
    if not trades:
        return {"label": label, "total_trades": 0}

    wins   = [t for t in trades if t["win"]]
    losses = [t for t in trades if not t["win"]]
    pnls   = [t["pnl_usd"] for t in trades]
    gp     = sum(p for p in pnls if p > 0)
    gl     = abs(sum(p for p in pnls if p < 0))
    pf     = gp / gl if gl > 0 else float("inf")
    max_dd     = round(peak_bal - final_balance, 2)
    max_dd_pct = round(max_dd / initial_balance * 100, 2)

    return {
        "label":           label,
        "total_trades":    len(trades),
        "wins":            len(wins),
        "losses":          len(losses),
        "win_rate":        round(len(wins) / len(trades) * 100, 1),
        "net_pnl":         round(sum(pnls), 2),
        "gross_profit":    round(gp, 2),
        "gross_loss":      round(-gl, 2),
        "profit_factor":   round(pf, 2),
        "avg_win":         round(gp / len(wins), 2) if wins else 0,
        "avg_loss":        round(-gl / len(losses), 2) if losses else 0,
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
    parser = argparse.ArgumentParser(description="NY Open Momentum Strategy")
    parser.add_argument("--backtest",   action="store_true")
    parser.add_argument("--start",      default="2025-01-01")
    parser.add_argument("--end",        default="2026-01-01")
    parser.add_argument("--balance",    type=float, default=1000.0)
    parser.add_argument("--tp",         type=float, default=TP_MULT,
                        help="TP multiplier (default 2.0)")
    parser.add_argument("--sl",         type=float, default=SL_MULT,
                        help="SL multiplier (default 1.0)")
    args = parser.parse_args()

    if args.backtest:
        metrics = backtest(args.start, args.end, args.tp, args.sl, args.balance)
        print_metrics(metrics)
        return metrics

    # Interactive signal preview
    print("NY Momentum — signal preview mode")
    print("Provide first 15-min NY candle OHLC:")
    try:
        o = float(input("  Open  : "))
        h = float(input("  High  : "))
        l = float(input("  Low   : "))
        c = float(input("  Close : "))
    except (ValueError, EOFError):
        print("Invalid input")
        sys.exit(1)

    strat = NYMomentumStrategy()
    sig   = strat.generate_signal(o, h, l, c)
    if sig is None:
        print("Doji candle — no signal generated")
    else:
        print(strat.format_signal(sig))


if __name__ == "__main__":
    main()
