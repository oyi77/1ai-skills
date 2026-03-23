#!/usr/bin/env python3
"""
BCA KlikBCA Mobile Scraper
Menggunakan Playwright dengan mobile emulation untuk bypass bot detection.
Mobile browser lebih mudah masuk karena UI lebih simple + fingerprint beda.
"""
import os, sys, json, time, re
from datetime import datetime, timedelta
from pathlib import Path

# Load .env
env_file = Path("/home/openclaw/.openclaw/.env")
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

BCA_USER = os.environ.get("BCA_USER", "")
BCA_PASS = os.environ.get("BCA_PASS", "")
COOKIES_FILE = Path("/home/openclaw/.openclaw/bca_cookies.json")

# Mobile device configs - rotate untuk avoid detection
MOBILE_CONFIGS = [
    {
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "viewport": {"width": 390, "height": 844},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
    },
    {
        "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "viewport": {"width": 412, "height": 915},
        "device_scale_factor": 2.625,
        "is_mobile": True,
        "has_touch": True,
    },
    {
        "user_agent": "Mozilla/5.0 (Linux; Android 12; Samsung Galaxy S21) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 SamsungBrowser/22.0",
        "viewport": {"width": 360, "height": 800},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
    }
]

# KlikBCA mobile URL
KLIKBCA_URL = "https://m.klikbca.com"
KLIKBCA_IBANK = "https://ibank.klikbca.com"

def run_check(headless=True):
    from playwright.sync_api import sync_playwright
    
    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "saldo": None,
        "mutasi": [],
        "error": None,
        "method": "mobile"
    }

    import random
    config = random.choice(MOBILE_CONFIGS)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox", 
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--lang=id-ID,id",
            ]
        )
        
        context = browser.new_context(
            **config,
            locale="id-ID",
            timezone_id="Asia/Jakarta",
            permissions=["geolocation"],
            geolocation={"latitude": -6.2088, "longitude": 106.8456},  # Jakarta
            color_scheme="light",
            extra_http_headers={
                "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
            }
        )
        
        # Remove navigator.webdriver flag
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
            window.chrome = {runtime: {}};
        """)
        
        # Load saved cookies if available
        if COOKIES_FILE.exists():
            try:
                saved = json.loads(COOKIES_FILE.read_text())
                context.add_cookies(saved)
                print("Loaded existing cookies")
            except:
                pass
        
        page = context.new_page()
        
        try:
            # Try ibank first (desktop) with mobile UA
            print(f"Navigating to KlikBCA...")
            page.goto(KLIKBCA_IBANK, timeout=30000, wait_until="domcontentloaded")
            time.sleep(2)
            
            content = page.content().lower()
            page_url = page.url
            print(f"URL: {page_url}")
            print(f"Logged in: {any(x in content for x in ['logout', 'selamat datang', 'informasi rekening', 'saldo'])}")
            
            already_logged_in = any(x in content for x in ["logout", "selamat datang", "informasi rekening"])
            
            if not already_logged_in:
                print("Not logged in, attempting login...")
                
                # Wait for login form
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(1)
                
                # Take screenshot for debug
                page.screenshot(path="/tmp/bca_login_page.png")
                
                # Check page elements
                inputs = page.query_selector_all("input")
                print(f"Found {len(inputs)} input fields")
                for inp in inputs:
                    print(f"  input: name={inp.get_attribute('name')} type={inp.get_attribute('type')}")
                
                # Try login
                try:
                    # Human-like typing with delays
                    user_input = page.locator('input[name="txt_user_id"]').first
                    user_input.click()
                    time.sleep(0.3)
                    for char in BCA_USER:
                        user_input.type(char)
                        time.sleep(0.05 + random.random() * 0.1)
                    
                    time.sleep(0.5)
                    
                    pass_input = page.locator('input[name="txt_pswd"]').first
                    pass_input.click()
                    time.sleep(0.3)
                    for char in BCA_PASS:
                        pass_input.type(char)
                        time.sleep(0.05 + random.random() * 0.1)
                    
                    time.sleep(0.5)
                    page.locator('input[name="value(Submit)"]').click()
                    page.wait_for_load_state("networkidle", timeout=20000)
                    time.sleep(2)
                    
                    content = page.content().lower()
                    page.screenshot(path="/tmp/bca_after_login.png")
                    
                    if any(x in content for x in ["logout", "selamat datang", "informasi rekening"]):
                        print("Login successful!")
                        # Save fresh cookies
                        new_cookies = context.cookies()
                        COOKIES_FILE.write_text(json.dumps(new_cookies, indent=2))
                    else:
                        result["error"] = "Login failed — OOB/verification required or wrong credentials"
                        print(f"Login failed. Page title: {page.title()}")
                        return result
                        
                except Exception as e:
                    result["error"] = f"Login form error: {e}"
                    print(f"Login form error: {e}")
                    page.screenshot(path="/tmp/bca_error.png")
                    return result
            
            # === Get Saldo ===
            print("Getting saldo...")
            try:
                # Navigate to informasi rekening
                page.goto(f"{KLIKBCA_IBANK}/authentication.do?value(actions)=menu&value(CorporateID)=&value(BranchID)=&value(UserID)={BCA_USER}&value(NavigationID)=000", timeout=15000)
                time.sleep(1)
                
                # Click Informasi Rekening
                info_link = page.get_by_text("Informasi Rekening", exact=False).first
                if info_link:
                    info_link.click()
                    page.wait_for_load_state("networkidle", timeout=10000)
                    time.sleep(1)
                    
                    saldo_link = page.get_by_text("Saldo Rekening", exact=False).first
                    if saldo_link:
                        saldo_link.click()
                        page.wait_for_load_state("networkidle", timeout=10000)
                        time.sleep(1)
                        
                        # Parse saldo
                        content = page.content()
                        # Look for IDR amount pattern
                        matches = re.findall(r'IDR[\s,.\d]+|Rp[\s,.\d]+|\d{1,3}(?:\.\d{3})+,\d{2}', content)
                        if matches:
                            result["saldo"] = matches[0].strip()
                        else:
                            # Get all text from page
                            result["saldo"] = page.inner_text("body")[:500]
                else:
                    result["error"] = "Cannot find 'Informasi Rekening' link"
            except Exception as e:
                result["error"] = f"Saldo error: {e}"
                page.screenshot(path="/tmp/bca_saldo_error.png")
            
        except Exception as e:
            result["error"] = f"Browser error: {e}"
            try:
                page.screenshot(path="/tmp/bca_main_error.png")
            except:
                pass
        finally:
            browser.close()
    
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-browser", action="store_true", help="Show browser (non-headless)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    
    print(f"BCA Mobile Checker — {datetime.now()}")
    print(f"User: {BCA_USER}")
    print("---")
    
    result = run_check(headless=not args.show_browser)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Timestamp: {result['timestamp']}")
        if result.get('error'):
            print(f"❌ Error: {result['error']}")
        if result.get('saldo'):
            print(f"💰 Saldo: {result['saldo']}")
        if result.get('mutasi'):
            print(f"📋 Mutasi: {len(result['mutasi'])} transaksi")
        
        # Screenshots saved to /tmp/bca_*.png for debug
        from pathlib import Path
        screenshots = list(Path("/tmp").glob("bca_*.png"))
        if screenshots:
            print(f"\n📸 Screenshots: {[str(s) for s in screenshots]}")
