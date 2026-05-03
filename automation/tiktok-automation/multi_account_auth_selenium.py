#!/usr/bin/env python3
"""
JENDRALBOT Multi-Account TikTok Auth (Selenium Version)
Login satu-satu ke 12 TikTok accounts menggunakan Selenium
Handle OTP/Email verification manual
"""

import asyncio
import json
import time
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Config
CONFIG_FILE = Path("/home/openclaw/.openclaw/workspace/skills/tiktok-automation/multi_account_config.json")
SESSIONS_DIR = Path("/home/openclaw/.openclaw/workspace/skills/tiktok-automation/sessions")

def load_config():
    """Load multi-account config"""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def login_single_account(account: dict):
    """
    Login ke satu TikTok account menggunakan Selenium
    Return session data atau error
    """
    if not SELENIUM_AVAILABLE:
        return {
            'username': account['username'],
            'success': False,
            'error': 'Selenium not available'
        }
    
    username = account['username']
    password = account['password']
    
    print(f"\n🔐 Starting login: @{username}")
    print(f"   Niche: {account['niche']}")
    
    try:
        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Mobile user agent
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36")
        
        # Create webdriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to TikTok
        print(f"🌐 Navigating ke TikTok login...")
        driver.get("https://www.tiktok.com/login")
        
        # Wait untuk halaman load
        time.sleep(3)
        
        try:
            # Find dan input username
            print(f"📝 Input username: {username}")
            
            # Try multiple selectors untuk username
            username_selectors = [
                (By.NAME, "username"),
                (By.CSS_SELECTOR, "input[name='username']"),
                (By.CSS_SELECTOR, "input[placeholder*='Username']"),
                (By.CSS_SELECTOR, "input[placeholder*='Email or username']"),
            ]
            
            username_input = None
            for selector in username_selectors:
                try:
                    username_input = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(selector)
                    )
                    break
                except:
                    continue
            
            if username_input:
                username_input.click()
                username_input.send_keys(username)
            else:
                raise Exception("Username input field not found")
            
            time.sleep(1)
            
            # Find dan input password
            print(f"🔑 Input password: {'*' * 10}")  # Masked
            
            password_selectors = [
                (By.NAME, "password"),
                (By.CSS_SELECTOR, "input[name='password']"),
                (By.CSS_SELECTOR, "input[placeholder*='Password']"),
                (By.CSS_SELECTOR, "input[type='password']"),
            ]
            
            password_input = None
            for selector in password_selectors:
                try:
                    password_input = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(selector)
                    )
                    break
                except:
                    continue
            
            if password_input:
                password_input.click()
                password_input.send_keys(password)
            else:
                raise Exception("Password input field not found")
            
            time.sleep(1)
            
            # Submit login
            print(f"📤 Submit login...")
            
            # Try Enter key
            password_input.send_keys("\n")
            
            # Atau klik submit button
            try:
                submit_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                )
                submit_button.click()
            except:
                pass  # Enter key sudah ter-input
            
            # Wait untuk login proses
            print(f"⏳ Waiting for login process (5 seconds)...")
            time.sleep(5)
            
            # Cek URL setelah login
            current_url = driver.current_url
            page_source = driver.page_source.lower()
            
            # Check apakah butuh OTP/Email verification
            need_otp = False
            need_email = False
            
            if 'otp' in current_url.lower() or 'verification' in current_url.lower():
                need_otp = True
            elif 'two-factor' in page_source or '2fa' in page_source:
                need_otp = True
            
            if 'email' in current_url and 'verify' in current_url:
                need_email = True
            elif 'check your email' in page_source or 'email code' in page_source:
                need_email = True
            
            if need_otp:
                print(f"\n⚠️ OTP VERIFICATION REQUIRED!")
                print(f"   Account: @{username}")
                print(f"   Boss, cek HP/Email untuk OTP code")
                print(f"   ")
                
                # Input OTP manual
                otp_code = input("   MASUKKAN OTP CODE: ")
                
                # Find OTP field dan input
                otp_selectors = [
                    (By.CSS_SELECTOR, "input[placeholder*='code']"),
                    (By.CSS_SELECTOR, "input[placeholder*='OTP']"),
                    (By.CSS_SELECTOR, "input[name='otp']"),
                    (By.CSS_SELECTOR, "input[name='code']"),
                ]
                
                otp_field = None
                for selector in otp_selectors:
                    try:
                        otp_field = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(selector)
                        )
                        break
                    except:
                        continue
                
                if otp_field:
                    otp_field.send_keys(otp_code)
                    time.sleep(1)
                    otp_field.send_keys("\n")
                
                # Wait untuk OTP verification
                print(f"⏳ Waiting for OTP verification...")
                time.sleep(5)
            
            if need_email:
                print(f"\n⚠️ EMAIL VERIFICATION REQUIRED!")
                print(f"   Account: @{username}")
                print(f"   Boss, cek email untuk verification code or link")
                print(f"   ")
                print(f"   Browser sudah open di verification page.")
                print(f"   Boss, complete verification di browser manual.")
                
                # Tunggu manual completion
                print(f"\n⏳ Menunggu boss complete verification...")
                input("   [TEKAN ENTER SETELAH VERIFICATION SELESAI]")
                
                time.sleep(3)
            
            # Cek login success
            time.sleep(3)
            final_url = driver.current_url
            
            if 'login' not in final_url.lower():
                # Login success!
                print(f"✅ LOGIN SUKSES: @{username}")
                
                # Save cookies sebagai session
                SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
                session_file = SESSIONS_DIR / f"{username}_session.json"
                
                cookies = driver.get_cookies()
                local_storage = driver.execute_script("return window.localStorage;")
                session_storage = driver.execute_script("return window.sessionStorage;")
                
                session_data = {
                    'cookies': cookies,
                    'localStorage': local_storage,
                    'sessionStorage': session_storage,
                    'username': username
                }
                
                with open(session_file, 'w') as f:
                    json.dump(session_data, f, indent=2)
                
                print(f"💾 Session saved: {session_file}")
                
                return {
                    'username': username,
                    'success': True,
                    'session_file': str(session_file)
                }
            else:
                print(f"❌ LOGIN GAGAL: @{username}")
                return {
                    'username': username,
                    'success': False,
                    'error': 'Login failed - still on login page'
                }
                
        except Exception as e:
            print(f"❌ ERROR pada @{username}: {str(e)}")
            return {
                'username': username,
                'success': False,
                'error': str(e)
            }
        finally:
            # Close browser
            try:
                driver.quit()
            except:
                pass
        
    except Exception as e:
        print(f"❌ FATAL ERROR pada @{username}: {str(e)}")
        return {
            'username': username,
            'success': False,
            'error': str(e)
        }

