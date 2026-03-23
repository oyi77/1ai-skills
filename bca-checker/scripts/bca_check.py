#!/usr/bin/env python3
"""
BCA KlikBCA Scraper — Production Version
Reliable scraper for saldo + mutasi via ibank.klikbca.com

Approach:
- Playwright with anti-bot spoofing (iframe-aware)
- Cookie persistence untuk skip login tiap run
- Retry logic + proper error handling
- Mobile + desktop fallback

Usage:
  python3 bca_check.py                  # saldo + mutasi 7 hari
  python3 bca_check.py --saldo          # saldo saja
  python3 bca_check.py --mutasi         # mutasi 7 hari
  python3 bca_check.py --mutasi --days 30
  python3 bca_check.py --json           # output JSON
  python3 bca_check.py --show-browser   # non-headless untuk debug
"""
import os, sys, json, time, re, argparse
from datetime import datetime, timedelta
from pathlib import Path

# ── Load credentials ────────────────────────────────────────────────────────

def load_env():
    for path in [
        Path("/home/openclaw/.openclaw/.env"),
        Path(__file__).parents[3] / ".env",
    ]:
        if path.exists():
            for line in path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())
            break

load_env()

BCA_USER = os.environ.get("BCA_USER", "")
BCA_PASS = os.environ.get("BCA_PASS", "")
COOKIES_FILE = Path("/home/openclaw/.openclaw/bca_cookies.json")
COOKIE_MAX_AGE = 3600  # 1 hour

if not BCA_USER or not BCA_PASS:
    print(json.dumps({"error": "BCA_USER/BCA_PASS not set in .env"}))
    sys.exit(1)

# ── Browser setup ────────────────────────────────────────────────────────────

