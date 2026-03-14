#!/usr/bin/env python3
"""
BCA Balance Checker via Vivaldi CDP
Uses OpenClaw's existing browser on port 18800 — bypasses all anti-bot.
Reuses logged-in session. Re-logins if session expired.

Usage:
  python3 bca_cdp.py                 # print balance
  python3 bca_cdp.py --save          # save to Supabase
  python3 bca_cdp.py --json          # JSON output

Cron (every 3 hours):
  0 */3 * * * cd ~/.openclaw/workspace && python3 scripts/bca_cdp.py --save >> logs/bca.log 2>&1
"""
import argparse, json, os, re, sys, time
from datetime import datetime
from pathlib import Path

import websocket

CDP_HOST    = "ws://127.0.0.1:18800"
CDP_HTTP    = "http://127.0.0.1:18800"
BCA_USER    = os.getenv("BCA_USER", "MUCHAMMA6064")
BCA_PASS    = os.getenv("BCA_PASS", "242424")
BCA_ACCOUNT = "1131323722"
SUPABASE_URL = "https://juoralxnkmfrnpmkiywk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1b3JhbHhua21mcm5wbWtpeXdrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MzM5NjU0MywiZXhwIjoyMDg4OTcyNTQzfQ.ghb9G0EbaYdESNcGfvYOONuAGBtcLWOD8HMacMnLnyI"
CACHE       = Path("/tmp/bca_cache")
CACHE.mkdir(exist_ok=True)


class CDPSession:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(
            ws_url, timeout=15,
            origin="http://localhost",
            header={"Origin": "http://localhost"}
        )
        self._id = 0

    def send(self, method, params=None):
        self._id += 1
        mid = self._id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        deadline = time.time() + 10
        while time.time() < deadline:
            try:
                msg = json.loads(self.ws.recv())
                if msg.get("id") == mid:
                    return msg.get("result", {})
            except websocket.WebSocketTimeoutException:
                break
        return {}

    def eval(self, js):
        r = self.send("Runtime.evaluate", {"expression": js, "returnByValue": True, "awaitPromise": False})
        return r.get("result", {}).get("value")

    def navigate(self, url):
        self.send("Page.navigate", {"url": url})
        time.sleep(3)

    def close(self):
        try:
            self.ws.close()
        except:
            pass


def get_ws_url():
    """Find the KlikBCA tab or any page tab."""
    import urllib.request
    r = urllib.request.urlopen(f"{CDP_HTTP}/json", timeout=5)
    tabs = json.loads(r.read())
    # Prefer KlikBCA tab
    for tab in tabs:
        if "klikbca" in tab.get("url", "").lower() and tab.get("type") == "page":
            return tab["webSocketDebuggerUrl"]
    # Fallback to first page tab
    for tab in tabs:
        if tab.get("type") == "page":
            return tab["webSocketDebuggerUrl"]
    raise Exception("No browser tab found — is openclaw browser running?")


def parse_idr(text):
    text = re.sub(r'[IDRRp\s]', '', text).strip()
    if ',' in text:
        text = text.replace('.', '').replace(',', '.')
    else:
        text = text.replace('.', '')
    try:
        return float(text)
    except:
        return 0.0


