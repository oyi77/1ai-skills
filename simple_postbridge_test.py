#!/usr/bin/env python3
"""
FIX POSTBRIDGE - Simple test and fix
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

# Simple test post
test_post = {
    'caption': f'Test post - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
    'social_accounts': [48178, 48177],  # Instagram
    'media': [],
    'scheduled_at': (datetime.now() + timedelta(hours=25)).strftime("%Y-%m-%dT%H:%M:%S")
}

print("="*70)
print("🧪 Testing PostBridge API...")
print()

try:
    r = requests.post(
        f"{BASE_URL}/posts",
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json=test_post,
        timeout=30
    )

    print(f"Status: {r.status_code}")
    
    if r.status_code == 201:
        result = r.json()
        print(f"✅ Post created! ID: {result.get('id')}")
        print(f"Caption: {result.get('caption')}")
        print("✅ POSTBRIDGE WORKS!")
        print()
        print("Next steps:")
        print("1. Morning workflow akan auto-post queue items")
        print("2. System will track yang sudah terposting")
        print("3. Monitor via ~/automation.log")
    else:
        print(f"Failed: {r.status_code}")
        if r.status_code == 400:
            print("  - Error 400: Invalid data structure")
            print("  - Solution: Clear queue + rebuild")

except Exception as e:
    print(f"Error: {e}")