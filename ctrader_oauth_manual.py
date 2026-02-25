#!/usr/bin/env python3
"""
CTRADER OPEN API - MANUAL OAUTH AUTHENTICATION
Script ini akan generate access token menggunakan OAuth flow manual
"""

import requests
import json

print("="*80)
print("CTRADER OPEN API - MANUAL OAUTH AUTHENTICATION")
print("="*80)
print()

# Credentials
CLIENT_ID = "21861_zgu5qR2pW4CP1uR6RjJFFpanWvHJoJb5PXnrx6V1pLnt9fuIqY"
CLIENT_SECRET = "D1tO3U2m3SyCoG0f3GUmCJkNFbeJEHnbRwTxSCY3LlZMfiZvEi"
REDIRECT_URI = "http://localhost:8080"

print("📋 CREDENTIALS:")
print(f"   Client ID: {CLIENT_ID}")
print(f"   Client Secret: {CLIENT_SECRET}")
print(f"   Redirect URI: {REDIRECT_URI}")
print()
print("="*80)
print()

# Step 1: Generate OAuth authorization URL
AUTH_URL = f"https://id.ctrader.com/my/settings/openapi/grantingaccess/?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"

print("📋 STEP 1: OAUTH AUTHORIZATION")
print("="*80)
print()
print("🌐 Open URL ini di browser:")
print()
print(f"   {AUTH_URL}")
print()
print("📋 INSTRUCTIONS:")
print("-"*80)
print("1. Copy URL di atas")
print("2. Buka di browser")
print("3. Login jika diminta (gunakan akun Fusion Markets atau cTrader ID)")
print("4. Grant permissions jika diminta")
print("5. Setelah grant, Anda akan di-redirect ke redirect URI")
print("6. Copy 'code' dari URL redirect")
print("   - Contoh: http://localhost:8080?code=AUTH_CODE_HERE")
print("7. Kirim code ke saya di chat")
print()
print("="*80)
print()

# Step 2: Try to get access token with password grant (if supported)
print("📋 STEP 2: TRY PASSWORD GRANT (ALTERNATIVE)")
print("="*80)
print()

# Try alternative endpoints
endpoints_to_try = [
    "https://api.ctrader.com/oauth2/token",
    "https://api.spotware.com/connect/token",
    "https://openapi.ctrader.com/oauth/token",
    "https://openapi.ctrader.com/token",
    "https://api.ctrader.com/token"
]

for endpoint in endpoints_to_try:
    print(f"🔗 Trying endpoint: {endpoint}")
    
    try:
        # Try password grant
        response = requests.post(
            endpoint,
            json={
                "grant_type": "password",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "username": "Openclaw@12",  # Fusion Markets username
                "password": "10100262"      # Fusion Markets password
            },
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS! Token obtained!")
            print()
            print(f"   Access Token: {data.get('access_token', 'N/A')[:50]}...")
            print(f"   Refresh Token: {data.get('refresh_token', 'N/A')[:50]}...")
            print(f"   Expires In: {data.get('expires_in', 'N/A')} seconds")
            print()
            
            # Save to file
            with open("/tmp/ctrader_tokens.json", 'w') as f:
                json.dump(data, f, indent=2)
            print("   ✅ Tokens saved to: /tmp/ctrader_tokens.json")
            print()
            
            print("="*80)
            print("✅ SUCCESS! ACCESS TOKEN OBTAINED!")
            print("="*80)
            print()
            print("📝 NEXT STEP: GET ACCOUNT ID")
            print()
            print("Dengan access token ini, saya bisa:")
            print("   - Connect ke cTrader API")
            print("   - Get account information")
            print("   - Dapatkan Account ID")
            print("   - Setup automated trading 24/7")
            print()
            sys.exit(0)
        else:
            print(f"   ❌ Failed: {response.text[:200]}")
            print()
    
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        print()

print()
print("="*80)
print("⚠️  ALTERNATIVE: USE OAUTH FLOW MANUAL")
print("="*80)
print()
print("Step 1: Buka URL ini di browser:")
print()
print(f"   {AUTH_URL}")
print()
print("Step 2: Login dan grant permissions")
print()
print("Step 3: Copy 'code' dari URL redirect")
print("   - Contoh: http://localhost:8080?code=AUTH_CODE_HERE")
print()
print("Step 4: Kirim code ke saya di chat:")
print("   - Format: Code: [paste code di sini]")
print()
print("Step 5: Saya akan:")
print("   - Exchange code untuk access token")
print("   - Get account ID")
print("   - Setup automated trading 24/7")
print()
print("="*80)
print("COMPLETE")
print("="*80)
