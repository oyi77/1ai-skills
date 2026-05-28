---
name: finance-tracker
description: >
  Real-time P&L tracking, cashflow monitoring, and revenue gap detection for BerkahKarya.
  Use when you need to check financial health, calculate runway, detect revenue droughts,
  run daily P&L reports, or send cashflow alerts to Telegram.
version: 1.0.0
author: Vilona (BerkahKarya AI GM)
tags: [finance, cashflow, pnl, revenue, alerts, berkahkarya]
---

# Finance Tracker — BerkahKarya

> **Mission:** Zero dead hours. Every IDR tracked. Every gap detected.
> Current status: **EMERGENCY MODE** (Bank: IDR 0.37)

---

## 1. Purpose

This skill provides real-time financial intelligence for BerkahKarya's 5 revenue lines.
It answers the critical question at any moment:

- **"Are we making money right now?"**
- **"How many days until we're dead?"**
- **"Which revenue stream is silent and for how long?"**

### Core Functions

| Function | What It Does |
|---|---|
| P&L Tracking | Daily revenue vs burn, by stream |
| Cashflow Monitoring | Bank balance + inflows + outflows |
| Revenue Gap Detection | Hours since last confirmed sale |
| Burn Rate | Daily/weekly/monthly spend rate |
| Runway Calculation | Days of cash left at current burn |
| Telegram Alerts | Push notifications for thresholds |

---

## 2. Revenue Streams

BerkahKarya has **5 active revenue lines**. Track each separately.

| Stream | Source | Tool | Expected Cadence |
|---|---|---|---|
| Affiliate Marketing | LYNK (lynk.id/jendralbot) | Manual + browser | Multiple/day |
| Digital Products | Gumroad (dizzuddi) | Gumroad API / email | On sale |
| Trading (XAUUSD) | Ostium broker | Trading log JSON | Asia session |
| Services | Software House invoices | Manual entry | Weekly |
| Talent Commissions | Talent agency deals | Manual entry | Irregular |

---

## 3. Data Sources

### 3.1 PostBridge API

```
Base URL:  https://api.post-bridge.com/v1
API Key:   REDACTED_ROTATED_CREDENTIAL
Auth:      Bearer token (Authorization: Bearer REDACTED_ROTATED_CREDENTIAL)
Rate Limit: 10 req/sec
```

Used for: Social post performance → correlate content activity with revenue timing.

```bash
# Check post activity (proxy for affiliate link exposure)
curl -s -H "Authorization: Bearer REDACTED_ROTATED_CREDENTIAL" \
  "https://api.post-bridge.com/v1/analytics" | python3 -m json.tool
```

### 3.2 LYNK Dashboard

```
URL:      https://lynk.id/jendralbot
Type:     Manual check (no public API)
Metrics:  Views, clicks, conversions, revenue (IDR)
```

Scrape or manually read: total conversions, revenue per product, daily totals.

### 3.3 Gumroad

```
Account:  dizzuddi
URL:      https://app.gumroad.com/dashboard
API:      https://api.gumroad.com/v2/sales (requires OAuth token)
```

Sales are also notified via email — parse email or check dashboard.

### 3.4 Manual Bank Entries

```
File:     cashflow/daily_entries.md  (or cashflow/YYYY-MM-DD.md)
Format:   See Section 7 below
Current:  IDR 0.37 (as of 2026-03-13 — EMERGENCY)
```

### 3.5 Trading Log

```
File:     .vilona/knowledge/trading/trading_log.json
Format:   JSON array of trade objects
Fields:   date, pair, direction, entry, exit, pnl_pips, pnl_usd, status
```

---

## 4. Key Metrics

### 4.1 Definitions

```
Daily Revenue     = Sum of all stream inflows for calendar day (IDR)
Burn Rate         = Total daily expenses (IDR/day)
Runway Days       = Cash Balance / Burn Rate
Revenue Gap       = Hours since last confirmed revenue event (any stream)
Cashflow Balance  = Actual bank balance + receivables - payables
```

### 4.2 Alert Thresholds

