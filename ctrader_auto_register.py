#!/usr/bin/env python3
"""
CTRADER OPEN API - AUTO REGISTER APPLICATION
Script ini akan buka cTrader Open API dan bantu Anda register aplikasi
"""

from playwright.sync_api import sync_playwright
import time

print("="*80)
print("CTRADER OPEN API - AUTO REGISTER APPLICATION")
print("="*80)
print()

# cTrader Open API URLs
URL_APPS = "https://openapi.ctrader.com/apps"
URL_LOGIN = "https://id.ctrader.com/login"
URL_REGISTER = "https://id.ctrader.com/register"

print("📋 INSTRUCTIONS:")
print("-"*80)
print()
print("STEP 1: Script akan buka cTrader Open API")
print("STEP 2: Anda akan diminta login")
print("STEP 3: Gunakan salah satu opsi:")
print("  Option A: Login dengan Fusion Markets akun Anda")
print("    Username: Openclaw@12")
print("    Password: 10100262")
print("  Option B: Login dengan cTrader ID (jika ada)")
print("  Option C: Register cTrader ID baru")
print()
print("STEP 4: Setelah login, Anda akan di-redirect ke Apps Dashboard")
print("STEP 5: Cari tombol 'Create New Application' atau 'Add Application'")
print("STEP 6: Isi form:")
print("   - Application Name: BerakahKaryaQuant-Automated")
print("   - Application Type: Web")
print("   - Redirect URI: http://localhost:8080")
print("   - Description: Automated trading bot for XAUUSD")
print("STEP 7: Klik 'Create' atau 'Save'")
print("STEP 8: Copy Client ID dan Client Secret")
print("STEP 9: Update CONFIG di asia7c_automated.py")
print()
print("="*80)
print()

print("🌐 Launching browser...")
print()

with sync_playwright() as p:
    # Launch browser
    browser = p.chromium.launch(
        headless=False,
        slow_mo=100,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    
    # Create context
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080}
    )
    
    # Create page
    page = context.new_page()
    
    try:
        # Navigate to cTrader Open API Apps
        print(f"🌐 Opening: {URL_APPS}")
        page.goto(URL_APPS, timeout=60000, wait_until='domcontentloaded')
        print("✅ Page loaded")
        print()
        
        # Wait for page to stabilize
        time.sleep(5)
        
        # Try to get page title
        try:
            title = page.title()
            print(f"📄 Page Title: {title}")
            print()
        except:
            print("⚠️  Could not get page title")
            print()
        
        # Take screenshot
        screenshot_path = "/tmp/ctrader_openapi_apps.png"
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"✅ Screenshot saved: {screenshot_path}")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("⚠️  Browser tetap terbuka - Anda bisa manual register")
        print()
    
    print("="*80)
    print("📋 FUSION MARKETS CREDENTIALS")
    print("="*80)
    print()
    print("   Username: Openclaw@12")
    print("   Password: 10100262")
    print("   Server: FusionMarkets-Demo")
    print()
    print("="*80)
    print("📋 APA YANG PERLU ANDA LAKUKAN")
    print("="*80)
    print()
    print("DI BROWSER YANG SUDAH TERBUKA:")
    print()
    print("1. Login ke cTrader Open API")
    print("   - Gunakan: Openclaw@12 / 10100262 (Fusion Markets)")
    print("   - ATAU register cTrader ID baru")
    print()
    print("2. Setelah login, cari 'Create New Application'")
    print()
    print("3. Isi form:")
    print("   - Application Name: BerakahKaryaQuant-Automated")
    print("   - Type: Web")
    print("   - Redirect URI: http://localhost:8080")
    print("   - Description: Automated XAUUSD trading bot")
    print()
    print("4. Klik 'Create'")
    print()
    print("5. Copy credentials yang muncul:")
    print("   - Client ID")
    print("   - Client Secret")
    print()
    print("6. Kirim ke saya di chat ini:")
    print("   - Client ID: [paste di sini]")
    print("   - Client Secret: [paste di sini]")
    print()
    print("7. Saya akan:")
    print("   - Update CONFIG di asia7c_automated.py")
    print("   - Jalankan automated trading 24/7")
    print()
    print("="*80)
    print("✅ BROWSER SIAP - SILAKAN REGISTER")
    print("="*80)
    print()
    print("⏱️  Browser akan tetap terbuka selama 15 menit...")
    print("   Setelah selesai, close browser manual atau tunggu 15 menit")
    print()
    
    # Keep browser open for 15 minutes
    try:
        time.sleep(900)  # 15 minutes
    except KeyboardInterrupt:
        print()
        print("🏹 Closing browser...")
    
    # Cleanup
    context.close()
    browser.close()
    
    print()
    print("✅ Browser closed")
    print()
    print("="*80)
    print("COMPLETE")
    print("="*80)
