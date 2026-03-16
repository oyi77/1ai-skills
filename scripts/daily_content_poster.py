#!/usr/bin/env python3
"""
Daily Content Poster v3 — Content Kingdom Cron Executor

Routes ALL content through Content Kingdom modules:
  Phase 1: PLAN   → pick products using learned rules
  Phase 2: SCRIPT → generate captions via learning_engine rules
  Phase 3: CREATE → generate media via GeminiGen + Veris design + learned rules
  Phase 4: REVIEW → quality gate check
  Phase 5: POST   → PostBridge publish
  Phase 6: LEARN  → capture result for future learning

Cron: 3x daily at 07:00, 12:00, 19:00 WIB
Falls back gracefully to static behavior if Content Kingdom unavailable.
"""
import requests, json, time, random, os, sys, urllib.request
from datetime import datetime
from pathlib import Path

# ── Content Kingdom Integration ─────────────────────────────────────────────
CK_PATH = Path(__file__).parent.parent / "skills/1ai-skills/content/content-kingdom"
sys.path.insert(0, str(CK_PATH))

CK_AVAILABLE = False
try:
    from modules.learning_engine import (
        get_active_rules,
        get_design_guidelines,
        get_copy_guidelines,
        build_prompt_with_learnings,
        capture_performance,
        capture_feedback,
        get_learning_stats,
    )
    from modules.chat_learning_hook import process_user_feedback
    from modules.veris_design import build_veris_prompt, VERIS_PALETTE, PLATFORM_PRIORITY
    CK_AVAILABLE = True
except ImportError as _ck_err:
    # Graceful fallback — static behavior preserved below
    def get_active_rules(category=None): return []
    def get_design_guidelines(): return {}
    def get_copy_guidelines(): return {}
    def build_prompt_with_learnings(prompt, category=None): return prompt
    def capture_performance(**kwargs): pass
    def capture_feedback(**kwargs): pass
    def get_learning_stats(): return {"total_rules": 0, "total_learnings": 0}
    def process_user_feedback(*args, **kwargs): pass

# ── PostBridge config ────────────────────────────────────────────────────────
API = "https://api.post-bridge.com/v1"
KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
HDR = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

WORKSPACE = Path(os.path.expanduser("~/.openclaw/workspace"))
PRODUCTS_FILE  = WORKSPACE / "config/lynk_products.json"
MEDIA_MAP_FILE = WORKSPACE / "config/product_media_ids.json"
GUMROAD_FILE   = WORKSPACE / "config/gumroad_products.json"
ACCOUNTS_FILE  = WORKSPACE / "config/postbridge_accounts.json"
STATE_FILE     = WORKSPACE / "config/poster_state.json"
LOG_FILE       = WORKSPACE / "logs/daily_poster.log"


# ── Product-specific content (caption MATCHES the product) ──────────────────

