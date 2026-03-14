#!/usr/bin/env python3
"""
Cashflow Monitoring - Autonomous
Reminds manual cashflow tracking and alerts if overdue
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path("/home/openclaw/.openclaw/workspace")
CASHFLOW_DIR = BASE_DIR / "cashflow"
ALERT_FILE = BASE_DIR / "temp" / "cashflow_alert.txt"
CHECKPOINT_FILE = BASE_DIR / "temp" / "cashflow_checkpoint.json"

# Tracking schedule
TRACKING_INTERVAL_HOURS = 24  # Should track daily
URGENT_THRESHOLD_HOURS = 48   # Urgent if not tracked for 2 days
EMERGENCY_THRESHOLD_HOURS = 72 # Emergency if not tracked for 3 days

def get_last_cashflow_time():
    """Get when cashflow was last tracked"""
    if not CASHFLOW_DIR.exists():
        CASHFLOW_DIR.mkdir(exist_ok=True)
        return None

    cashflow_files = list(CASHFLOW_DIR.glob('*.md'))
    if not cashflow_files:
        return None

    # Get most recent file
    latest_file = max(cashflow_files, key=lambda p: p.stat().st_mtime)
    mtime = datetime.fromtimestamp(latest_file.stat().st_mtime)

    return mtime

def load_checkpoint():
    """Load tracking checkpoint"""
    try:
        if CHECKPOINT_FILE.exists():
            with open(CHECKPOINT_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return None

def save_checkpoint(data):
    """Save checkpoint"""
    CHECKPOINT_FILE.parent.mkdir(exist_ok=True)
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def analyze_status(last_track_time):
    """Analyze tracking status"""
    if last_track_time is None:
        return {
            'status': 'never',
            'hours_since': None,
            'level': 'emergency',
            'message': 'NEVER TRACKED'
        }

    hours_since = (datetime.now() - last_track_time).total_seconds() / 3600

    if hours_since < TRACKING_INTERVAL_HOURS:
        level = 'ok'
        message = f'Tracked {hours_since:.1f}h ago'
    elif hours_since < URGENT_THRESHOLD_HOURS:
        level = 'warning'
        message = f'Tracked {hours_since:.1f}h ago (should be daily)'
    elif hours_since < EMERGENCY_THRESHOLD_HOURS:
        level = 'urgent'
        message = f'OVERDUE: Tracked {hours_since:.1f}h ago'
    else:
        level = 'emergency'
        message = f'CRITICAL: Never tracked for {hours_since:.0f}h'

    return {
        'status': level,
        'hours_since': hours_since,
        'level': level,
        'message': message
    }

def generate_alert(status):
    """Generate alert based on status"""
    level = status['level']

    if level == 'ok':
        return None

    alert = f"""
📊 CASHFLOW TRACKING ALERT

Status: {status['level'].upper()}
{status['message']}

"""

    if level == 'warning':
        alert += f"""
⚠️ Tracking overdue by {status['hours_since'] - TRACKING_INTERVAL_HOURS:.0f}h

Recommended: Track cashflow today
Location: {CASHFLOW_DIR}/

Template:
Date: {datetime.now().strftime('%Y-%m-%d')}
Cash Balance Start: IDR ________
Revenue Today: Trading IDR ____, Marketing IDR ____
Expenses Today: IDR ________
Cash Balance End: IDR ________
"""
    elif level == 'urgent':
        alert += f"""
🚨 URGENT: Cashflow tracking significantly overdue

Last tracked: {status['hours_since']:.0f}h ago
Standard: Every {TRACKING_INTERVAL_HOURS}h

⚠️  Strategic decisions may be WRONG without current cashflow data

🚨 Action Required IMMEDIATELY:
1. Check ALL bank balances
2. Calculate current runway
3. Update: {CASHFLOW_DIR}/
4. Make decisions based on ACTUAL data
"""
    elif level == 'emergency':
        hours_val = status['hours_since'] if status['hours_since'] else 0
        alert += f"""
🆘 EMERGENCY: CRITICAL cashflow blindness

Never tracked for {hours_val:.0f}h

💥 Business operating BLIND - making decisions without runway data
💥 40%+ strategic decisions may be WRONG
💥 Bankruptcy risk UNKNOWN (could be imminent)

🚨 CRITICAL ACTION REQUIRED NOW:
1. DROP EVERYTHING
2. Check ALL bank balances
3. Calculate runway (weeks to $0)
4. Document: {CASHFLOW_DIR}/
5. NO DECISIONS until cashflow recorded

This is survival priority.
"""

    return alert

def main():
    """Main cashflow monitoring execution"""
    print("="*70)
    print(f"Cashflow Monitoring - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    # Get last tracking time
    last_track = get_last_cashflow_time()

    # Analyze status
    status = analyze_status(last_track)

    print(f"\nStatus: {status['status'].upper()}")

    if status['hours_since']:
        print(f"Last Track: {status['hours_since']:.1f}h ago")
    else:
        print(f"Last Track: Never")

    print(f"Message: {status['message']}")

    # Generate alert if needed
    alert = generate_alert(status)

    if alert:
        # Save alert
        ALERT_FILE.parent.mkdir(exist_ok=True)
        with open(ALERT_FILE, 'w') as f:
            f.write(f"GENERATED: {datetime.now().isoformat()}\n")
            f.write(alert)

        print(f"\n🚨 ALERT GENERATED")
        print(alert)
        print(f"Alert saved: {ALERT_FILE}")

        # Save checkpoint
        save_checkpoint({
            'last_alert': datetime.now().isoformat(),
            'alert_level': status['level'],
            'hours_since': status['hours_since']
        })
    else:
        print(f"\n✅ Cashflow tracking up to date")

        # Save checkpoint
        save_checkpoint({
            'last_check': datetime.now().isoformat(),
            'status': 'ok',
            'hours_since': status['hours_since']
        })

    print("="*70)
    return 0

if __name__ == "__main__":
    main()