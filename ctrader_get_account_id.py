#!/usr/bin/env python3
"""
CTRADER API - GET ACCOUNT ID
Script ini akan connect dan dapat account_id dari Fusion Markets
"""

import sys
from ctrader_sdk import CTraderBot

print("="*80)
print("CTRADER API - GET ACCOUNT ID FROM FUSION MARKETS")
print("="*80)
print()

# Credentials dari user
CLIENT_ID = "21861_zgu5qR2pW4CP1uR6RjJFFpanWvHJoJb5PXnrx6V1pLnt9fuIqY"
CLIENT_SECRET = "D1tO3U2m3SyCoG0f3GUmCJkNFbeJEHnbRwTxSCY3LlZMfiZvEi"

print("📋 CREDENTIALS:")
print(f"   Client ID: {CLIENT_ID}")
print(f"   Client Secret: {CLIENT_SECRET}")
print(f"   Access Token: Will be auto-generated")
print()
print("="*80)
print()

try:
    print("🔗 Connecting to cTrader API...")
    
    # Initialize bot tanpa account_id dulu
    bot = CTraderBot(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=None,  # Will be auto-generated
        account_id=None      # Will try to get account list
    )
    
    print("✅ Connected!")
    print()
    
    # Try to get access token
    print("🔑 Getting access token...")
    access_token = bot.get_access_token()
    print(f"✅ Access token generated: {access_token[:20]}..." if len(access_token) > 20 else f"✅ Access token: {access_token}")
    print()
    
    # Try to get account information
    print("📊 Getting account information...")
    account_info = bot.get_account_information()
    print(f"✅ Account info: {account_info}")
    print()
    
    # Check if account_id is in response
    if isinstance(account_info, dict):
        if 'account_id' in account_info:
            account_id = account_info['account_id']
            print(f"✅ ACCOUNT ID FOUND: {account_id}")
            print()
        elif 'accountId' in account_info:
            account_id = account_info['accountId']
            print(f"✅ ACCOUNT ID FOUND: {account_id}")
            print()
        elif 'accounts' in account_info:
            accounts = account_info['accounts']
            print(f"📋 Found {len(accounts)} account(s):")
            print()
            for i, acc in enumerate(accounts, 1):
                print(f"   Account {i}:")
                if isinstance(acc, dict):
                    for key, value in acc.items():
                        print(f"     {key}: {value}")
                else:
                    print(f"     {acc}")
                print()
            
            # Ask user to choose account
            if len(accounts) == 1:
                account_id = accounts[0].get('account_id') or accounts[0].get('accountId')
                print(f"✅ Using only account: {account_id}")
            else:
                print("⚠️  Multiple accounts found!")
                print("⚠️  Check your Fusion Markets cTrader Webtrader for Account ID")
        else:
            print("⚠️  Could not find account_id in response")
            print("⚠️  Available keys:", list(account_info.keys()))
    else:
        print(f"⚠️  Unexpected account info type: {type(account_info)}")
        print("⚠️  Full info:", account_info)
    
    print()
    print("="*80)
    print("NEXT STEPS")
    print("="*80)
    print()
    
    if 'account_id' in locals() and account_id:
        print("✅ ACCOUNT ID SUCCESSFULLY RETRIEVED!")
        print(f"   Account ID: {account_id}")
        print()
        print("📝 COPY THIS ACCOUNT ID:")
        print(f"   {account_id}")
        print()
        print("📝 Kirim ke saya di chat:")
        print("   Account ID: [paste di sini]")
        print()
        print("✅ Setelah Anda kirim Account ID, saya akan:")
        print("   - Update CONFIG di asia7c_automated.py")
        print("   - Jalankan automated trading 24/7")
        print("   - Bot akan trade otomatis tanpa intervensi!")
    else:
        print("⚠️  COULDN'T AUTOMATICALLY GET ACCOUNT ID")
        print()
        print("📋 MANUAL STEPS TO GET ACCOUNT ID:")
        print()
        print("STEP 1: Login ke Fusion Markets cTrader Webtrader")
        print("   - URL: https://fusionmarkets.com/Platforms/cTrader-Webtrader")
        print("   - Username: Openclaw@12")
        print("   - Password: 10100262")
        print()
        print("STEP 2: Cari Account ID")
        print("   - Cek bagian 'Accounts' atau 'Settings'")
        print("   - Cari field 'Account ID' atau 'Account Number'")
        print("   - Copy angka tersebut")
        print()
        print("STEP 3: Kirim Account ID ke saya")
        print("   - Format: Account ID: [angka]")
        print()
        print("✅ Setelah saya dapat Account ID, bot akan siap jalan!")
    
    print()
    print("="*80)
    print("COMPLETE")
    print("="*80)
    print()

except Exception as e:
    print()
    print("="*80)
    print("❌ CONNECTION FAILED")
    print("="*80)
    print()
    print(f"Error: {e}")
    print()
    print("⚠️  Troubleshooting:")
    print("   - Check if Client ID dan Client Secret benar")
    print("   - Check if internet connection stable")
    print("   - Check if cTrader Open API is accessible")
    print("   - Verify credentials from cTrader Open API dashboard")
    print()
    print("📚 Reference:")
    print("   - https://help.ctrader.com/open-api/")
    print("   - https://help.ctrader.com/open-api/python-SDK/python-sdk-index/")
    print()
    print("="*80)
    print()
    sys.exit(1)
