"""
Module 7: ContentRepurposer — One piece → many platform formats.
NEW module: no equivalent in existing codebase.

Pure text transformation — no API, no LLM, works offline.
Hashtag pools are static (domain knowledge), avoiding unnecessary web calls.
"""

import re
import textwrap
import random
from typing import Dict, List, Optional

try:
    from .base import BaseModule, load_config
except ImportError:
    import os as _os, json as _json
    _CFG_PATH = _os.path.join(_os.path.dirname(__file__), "../config.json")
    def load_config(path=_CFG_PATH):
        with open(_os.path.abspath(path)) as f:
            return _json.load(f)
    class BaseModule:
        def __init__(self, config): self.config = config
        def platform_cfg(self, p): return self.config.get("platforms", {}).get(p, {})

# ── PLATFORM RULES ────────────────────────────────────────────────────────────
PLATFORM_RULES = {
    "tiktok":    {"max_cap": 2200, "max_tags": 5,  "cta": "Cek link di bio! 👆"},
    "instagram": {"max_cap": 2200, "max_tags": 15, "cta": "Link di bio ya! 🔗"},
    "facebook":  {"max_cap": 5000, "max_tags": 5,  "cta": "Klik link di komentar!"},
    "youtube":   {"max_cap": 5000, "max_tags": 3,  "cta": "Link lengkap di deskripsi!"},
    "x":         {"max_cap": 280,  "max_tags": 2,  "cta": "Link ↓"},
}

HASHTAG_POOL = {
    "digital-marketing": ["#digitalmarketing", "#kontenkreatif", "#socialmedia", "#contentcreator",
                          "#marketingtips", "#bisnisdigital", "#affiliatemarketing", "#makemoneyonline",
                          "#passiveincome", "#jualanonline", "#tipsbisnis", "#entrepreneur",
                          "#UMKM", "#onlinebusiness", "#growthhacking"],
    "ai-tools":          ["#AI", "#kecerdasanbuatan", "#AItools", "#teknologi", "#chatgpt",
                          "#automasi", "#produktivitas", "#aiindonesia", "#worksmarter", "#digitaltransformation"],
    "kuliner":           ["#kuliner", "#usahakuliner", "#foodbusiness", "#modalminim",
                          "#jualmakanan", "#kulinerIndonesia", "#foodpreneur", "#bisnis2025"],
}

CAPTION_OPENERS = [
    "🔥 ", "⚡ Perhatian! ", "💡 Tau gak? ", "✅ Pro tip: ", "👀 Rahasia: ",
    "📢 Breaking: ", "🎯 Penting! ", "💰 Cuan alert: ",
]


