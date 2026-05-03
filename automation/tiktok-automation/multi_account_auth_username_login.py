#!/usr/bin/env python3
"""
JENDRALBOT Multi-Account TikTok Auth with Username Login
Login satu-satu ke 12 TikTok accounts
Pilih "Login with Username" option
Take screenshot profil setelah berhasil login
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
    from selenium.webdriver.common.action_chains import ActionChains
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
    
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    
    driver.save_screenshot(str(filepath))
    
    print(f"📸 Screenshot saved: {filepath}")
    return filepath

def select_login_method(driver):
    """Pilih 'Login with Username' option di TikTok login page"""
    try:
        print(f"   🔍 Mencari pilihan login method...")
        
        # Cari berbagai text/bagian yang mengindikasikan pilihan login method
        login_method_selectors = [
            # Text-based selectors
            (By.XPATH, "//div[contains(text(), 'Login with Username') or contains(text(), 'Login with username') or contains(text(), 'Username') or contains(text(), 'Use username')]"),
            (By.XPATH, "//button[contains(text(), 'Username') or contains(text(), 'Login with username')]"),
            (By.XPATH, "//a[contains(text(), 'Username')]"),
            (By.XPATH, "//span[contains(text(), 'Username')]"),
            # Radio button/checkbox
            (By.CSS_SELECTOR, "input[type='radio'][value='username']"),
            (By.XPATH, "//input[@type='radio' and (@value='username' or @name='username')]"),
            # Tab/div yang mengindikasikan
            (By.XPATH, "//div[contains(@class, 'tab') or contains(@class, 'option') or contains(@class, 'method')]//*[contains(text(), 'Username')]"),
        ]
        
        element_clicked = False
        for selector_by, selector_value in login_method_selectors:
            try:
                elements = driver.find_elements(selector_by, selector_value)
                if elements:
                    for elem in elements:
                        if elem.is_displayed() and elem.is_enabled():
                            elem.click()
                            element_clicked = True
                            print(f"   ✅ Clicked: Login with Username option")
                            time.sleep(2)
                            break
                if element_clicked:
                    break
            except Exception as e:
                continue
        
        if not element_clicked:
            # Coba cari dengan JavaScript injection buat pindah ke form dengan input username
            print(f"   ⚠️ Login method button not found, mencoba alternative...")
            try:
                # Find first visible username input dan focus
                all_inputs = driver.find_elements(By.TAG_NAME, "input")
                for inp in all_inputs:
                    name = inp.get_attribute('name') or ''
                    placeholder = inp.get_attribute('placeholder') or ''
                    input_type = inp.get_attribute('type') or 'text'
                    
                    if ('username' in name.lower() or 'username' in placeholder.lower()) and inp.is_displayed():
                        inp.click()
                        print(f"   ✅ Focused on username input field")
                        time.sleep(2)
                        element_clicked = True
                        break
                
                if not element_clicked:
                    print(f"   ⚠️ Tidak dapat menemukan pilihan login dengan username")
                    print(f"   ℹ️ Menggunakan default approach...")
            except Exception as e:
                print(f"   ⚠️ Error pada alternative: {str(e)}")
        
        return element_clicked
        
    except Exception as e:
        print(f"   ❌ Error memilih login method: {str(e)}")
        return False

def login_single_account(account: dict):
    """
    Login ke satu TikTok account
    Pilih "Login with Username" option
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
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        print(f"🌐 Navigating ke TikTok login...")
        driver.get("https://www.tiktok.com/login")
        
        time.sleep(5)
        take_screenshot(driver, account, "login_page")
        
        # Pilih login method "Login with Username"
        print(f"🔍 Memilih login method: Username")
        select_login_method(driver)
        
        # Screenshot setelah pilih login method
        time.sleep(2)
        take_screenshot(driver, account, "after_select_login_method")
        
        # Find username field
        print(f"🔍 Mencari username field...")
        username_found = False
        username_input = None
        
        username_selectors = [
            (By.NAME, "username"),
            (By.CSS_SELECTOR, 'input[name="username"]'),
            (By.CSS_SELECTOR, 'input[placeholder*="Username"]'),
            (By.XPATH, '//input[contains(@placeholder, "Username") or contains(@placeholder, "Email")]'),
        ]
        
        for selector_by, selector_value in username_selectors:
            try:
                elements = driver.find_elements(selector_by, selector_value)
                if elements:
                    for elem in elements:
                        if elem.is_displayed() and elem.is_enabled():
                            username_input = elem
                            username_found = True
                            print(f"   ✅ Found username field")
                            break
                if username_found:
                    break
            except Exception as e:
                continue
        
        if not username_found:
            all_inputs = driver.find_elements(By.TAG_NAME, "input")
            for inp in all_inputs:
                if inp.is_displayed() and inp.is_enabled():
                    placeholder = inp.get_attribute('placeholder') or ''
                    input_type = inp.get_attribute('type') or 'text'
                    if 'username' in str(placeholder).lower() or 'email' in str(placeholder).lower():
                        username_input = inp
                        username_found = True
                        print(f"   ✅ Found username field by placeholder")
                        break
                    elif input_type == 'text' and not username_input:
                        username_input = inp
        
        if not username_input:
            raise Exception("Tidak dapat menemukan field username")
        
        time.sleep(1)
        username_input.clear()
        username_input.send_keys(username)
        print(f"✅ Username input: {username}")
        
        time.sleep(1)
        take_screenshot(driver, account, "username_filled")
        
        # Find password field
        print(f"(   🔍 Mencari password field...")
        password_input = None
        
        password_selectors = [
            (By.NAME, "password"),
            (By.CSS_SELECTOR, 'input[name="password"]'),
            (By.CSS_SELECTOR, 'input[type="password"]'),
            (By.XPATH, '//input[@type="password"]'),
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
                            print(f"   ✅ Found password field")
                            break
                if password_found:
                    break
            except Exception as e:
                continue
        
        if not password_input:
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
        
        time.sleep(1)
        password_input.clear()
        password_input.send_keys(password)
        print(f"✅ Password input: {'*' * 10}")
        
        time.sleep(1)
        take_screenshot(driver, account, "password_filled")
        
        # Submit login
        print(f"📤 Submit login...")
        password_input.send_keys("\n")
        
        print(f"⏳ Waiting for login process (10 seconds)...")
        time.sleep(10)
        
        current_url = driver.current_url
        page_source = driver.page_source.lower()
        
        print(f"🔍 Current URL: {current_url}")
        
        need_otp = 'otp' in current_url.lower() or 'verification' in current_url.lower() or 'two-factor' in page_source
        need_email = 'email' in current_url and 'verify' in current_url
        
        if need_otp or need_email:
            take_screenshot(driver, account, "verification_page")
        
        if need_otp:
            print(f"\n⚠️ OTP VERIFICATION REQUIRED!")
            otp_code = input("   MASUKKAN OTP CODE: ")
            
            otp_field = None
            try:
                otp_selectors = [
                    (By.CSS_SELECTOR, 'input[placeholder*="code"]'),
                    (By.CSS_SELECTOR, 'input[placeholder*="OTP"]'),
                    (By.CSS_SELECTOR, 'input[name="otp"]'),
                ]
                for selector_by, selector_value in otp_selectors:
                    elements = driver.find_elements(selector_by, selector_value)
                    if elements:
                        for elem in elements:
                            if elem.is_displayed() and elem.is_enabled():
                                otp_field = elem
                                break
                    if otp_field:
                        break
            except:
                pass
            
            if otp_field:
                otp_field.clear()
                otp_field.send_keys(otp_code)
                time.sleep(2)
                otp_field.send_keys("\n")
            
            time.sleep(10)
        
        if need_email:
            print(f"\n⚠️ EMAIL VERIFICATION REQUIRED!")
            take_screenshot(driver, account, "email_verification")
            input("   [TEKAN ENTER SETELAH VERIFICATION SELESAI]")
            time.sleep(5)
        
        final_url = driver.current_url
        print(f"🔍 Final URL: {final_url}")
        
        time.sleep(3)
        profile_url = f"https://www.tiktok.com/@{username}"
        print(f"🌐 Navigating ke profile: {profile_url}")
        driver.get(profile_url)
        time.sleep(5)
        
        take_screenshot(driver, account, "profile_page")
        
        page_source = driver.page_source.lower()
        if username.lower() in page_source:
            print(f"✅ LOGIN SUKSES: @{username}")
            
            take_screenshot(driver, account, "login_success")
            
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
            return {
                'username': username,
                'success': False,
                'error': 'Profile tidak valid'
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
        if driver:
            try:
                time.sleep(3)
                driver.quit()
            except:
                pass

def multi_account_login():
    """Login ke semua 12 TikTok accounts"""
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium tidak tersedia!")
        return
    
    config = load_config()
    accounts = config['accounts']
    
    print("\n" + "="*80)
    print("🚀 JENDRALBOT - MULTI-ACCOUNT TIKTOK AUTH (LOGIN WITH USERNAME)")
    print("="*80)
    print(f"📱 Total accounts: {len(accounts)}")
    print(f"📸 Screenshots: {SCREENSHOTS_DIR}")
    print(f"⏱️ Estimated time: {len(accounts) * 3-5} minutes")
    print("="*80 + "\n")
    
    results = []
    
    for i, account in enumerate(accounts):
        print(f"\n{'='*80}")
        print(f"🔐 ACCOUNT {i+1}/{len(accounts)}")
        print(f"{'='*80}")
        
        result = login_single_account(account)
        results.append(result)
        
        if i < len(accounts) - 1:
            print(f"\n⏸️ Waiting 5 seconds...")
            time.sleep(5)
    
    print("\n" + "="*80)
    print("📊 MULTI-ACCOUNT LOGIN SUMMARY")
    print("="*80)
    
    success_count = sum(1 for r in results if r['success'])
    fail_count = len(results) - success_count
    
    print(f"✅ Successful: {success_count}/{len(accounts)}")
    print(f"❌ Failed: {fail_count}/{len(accounts)}")
    
    if success_count > 0:
        print(f"\n✅ Screenshots: {SCREENSHOTS_DIR}/")
    
    if fail_count > 0:
        print(f"\n⚠️ Failed accounts:")
        for result in results:
            if not result['success']:
                print(f"   - @{result['username']}: {result.get('error', 'Unknown')}")
    
    print(f"\n💾 Sessions saved untuk {success_count} accounts")

def main():
    print("🎯 MULTI-ACCOUNT TIKTOK AUTH - LOGIN WITH USERNAME")
    print("📸 Screenshots akan diambil untuk setiap PROFIL!")
    
    try:
        multi_account_login()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()