def check_balance():
    ws_url = get_ws_url()
    cdp = CDPSession(ws_url)
    balance_idr = 0.0
    raw_text = ""

    try:
        # Check current page
        url = cdp.eval("window.location.href")
        print(f"  Current: {url}", file=sys.stderr)

        # Navigate to KlikBCA if not there
        if "klikbca.com" not in (url or ""):
            cdp.navigate("https://ibank.klikbca.com/")
            url = cdp.eval("window.location.href")
            print(f"  Navigated to: {url}", file=sys.stderr)

        # Check if login page
        frames = cdp.eval("Array.from(document.querySelectorAll('frame')).map(function(f){return f.name;}).join(',')") or ""
        is_logged_in = "menu" in frames and "atm" in frames

        if not is_logged_in:
            print("  Not logged in, attempting login...", file=sys.stderr)
            # Navigate to main page
            if "ibank.klikbca.com" not in url:
                cdp.navigate("https://ibank.klikbca.com/")

            login_js = f"""(function(){{
                var nS=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
                var uid=document.getElementById('txt_user_id');
                var pwd=document.getElementById('txt_pswd');
                if(!uid||!pwd) return 'NO_FORM';
                nS.call(uid,'{BCA_USER}');uid.dispatchEvent(new Event('input',{{bubbles:true}}));
                nS.call(pwd,'{BCA_PASS}');pwd.dispatchEvent(new Event('input',{{bubbles:true}}));
                document.getElementById('btnSubmit').click();
                return 'OK';
            }})()"""
            login_result = cdp.eval(login_js)
            print(f"  Login: {login_result}", file=sys.stderr)
            if login_result == "OK":
                time.sleep(5)
            else:
                return 0.0, f"Login failed: {login_result}"

        # Check if Balance Inquiry already loaded
        atm_text = cdp.eval("""(function(){
            var f=document.querySelector('frame[name=atm]');
            if(!f||!f.contentDocument) return '';
            return f.contentDocument.body.innerText.substring(0,400);
        })()""") or ""

        if "BALANCE INQUIRY" in atm_text:
            print("  Balance Inquiry already loaded", file=sys.stderr)
            raw_text = atm_text
        else:
            # Navigate via menu: Account Information → Balance Inquiry
            # Step 1: click Account Information
            click1 = cdp.eval("""(function(){
                var mf=document.querySelector('frame[name=menu]');
                if(!mf||!mf.contentDocument) return 'NO_MENU';
                var links=Array.from(mf.contentDocument.querySelectorAll('a'));
                var ai=links.find(function(a){return a.textContent.trim()==='Account Information';});
                if(ai){ai.click(); return 'OK';}
                return 'NO_LINK:'+links.map(function(a){return a.textContent.trim();}).join(',');
            })()""")
            print(f"  Click AcctInfo: {click1}", file=sys.stderr)
            time.sleep(1.5)

            # Step 2: click Balance Inquiry
            click2 = cdp.eval("""(function(){
                var mf=document.querySelector('frame[name=menu]');
                if(!mf||!mf.contentDocument) return 'NO_MENU';
                var links=Array.from(mf.contentDocument.querySelectorAll('a'));
                var bi=links.find(function(a){return a.textContent.trim()==='Balance Inquiry';});
                if(!bi) return 'NO_BI:'+links.map(function(a){return a.textContent.trim();}).join(',');
                var onc=bi.getAttribute('onclick');
                if(onc){mf.contentWindow.eval(onc.replace('return false;',''));return 'ONCLICK';}
                bi.click(); return 'CLICK';
            })()""")
            print(f"  Click BalanceInq: {click2}", file=sys.stderr)
            time.sleep(2.5)

            raw_text = cdp.eval("""(function(){
                var f=document.querySelector('frame[name=atm]');
                if(!f||!f.contentDocument) return '';
                return f.contentDocument.body.innerText.substring(0,400);
            })()""") or ""

        print(f"  ATM text: {raw_text[:150]}", file=sys.stderr)

        # Parse
        m = re.search(r'1131323722.*?IDR\s+([\d,\.]+)', raw_text, re.DOTALL)
        if m:
            balance_idr = parse_idr(m.group(1))
        else:
            nums = re.findall(r'([\d,\.]+)', raw_text)
            for n in nums:
                v = parse_idr(n)
                if 0 <= v < 1e9:
                    balance_idr = v
                    break

    finally:
        cdp.close()

    return balance_idr, raw_text


def save_to_supabase(balance_idr):
    try:
        from supabase import create_client
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        today = datetime.now().strftime("%Y-%m-%d")
        client.table("cashflow").upsert({
            "date": today,
            "bank_balance_idr": balance_idr,
            "notes": f"Auto BCA CDP {datetime.now().strftime('%H:%M')}",
        }, on_conflict="date").execute()
        return True
    except Exception as e:
        print(f"Supabase: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_out")
    args = parser.parse_args()

    balance_idr, raw_text = check_balance()
    ts = datetime.now().isoformat()

    result = {
        "checked_at": ts,
        "account": BCA_ACCOUNT,
        "balance_idr": balance_idr,
        "status": "EMERGENCY" if balance_idr < 50000 else ("WARNING" if balance_idr < 500000 else "OK"),
    }
    (CACHE / "last_balance.json").write_text(json.dumps(result))

    if args.save:
        result["supabase_saved"] = save_to_supabase(balance_idr)

    if args.json_out:
        print(json.dumps(result, indent=2))
    else:
        emoji = "🚨" if balance_idr < 50000 else ("⚠️" if balance_idr < 500000 else "✅")
        print(f"\n{emoji} BCA: IDR {balance_idr:,.2f}")
        print(f"Account : {BCA_ACCOUNT}")
        print(f"Checked : {ts[:16]}")
        if result["supabase_saved"] if args.save else False:
            print(f"Supabase: ✅ saved")

    return result


if __name__ == "__main__":
    main()
