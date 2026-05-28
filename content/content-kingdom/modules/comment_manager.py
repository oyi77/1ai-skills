"""
Module 5: CommentManager — HIGHEST PRIORITY (196 clicks, 0 sales)
NEW module: no equivalent in existing codebase.

Goal: classify comments → reply fast → DM purchase-intent users → convert clicks to sales.
PostBridge API: GET /v1/comments (when available).
"""

import re
import json
import random
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    from .base import BaseModule, load_config
except ImportError:
    # Standalone / __main__ mode
    import os as _os
    _CFG_PATH = _os.path.join(_os.path.dirname(__file__), "../config.json")
    def load_config(path=_CFG_PATH):
        with open(_os.path.abspath(path)) as f:
            return json.load(f)
    class BaseModule:
        def __init__(self, config): self.config = config
        def platform_cfg(self, p): return self.config.get("platforms", {}).get(p, {})

# ── FAQ DATABASE ──────────────────────────────────────────────────────────────
FAQ_DB = [
    (r"berapa harga|harga(nya)?|biaya|cost|bayar berapa",
     "Harganya mulai FREE sampai 89K aja! 🔥 Cek: https://lynk.id/jendralbot"),
    (r"grat(is|isan)?|free|tanpa bayar|0 rupiah",
     "Ada yang GRATIS! Mesin Cetak Kuliner — ambil di: https://lynk.id/jendralbot/mesin-cetak-kuliner 🎁"),
    (r"cara beli|gimana beli|order|checkout",
     "Gampang: 1️⃣ Klik link di bio  2️⃣ Pilih produk  3️⃣ Checkout via LYNK ⚡ → https://lynk.id/jendralbot"),
    (r"garansi|refund|uang kembali|jaminan",
     "Ada garansi kepuasan! ✅ Kalau gak puas, hubungi kami — kita pastikan kamu happy 🤝"),
    (r"\bhp\b|handphone|android|iphone|mobile",
     "Bisa di HP, tablet, laptop — semua device! 📱💻 Langsung bisa dipake."),
]

PURCHASE_SIGNALS   = [r"mau beli", r"pengen beli", r"minat", r"tertarik", r"order dong",
                      r"beli dimana", r"\blink\b", r"dm dong", r"info dong", r"boleh tau", r"mau dong"]
NEGATIVE_SIGNALS   = [r"tipu", r"scam", r"bohong", r"gak worth", r"jelek", r"kecewa", r"zonk"]
SPAM_SIGNALS       = [r"follow back", r"f4f", r"l4l", r"cek ig saya", r"free followers", r"join group"]

REPLY_TEMPLATES = {
    "positive":        ["Makasih banyak! 🙏 {extra}", "Terima kasih, semangat terus! 🔥 {extra}"],
    "question":        ["{answer}\nCek linknya di bio ya! 👆", "{answer} — ada pertanyaan lain? DM aja! 💬"],
    "purchase_intent": ["Mantap! {prod} Grab di: {url} 🔥", "Gas! {prod} Klik sekarang: {url} ⚡"],
    "negative":        ["Makasih feedbacknya! 🙏 {concern} Boleh DM kalau mau diskusi lebih lanjut."],
}

PRODUCT_KW = {
    "kuliner": "mesin_cetak_kuliner", "masak": "mesin_cetak_kuliner",
    "guru": "guru_pintar_ai",         "belajar": "guru_pintar_ai",
    "konten": "ai_content_pro_seller","content": "ai_content_pro_seller",
    "foto": "sellpix_ai",             "desain": "sellpix_ai",
    "cashback": "belanja_duit_balik", "belanja": "belanja_duit_balik",
    "template": "starter_content_4k",
    "iklan": "ai_creative_ad_engineer","ads": "ai_creative_ad_engineer",
    "sosmed": "ai_social_media_manager",
}


