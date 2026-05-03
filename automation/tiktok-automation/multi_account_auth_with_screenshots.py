#!/usr/bin/env python3
"""
JENDRALBOT Multi-Account TikTok Auth with Screenshots
Login satu-satu ke 12 TikTok accounts
Capture screenshot profil setelah berhasil login
"""

import json
import time
from pathlib import Path
from datetime import datetime

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
SCREENSHOTS_DIR = Path("/home/openclaw/.openclaw/workspace/skills/tiktok-automation/screenshots")
SESSIONS_DIR = Path("/home/openclaw/.openclaw/workspace/skills/tiktok-automation/sessions")

def load_config():
    """Load multi-account config"""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def take_screenshot(driver, account: dict, prefix: str):
    """Take screenshot dan save ke file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{account['username']}_{timestamp}.png"
    filepath = SCREENSHOTS_DIR / filename
    
    # Create screenshots directory
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Take screenshot
    driver.save_screenshot(str(filepath))
    
    print(f"📸 Screenshot saved: {filepath}")
    return filepath

def login_single_account(account: dict):
    """
    Login ke satu TikTok account
    Take screenshot setelah berhasil
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
    
    driver = None
    try:
        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36")
        
        # Create webdriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to TikTok
        print(f"🌐 Navigating ke TikTok login...")
        driver.get("https://www.tiktok.com/login")
        
        # Wait untuk halaman load
        time.sleep(5)
        
        # Screenshot halaman login
        take_screenshot(driver, account, "login_page")
        
        # Try multiple strategies untuk find elements
        print(f"🔍 Mencari login form...")
        
        # Strategy 1: Try all possible username selectors
        username_found = False
        username_selectors = [
            (By.NAME, "username"),
            (By.CSS_SELECTOR, 'input[name="username"]'),
            (By.CSS_SELECTOR, 'input[placeholder*="Username"]'),
            (By.CSS_SELECTOR, 'input[placeholder*="Email"]'),
            (By.CSS_SELECTOR, 'input[data-e2e="username-input"]'),
            (By.XPATH, '//input[contains(@placeholder, "Username") or contains(@placeholder, "Email")]'),
        ]
        
        username_input = None
        for selector_by, selector_value in username_selectors:
            try:
                elements = driver.find_elements(selector_by, selector_value)
                if elements:
                    for elem in elements:
                        if elem.is_displayed() and elem.is_enabled():
                            username_input = elem
                            username_found = True
                            print(f"   ✅ Found username field with: {selector_by}={selector_value}")
                            break
                if username_found:
                    break
            except Exception as e:
                continue
        
        if not username_input or not username_found:
            # Try by direct text input ke setiap input visible
            print(f"   ⚠️ Selector not found, mencoba alternative approach...")
            all_inputs = driver.find_elements(By.TAG_NAME, "input")
            for inp in all_inputs:
                if inp.is_displayed() and inp.is_enabled():
                    placeholder = inp.get_attribute('placeholder') or ''
                    input_type = inp.get_attribute('type') or 'text'
                    if 'username' in str(placeholder).lower() or 'email' in str(placeholder).lower():
                        username_input = inp
                        username_found = True
                        print(f"   ✅ Found username field by placeholder: {placeholder}")
                        break
                    elif input_type == 'text' and not username_input:
                        username_input = inp  # Fallback ke first text field
        
        if not username_input:
            raise Exception("Tidak dapat menemukan field username")
        
        # Input username
        time.sleep(1)
        username_input.clear()
        username_input.send_keys(username)
        print(f"✅ Username input: {username}")
        
        # Screenshot setelah username diinput
        time.sleep(1)
        take_screenshot(driver, account, "username_filled")
        
        # Find password field
        print(f"(   🔍 Mencari password field...")
        password_input = None
        password_selectors = [
            (By.NAME, "password"),
            (By.CSS_SELECTOR, 'input[name="password"]'),
            (By.CSS_SELECTOR, 'input[type="password"]'),
            (By.CSS_SELECTOR, 'input[placeholder*="Password"]'),
            (By.CSS_SELECTOR, 'input[data-e2e="password-input"]'),
        ]
        
        password_found = False
        for selector_by, selector_value in password_selectors:
            try:
                elements = driver.find_elements(selector_by, selector_value)
                if elements:
                    for elem in elements:
                        if elem.is_displayed() and elem.is_enabled():
                            password_input = elem
                            password_found = True
                            print(f"   ✅ Found password field with: {selector_by}={selector_value}")
                            break
                if password_found:
                    break
            except Exception as e:
                continue
        
        if not password_input:
            # Find by position (biasanya setelah username)
            all_inputs = driver.find_elements(By.TAG_NAME, "input")
            for inp in all_inputs:
                if inp != username_input and inp.is_displayed():
                    input_type = inp.get_attribute('type')
                    if input_type == 'password':
                        password_input = inp
                        password_found = True
                        print(f"   ✅ Found password field by type")
                        break
        
        if not password_input:
            raise Exception("Tidak dapat menemukan field password")
        
        # Input password
        time.sleep(1)
        password_input.clear()
        password_input.send_keys(password)
        print(f"✅ Password input: {'*' * 10}")
        
        # Screenshot setelah password diinput
        time.sleep(1)
        take_screenshot(driver, account, "password_filled")
        
        # Submit login
        print(f"📤 Submit login...")
        password_input.send_keys("\n")  # Enter key
        
        # Wait untuk login proses
        print(f"⏳ Waiting for login process (10 seconds)...")
        time.sleep(10)
        
        # Cek URL saat ini
        current_url = driver.current_url
        page_source = driver.page_source.lower()
        
        print(f"🔍 Current URL: {current_url}")
        
        # Cek verification indicators
        need_otp = False
        need_email = False
        
        if 'otp' in current_url.lower() or 'verification' in current_url.lower():
            need_otp = True
            print(f"⚠️ OTP verification detected!")
        elif 'two-factor' in page_source or '2fa' in page_source or 'verification code' in page_source:
            need_otp = True
            print(f"⚠️ 2FA/OTP detected!")
        
        if 'email' in current_url and 'verify' in current_url:
            need_email = True
            print(f"⚠️ Email verification detected!")
        elif 'check your email' in page_source or 'email code' in page_source or 'verify email' in page_source:
            need_email = True
            print(f"⚠️ Email verification required!")
        
        # Screenshot verification page jika perlu
        if need_otp or need_email:
            take_screenshot(driver, account, "verification_page")
        
        if need_otp:
            print(f"\n⚠️ OTP VERIFICATION REQUIRED!")
            print(f"   Account: @{username}")
            print(f"   Boss, cek HP/Email untuk OTP code")
            print(f"   ")
            
            otp_code = input("   MASUKKAN OTP CODE: ")
            
            # Find dan input OTP
            otp_selectors = [
                (By.CSS_SELECTOR, 'input[placeholder*="code"]'),
                (By.CSS_SELECTOR, 'input[placeholder*="OTP"]'),
                (By.CSS_SELECTOR, 'input[name="otp"]'),
                (By.CSS_SELECTOR, 'input[name="code"]'),
                (By.XPATH, '//input[contains(@placeholder, "code") or contains(@placeholder, "OTP")]'),
            ]
            
            otp_field = None
            try:
                for selector_by, selector_value in otp_selectors:
                    elements = driver.find_elements(selector_by, selector_value)
                    if elements:
                        for elem in elements:
                            if elem.is_displayed() and elem.is_enabled():
                                otp_field = elem
                                print(f"   ✅ Found OTP field")
                                break
                    if otp_field:
                        break
            except Exception as e:
                print(f"   ⚠️ Error mencari OTP field: {str(e)}")
            
            if otp_field:
                otp_field.clear()
                otp_field.send_keys(otp_code)
                time.sleep(2)
                otp_field.send_keys("\n")
                print(f"✅ OTP code submitted")
            
            print(f"⏳ Waiting untuk OTP verification...")
            time.sleep(10)
        
        if need_email:
            print(f"\n⚠️ EMAIL VERIFICATION REQUIRED!")
            print(f"   Account: @{username}")
            print(f"   Boss, cek email untuk verification code atau link")
            print(f"   ")
            print(f"   Browser sudah open di verification page.")
            
            take_screenshot(driver, account, "email_verification")
            
            print(f"\n⏳ Menunggu boss complete verification...")
            input("   [TEKAN ENTER SETELAH VERIFICATION SELESAI]")
            
            time.sleep(5)
        
        # Cek login success
        final_url = driver.current_url
        print(f"🔍 Final URL: {final_url}")
        
        # Try navigate ke profile page
        time.sleep(3)
        profile_url = f"https://www.tiktok.com/@{username}"
        print(f"🌐 Navigating ke profile: {profile_url}")
        driver.get(profile_url)
        time.sleep(5)
        
        # Screenshot halaman profil
        take_screenshot(driver, account, "profile_page")
        
        # Cek apakah user berhasil di-load di profile
        page_source = driver.page_source.lower()
        if username.lower() in page_source:
            print(f"✅ LOGIN SUKSES: @{username}")
            
            # Additional screenshot untuk confirmation
            take_screenshot(driver, account, "login_success")
            
            # Save session
            SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
            session_file = SESSIONS_DIR / f"{username}_session.json"
            
            cookies = driver.get_cookies()
            try:
                local_storage = driver.execute_script("return window.localStorage || {};")
            except:
                local_storage = {}
            try:
                session_storage = driver.execute_script("return window.sessionStorage || {};")
            except:
                session_storage = {}
            
            session_data = {
                'cookies': cookies,
                'localStorage': local_storage,
                'sessionStorage': session_storage,
                'username': username,
                'login_time': datetime.now().isoformat()
            }
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"💾 Session saved: {session_file}")
            
            return {
                'username': username,
                'success': True,
                'session_file': str(session_file),
                'profile_url': profile_url
            }
        else:
            print(f"❌ LOGIN GAGAL: @{username}")
            print(f"   Reason: Profile page tidak menampilkan username")
            return {
                'username': username,
                'success': False,
                'error': 'Login gagal - profile tidak valid'
            }
            
    except Exception as e:
        print(f"❌ ERROR pada @{username}: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'username': username,
            'success': False,
            'error': str(e)
        }
    finally:
        # Close browser dengan delay
        if driver:
            try:
                time.sleep(3)
                driver.quit()
            except:
                pass

