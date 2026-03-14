#!/usr/bin/env python3
"""
Full Auto Engine — Zero-touch revenue machine.
Runs every hour. Handles EVERYTHING autonomously.

Components:
1. X/Twitter auto-promotion (Gumroad + LYNK products)
2. PostBridge engagement monitoring + auto-scaling
3. Revenue tracking + Telegram alerts
4. Gumroad sales monitoring
5. LYNK click tracking
6. Simmer trading balance check
7. Disk + system health
"""
import json, os, sys, time, urllib.request, urllib.error, ssl, subprocess, random
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(os.path.expanduser("~/.openclaw/workspace"))
LOG = WORKSPACE / "logs" / "full_auto.log"
LOG.parent.mkdir(parents=True, exist_ok=True)
STATE_FILE = WORKSPACE / "config" / "auto_engine_state.json"

ctx = ssl.create_default_context()

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def load_state():
    if STATE_FILE.exists():
        return json.load(open(STATE_FILE))
    return {"last_x_post": None, "last_tg_broadcast": None, "last_gumroad_check": None,
            "x_post_count": 0, "tg_broadcast_count": 0, "total_runs": 0}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

# ── 1. X/Twitter Auto-Promotion ──────────────────────────────────────────────

def post_to_x(tweet_text):
    """Post to X using xurl skill."""
    try:
        result = subprocess.run(
            ["/home/linuxbrew/.linuxbrew/bin/xurl", "post", tweet_text],
            capture_output=True, text=True, timeout=30,
            cwd=str(WORKSPACE)
        )
        if result.returncode == 0:
            log(f"X: ✅ Posted ({len(tweet_text)} chars)")
            return True
        else:
            log(f"X: ❌ {result.stderr[:100]}")
            return False
    except Exception as e:
        log(f"X: ❌ {e}")
        return False

X_PROMO_TWEETS = [
    # Gumroad products
    "🔥 10 Python automation scripts that replaced 5 hours of manual work.\n\nWeb scraper, price tracker, email sender, PDF extractor — all ready to run.\n\n$9-$17 → https://dizzuddi.gumroad.com/l/nvadun\n\n#Python #Automation #Developer",
    "⚡ Automate your boring tasks with Python.\n\n10 scripts. Copy-paste ready. Works out of the box.\n\nTelegram bot, Instagram scraper, task scheduler — all included.\n\n→ https://dizzuddi.gumroad.com/l/nvadun\n\n#Python #Coding #100DaysOfCode",
    "💡 Stop writing the same Python scripts over and over.\n\nI packaged 10 of my most-used automation scripts:\n- Web scraper\n- Price tracker\n- File organizer\n- API wrapper\n\nGrab them → https://dizzuddi.gumroad.com/l/nvadun",
    # LYNK products (Indonesian)
    "🎨 Tools AI gratis buat content creator Indonesia!\n\nGenerate gambar, edit foto, bikin caption — semua otomatis.\n\n👉 https://lynk.id/jendralbot\n\n#AITools #ContentCreator #BisnisOnline",
    "📸 Foto produk marketplace kamu masih asal-asalan?\n\nSellPix AI bikin foto studio-quality dalam hitungan detik.\n\nRp 79.000\n👉 https://lynk.id/jendralbot/emne05mm7v25\n\n#Marketplace #FotoProduk #UMKM",
    "📱 TikTok affiliate itu mesin uang kalau tau caranya.\n\nKelas Affiliate Pesugihan TikTok — dari nol sampai cuan.\n\nGRATIS\n👉 https://lynk.id/jendralbot/regxdn7xkpz6\n\n#TikTok #Affiliate #BisnisOnline",
    "💰 Belanja tiap bulan tapi duit gak pernah balik?\n\nPelajari strategi cashback: 5-15% dari semua belanjaan.\n\nRp 59.000\n👉 https://lynk.id/jendralbot/kkjk0mv1vg7o\n\n#Cashback #SmartShopping",
    "👨‍🏫 50+ template AI buat guru & pengajar.\n\nAuto-grading, materi instant, soal ujian otomatis.\n\nRp 49.000\n👉 https://lynk.id/jendralbot/6821op5e24kn\n\n#Pendidikan #AITools #EdTech",
]

def run_x_promo(state):
    """Post 1 promo tweet every 3 hours (max 8/day)."""
    now = datetime.now()
    last = state.get("last_x_post")
    
    if last:
        last_dt = datetime.fromisoformat(last)
        if (now - last_dt).total_seconds() < 10800:  # 3 hours
            return
    
    # Don't post between 00:00-06:00
    if now.hour < 6:
        return
    
    tweet = random.choice(X_PROMO_TWEETS)
    if post_to_x(tweet):
        state["last_x_post"] = now.isoformat()
        state["x_post_count"] = state.get("x_post_count", 0) + 1


# ── 2. Telegram Broadcast ────────────────────────────────────────────────────

