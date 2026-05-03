import os
"""
Kling AI Account Generator
==========================
Automates Kling account registration using temp Gmail addresses (Emailnator)
with optional proxy rotation support.

Flow per account:
  1. Generate temp Gmail via Emailnator (pynator)
  2. Visit klingai.com to get session cookies + browser fingerprint (primp)
  3. Send OTP to temp email
  4. Poll Emailnator inbox for OTP code
  5. Submit registration with OTP + random password
  6. Login to get session cookie
  7. Claim daily login bonus
  8. Save account to JSON store

Usage:
  from kling_account_generator import KlingAccountGenerator
  gen = KlingAccountGenerator()
  result = gen.generate_account(proxy="http://user:pass@host:port")
  gen.batch_generate(count=5, proxy_list=["http://p1:p2@h:p", ...])
"""

import re
import json
import time
import uuid
import secrets
import string
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

# ── Optional deps ──────────────────────────────────────────────────────────────
try:
    from pynator import EmailNator
    PYNATOR_OK = True
except ImportError:
    PYNATOR_OK = False
    logging.warning("pynator not installed — run: pip install pynator")

try:
    import primp
    PRIMP_OK = True
except ImportError:
    PRIMP_OK = False
    logging.warning("primp not installed — using plain requests (less realistic fingerprint)")

# ── Constants ──────────────────────────────────────────────────────────────────
KLING_HOME        = "https://klingai.com"
KLING_SEND_OTP    = "https://klingai.com/api/user/sendEmailCode"
KLING_REGISTER    = "https://klingai.com/api/user/register"
KLING_REGISTER_2  = "https://klingai.com/api/user/emailRegister"
KLING_REGISTER_3  = "https://klingai.com/api/user/registerByEmail"
KLING_LOGIN       = "https://id.klingai.com/pass/ksi18n/web/login/emailPassword"
KLING_USER_INFO   = "https://klingai.com/api/user/userInfo"
KLING_DAILY_BONUS = "https://klingai.com/api/user/signIn"   # guess — adjust if needed

DEFAULT_ACCOUNTS_PATH = Path.home() / ".openclaw" / "workspace" / "config" / "kling_accounts.json"
LOG_PATH = Path.home() / ".openclaw" / "workspace" / "logs" / "kling_generator.log"

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xhtml+xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Upgrade-Insecure-Requests": "1",
}

API_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "x-platform": "web",
    "x-language": "en",
    "Origin": "https://klingai.com",
    "Referer": "https://klingai.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

# ── Logging setup ──────────────────────────────────────────────────────────────
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("kling_generator")


