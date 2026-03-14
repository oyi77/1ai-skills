#!/usr/bin/env python3
"""BCA Balance Check - Fixed RSA encryption with server timestamp"""
import requests, base64, re, json, time, sys
from datetime import datetime
from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1F3Tb5ME9iY7HwrNiOUMdTDZJRs65HY+XHNJJYrI/165H9NigorOOLVrC/YV7QLyssXbZ9lUDzo4KZAZhQcSNekK2dfV3Gwg7X4XT3Nbs18I+YqTUqhFiedPTf7sefT3nkqvV5FE3XeY6A/l0rOk50DtRnI68fqhf50pQgy9L9DAViYvVno2B8MZyb/U0vA0PX29ruMntmGJeU9SQg7kPjBpGScFn3CFkWn509R0iVYaNvhjvJhcGMSTldd2GQUwdh7IMTMGdKn4NliFy7oLRnE3LiGoMVnPbwnw67EWcr+e3UMKkNk91kgiPk/vvb6UEGtFRCoE4g6kql014tvNdwIDAQAB
-----END PUBLIC KEY-----"""

BCA_USER = "MUCHAMMA6064"
BCA_PIN = "242424"
BASE = "https://ibank.klikbca.com"

s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
})

# Step 1: Get login page + extract server timestamp
print("Getting login page...", flush=True)
r = s.get(f"{BASE}/authentication.do?value(actions)=login", timeout=15)
page_load_time = time.time()

# Parse dtSign from JS: var dtSign = new Date(2026, parseInt("03")-1, 14, 15, 12, 33);
match = re.search(r'var dtSign = new Date\((\d+),\s*parseInt\("(\d+)"\)-1,\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', r.text)
if match:
    year, month, day, hour, minute, second = [int(x) for x in match.groups()]
    print(f"Server timestamp: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}", flush=True)
else:
    print("ERROR: Could not parse server timestamp!", flush=True)
    sys.exit(1)

# Step 2: Encrypt PIN using server timestamp (like JS does)
# JS: concat PIN + formatted_date where date = server_time + elapsed
elapsed_ms = int((time.time() - page_load_time) * 1000)

# Reconstruct the timestamp the same way JS does
from datetime import timedelta
server_dt = datetime(year, month, day, hour, minute, second)
adjusted_dt = server_dt + timedelta(milliseconds=elapsed_ms)

formatted_date = adjusted_dt.strftime("%Y%m%d%H%M%S")
pin_with_date = BCA_PIN + formatted_date

print(f"Encrypting: PIN+{formatted_date}", flush=True)

key = RSA.import_key(PUBLIC_KEY)
cipher = PKCS1_v1_5.new(key)
encrypted = cipher.encrypt(pin_with_date.encode())
encrypted_b64 = base64.b64encode(encrypted).decode()

# Step 3: Submit login
print("Submitting login...", flush=True)
r2 = s.post(f"{BASE}/authentication.do", data={
    "value(user_id)": BCA_USER,
    "value(pswd)": encrypted_b64,
    "value(actions)": "login",
    "value(Submit)": "LOGIN",
}, timeout=15, allow_redirects=True)

# Check for errors
if "5 menit" in r2.text or "re-login after" in r2.text:
    print("❌ Account locked - wait 5 minutes", flush=True)
    sys.exit(2)
elif "salah" in r2.text.lower() and "user id" in r2.text.lower():
    print("❌ Wrong credentials", flush=True)
    sys.exit(3)

# Check for frameset (= success)
if "frameset" in r2.text.lower() or "frame" in r2.text.lower():
    print("✅ LOGIN SUCCESS! (frameset loaded)", flush=True)
    
    # Navigate frames
    soup = BeautifulSoup(r2.text, 'html.parser')
    frames = soup.find_all('frame')
    for f in frames:
        print(f"  Frame: {f.get('name','')} → {f.get('src','')}", flush=True)
    
    # Try balance inquiry
    r3 = s.post(f"{BASE}/balanceinquiry.do", data={"value(actions)": "balanceinquiry"}, timeout=15)
    soup3 = BeautifulSoup(r3.text, 'html.parser')
    
    # Extract balance from table
    tds = soup3.find_all('td')
    for td in tds:
        text = td.get_text(strip=True)
        if text and len(text) > 2:
            if any(keyword in text.lower() for keyword in ['idr', 'tabungan', 'pedi', '1131']):
                print(f"  💰 {text}", flush=True)
            elif re.match(r'^[\d,\.]+$', text.replace(',','').replace('.','')) and len(text) > 3:
                print(f"  💰 {text}", flush=True)
    
    # Logout
    try: s.get(f"{BASE}/authentication.do?value(actions)=logout", timeout=5)
    except: pass
    print("Logged out", flush=True)
else:
    # Check if we're still on login page
    if "txt_user_id" in r2.text:
        # Check for error message
        err_match = re.search(r"var err='([^']+)'", r2.text)
        if err_match:
            print(f"❌ Error: {err_match.group(1)}", flush=True)
        else:
            print("❌ Login failed - returned to login page (no specific error)", flush=True)
    else:
        print(f"Unknown response. Title: ", flush=True)
        soup = BeautifulSoup(r2.text, 'html.parser')
        print(soup.title.text if soup.title else "N/A", flush=True)
