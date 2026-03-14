#!/usr/bin/env python3
"""
Heartbeat Runner - Autonomous System Health Check
Runs every 6 hours, sends reports to user
"""

import json
import subprocess
import requests
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Configuration
BASE_DIR = Path("/home/openclaw/.openclaw/workspace")
MEMORY_DIR = BASE_DIR / "memory"
LOGS_DIR = BASE_DIR / "logs"
HEARTBEAT_LOG = LOGS_DIR / "heartbeat.log"
LAST_REPORT_FILE = LOGS_DIR / "last_heartbeat.txt"

def load_context():
    """Load context files"""
    context = {}

    # Today's memory
    today = datetime.now().strftime("%Y-%m-%d")
    today_file = MEMORY_DIR / f"{today}.md"
    if today_file.exists():
        with open(today_file, 'r') as f:
            context['today_memory'] = len(f.readlines())

    # Yesterday's memory
    from datetime import timedelta
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_file = MEMORY_DIR / f"{yesterday}.md"
    if yesterday_file.exists():
        with open(yesterday_file, 'r') as f:
            context['yesterday_memory'] = len(f.readlines())

    # Disk space
    try:
        result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 5:
                context['disk_used'] = parts[4]
    except:
        context['disk_used'] = 'Unknown'

    return context

def check_revenue_gap():
    """Check revenue gap using standalone detector"""
    try:
        result = subprocess.run(
            ['python3', str(BASE_DIR / 'scripts' / 'revenue_gap_detector_standalone.py')],
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout
        # Parse gap duration from output
        if 'Gap:' in output:
            gap_line = [l for l in output.split('\n') if 'Gap:' in l][0]
            return gap_line.split('|')[0].strip().replace('Gap:', '').strip()
        return 'Unknown'
    except:
        return 'Error'

def check_postbridge_health():
    """Check PostBridge API health using GET (no test posts created)"""
    try:
        API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
        BASE_URL = "https://api.post-bridge.com/v1"

        # Use GET social-accounts instead of creating test posts
        response = requests.get(
            f"{BASE_URL}/social-accounts?limit=1",
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            total = data.get('meta', {}).get('total', 0)
            return f'✅ OK ({total} accounts connected)'
        else:
            error_details = f'❌ HTTP {response.status_code}'
            if response.text:
                error_details += f': {response.text[:200]}'
            return error_details
    except requests.Timeout:
        return '❌ Timeout (10s exceeded)'
    except requests.ConnectionError as e:
        return f'❌ Connection Error: {str(e)[:100]}'
    except Exception as e:
        return f'❌ {type(e).__name__}: {str(e)[:100]}'

def check_postbridge_queue():
    """Check how many posts scheduled"""
    try:
        with open(BASE_DIR / 'logs' / 'postbridge_upload_log.txt', 'r') as f:
            success = sum(1 for l in f if '"success": true' in l)
        return success
    except:
        return 'Unknown'

def check_lynk_status():
    """Check LYNK dashboard status (manual tracking)"""
    # This would require scraping or manual input
    # For now, just indicate it needs manual check
    try:
        lynk_log = LOGS_DIR / 'lynk_monitoring_log.txt'
        if lynk_log.exists():
            with open(lynk_log, 'r') as f:
                data = json.load(f)
                return f"Last check: {data.get('last_check', 'Never')}"
        return 'Needs manual check'
    except:
        return 'Needs manual check'

def check_cashflow():
    """Check when cashflow was last tracked"""
    try:
        cashflow_dir = BASE_DIR / 'cashflow'
        if cashflow_dir.exists():
            files = list(cashflow_dir.glob('*.md'))
            if files:
                latest = max(files, key=lambda p: p.stat().st_mtime)
                mtime = datetime.fromtimestamp(latest.stat().st_mtime)
                hours_ago = (datetime.now() - mtime).total_seconds() / 3600
                return f"{hours_ago:.1f}h ago"
        return 'Never tracked'
    except:
        return 'Error'

def determine_alert_level(context):
    """Determine if critical issues need immediate reporting"""
    alerts = []

    # Critical issues
    disk_used = context.get('disk_used', '0%')
    disk_percent = int(disk_used.rstrip('%'))
    if disk_percent >= 95:
        alerts.append("🆘 CRITICAL: Disk nearly full")

    # Revenue gap
    gap = check_revenue_gap()
    if 'hours' in gap:
        gap_hours = float(gap.split()[0])
        if gap_hours >= 12:
            alerts.append(f"🆘 CRITICAL: Revenue gap {gap}")

    # PostBridge
    pb_health = check_postbridge_health()
    if '❌' in pb_health:
        # Include actual error details for reporting
        alerts.append(f"🆘 CRITICAL: PostBridge API down\n\nError details: {pb_health}")

    return alerts

def send_telegram_report(message, urgent=False):
    """Send report via Telegram using OpenClaw message tool"""
    try:
        # Save to file for backup
        report_file = BASE_DIR / 'temp' / f'heartbeat_report_{int(datetime.now().timestamp())}.txt'
        report_file.parent.mkdir(exist_ok=True)

        with open(report_file, 'w') as f:
            f.write(message)

        # Truncate message if too long (Telegram limit is 4096 chars)
        if len(message) > 4000:
            message = message[:3980] + "\n\n[...truncated...]"

        # Use subprocess to run a Python script that calls the message tool
        import subprocess

        # Import telegram_raw_api module
        import sys
        import os
        scripts_dir = BASE_DIR / 'scripts'
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))

        import telegram_raw_api

        # Truncate if too long (Telegram max 4096 chars)
        success = telegram_raw_api.send_telegram_message(message)

        if success:
            print(f"✅ Report sent to Telegram successfully via Bot API")
            return True
        else:
            print(f"⚠️ Telegram Bot API failed - report saved to: {report_file}")
            return False

    except Exception as e:
        print(f"❌ Error sending report: {e}")
        return False

