#!/usr/bin/env python3
"""
Check PostBridge Connected Accounts
"""

import urllib.request
import json

API_KEY = "pb_live_Kyc2gafDF7Qc8c2ALELtEC"

def get_connected_accounts(offset=0, limit=50):
    """Fetch all connected accounts from PostBridge."""
    accounts = []
    
    while True:
        url = f"https://api.post-bridge.com/v1/social-accounts?limit={limit}&offset={offset}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {API_KEY}")
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                
                if not data.get("success", False):
                    print(f"❌ API Error: {data.get('message', 'Unknown')}")
                    break
                
                items = data.get("items", [])
                if not items:
                    break
                
                accounts.extend(items)
                offset += len(items)
                
                print(f"📥 Fetched {len(items)} accounts (total: {len(accounts)})")
                
                if len(items) < limit:
                    break
                    
        except urllib.error.HTTPError as e:
            print(f"❌ HTTP Error {e.code}: {e.read().decode()[:200]}")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break
    
    return accounts

def main():
    print("=" * 80)
    print("🔍 POSTBRIDGE CONNECTED ACCOUNTS CHECKER")
    print("=" * 80)
    
    accounts = get_connected_accounts()
    
    if not accounts:
        print("\n❌ No accounts found!")
        return
    
    print(f"\n✅ Found {len(accounts)} connected accounts\n")
    print("=" * 80)
    
    # Group by platform
    platforms = {}
    for account in accounts:
        platform = account.get("platform", "unknown")
        if platform not in platforms:
            platforms[platform] = []
        platforms[platform].append(account)
    
    # Display by platform
    for platform, accs in sorted(platforms.items()):
        print(f"\n📱 {platform.upper()} ({len(accs)} accounts)")
        print("-" * 80)
        
        for i, acc in enumerate(accs, 1):
            name = acc.get("name", "N/A")
            username = acc.get("username", "N/A")
            connected = acc.get("connected", False)
            status = "✅ Connected" if connected else "❌ Disconnected"
            
            print(f"{i}. {name}")
            print(f"   Username: {username}")
            print(f"   Status: {status}")
            print(f"   ID: {acc.get('id', 'N/A')}")
            print()
    
    print("=" * 80)
    
    # Summary
    print("\n📊 SUMMARY:")
    print(f"   Total Accounts: {len(accounts)}")
    print(f"   Total Platforms: {len(platforms)}")
    
    for platform, accs in platforms.items():
        connected_count = sum(1 for a in accs if a.get("connected", False))
        print(f"   {platform.upper()}: {connected_count}/{len(accs)} connected")
    
    print("=" * 80)

if __name__ == "__main__":
    main()