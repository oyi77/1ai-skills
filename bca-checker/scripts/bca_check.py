#!/usr/bin/env /tmp/bca-venv/bin/python3
"""
BCA KlikBCA Scraper — saldo + mutasi
Credentials: BCA_USER, BCA_PASS from env file

Usage:
  python3 bca_check.py                  # full check: saldo + mutasi
  python3 bca_check.py --saldo          # saldo saja
  python3 bca_check.py --mutasi         # mutasi 7 hari terakhir
  python3 bca_check.py --mutasi --days 30

Output JSON: {"saldo": "...", "mutasi": [...], "timestamp": "..."}
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Load .env if available
env_file = Path(__file__).parents[3] / ".env"
if not env_file.exists():
    env_file = Path("/home/openclaw/.openclaw/.env")

if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

BCA_USER = os.environ.get("BCA_USER", "")
BCA_PASS = os.environ.get("BCA_PASS", "")

if not BCA_USER or not BCA_PASS:
    print(json.dumps({"error": "BCA_USER/BCA_PASS not set in .env"}))
    sys.exit(1)


def run_check(check_saldo=True, check_mutasi=True, days=7):
    from playwright.sync_api import sync_playwright

    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "saldo": None,
        "mutasi": [],
        "error": None,
    }

    COOKIES_FILE = Path("/home/openclaw/.openclaw/bca_cookies.json")
    
    with sync_playwright() as p:
        # Try existing chromium first, then bundled
        try:
            browser = p.chromium.launch(
                executable_path="/usr/bin/chromium",
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
            )
        except Exception:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
            )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        # Inject saved cookies jika ada (bypass OOB device verification)
        if COOKIES_FILE.exists():
            saved_cookies = json.loads(COOKIES_FILE.read_text())
            context.add_cookies(saved_cookies)
        
        page = context.new_page()

        try:
            # Step 1: Buka KlikBCA langsung ke authenticated area
            page.goto("https://ibank.klikbca.com/", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=15000)

            # Cek apakah sudah login via cookies
            content = page.content()
            already_logged_in = any(x in content.lower() for x in ["logout", "selamat datang", "informasi rekening"])
            
            if not already_logged_in:
                # Cookies expired/invalid → login ulang
                page.fill('input[name="txt_user_id"]', BCA_USER)
                page.fill('input[name="txt_pswd"]', BCA_PASS)
                page.click('input[name="value(Submit)"]')
                page.wait_for_load_state("networkidle", timeout=15000)

                # Check login berhasil
                content = page.content()
                if not any(x in content.lower() for x in ["logout", "selamat datang", "informasi rekening"]):
                    if "wrong" in content.lower() or "salah" in content.lower() or "gagal" in content.lower():
                        result["error"] = "Login gagal — cek BCA_USER/BCA_PASS"
                    else:
                        result["error"] = "Login gagal — OOB verification diperlukan. Jalankan export_cookies.py dulu!"
                    return result
                
                # Save fresh cookies setelah login berhasil
                new_cookies = context.cookies()
                COOKIES_FILE.write_text(json.dumps(new_cookies, indent=2))

            # Step 3: Cek Saldo
            if check_saldo:
                try:
                    page.click("text=Informasi Rekening", timeout=5000)
                    page.wait_for_load_state("networkidle", timeout=10000)
                    page.click("text=Saldo Rekening", timeout=5000)
                    page.wait_for_load_state("networkidle", timeout=10000)
                    
                    # Parse saldo dari tabel
                    saldo_text = page.inner_text("table").strip()
                    # Extract angka saldo (IDR format)
                    import re
                    lines = [l.strip() for l in saldo_text.splitlines() if l.strip()]
                    for i, line in enumerate(lines):
                        if "IDR" in line or re.search(r'\d{1,3}(,\d{3})+', line):
                            result["saldo"] = line
                            break
                    
                    if not result["saldo"]:
                        result["saldo"] = "Parsed gagal — lihat raw:\n" + saldo_text[:500]
                except Exception as e:
                    result["error"] = f"Saldo error: {str(e)}"

            # Step 4: Mutasi Rekening
            if check_mutasi:
                try:
                    page.goto("https://ibank.klikbca.com/", timeout=10000)
                    page.click("text=Informasi Rekening", timeout=5000)
                    page.wait_for_load_state("networkidle", timeout=10000)
                    page.click("text=Mutasi Rekening", timeout=5000)
                    page.wait_for_load_state("networkidle", timeout=10000)

                    # Set tanggal: hari ini - days s/d hari ini
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=days)
                    
                    # Fill form tanggal
                    page.fill('input[name*="start"]', start_date.strftime("%d/%m/%Y"), timeout=3000)
                    page.fill('input[name*="end"]', end_date.strftime("%d/%m/%Y"), timeout=3000)
                    page.click('input[type="submit"]', timeout=5000)
                    page.wait_for_load_state("networkidle", timeout=10000)

                    # Parse tabel mutasi
                    import re
                    rows = page.query_selector_all("table tr")
                    for row in rows[1:]:  # skip header
                        cells = [td.inner_text().strip() for td in row.query_selector_all("td")]
                        if len(cells) >= 4:
                            result["mutasi"].append({
                                "tanggal": cells[0] if cells else "",
                                "keterangan": cells[1] if len(cells) > 1 else "",
                                "debet": cells[2] if len(cells) > 2 else "",
                                "kredit": cells[3] if len(cells) > 3 else "",
                                "saldo": cells[4] if len(cells) > 4 else "",
                            })
                except Exception as e:
                    if "error" in result and result["error"]:
                        result["error"] += f" | Mutasi error: {str(e)}"
                    else:
                        result["error"] = f"Mutasi error: {str(e)}"

            # Logout
            try:
                page.click("text=Logout", timeout=3000)
            except Exception:
                pass

        except Exception as e:
            result["error"] = str(e)
        finally:
            browser.close()

    return result


def format_report(result):
    """Format hasil sebagai teks human-readable untuk Telegram."""
    lines = [f"🏦 BCA Check — {result['timestamp']}"]
    
    if result.get("error"):
        lines.append(f"❌ Error: {result['error']}")
    
    if result.get("saldo"):
        lines.append(f"\n💰 Saldo: {result['saldo']}")
    
    if result.get("mutasi"):
        lines.append(f"\n📋 Mutasi ({len(result['mutasi'])} transaksi):")
        for tx in result["mutasi"][:10]:  # max 10 per report
            debet = f"-{tx['debet']}" if tx.get('debet') else ""
            kredit = f"+{tx['kredit']}" if tx.get('kredit') else ""
            amount = debet or kredit or ""
            lines.append(f"  {tx.get('tanggal','')} | {tx.get('keterangan','')[:30]} | {amount}")
        if len(result["mutasi"]) > 10:
            lines.append(f"  ... +{len(result['mutasi'])-10} transaksi lagi")
    
    return "\n".join(lines)


def save_to_cashflow(result):
    """Append saldo ke cashflow tracker."""
    from pathlib import Path
    import re
    
    cashflow_dir = Path("/home/openclaw/.openclaw/workspace/cashflow")
    cashflow_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    cashflow_file = cashflow_dir / f"{today}.md"
    
    entry = f"""
---
## {result['timestamp']} — BCA Auto-Check

**Saldo:** {result.get('saldo', 'N/A')}
**Mutasi:** {len(result.get('mutasi', []))} transaksi
"""
    if result.get("error"):
        entry += f"**Error:** {result['error']}\n"
    
    with open(cashflow_file, "a") as f:
        f.write(entry)
    
    return str(cashflow_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BCA KlikBCA checker")
    parser.add_argument("--saldo", action="store_true", default=False)
    parser.add_argument("--mutasi", action="store_true", default=False)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--no-cashflow", action="store_true", help="Skip cashflow save")
    args = parser.parse_args()

    # Default: check keduanya
    check_saldo = args.saldo or (not args.saldo and not args.mutasi)
    check_mutasi = args.mutasi or (not args.saldo and not args.mutasi)

    result = run_check(check_saldo=check_saldo, check_mutasi=check_mutasi, days=args.days)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result))

    # Auto-save ke cashflow
    if not args.no_cashflow and (result.get("saldo") or result.get("mutasi")):
        saved = save_to_cashflow(result)
        print(f"\n💾 Tersimpan: {saved}")