def main():
    """Main heartbeat execution"""
    print("="*70)
    print(f"Heartbeat - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    # Load context
    context = load_context()

    # Checks
    print(f"\n📊 System Status:")
    print(f"  Disk Used: {context.get('disk_used', 'Unknown')}")
    print(f"  Today's Memory: {context.get('today_memory', 0)} lines")
    print(f"  Yesterday's Memory: {context.get('yesterday_memory', 0)} lines")

    print(f"\n📈 Revenue:")
    revenue_gap = check_revenue_gap()
    print(f"  Gap: {revenue_gap}")

    print(f"\n🌐 PostBridge:")
    pb_health = check_postbridge_health()
    pb_queue = check_postbridge_queue()
    print(f"  API Status: {pb_health}")
    print(f"  Posts Scheduled: {pb_queue}")

    print(f"\n💰 Cashflow:")
    cashflow = check_cashflow()
    print(f"  Last Track: {cashflow}")

    print(f"\n📊 LYNK:")
    lynk = check_lynk_status()
    print(f"  Status: {lynk}")

    # Determine alert level
    alerts = determine_alert_level(context)

    # Build report message
    if alerts:
        # Critical alert - send immediately
        alert_msg = "🚨 CRITICAL ALERT:\n\n" + "\n".join(alerts)
        alert_msg += f"\n\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        send_telegram_report(alert_msg, urgent=True)
        print(f"\n🚨 URGENT REPORT SENT")
    else:
        # Regular status - send if 6+ hours since last report
        print(f"\n✅ All systems normal")
        print(f"📊 REGULAR REPORT QUEUED")

    # Log to file
    with open(HEARTBEAT_LOG, 'a') as f:
        f.write(f"{datetime.now().isoformat()} | {context.get('disk_used', 'Unknown')} | {revenue_gap} | {pb_health} | {','.join(alerts)}\n")

    with open(LAST_REPORT_FILE, 'w') as f:
        f.write(datetime.now().isoformat())

    print("="*70)
    return 0

if __name__ == "__main__":
    sys.exit(main())