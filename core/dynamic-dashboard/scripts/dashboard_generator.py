#!/usr/bin/env python3
"""Dynamic Dashboard Generator - aggregates data from PostBridge, memory, logs, and notes."""
import json, os, sys, re
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]
POSTBRIDGE_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
POSTBRIDGE_BASE = "https://api.postbridge.app/v1"
TODAY = datetime.now().strftime("%Y-%m-%d")


def fetch_postbridge_revenue():
    """Fetch revenue data from PostBridge API."""
    try:
        import urllib.request

        req = urllib.request.Request(
            f"{POSTBRIDGE_BASE}/analytics/revenue",
            headers={"Authorization": f"Bearer {POSTBRIDGE_KEY}"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e), "note": "PostBridge API unreachable"}


def read_memory_today():
    """Read today's memory file."""
    mem_file = WORKSPACE / "memory" / f"{TODAY}.md"
    if mem_file.exists():
        return mem_file.read_text()
    return "No memory entry for today."


def read_cashflow_log():
    """Parse recent cashflow entries."""
    log_file = WORKSPACE / "logs" / "cashflow.log"
    if not log_file.exists():
        return []
    lines = log_file.read_text().strip().split("\n")
    return lines[-20:] if len(lines) > 20 else lines


def read_open_loops():
    """Read open loops / pending items."""
    loops_file = WORKSPACE / "notes" / "open-loops.md"
    if loops_file.exists():
        return loops_file.read_text()
    return "No open loops found."


def read_analytics_log():
    """Read recent analytics entries."""
    log_file = WORKSPACE / "logs" / "analytics.log"
    if not log_file.exists():
        return []
    lines = log_file.read_text().strip().split("\n")
    return lines[-10:] if len(lines) > 10 else lines


def generate_dashboard():
    """Generate the full markdown dashboard."""
    revenue = fetch_postbridge_revenue()
    memory = read_memory_today()
    cashflow = read_cashflow_log()
    open_loops = read_open_loops()
    analytics = read_analytics_log()

    dashboard = f"""# Daily Dashboard — {TODAY}

## Revenue & PostBridge
```json
{json.dumps(revenue, indent=2, default=str)}
```

## Cashflow (Last 20 entries)
```
{chr(10).join(cashflow) if cashflow else "No cashflow data."}
```

## Analytics (Recent)
```
{chr(10).join(analytics) if analytics else "No analytics data."}
```

## Memory — Today
{memory}

## Open Loops
{open_loops}

---
_Generated at {datetime.now().isoformat()}_
"""
    # Save dashboard
    output_dir = WORKSPACE / "notes"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"dashboard-{TODAY}.md"
    output_file.write_text(dashboard)
    return dashboard, str(output_file)


if __name__ == "__main__":
    dashboard, path = generate_dashboard()
    print(f"Dashboard saved to: {path}")
    print("---")
    # Print summary
    lines = dashboard.split("\n")
    for line in lines[:30]:
        print(line)
    if len(lines) > 30:
        print(f"... ({len(lines) - 30} more lines)")
