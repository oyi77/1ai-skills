#!/usr/bin/env python3
"""
Standalone Revenue Gap Detector - Works WITHOUT PostBridge API
Runs locally, checks direct file sources, alerts when gap thresholds exceeded
"""

import json
import os
import sys
from datetime import datetime, timedelta
import glob

# Configuration
CONFIG = {
    "thresholds": {
        "warning_hours": 4,
        "critical_hours": 8,
        "emergency_hours": 12
    },
    "sources": {
        "trading_logs": "/home/openclaw/.openclaw/workspace/.vilona/knowledge/trading/trading_log.json",
        "cashflow_files": "/home/openclaw/.openclaw/workspace/cashflow/*.md",
        "manual_tracking": "/home/openclaw/.openclaw/workspace/memory/revenue_tracking.md"
    },
    "output_file": "/home/openclaw/.openclaw/workspace/logs/revenue_gaps.log"
}

def get_latest_trading_activity():
    """Get latest trading activity from log file"""
    try:
        if os.path.exists(CONFIG["sources"]["trading_logs"]):
            with open(CONFIG["sources"]["trading_logs"], 'r') as f:
                data = json.load(f)
                if data and len(data) > 0:
                    latest = data[-1]
                    return datetime.fromisoformat(latest["timestamp"]), "trade_execution"
    except Exception as e:
        pass
    return None, None

def get_latest_cashflow_activity():
    """Get latest manual cashflow entry"""
    try:
        # Check manual tracking file
        manual_file = CONFIG["sources"]["manual_tracking"]
        if os.path.exists(manual_file):
            mtime = datetime.fromtimestamp(os.path.getmtime(manual_file))
            # Parse date from filename or content
            if mtime:
                return mtime, "manual_cashflow_entry"

        # Check cashflow folder
        files = glob.glob(CONFIG["sources"]["cashflow_files"])
        if files:
            latest_file = max(files, key=os.path.getmtime)
            mtime = datetime.fromtimestamp(os.path.getmtime(latest_file))
            return mtime, "cashflow_file_update"
    except Exception as e:
        pass
    return None, None

def check_memory_files():
    """Check memory files for recent revenue activity notes"""
    memory_dir = "/home/openclaw/.openclaw/workspace/memory"
    try:
        # Check today's memory file
        today = datetime.now().strftime("%Y-%m-%d")
        today_file = os.path.join(memory_dir, f"{today}.md")
        if os.path.exists(today_file):
            mtime = datetime.fromtimestamp(os.path.getmtime(today_file))
            hours_ago = (datetime.now() - mtime).total_seconds() / 3600
            if hours_ago < 2:  # Recent activity
                return mtime, "memory_update"
    except Exception as e:
        pass
    return None, None

def calculate_gap():
    """Calculate revenue gap in hours"""
    # Get latest activity from all sources
    sources = [
        check_memory_files(),
        get_latest_cashflow_activity(),
        get_latest_trading_activity()
    ]

    # Find latest activity
    latest_time = None
    latest_source = None

    for time, source in sources:
        if time and (latest_time is None or time > latest_time):
            latest_time = time
            latest_source = source

    if latest_time:
        gap_hours = (datetime.now() - latest_time).total_seconds() / 3600
        return gap_hours, latest_source
    else:
        # No activity found - assume 24 hours or more
        return 24.0, "no_activity"

def log_alert(gap_hours, source):
    """Log alert to file"""
    # Determine alert level
    thresholds = CONFIG["thresholds"]
    if gap_hours >= thresholds["emergency_hours"]:
        level = "EMERGENCY"
    elif gap_hours >= thresholds["critical_hours"]:
        level = "CRITICAL"
    elif gap_hours >= thresholds["warning_hours"]:
        level = "WARNING"
    else:
        level = "OK"

    # Generate recommendation
    recommendation = generate_recommendation(level)

    # Create alert entry
    alert = {
        "timestamp": datetime.now().isoformat(),
        "gap_hours": round(gap_hours, 1),
        "level": level,
        "last_activity": source if source != "no_activity" else None,
        "source": source if source else "No Activity Detected",
        "recommendation": recommendation,
        "config": thresholds
    }

    # Write to log
    with open(CONFIG["output_file"], 'a') as f:
        f.write(json.dumps(alert) + "\n")
        f.write("-" * 80 + "\n")

    return alert

def generate_recommendation(level):
    """Generate recommendation based on alert level"""
    if level == "EMERGENCY":
        return "🆘 URGENT: All hands on deck - generate revenue NOW\n🆘 Execute all pending marketing content\n🆘 Check bank balance and calculate runway\n🆘 Manual outreach to all leads\n🆘 Review crisis protocols"
    elif level == "CRITICAL":
        return "⚠️ CRITICAL: Revenue gap significant - immediate action required\n⚠️ Execute marketing uploads if blocked\n⚠️ Check cashflow visibility\n⚠️ Monitor for any revenue signals"
    elif level == "WARNING":
        return "⚠️ WARNING: Revenue gap approaching threshold\n⚠️ Check upcoming scheduled tasks\n⚠️ Verify marketing content scheduled"
    else:
        return "✅ Revenue monitoring OK - continue tracking"

def main():
    """Main execution"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running standalone revenue gap detector...")

    # Calculate gap
    gap_hours, source = calculate_gap()

    print(f"Gap: {gap_hours:.1f} hours | Source: {source}")

    # Log alert
    alert = log_alert(gap_hours, source)

    # Print summary
    print(f"Level: {alert['level']}")
    print(f"Last Activity: {source or 'None'}")
    print(f"Recommendation: {alert['recommendation']}")

    # Set exit code based on level
    if alert['level'] == "EMERGENCY" or alert['level'] == "CRITICAL":
        return 2  # Critical
    elif alert['level'] == "WARNING":
        return 1  # Warning
    else:
        return 0  # OK

if __name__ == "__main__":
    sys.exit(main())