| Metric | Level | Threshold | Action |
|---|---|---|---|
| Revenue Gap | ⚠️ WARNING | > 4 hours | Telegram warning |
| Revenue Gap | 🚨 CRITICAL | > 8 hours | Telegram urgent + checklist |
| Revenue Gap | 🆘 EMERGENCY | > 12 hours | Telegram + immediate action plan |
| Runway | 🆘 EMERGENCY | < 3 days | Immediate escalation |
| Runway | 🚨 CRITICAL | < 7 days | Daily alert |
| Runway | ⚠️ WARNING | < 14 days | Weekly alert |
| Daily Revenue | ⚠️ ZERO DAY | IDR 0 by 18:00 | Push checklist |

### 4.3 Revenue Gap Logic

```python
# Revenue gap = time since LAST confirmed event across ALL streams:
# - LYNK: last conversion timestamp
# - Gumroad: last sale email / API timestamp
# - Trading: last closed profitable trade
# - Services: last invoice paid
# - Talent: last commission received

# If gap > threshold → fire alert
```

---

## 5. Scripts

### 5.1 `scripts/daily_pnl.py`

**Purpose:** Calculate and display today's P&L across all streams.

```python
#!/usr/bin/env python3
"""
BerkahKarya Daily P&L Calculator
Run: python3 scripts/daily_pnl.py
Or:  python3 scripts/daily_pnl.py --date 2026-03-13
"""

import json
import os
import sys
import argparse
from datetime import datetime, date
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
TRADING_LOG = WORKSPACE / ".vilona/knowledge/trading/trading_log.json"
CASHFLOW_DIR = WORKSPACE / "cashflow"
MEMORY_DIR = WORKSPACE / "memory"

# ─── Revenue Stream Readers ───────────────────────────────────────────────────

def read_trading_pnl(target_date: date) -> dict:
    """Read XAUUSD P&L from trading log."""
    if not TRADING_LOG.exists():
        return {"revenue_idr": 0, "trades": 0, "note": "No trading log found"}

    with open(TRADING_LOG) as f:
        trades = json.load(f)

    day_trades = [
        t for t in trades
        if t.get("date", "").startswith(str(target_date))
        and t.get("status") == "closed"
    ]

    total_usd = sum(t.get("pnl_usd", 0) for t in day_trades)
    # Convert USD → IDR (approximate rate; update as needed)
    USD_TO_IDR = 16_300
    total_idr = total_usd * USD_TO_IDR

    return {
        "revenue_idr": total_idr,
        "revenue_usd": total_usd,
        "trades": len(day_trades),
        "note": f"{len(day_trades)} trades closed"
    }


def read_manual_cashflow(target_date: date) -> dict:
    """Read manual entries from cashflow/YYYY-MM-DD.md."""
    cf_file = CASHFLOW_DIR / f"{target_date}.md"
    if not cf_file.exists():
        # Try daily_entries.md
        cf_file = CASHFLOW_DIR / "daily_entries.md"

    if not cf_file.exists():
        return {"revenue_idr": 0, "expenses_idr": 0, "note": "No cashflow file"}

    content = cf_file.read_text()
    # Parse simple key:value format
    revenue = 0
    expenses = 0
    for line in content.splitlines():
        if "revenue" in line.lower() and ":" in line:
            try:
                val = line.split(":")[-1].strip().replace("IDR", "").replace(",", "").strip()
                revenue += float(val)
            except ValueError:
                pass
        if "expense" in line.lower() and ":" in line:
            try:
                val = line.split(":")[-1].strip().replace("IDR", "").replace(",", "").strip()
                expenses += float(val)
            except ValueError:
                pass

    return {"revenue_idr": revenue, "expenses_idr": expenses, "note": "Manual entry"}


def read_memory_revenue(target_date: date) -> dict:
    """Extract revenue mentions from daily memory file."""
    mem_file = MEMORY_DIR / f"{target_date}.md"
    if not mem_file.exists():
        return {"revenue_idr": 0, "note": "No memory file"}

    content = mem_file.read_text()
    # Look for revenue patterns like "IDR 150,000" or "Rp 75.000"
    import re
    pattern = r'(?:IDR|Rp)\s*([\d,\.]+)'
    matches = re.findall(pattern, content, re.IGNORECASE)
    # Heuristic: sum only if explicitly tagged as revenue
    return {"revenue_idr": 0, "raw_mentions": matches, "note": "Memory scan (manual verify)"}


# ─── P&L Report ───────────────────────────────────────────────────────────────

def generate_pnl_report(target_date: date) -> dict:
    trading = read_trading_pnl(target_date)
    manual = read_manual_cashflow(target_date)
    memory = read_memory_revenue(target_date)

    streams = {
        "Affiliate (LYNK)":    {"revenue": 0, "note": "Manual check required → lynk.id/jendralbot"},
        "Digital (Gumroad)":   {"revenue": 0, "note": "Manual check required → app.gumroad.com"},
        "Trading (XAUUSD)":    {"revenue": trading["revenue_idr"], "note": trading["note"]},
        "Services (SoftHouse)":{"revenue": manual.get("revenue_idr", 0), "note": manual["note"]},
        "Talent Commissions":  {"revenue": 0, "note": "Manual check required"},
    }

    total_revenue = sum(s["revenue"] for s in streams.values())
    total_expenses = manual.get("expenses_idr", 0)
    net_pnl = total_revenue - total_expenses

    return {
        "date": str(target_date),
        "streams": streams,
        "total_revenue_idr": total_revenue,
        "total_expenses_idr": total_expenses,
        "net_pnl_idr": net_pnl,
        "generated_at": datetime.now().isoformat(),
    }


def print_pnl_table(report: dict):
    """Print ASCII table P&L report."""
    date_str = report["date"]
    print(f"\n{'═'*60}")
    print(f"  💰 BERKAHKARYA DAILY P&L — {date_str}")
    print(f"{'═'*60}")
    print(f"  {'Stream':<25} {'Revenue (IDR)':>15}  Note")
    print(f"  {'─'*25} {'─'*15}  {'─'*15}")

    for stream, data in report["streams"].items():
        rev = f"{data['revenue']:>15,.0f}" if data['revenue'] > 0 else f"{'—':>15}"
        note = data['note'][:20]
        print(f"  {stream:<25} {rev}  {note}")

    print(f"  {'─'*25} {'─'*15}")
    print(f"  {'TOTAL REVENUE':<25} {report['total_revenue_idr']:>15,.0f}")
    print(f"  {'TOTAL EXPENSES':<25} {report['total_expenses_idr']:>15,.0f}")

    net = report['net_pnl_idr']
    net_str = f"{net:>15,.0f}"
    net_icon = "✅" if net >= 0 else "🔴"
    print(f"  {'NET P&L':<25} {net_str}  {net_icon}")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BerkahKarya Daily P&L")
    parser.add_argument("--date", default=str(date.today()), help="Date YYYY-MM-DD")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    target = date.fromisoformat(args.date)
    report = generate_pnl_report(target)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_pnl_table(report)
```