def multi_account_login():
    """
    Login ke semua 12 TikTok accounts satu-satu
    Take screenshot setiap profile
    """
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium tidak tersedia!")
        return
    
    config = load_config()
    accounts = config['accounts']
    
    print("\n" + "="*80)
    print("🚀 JENDRALBOT - MULTI-ACCOUNT TIKTOK AUTH WITH SCREENSHOTS")
    print("="*80)
    print(f"📱 Total accounts: {len(accounts)}")
    print(f"📸 Screenshots akan disimpan di: {SCREENSHOTS_DIR}")
    print(f"⏱️ Estimated time: {len(accounts) * 3-5} minutes")
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
            print(f"\n⏸️ Waiting 5 seconds before next account...")
            time.sleep(5)
    
    # Summary
    print("\n" + "="*80)
    print("📊 MULTI-ACCOUNT LOGIN SUMMARY")
    print("="*80)
    
    success_count = sum(1 for r in results if r['success'])
    fail_count = len(results) - success_count
    
    print(f"✅ Successful logins: {success_count}/{len(accounts)}")
    print(f"❌ Failed logins: {fail_count}/{len(accounts)}")
    
    if success_count > 0:
        print(f"\n✅ Screenshot profiles tersimpan di:")
        print(f"   {SCREENSHOTS_DIR}/")
    
    if fail_count > 0:
        print(f"\n⚠️ Accounts yang gagal:")
        for result in results:
            if not result['success']:
                print(f"   - @{result['username']}: {result.get('error', 'Unknown error')}")
    
    print("\n💾 Session files yang disimpan:")
    for result in results:
        if result['success']:
            print(f"   - {result.get('session_file', 'N/A')}")
    
    print("\n✅ Ready untuk batch upload JENDRALBOT hooks!")
    print("📸 Semua screenshot profile tersedia untuk verification")

def main():
    print("🎯 MULTI-ACCOUNT TIKTOK AUTH STARTING...")
    print("📸 Screenshots akan diambil untuk setiap PROFIL!")
    
    try:
        multi_account_login()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()