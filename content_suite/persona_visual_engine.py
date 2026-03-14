#!/usr/bin/env python3
"""
Persona Visual Engine v3 — BerkahKarya Brand Identity
- Lato font (modern, social-media friendly)
- Noto Color Emoji (no more □□□)
- Geometric illustration background
- Rich layout: no empty space
"""
from __future__ import annotations
import json, os, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from datetime import datetime
from typing import Optional

WORKSPACE  = Path("/home/openclaw/.openclaw/workspace")
PERSONA_DB = WORKSPACE / "content_suite/personas/persona_database.json"
OUTPUT_DIR = WORKSPACE / "content_suite/output"
W, H = 1080, 1350

# ── Fonts ─────────────────────────────────────────────────────────────────────
LATO_BOLD   = "/usr/share/fonts/truetype/lato/Lato-Black.ttf"
LATO_REG    = "/usr/share/fonts/truetype/lato/Lato-Regular.ttf"
LATO_MED    = "/usr/share/fonts/truetype/lato/Lato-Medium.ttf"
EMOJI_FONT  = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

def fnt(size, bold=False):
    path = LATO_BOLD if bold else LATO_MED
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

# ── BerkahKarya palette ───────────────────────────────────────────────────────
BK_BLUE   = (37,  99, 235)
BK_NAVY   = (5,   44, 101)
BK_SLATE  = (30,  41,  59)
BK_WHITE  = (255,255,255)
BK_OFFWH  = (241,245,249)

PERSONA_THEME = {
    "trading-finance":       dict(pri=BK_BLUE,       acc=(226,183,20),  bg1=(5,25,60),    bg2=(15,10,35)),
    "health-wellness":       dict(pri=(22,163,74),   acc=(134,239,172), bg1=(3,40,20),    bg2=(5,20,12)),
    "product-review":        dict(pri=(234,88,12),   acc=(254,215,170), bg1=(45,15,5),    bg2=(25,8,2)),
    "digital-marketing":     dict(pri=BK_BLUE,       acc=(147,210,255), bg1=BK_NAVY,      bg2=BK_SLATE),
    "food-recipe":           dict(pri=(13,148,136),  acc=(153,246,228), bg1=(4,40,35),    bg2=(3,20,18)),
    "fashion-lifestyle":     dict(pri=(168,85,247),  acc=(233,213,255), bg1=(35,8,55),    bg2=(20,4,35)),
    "ai-content-creator":    dict(pri=(99,102,241),  acc=(199,210,254), bg1=BK_NAVY,      bg2=BK_SLATE),
    "tech-developer":        dict(pri=(6,182,212),   acc=(165,243,252), bg1=(4,30,40),    bg2=(3,15,22)),
    "entertainment-engagement": dict(pri=(220,38,38),acc=(252,165,165), bg1=(45,5,5),     bg2=(25,3,3)),
    "_default":              dict(pri=BK_BLUE,       acc=(147,210,255), bg1=BK_NAVY,      bg2=BK_SLATE),
}

DEFAULT_POINTS = {
    "trading-finance":          ["Risk management lebih penting dari profit besar","Jurnal trading adalah kunci konsistensi","Psikologi menentukan 80% hasil trading"],
    "health-wellness":          ["Tidur 7-8 jam tingkatkan performa 40%","Hidrasi cukup = energi stabil seharian","10 menit olahraga lebih baik dari nol"],
    "product-review":           ["Review jujur tanpa bias sponsor","Gue test sendiri sebelum rekomendasiin","Worth it atau skip? Ada jawabannya di sini"],
    "digital-marketing":        ["Konsistensi konten > viral sekali lalu hilang","Niche down = audience lebih engaged & loyal","AI tools bisa hemat 5-10 jam kerja/minggu"],
    "food-recipe":              ["Bahan simpel, hasil setara bintang lima","Siap dalam 30 menit atau kurang","Budget hemat, gizi tetap terjaga"],
    "fashion-lifestyle":        ["Style bukan soal budget, tapi taste","3 warna dasar sudah cukup untuk mix & match","Confidence adalah aksesori terbaik"],
    "ai-content-creator":       ["Prompt yang tepat = output 10x lebih baik","Otomasi konten = kerja sedikit, hasil banyak","Creator pakai AI tumbuh 3x lebih cepat"],
    "tech-developer":           ["Automation selesaikan 80% pekerjaan repetitif","Python script = hemat ribuan jam setahun","Build tools sendiri = keunggulan kompetitif"],
    "entertainment-engagement": ["Fakta ini bikin kamu terkejut banget","Tips simpel yang sering dilewatkan orang","Coba sekarang dan rasakan sendiri bedanya"],
}

