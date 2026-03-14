#!/usr/bin/env python3
"""
BCA Balance Checker via Playwright
Handles KlikBCA frameset + anti-bot properly.

Usage:
  python3 bca_playwright.py
  python3 bca_playwright.py --save   # also save to Supabase
  python3 bca_playwright.py --json   # JSON output
"""
import argparse, json, os, sys, time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

BCA_USER = os.getenv("BCA_USER", "MUCHAMMA6064")
BCA_PASS = os.getenv("BCA_PASS", "242424")
SUPABASE_URL = "https://juoralxnkmfrnpmkiywk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1b3JhbHhua21mcm5wbWtpeXdrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MzM5NjU0MywiZXhwIjoyMDg4OTcyNTQzfQ.ghb9G0EbaYdESNcGfvYOONuAGBtcLWOD8HMacMnLnyI"

CACHE = Path("/tmp/bca_cache")
CACHE.mkdir(exist_ok=True)


def parse_idr(text):
    """Extract IDR amount from text like '1.234.567,89' or '0,37'."""
    import re
    # Indonesian format: dots as thousand sep, comma as decimal
    text = text.strip().replace(" ", "")
    # Remove IDR, Rp prefix
    text = re.sub(r'[IDRRp]', '', text).strip()
    # Handle Indonesian format (1.234.567,89)
    if ',' in text:
        text = text.replace('.', '').replace(',', '.')
    else:
        text = text.replace('.', '')
    try:
        return float(text)
    except:
        return 0.0


def check_balance(save_to_supabase=False, json_output=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--window-size=1280,800",
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.130 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            java_script_enabled=True,
            ignore_https_errors=False,
            extra_http_headers={
                "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            }
        )
        # Remove webdriver flag
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['id-ID', 'id', 'en-US']});
        """)
        page = context.new_page()

        try:
            # Step 1: Load login page
            page.goto("https://ibank.klikbca.com/", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=15000)

            # Step 2: Fill login form
            page.fill("#txt_user_id", BCA_USER)
            page.wait_for_timeout(300)
            page.fill("#txt_pswd", BCA_PASS)
            page.wait_for_timeout(300)
            page.click("#btnSubmit")
            page.wait_for_load_state("networkidle", timeout=15000)
            page.wait_for_timeout(2000)

            # Step 3: Check logged in
            if "authentication.do?value(actions)=block" in page.url:
                raise Exception("Login blocked — too many attempts or session conflict")

            if "welcome" not in page.url and "authentication.do" in page.url:
                # Check content frame
                pass

            # Step 4: Navigate to account info via menu frame
            # KlikBCA uses frameset — access menu frame
            menu_frame = page.frame("menu")
            if menu_frame:
                # Click Account Information in menu
                acct_link = menu_frame.locator("a", has_text="Account Information")
                if acct_link.count() > 0:
                    acct_link.first.click()
                    page.wait_for_timeout(2000)
            else:
                # Direct navigation to account info within session
                atm_frame = page.frame("atm")
                if atm_frame:
                    atm_frame.goto("https://ibank.klikbca.com/accountstmt.do?value(actions)=acct_info")
                    page.wait_for_timeout(2000)

            # Step 5: Get content frame balance
            balances = []
            for frame_name in ["atm", "content", None]:
                try:
                    target = page.frame(frame_name) if frame_name else page
                    if not target:
                        continue
                    text = target.inner_text("body") if target else ""

                    import re
                    # Look for balance patterns
                    lines = text.split("\n")
                    for line in lines:
                        if any(kw in line for kw in ["Tabungan", "Balance", "Saldo", "IDR"]):
                            amounts = re.findall(r'[\d.,]+', line)
                            for amt in amounts:
                                val = parse_idr(amt)
                                if val >= 0:
                                    balances.append({"line": line[:80], "amount": val, "frame": frame_name})
                except Exception as e:
                    pass

            # Step 6: Try account statement page directly
            if not balances:
                try:
                    atm_frame = page.frame("atm")
                    if atm_frame:
                        atm_frame.goto(
                            "https://ibank.klikbca.com/accountstmt.do?value(actions)=acct_info",
                            wait_until="networkidle",
                            timeout=15000
                        )
                        page.wait_for_timeout(2000)
                        text = atm_frame.inner_text("body")
                        import re
                        for line in text.split("\n"):
                            amounts = re.findall(r'[\d.,]+', line)
                            for amt in amounts:
                                val = parse_idr(amt)
                                if val >= 0 and ("Tabungan" in line or "Balance" in line or "Saldo" in line or "1131323722" in line):
                                    balances.append({"line": line[:80], "amount": val, "frame": "atm"})
                except Exception as e:
                    print(f"atm frame nav error: {e}", file=sys.stderr)

            # Screenshot for debug
            page.screenshot(path=str(CACHE / "bca_debug.png"))

            # Get all frame texts for parsing
            all_text = []
            for frame in page.frames:
                try:
                    t = frame.inner_text("body")
                    if t.strip():
                        all_text.append(t)
                except:
                    pass
            combined = "\n".join(all_text)

            # Parse balance from all text
            import re
            # Look for the specific account number
            acct_section = ""
            idx = combined.find("1131323722")
            if idx > -1:
                acct_section = combined[max(0,idx-100):idx+300]

            # Find IDR amounts
            idr_amounts = re.findall(r'([\d]{1,3}(?:[.,][\d]{3})*(?:[.,][\d]{2})?)', combined)

            result = {
                "checked_at": datetime.now().isoformat(),
                "account": "1131323722",
                "user": BCA_USER,
                "url_after_login": page.url,
                "frames": [f.name for f in page.frames if f.name],
                "balance_raw": acct_section[:200] if acct_section else combined[:300],
                "balances": balances[:5],
                "primary_balance": balances[0]["amount"] if balances else 0.0,
            }

            # Save cache
            (CACHE / "last_balance.json").write_text(json.dumps(result))

            if save_to_supabase and balances:
                try:
                    from supabase import create_client
                    client = create_client(SUPABASE_URL, SUPABASE_KEY)
                    today = datetime.now().strftime("%Y-%m-%d")
                    client.table("cashflow").upsert({
                        "date": today,
                        "bank_balance_idr": result["primary_balance"],
                        "notes": f"Auto BCA check {datetime.now().strftime('%H:%M')}",
                    }, on_conflict="date").execute()
                    result["supabase_saved"] = True
                except Exception as e:
                    result["supabase_error"] = str(e)

            return result

        finally:
            browser.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_out")
    args = parser.parse_args()

    result = check_balance(save_to_supabase=args.save, json_output=args.json_out)

    bal = result.get("primary_balance", 0)
    if args.json_out:
        print(json.dumps(result, indent=2))
    else:
        print(f"BCA Balance Check — {result['checked_at'][:16]}")
        print(f"Account: {result['account']}")
        print(f"Balance: IDR {bal:,.2f}")
        if bal < 50000:
            print("🚨 EMERGENCY: Balance < IDR 50K")
        elif bal < 500000:
            print("⚠️  WARNING: Balance < IDR 500K")
        else:
            print("✅ Balance OK")
        print(f"\nDebug frames: {result.get('frames', [])}")
        print(f"Raw text snippet: {result.get('balance_raw', '')[:150]}")


if __name__ == "__main__":
    main()