class CommentManager(BaseModule):
    """Convert comment engagement into sales via fast, context-aware replies."""

    def __init__(self, config: dict):
        super().__init__(config)
        self.products = {p["id"]: p for p in config.get("products", [])}
        _logs = Path(config.get("paths", {}).get("logs_dir", "/tmp/ck_logs"))
        _logs.mkdir(parents=True, exist_ok=True)
        self._log_file = _logs / "comment_manager.jsonl"
        _pb = config.get("postbridge_api_key", "")
        self._pb_url = config.get("postbridge_base_url", "https://api.post-bridge.com/v1")
        self._headers = {"Authorization": f"Bearer {_pb}", "Content-Type": "application/json"}

    # ── PUBLIC ────────────────────────────────────────────────────────────────

    def monitor_comments(self, hours: int = 24) -> List[Dict]:
        """Fetch comments via PostBridge. Returns [] on API failure."""
        url = f"{self._pb_url}/comments?hours={hours}"
        req = urllib.request.Request(url, headers=self._headers)
        try:
            with urllib.request.urlopen(req, timeout=12) as r:
                data = json.loads(r.read())
                return data.get("data", data) if isinstance(data, dict) else data
        except Exception as e:
            print(f"[CommentManager] PostBridge unavailable: {e}")
            return []

    def classify_comment(self, text: str) -> str:
        """Returns: spam | purchase_intent | negative | question | positive"""
        t = text.lower()
        if any(re.search(p, t) for p in SPAM_SIGNALS):      return "spam"
        if any(re.search(p, t) for p in PURCHASE_SIGNALS):  return "purchase_intent"
        if any(re.search(p, t) for p in NEGATIVE_SIGNALS):  return "negative"
        if "?" in t or re.search(r"\b(apa|gimana|caranya|berapa|kapan|dimana)\b", t):
            return "question"
        return "positive"

    def generate_reply(self, comment: Dict, persona: str = "jendralbot_main",
                       product: Optional[str] = None) -> str:
        """Generate contextual reply. Returns '' for spam."""
        text = comment.get("text", "") if isinstance(comment, dict) else str(comment)
        sentiment = self.classify_comment(text)
        tmpls = REPLY_TEMPLATES.get(sentiment, [])
        if not tmpls:
            return ""

        tmpl = random.choice(tmpls)
        prod = self._pick_product(text, product)

        if sentiment == "question":
            ans = self.get_faq_response(text) or "Boleh DM untuk info lengkapnya ya!"
            return tmpl.format(answer=ans)
        if sentiment == "purchase_intent":
            return tmpl.format(
                prod=f"[{prod['name']} — {prod['price_label']}]" if prod else "[cek semua produk]",
                url=prod["url"] if prod else "https://lynk.id/jendralbot",
            )
        if sentiment == "negative":
            return tmpl.format(concern="Kami terus improve produknya!")
        return tmpl.format(extra="Semoga bermanfaat! 🌟")

    def dm_interested_users(self, comments: List[Dict]) -> List[Dict]:
        """Filter purchase-intent → prepare DM payloads. Does NOT send."""
        out = []
        for c in comments:
            if self.classify_comment(c.get("text", "")) != "purchase_intent":
                continue
            prod = self._pick_product(c.get("text", ""))
            out.append({
                "user_id":  c.get("user_id"),
                "username": c.get("username"),
                "original": c.get("text"),
                "dm": (f"Hei {c.get('username','kak')}! 👋 Info lengkap "
                       f"{prod['name'] if prod else 'produk kami'}: "
                       f"{prod['url'] if prod else 'https://lynk.id/jendralbot'} 🔥"),
                "product":  prod["id"] if prod else None,
            })
        print(f"[CommentManager] {len(out)} DM candidates")
        return out

    def get_faq_response(self, question: str) -> Optional[str]:
        q = question.lower()
        for pattern, answer in FAQ_DB:
            if re.search(pattern, q):
                return answer
        return None

    def get_engagement_stats(self) -> Dict:
        stats = {"total": 0, "replied": 0, "sentiment": {}, "purchase_intent_rate": 0.0}
        if not self._log_file.exists():
            return stats
        entries = []
        with open(self._log_file) as f:
            for line in f:
                try: entries.append(json.loads(line))
                except: pass
        stats["total"]   = len(entries)
        stats["replied"] = sum(1 for e in entries if e.get("reply"))
        for e in entries:
            s = e.get("sentiment", "unknown")
            stats["sentiment"][s] = stats["sentiment"].get(s, 0) + 1
        if stats["total"]:
            pi = stats["sentiment"].get("purchase_intent", 0)
            stats["purchase_intent_rate"] = round(pi / stats["total"] * 100, 1)
            stats["reply_rate"] = round(stats["replied"] / stats["total"] * 100, 1)
        return stats

    def log_comment(self, comment: Dict, reply: str, sentiment: str):
        entry = {"ts": datetime.now().isoformat(), "user": comment.get("username"),
                 "text": comment.get("text","")[:200], "sentiment": sentiment,
                 "reply": reply[:300] if reply else None}
        with open(self._log_file, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # ── PRIVATE ───────────────────────────────────────────────────────────────

    def _pick_product(self, text: str, override: Optional[str] = None) -> Optional[Dict]:
        if override and override in self.products:
            return self.products[override]
        t = text.lower()
        for kw, pid in PRODUCT_KW.items():
            if kw in t and pid in self.products:
                return self.products[pid]
        return self.products.get("mesin_cetak_kuliner")  # lowest barrier default


# ── STANDALONE TEST ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = load_config()
    cm = CommentManager(cfg)
    tests = [
        {"id":"1","user_id":"u1","username":"budi",  "text":"Pengen beli dong, link mana kak?"},
        {"id":"2","user_id":"u2","username":"sari",  "text":"Berapa harganya?"},
        {"id":"3","user_id":"u3","username":"andi",  "text":"Keren banget kontennya! 🔥"},
        {"id":"4","user_id":"u4","username":"spam",  "text":"f4f cek ig saya free followers"},
        {"id":"5","user_id":"u5","username":"dewi",  "text":"Bisa dipake di HP gak?"},
        {"id":"6","user_id":"u6","username":"rizky", "text":"Harga segini mahal, gak worth"},
    ]
    print("=" * 55 + "\nCOMMENT MANAGER — Test\n" + "=" * 55)
    for c in tests:
        s = cm.classify_comment(c["text"])
        r = cm.generate_reply(c)
        cm.log_comment(c, r, s)
        print(f"\n[{s.upper():16}] @{c['username']}: {c['text'][:45]}")
        print(f"  → {r[:90] or '(no reply)'}")
    dms = cm.dm_interested_users(tests)
    print(f"\n📬 DM candidates: {len(dms)}")
    print(f"📊 Stats: {cm.get_engagement_stats()}")