class PersonaVisualEngine:
    def __init__(self):
        self.personas = {}
        if PERSONA_DB.exists():
            db = json.loads(PERSONA_DB.read_text())
            for p in db.get("personas", []):
                self.personas[p["persona_id"]] = p
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def _wrap(self, text, max_w, font, draw):
        words = text.split()
        lines, line = [], ""
        for w in words:
            test = (line + " " + w).strip()
            if draw.textbbox((0,0), test, font=font)[2] <= max_w:
                line = test
            else:
                if line: lines.append(line)
                line = w
        if line: lines.append(line)
        return lines

    def _gradient(self, draw, top, bot):
        for y in range(H):
            r = int(top[0]+(bot[0]-top[0])*y/H)
            g = int(top[1]+(bot[1]-top[1])*y/H)
            b = int(top[2]+(bot[2]-top[2])*y/H)
            draw.line([(0,y),(W,y)], fill=(r,g,b))

    def _draw_geo_bg(self, img, acc, seed=42):
        """Draw geometric illustration layer — circles, rings, dots, diagonal lines."""
        overlay = Image.new("RGBA", (W, H), (0,0,0,0))
        d = ImageDraw.Draw(overlay)
        rng = random.Random(seed)
        ar, ag, ab = acc

        # Large accent circles (blurred glow effect)
        for _ in range(4):
            cx = rng.randint(-100, W+100)
            cy = rng.randint(-100, H+100)
            r  = rng.randint(180, 380)
            alpha = rng.randint(12, 28)
            d.ellipse([(cx-r, cy-r),(cx+r, cy+r)], fill=(ar,ag,ab,alpha))

        # Medium rings
        for _ in range(6):
            cx = rng.randint(0, W)
            cy = rng.randint(0, H)
            r  = rng.randint(60, 160)
            alpha = rng.randint(15, 35)
            d.ellipse([(cx-r,cy-r),(cx+r,cy+r)], outline=(ar,ag,ab,alpha), width=2)

        # Small accent dots scattered
        for _ in range(30):
            cx = rng.randint(0, W)
            cy = rng.randint(0, H)
            r  = rng.randint(3, 10)
            alpha = rng.randint(30, 70)
            d.ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(ar,ag,ab,alpha))

        # Diagonal accent lines (top-right corner decoration)
        for i in range(8):
            offset = 60 + i*55
            alpha = max(8, 40 - i*5)
            d.line([(W-offset, 0),(W, offset)], fill=(ar,ag,ab,alpha), width=2)

        # Bottom-left corner lines
        for i in range(6):
            offset = 40 + i*50
            alpha = max(8, 35 - i*5)
            d.line([(0, H-offset),(offset, H)], fill=(ar,ag,ab,alpha), width=2)

        # Grid dot pattern (subtle, top area)
        for gx in range(0, W, 60):
            for gy in range(56, 300, 60):
                alpha = rng.randint(10, 25)
                d.ellipse([(gx-2,gy-2),(gx+2,gy+2)], fill=(ar,ag,ab,alpha))

        # Blur for softness
        blurred = overlay.filter(ImageFilter.GaussianBlur(radius=2))
        img.paste(blurred, (0,0), blurred)

    def _draw_text_with_emoji(self, draw, img, pos, text, font, fill, anchor="lt"):
        """Draw text — emoji rendered as colored bitmap via NotoColorEmoji."""
        # Split text into emoji and non-emoji segments
        import re
        emoji_pattern = re.compile(
            "[\U0001F300-\U0001F9FF\U0001FA00-\U0001FFFF"
            "\U00002600-\U000027BF\U0001F000-\U0001F02F"
            "\U0001F0A0-\U0001F0FF\U0001F100-\U0001F1FF"
            "\U0001F200-\U0001F2FF\U0001F900-\U0001F9FF]+", re.UNICODE
        )

        # Simple approach: replace emoji with text equivalent markers, draw separately
        # For PIL without emoji support: strip emoji and draw clean text
        # Then overdraw emoji using NotoColorEmoji at correct positions

        # First pass: draw full text with main font (emoji show as □)
        # Second pass: measure & draw emoji-only segments with emoji font
        x, y = pos
        segments = re.split(r'([\U0001F300-\U0001FFFF\U00002600-\U000027BF]+)', text)

        cursor_x = x
        for seg in segments:
            if not seg: continue
            if emoji_pattern.match(seg):
                # Draw with emoji font
                try:
                    efont = ImageFont.truetype(EMOJI_FONT, int(font.size * 0.85))
                    draw.text((cursor_x, y), seg, font=efont, fill=fill, embedded_color=True)
                    w = draw.textbbox((0,0), seg, font=efont)[2]
                except Exception:
                    # Fallback: skip emoji or use text substitute
                    w = 0
            else:
                draw.text((cursor_x, y), seg, font=font, fill=fill)
                w = draw.textbbox((0,0), seg, font=font)[2]
            cursor_x += w

    def generate_hook_frame(
        self,
        persona_id: str,
        headline: str,
        points: Optional[list[str]] = None,
        stat: Optional[str] = None,
        stat_label: Optional[str] = None,
        product_name: Optional[str] = None,
        output_filename: Optional[str] = None,
    ) -> Path:

        persona = self.personas.get(persona_id, {})
        theme   = PERSONA_THEME.get(persona_id, PERSONA_THEME["_default"])
        pri     = theme["pri"]
        acc     = theme["acc"]
        bg1     = theme["bg1"]
        bg2     = theme["bg2"]
        display = persona.get("display_name", "BerkahKarya")
        emoji_sig = persona.get("avatar", {}).get("emoji_signature", "🔥")
        pts     = points or DEFAULT_POINTS.get(persona_id, DEFAULT_POINTS["entertainment-engagement"])
        product = product_name or ((persona.get("primary_product") or "").replace("-"," ").title() or None)
        PAD = 52

        # ── Canvas ──────────────────────────────────────────────────────────
        img  = Image.new("RGB", (W,H), bg1)
        draw = ImageDraw.Draw(img, "RGBA")

        # Gradient BG
        self._gradient(draw, bg1, bg2)

        # Geometric illustration layer
        self._draw_geo_bg(img, acc, seed=hash(persona_id) % 9999)

        # Re-draw on top
        draw = ImageDraw.Draw(img, "RGBA")

        y = 0

        # ── Top brand bar ────────────────────────────────────────────────────
        BAR_H = 60
        draw.rectangle([(0,0),(W,BAR_H)], fill=(*pri,255))
        # BK logo text
        draw.text((PAD, 16), "BERKAH", font=fnt(26,bold=True), fill=BK_WHITE)
        draw.text((PAD+98, 16), "KARYA", font=fnt(26,bold=False), fill=(*acc,255))
        # Right: website
        draw.text((W-PAD, 16), "berkahkarya.org", font=fnt(22), fill=(*BK_WHITE,160), anchor="ra")
        # Thin accent underline
        draw.rectangle([(0,BAR_H-3),(W,BAR_H)], fill=(*acc,200))
        y = BAR_H + 30

        # ── Persona badge ────────────────────────────────────────────────────
        badge_font = fnt(28, bold=True)
        badge_txt  = display
        btw = draw.textbbox((0,0), badge_txt, font=badge_font)[2] + 56
        bth = 44
        # Pill background
        draw.rounded_rectangle([(PAD,y),(PAD+btw,y+bth)], radius=22,
                                fill=(*acc,200))
        # Emoji separately
        try:
            efont_sm = ImageFont.truetype(EMOJI_FONT, 28)
            draw.text((PAD+12, y+8), emoji_sig, font=efont_sm, embedded_color=True)
            ew = draw.textbbox((0,0), emoji_sig, font=efont_sm)[2]
        except:
            ew = 0
        # Text after emoji
        txt_col = (20,20,20) if (acc[0]+acc[1]+acc[2]) > 400 else BK_WHITE
        draw.text((PAD+14+ew, y+9), f"  {badge_txt}", font=badge_font, fill=txt_col)
        y += bth + 28

        # ── Headline ─────────────────────────────────────────────────────────
        hl_size = 82 if len(headline)<22 else 68 if len(headline)<35 else 56
        hl_font = fnt(hl_size, bold=True)
        hl_lines = self._wrap(headline, W-PAD*2, hl_font, draw)
        lh = int(hl_size * 1.18)
        for line in hl_lines[:4]:
            draw.text((PAD,y), line, font=hl_font, fill=BK_WHITE)
            y += lh
        y += 10

        # Accent divider
        draw.rectangle([(PAD,y),(PAD+90,y+4)], fill=(*acc,220))
        draw.rectangle([(PAD+98,y),(PAD+118,y+4)], fill=(*acc,100))
        y += 22

        # ── Stat block (optional, shows above cards) ──────────────────────────
        if stat:
            stat_font  = fnt(130, bold=True)
            label_font = fnt(36)
            draw.text((W//2, y), stat, font=stat_font, fill=(*acc,255), anchor="mt")
            if stat_label:
                y += 140
                draw.text((W//2, y), stat_label, font=label_font,
                          fill=(*BK_WHITE,180), anchor="mt")
            y += 30

        # ── 3 Point cards ─────────────────────────────────────────────────────
        card_h   = 96
        card_gap = 14
        ct_font  = fnt(34)
        ct_bold  = fnt(34, bold=True)

        for i, pt in enumerate(pts[:3]):
            cx1,cy1 = PAD, y
            cx2,cy2 = W-PAD, y+card_h

            # Card: semi-transparent dark overlay
            draw.rounded_rectangle([(cx1,cy1),(cx2,cy2)], radius=18,
                                   fill=(*BK_SLATE, 80))
            # Left accent bar
            draw.rounded_rectangle([(cx1,cy1),(cx1+5,cy2)], radius=3,
                                   fill=(*acc,255))
            # Number badge
            num_font = fnt(28, bold=True)
            num_x, num_y = cx1+22, cy1+34
            draw.ellipse([(num_x-16,num_y-16),(num_x+16,num_y+16)], fill=(*acc,200))
            draw.text((num_x,num_y), str(i+1), font=num_font,
                      fill=(20,20,20) if (acc[0]+acc[1]+acc[2])>400 else BK_WHITE,
                      anchor="mm")

            # Point text — strip leading emoji for clean render
            import re
            clean_pt = re.sub(r'^[\U0001F300-\U0001FFFF\U00002600-\U000027BF\s]+', '', pt).strip()
            pt_lines = self._wrap(clean_pt, W-PAD*2-80, ct_font, draw)
            for li, pl in enumerate(pt_lines[:2]):
                draw.text((cx1+52, cy1+20+li*38), pl, font=ct_font, fill=BK_WHITE)
            y += card_h + card_gap

        y += 12

        # ── CTA Card ──────────────────────────────────────────────────────────
        cta_y = H - 195
        cta_h = 130

        # BG card with gradient-ish
        draw.rounded_rectangle([(PAD,cta_y),(W-PAD,cta_y+cta_h)], radius=22,
                               fill=(*pri,230))
        draw.rounded_rectangle([(PAD,cta_y),(W-PAD,cta_y+cta_h)], radius=22,
                               outline=(*acc,180), width=2)

        cta_big  = fnt(40, bold=True)
        cta_sub  = fnt(32)

        if product:
            draw.text((W//2, cta_y+22), f"✅  {product}", font=cta_big,
                      fill=BK_WHITE, anchor="mt")
        else:
            draw.text((W//2, cta_y+22), "Kunjungi link di bio", font=cta_big,
                      fill=BK_WHITE, anchor="mt")
        draw.text((W//2, cta_y+72), "👆  berkahkarya.org", font=cta_sub,
                  fill=(*acc,255), anchor="mt")

        # ── Footer bar ────────────────────────────────────────────────────────
        draw.rectangle([(0,H-52),(W,H)], fill=(*pri,255))
        draw.text((PAD, H-36), "Digital Growth Agency", font=fnt(22),
                  fill=(*BK_WHITE,140))
        draw.text((W-PAD, H-36), "@berkahkarya", font=fnt(22),
                  fill=(*acc,200), anchor="ra")

        # ── Save ──────────────────────────────────────────────────────────────
        date_str = datetime.now().strftime("%Y%m%d")
        if not output_filename:
            safe = headline[:25].replace(" ","_").replace("/","-")
            output_filename = f"{persona_id}_{safe}_{date_str}.png"
        out_dir = OUTPUT_DIR / date_str
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / output_filename
        img.save(out_path, "PNG", optimize=True)
        return out_path

    def generate_batch(self, persona_id, content_items):
        return [self.generate_hook_frame(persona_id=persona_id, **item) for item in content_items]


if __name__ == "__main__":
    engine = PersonaVisualEngine()
    tests = [
        ("trading-finance",   "5 Kesalahan Fatal Trader Pemula",         None, "82%",  "trader rugi tahun pertama"),
        ("digital-marketing", "3 Strategi Konten yang Benar-Benar Work", None, None,   None),
        ("fashion-lifestyle", "Outfit Modis Budget Rp200K",              None, None,   None),
        ("health-wellness",   "Sehat Itu Murah Kalau Tahu Caranya",      None, None,   None),
        ("ai-content-creator","AI Tools Wajib Creator 2026",
         ["ChatGPT untuk riset dan brainstorming ide konten",
          "Canva AI untuk desain grafis dalam 2 menit",
          "Automation tools untuk scale konten 10x lebih cepat"], None, None),
    ]
    for pid, hl, pts, stat, sl in tests:
        p = engine.generate_hook_frame(persona_id=pid, headline=hl, points=pts, stat=stat, stat_label=sl)
        print(f"  ✅ {p.name}")