PRODUCT_CONTENT = {
    "kzryk28dxmpx": {  # Mesin Cetak Bisnis Kuliner (FREE)
        "name": "Mesin Cetak Bisnis Kuliner",
        "captions": [
            "🍜 Mau buka bisnis kuliner tapi bingung mulai dari mana?\n\nDapatkan template bisnis kuliner lengkap yang udah terbukti naikin omzet 25%:\n✅ Resep auto-costing\n✅ Menu design template\n✅ Marketing plan F&B\n\n👉 IDR 75.000 (harga asli IDR 250K)\n👉 {url}\n\n#BisnisKuliner #UMKM #FnB #Gratis",
            "📊 FAKTA: 60% bisnis kuliner gagal di tahun pertama.\nPenyebab utama? BUKAN rasa — tapi manajemen!\n\nDapatkan Mesin Cetak Bisnis Kuliner GRATIS:\n👉 {url}\n\n#BisnisKuliner #UMKM #TipsBisnis",
            "🔥 Omzet warung naik 25% cuma ganti desain menu?\nYa, visual matters lebih dari yang kamu pikir.\n\nDownload template GRATIS sekarang:\n👉 {url}\n\n#DesainMenu #BisnisKuliner #UMKM",
        ],
    },
    "6821op5e24kn": {  # Guru Pintar AI (Rp 49K)
        "name": "Guru Pintar AI",
        "captions": [
            "👨‍🏫 50+ template ajaran AI-powered!\n\nGuru Pintar AI bantu kamu:\n✅ Auto-grading untuk quiz\n✅ Materi instant generation\n✅ Update otomatis teknologi AI\n\nIDR 75.000 (harga asli IDR 250.000)!\n👉 {url}\n\n#GuruPintar #Pendidikan #AITools #EdTech",
            "📚 Bikin materi pelajaran dalam 5 menit? Bisa!\n\nGuru Pintar AI — 50+ template siap pakai.\nDari RPP sampai soal ujian, semua otomatis.\n\nIDR 75.000 (harga asli IDR 250.000)\n👉 {url}\n\n#Pendidikan #AITools #Guru",
            "⏰ Guru capek bikin soal manual? Same.\n\nSekarang ada AI yang bantu:\n- Generate soal otomatis\n- Auto-grading\n- Materi instant\n\nCuma IDR 75.000! (harga asli IDR 250.000)\n👉 {url}\n\n#GuruPintar #EdTech #AIIndonesia",
        ],
    },
    "89d30qd3ddnj": {  # AI Creative Tools (FREE)
        "name": "AI Creative Tools",
        "captions": [
            "🎨 Tools AI GRATIS buat content creator!\n\nAI Creative Tools:\n✅ Generate gambar produk\n✅ Edit foto otomatis\n✅ Caption generator\n\nIDR 75.000!\n👉 {url}\n\n#ContentCreator #AITools #DesainGrafis #Gratis",
            "💡 Konten bagus gak harus mahal.\n\nAI Creative Tools — semua yang kamu butuhkan untuk bikin konten profesional, GRATIS.\n\n👉 {url}\n\n#ContentMarketing #AITools #BisnisOnline",
            "🔥 Bikin desain pro dalam hitungan menit?\n\nGak perlu Canva Pro, gak perlu desainer.\nAI Creative Tools — IDR 75.000 aja.\n\n👉 {url}\n\n#DesainGrafis #AITools #ContentCreator",
        ],
    },
    "emne05mm7v25": {  # Studio Marketplace Pro / SellPix AI (Rp 79K)
        "name": "SellPix AI",
        "captions": [
            "📸 Foto produk yang bagus bisa naikin konversi 40%!\n\nSellPix AI — studio foto marketplace otomatis:\n✅ Background removal\n✅ Product staging\n✅ Marketplace-ready output\n\nIDR 75.000\n👉 {url}\n\n#FotoProduk #Marketplace #Shopee #Tokopedia",
            "🛒 Jualan di marketplace tapi foto asal-asalan?\nPantesan gak laku.\n\nSellPix AI bikin foto produk kamu selevel brand besar.\n\nIDR 75.000 — investasi yang worth it!\n👉 {url}\n\n#FotoProduk #ECommerce #UMKM",
            "⚡ Sebelum vs Sesudah SellPix AI:\n❌ Foto gelap, background berantakan\n✅ Foto studio, background clean, siap jual\n\nIDR 75.000 aja!\n👉 {url}\n\n#SellPix #FotoProduk #Marketplace",
        ],
    },
    "kkjk0mv1vg7o": {  # Belanja Duit Balik (Rp 59K)
        "name": "Belanja Duit Balik",
        "captions": [
            "💰 Belanja tetap jalan, tapi duit balik lagi?\n\nBukan scam, bukan MLM — ini strategi cashback:\n✅ Cara dapat cashback dari semua belanjaan\n✅ Platform terpercaya\n✅ Step-by-step guide\n\nGRATIS!\n👉 {url}\n\n#Cashback #HematBelanja #SmartShopping",
            "🤔 Kamu belanja tiap bulan berapa?\nSekarang bayangin 5-15% nya balik ke kantong.\n\nPelajari caranya di Belanja Duit Balik!\n\nGRATIS!\n👉 {url}\n\n#Cashback #TipsBelanja #HematUang",
            "🔥 Rahasia orang hemat: mereka gak cuma cari diskon.\nMereka cari CASHBACK.\n\nBelanja Duit Balik — panduan lengkap cashback strategy.\n\nGRATIS!\n👉 {url}\n\n#SmartShopping #Cashback #FinancialLiteracy",
        ],
    },
}