# ── Main class ─────────────────────────────────────────────────────────────────
class KlingAccountGenerator:
    """Automated Kling AI account registration with temp email + proxy support."""

    def __init__(self, accounts_path: Optional[Path] = None, otp_timeout: int = 90):
        self.accounts_path = Path(accounts_path or DEFAULT_ACCOUNTS_PATH)
        self.accounts_path.parent.mkdir(parents=True, exist_ok=True)
        self.otp_timeout = otp_timeout
        self._load_accounts()

    # ── Public API ─────────────────────────────────────────────────────────────

    def generate_account(self, proxy: Optional[str] = None) -> dict:
        """
        Full registration flow for a single account.

        Returns:
            {
              "success": bool,
              "email": str,
              "password": str,
              "cookie": str,
              "credits": float,
              "error": str | None,
              "timestamp": str,
            }
        """
        result = {
            "success": False,
            "email": "",
            "password": "",
            "cookie": "",
            "credits": 0.0,
            "error": None,
            "timestamp": datetime.utcnow().isoformat(),
        }

        try:
            # 1. Generate temp email
            log.info("Generating temp email...")
            email = self._generate_temp_email()
            if not email:
                result["error"] = "Failed to generate temp email"
                return result
            result["email"] = email
            log.info(f"Temp email: {email}")

            # 2. Generate password
            password = self.generate_password()
            result["password"] = password

            # 3. Get session with fingerprint
            log.info("Getting session + fingerprint from klingai.com...")
            session = self._get_session_with_fingerprint(proxy=proxy)

            # 4. Send OTP
            log.info(f"Sending OTP to {email}...")
            otp_sent = self._send_otp(session, email)
            if not otp_sent:
                result["error"] = "Failed to send OTP (possibly blocked or CAPTCHA)"
                return result

            # 5. Retrieve OTP
            log.info("Polling inbox for OTP...")
            otp = self._get_otp_from_inbox(email, timeout=self.otp_timeout)
            if not otp:
                result["error"] = f"OTP not received within {self.otp_timeout}s"
                return result
            log.info(f"Got OTP: {otp}")

            # 6. Register
            log.info("Submitting registration...")
            registered = self._register(session, email, otp, password)
            if not registered:
                result["error"] = "Registration failed (all endpoints rejected)"
                return result
            log.info("Registration successful!")

            # 7. Login
            log.info("Logging in...")
            cookie = self._login(email, password, proxy=proxy)
            if not cookie:
                result["error"] = "Login failed after registration"
                # Still partial success — we have the account creds
                result["success"] = True
                self._save_account(result)
                return result
            result["cookie"] = cookie
            log.info("Login successful!")

            # 8. Claim daily bonus
            log.info("Claiming daily bonus...")
            credits = self._claim_daily_bonus(cookie, proxy=proxy)
            result["credits"] = credits
            log.info(f"Credits: {credits}")

            result["success"] = True
            self._save_account(result)
            return result

        except Exception as exc:
            log.error(f"Unexpected error: {exc}\n{traceback.format_exc()}")
            result["error"] = str(exc)
            return result

    def batch_generate(self, count: int, proxy_list: Optional[list] = None) -> list:
        """
        Generate `count` accounts, rotating through proxy_list if provided.

        Returns list of result dicts.
        """
        results = []
        for i in range(count):
            proxy = None
            if proxy_list:
                proxy = proxy_list[i % len(proxy_list)]
            log.info(f"\n{'='*50}\nAccount {i+1}/{count} | proxy={proxy}\n{'='*50}")

            success = False
            for attempt in range(1, 4):  # up to 3 retries
                log.info(f"  Attempt {attempt}/3")
                result = self.generate_account(proxy=proxy)
                results.append(result)
                if result["success"]:
                    success = True
                    break
                log.warning(f"  Attempt {attempt} failed: {result['error']}")
                time.sleep(5)

            if not success:
                log.error(f"Account {i+1} failed after 3 attempts.")

            # Polite delay between accounts
            if i < count - 1:
                time.sleep(3)

        return results

    def generate_password(self) -> str:
        """Generate a random strong 16-char password."""
        chars = string.ascii_letters + string.digits + "!@#$"
        return ''.join(secrets.choice(chars) for _ in range(16))

    # ── Private helpers ────────────────────────────────────────────────────────

    def _generate_temp_email(self) -> Optional[str]:
        """Generate a temp Gmail address via Emailnator (pynator)."""
        if not PYNATOR_OK:
            log.error("pynator not installed — cannot generate temp email")
            return None
        try:
            client = EmailNator()
            email = client.generate_email()
            if email:
                # Store client ref for inbox polling
                self._emailnator_client = client
                self._emailnator_email = email
                return email
            return None
        except Exception as exc:
            log.error(f"EmailNator error: {exc}")
            return None

    def _get_session_with_fingerprint(self, proxy: Optional[str] = None) -> requests.Session:
        """
        Visit klingai.com to get valid session cookies + kGateway-identity.
        Uses primp for realistic browser fingerprint if available.
        """
        proxies = {"http": proxy, "https": proxy} if proxy else None

        if PRIMP_OK:
            try:
                # primp impersonates real browser TLS fingerprint
                client = primp.Client(impersonate="chrome_131", proxies=proxies, verify=False)
                resp = client.get(KLING_HOME, headers=BROWSER_HEADERS, timeout=20)
                log.info(f"  [fingerprint] Home page: {resp.status_code}")

                # Convert primp cookies → requests.Session
                session = requests.Session()
                if proxies:
                    session.proxies.update(proxies)
                for name, value in resp.cookies.items():
                    session.cookies.set(name, value)
                return session
            except Exception as exc:
                log.warning(f"  primp failed ({exc}), falling back to requests")

        # Fallback: plain requests
        session = requests.Session()
        if proxies:
            session.proxies.update(proxies)
        try:
            resp = session.get(KLING_HOME, headers=BROWSER_HEADERS, timeout=20)
            log.info(f"  [session] Home page: {resp.status_code} | cookies: {list(resp.cookies.keys())}")
        except Exception as exc:
            log.warning(f"  Could not reach klingai.com: {exc}")
        return session

    def _send_otp(self, session: requests.Session, email: str) -> bool:
        """POST /api/user/sendEmailCode — type=1 for registration."""
        headers = {**API_HEADERS, "x-client-id": str(uuid.uuid4())}
        payload = {"email": email, "type": 1}

        try:
            resp = session.post(KLING_SEND_OTP, json=payload, headers=headers, timeout=20)
            log.info(f"  [sendOTP] status={resp.status_code} body={resp.text[:300]}")

            if resp.status_code == 200:
                data = resp.json()
                # Kling returns {status: 200, message: "OK"} on success
                # or {status: 500, message: "..."} on error
                api_status = data.get("status", data.get("code", 0))
                if api_status in (200, 0):
                    return True
                msg = data.get("message", "")
                if "captcha" in msg.lower():
                    log.warning("  CAPTCHA detected — skipping")
                    return False
                log.warning(f"  OTP API returned status {api_status}: {msg}")
                # Some regions return 200/OK in different fields
                return api_status == 200 or "success" in msg.lower()

            return False
        except Exception as exc:
            log.error(f"  sendOTP exception: {exc}")
            return False

    def _get_otp_from_inbox(self, email: str, timeout: int = 90) -> Optional[str]:
        """Poll Emailnator inbox for 6-digit OTP from Kling."""
        if not PYNATOR_OK:
            return None

        client = getattr(self, "_emailnator_client", None)
        if not client:
            log.error("No emailnator client — cannot poll inbox")
            return None

        deadline = time.time() + timeout
        poll_interval = 5
        seen_subjects = set()

        while time.time() < deadline:
            try:
                messages = client.get_messages(email)
                for msg in (messages or []):
                    subject = msg.get("subject", "")
                    body = msg.get("body", "") or msg.get("text", "") or ""

                    # Skip already-seen
                    key = subject + body[:50]
                    if key in seen_subjects:
                        continue
                    seen_subjects.add(key)

                    # Filter for Kling emails
                    if "kling" in subject.lower() or "kling" in body.lower() or \
                       "verification" in subject.lower() or "code" in subject.lower():
                        # Extract 6-digit OTP
                        otp_match = re.search(r'\b(\d{6})\b', subject + " " + body)
                        if otp_match:
                            return otp_match.group(1)

                    # Even without "kling" in subject, try to extract any 6-digit code
                    # (some OTP emails have minimal branding)
                    otp_match = re.search(r'\b(\d{6})\b', subject + " " + body)
                    if otp_match:
                        log.info(f"  Found 6-digit code in email: subject='{subject[:60]}'")
                        return otp_match.group(1)

            except Exception as exc:
                log.warning(f"  Inbox poll error: {exc}")

            remaining = deadline - time.time()
            log.info(f"  Waiting for OTP... ({remaining:.0f}s remaining)")
            time.sleep(poll_interval)

        return None

    def _register(self, session: requests.Session, email: str, otp: str, password: str) -> bool:
        """
        Try multiple registration endpoints in order.
        Returns True if any endpoint succeeds.
        """
        headers = {**API_HEADERS, "x-client-id": str(uuid.uuid4())}
        payload = {"email": email, "code": otp, "password": password}

        endpoints = [KLING_REGISTER, KLING_REGISTER_2, KLING_REGISTER_3]

        for endpoint in endpoints:
            try:
                resp = session.post(endpoint, json=payload, headers=headers, timeout=20)
                log.info(f"  [register] {endpoint.split('/')[-1]} → {resp.status_code} | {resp.text[:300]}")

                if resp.status_code == 200:
                    data = resp.json()
                    api_status = data.get("status", data.get("code", -1))
                    msg = data.get("message", "")

                    if api_status in (200, 0) or "success" in msg.lower():
                        return True
                    if "captcha" in msg.lower():
                        log.warning(f"  CAPTCHA on {endpoint} — stopping")
                        return False
                    log.warning(f"  Endpoint {endpoint}: api_status={api_status} msg={msg}")

                elif resp.status_code == 404:
                    log.info(f"  Endpoint {endpoint} not found, trying next...")
                    continue
                elif resp.status_code in (429, 403):
                    log.warning(f"  Rate limited / forbidden on {endpoint}")
                    break

            except Exception as exc:
                log.error(f"  Register exception ({endpoint}): {exc}")
                continue

        return False

    def _login(self, email: str, password: str, proxy: Optional[str] = None) -> Optional[str]:
        """
        Login via Kling ID endpoint.
        Returns cookie string on success, None on failure.
        """
        proxies = {"http": proxy, "https": proxy} if proxy else None
        session = requests.Session()
        if proxies:
            session.proxies.update(proxies)

        form_data = {
            "sid": "ksi18n.ai.portal",
            "email": email,
            "password": password,
            "language": "en",
        }
        headers = {
            "User-Agent": API_HEADERS["User-Agent"],
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://klingai.com",
            "Referer": "https://klingai.com/",
        }

        try:
            resp = session.post(KLING_LOGIN, data=form_data, headers=headers, timeout=20)
            log.info(f"  [login] status={resp.status_code} | {resp.text[:300]}")

            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") in (200, 0) or data.get("code") in (200, 0):
                    # Extract cookie string
                    cookies = "; ".join([f"{k}={v}" for k, v in session.cookies.items()])
                    # Also check for token in response body
                    token = data.get("data", {})
                    if isinstance(token, dict):
                        access_token = token.get("accessToken") or token.get("token")
                        if access_token:
                            cookies = f"kToken={access_token}; {cookies}"
                    return cookies if cookies else None

        except Exception as exc:
            log.error(f"  Login exception: {exc}")

        return None

    def _claim_daily_bonus(self, cookie: str, proxy: Optional[str] = None) -> float:
        """
        Attempt to claim daily login bonus.
        Returns credits (float), 0.0 if unknown or failed.
        """
        proxies = {"http": proxy, "https": proxy} if proxy else None
        headers = {
            **API_HEADERS,
            "Cookie": cookie,
        }
        session = requests.Session()
        if proxies:
            session.proxies.update(proxies)

        # Try sign-in endpoint
        try:
            resp = session.post(KLING_DAILY_BONUS, headers=headers, json={}, timeout=20)
            log.info(f"  [daily_bonus] signIn: {resp.status_code} | {resp.text[:200]}")
            if resp.status_code == 200:
                data = resp.json()
                credits = (
                    data.get("data", {}).get("credits")
                    or data.get("credits")
                    or data.get("data", {}).get("point")
                    or 0.0
                )
                return float(credits)
        except Exception as exc:
            log.warning(f"  Daily bonus exception: {exc}")

        # Try fetching user info to get current credits
        try:
            resp = session.get(KLING_USER_INFO, headers=headers, timeout=20)
            log.info(f"  [userInfo] {resp.status_code} | {resp.text[:200]}")
            if resp.status_code == 200:
                data = resp.json()
                info = data.get("data", {})
                credits = info.get("credits") or info.get("point") or info.get("balance") or 0.0
                return float(credits)
        except Exception as exc:
            log.warning(f"  userInfo exception: {exc}")

        return 0.0

    # ── Storage ────────────────────────────────────────────────────────────────

    def _load_accounts(self):
        """Load existing accounts from JSON store."""
        if self.accounts_path.exists():
            try:
                with open(self.accounts_path) as f:
                    self._accounts = json.load(f)
            except Exception:
                self._accounts = []
        else:
            self._accounts = []

    def _save_account(self, result: dict):
        """Append account to JSON store."""
        self._accounts.append(result)
        try:
            with open(self.accounts_path, "w") as f:
                json.dump(self._accounts, f, indent=2)
            log.info(f"  Saved account to {self.accounts_path}")
        except Exception as exc:
            log.error(f"  Failed to save account: {exc}")

    def list_accounts(self) -> list:
        """Return all saved accounts."""
        return self._accounts

    def export_cookies(self) -> list:
        """Return only successful accounts with cookies."""
        return [a for a in self._accounts if a.get("success") and a.get("cookie")]


