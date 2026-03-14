#!/usr/bin/env python3
"""
Shopee Affiliate Login Script
Connect to existing Chrome instance and login via Gmail
"""

from playwright.sync_api import sync_playwright
import time
import sys

# Credentials
GMAIL_EMAIL = "nyamiresepdapur@gmail.com"
GMAIL_PASS = "1Milyarberkahbro$"

def main():
    with sync_playwright() as p:
        # Connect to existing browser
        print("Connecting to browser on port 9222...")
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        # Get existing context and page
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        
        print(f"Current URL: {page.url}")
        
        # Navigate to Google login
        print("Navigating to Google login...")
        page.goto("https://accounts.google.com/signin", wait_until="networkidle")
        time.sleep(2)
        
        # Check if already logged in
        if "myaccount.google.com" in page.url:
            print("Already logged in to Google!")
        else:
            # Enter email
            print("Entering email...")
            email_input = page.locator('input[type="email"]')
            if email_input.is_visible():
                email_input.fill(GMAIL_EMAIL)
                page.locator('button:has-text("Next"), #identifierNext').click()
                time.sleep(3)
            
            # Enter password
            print("Entering password...")
            pass_input = page.locator('input[type="password"]')
            if pass_input.is_visible():
                pass_input.fill(GMAIL_PASS)
                page.locator('button:has-text("Next"), #passwordNext').click()
                time.sleep(3)
        
        print(f"Final URL: {page.url}")
        
        # Now go to Shopee Affiliate
        print("Going to Shopee Affiliate...")
        page.goto("https://affiliate.shopee.co.id/", wait_until="networkidle")
        time.sleep(3)
        
        print(f"Shopee URL: {page.url}")
        print("Script completed!")
        
        # Keep browser open
        browser.close()

if __name__ == "__main__":
    main()