---

### 5.2 `scripts/cashflow_dashboard.py`

**Purpose:** Terminal dashboard showing real-time cashflow, runway, and stream status.

```python
#!/usr/bin/env python3
"""
BerkahKarya Cashflow Dashboard
Run: python3 scripts/cashflow_dashboard.py
Run (watch mode): watch -n 300 python3 scripts/cashflow_dashboard.py
"""

import json
import os
from datetime import datetime, date, timedelta
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
CASHFLOW_DIR = WORKSPACE / "cashflow"

# ─── Config ───────────────────────────────────────────────────────────────────

# Update these daily (or automate via bank scraping)
BANK_BALANCE_IDR = 0.37       # Current actual balance — UPDATE DAILY
DAILY_BURN_RATE_IDR = 50_000  # Conservative estimate — UPDATE MONTHLY

# Revenue targets (IDR/day)
TARGETS = {
    "Affiliate (LYNK)":     150_000,
    "Digital (Gumroad)":     75_000,
    "Trading (XAUUSD)":     100_000,
    "Services":              50_000,
    "Talent":                25_000,
}

# ─── Dashboard ────────────────────────────────────────────────────────────────

def calculate_runway(balance: float, burn_rate: float) -> float:
    if burn_rate <= 0:
        return float('inf')
    return balance / burn_rate


def get_runway_status(days: float) -> tuple[str, str]:
    if days < 3:
        return "🆘 EMERGENCY", "< 3 days"
    elif days < 7:
        return "🚨 CRITICAL", f"{days:.1f} days"
    elif days < 14:
        return "⚠️  WARNING", f"{days:.1f} days"
    else:
        return "✅ STABLE", f"{days:.1f} days"


def format_idr(amount: float) -> str:
    if amount >= 1_000_000:
        return f"Rp {amount/1_000_000:.2f}M"
    elif amount >= 1_000:
        return f"Rp {amount/1_000:.1f}K"
    else:
        return f"Rp {amount:.2f}"


def load_last_revenue_time() -> dict:
    """Load last known revenue event times per stream."""
    tracker_file = WORKSPACE / "cashflow" / "last_revenue.json"
    if tracker_file.exists():
        with open(tracker_file) as f:
            return json.load(f)
    # Defaults — update when revenue is confirmed
    return {
        "Affiliate (LYNK)":     None,
        "Digital (Gumroad)":    None,
        "Trading (XAUUSD)":     None,
        "Services":             None,
        "Talent":               None,
    }


def get_gap_hours(last_time_str: str | None) -> float | None:
    if not last_time_str:
        return None
    try:
        last_time = datetime.fromisoformat(last_time_str)
        delta = datetime.now() - last_time
        return delta.total_seconds() / 3600
    except Exception:
        return None


def gap_status(hours: float | None) -> str:
    if hours is None:
        return "❓ UNKNOWN"
    elif hours > 12:
        return f"🆘 {hours:.1f}h"
    elif hours > 8:
        return f"🚨 {hours:.1f}h"
    elif hours > 4:
        return f"⚠️  {hours:.1f}h"
    else:
        return f"✅ {hours:.1f}h"


def print_dashboard():
    now = datetime.now()
    runway_days = calculate_runway(BANK_BALANCE_IDR, DAILY_BURN_RATE_IDR)
    runway_label, runway_str = get_runway_status(runway_days)
    last_revenue = load_last_revenue_time()

    print(f"\n{'╔'+'═'*58+'╗'}")
    print(f"║{'  🏦 BERKAHKARYA CASHFLOW DASHBOARD':^58}║")
    print(f"║{'  ' + now.strftime('%Y-%m-%d %H:%M') + ' WIB':^58}║")
    print(f"{'╠'+'═'*58+'╣'}")

    # Cashflow summary
    print(f"║  {'CASHFLOW SUMMARY':^54}  ║")
    print(f"╠{'═'*58}╣")
    print(f"║  {'Bank Balance':<30} {format_idr(BANK_BALANCE_IDR):>22}  ║")
    print(f"║  {'Daily Burn Rate':<30} {format_idr(DAILY_BURN_RATE_IDR):>22}  ║")
    print(f"║  {'Runway':<30} {runway_str:>22}  ║")
    print(f"║  {'Status':<30} {runway_label:>22}  ║")

    print(f"╠{'═'*58}╣")
    print(f"║  {'REVENUE STREAMS — GAP TRACKER':^54}  ║")
    print(f"╠{'═'*58}╣")
    print(f"║  {'Stream':<28} {'Target/Day':>12} {'Gap':>14}  ║")
    print(f"║  {'─'*28} {'─'*12} {'─'*14}  ║")

    for stream, target in TARGETS.items():
        last_t = last_revenue.get(stream)
        gap_h = get_gap_hours(last_t)
        gap_s = gap_status(gap_h)
        tgt_s = format_idr(target)
        print(f"║  {stream:<28} {tgt_s:>12} {gap_s:>14}  ║")

    print(f"╠{'═'*58}╣")
    print(f"║  {'ALERT THRESHOLDS':^54}  ║")
    print(f"╠{'═'*58}╣")
    print(f"║  ⚠️  WARNING  : Revenue gap > 4h                        ║")
    print(f"║  🚨 CRITICAL : Revenue gap > 8h                        ║")
    print(f"║  🆘 EMERGENCY: Revenue gap > 12h | Runway < 3 days     ║")
    print(f"╠{'═'*58}╣")
    print(f"║  {'QUICK ACTIONS':^54}  ║")
    print(f"╠{'═'*58}╣")
    print(f"║  1. Check LYNK:   lynk.id/jendralbot                   ║")
    print(f"║  2. Check Gumroad: app.gumroad.com (dizzuddi)          ║")
    print(f"║  3. Check Trading: .vilona/knowledge/trading/           ║")
    print(f"║  4. Run alert:    python3 scripts/revenue_alert.py      ║")
    print(f"╚{'═'*58}╝\n")


if __name__ == "__main__":
    print_dashboard()
```

