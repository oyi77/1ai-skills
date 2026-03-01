#!/usr/bin/env python3
"""
Lynx.id Product Automation Script
Deploy "BerkahKarya All-Access Pass" - Rp 499,000
"""

import os
import time
import json
from pathlib import Path
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Configuration
LYNX_URL = "https://lynk.id/login"
EMAIL = "ketananna@yahoo.com"
PASSWORD = "1Milyarberakh$"
PRODUCT_NAME = "BerkahKarya All-Access Pass"
PRODUCT_PRICE = "499000"
PRODUCT_CATEGORY = "Digital Product"
PRODUCT_DESCRIPTION = """🔥 BERKAHKARYA ALL-ACCESS PASS - Rp 499.000 (Dari Rp 2.499.000)

Akses SEUMUR HIDUP ke 14+ Tools AI Premium BerkahKarya:

✅ Agency Performance Ad OS - Kelola iklan & scaling ads
✅ AURA Beauty Studio - Edit foto profesional AI
✅ Guru Pintar AI - Buat konten edukasi otomatis
✅ JobMagnet - Temukan & posting lowongan kerja
✅ Social Media Manager - Auto post ke semua platform
✅ Email Marketing Suite - Campaign & follow-up otomatis
✅ Analytics Dashboard - Track performa semua channel
✅ WhatsApp Business Bot - Customer service otomatis
✅ TikTok Content Generator - Buat video viral AI
✅ Instagram Reels Maker - Konten short-form otomatis
✅ YouTube Shorts Creator - Upload & optimasi video
✅ SEO Optimizer - Ranking tools & keyword research
✅ Lead Generation System - Scrape & qualify leads
✅ CRM & Pipeline Management - Track deals & conversions

🎁 BONUS:
- Blueprint Scaling Veris (Ads Mastery)
- Weekly Live Support dari Veris (Ads Master)
- Free Updates Selamanya
- Private Community Access

⏰ PROMO TERBATAS - HARGA AKAN NAIK BESOK!"""

# Assets paths
ASSETS_DIR = "/home/openclaw/.openclaw/workspace/output/bundle_assets"
ASSETS = {
    "hero": os.path.join(ASSETS_DIR, "master_key_hero.jpg"),
    "grid": os.path.join(ASSETS_DIR, "arsenal_grid.jpg"),
    "infographic": os.path.join(ASSETS_DIR, "bundle_master_infographic.jpg")
}

