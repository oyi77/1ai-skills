#!/usr/bin/env python3
"""
CTRADER OAUTH WITH CURL - AVOID BROWSER SSL ISSUES
Use command-line curl instead of browser for OAuth
"""

import subprocess
import urllib.parse

print("="*80)
print("CTRADER OAUTH WITH CURL - AVOID SSL ISSUES")
print("="*80)
print()

# OAuth Configuration
CLIENT_ID = "21861_zgu5qR2pW4CP1uR6RjJFFpanWvHJoJb5PXnrx6V1pLnt9fuIqY"
CLIENT_SECRET = "D1tO3U2m3SyCoG0f3GUmCJkNFbeJEHnbRwTxSCY3LlZMfiZvEi"
REDIRECT_URI = "http://localhost:8080"

# Generate OAuth authorization URL
AUTH_URL = f"https://id.ctrader.com/my/settings/openapi/grantingaccess/?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"

print("📋 STEP 1: MANUALLY GRANT ACCESS")
print("="*80)
print()
print("Buka URL ini di browser Anda sendiri (Chrome, Firefox, Edge):")
print()
print(f"{AUTH_URL}")
print()
print("📋 INSTRUCTIONS:")
print("-"*80)
print("1. Copy URL di atas")
print("2. Buka di browser ANDA SENDIRI")
print("3. Login jika diminta:")
print("   - Username: Openclaw@12")
print("   - Password: 10100262")
print("4. Grant permissions jika diminta")
print("5. Setelah grant, Anda akan di-redirect ke:")
print("   http://localhost:8080?code=AUTH_CODE_HERE")
print("6. Copy 'code' dari URL redirect tersebut")
print()
print("="*80)
print()

# Ask user for authorization code
print("📝 STEP 2: PASTE AUTHORIZATION CODE")
print("="*80)
print()
auth_code = input("Paste authorization code dari URL redirect: ").strip()

if not auth_code or auth_code.lower() == 'exit':
    print("❌ No authorization code provided")
    exit(1)

print()
print("✅ Authorization code received")
print(f"   Code: {auth_code[:20]}..." if len(auth_code) > 20 else f"   Code: {auth_code}")
print()

print("📋 STEP 3: EXCHANGE CODE FOR ACCESS TOKEN")
print("="*80)
print()

# Prepare curl command to exchange code for token
token_url = "https://openapi.ctrader.com/oauth/token"

curl_command = f"""curl -X POST '{token_url}' \\
  -H 'Accept: application/json' \\
  -H 'Content-Type: application/json' \\
  -d '{{
    "grant_type": "authorization_code",
    "code": "{auth_code}",
    "client_id": "{CLIENT_ID}",
    "client_secret": "{CLIENT_SECRET}",
    "redirect_uri": "{REDIRECT_URI}"
  }}'"""

print("📋 CURL COMMAND:")
print()
print(curl_command)
print()

# Execute curl command
print("🔗 Executing curl...")
print()

try:
    result = subprocess.run(
        curl_command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    print(f"Status Code: {result.returncode}")
    print()
    print("Response:")
    print(result.stdout)
    
    if result.stderr:
        print()
        print("Errors:")
        print(result.stderr)
    
    if result.returncode == 0:
        print()
        print("✅ TOKEN SUCCESSFULLY OBTAINED!")
        print()
        
        # Try to parse JSON response
        try:
            import json
            token_data = json.loads(result.stdout)
            
            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token')
            expires_in = token_data.get('expires_in')
            
            if access_token:
                print(f"✅ Access Token: {access_token[:50]}...")
                print(f"✅ Refresh Token: {refresh_token[:50]}..." if refresh_token else "⚠️  No Refresh Token"
                print(f"✅ Expires In: {expires_in} seconds" if expires_in else "⚠️  No Expiry Info")
                print()
                
                # Save tokens to file
                import json as json_module
                tokens = {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'expires_in': expires_in,
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'obtained_at': subprocess.check_output(['date', '+%Y-%m-%d %H:%M:%S']).decode().strip()
                }
                
                with open('/tmp/ctrader_tokens.json', 'w') as f:
                    json_module.dump(tokens, f, indent=2)
                
                print(f"✅ Tokens saved to: /tmp/ctrader_tokens.json")
                print()
                
                print("="*80)
                print("NEXT STEPS")
                print("="*80)
                print()
                print("Saya akan:")
                print("1. Load tokens dari /tmp/ctrader_tokens.json")
                print("2. Connect ke cTrader API")
                print("3. Get Account ID")
                print("4. Update asia7c_automated.py")
                print("5. Jalankan automated trading 24/7")
                print()
                print("="*80)
                print("COMPLETE - READY FOR AUTOMATED TRADING!")
                print("="*80)
                
            else:
                print("⚠️  Could not parse JSON response")
                print("⚠️  Manual parsing may be needed")
        
        except Exception as e:
            print(f"⚠️  JSON parse error: {e}")
    else:
        print()
        print("❌ CURL FAILED")
        print()
        print("⚠️  Troubleshooting:")
        print("   - Check if authorization code is correct")
        print("   - Check if client_id and client_secret are correct")
        print("   - Check if redirect_uri matches what was used")
        print("   - Try again with new authorization code")

except Exception as e:
    print(f"❌ Error executing curl: {e}")
    print()
    print("⚠️  Alternative: Copy curl command and run manually")
