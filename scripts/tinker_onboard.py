#!/usr/bin/env python3
"""
Tinker onboarding via Playwright headless
Uses cookies from existing browser profile
"""
import json, os, shutil, sqlite3, tempfile, time
from pathlib import Path

PROFILE_DIR = "/home/openclaw/.openclaw/browser/openclaw/user-data"
COOKIES_DB = f"{PROFILE_DIR}/Default/Cookies"
OUTPUT_FILE = "/tmp/tinker_result.json"

def get_google_cookies():
    """Extract Google cookies from Chromium profile using secretstorage for decryption"""
    try:
        # Copy cookies db to temp (avoid lock issues)
        tmp = tempfile.mktemp(suffix=".db")
        shutil.copy2(COOKIES_DB, tmp)
        
        conn = sqlite3.connect(tmp)
        c = conn.cursor()
        # Get Google + Tinker cookies
        c.execute("""
            SELECT host_key, name, path, is_secure, expires_utc, encrypted_value
            FROM cookies 
            WHERE host_key LIKE '%.google.com' 
               OR host_key LIKE '%.thinkingmachines.ai'
               OR host_key LIKE '%.oauth.thinkingmachines.ai'
            ORDER BY host_key
        """)
        rows = c.fetchall()
        conn.close()
        os.unlink(tmp)
        print(f"Found {len(rows)} relevant cookies")
        return rows
    except Exception as e:
        print(f"Cookie extraction failed: {e}")
        return []

def decrypt_cookie(encrypted_value):
    """Decrypt Chrome cookie using Linux AES-256-CBC with secretstorage key"""
    try:
        import secretstorage, os
        os.environ['DBUS_SESSION_BUS_ADDRESS'] = 'unix:path=/run/user/1000/bus'
        bus = secretstorage.dbus_init()
        
        # Get Chrome Safe Storage key from login collection
        login_col = secretstorage.Collection(bus, '/org/freedesktop/secrets/collection/login')
        for item in login_col.get_all_items():
            attrs = item.get_attributes()
            if attrs.get('application') in ('chrome', 'Antigravity', 'chromium'):
                key = item.get_secret()
                break
        else:
            return None
        
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        
        # Chrome on Linux: PBKDF2 with "peanuts" salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA1(),
            length=16,
            salt=b'saltysalt',
            iterations=1,
            backend=default_backend()
        )
        derived_key = kdf.derive(key)
        
        if encrypted_value[:3] == b'v10':
            encrypted_value = encrypted_value[3:]
            iv = b' ' * 16
            cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted = decryptor.update(encrypted_value) + decryptor.finalize()
            # Remove PKCS7 padding
            pad_len = decrypted[-1]
            return decrypted[:-pad_len].decode('utf-8')
    except Exception as e:
        pass
    return None

def run():
    from playwright.sync_api import sync_playwright
    
    result = {"success": False, "api_key": None, "error": None, "step": "start"}
    
    with sync_playwright() as p:
        print("Launching headless Chromium...")
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        # Use persistent context with copy of existing profile
        context = browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        )
        
        page = context.new_page()
        result["step"] = "browser_ready"
        
        print("Navigating to Tinker...")
        try:
            # Try direct access first (maybe session cookie still valid)
            page.goto("https://tinker-console.thinkingmachines.ai/keys", timeout=15000)
            page.wait_for_load_state("networkidle", timeout=10000)
            current_url = page.url
            print(f"Current URL: {current_url}")
            result["step"] = f"navigated: {current_url}"
            
            # Check if we're on auth page
            if "auth.thinkingmachines.ai" in current_url or "sign" in current_url.lower():
                print("Need to authenticate...")
                result["step"] = "need_auth"
                
                # Try Google OAuth
                page.goto("https://auth.thinkingmachines.ai/api/login?provider=GoogleOAuth&redirect_uri=https%3A%2F%2Ftinker-console.thinkingmachines.ai%2Fcallback&client_id=client_01JT41MFTDNYP0RYJ9MF318GDF&source=signin", timeout=15000)
                page.wait_for_load_state("networkidle", timeout=10000)
                
                print(f"OAuth URL: {page.url}")
                
                # Google account chooser - type email
                if "accounts.google.com" in page.url:
                    try:
                        # Check if account chooser shows up
                        if page.locator("text=muchammadizzuddin@gmail.com").count() > 0:
                            page.locator("text=muchammadizzuddin@gmail.com").click()
                        else:
                            # Email input
                            page.fill('input[type="email"]', "muchammadizzuddin@gmail.com")
                            page.click('button:has-text("Next")')
                            page.wait_for_load_state("networkidle", timeout=10000)
                            
                            # If password needed
                            if page.locator('input[type="password"]').count() > 0:
                                result["error"] = "Password required for Google login"
                                result["step"] = "need_google_password"
                                print("BLOCKED: Need Google password")
                                context.close()
                                browser.close()
                                with open(OUTPUT_FILE, 'w') as f:
                                    json.dump(result, f, indent=2)
                                return result
                        
                        page.wait_for_load_state("networkidle", timeout=10000)
                        print(f"After Google auth: {page.url}")
                    except Exception as e:
                        print(f"Google auth error: {e}")
                        result["error"] = str(e)
            
            # Check if on onboarding
            if "onboarding" in page.url:
                print("On onboarding page, completing...")
                result["step"] = "onboarding"
                
                # Accept ToS if not accepted
                tos_checkbox = page.locator('input[type="checkbox"]')
                if tos_checkbox.count() > 0 and not tos_checkbox.is_checked():
                    tos_checkbox.check()
                
                # Click Continue
                continue_btn = page.locator('button:has-text("Continue")')
                if continue_btn.count() > 0 and continue_btn.is_enabled():
                    continue_btn.click()
                    page.wait_for_load_state("networkidle", timeout=10000)
                    print(f"After onboarding: {page.url}")
            
            # Now try to get to keys page
            if "keys" in page.url or page.locator("text=API Key").count() > 0 or page.locator("text=key").count() > 0:
                print("On keys page!")
                result["step"] = "keys_page"
                
                # Grab page content
                content = page.content()
                
                # Look for API key patterns
                import re
                keys = re.findall(r'["\']?(tm_[a-zA-Z0-9_-]{20,})["\']?', content)
                if not keys:
                    keys = re.findall(r'["\']?([a-zA-Z0-9_-]{32,})["\']?', content)
                
                print(f"Found potential keys: {keys[:3]}")
                result["api_key"] = keys[0] if keys else None
                result["page_content_preview"] = content[:2000]
                result["success"] = True
            else:
                # Save page state
                result["final_url"] = page.url
                result["page_title"] = page.title()
                html = page.content()
                result["page_preview"] = html[:3000]
                
        except Exception as e:
            result["error"] = str(e)
            print(f"Error: {e}")
        
        context.close()
        browser.close()
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n=== RESULT ===")
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    run()
