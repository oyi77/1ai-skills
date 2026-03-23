#!/usr/bin/env python3
"""
BCA KlikBCA Scraper — Stealth version
Uses playwright-stealth to bypass Imperva/Distil bot detection
"""
import os, sys, json, time, re
from datetime import datetime, timedelta
from pathlib import Path

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

def run(headless=True):
    from playwright.sync_api import sync_playwright
    try:
        from playwright_stealth import stealth_sync
        has_stealth = True
    except ImportError:
        has_stealth = False

    result = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "saldo": None, "mutasi": [], "error": None}

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--no-sandbox", "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--window-size=1280,800",
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="id-ID",
            timezone_id="Asia/Jakarta",
            extra_http_headers={
                "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
                "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
            }
        )
        
        page = context.new_page()
        if has_stealth:
            stealth_sync(page)
            print("Stealth mode active")
        
        try:
            # Load cookies if available and recent
            if COOKIES_FILE.exists():
                age = time.time() - COOKIES_FILE.stat().st_mtime
                if age < 3600:  # cookies < 1 hour old
                    context.add_cookies(json.loads(COOKIES_FILE.read_text()))
                    print(f"Loaded cookies ({int(age)}s old)")
            
            # Navigate
            print("Opening KlikBCA...")
            page.goto("https://ibank.klikbca.com", timeout=30000, wait_until="domcontentloaded")
            time.sleep(3)
            
            # Check if already logged in
            frames = page.frames
            logged_in = len(frames) > 2
            
            if not logged_in:
                print("Not logged in, attempting login...")
                print(f"Current URL: {page.url}")
                
                # Random delay to appear human
                time.sleep(2)
                
                # Fill with natural delays
                user_field = page.locator('#txt_user_id')
                user_field.click()
                time.sleep(0.3)
                user_field.type(BCA_USER, delay=80)
                time.sleep(0.8)
                
                pass_field = page.locator('#txt_pswd')
                pass_field.click()
                time.sleep(0.3)
                pass_field.type(BCA_PASS, delay=100)
                time.sleep(1)
                
                page.locator('#btnSubmit').click()
                
                # Wait for login to complete
                try:
                    page.wait_for_url("**/authentication.do*", timeout=25000)
                    time.sleep(4)
                except:
                    time.sleep(5)
                
                frames = page.frames
                print(f"Post-login: {page.url}, frames={len(frames)}")
                
                if len(frames) <= 1 and 'login' in page.url.lower():
                    page_text = page.inner_text("body").lower()
                    if "salah" in page_text or "block" in page_text:
                        result["error"] = "Login gagal: akun mungkin temporary blocked (terlalu banyak attempt). Tunggu 30 menit."
                    elif "salah" in page_text:
                        result["error"] = "Login gagal: User ID atau PIN salah"
                    else:
                        result["error"] = "Login gagal: " + page.inner_text("body")[:200]
                    return result
                
                # Save fresh cookies
                cookies = context.cookies()
                COOKIES_FILE.write_text(json.dumps(cookies, indent=2))
                print(f"Saved {len(cookies)} cookies")
            
            print("Logged in! Getting frames...")
            frames = page.frames
            print(f"Frames: {[(f.name, f.url[:50]) for f in frames]}")
            
            menu_frame = next((f for f in frames if f.name == "menu"), None)
            atm_frame = next((f for f in frames if f.name == "atm"), None)
            
            if not menu_frame:
                result["error"] = "Login OK but frame structure not found"
                return result
            
            # === SALDO ===
            print("Getting saldo...")
            try:
                menu_frame.click("a[href='account_information_menu.htm']", timeout=5000)
                time.sleep(1.5)
                menu_frame.click("a[onclick*='balanceinquiry']", timeout=5000)
                time.sleep(2)
                
                content = atm_frame.inner_text("body")
                print("Saldo content:", content[:300])
                
                # Parse table
                rows = atm_frame.query_selector_all("table tr")
                for row in rows[1:]:
                    cells = [td.inner_text().strip() for td in row.query_selector_all("td")]
                    if cells and any(cells):
                        result["saldo"] = " | ".join(c for c in cells if c)
                        break
                
                if not result["saldo"]:
                    amounts = re.findall(r'[\d,\.]{5,}', content)
                    result["saldo"] = amounts[0] if amounts else content[:100]
                    
            except Exception as e:
                result["error"] = f"Saldo error: {e}"
            
            # === MUTASI ===
            print("Getting mutasi...")
            try:
                menu_frame.click("a[href='account_information_menu.htm']", timeout=3000)
                time.sleep(1)
                menu_frame.click("a[onclick*='accountstmt']", timeout=3000)
                time.sleep(2)
                
                now = datetime.now()
                start = now - timedelta(days=7)
                
                atm_frame.fill("#startDt", start.strftime("%d"), timeout=3000)
                atm_frame.select_option("#startMt", str(int(start.strftime("%m"))), timeout=3000)
                atm_frame.fill("#startYr", start.strftime("%Y"), timeout=3000)
                atm_frame.fill("#endDt", now.strftime("%d"), timeout=3000)
                atm_frame.select_option("#endMt", str(int(now.strftime("%m"))), timeout=3000)
                atm_frame.fill("#endYr", now.strftime("%Y"), timeout=3000)
                atm_frame.click('input[name="value(submit1)"]', timeout=3000)
                time.sleep(2)
                
                rows = atm_frame.query_selector_all("table tr")
                for row in rows[1:]:
                    cells = [td.inner_text().strip() for td in row.query_selector_all("td")]
                    if len(cells) >= 3 and cells[0] and re.search(r'\d', cells[0]):
                        result["mutasi"].append({
                            "tanggal": cells[0],
                            "keterangan": cells[1] if len(cells) > 1 else "",
                            "debet": cells[2] if len(cells) > 2 else "",
                            "kredit": cells[3] if len(cells) > 3 else "",
                        })
            except Exception as e:
                if not result.get("error"):
                    result["error"] = f"Mutasi error: {e}"
        
        except Exception as e:
            result["error"] = str(e)
        finally:
            browser.close()
    
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-browser", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    
    print(f"🏦 BCA Stealth Check — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    result = run(headless=not args.show_browser)
    
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result.get("error"): print(f"❌ {result['error']}")
        if result.get("saldo"): print(f"💰 Saldo: {result['saldo']}")
        if result.get("mutasi"):
            print(f"📋 {len(result['mutasi'])} transaksi:")
            for tx in result["mutasi"][:10]:
                print(f"  {tx.get('tanggal')} | {tx.get('keterangan','')[:40]} | -{tx.get('debet','')} +{tx.get('kredit','')}")