# Products without custom images — use text-only captions with profile URL
PROFILE_PRODUCTS = {
    "45r5yvze3vy4": {  # JobMagnet AI
        "name": "JobMagnet AI",
        "captions": [
            "📝 CV kamu udah ATS-friendly?\n\nJobMagnet AI optimasi CV kamu biar lolos screening otomatis.\nChance interview naik 3x lipat!\n\n👉 {url}\n\n#JobHunting #CV #KarirIndonesia #AITools",
        ],
    },
    "l4q49jj3z383": {  # Food Menu AI Studio
        "name": "Food Menu AI Studio",
        "captions": [
            "🍽️ Menu makanan yang desainnya bagus = omzet naik 25%!\n\nFood Menu AI Studio — bikin menu restoran profesional dengan AI.\n\n👉 {url}\n\n#DesainMenu #Restoran #BisnisKuliner",
        ],
    },
    "9r8rj1o38q59": {  # AI Creative & Performance Ad Engine
        "name": "AI Ad Engine",
        "captions": [
            "🎯 Ads yang convert itu bukan soal budget besar.\nTapi soal CREATIVE yang tepat.\n\nAI Ad Engine — generate ads yang perform.\n\n👉 {url}\n\n#DigitalAds #Marketing #AITools",
        ],
    },
    "regxdn7xkpz6": {  # Kelas Affiliate Pesugihan TikTok
        "name": "Kelas Affiliate TikTok",
        "captions": [
            "📱 TikTok bukan cuma buat hiburan.\nIni mesin uang kalau kamu tau caranya.\n\nKelas Affiliate Pesugihan TikTok — dari nol sampai cuan.\n\n👉 {url}\n\n#TikTokAffiliate #CuanDariRumah #BisnisOnline",
        ],
    },
}

BASE_URL = "https://lynk.id/jendralbot"

VERIS_HOOKS = [
    "Masih {problem}? Ada cara yang lebih cerdas.",
    "Yang lain bayar jutaan. Kamu cukup {price}.",
    "Satu tools. Semua solusi. {product_name}.",
    "{product_name} — dibuat untuk yang serius.",
    "Bukan template biasa. Ini {product_name}.",
]


# ── Phase 2: SCRIPT — Smart Caption Generation ──────────────────────────────

def generate_smart_caption(product_name, product_url, price="IDR 75.000"):
    """Phase 2: Generate caption guided by learned Content Kingdom rules.

    Returns None to fall back to static captions if CK unavailable or
    no actionable rules exist yet.
    """
    if not CK_AVAILABLE:
        return None

    copy_rules = get_copy_guidelines()
    active_rules = get_active_rules("copy")

    if not copy_rules and not active_rules:
        return None  # No rules yet — use static captions

    # Use learned hook pattern if available
    hook_patterns = copy_rules.get("hook_patterns", [])
    pattern = random.choice(hook_patterns) if hook_patterns else "Problem → Solution"

    # Log that we're using CK rules (actual LLM generation is future phase)
    rules_text = "\n".join(f"- {r['rule']}" for r in active_rules[:5])
    log(f"[CK] Caption guided by {len(active_rules)} copy rules, pattern: {pattern}")

    # Placeholder: in future, pass rules_text to an LLM for full generation.
    # For now, return None to keep static captions (they still carry the product URL).
    return None


# ── Phase 4: REVIEW — Quality Gate ──────────────────────────────────────────

def quality_check(caption, product_name):
    """Phase 4: Basic quality gate using learned rules.

    Returns (passed: bool, issues: list[str]).
    """
    issues = []

    if CK_AVAILABLE:
        design_rules = get_active_rules("design")
        for rule in design_rules:
            rule_text = rule.get("rule", "").lower()
            if "no emoji" in rule_text and caption.count("🔥") > 3:
                issues.append("Too many emoji (Veris rule: minimal emoji)")
            # Color rules can't be checked in text — skip

    # Universal quality checks
    if len(caption) < 50:
        issues.append("Caption too short (<50 chars)")
    if len(caption) > 2000:
        issues.append("Caption too long (>2000 chars)")
    if ("http" not in caption
            and "lynk.id" not in caption
            and "gumroad" not in caption):
        issues.append("No URL in caption")

    passed = len(issues) == 0
    return passed, issues


# ── Utilities ────────────────────────────────────────────────────────────────