---

### 5.3 `scripts/revenue_alert.py`

**Purpose:** Check revenue gaps and fire Telegram alerts when thresholds are breached.

```python
#!/usr/bin/env python3
"""
BerkahKarya Revenue Alert System
Run: python3 scripts/revenue_alert.py
Cron: */120 * * * * python3 /path/to/scripts/revenue_alert.py

Exit codes:
  0 = OK (all gaps within thresholds)
  1 = WARNING (gap > 4h)
  2 = CRITICAL/EMERGENCY (gap > 8h or > 12h)
  3 = ERROR
"""

import json
import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent

# ─── Config ───────────────────────────────────────────────────────────────────

ALERT_THRESHOLDS = {
    "WARNING":   4,   # hours
    "CRITICAL":  8,
    "EMERGENCY": 12,
}

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID", "5220170786")  # Coder $String$

LAST_REVENUE_FILE = WORKSPACE / "cashflow" / "last_revenue.json"
LOG_FILE          = WORKSPACE / "logs" / "revenue_alerts.log"

# ─── Telegram ─────────────────────────────────────────────────────────────────

def send_telegram(message: str) -> bool:
    """Send alert via Telegram (uses openclaw message tool via CLI)."""
    try:
        # Method 1: via openclaw CLI (preferred — uses existing telegram config)
        result = subprocess.run(
            ["openclaw", "message", "send",
             "--channel", "telegram",
             "--target", TELEGRAM_CHAT_ID,
             "--message", message],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            return True

        # Method 2: direct Bot API (fallback)
        if TELEGRAM_BOT_TOKEN:
            import urllib.request
            import urllib.parse
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = urllib.parse.urlencode({
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML"
            }).encode()
            req = urllib.request.Request(url, data=data)
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status == 200

    except Exception as e:
        log(f"Telegram send failed: {e}")
    return False


# ─── Gap Detection ────────────────────────────────────────────────────────────

def load_last_revenue() -> dict:
    if LAST_REVENUE_FILE.exists():
        with open(LAST_REVENUE_FILE) as f:
            return json.load(f)
    return {}


def get_global_gap() -> tuple[float, str]:
    """Return (hours_since_last_revenue, source_stream)."""
    last_revenue = load_last_revenue()

    if not last_revenue:
        # No data — treat as worst case (12h)
        return 12.0, "no_data"

    most_recent = None
    most_recent_stream = "unknown"

    for stream, timestamp in last_revenue.items():
        if not timestamp:
            continue
        try:
            t = datetime.fromisoformat(timestamp)
            if most_recent is None or t > most_recent:
                most_recent = t
                most_recent_stream = stream
        except Exception:
            continue

    if most_recent is None:
        return 12.0, "no_timestamps"

    gap_hours = (datetime.now() - most_recent).total_seconds() / 3600
    return gap_hours, most_recent_stream


def determine_level(gap_hours: float) -> str:
    if gap_hours >= ALERT_THRESHOLDS["EMERGENCY"]:
        return "EMERGENCY"
    elif gap_hours >= ALERT_THRESHOLDS["CRITICAL"]:
        return "CRITICAL"
    elif gap_hours >= ALERT_THRESHOLDS["WARNING"]:
        return "WARNING"
    return "OK"


# ─── Alert Messages ───────────────────────────────────────────────────────────

def build_alert_message(level: str, gap_hours: float, source: str) -> str:
    now = datetime.now().strftime("%H:%M WIB")
    gap_str = f"{gap_hours:.1f}h"

    if level == "EMERGENCY":
        return (
            f"🆘 <b>EMERGENCY — REVENUE DROUGHT</b>\n\n"
            f"⏰ Gap: <b>{gap_str}</b> since last sale\n"
            f"📍 Last stream: {source}\n"
            f"🕐 Time: {now}\n\n"
            f"<b>IMMEDIATE ACTIONS:</b>\n"
            f"1. Post 3x on TikTok NOW (LYNK links)\n"
            f"2. DM top 5 prospects (Software House)\n"
            f"3. Check Gumroad: app.gumroad.com\n"
            f"4. Review trading setup for Asia session\n\n"
            f"<code>python3 scripts/cashflow_dashboard.py</code>"
        )
    elif level == "CRITICAL":
        return (
            f"🚨 <b>CRITICAL — Revenue gap {gap_str}</b>\n\n"
            f"📍 Last: {source} | {now}\n\n"
            f"Actions:\n"
            f"• Post LYNK content now\n"
            f"• Check Gumroad dashboard\n"
            f"• Review open deals"
        )
    elif level == "WARNING":
        return (
            f"⚠️ <b>WARNING — Revenue gap {gap_str}</b>\n"
            f"📍 Last: {source} | {now}\n"
            f"→ Check all 5 streams now."
        )
    return ""


def build_daily_report(period: str = "morning") -> str:
    """Build 9AM or 9PM daily summary report."""
    gap_hours, source = get_global_gap()
    level = determine_level(gap_hours)

    icon = "🌅" if period == "morning" else "🌙"
    now = datetime.now().strftime("%Y-%m-%d %H:%M WIB")

    # Load revenue data (simplified — extend with actual stream data)
    last_revenue = load_last_revenue()
    stream_lines = []
    for stream, ts in last_revenue.items():
        if ts:
            t = datetime.fromisoformat(ts)
            hrs = (datetime.now() - t).total_seconds() / 3600
            stream_lines.append(f"  • {stream}: {hrs:.1f}h ago")
        else:
            stream_lines.append(f"  • {stream}: No data")

    streams_str = "\n".join(stream_lines) if stream_lines else "  No data"

    return (
        f"{icon} <b>BerkahKarya {'Morning' if period == 'morning' else 'Evening'} Report</b>\n"
        f"📅 {now}\n\n"
        f"💰 Revenue Status: <b>{level}</b>\n"
        f"⏱ Global Gap: {gap_hours:.1f}h (last: {source})\n\n"
        f"📊 Stream Status:\n{streams_str}\n\n"
        f"<code>python3 scripts/daily_pnl.py</code>\n"
        f"<code>python3 scripts/cashflow_dashboard.py</code>"
    )


# ─── Logging ──────────────────────────────────────────────────────────────────

def log(message: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = f"[{datetime.now().isoformat()}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)
    print(entry.strip())


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="BerkahKarya Revenue Alert")
    parser.add_argument("--daily-report", choices=["morning", "evening"],
                        help="Send daily summary report")
    parser.add_argument("--record", metavar="STREAM",
                        help="Record revenue event for stream (updates last_revenue.json)")
    args = parser.parse_args()

    # Record revenue event
    if args.record:
        LAST_REVENUE_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = load_last_revenue()
        data[args.record] = datetime.now().isoformat()
        with open(LAST_REVENUE_FILE, "w") as f:
            json.dump(data, f, indent=2)
        log(f"Revenue recorded: {args.record} at {data[args.record]}")
        sys.exit(0)

    # Daily report
    if args.daily_report:
        msg = build_daily_report(args.daily_report)
        sent = send_telegram(msg)
        log(f"Daily {args.daily_report} report {'sent' if sent else 'FAILED'}")
        sys.exit(0 if sent else 3)

    # Gap check
    gap_hours, source = get_global_gap()
    level = determine_level(gap_hours)
    log(f"Gap: {gap_hours:.1f}h | Source: {source} | Level: {level}")

    if level == "OK":
        sys.exit(0)

    msg = build_alert_message(level, gap_hours, source)
    sent = send_telegram(msg)
    log(f"Alert [{level}] {'sent' if sent else 'FAILED'}: {gap_hours:.1f}h gap")

    sys.exit(2 if level in ("CRITICAL", "EMERGENCY") else 1)


if __name__ == "__main__":
    main()
```

