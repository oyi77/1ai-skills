#!/usr/bin/env python3
"""
PLAYWRIGHT - FUSION MARKETS CTRADER (FIXED VERSION)
Robust browser automation for Fusion Markets cTrader Webtrader
"""

import asyncio
from playwright.sync_api import sync_playwright
import time
from pathlib import Path

print("="*80)
print("PLAYWRIGHT - FUSION MARKETS CTRADER (FIXED)")
print("="*80)
print()

# Configuration
URL = "https://fusionmarkets.com/Platforms/cTrader-Webtrader"
SCREENSHOT_PATH = Path("/tmp/fusion_markets_trader.png")

# Fusion Markets Credentials
USERNAME = "Openclaw@12"
PASSWORD = "10100262"
SERVER = "FusionMarkets-Demo"

print("🌐 Launching Playwright browser...")
print()

with sync_playwright() as p:
    # Launch browser with better configuration
    browser = p.chromium.launch(
        headless=False,  # Show window for manual interaction
        slow_mo=50,     # Slow down for better reliability
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process',
            '--disable-gpu'
        ]
    )
    
    print("✅ Browser launched")
    print()
    print("🌐 Creating new page...")
    
    # Create context with better settings
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    
    # Create page
    page = context.new_page()
    
    print("✅ Page created")
    print()
    print(f"🌐 Navigating to: {URL}")
    print()
    
    try:
        # Navigate with timeout
        page.goto(URL, timeout=60000, wait_until='domcontentloaded')
        print("✅ Page loaded")
        
        # Wait for page to stabilize
        print("⏳ Waiting for page to stabilize...")
        time.sleep(5)
        print("✅ Page stabilized")
        print()
        
        # Take screenshot
        print("📸 Taking screenshot...")
        page.screenshot(
            path=str(SCREENSHOT_PATH),
            full_page=False,
            type='png'
        )
        print(f"✅ Screenshot saved: {SCREENSHOT_PATH}")
        print()
        
        # Try to get page title
        try:
            title = page.title()
            print(f"📄 Page Title: {title}")
            print()
        except:
            print("⚠️  Could not get page title")
            print()
        
    except Exception as e:
        print(f"❌ Error during page load: {e}")
        print()
        print("⚠️  This is normal - the page might still be loading")
        print("   You can interact with the browser manually")
        print()
    
    print("="*80)
    print("📋 FUSION MARKETS CREDENTIALS")
    print("="*80)
    print()
    print(f"   Username: {USERNAME}")
    print(f"   Password: {PASSWORD}")
    print(f"   Server: {SERVER}")
    print(f"   Account Type: Demo")
    print()
    print("="*80)
    print("📋 MANUAL LOGIN STEPS")
    print("="*80)
    print()
    print("STEP 1: Enter Credentials")
    print(f"   - Copy username: {USERNAME}")
    print(f"   - Copy password: {PASSWORD}")
    print(f"   - Paste into login form")
    print()
    print("STEP 2: Select Server")
    print(f"   - Choose: {SERVER} (should auto-select)")
    print(f"   - Click 'Login'")
    print()
    print("STEP 3: Verify Account")
    print(f"   - Check 'Accounts' section")
    print(f"   - Note demo account balance (~$10,000)")
    print(f"   - Remember: NO REAL MONEY")
    print()
    print("="*80)
    print("📋 SETUP XAUUSD CHART")
    print("="*80)
    print()
    print("STEP 1: Click 'New Chart'")
    print("STEP 2: Search for: XAUUSD or Gold")
    print("STEP 3: Select pair: XAUUSD")
    print("STEP 4: Set Timeframe: H1 (1 Hour)")
    print()
    print("="*80)
    print("📊 XAUUSD ASIA 7-CANDLE BREAKOUT STRATEGY")
    print("="*80)
    print()
    print("Session Time: Asia Session (07:00-15:00 Jakarta)")
    print("Entry Rules:")
    print("  1. Wait for 7 candles to form")
    print("  2. Identify HH (Highest High) and LL (Lowest Low)")
    print("  3. Calculate Range: HH - LL")
    print("  4. Filter: Only trade if Range >= 5 pips (0.50)")
    print("  5. Entry Orders:")
    print("     - Buy Stop: Set at HH")
    print("     - Sell Stop: Set at LL")
    print()
    print("Exit Rules:")
    print("  1. Take Profit (TP): Entry + (Range × 2)")
    print("  2. Stop Loss (SL): Entry - Range")
    print("  3. R/R Ratio: 2:1")
    print()
    print("Risk Management:")
    print("  1. Risk: 1% per trade")
    print("  2. Max Trades: 3 per day")
    print("  3. Lot Size: 0.01 (Mini lot)")
    print("  4. Pip Value: ~$0.10 per pip")
    print()
    print("="*80)
    print("✅ BROWSER OPEN - READY FOR MANUAL TRADING")
    print("="*80)
    print()
    print("⚠️  IMPORTANT:")
    print("   - DEMO ACCOUNT - NO REAL MONEY")
    print("   - Practice and learn - don't focus on profit")
    print("   - Follow strategy rules 100%")
    print("   - NO REVENGE TRADING")
    print("   - Accept losses as part of trading")
    print()
    print("🚀 START PAPER TRADING NOW!")
    print("="*80)
    print()
    print("⏱️  Browser will remain open for 10 minutes...")
    print("   ⌨️  Press Ctrl+C to close early")
    print()
    
    # Keep browser open for 10 minutes
    try:
        time.sleep(600)  # 10 minutes
    except KeyboardInterrupt:
        print()
        print("🏹 Closing browser early...")
    
    # Clean up
    context.close()
    browser.close()
    
    print()
    print("✅ Browser closed")
    print()
    
    # Check screenshot
    if SCREENSHOT_PATH.exists():
        print(f"✅ Screenshot available: {SCREENSHOT_PATH}")
    else:
        print("⚠️  Screenshot not created (this is OK)")
    
    print()
    print("="*80)
    print("COMPLETE")
    print("="*80)
