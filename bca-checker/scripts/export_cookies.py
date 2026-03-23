#!/tmp/bca-venv/bin/python3
"""
Step 1: Lo login manual di Chromium, script nunggu, lalu export cookies.
Jalankan sekali saja. Cookies disimpan ke ~/.openclaw/bca_cookies.json

Usage:
  python3 export_cookies.py
  
Setelah dijalankan:
1. Browser akan buka KlikBCA
2. Login MANUAL (klik sendiri, isi PIN sendiri, approve OOB di HP)
3. Setelah berhasil masuk dashboard, tekan ENTER di terminal
4. Cookies otomatis tersimpan
"""

import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

COOKIES_FILE = Path("/home/openclaw/.openclaw/bca_cookies.json")

def export_cookies():
    print("🔐 BCA Cookie Exporter")
    print("=" * 50)
    print("1. Browser akan buka KlikBCA")
    print("2. Login MANUAL (isi User ID + PIN + approve OOB di HP)")
    print("3. Setelah masuk dashboard, tekan ENTER di terminal ini")
    print("4. Cookies tersimpan → script bca_check.py bisa jalan tanpa OOB")
    print("=" * 50)
    input("\nTekan ENTER untuk buka browser...")

    with sync_playwright() as p:
        # Pakai non-headless agar lo bisa login manual
        try:
            browser = p.chromium.launch(
                executable_path="/usr/bin/chromium",
                headless=False,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )
        except Exception:
            browser = p.chromium.launch(
                headless=False,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto("https://ibank.klikbca.com/")
        
        print("\n⏳ Browser terbuka. Silakan login manual...")
        print("   Setelah masuk dashboard BCA, kembali ke terminal ini dan tekan ENTER")
        input("\n[ENTER setelah login berhasil] ")
        
        # Export cookies
        cookies = context.cookies()
        
        COOKIES_FILE.write_text(json.dumps(cookies, indent=2))
        print(f"\n✅ {len(cookies)} cookies tersimpan ke: {COOKIES_FILE}")
        
        browser.close()
    
    print("\n✅ Done! Sekarang jalankan: python3 bca_check.py")

if __name__ == "__main__":
    export_cookies()