---

## 6. Cashflow Data Format

### Manual Bank Entry File

**Path:** `cashflow/YYYY-MM-DD.md`

```markdown
# Cashflow — 2026-03-13

## Bank Balance
Start:  IDR 0.37
End:    IDR ________

## Revenue
Affiliate (LYNK):    IDR ________
Digital (Gumroad):   IDR ________
Trading (XAUUSD):    IDR ________
Services:            IDR ________
Talent:              IDR ________
TOTAL REVENUE:       IDR ________

## Expenses
Item 1:              IDR ________
Item 2:              IDR ________
TOTAL EXPENSES:      IDR ________

## Net P&L
Net: IDR ________

## Notes
- 
```

### Last Revenue Tracker

**Path:** `cashflow/last_revenue.json`

```json
{
  "Affiliate (LYNK)":     "2026-03-13T09:30:00",
  "Digital (Gumroad)":    null,
  "Trading (XAUUSD)":     "2026-03-12T18:45:00",
  "Services":             null,
  "Talent":               null
}
```

Update this file **every time a sale is confirmed** using:

```bash
python3 scripts/revenue_alert.py --record "Affiliate (LYNK)"
python3 scripts/revenue_alert.py --record "Digital (Gumroad)"
python3 scripts/revenue_alert.py --record "Trading (XAUUSD)"
```

