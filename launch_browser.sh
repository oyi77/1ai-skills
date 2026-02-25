#!/bin/bash
# LAUNCH BROWSER FOR FUSION MARKETS
# Using playwright automation

echo "🎭 BROWSER LAUNCHER - FUSION MARKETS CTRADER"
echo "=================================================="
echo ""

# Activate virtual environment
source ~/.trading-venv/bin/activate

# Install playwright if needed
pip install playwright -q

# Install chromium
playwright install chromium -q

# Launch headful browser
echo "🌐 Launching Chromium Browser..."
echo "📋 Opening Fusion Markets cTrader Webtrader..."
echo "=================================================="
echo ""
echo "📊 FUSION MARKETS CREDENTIALS:"
echo "   Username: Openclaw@12"
echo "   Password: 10100262"
echo "   Server: FusionMarkets-Demo"
echo "   Account Type: Demo"
echo ""
echo "⚠️  IMPORTANT:"
echo "   These are DEMO credentials - NO REAL MONEY"
echo "   Practice and learn - don't focus on profit"
echo "=================================================="
echo ""

# Run playwright with chromium (headful - shows window)
playwright codegen https://fusionmarkets.com/Platforms/cTrader-Webtrader -o codegen.js

# Or open directly
echo "🌐 Opening cTrader Webtrader..."
python -c "
import asyncio
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    page.goto('https://fusionmarkets.com/Platforms/cTrader-Webtrader')
    
    print('✅ Browser launched')
    print('✅ cTrader Webtrader loaded')
    print('📋 Credentials:')
    print('   Username: Openclaw@12')
    print('   Password: 10100262')
    print('   Server: FusionMarkets-Demo')
    print('')
    print('📋 INSTRUCTIONS:')
    print('   1. Copy username: Openclaw@12')
    print('   2. Copy password: 10100262')
    print('   3. Login to demo account')
    print('   4. Setup XAUUSD H1 chart')
    print('   5. Follow XAUUSD Asia 7-Candle Breakout strategy')
    print('')
    print('🎯 TARGET: 4-8 weeks profitable paper trading')
    print('   - Win Rate: ≥ 60%')
    print('   - Net PNL: Positive')
    print('   - Max DD: ≤ 15%')
    print('')
    print('⚠️  BROWSER READY - TRADING READY!')
    print('==================================================')
    input('Press Enter to close browser...')
    
    browser.close()
    print('✅ Browser closed')
"
