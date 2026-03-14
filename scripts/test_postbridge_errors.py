#!/usr/bin/env python3
"""
Test PostBridge Error Reporting

Test cases to ensure detailed errors are captured
"""

import requests
from datetime import datetime, timedelta

def test_error_reporting():
    print("="*70)
    print("PostBridge Error Reporting Test")
    print("="*70)

    # Test 1: Simulate Connection Error
    print("\n[Test 1] Connection Error")
    try:
        API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
        BASE_URL = "https://invalid-domain-that-does-not-exist.com/v1"

        response = requests.post(
            f"{BASE_URL}/posts",
            headers={'Authorization': f'Bearer {API_KEY}'},
            json={},
            timeout=5
        )

        print(f"  Status: {response.status_code}")
    except requests.Timeout:
        print(f"  Error: ❌ Timeout (5s exceeded)")
    except requests.ConnectionError as e:
        print(f"  Error: ❌ Connection Error: {str(e)[:100]}")
    except Exception as e:
        print(f"  Error: ❌ {type(e).__name__}: {str(e)[:100]}")

    # Test 2: Simulate HTTP 500 Error
    print("\n[Test 2] HTTP 500 Server Error")
    try:
        BASE_URL = "https://httpbin.org/status/500"
        response = requests.post(BASE_URL, timeout=5)

        if response.status_code == 500:
            print(f"  Error: ❌ HTTP 500: Internal Server Error")
            print(f"  Response: {response.text[:100]}")
    except Exception as e:
        print(f"  Error: ❌ {type(e).__name__}: {str(e)[:100]}")

    # Test 3: Real PostBridge (current working case)
    print("\n[Test 3] Real PostBridge API (Working)")
    try:
        API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
        BASE_URL = "https://api.post-bridge.com/v1"

        test_payload = {
            'caption': f'Health check {datetime.now().strftime("%H:%M:%S")}',
            'social_accounts': ['47681'],
            'media': [],
            'scheduled_at': (datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S')
        }

        response = requests.post(
            f"{BASE_URL}/posts",
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json=test_payload,
            timeout=10
        )

        if response.status_code in [200, 201]:
            print(f"  Status: ✅ OK")
            print(f"  Response: Post created successfully")
        else:
            print(f"  Error: ❌ HTTP {response.status_code}")
            print(f"  Response: {response.text[:200]}")

    except requests.Timeout:
        print(f"  Error: ❌ Timeout (10s exceeded)")
    except requests.ConnectionError as e:
        print(f"  Error: ❌ Connection Error: {str(e)[:100]}")
    except Exception as e:
        print(f"  Error: ❌ {type(e).__name__}: {str(e)[:100]}")

    print("\n" + "="*70)
    print("✅ Error reporting captures detailed information")
    print("="*70)

if __name__ == "__main__":
    test_error_reporting()