class ContentRepurposer(BaseModule):
    """Convert one caption/blog/text into multiple platform-ready formats."""

    def __init__(self, config: dict):
        super().__init__(config)

    # ── CAROUSEL ──────────────────────────────────────────────────────────────

    def text_to_carousel(self, text: str, num_slides: int = 5) -> List[Dict]:
        """Convert text to carousel slides [{slide, type, title, body, cta}]."""
        sentences = self._sentences(text)
        slides = []

        # Slide 1: hook
        hook = sentences[0] if sentences else text[:100]
        slides.append({"slide": 1, "type": "hook", "title": "👆 SWIPE →", "body": hook, "cta": ""})

        # Middle slides: distribute body content
        body_sents = sentences[1:]
        content_slots = num_slides - 2
        chunk = max(1, len(body_sents) // content_slots) if body_sents else 1
        for i in range(content_slots):
            part = body_sents[i * chunk: (i + 1) * chunk]
            slides.append({
                "slide": i + 2,
                "type":  "content",
                "title": f"#{i + 2}",
                "body":  " ".join(part)[:220] or f"Poin ke-{i + 2}",
                "cta":   "",
            })

        # Last slide: CTA
        slides.append({
            "slide": num_slides,
            "type":  "cta",
            "title": "🔥 TAKE ACTION",
            "body":  "Cek link di bio untuk info lengkap!",
            "cta":   "https://lynk.id/jendralbot",
        })
        return slides

    # ── SHORT FORM ────────────────────────────────────────────────────────────

    def long_to_shorts(self, text: str, max_length: int = 150) -> List[str]:
        """Extract punchy standalone sentences for short-form content."""
        shorts = []
        for s in self._sentences(text):
            s = s.strip()
            if 30 <= len(s) <= max_length:
                shorts.append(s)
            elif len(s) > max_length:
                t = textwrap.shorten(s, width=max_length, placeholder="...")
                if len(t) >= 30:
                    shorts.append(t)
        return shorts[:8]

    # ── THREAD ────────────────────────────────────────────────────────────────

    def caption_to_thread(self, caption: str) -> List[str]:
        """Split caption into numbered X/Twitter thread (≤280 chars each)."""
        tweets, current = [], ""
        for s in self._sentences(caption):
            candidate = (current + " " + s).strip() if current else s
            if len(candidate) <= 260:
                current = candidate
            else:
                if current:
                    tweets.append(current)
                current = s
        if current:
            tweets.append(current)

        total = len(tweets)
        result = []
        for i, t in enumerate(tweets, 1):
            prefix = f"{i}/{total} " if total > 1 else ""
            suffix = " 🧵" if i == 1 and total > 1 else (" ↑" if i == total and total > 1 else "")
            result.append(f"{prefix}{t}{suffix}")
        return result

    # ── BLOG → SOCIAL ─────────────────────────────────────────────────────────

    def blog_to_social(self, blog_text: str, platforms: Optional[List[str]] = None) -> Dict[str, str]:
        """Adapt blog post for each platform. Returns {platform: caption}."""
        targets = platforms or list(PLATFORM_RULES.keys())
        return {p: self.adapt_for_platform(blog_text, "blog", p) for p in targets}

    # ── QUOTES ────────────────────────────────────────────────────────────────

    def extract_quotes(self, text: str, num: int = 3) -> List[str]:
        """Pull most shareable standalone quotes."""
        def score(s: str) -> float:
            sl = s.lower()
            pts = 0.0
            if 40 <= len(s) <= 120: pts += 2.0
            if "!" in s or "?" in s: pts += 1.0
            for kw in ["rahasia", "tips", "terbukti", "gratis", "mudah", "cuan", "viral"]:
                if kw in sl: pts += 1.5
            for kw in ["banyak orang", "semua bisa", "kamu bisa"]:
                if kw in sl: pts += 1.0
            return pts
        ranked = sorted(self._sentences(text), key=score, reverse=True)
        return [s.strip() for s in ranked[:num] if s.strip()]

    # ── VARIATIONS ────────────────────────────────────────────────────────────

    def generate_variations(self, caption: str, num: int = 3) -> List[str]:
        """Generate caption variations via opener swaps — no LLM needed."""
        sentences = self._sentences(caption)
        if not sentences:
            return [caption]
        body = " ".join(sentences[1:]) if len(sentences) > 1 else ""
        openers = random.sample(CAPTION_OPENERS, min(num, len(CAPTION_OPENERS)))
        out = []
        for opener in openers:
            v = f"{opener}{sentences[0]}"
            if body:
                v += f"\n\n{body}"
            out.append(v.strip())
        return out[:num]

    # ── PLATFORM ADAPTER ──────────────────────────────────────────────────────

    def adapt_for_platform(self, content: str, source_platform: str, target_platform: str) -> str:
        """Reformat content for target platform: length + hashtags + CTA."""
        rules = PLATFORM_RULES.get(target_platform, PLATFORM_RULES["instagram"])
        max_body = max(80, rules["max_cap"] - 160)
        body = textwrap.shorten(content, width=max_body, placeholder="...")
        tags = (HASHTAG_POOL["digital-marketing"] + HASHTAG_POOL["ai-tools"])[:rules["max_tags"]]
        cta  = rules["cta"]

        if target_platform == "x":
            base = f"{body} {cta}"
            tag_str = " ".join(tags[:2])
            return (base + " " + tag_str)[:280]

        return f"{body}\n\n{cta}\n\n{' '.join(tags)}"

    # ── PRIVATE ───────────────────────────────────────────────────────────────

    @staticmethod
    def _sentences(text: str) -> List[str]:
        """Split text into sentences, handling Indonesian patterns."""
        return [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n{2,}', text.strip()) if s.strip()]


# ── STANDALONE TEST ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = load_config()
    cr  = ContentRepurposer(cfg)

    sample = (
        "Mau penghasilan tambahan tapi bingung mulai dari mana? "
        "Sekarang ada solusinya! Dengan AI tools yang tepat, kamu bisa bikin konten viral "
        "dalam 5 menit. Banyak orang sudah buktiin hasilnya. "
        "Cukup modal 49K, akses semua template dan panduan lengkapnya. "
        "Jangan tunda lagi — kesempatan tidak datang dua kali!"
    )

    print("=" * 55 + "\nCONTENT REPURPOSER — Test\n" + "=" * 55)

    slides = cr.text_to_carousel(sample, num_slides=4)
    print(f"\n📱 Carousel ({len(slides)} slides):")
    for s in slides:
        print(f"  [{s['slide']}] {s['type'].upper()}: {s['body'][:55]}...")

    shorts = cr.long_to_shorts(sample)
    print(f"\n⚡ Shorts ({len(shorts)}):")
    for s in shorts: print(f"  • {s}")

    thread = cr.caption_to_thread(sample)
    print(f"\n🧵 Thread ({len(thread)} tweets):")
    for t in thread: print(f"  [{len(t)}c] {t[:70]}")

    quotes = cr.extract_quotes(sample, num=2)
    print(f"\n💬 Quotes: {quotes}")

    variations = cr.generate_variations(sample, num=2)
    print(f"\n🔁 Variations:")
    for v in variations: print(f"  → {v[:75]}...")

    x_post = cr.adapt_for_platform(sample, "blog", "x")
    print(f"\n🐦 X ({len(x_post)}c): {x_post}")
