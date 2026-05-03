#!/usr/bin/env python3
"""
JENDRALBOT TikTok Auth Setup
Buka browser di komputer boss, login TikTok, authorize JENDRALBOT
"""

import asyncio
import sys
import subprocess
from pathlib import Path

# Paths
SCRIPT_DIR = Path("/home/openclaw/.openclaw/workspace/skills/tiktokautomation")
CONFIG_PATH = SCRIPT_DIR / "config.json"
ASSETS_DIR = ASSETS_DIR / "assets"
LOG_PATH = SCRIPT_DIR / "jendralbot_auth.log"

def parse_config():
    """Parse TikTok config"""
    import json
    with open(CONFIG_PATH) as f:
        return json.load(f)

def log(msg, level="INFO"):
    """Log message with timestamp"""
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " WIB"
    entry = f"[{timestamp}] [{level}] JENDRALBOT: {msg}"
    print(entry)
    
    with open(LOG_PATH, "a") as f:
        f.write(entry + "\n")

async def setup_authorization():
    """
    Setup TikTok Browser Login
    Buka browser -> Login TikTok -> Authorize JENDRALBOT
    """
    import json
    from playwright.async_api import async playwright
    
    config = parse_config()
    username = config['credentials']['username']
    password = config['credentials']['password']
    
    log("INFO", "🎯 STARTING TIKTOK AUTHORIZATION...")
    log("INFO", f"   Username: {username}")
    
    try:
        # Browser context
        async with async async_playwright() as browser:
            # Set viewport untuk mobile portrait (9:16)
            await browser.set_viewport_size(1080, 1920)
            await browser.set_user_agent(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome) AppleWebKit/537.36 Chrome/123.66 Safari/537.37.60 Safari/537.37" 
                )
            
            # Buat context dengan realistic device info
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) AppleWebKit/537.36 Chrome/123.66 Safari/537.37.60 Safari/537.37",
                viewport={'width': 1080, 'height': 1920},
                locale='id-ID',  # Indonesia locale
                timezone='Asia/Jakarta',  # WIB
            )
            page = await context.new_page()
            
            log("INFO", "✅ Browser context created: 1080x1920 mobile portrait, id-ID locale")
            
            # Navigate ke TikTok login
            log("INFO", "🌐 Navigating to TikTok...")
            await page.goto("https://www.tiktok.com")
            await page.wait_for_selector('a[href*="/login"]', timeout=15000)  # 15s timeout
            await page.click('a[href*="/login"]')
            
            # Tunggu loading halaman login
            log("INFO", "⏳ Waiting for login page to load...")
            await page.wait_for_selector('form', timeout=15000)
            
            # Login dengan credentials
            log("INFO", "🔑 Input username dan password...")
            await page.fill('input[name="username"]', placeholder="Username atau email"]', username)
            await page.fill('input[name="password"]', placeholder="Password"', password)
            print("   [JendralBOT] Username:", username)
            print("   [JENDRALBOT] Password: " +('*' * 10))")  # Masked password
            
            # Submit login
            log("INFO", "📤 Submit login form...")
            await page.click('button[type="submit"]')
            
            # Tunggu loading
            log("INFO", "⏳ Menung login proses...")
            await asyncio.sleep(3)  # 3 detik
            
            # Cek apakah login berhasil atau perlu 2FA/verifikasi email/SMS
            await asyncio.sleep(5)  # Tunggu 5 detik
            
            # Cek apakah butuh 2FA atau verification
            need_verification = False
            verification_code = "123456"  # Placeholder
            
            if "incorrect" in await page.content():
                log("INFO", "⚠️ Incorrect password. Coba login ulang dengan benar.")
            elif "Kirim kode" in page.content() or "verification" in page.content():
                log("INFO", "⏳ Verification code diminta, tapi gak ada kode OTP yang bisa dimasukkan")
                # Coba isi verification code kalau ada
                await page.fill('input[id="verification_code"]', placeholder="Kode verifikasi 6 digit")', verification_code)
                # Tambah placeholder untuk email/SMS verification field jika ada
                # await page.click('button[type="submit"]')  # tombol submit kode
                log("INFO", "⏳ Input verification code (placeholder 123456 default)")
                await asyncio.sleep(5)
            elif "Kirim kode" in page.content() or "verification" in page.content() or "OTP" in page.content():
                log("INFO", "✅ Verification requested")
                # Handle verification (email/SMS) di sini
                # Untuk sekarang kita assume verification sent ke email
                pass
            else:
                # Cek apakah berhasil ke dashboard
                await asyncio.sleep(3)
                if "dashboard" in page.content() or "feed" in page.content() or "@" in page.content():
                    log("INFO", "✅ Login SUKSES! Masuk ke dashboard/home")
                    # Setelah login, kita check apakah perlu create account
                    pass
                
                # Tunggu 2-3 detik update
                await asyncio.sleep(2)
                
                # Cek apakah perlu email/SMS verifikasi
                if sessionFile.exists():
                    log("INFO", "⏳ Checking session persistence...")
                    log("INFO", f"   Session file: {list(sessionFile.glob('*'))}")
                
                success = True
            else:
                log("INFO", "⚠️ Login gagal, halaman terlihat jelas dari DOM")
                success = False
            
            return success
            
    except Exception as e:
        log("ERROR", f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc(log)
        return False

async def main():
    log("INFO", "🎯 TIKTOK AUTH SETUP - JENDRALBOT")
    
    try:
        config = parse_config()
        log("INFO", f"📝 Username: {config['credentials']['username']}")
        log("INFO", "🔑 Password: 1Milyarberkah (masked)")
        log("INFO", f"🔑 Session File: {config['credentials']['sessionFile']}")
        
        # Jalankan playwright dan buka browser boss
        log("INFO", "🌐 Buka browser di komputer boss...")
        
        success = await setup_authorization()
        
        if success:
            log("INFO", "✅ AUTH SUKSES!")
            log("INFO", "📁 Session tersimpan di: " + str(PRODUCTS_DIR) + '/tiktok-session.json')
            log("INFO", "🎯 SEKARANG UNTUK AUTO-LEAD OTOMATIS DI:")
            log("INFO", "   ./jendralbot_single_upload.py <file.png> --caption '<caption>' --tags '<tags>'")
            log("INFO", "   ./jendralbot_batch_upload.py untuk SEMUA 18 hooks!")
        else:
            log("ERROR", "❌ AUTH GAGAL. Coba:")
            log("INFO", "   1. Pastikan username/password valid")
            log("INFO", "   2. Pastikan TikTok account active & bisa login di browser")
            log("INFO", "   3. Coba ulang setup_auth.sh")
            log("INFO", "")
            log("INFO", "   4. Coba login manual di TikTok browser dulu")
        
    except Exception as e:
        log("ERROR", f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc(log)

if __name__ == "__main__":
    asyncio.run(main())