# ── CLI entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Kling AI Account Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 kling_account_generator.py --count 1
  python3 kling_account_generator.py --count 5 --proxy-list proxies.txt
  python3 kling_account_generator.py --count 3 --proxy http://user:pass@host:port
  python3 kling_account_generator.py --list-accounts
        """,
    )
    parser.add_argument("--count", type=int, default=1, help="Number of accounts to generate")
    parser.add_argument("--proxy", type=str, default=None, help="Single proxy URL (http://user:pass@host:port)")
    parser.add_argument("--proxy-list", type=str, default=None, help="Path to file with one proxy per line")
    parser.add_argument("--output", type=str, default=None, help="Output JSON file path")
    parser.add_argument("--otp-timeout", type=int, default=90, help="OTP wait timeout in seconds")
    parser.add_argument("--list-accounts", action="store_true", help="List all saved accounts and exit")
    args = parser.parse_args()

    # Load proxy list
    proxy_list = None
    if args.proxy_list:
        with open(args.proxy_list) as f:
            proxy_list = [line.strip() for line in f if line.strip()]
        log.info(f"Loaded {len(proxy_list)} proxies from {args.proxy_list}")
    elif args.proxy:
        proxy_list = [args.proxy]

    # Init generator
    output_path = Path(args.output) if args.output else None
    gen = KlingAccountGenerator(accounts_path=output_path, otp_timeout=args.otp_timeout)

    # List mode
    if args.list_accounts:
        accounts = gen.list_accounts()
        print(f"\n{'='*60}")
        print(f"Saved Accounts: {len(accounts)}")
        print(f"{'='*60}")
        for i, acc in enumerate(accounts, 1):
            status = "✅" if acc.get("success") else "❌"
            print(f"{i:3}. {status} {acc.get('email','?')} | credits={acc.get('credits',0)} | {acc.get('timestamp','')[:19]}")
        import sys; sys.exit(0)

    # Generate accounts
    if args.count == 1:
        proxy = proxy_list[0] if proxy_list else None
        result = gen.generate_account(proxy=proxy)
        print(f"\n{'='*60}")
        print(f"Result: {'✅ SUCCESS' if result['success'] else '❌ FAILED'}")
        for k, v in result.items():
            if k == "cookie" and v:
                print(f"  {k}: {v[:60]}...")
            else:
                print(f"  {k}: {v}")
    else:
        results = gen.batch_generate(count=args.count, proxy_list=proxy_list)
        ok = sum(1 for r in results if r.get("success"))
        print(f"\n{'='*60}")
        print(f"Batch complete: {ok}/{len(results)} succeeded")
        for i, r in enumerate(results, 1):
            status = "✅" if r.get("success") else "❌"
            print(f"  {i}. {status} {r.get('email','?')} — {r.get('error') or 'OK'}")
        print(f"\nAccounts saved to: {gen.accounts_path}")


# ─── 1proxy Integration ───────────────────────────────────────────────────────

ONEPROXY_API = os.environ.get("ONEPROXY_API_URL", "https://helpful-alignment-production-2ae5.up.railway.app")  # Local 1proxy backend


def get_proxy_from_1proxy(
    strategy: str = "quality",
    protocol: str = "http",
    max_latency: int = 3000,
    session_id: str = None,
    retries: int = 2,
) -> Optional[str]:
    """
    Get a fresh proxy from 1proxy backend (Railway cloud).
    Handles Railway cold-start with retry.
    
    Returns:
        Proxy URL string like "http://ip:port" or None if unavailable
    """
    params = {
        "strategy": strategy,
        "protocol": protocol,
    }
    if max_latency:
        params["max_latency"] = max_latency
    if session_id:
        params["session_id"] = session_id

    for attempt in range(retries + 1):
        try:
            # Railway cold start can take 15-30s
            timeout = 30 if attempt > 0 else 10
            r = requests.get(
                f"{ONEPROXY_API}/api/v1/proxies/rotate",
                params=params,
                timeout=timeout
            )
            if r.status_code == 200:
                data = r.json()
                url = data.get("url")
                if url:
                    return url
        except Exception as e:
            if attempt < retries:
                logging.info(f"1proxy attempt {attempt+1} failed ({e}), retrying (Railway cold start)...")
                time.sleep(5)
            else:
                logging.debug(f"1proxy unavailable after {retries+1} attempts: {e}")
    return None


def get_proxy_list_from_1proxy(count: int = 20, protocol: str = "http") -> list:
    """
    Get a list of proxies from 1proxy backend.
    
    Returns:
        List of proxy URL strings
    """
    try:
        r = requests.get(
            f"{ONEPROXY_API}/api/v1/proxies",
            params={"limit": count, "protocol": protocol, "is_working": "true"},
            timeout=5
        )
        if r.status_code == 200:
            data = r.json()
            proxies = data.get("proxies", [])
            urls = []
            for p in proxies:
                url = p.get("url") or f"http://{p['ip']}:{p['port']}"
                urls.append(url)
            return urls
    except Exception as e:
        logging.debug(f"1proxy list unavailable: {e}")
    return []


def test_proxy_for_kling(proxy_url: str, timeout: int = 10) -> bool:
    """Test if a proxy can reach Kling."""
    proxies = {"http": proxy_url, "https": proxy_url}
    try:
        r = requests.get(
            "https://klingai.com/",
            proxies=proxies,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0 Chrome/120.0"}
        )
        return r.status_code == 200 and "kGateway-identity" in r.cookies
    except Exception:
        return False


def find_working_proxy(max_tries: int = 20) -> Optional[str]:
    """
    Find a proxy that actually works for Kling.
    Tries proxies from 1proxy until one succeeds.
    
    Returns:
        Working proxy URL or None
    """
    proxy_list = get_proxy_list_from_1proxy(count=max_tries)
    
    if not proxy_list:
        logging.warning("No proxies from 1proxy backend")
        return None
    
    logging.info(f"Testing {len(proxy_list)} proxies for Kling access...")
    
    for i, proxy_url in enumerate(proxy_list):
        logging.debug(f"Testing proxy {i+1}/{len(proxy_list)}: {proxy_url}")
        if test_proxy_for_kling(proxy_url, timeout=8):
            logging.info(f"✅ Working proxy found: {proxy_url}")
            return proxy_url
        
    logging.warning("No working proxies found in pool")
    return None