---

## 7. Telegram Integration

### Alert Delivery Method

Alerts are sent via the **openclaw telegram channel** (already configured). No separate bot required.

The `revenue_alert.py` script uses:
1. **Primary:** `openclaw message send` CLI → uses existing Telegram session
2. **Fallback:** Direct Bot API (set `TELEGRAM_BOT_TOKEN` env var)

### Environment Variables (Optional)

```bash
# ~/.bashrc or ~/.zshrc
export TELEGRAM_CHAT_ID="5220170786"       # Coder $String$ Telegram ID
export TELEGRAM_BOT_TOKEN="your_bot_token" # Only needed for fallback
```

### Alert Format Examples

**WARNING (4h gap):**
```
⚠️ WARNING — Revenue gap 4.2h
📍 Last: Affiliate (LYNK) | 14:30 WIB
→ Check all 5 streams now.
```

**CRITICAL (8h gap):**
```
🚨 CRITICAL — Revenue gap 8.5h

📍 Last: Trading (XAUUSD) | 14:30 WIB

Actions:
• Post LYNK content now
• Check Gumroad dashboard
• Review open deals
```

**EMERGENCY (12h gap):**
```
🆘 EMERGENCY — REVENUE DROUGHT

⏰ Gap: 13.2h since last sale
📍 Last stream: Gumroad
🕐 Time: 22:15 WIB

IMMEDIATE ACTIONS:
1. Post 3x on TikTok NOW (LYNK links)
2. DM top 5 prospects (Software House)
3. Check Gumroad: app.gumroad.com
4. Review trading setup for Asia session
```