STEALTH_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
window.chrome = {runtime: {}};
"""

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

# ── Core scraper ─────────────────────────────────────────────────────────────

def get_frames(page):
    frames = page.frames
    return (
        next((f for f in frames if f.name == "menu"), None),
        next((f for f in frames if f.name == "atm"), None),
    )

def login(page, context):
    """Login and return (menu_frame, atm_frame). Raises on failure."""
    page.goto("https://ibank.klikbca.com", timeout=30000, wait_until="domcontentloaded")
    time.sleep(3)

    menu_frame, atm_frame = get_frames(page)
    if menu_frame:
        return menu_frame, atm_frame  # already logged in via cookies

    # Fill login form
    page.locator("#txt_user_id").type(BCA_USER, delay=80)
    time.sleep(0.8)
    page.locator("#txt_pswd").type(BCA_PASS, delay=100)
    time.sleep(1)
    page.locator("#btnSubmit").click()

    try:
        page.wait_for_url("**/authentication.do*", timeout=25000)
    except Exception:
        pass
    time.sleep(4)

    # Save fresh cookies
    cookies = context.cookies()
    COOKIES_FILE.write_text(json.dumps(cookies, indent=2))

    menu_frame, atm_frame = get_frames(page)
    if not menu_frame:
        body = page.inner_text("body").lower()
        if "salah" in body or "block" in body:
            raise RuntimeError("Login blocked — too many attempts. Wait 30 min.")
        raise RuntimeError(f"Login failed. Page: {page.url}")

    return menu_frame, atm_frame


def get_saldo(menu_frame, atm_frame):
    """Navigate to Balance Inquiry and parse saldo."""
    menu_frame.click("a[href='account_information_menu.htm']", timeout=5000)
    time.sleep(1.5)
    menu_frame.click("a[onclick*='balanceinquiry']", timeout=5000)
    time.sleep(2)

    content = atm_frame.inner_text("body")
    rows = atm_frame.query_selector_all("table tr")
    for row in rows[1:]:
        cells = [td.inner_text().strip() for td in row.query_selector_all("td")]
        if cells and len(cells) >= 4 and any(cells):
            return {
                "account_no": cells[0],
                "type": cells[1],
                "currency": cells[2],
                "balance": cells[3],
                "raw": " | ".join(c for c in cells if c),
            }

    amounts = re.findall(r"[\d,\.]{5,}", content)
    return {"balance": amounts[0] if amounts else "parse_failed", "raw": content[:200]}


def get_mutasi(page, menu_frame, atm_frame, days=7):
    """Navigate to Account Statement and parse mutasi."""
    # Re-navigate to main menu first
    menu_frame.click("a[href='account_information_menu.htm']", timeout=5000)
    time.sleep(1)
    menu_frame.click("a[onclick*='accountstmt']", timeout=5000)
    time.sleep(2)

    # Re-get atm frame after navigation
    _, atm_frame = get_frames(page)
    if not atm_frame:
        raise RuntimeError("atm frame lost after navigation")

    now = datetime.now()
    start = now - timedelta(days=days)

    # All date fields are <select> dropdowns
    atm_frame.select_option("#startDt", start.strftime("%d"))
    atm_frame.select_option("#startMt", str(int(start.strftime("%m"))))
    atm_frame.select_option("#startYr", start.strftime("%Y"))
    atm_frame.select_option("#endDt", now.strftime("%d"))
    atm_frame.select_option("#endMt", str(int(now.strftime("%m"))))
    atm_frame.select_option("#endYr", now.strftime("%Y"))
    atm_frame.click('input[name="value(submit1)"]')
    time.sleep(3)

    _, atm_frame = get_frames(page)
    content = atm_frame.inner_text("body")

    # Parse summary
    summary = {}
    for label, key in [("Starting Balance", "starting_balance"), ("Total Credits", "total_credits"),
                       ("Total Debits", "total_debits"), ("Ending Balance", "ending_balance")]:
        m = re.search(rf"{label}\s*:\s*([\d,\.]+)", content)
        if m:
            summary[key] = m.group(1)

    # Parse transactions
    mutasi = []
    rows = atm_frame.query_selector_all("table tr")
    for row in rows:
        cells = [td.inner_text().strip() for td in row.query_selector_all("td")]
        if len(cells) >= 5 and cells[0] and re.search(r"\d{2}/\d{2}/\d{4}", cells[0]):
            amount = cells[3] if len(cells) > 3 else ""
            txn_type = cells[4] if len(cells) > 4 else ""
            balance = cells[5] if len(cells) > 5 else ""
            mutasi.append({
                "tanggal": cells[0],
                "keterangan": re.sub(r"\s+", " ", cells[1]) if len(cells) > 1 else "",
                "cabang": cells[2] if len(cells) > 2 else "",
                "amount": amount,
                "type": txn_type,  # DB or CR
                "balance": balance,
                "debet": amount if txn_type == "DB" else "",
                "kredit": amount if txn_type == "CR" else "",
            })

    return {"transactions": mutasi, "summary": summary, "period_days": days}


def run_check(check_saldo=True, check_mutasi=True, days=7, headless=True, max_retries=2):
    from playwright.sync_api import sync_playwright

    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": BCA_USER,
        "saldo": None,
        "mutasi": None,
        "error": None,
    }

    for attempt in range(1, max_retries + 1):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=headless,
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-blink-features=AutomationControlled",
                        "--disable-dev-shm-usage",
                    ]
                )
                context = browser.new_context(
                    user_agent=UA,
                    viewport={"width": 1280, "height": 800},
                    locale="id-ID",
                    timezone_id="Asia/Jakarta",
                    extra_http_headers={"Accept-Language": "id-ID,id;q=0.9,en;q=0.8"},
                )
                context.add_init_script(STEALTH_SCRIPT)

                # Load cookies if fresh
                if COOKIES_FILE.exists():
                    age = time.time() - COOKIES_FILE.stat().st_mtime
                    if age < COOKIE_MAX_AGE:
                        context.add_cookies(json.loads(COOKIES_FILE.read_text()))

                page = context.new_page()

                menu_frame, atm_frame = login(page, context)

                if check_saldo:
                    result["saldo"] = get_saldo(menu_frame, atm_frame)

                if check_mutasi:
                    result["mutasi"] = get_mutasi(page, menu_frame, atm_frame, days=days)

                browser.close()
                result["error"] = None
                break  # success

        except Exception as e:
            err_msg = str(e)
            result["error"] = err_msg
            # Don't clear cookies on block detection — clearing forces re-login which makes block worse
            if "blocked" in err_msg.lower() or "block" in err_msg.lower():
                result["error"] = "⚠️ BCA temporarily blocked login. Wait ~1 hour then retry."
                break  # Don't retry if blocked
            if attempt < max_retries and "cookies" not in err_msg.lower():
                time.sleep(10)
            # else: keep error

    return result


def format_report(result):
    lines = [f"🏦 BCA Check — {result['timestamp']}"]

    if result.get("error"):
        lines.append(f"❌ Error: {result['error']}")
        return "\n".join(lines)

    if result.get("saldo"):
        s = result["saldo"]
        lines.append(f"💰 Saldo: IDR {s.get('balance', '?')} (Rek: {s.get('account_no', '?')})")

    if result.get("mutasi"):
        m = result["mutasi"]
        summary = m.get("summary", {})
        txns = m.get("transactions", [])

        lines.append(f"\n📊 Ringkasan {m['period_days']} hari:")
        if summary:
            lines.append(f"  Saldo awal : IDR {summary.get('starting_balance', '?')}")
            lines.append(f"  Total masuk: IDR {summary.get('total_credits', '?')}")
            lines.append(f"  Total keluar: IDR {summary.get('total_debits', '?')}")
            lines.append(f"  Saldo akhir: IDR {summary.get('ending_balance', '?')}")

        if txns:
            lines.append(f"\n📋 {len(txns)} transaksi terakhir:")
            for tx in txns[:10]:
                sign = "-" if tx["type"] == "DB" else "+"
                lines.append(f"  {tx['tanggal']} | {tx['keterangan'][:35]} | {sign}IDR {tx['amount']}")

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BCA KlikBCA Scraper")
    parser.add_argument("--saldo", action="store_true", help="Cek saldo saja")
    parser.add_argument("--mutasi", action="store_true", help="Cek mutasi saja")
    parser.add_argument("--days", type=int, default=7, help="Periode mutasi dalam hari (default: 7)")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output JSON")
    parser.add_argument("--show-browser", action="store_true", help="Tampilkan browser (debug)")
    args = parser.parse_args()

    check_saldo = args.saldo or not (args.saldo or args.mutasi)
    check_mutasi = args.mutasi or not (args.saldo or args.mutasi)

    result = run_check(
        check_saldo=check_saldo,
        check_mutasi=check_mutasi,
        days=args.days,
        headless=not args.show_browser,
        max_retries=2,
    )

    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_report(result))

    sys.exit(0 if not result.get("error") else 1)


if __name__ == "__main__":
    main()
