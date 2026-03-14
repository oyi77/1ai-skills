#!/usr/bin/env python3
"""
Debug PostBridge API Error - Get exact error message
"""

import json
import requests
from datetime import datetime, timedelta

# PostBridge API Configuration
API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"
ACCOUNT_ID = "47681"

def test_postbridge_api():
    """Test PostBridge API and get exact error"""
    print("="*70)
    print("PostBridge API Debug")
    print("="*70)

    try:
        # Test 1: Check health endpoint
        print("\n[Test 1] Health Endpoint Check")
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=10)
            print(f"  Status Code: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

        # Test 2: Create post (same as heartbeat)
        print("\n[Test 2] Create Post (Heartbeat Method)")
        test_payload = {
            'caption': f'Health check {datetime.now().strftime("%H:%M:%S")}',
            'social_accounts': [ACCOUNT_ID],
            'media': [],
            'scheduled_at': (datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S')
        }

        print(f"  URL: {BASE_URL}/posts")
        print(f"  Account ID: {ACCOUNT_ID}")
        print(f"  Payload keys: {list(test_payload.keys())}")

        start = datetime.now()
        response = requests.post(
            f"{BASE_URL}/posts",
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json=test_payload,
            timeout=10
        )
        elapsed = (datetime.now() - start).total_seconds()

        print(f"\n  Status Code: {response.status_code}")
        print(f"  Latency: {elapsed:.2f}s")
        print(f"  Response Headers: {dict(response.headers)}")

        if response.status_code in [200, 201]:
            print(f"  ✅ SUCCESS")
            try:
                print(f"  Response Body: {response.text[:500]}")
            except:
                print(f"  Response Body: (binary)")
        else:
            print(f"  ❌ HTTP ERROR")
            print(f"  Response Body: {response.text}")
            print(f"\n  📋 ERROR MESSAGE TO REPORT:")
            print(f"  ================")
            print(f"  Status Code: {response.status_code}")
            print(f"  Response: {response.text}")
            print(f"  ================")

        # Test 3: Check scheduled posts
        print("\n[Test 3] List Scheduled Posts")
        try:
            response = requests.get(
                f"{BASE_URL}/scheduled-posts",
                headers={
                    'Authorization': f'Bearer {API_KEY}',
                    'Content-Type': 'application/json'
                },
                params={'account_id': ACCOUNT_ID},
                timeout=10
            )
            print(f"  Status Code: {response.status_code}")
            print(f"  Response: {response.text[:500]}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

    except requests.Timeout:
        print("\n❌ TIMEOUT (10s)")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print(f"Error Type: {type(e).__name__}")

    print("\n" + "="*70)
    return 0

if __name__ == "__main__":
    test_postbridge_api()