class LynxAutomator:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Setup Chrome WebDriver"""
        print("🔧 Setting up Chrome WebDriver (undetected)...")

        chrome_options = uc.ChromeOptions()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Point to installed chromium binary if it's not the default google-chrome
        # On this environment, it's likely /usr/bin/chromium or /usr/bin/google-chrome
        # Let's try to let UC find it or specify if we know
        # chrome_options.binary_location = "/usr/bin/chromium"

        try:
             # Use undetected-chromedriver
             # Force version 144 to match installed browser
             self.driver = uc.Chrome(options=chrome_options, version_main=144)
        except Exception as e:
             print(f"⚠️ UC Driver install failed: {e}")
             # Fallback or re-raise
             raise e

        self.wait = WebDriverWait(self.driver, 10)

        print("✅ WebDriver setup complete")

    def login(self):
        """Login to Lynx.id"""
        print(f"🔐 Logging in to Lynx.id as {EMAIL}...")

        try:
            self.driver.get(LYNX_URL)
            print(f"📍 Navigated to {LYNX_URL}")

            # Wait for page load
            time.sleep(5)
            self.take_screenshot("01b_login_loaded.png")

            # Save page source for debugging
            with open("output/lynx_source.html", "w") as f:
                f.write(self.driver.page_source)

            # Find email field and fill
            # Correct selector from source is name="username"
            try:
                email_field = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                print("✅ Found email field")
                email_field.clear()
                email_field.send_keys(EMAIL)
                print("✅ Email entered")
            except Exception as e:
                print(f"❌ Could not find email field: {e}")
                raise e
            
            # Password field
            # <input id="pwd1" type="password" name="password" ...>
            try:
                password_field = self.driver.find_element(By.NAME, "password")
                password_field.send_keys(PASSWORD)
                print("✅ Password entered")
            except Exception as e:
                print(f"❌ Could not find password field: {e}")
                raise e

            # Submit
            # <button type="submit" ...>Sign In</button>
            try:
                submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                submit_btn.click()
                print("🚀 Login form submitted")
            except Exception as e:
                print(f"❌ Could not find submit button: {e}")
                raise e

            # Wait for login to complete
            time.sleep(5)

            # Check if login successful
            if "dashboard" in self.driver.current_url.lower():
                print("✅ Login successful!")
                return True
            else:
                print(f"❌ Login failed. Current URL: {self.driver.current_url}")
                return False

        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False

    def navigate_to_create_product(self):
        """Navigate to create product page"""
        print("📦 Navigating to create product page...")

        try:
            # Look for "Add Product" or "Create Product" button/link
            # Try multiple possible selectors
            selectors = [
                "//button[contains(text(), 'Digital Product')]",
                "//a[contains(text(), 'Digital Product')]",
                "//span[contains(text(), 'Digital Product')]",
                "//div[contains(text(), 'Digital Product')]",
                "//a[contains(text(), 'Add Product')]",
                "//a[contains(text(), 'Create Product')]",
                "//a[contains(text(), 'Tambah Produk')]",
                "//button[contains(text(), 'Add Product')]",
                "//button[contains(text(), 'Create Product')]",
                "//a[@href='/products/create']",
                "//a[@href='/dashboard/products/add']",
            ]

            for selector in selectors:
                try:
                    element = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    element.click()
                    print(f"✅ Clicked on product button using selector: {selector}")
                    time.sleep(2)
                    break
                except:
                    continue
            else:
                print("❌ Could not find product creation button")
                return False

            return True

        except Exception as e:
            print(f"❌ Navigation error: {str(e)}")
            return False

    def fill_product_form(self):
        """Fill the product creation form"""
        print("📝 Filling product form...")

        try:
            # Product Name
            name_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "name"))
            )
            name_field.send_keys(PRODUCT_NAME)
            print(f"✅ Product name: {PRODUCT_NAME}")

            # Price
            price_field = self.driver.find_element(By.NAME, "price")
            price_field.send_keys(PRODUCT_PRICE)
            print(f"✅ Price: Rp {PRODUCT_PRICE}")

            # Category (if exists)
            try:
                category_field = self.driver.find_element(By.NAME, "category")
                category_field.send_keys(PRODUCT_CATEGORY)
                print(f"✅ Category: {PRODUCT_CATEGORY}")
            except:
                print("⚠️ Category field not found")

            # Description
            desc_field = self.driver.find_element(By.NAME, "description")
            desc_field.send_keys(PRODUCT_DESCRIPTION)
            print("✅ Description filled")

            return True

        except Exception as e:
            print(f"❌ Form filling error: {str(e)}")
            return False

    def upload_assets(self):
        """Upload product assets"""
        print("📤 Uploading assets...")

        try:
            # Check if assets exist
            for key, path in ASSETS.items():
                if not os.path.exists(path):
                    print(f"⚠️ Asset not found: {path}")
                    continue

                # Try to find file upload inputs
                file_inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")

                if file_inputs:
                    for i, file_input in enumerate(file_inputs):
                        if i < len(ASSETS):
                            key_name = list(ASSETS.keys())[i]
                            path_name = ASSETS[key_name]
                            file_input.send_keys(os.path.abspath(path_name))
                            print(f"✅ Uploaded: {key_name}")
                            time.sleep(1)
                else:
                    print("⚠️ No file upload inputs found")

            return True

        except Exception as e:
            print(f"❌ Upload error: {str(e)}")
            return False

    def submit_form(self):
        """Submit the product form"""
        print("💾 Submitting form...")

        try:
            # Find submit button
            submit_selectors = [
                "//button[@type='submit']",
                "//button[contains(text(), 'Save')]",
                "//button[contains(text(), 'Publish')]",
                "//button[contains(text(), 'Create')]",
            ]

            for selector in submit_selectors:
                try:
                    submit_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    submit_btn.click()
                    print("✅ Form submitted")
                    time.sleep(3)
                    break
                except:
                    continue

            return True

        except Exception as e:
            print(f"❌ Submit error: {str(e)}")
            return False

    def take_screenshot(self, filename):
        """Take a screenshot"""
        try:
            screenshot_dir = "/home/openclaw/.openclaw/workspace/output/screenshots/lynx"
            os.makedirs(screenshot_dir, exist_ok=True)
            filepath = os.path.join(screenshot_dir, filename)
            self.driver.save_screenshot(filepath)
            print(f"📸 Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Screenshot error: {str(e)}")
            return None

    def run(self):
        """Run the full automation"""
        print("\n🚀 STARTING LYNX.ID AUTOMATION\n")
        print("="*50)

        try:
            # Step 1: Setup
            self.setup_driver()

            # Screenshot 1: Login page
            self.take_screenshot("01_login_page.png")

            # Step 2: Login
            if not self.login():
                raise Exception("Login failed")

            # Screenshot 2: Dashboard
            self.take_screenshot("02_dashboard.png")

            # Step 3: Navigate to create product
            if not self.navigate_to_create_product():
                print("⚠️ Could not auto-navigate, please manually go to create product page")
                input("Press Enter after navigating to create product page...")

            # Screenshot 3: Empty form
            self.take_screenshot("03_empty_form.png")

            # Step 4: Fill form
            if not self.fill_product_form():
                raise Exception("Form filling failed")

            # Screenshot 4: Filled form
            self.take_screenshot("04_filled_form.png")

            # Step 5: Upload assets
            if not self.upload_assets():
                print("⚠️ Asset upload had issues, continuing...")

            # Step 6: Submit
            if not self.submit_form():
                print("⚠️ Submit failed, please manually click submit button")
                input("Press Enter after submitting...")

            # Screenshot 5: Result
            self.take_screenshot("05_result.png")

            print("\n✅ AUTOMATION COMPLETE")
            print("="*50)
            print("\n📊 SUMMARY:")
            print(f"- Product: {PRODUCT_NAME}")
            print(f"- Price: Rp {PRODUCT_PRICE}")
            print(f"- Screenshots saved in: output/screenshots/lynx/")

            return True

        except Exception as e:
            print(f"\n❌ AUTOMATION FAILED: {str(e)}")
            return False

        finally:
            # Keep browser open for inspection
            print("\n⏸️ Browser will stay open for inspection...")
            print("Close it manually or press Ctrl+C to exit")
            try:
                input()
            except KeyboardInterrupt:
                pass
            finally:
                if self.driver:
                    self.driver.quit()

if __name__ == "__main__":
    # Run automation
    automator = LynxAutomator(headless=False)
    success = automator.run()

    if success:
        print("\n✅ SUCCESS! Product deployed to Lynx.id")
    else:
        print("\n❌ FAILED! Check screenshots for debugging")
