#!/usr/bin/env python3
"""
PostBridge API Health Check - Autonomous
Checks PostBridge API status and reports issues
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path("/home/openclaw/.openclaw/workspace")
LOG_FILE = BASE_DIR / "logs" / "postbridge_health_log.txt"

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

def check_api():
    """Check PostBridge API health"""
    status = {
        'timestamp': datetime.now().isoformat(),
        'status': 'unknown',
        'latency_ms': None,
        'error': None
    }

    try:
        # Use GET instead of POST to avoid creating test posts
        start = datetime.now()
        response = requests.get(
            f"{BASE_URL}/social-accounts?limit=1",
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json=test_payload,
            timeout=30
        )
        elapsed = (datetime.now() - start).total_seconds() * 1000

        status['latency_ms'] = round(elapsed, 2)

        if response.status_code in [200, 201]:
            status['status'] = 'ok'
        else:
            status['status'] = 'error'
            status['error'] = f"HTTP {response.status_code}: {response.text[:100]}"

    except requests.Timeout:
        status['status'] = 'error'
        status['error'] = 'Timeout (30s)'
    except Exception as e:
        status['status'] = 'error'
        status['error'] = str(e)[:100]

    return status

def load_health_history():
    """Load previous health checks"""
    try:
        if LOG_FILE.exists():
            with open(LOG_FILE, 'r') as f:
                return json.load(f)
    except:
        pass

    return []

def save_health_check(status):
    """Save health check to log"""
    history = load_health_history()
    history.append(status)

    # Keep last 100 checks
    history = history[-100:]

    LOG_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def analyze_trends(history):
    """Analyze health trends"""
    if len(history) < 2:
        return {
            'error_rate': 0,
            'consecutive_errors': 0,
            'recent_errors': 0,
            'total_checks': len(history),
            'message': 'insufficient_data'
        }

    recent = history[-10:]  # Last 10 checks

    # Count errors
    errors = sum(1 for s in recent if s['status'] == 'error')
    total = len(recent)
    error_rate = errors / total if total > 0 else 0

    # Check for consecutive errors
    consecutive_errors = 0
    for s in reversed(recent):
        if s['status'] == 'error':
            consecutive_errors += 1
        else:
            break

    return {
        'error_rate': error_rate,
        'consecutive_errors': consecutive_errors,
        'recent_errors': errors,
        'total_checks': total,
        'message': 'ok'
    }

def generate_alert(status, trends):
    """Generate alert if needed"""
    if status['status'] == 'error':
        if trends['consecutive_errors'] >= 3:
            return f"""
🚨 CRITICAL: PostBridge API DOWN

Status: {status['status']}
Error: {status['error']}
Consecutive Failures: {trends['consecutive_errors']}
Last Error Time: {status['timestamp']}

🆘 Action Required:
- Check PostBridge Discord: https://discord.gg/ypq3AhPTxf
- Contact support: support@post-bridge.com
- Verify service status page
"""
        else:
            return f"""
⚠️ WARNING: PostBridge API Issue

Status: {status['status']}
Error: {status['error']}
Time: {status['timestamp']}

🔄 Will continue monitoring...
"""

    elif trends['error_rate'] > 0.5:
        return f"""
⚠️ WARNING: High Failure Rate

Recent Failure Rate: {trends['error_rate']*100:.0f}%
Errors: {trends['recent_errors']}/{trends['total_checks']} in last {len(recent)} checks

Monitor closely for service degradation.
"""

    return None

def main():
    """Main health check execution"""
    print("="*70)
    print(f"PostBridge Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    # Check API
    status = check_api()

    # Save to log
    save_health_check(status)

    # Analyze trends
    history = load_health_history()
    trends = analyze_trends(history)

    # Display results
    print(f"\nStatus: {status['status'].upper()}")
    if status['latency_ms']:
        print(f"Latency: {status['latency_ms']}ms")

    if status['status'] == 'error':
        print(f"Error: {status['error']}")

    print(f"\nTrends (Last 10 checks):")
    print(f"  Error Rate: {trends['error_rate']*100:.0f}%")
    print(f"  Consecutive Errors: {trends['consecutive_errors']}")
    print(f"  Total History: {len(history)} checks")

    # Generate alert if needed
    alert = generate_alert(status, trends)
    if alert:
        print(f"\n🚨 ALERT GENERATED")
        print(alert)

        # Save alert to file
        alert_file = BASE_DIR / 'temp' / 'postbridge_alert.txt'
        alert_file.parent.mkdir(exist_ok=True)
        with open(alert_file, 'w') as f:
            f.write(f"GENERATED: {datetime.now().isoformat()}\n")
            f.write(alert)

        print(f"Alert saved: {alert_file}")
    else:
        print(f"\n✅ No alerts - API healthy")

    print("="*70)
    return 0

if __name__ == "__main__":
    main()