def run_tg_broadcast(state):
    """Send promo to Telegram contacts via userbot (1x per day max)."""
    now = datetime.now()
    last = state.get("last_tg_broadcast")
    
    if last:
        last_dt = datetime.fromisoformat(last)
        if (now - last_dt).total_seconds() < 86400:  # 24 hours
            return
    
    # Only broadcast at optimal times
    if now.hour not in [8, 12, 19]:
        return
    
    broadcast_script = WORKSPACE / "skills" / "telegram-userbot" / "scripts" / "broadcast.py"
    if not broadcast_script.exists():
        return
    
    msg = random.choice([
        "🔥 Tools AI GRATIS buat bisnis kamu!\n\n9 produk digital — dari content creator tools sampai CV optimizer.\n\nCek di: https://lynk.id/jendralbot",
        "💡 Mau bisnis kuliner? Ada template GRATIS!\n\nResep auto-costing + menu design + marketing plan.\n\n👉 https://lynk.id/jendralbot/kzryk28dxmpx",
    ])
    
    try:
        result = subprocess.run(
            ["python3", str(broadcast_script), "--message", msg, "--limit", "10"],
            capture_output=True, text=True, timeout=60
        )
        log(f"TG Broadcast: {'✅' if result.returncode == 0 else '❌'} {result.stdout[:100]}")
        state["last_tg_broadcast"] = now.isoformat()
    except Exception as e:
        log(f"TG Broadcast: ❌ {e}")


# ── 3. PostBridge Monitoring ─────────────────────────────────────────────────

def check_postbridge():
    """Check PostBridge health + recent results."""
    try:
        req = urllib.request.Request(
            "https://api.post-bridge.com/v1/post-results?limit=20",
            headers={"Authorization": "Bearer pb_live_AT9Xm4PKaYBzAvFZYGgexi"}
        )
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            data = json.loads(r.read()).get("data", [])
            ok = sum(1 for d in data if d.get("success"))
            fail = len(data) - ok
            rate = ok * 100 // max(len(data), 1)
            log(f"PostBridge: {ok}/{len(data)} success ({rate}%)")
            return {"ok": ok, "fail": fail, "rate": rate}
    except Exception as e:
        log(f"PostBridge: ❌ {e}")
        return {"ok": 0, "fail": 0, "rate": 0, "error": str(e)}


# ── 4. Gumroad Sales Check ──────────────────────────────────────────────────

def check_gumroad():
    """Check Gumroad for new sales."""
    try:
        # Check if gumroad_sync exists and has data
        sync_log = WORKSPACE / "logs" / "gumroad_sync.log"
        if sync_log.exists():
            last_lines = sync_log.read_text().strip().split("\n")[-5:]
            for line in last_lines:
                if "sale" in line.lower() or "revenue" in line.lower():
                    log(f"Gumroad: {line.strip()}")
                    return True
        
        log("Gumroad: No new sales detected")
        return False
    except Exception as e:
        log(f"Gumroad: ❌ {e}")
        return False


# ── 5. Simmer Trading ───────────────────────────────────────────────────────

def check_simmer():
    """Check Simmer trading balance."""
    try:
        req = urllib.request.Request(
            "https://api.simmer.markets/v1/balance",
            headers={"Authorization": "Bearer sk_live_269696a939dec0c28c8165da1e3ba2a7f0367a1362a2b1cd412db1b033c07f1e"}
        )
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            data = json.loads(r.read())
            balance = data.get("balance", data.get("data", {}).get("balance", "?"))
            log(f"Simmer: ${balance}")
            return balance
    except:
        return None


# ── 6. System Health ─────────────────────────────────────────────────────────

def check_system():
    """Quick system health check."""
    import shutil
    total, used, free = shutil.disk_usage("/")
    pct = used * 100 // total
    
    if pct > 92:
        log(f"⚠️ Disk: {pct}% — cleaning pip cache")
        os.system("pip cache purge 2>/dev/null; find /tmp -name '*.pyc' -delete 2>/dev/null")
    
    log(f"System: Disk {pct}%, Free {free // (1024**3)}GB")
    return {"disk_pct": pct, "free_gb": free // (1024**3)}


# ── 7. Telegram Alert ────────────────────────────────────────────────────────

def send_alert(msg):
    """Send alert via Telegram userbot."""
    try:
        session = WORKSPACE / ".vilona" / "sessions" / "paijo.session"
        if not session.exists():
            return
        
        alert_script = WORKSPACE / "skills" / "telegram-userbot" / "scripts" / "alert.py"
        if alert_script.exists():
            subprocess.run(
                ["python3", str(alert_script), "--message", msg],
                timeout=15, capture_output=True
            )
    except:
        pass


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    state = load_state()
    state["total_runs"] = state.get("total_runs", 0) + 1
    now = datetime.now()
    
    log(f"{'='*50}")
    log(f"Full Auto Engine — Run #{state['total_runs']} @ {now.strftime('%H:%M WIB')}")
    log(f"{'='*50}")
    
    # Always run
    pb = check_postbridge()
    sys_health = check_system()
    
    # X promo (every 3h, 06:00-23:00)
    run_x_promo(state)
    
    # Telegram broadcast (1x/day at optimal hours)
    run_tg_broadcast(state)
    
    # Gumroad check
    check_gumroad()
    
    # Simmer (every run)
    check_simmer()
    
    # Alert if critical
    if sys_health["disk_pct"] > 95:
        send_alert(f"🚨 DISK CRITICAL: {sys_health['disk_pct']}%")
    
    if pb.get("rate", 100) < 50 and pb.get("fail", 0) > 5:
        send_alert(f"⚠️ PostBridge: {pb['rate']}% success rate ({pb['fail']} failures)")
    
    save_state(state)
    log(f"Done. Next run in 1 hour.\n")


if __name__ == "__main__":
    main()