def multi_account_login():
    """
    Login ke semua 12 TikTok accounts satu-satu
    """
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium tidak tersedia!")
        print("   Install selenium: pip install selenium")
        print("   Install ChromeDriver: https://chromedriver.chromium.org/")
        return
    
    config = load_config()
    accounts = config['accounts']
    
    print("\n" + "="*80)
    print("🚀 JENDRALBOT - MULTI-ACCOUNT TIKTOK AUTH (SELENIUM)")
    print("="*80)
    print(f"📱 Total accounts: {len(accounts)}")
    print(f"⏱️ Estimated time: {len(accounts) * 2-3} minutes")
    print("="*80 + "\n")
    
    results = []
    
    for i, account in enumerate(accounts):
        print(f"\n{'='*80}")
        print(f"🔐 ACCOUNT {i+1}/{len(accounts)}")
        print(f"{'='*80}")
        
        result = login_single_account(account)
        results.append(result)
        
        # Delay sebelum next account
        if i < len(accounts) - 1:
            print(f"\n⏸️ Waiting 3 seconds before next account...")
            time.sleep(3)
    
    # Summary
    print("\n" + "="*80)
    print("📊 MULTI-ACCOUNT LOGIN SUMMARY")
    print("="*80)
    
    success_count = sum(1 for r in results if r['success'])
    fail_count = len(results) - success_count
    
    print(f"✅ Successful logins: {success_count}/{len(accounts)}")
    print(f"❌ Failed logins: {fail_count}/{len(accounts)}")
    
    if fail_count > 0:
        print(f"\n⚠️ Failed accounts:")
        for result in results:
            if not result['success']:
                print(f"   - @{result['username']}: {result.get('error', 'Unknown error')}")
    
    print("\n💾 Session files saved to:")
    print(f"   {SESSIONS_DIR}/")
    
    print("\n✅ Ready untuk batch upload JENDRALBOT hooks!")
    print("📈 Next step: Run multi_account_upload.py untuk upload semua hook frames\n")

def main():
    print("🎯 MULTI-ACCOUNT TIKTOK AUTH STARTING...")
    print("⚠️ Boss: Kalau butuh OTP/Email verification, siapkan kode/link!")
    
    try:
        multi_account_login()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()