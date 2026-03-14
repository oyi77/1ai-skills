#!/usr/bin/env python3
"""
LYNK Revenue Monitor - Polls orders page and sends Telegram alert on new paid sales.
Cron: every hour. Alerts on new SUCCESS+paid orders.
"""
import requests, re, json, time
from datetime import datetime
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def make_session():
    """Session with auto-retry on connection errors."""
    s = requests.Session()
    retry = Retry(total=3, backoff_factor=2,
                  status_forcelist=[500, 502, 503, 504],
                  allowed_methods=["GET", "POST"])
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    s.headers["User-Agent"] = "Mozilla/5.0 Chrome/120"
    return s

BASE_DIR   = Path("/home/openclaw/.openclaw/workspace")
STATE_FILE = BASE_DIR / "logs" / "lynk_revenue_state.json"
LOG_FILE   = BASE_DIR / "logs" / "lynk_monitoring.log"
LYNK_BASE  = "https://lynk.id"
LYNK_EMAIL    = "ketananna@yahoo.com"
LYNK_PASSWORD = "1Milyarberkah$"
BOT_TOKEN  = "8581574594:AAGzrA9DGjzJx3Ak2D6P3NhoQyXyskpMF2Q"
CHAT_ID    = "5220170786"

def tg(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=20)
    except: pass

def load_state():
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
    except: pass
    return {"known_ids": [], "total_paid": 0}

def save_state(s):
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(s, indent=2))

def login():
    s = make_session()
    r = s.get(f"{LYNK_BASE}/login", timeout=20)
    csrf = re.search(r'name=["\']_csrf_token["\'][^>]*value=["\']([^"\']+)["\']', r.text) or \
           re.search(r'value=["\']([^"\']+)["\'][^>]*name=["\']_csrf_token["\']', r.text)
    r2 = s.post(f"{LYNK_BASE}/auth/login", data={
        '_csrf_token': csrf.group(1) if csrf else '',
        'username': LYNK_EMAIL, 'password': LYNK_PASSWORD,
    }, allow_redirects=True, timeout=20)
    return s if 'dashboard' in r2.url or 'admin' in r2.url else None

def get_orders(session):
    r = session.get(f"{LYNK_BASE}/admin/orders/home", timeout=20)
    if 'orders' not in r.url:
        return None
    html = r.text
    
    # Parse order blocks from data attributes
    # Each order has: data-order-id, data-source, data-ref-id, data-cust-email, data-created-at
    order_blocks = re.findall(
        r'data-order-id=["\']([^"\']+)["\']'     # order_id
        r'.*?data-(?:transaction-id)=["\']([^"\']+)["\']'  # txn_id
        r'.*?data-is-printed=["\']([^"\']*)["\']'
        r'.*?data-source=["\']([^"\']+)["\']'    # FREE or payment method
        r'.*?data-ref-id=["\']([^"\']+)["\']'    # detail page id
        r'.*?data-cust-name=["\']([^"\']*)["\']'
        r'.*?data-cust-email=["\']([^"\']*)["\']',
        html, re.DOTALL
    )
    
    # Get created-at dates
    created_ats = re.findall(r'data-created-at=["\']([^"\']+)["\']', html)
    
    # Get amounts from SUCCESS order blocks  
    amounts_map = {}
    for ref_id in re.findall(r'data-ref-id=["\']([^"\']+)["\']', html):
        idx = html.index(f'data-ref-id="{ref_id}"')
        chunk = html[idx:idx+2000]
        amt = re.search(r'Rp\.\s*([\d,]+)', chunk)
        status = re.search(r'(SUCCESS|EXPIRED|PENDING|PAID|FREE)', chunk)
        amounts_map[ref_id] = {
            'amount': int(amt.group(1).replace(',', '')) if amt else 0,
            'status': status.group(1) if status else 'UNKNOWN'
        }
    
    orders = []
    for i, blk in enumerate(order_blocks):
        order_id, txn_id, _, source, ref_id, cust_name, cust_email = blk
        created = created_ats[i*2] if i*2 < len(created_ats) else 'Unknown'
        info = amounts_map.get(ref_id, {})
        
        orders.append({
            'id': ref_id,
            'order_id': order_id,
            'source': source,  # 'FREE' or payment method
            'cust_email': cust_email,
            'cust_name': cust_name,
            'created': created,
            'amount': info.get('amount', 0),
            'status': info.get('status', 'UNKNOWN'),
            'is_paid': source != 'FREE' and info.get('status') in ('SUCCESS', 'PAID'),
        })
    
    return orders

def check():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    state = load_state()
    known = set(state.get('known_ids', []))
    total_paid = state.get('total_paid', 0)
    
    print(f"[{now}] Logging into LYNK...")
    session = login()
    if not session:
        tg(f"⚠️ LYNK Monitor: Login FAILED at {now}")
        return
    
    orders = get_orders(session)
    if orders is None:
        tg(f"⚠️ LYNK Monitor: Could not fetch orders at {now}")
        return
    
    print(f"  {len(orders)} orders fetched")
    
    new_paid = [o for o in orders if o['id'] not in known and o['is_paid']]
    
    if new_paid:
        for o in new_paid:
            total_paid += o['amount']
            msg = (f"💰 <b>NEW PAID SALE!</b>\n\n"
                   f"Customer: {o['cust_email']}\n"
                   f"Amount: IDR {o['amount']:,}\n"
                   f"Source: {o['source']}\n"
                   f"Date: {o['created']}\n\n"
                   f"📊 Total LYNK Revenue: IDR {total_paid:,}")
            tg(msg)
            print(f"  💰 NEW SALE: {o['cust_email']} IDR {o['amount']:,}")
    else:
        print(f"  No new paid sales | Total: IDR {total_paid:,}")

    # Summary stats
    paid_count = sum(1 for o in orders if o['is_paid'])
    free_count = sum(1 for o in orders if o['source'] == 'FREE')
    
    state['known_ids'] = list({o['id'] for o in orders} | known)
    state['total_paid'] = total_paid
    state['last_check'] = now
    state['stats'] = {'total_orders': len(orders), 'paid': paid_count, 'free': free_count}
    save_state(state)
    
    # Log
    LOG_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{now}] orders={len(orders)} paid={paid_count} free={free_count} new_paid={len(new_paid)} total_idr={total_paid}\n")

if __name__ == "__main__":
    check()