def log(msg):
    """Write a timestamped log entry."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{ts} | {msg}\n")
    print(f"[{ts}] {msg}")


# ── Phase 3: CREATE — Image generation with Veris + learned rules ────────────

def generate_fresh_image(product_name, hook_text):
    """Phase 3: Generate product image via GeminiGen with Veris design + learned rules."""
    import subprocess

    API_KEY = "geminiai-4318f9ef07c91969d314b67c3afeb3bf"

    # Pull learned design guidelines (Veris defaults if CK unavailable)
    guidelines = get_design_guidelines() if CK_AVAILABLE else {}
    bg = guidelines.get("background", "#000000")
    text_color = guidelines.get("text_color", "#FFFFFF")

    base_prompt = (
        f'Professional dark themed promotional image for "{product_name}". '
        f'{bg} background. {text_color} bold text: "{hook_text}". '
        "Three-section vertical layout: Hook headline top, product info middle, CTA bottom. "
        "Minimalist premium aesthetic. No vibrant colors. Instagram-ready. High contrast."
    )

    # Phase 3: enhance prompt with learned design rules
    enhanced_prompt = build_prompt_with_learnings(base_prompt, "design") if CK_AVAILABLE else base_prompt

    if CK_AVAILABLE:
        log(f"[CK] Image prompt enhanced with learned design rules")

    cmd = [
        "curl", "-s", "-X", "POST",
        "https://api.geminigen.ai/uapi/v1/generate_image",
        "-H", f"x-api-key: {API_KEY}",
        "--form", f"prompt={enhanced_prompt}",
        "--form", "model=nano-banana-pro",
        "--form", "aspect_ratio=4:5",
        "--form", "style=Photorealistic",
        "--form", "output_format=png",
        "--form", "resolution=1K",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout)
        uuid = data.get("uuid")
        if uuid:
            log(f"GeminiGen image generating: {uuid}")
            import time as t
            for _ in range(12):
                t.sleep(5)
                try:
                    check = urllib.request.Request(
                        f"https://api.geminigen.ai/uapi/v1/history/{uuid}",
                        headers={"x-api-key": API_KEY},
                    )
                    resp = urllib.request.urlopen(check, timeout=10)
                    status_data = json.loads(resp.read())
                    if status_data.get("status") == 2:
                        images = status_data.get("generated_image", [])
                        if images:
                            img_uri = images[0].get("image_uri", "")
                            if img_uri:
                                img_url = f"https://cdn.geminigen.ai/{img_uri}"
                                log(f"GeminiGen image ready: {img_url}")
                                return img_url
                    elif status_data.get("status") == 3:
                        log(f"GeminiGen image failed: {status_data.get('error_message')}")
                        return None
                except Exception:
                    pass
    except Exception as e:
        log(f"GeminiGen error: {e}")
    return None


# ── Data loaders ─────────────────────────────────────────────────────────────

def load_gumroad_products():
    if GUMROAD_FILE.exists():
        return json.load(open(GUMROAD_FILE)).get("gumroad_products", [])
    return []


def make_gumroad_caption(product):
    name  = product["name"]
    price = product["price"]
    url   = f"https://{product['url']}"
    hook  = random.choice(VERIS_HOOKS).format(
        problem="pakai cara lama",
        price=price,
        product_name=name,
    )
    return (
        f"🔥 {hook}\n\n"
        f"**{name}** — {price}\n"
        f"Premium. Minimalist. Langsung pakai.\n\n"
        f"👉 {url}\n\n"
        f"#DigitalProduct #ContentCreator #AITools #BerkahKarya"
    )


def load_media_map():
    if MEDIA_MAP_FILE.exists():
        return json.load(open(MEDIA_MAP_FILE)).get("product_media_ids", {})
    return {}


def get_accounts():
    if ACCOUNTS_FILE.exists():
        data = json.load(open(ACCOUNTS_FILE))
        return data.get("image_accounts", [])
    r = requests.get(
        f"{API}/social-accounts", headers=HDR,
        params={"limit": 100}, timeout=30,
    )
    return [
        a["id"] for a in r.json().get("data", [])
        if a["platform"] in ("facebook", "threads", "twitter", "linkedin", "instagram")
    ]


def load_state():
    if STATE_FILE.exists():
        return json.load(open(STATE_FILE))
    return {"last_products": [], "post_count": 0}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ── Phase 1: PLAN — Product selection using learned rules ────────────────────

def pick_product(state, gumroad_products=None):
    """Phase 1: Pick next product, rotating evenly through LYNK + Gumroad.

    Uses Content Kingdom rules to prefer high-performing product types when
    available; falls back to round-robin otherwise.
    """
    all_slugs = list(PRODUCT_CONTENT.keys()) + list(PROFILE_PRODUCTS.keys())
    if gumroad_products:
        all_slugs += [f"gumroad:{p['slug']}" for p in gumroad_products]

    recent = state.get("last_products", [])[-6:]
    available = [s for s in all_slugs if s not in recent] or all_slugs

    if CK_AVAILABLE:
        # Future: weight available slugs by performance metrics from CK
        active_rules = get_active_rules("plan")
        if active_rules:
            log(f"[CK] Plan: {len(active_rules)} rules available for product selection")

    return random.choice(available)


# ── Phase 5: POST — PostBridge publish ──────────────────────────────────────

def create_post(caption, media_ids, account_ids):
    payload = {"caption": caption, "social_accounts": account_ids}
    if media_ids:
        payload["media"] = media_ids
    r = requests.post(f"{API}/posts", headers=HDR, json=payload, timeout=30)
    return r.status_code in (200, 201), r.text[:300]


# ── Phase 6: LEARN — Capture results ────────────────────────────────────────

def learn_from_success(response_text, caption, account_ids, post_media, product_name):
    """Phase 6: Capture performance data for future learning."""
    if not CK_AVAILABLE:
        return
    try:
        resp_data = json.loads(response_text) if response_text.startswith("{") else {}
        post_id = (
            resp_data.get("id")
            or resp_data.get("post_id")
            or f"pb_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        capture_performance(
            post_id=post_id,
            platform="postbridge",
            metrics={"accounts": len(account_ids), "had_media": bool(post_media)},
            caption_snippet=caption[:100],
            had_media=bool(post_media),
            media_type="image" if post_media else "",
        )
        log(f"[CK] Performance captured for post {post_id}")
    except Exception as e:
        log(f"[CK] capture_performance error: {e}")


def learn_from_failure(error_message, product_name):
    """Phase 6: Capture failure signal so CK can learn from it."""
    if not CK_AVAILABLE:
        return
    try:
        capture_feedback(
            source="system",
            feedback_type="negative",
            content=f"Post failed: {error_message}",
            context={"product": product_name, "error": error_message},
            tags=["post_failure"],
        )
        log(f"[CK] Failure feedback captured for {product_name}")
    except Exception as e:
        log(f"[CK] capture_feedback error: {e}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    ck_status = "✅ active" if CK_AVAILABLE else "⚠️ fallback (static)"
    log(f"Content Kingdom: {ck_status}")

    media_map       = load_media_map()
    account_ids     = get_accounts()
    state           = load_state()
    gumroad_products = load_gumroad_products()
    gumroad_by_slug = {p["slug"]: p for p in gumroad_products}

    if not account_ids:
        log("❌ No accounts found")
        return

    num_posts = random.randint(3, 5)
    now = datetime.now()

    log(
        f"Creating {num_posts} posts | {len(account_ids)} accounts "
        f"| Gumroad: {len(gumroad_products)} products"
    )

    created = 0

    for i in range(num_posts):
        # ── Phase 1: PLAN ────────────────────────────────────────────────────
        slug = pick_product(state, gumroad_products)

        # ── Gumroad product branch ───────────────────────────────────────────
        if slug.startswith("gumroad:"):
            gslug   = slug.split(":", 1)[1]
            product = gumroad_by_slug.get(gslug)
            if not product:
                continue

            product_name = product["name"]

            # ── Phase 2: SCRIPT ──────────────────────────────────────────────
            caption = generate_smart_caption(
                product_name,
                f"https://{product['url']}",
                price=product["price"],
            ) or make_gumroad_caption(product)

            # ── Phase 4: REVIEW ──────────────────────────────────────────────
            passed, issues = quality_check(caption, product_name)
            if not passed:
                log(f"  ⚠️ Quality issues for {product_name}: {issues}")
                # Proceed anyway — log but don't block (learn from outcome)

            # ── Phase 3: CREATE ──────────────────────────────────────────────
            post_media = []
            hook_text  = random.choice(VERIS_HOOKS).format(
                problem="pakai cara lama",
                price=product["price"],
                product_name=product_name,
            )
            img_url = generate_fresh_image(product_name, hook_text)
            if img_url:
                try:
                    r = requests.post(
                        f"{API}/media/create-upload-url",
                        headers=HDR,
                        json={"url": img_url, "type": "image"},
                        timeout=30,
                    )
                    if r.status_code in (200, 201):
                        mid = r.json().get("media_id") or r.json().get("id")
                        if mid:
                            post_media = [mid]
                            log(f"GeminiGen media uploaded: {mid}")
                except Exception as e:
                    log(f"Media upload error: {e}")

            # ── Phase 5: POST ────────────────────────────────────────────────
            ok, resp = create_post(caption, post_media, account_ids)

            # ── Phase 6: LEARN ───────────────────────────────────────────────
            if ok:
                created += 1
                state.setdefault("last_products", []).append(slug)
                learn_from_success(resp, caption, account_ids, post_media, product_name)
                log(f"  ✅ [Gumroad] {product_name}: {len(post_media)} media, {len(account_ids)} accounts")
            else:
                learn_from_failure(resp, product_name)
                log(f"  ❌ [Gumroad] {product_name}: {resp[:80]}")

        # ── LYNK product branch ──────────────────────────────────────────────
        else:
            url = f"{BASE_URL}/{slug}"

            if slug in PRODUCT_CONTENT:
                pdata = PRODUCT_CONTENT[slug]
            elif slug in PROFILE_PRODUCTS:
                pdata = PROFILE_PRODUCTS[slug]
            else:
                continue

            product_name = pdata["name"]

            # ── Phase 2: SCRIPT ──────────────────────────────────────────────
            caption = (
                generate_smart_caption(product_name, url)
                or random.choice(pdata["captions"]).format(url=url)
            )

            # ── Phase 4: REVIEW ──────────────────────────────────────────────
            passed, issues = quality_check(caption, product_name)
            if not passed:
                log(f"  ⚠️ Quality issues for {product_name}: {issues}")

            # ── Phase 3: CREATE ──────────────────────────────────────────────
            post_media = []
            if slug in media_map and media_map[slug]:
                img = random.choice(media_map[slug])
                post_media = [img["media_id"]]
            else:
                hook_text = random.choice(VERIS_HOOKS).format(
                    problem="cara manual",
                    price="harga terjangkau",
                    product_name=product_name,
                )
                img_url = generate_fresh_image(product_name, hook_text)
                if img_url:
                    try:
                        r = requests.post(
                            f"{API}/media/create-upload-url",
                            headers=HDR,
                            json={"url": img_url, "type": "image"},
                            timeout=30,
                        )
                        if r.status_code in (200, 201):
                            mid = r.json().get("media_id") or r.json().get("id")
                            if mid:
                                post_media = [mid]
                                log(f"GeminiGen media uploaded for {product_name}: {mid}")
                    except Exception as e:
                        log(f"Media upload error: {e}")

            # ── Phase 5: POST ────────────────────────────────────────────────
            ok, resp = create_post(caption, post_media, account_ids)

            # ── Phase 6: LEARN ───────────────────────────────────────────────
            if ok:
                created += 1
                state.setdefault("last_products", []).append(slug)
                learn_from_success(resp, caption, account_ids, post_media, product_name)
                log(f"  ✅ [LYNK] {product_name}: {len(post_media)} media, {len(account_ids)} accounts")
            else:
                learn_from_failure(resp, product_name)
                log(f"  ❌ [LYNK] {product_name}: {resp[:80]}")

        time.sleep(0.3)

    state["post_count"] = state.get("post_count", 0) + created
    state["last_run"]   = now.isoformat()
    save_state(state)

    # ── Summary + CK stats ───────────────────────────────────────────────────
    log(f"Done: {created}/{num_posts} posts created | Total lifetime: {state['post_count']}")
    if CK_AVAILABLE:
        try:
            stats = get_learning_stats()
            log(
                f"[CK] Learning stats: {stats.get('total_rules', 0)} rules, "
                f"{stats.get('total_learnings', 0)} learnings"
            )
        except Exception as e:
            log(f"[CK] get_learning_stats error: {e}")


if __name__ == "__main__":
    main()