---

## 8. Cron Schedule

Add to crontab with `crontab -e`:

```cron
# ──────────────────────────────────────────────────────────────────────────────
# BerkahKarya Finance Tracker
# ──────────────────────────────────────────────────────────────────────────────

# Every 2 hours: Revenue gap check + alerts
0 */2 * * * cd /home/openclaw/.openclaw/workspace && python3 scripts/revenue_alert.py >> logs/revenue_alerts_cron.log 2>&1

# 9:00 AM WIB: Morning daily report
0 9 * * * cd /home/openclaw/.openclaw/workspace && python3 scripts/revenue_alert.py --daily-report morning >> logs/revenue_alerts_cron.log 2>&1

# 9:00 PM WIB: Evening daily report + P&L summary
0 21 * * * cd /home/openclaw/.openclaw/workspace && python3 scripts/daily_pnl.py >> logs/pnl_cron.log 2>&1 && python3 scripts/revenue_alert.py --daily-report evening >> logs/revenue_alerts_cron.log 2>&1

# Midnight: Cashflow dashboard snapshot to log
0 0 * * * cd /home/openclaw/.openclaw/workspace && python3 scripts/cashflow_dashboard.py >> logs/cashflow_snapshots.log 2>&1
```

**Install cron:**
```bash
cd /home/openclaw/.openclaw/workspace
# Preview current crontab
crontab -l

# Add finance tracker jobs
(crontab -l 2>/dev/null; cat << 'EOF'

# BerkahKarya Finance Tracker
0 */2 * * * cd /home/openclaw/.openclaw/workspace && python3 scripts/revenue_alert.py >> logs/revenue_alerts_cron.log 2>&1
0 9 * * * cd /home/openclaw/.openclaw/workspace && python3 scripts/revenue_alert.py --daily-report morning >> logs/revenue_alerts_cron.log 2>&1
0 21 * * * cd /home/openclaw/.openclaw/workspace && python3 scripts/daily_pnl.py >> logs/pnl_cron.log 2>&1 && python3 scripts/revenue_alert.py --daily-report evening >> logs/revenue_alerts_cron.log 2>&1
EOF
) | crontab -
```

