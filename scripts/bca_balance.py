#!/usr/bin/env python3
"""
BCA Balance Checker
Uses KlikBCA web session to get balance without wasting AI tokens.
Caches session token for reuse.

Usage:
  python3 bca_balance.py                 # check balance
  python3 bca_balance.py --json          # output JSON
  python3 bca_balance.py --save          # check + save to Supabase
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

CACHE_DIR = Path("/tmp/bca_cache")
CACHE_DIR.mkdir(exist_ok=True)
SESSION_CACHE = CACHE_DIR / "session.json"
BALANCE_CACHE = CACHE_DIR / "last_balance.json"

# BCA credentials — load from env or hardcoded (private machine only)
BCA_USER = os.getenv("BCA_USER", "")
BCA_PASS = os.getenv("BCA_PASS", "")

KLIKBCA_BASE = "https://ibank.klikbca.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}


def load_session():
    """Load cached session if still valid."""
    if SESSION_CACHE.exists():
        try:
            data = json.loads(SESSION_CACHE.read_text())
            # Session valid for 10 minutes
            if time.time() - data.get("timestamp", 0) < 600:
                return data.get("cookies"), data.get("token")
        except:
            pass
    return None, None


def save_session(cookies, token):
    SESSION_CACHE.write_text(json.dumps({
        "cookies": cookies,
        "token": token,
        "timestamp": time.time()
    }))


def login(user, password):
    """Login to KlikBCA, return session cookies."""
    session = requests.Session()
    session.headers.update(HEADERS)

    # Get login page (to get CSRF token)
    r = session.get(f"{KLIKBCA_BASE}/authentication.do?value(actions)=login", timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    # Extract token
    token_input = soup.find("input", {"name": "value(token)"})
    token = token_input["value"] if token_input else ""

    # Submit login
    login_data = {
        "value(login_id)": user,
        "value(password)": password,
        "value(actions)": "login",
        "value(token)": token,
    }
    r2 = session.post(
        f"{KLIKBCA_BASE}/authentication.do",
        data=login_data,
        timeout=15
    )

    if "Invalid User ID" in r2.text or "salah" in r2.text.lower():
        raise ValueError("Login failed: invalid credentials")

    cookies = dict(session.cookies)
    save_session(cookies, token)
    return session, cookies


def get_balance(session=None, cookies=None):
    """Get balance from account summary page."""
    if session is None:
        session = requests.Session()
        session.headers.update(HEADERS)
        if cookies:
            for k, v in cookies.items():
                session.cookies.set(k, v)

    r = session.get(
        f"{KLIKBCA_BASE}/accountstmt.do?value(actions)=acct_info",
        timeout=15
    )
    soup = BeautifulSoup(r.text, "html.parser")

    # Parse balance from account info table
    balances = []
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 3:
            text = " ".join(c.get_text(strip=True) for c in cells)
            # Look for IDR balance patterns
            match = re.search(r"([\d,]+\.\d{2})", text)
            if match and ("IDR" in text or "Rp" in text or "Tabungan" in text):
                balances.append({
                    "label": cells[0].get_text(strip=True),
                    "account": cells[1].get_text(strip=True) if len(cells) > 1 else "",
                    "balance": match.group(1),
                    "raw": text[:100]
                })

    return balances


def save_to_supabase(balance_idr):
    """Update Supabase cashflow table with current balance."""
    try:
        sys.path.insert(0, "/home/openclaw/.openclaw/workspace")
        from supabase import create_client

        url = "https://juoralxnkmfrnpmkiywk.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1b3JhbHhua21mcm5wbWtpeXdrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MzM5NjU0MywiZXhwIjoyMDg4OTcyNTQzfQ.ghb9G0EbaYdESNcGfvYOONuAGBtcLWOD8HMacMnLnyI"
        client = create_client(url, key)

        today = datetime.now().strftime("%Y-%m-%d")
        client.table("cashflow").upsert({
            "date": today,
            "bank_balance_idr": balance_idr,
            "notes": f"Auto-updated by bca_balance.py at {datetime.now().strftime('%H:%M')}",
        }, on_conflict="date").execute()
        return True
    except Exception as e:
        print(f"Supabase save failed: {e}", file=sys.stderr)
        return False


def parse_balance_idr(balance_str):
    """Convert '0.37' or '1,234,567.89' to float."""
    try:
        return float(balance_str.replace(",", ""))
    except:
        return 0.0


def main():
    parser = argparse.ArgumentParser(description="BCA Balance Checker")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--save", action="store_true", help="Save to Supabase")
    parser.add_argument("--user", default=BCA_USER)
    parser.add_argument("--pass", dest="password", default=BCA_PASS)
    args = parser.parse_args()

    if not args.user or not args.password:
        print("ERROR: BCA_USER and BCA_PASS env vars required", file=sys.stderr)
        print("Usage: BCA_USER=xxx BCA_PASS=xxx python3 bca_balance.py")
        sys.exit(1)

    # Try cached session first
    cached_cookies, _ = load_session()
    try:
        if cached_cookies:
            balances = get_balance(cookies=cached_cookies)
        else:
            session, cookies = login(args.user, args.password)
            balances = get_balance(session=session)
    except Exception as e:
        # Session expired, re-login
        print(f"Session expired, re-logging in... ({e})", file=sys.stderr)
        session, cookies = login(args.user, args.password)
        balances = get_balance(session=session)

    if not balances:
        print("WARNING: Could not parse balance from page", file=sys.stderr)
        sys.exit(2)

    result = {
        "checked_at": datetime.now().isoformat(),
        "account": "1131323722",
        "balances": balances,
        "primary_balance": balances[0]["balance"] if balances else "unknown",
        "primary_idr": parse_balance_idr(balances[0]["balance"]) if balances else 0,
    }

    # Save balance cache
    BALANCE_CACHE.write_text(json.dumps(result))

    if args.save:
        saved = save_to_supabase(result["primary_idr"])
        result["supabase_saved"] = saved

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        bal = result["primary_balance"]
        idr = result["primary_idr"]
        print(f"BCA Balance: IDR {idr:,.2f}")
        print(f"Checked at: {result['checked_at'][:16]}")
        if idr < 50000:
            print("⚠️  EMERGENCY: Balance < IDR 50K")
        elif idr < 500000:
            print("⚠️  WARNING: Balance < IDR 500K")
        else:
            print("✅ Balance OK")

    return result


if __name__ == "__main__":
    main()
