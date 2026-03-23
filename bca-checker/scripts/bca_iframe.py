#!/usr/bin/env python3
"""
BCA KlikBCA Scraper — iframe-aware version
Based on: https://github.com/pentolbakso/klikBCAselenium
KlikBCA desktop uses iframe frames: 'menu' and 'atm' (content)
"""
import os, sys, json, time, re
from datetime import datetime, timedelta
from pathlib import Path

# Load env
env_file = Path("/home/openclaw/.openclaw/.env")
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

BCA_USER = os.environ.get("BCA_USER", "")
BCA_PASS = os.environ.get("BCA_PASS", "")

def run(headless=True):
    from playwright.sync_api import sync_playwright

    result = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "saldo": None, "mutasi": [], "error": None}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="id-ID",
            timezone_id="Asia/Jakarta",
        )
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = context.new_page()

        try:
            # Step 1: Login via ibank.klikbca.com
            print("Opening login page...")
            page.goto("https://ibank.klikbca.com", timeout=30000, wait_until="domcontentloaded")
            time.sleep(2)
            
            print(f"Login page URL: {page.url}")
            
            # ibank uses id="user_id" and id="pswd"
            # Fill login form
            try:
                page.fill('#user_id', BCA_USER, timeout=5000)
                page.fill('#pswd', BCA_PASS, timeout=5000)
            except:
                # Try name-based selectors
                page.fill('input[name="value(user_id)"]', BCA_USER, timeout=5000)
                page.fill('input[name="value(pswd)"]', BCA_PASS, timeout=5000)
            
            time.sleep(0.5)
            page.click('input[name="value(Submit)"]', timeout=5000)
            page.wait_for_load_state("domcontentloaded", timeout=20000)
            time.sleep(3)
            
            print(f"After login URL: {page.url}")
            
            # Check for frames (main structure of ibank)
            frames = page.frames
            print(f"Frames found: {[f.name for f in frames]}")
            
            # Get menu frame
            menu_frame = None
            content_frame = None
            for frame in frames:
                if frame.name == "menu":
                    menu_frame = frame
                elif frame.name == "atm":
                    content_frame = frame
            
            if not menu_frame:
                # Check if we're logged in at all
                all_text = page.inner_text("body")
                if "logout" in all_text.lower() or "selamat" in all_text.lower():
                    print("Logged in (no frames, single page)")
                    # Single page mode
                    result["saldo"] = "Login OK but frame structure changed"
                else:
                    result["error"] = "Login failed or page structure changed"
                    print("Page content:", all_text[:500])
                return result
            
            print("Found menu frame! Navigating to balance...")
            
            # Click Informasi Rekening in menu frame
            try:
                menu_frame.click("a[href='account_information_menu.htm']", timeout=5000)
                time.sleep(1)
            except:
                try:
                    menu_frame.get_by_text("Informasi Rekening").click(timeout=5000)
                    time.sleep(1)
                except Exception as e:
                    print(f"Menu click failed: {e}")
                    # Try direct URL
                    page.goto("https://ibank.klikbca.com/balanceinquiry.do", timeout=15000)
                    time.sleep(2)
            
            # Click Balance Inquiry submenu
            try:
                menu_frame.click("a[onclick*='balanceinquiry.do']", timeout=5000)
                time.sleep(2)
            except:
                try:
                    menu_frame.get_by_text("Saldo Rekening").click(timeout=3000)
                    time.sleep(2)
                except Exception as e:
                    print(f"Balance submenu click failed: {e}")
            
            # Get balance from content frame (atm frame)
            if content_frame:
                content = content_frame.inner_text("body")
                print("Content frame text:", content[:500])
                
                # Extract IDR amounts
                if "INFORMASI SALDO" in content.upper() or "SALDO" in content.upper():
                    # Parse table
                    rows = content_frame.query_selector_all("table tr")
                    for row in rows[1:]:
                        cells = [td.inner_text().strip() for td in row.query_selector_all("td")]
                        if len(cells) >= 4 and any(c for c in cells if c):
                            result["saldo"] = " | ".join(cells)
                            break
                    
                    if not result["saldo"]:
                        # Fallback: grab IDR amount from text
                        amounts = re.findall(r'[\d]{1,3}(?:[.,]\d{3})+(?:[.,]\d{2})?', content)
                        if amounts:
                            result["saldo"] = f"Saldo: {amounts[0]}"
                        else:
                            result["saldo"] = content[:300]
                else:
                    result["saldo"] = content[:300]
            else:
                # Try main page
                content = page.inner_text("body")
                amounts = re.findall(r'[\d]{1,3}(?:[.,]\d{3})+(?:[.,]\d{2})?', content)
                result["saldo"] = amounts[0] if amounts else "Parse failed: " + content[:200]
            
            # === Get Mutasi ===
            try:
                # Navigate back to menu
                menu_frame.click("a[onclick*='accountstmt.do']", timeout=3000)
                time.sleep(2)
                
                if content_frame:
                    # Fill date range
                    now = datetime.now()
                    start = now - timedelta(days=7)
                    
                    try:
                        content_frame.fill("#startDt", start.strftime("%d"), timeout=3000)
                        content_frame.select_option("#startMt", str(int(start.strftime("%m"))), timeout=3000)
                        content_frame.fill("#startYr", start.strftime("%Y"), timeout=3000)
                        content_frame.fill("#endDt", now.strftime("%d"), timeout=3000)
                        content_frame.select_option("#endMt", str(int(now.strftime("%m"))), timeout=3000)
                        content_frame.fill("#endYr", now.strftime("%Y"), timeout=3000)
                        content_frame.click('input[name="value(submit1)"]', timeout=3000)
                        time.sleep(3)
                        
                        # Parse mutasi table
                        rows = content_frame.query_selector_all("table tr")
                        for row in rows[1:]:
                            cells = [td.inner_text().strip() for td in row.query_selector_all("td")]
                            if len(cells) >= 3 and cells[0]:
                                result["mutasi"].append({
                                    "tanggal": cells[0],
                                    "keterangan": cells[1] if len(cells) > 1 else "",
                                    "debet": cells[2] if len(cells) > 2 else "",
                                    "kredit": cells[3] if len(cells) > 3 else "",
                                })
                    except Exception as e:
                        print(f"Mutasi form error: {e}")
            except Exception as e:
                print(f"Mutasi navigation error: {e}")
            
        except Exception as e:
            result["error"] = str(e)
        finally:
            browser.close()
    
    return result

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--show-browser", action="store_true")
    p.add_argument("--json", action="store_true", dest="as_json")
    args = p.parse_args()
    
    print(f"🏦 BCA Check (iframe mode) — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    result = run(headless=not args.show_browser)
    
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result.get("error"): print(f"❌ Error: {result['error']}")
        if result.get("saldo"): print(f"💰 Saldo: {result['saldo']}")
        if result.get("mutasi"): 
            print(f"📋 Mutasi ({len(result['mutasi'])} transaksi):")
            for tx in result["mutasi"][:10]:
                print(f"  {tx.get('tanggal')} | {tx.get('keterangan','')[:40]} | -{tx.get('debet','')} +{tx.get('kredit','')}")
