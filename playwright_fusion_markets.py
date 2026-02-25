import asyncio
from playwright.sync_api import sync_playwright

print("🎭 PLAYWRIGHT - FUSION MARKETS CTRADER")
print("="*80)
print()

with sync_playwright() as p:
    print("✅ Playwright loaded")
    print("🌐 Launching Chromium browser...")
    print()
    
    # Launch browser (headful - show window)
    browser = p.chromium.launch(
        headless=False,  # Show window
        slow_mo=100,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    
    print("✅ Browser launched!")
    print()
    print("🌐 Opening Fusion Markets cTrader Webtrader...")
    print()
    
    # Create new page
    page = browser.new_page()
    
    # Navigate to Fusion Markets cTrader Webtrader
    page.goto("https://fusionmarkets.com/Platforms/cTrader-Webtrader")
    
    print("✅ Page loaded: https://fusionmarkets.com/Platforms/cTrader-Webtrader")
    print()
    
    # Wait for page to load
    page.wait_for_load_state('networkidle')
    
    # Take screenshot
    print("📸 Taking screenshot...")
    screenshot_path = "/tmp/fusion_markets_trader.png"
    page.screenshot(path=screenshot_path, full_page=False)
    print(f"✅ Screenshot saved: {screenshot_path}")
    print()
    
    print("="*80)
    print("📋 FUSION MARKETS CREDENTIALS")
    print("="*80)
    print()
    print(f"   Username: Openclaw@12")
    print(f"   Password: 10100262")
    print(f"   Server: FusionMarkets-Demo")
    print(f"   Account Type: Demo")
    print()
    print("="*80)
    print("📋 MANUAL LOGIN STEPS")
    print("="*80)
    print()
    print("STEP 1: Enter Credentials")
    print(f"   - Copy username: Openclaw@12")
    print(f"   - Copy password: 10100262")
    print(f"   - Paste into login form")
    print()
    print("STEP 2: Select Server")
    print(f"   - Choose: FusionMarkets-Demo (should auto-select)")
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
    
    # Keep browser open until user closes it
    try:
        input("Press Enter to close browser when done trading... ")
    except KeyboardInterrupt:
        print()
        print("🏹 Closing browser...")
    
    browser.close()
    print()
    print("✅ Browser closed")
    print()
    print("="*80)
    print("COMPLETE")
    print("="*80)