---

## 9. Quick Reference

### Daily Workflow

```bash
# Morning check (after 9AM report)
python3 scripts/cashflow_dashboard.py   # Overview
python3 scripts/daily_pnl.py           # Yesterday's numbers

# After confirmed sale
python3 scripts/revenue_alert.py --record "Affiliate (LYNK)"

# Manual trigger alert check
python3 scripts/revenue_alert.py

# End of day P&L
python3 scripts/daily_pnl.py --date $(date +%Y-%m-%d)
```

### File Locations

```
skills/1ai-skills/finance/finance-tracker/
├── SKILL.md                     ← This file
└── scripts/
    ├── daily_pnl.py             ← P&L calculator
    ├── cashflow_dashboard.py    ← Terminal dashboard
    └── revenue_alert.py         ← Gap detector + Telegram alerts

cashflow/
├── YYYY-MM-DD.md               ← Daily bank entries
└── last_revenue.json           ← Last sale timestamps per stream

logs/
├── revenue_alerts.log          ← Alert history
├── revenue_alerts_cron.log     ← Cron run log
├── pnl_cron.log                ← P&L cron log
└── cashflow_snapshots.log      ← Midnight snapshots
```

### Revenue Stream Checklist (Manual)

| Stream | URL | Check Frequency |
|---|---|---|
| LYNK | https://lynk.id/jendralbot | Every 2-3h |
| Gumroad | https://app.gumroad.com (dizzuddi) | Every 4h |
| Trading | `.vilona/knowledge/trading/trading_log.json` | After Asia session |
| Software House | `cashflow/YYYY-MM-DD.md` | On invoice paid |
| Talent | `cashflow/YYYY-MM-DD.md` | On commission received |

---

## 10. Implementation Checklist

Run this once to bootstrap the system:

```bash
cd /home/openclaw/.openclaw/workspace

# 1. Create directories
mkdir -p cashflow logs

# 2. Copy scripts from this SKILL.md to actual files
#    (or let the agent write them)

# 3. Initialize last_revenue.json
echo '{}' > cashflow/last_revenue.json

# 4. Create today's cashflow file
DATE=$(date +%Y-%m-%d)
cp skills/1ai-skills/finance/finance-tracker/cashflow_template.md cashflow/$DATE.md 2>/dev/null || \
  echo "# Cashflow — $DATE\n\n## Bank Balance\nStart: IDR 0.37\n" > cashflow/$DATE.md

# 5. Test scripts
python3 scripts/cashflow_dashboard.py
python3 scripts/daily_pnl.py
python3 scripts/revenue_alert.py

# 6. Install cron jobs (see Section 8)
crontab -l  # verify

# 7. Test Telegram alert
python3 scripts/revenue_alert.py --daily-report morning
```

---

> **Remember:** IDR 0.37 is not a number. It's a countdown.
> Every hour without revenue is an hour closer to zero.
> Run the alerts. Check the dashboard. Record every sale.
> 🔥 — Vilona, BerkahKarya AI GM
