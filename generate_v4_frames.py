#!/usr/bin/env python3
"""
Hook Frame Generator v4 — High Contrast, No Dead Space
Fixes from user feedback:
1. Text contrast: stat labels WHITE (not grey #888)
2. Checkmarks: ✓ real Unicode (not "OK" box)
3. Dead space: visual feature card fills bottom 40%
4. Design: more professional, bold hierarchy
"""

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path("/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/jendralbot_assets/hook_frames_v4")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONTS = {
    "bold": "/home/openclaw/.openclaw/workspace/fonts/Montserrat-ExtraBold.ttf",
    "regular": "/home/openclaw/.openclaw/workspace/fonts/Roboto-Regular.ttf",
    "bold_fb": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "regular_fb": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}

def gf(style="regular", size=36):
    try:
        path = FONTS["bold"] if style == "bold" else FONTS["regular"]
        return ImageFont.truetype(path, size)
    except:
        path = FONTS["bold_fb"] if style == "bold" else FONTS["regular_fb"]
        try:
            return ImageFont.truetype(path, size)
        except:
            return ImageFont.load_default()

def clean(text):
    # Remove emoji/non-latin BUT keep checkmark character
    out = re.sub(r'[^\x20-\x7Eu\u2713\u2714\u00C0-\u024F]', '', text)
    return out.strip()

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], []
    for w in words:
        test = " ".join(cur + [w])
        if draw.textbbox((0,0), test, font=font)[2] > max_w and cur:
            lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))
    return lines

def rr(draw, xy, r, fill, outline=None, ow=0):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=ow)

def text_h(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[3] - bb[1]


def draw_checkmark(draw, x, y, size, color):
    """Draw a real checkmark using lines."""
    # Check circle background
    rr(draw, [x, y, x+size, y+size], size//2, color)
    # Draw checkmark ✓ using lines
    s = size
    # left part of check
    draw.line([(x+s//5, y+s//2), (x+s*2//5, y+s*3//4)], fill="#000000" if color != "#000000" else "#FFFFFF", width=3)
    # right part of check
    draw.line([(x+s*2//5, y+s*3//4), (x+s*4//5, y+s//4)], fill="#000000" if color != "#000000" else "#FFFFFF", width=3)


def dark_frame(product, hook, benefits, price, original, cta, proof, features_extra, fname):
    """
    v4 Dark: 1080x1080, black bg
    Zones:
    - Top (0-60): color bar
    - Hook (60-240): big headline
    - Product name + divider (240-310)
    - Benefits (310-530): 4 items, real checkmarks
    - Social proof badge (530-590) if exists
    - FEATURE VISUAL (590-780): 3 feature boxes or product mockup zone
    - Stat row (780-870)
    - Price + CTA (870-1080)
    """
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), "#0D0D0D")
    d = ImageDraw.Draw(img)
    ACC = "#00D4FF"   # Cyan accent

    # Subtle grid
    for x in range(0, W, 72):
        d.line([(x,0),(x,H)], fill="#131313", width=1)
    for y in range(0, H, 72):
        d.line([(0,y),(W,y)], fill="#131313", width=1)

    # Top accent bar (5px)
    d.rectangle([0,0,W,5], fill=ACC)

    # --- HOOK HEADLINE ---
    y = 52
    fh = gf("bold", 72)
    fh_s = gf("bold", 56)
    h_text = clean(hook).upper()
    lines = wrap(d, h_text, fh, W-100)
    if len(lines) > 2:
        lines = wrap(d, h_text, fh_s, W-100)
        fh = fh_s
    for line in lines[:3]:
        d.text((54, y), line, font=fh, fill="#FFFFFF")
        y += text_h(d, line, fh) + 12
    y += 10

    # Accent underline
    d.line([(54, y), (260, y)], fill=ACC, width=3)
    y += 18

    # --- PRODUCT NAME ---
    fp = gf("bold", 28)
    d.text((54, y), clean(product).upper(), font=fp, fill=ACC)
    y += text_h(d, product, fp) + 22

    # --- BENEFITS with real checkmark ---
    fb = gf("regular", 28)
    for b in benefits[:4]:
        bc = clean(b)
        if not bc:
            continue
        # Circle checkmark
        draw_checkmark(d, 54, y+2, 30, ACC)
        blines = wrap(d, bc, fb, W-118)
        for i, bl in enumerate(blines[:2]):
            d.text((96, y + i*(text_h(d, bl, fb)+4)), bl, font=fb, fill="#FFFFFF")
        y += text_h(d, blines[0], fb) * len(blines[:2]) + 14
    y += 8

    # --- SOCIAL PROOF BADGE ---
    if proof:
        sp = clean(proof)
        fsp = gf("regular", 22)
        spw = d.textbbox((0,0), sp, font=fsp)[2] + 44
        rr(d, [54, y, 54+spw, y+36], 6, "#0D2B0D", "#00AA44", 1)
        d.text((74, y+7), sp, font=fsp, fill="#00EE66")
        y += 48
    y += 8

    # --- FEATURE CARDS (fill dead space) ---
    # 3 horizontal mini-cards showing key features
    card_y = max(y, 590)
    card_h = 80
    card_w = (W - 108 - 32) // 3
    for i, feat in enumerate(features_extra[:3]):
        cx = 54 + i * (card_w + 16)
        rr(d, [cx, card_y, cx+card_w, card_y+card_h], 12, "#161B22", ACC, 1)
        # Feature number/icon
        fn_f = gf("bold", 34)
        num = feat.get("num", str(i+1))
        d.text((cx+14, card_y+8), num, font=fn_f, fill=ACC)
        # Feature label
        fl_f = gf("regular", 20)
        fl_lines = wrap(d, feat.get("label",""), fl_f, card_w-16)
        for j, fl in enumerate(fl_lines[:2]):
            d.text((cx+14, card_y+46+j*22), fl, font=fl_f, fill="#CCCCCC")
    y = card_y + card_h + 16

    # --- STAT ROW ---
    # 3 stat boxes: high contrast labels
    stats = [("HEMAT", "75%"), ("AKSES", "SEUMUR\nHIDUP"), ("UPDATE", "GRATIS")]
    sw = (W - 108 - 32) // 3
    stat_y = max(y + 10, 790)
    fsl = gf("regular", 17)
    fsv = gf("bold", 26)
    for i, (lbl, val) in enumerate(stats):
        sx = 54 + i * (sw + 16)
        rr(d, [sx, stat_y, sx+sw, stat_y+72], 10, "#1A1A1A", ACC, 1)
        # HIGH CONTRAST label — WHITE not grey
        d.text((sx+12, stat_y+6), lbl, font=fsl, fill="#FFFFFF")  # WHITE
        # Value in accent color
        vlines = val.split("\n")
        for vi, vl in enumerate(vlines):
            d.text((sx+12, stat_y+28+vi*26), vl, font=fsv, fill=ACC)

    # --- PRICE ZONE ---
    price_y = H - 190
    d.rectangle([0, price_y-12, W, H], fill="#121212")
    d.line([(0, price_y-12), (W, price_y-12)], fill=ACC, width=2)

    # Strikethrough original price
    if original:
        fo = gf("regular", 24)
        oc = clean(original)
        d.text((54, price_y), oc, font=fo, fill="#666666")
        bb = d.textbbox((54, price_y), oc, font=fo)
        d.line([(54, (bb[1]+bb[3])//2), (bb[2], (bb[1]+bb[3])//2)], fill="#FF4444", width=2)

    # Main price (big + white)
    fp2 = gf("bold", 72)
    pr_y = price_y + (26 if original else 0)
    d.text((54, pr_y), clean(price), font=fp2, fill="#FFFFFF")

    # HEMAT badge
    rr(d, [W-174, price_y, W-18, price_y+52], 8, "#FF3B30")
    d.text((W-162, price_y+12), "HEMAT 75%", font=gf("bold",23), fill="#FFFFFF")

    # CTA button (full width, bright)
    cta_y = H - 92
    rr(d, [54, cta_y, W-54, cta_y+66], 12, ACC)
    fc = gf("bold", 28)
    ctac = clean(cta)
    cx = (W - d.textbbox((0,0), ctac, font=fc)[2]) // 2
    d.text((cx, cta_y+18), ctac, font=fc, fill="#000000")

    img.save(str(OUTPUT_DIR / fname), "PNG", quality=95)


def white_frame(product, hook, benefits, price, original, cta, proof, features_extra, fname):
    """v4 White: clean minimal, accent color per product"""
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), "#FAFAFA")
    d = ImageDraw.Draw(img)

    ACCENT_MAP = {
        "jobmagnet": "#E8501A",
        "ai_ad": "#6B21A8",
        "food": "#D97706",
        "sellpix": "#1D4ED8",
        "ai_creative": "#0369A1",
        "mesin": "#C2410C",
        "guru": "#166534",
        "belanja": "#DC2626",
        "kelas": "#1E3A8A",
        "ai_content": "#7C3AED",
    }
    A = "#1E293B"
    for k, v in ACCENT_MAP.items():
        if k in fname.lower():
            A = v
            break

    # Header band with gradient feel (solid)
    d.rectangle([0, 0, W, 200], fill=A)
    d.rectangle([0, 196, W, 204], fill="#FFFFFF")  # white separator

    # Hook inside header
    fh = gf("bold", 58)
    fh_s = gf("bold", 46)
    h_text = clean(hook)
    lines = wrap(d, h_text, fh, W - 100)
    if len(lines) > 2:
        lines = wrap(d, h_text, fh_s, W-100)
        fh = fh_s
    y = 30
    for line in lines[:2]:
        d.text((54, y), line, font=fh, fill="#FFFFFF")
        y += text_h(d, line, fh) + 8

    # Product name below header
    y = 224
    fpn = gf("bold", 34)
    plines = wrap(d, clean(product), fpn, W-108)
    for line in plines[:1]:
        d.text((54, y), line, font=fpn, fill=A)
        y += text_h(d, line, fpn) + 6
    y += 12

    d.line([(54, y), (W-54, y)], fill="#E2E8F0", width=2)
    y += 20

    # Benefits with real checkmarks
    fb = gf("regular", 28)
    for b in benefits[:4]:
        bc = clean(b)
        if not bc:
            continue
        draw_checkmark(d, 54, y+2, 30, A)
        blines = wrap(d, bc, fb, W-118)
        for i, bl in enumerate(blines[:2]):
            d.text((96, y + i*(text_h(d, bl, fb)+4)), bl, font=fb, fill="#1E293B")
        y += text_h(d, blines[0], fb) * len(blines[:2]) + 14
    y += 8

    # Social proof
    if proof:
        sp = clean(proof)
        fsp = gf("regular", 22)
        spw = d.textbbox((0,0), sp, font=fsp)[2] + 44
        rr(d, [54, y, 54+spw, y+36], 6, "#F0FFF4", "#16A34A", 2)
        d.text((74, y+7), sp, font=fsp, fill="#15803D")
        y += 48
    y += 8

    # Feature cards
    card_y = max(y, 590)
    card_h = 80
    card_w = (W - 108 - 32) // 3
    for i, feat in enumerate(features_extra[:3]):
        cx = 54 + i * (card_w + 16)
        rr(d, [cx, card_y, cx+card_w, card_y+card_h], 12, "#F1F5F9", "#CBD5E1", 1)
        fn_f = gf("bold", 32)
        num = feat.get("num", str(i+1))
        d.text((cx+14, card_y+8), num, font=fn_f, fill=A)
        fl_f = gf("regular", 20)
        fl_lines = wrap(d, feat.get("label",""), fl_f, card_w-16)
        for j, fl in enumerate(fl_lines[:2]):
            d.text((cx+14, card_y+46+j*22), fl, font=fl_f, fill="#475569")
    y = card_y + card_h + 16

    # Stat row — HIGH CONTRAST labels
    stats = [("HEMAT", "75%"), ("AKSES", "SEUMUR\nHIDUP"), ("UPDATE", "GRATIS")]
    sw = (W - 108 - 32) // 3
    stat_y = max(y + 10, 790)
    fsl = gf("regular", 17)
    fsv = gf("bold", 26)
    for i, (lbl, val) in enumerate(stats):
        sx = 54 + i * (sw + 16)
        rr(d, [sx, stat_y, sx+sw, stat_y+72], 10, "#F8FAFC", A, 1)
        # HIGH CONTRAST label — dark text on light bg
        d.text((sx+12, stat_y+6), lbl, font=fsl, fill="#475569")  # medium-dark grey
        vlines = val.split("\n")
        for vi, vl in enumerate(vlines):
            d.text((sx+12, stat_y+28+vi*26), vl, font=fsv, fill=A)

    # Price zone
    price_y = H - 190
    d.rectangle([0, price_y-12, W, H], fill="#F1F5F9")
    d.line([(0, price_y-12), (W, price_y-12)], fill=A, width=2)

    if original:
        fo = gf("regular", 24)
        oc = clean(original)
        d.text((54, price_y), oc, font=fo, fill="#94A3B8")
        bb = d.textbbox((54, price_y), oc, font=fo)
        d.line([(54, (bb[1]+bb[3])//2), (bb[2], (bb[1]+bb[3])//2)], fill="#EF4444", width=2)

    fp2 = gf("bold", 72)
    pr_y = price_y + (26 if original else 0)
    d.text((54, pr_y), clean(price), font=fp2, fill=A)

    rr(d, [W-174, price_y, W-18, price_y+52], 8, "#EF4444")
    d.text((W-162, price_y+12), "HEMAT 75%", font=gf("bold",23), fill="#FFFFFF")

    cta_y = H - 92
    rr(d, [54, cta_y, W-54, cta_y+66], 12, A)
    fc = gf("bold", 28)
    ctac = clean(cta)
    cx = (W - d.textbbox((0,0), ctac, font=fc)[2]) // 2
    d.text((cx, cta_y+18), ctac, font=fc, fill="#FFFFFF")

    img.save(str(OUTPUT_DIR / fname), "PNG", quality=95)


# ─── PRODUCT DATA ───────────────────────────────────────────────────────────

PRODUCTS = [
    {
        "id": "jobmagnet_ai",
        "name": "JobMagnet AI",
        "hook_dark": "CV kamu dilewati HRD dalam 6 detik.",
        "hook_white": "90% CV Ditolak Bukan Karena Kemampuan.",
        "benefits": [
            "ATS optimizer: CV lolos screening otomatis",
            "Template yang sudah terbukti dipakai 500+ pelamar",
            "Keyword booster per bidang & perusahaan",
            "Instant cover letter generator berbahasa Indonesia",
        ],
        "price": "Rp 75.000",
        "original": "Rp 299.000",
        "cta_dark": "OPTIMALKAN CV SEKARANG - LINK DI BIO",
        "cta_white": "DOWNLOAD TEMPLATE - LINK DI BIO",
        "proof": "500+ jobseeker sudah lolos interview",
        "features": [
            {"num": "ATS", "label": "Lolos\nAuto-Screening"},
            {"num": "3x", "label": "Lebih Banyak\nInterview"},
            {"num": "1h", "label": "Setup\nLangsung Pakai"},
        ],
    },
    {
        "id": "ai_ad_engine",
        "name": "AI Creative & Ad Engine",
        "hook_dark": "Iklan habis budget, tapi ROAS masih di bawah 2.",
        "hook_white": "Iklan Bagus Bukan Soal Budget — Soal Copy.",
        "benefits": [
            "AI copywriter: headline + body text yang convert",
            "Template iklan FB/IG/TikTok sudah proven",
            "A/B test variant generator (5 versi per produk)",
            "Riset kompetitor & winning ad analysis",
        ],
        "price": "Rp 75.000",
        "original": "Rp 499.000",
        "cta_dark": "TINGKATKAN ROAS SEKARANG - LINK DI BIO",
        "cta_white": "COBA GRATIS 7 HARI - LINK DI BIO",
        "proof": "ROAS rata-rata 3.2x dari pengguna aktif",
        "features": [
            {"num": "5x", "label": "Lebih Cepat\nBuat Iklan"},
            {"num": "AI", "label": "Copy yang\nSudah Terbukti"},
            {"num": "∞", "label": "Variasi A/B\nTanpa Batas"},
        ],
    },
    {
        "id": "guru_pintar_ai",
        "name": "Guru Pintar AI",
        "hook_dark": "Belajar 1 jam tapi tidak ada yang nyangkut.",
        "hook_white": "Cara Belajar yang Benar Bikin Kamu 10x Lebih Pintar.",
        "benefits": [
            "AI tutor personal 24/7 untuk semua mata pelajaran",
            "Rangkuman materi otomatis dari file apapun",
            "Latihan soal + penjelasan step-by-step",
            "Mode tanya-jawab interaktif seperti guru privat",
        ],
        "price": "Rp 75.000",
        "original": "Rp 250.000",
        "cta_dark": "BELAJAR LEBIH EFEKTIF - LINK DI BIO",
        "cta_white": "AKSES GURU AI - LINK DI BIO",
        "proof": "Dipakai 300+ pelajar & mahasiswa Indonesia",
        "features": [
            {"num": "24/7", "label": "Tutor\nSelalu Siap"},
            {"num": "∞", "label": "Materi\nSemua Pelajaran"},
            {"num": "AI", "label": "Penjelasan\nPersonal"},
        ],
    },
    {
        "id": "food_menu_ai",
        "name": "Food Menu AI Studio",
        "hook_dark": "Menu jelek bikin pelanggan order di tempat lain.",
        "hook_white": "Menu yang Bagus Bisa Naikkan Omzet 25%.",
        "benefits": [
            "Desain menu profesional dalam 10 menit",
            "500+ template untuk semua jenis restoran & cafe",
            "Photo enhancement: foto biasa jadi kelihatan premium",
            "Deskripsi menu AI yang bikin nafsu makan",
        ],
        "price": "Rp 75.000",
        "original": "Rp 350.000",
        "cta_dark": "UPGRADE MENU SEKARANG - LINK DI BIO",
        "cta_white": "BUAT MENU KEREN - LINK DI BIO",
        "proof": "200+ pemilik kuliner sudah pakai",
        "features": [
            {"num": "10'", "label": "Desain\nMenu Siap"},
            {"num": "500+", "label": "Template\nProfesional"},
            {"num": "+25%", "label": "Potensi\nNaik Omzet"},
        ],
    },
    {
        "id": "sellpix_ai",
        "name": "SellPix AI",
        "hook_dark": "Foto produk jelek bunuh konversimu.",
        "hook_white": "Foto Produk Pro Tanpa Kamera Mahal.",
        "benefits": [
            "Background remover + studio foto virtual AI",
            "Template listing Shopee/Tokopedia yang convert",
            "Bulk edit 100 foto dalam 10 menit",
            "Optimasi gambar khusus TikTok Shop & marketplace",
        ],
        "price": "Rp 75.000",
        "original": "Rp 399.000",
        "cta_dark": "FOTO PRODUK PRO - LINK DI BIO",
        "cta_white": "UPGRADE FOTO SEKARANG - LINK DI BIO",
        "proof": "1.000+ seller marketplace aktif pakai",
        "features": [
            {"num": "AI", "label": "Studio Foto\nVirtual"},
            {"num": "100x", "label": "Bulk Edit\n10 Menit"},
            {"num": "+30%", "label": "Konversi\nListing Naik"},
        ],
    },
    {
        "id": "mesin_cetak",
        "name": "Mesin Cetak Bisnis Kuliner",
        "hook_dark": "Bisnis kuliner ramai tapi profit tipis.",
        "hook_white": "Kuliner Laris Itu Bukan Cuma Soal Rasa.",
        "benefits": [
            "System operasional kuliner siap pakai (SOP + template)",
            "Menu engineering: harga yang maximize profit",
            "Marketing toolkit khusus bisnis F&B Indonesia",
            "Analisis biaya + HPP + break-even calculator",
        ],
        "price": "Rp 75.000",
        "original": "Rp 350.000",
        "cta_dark": "SCALE KULINER SEKARANG - LINK DI BIO",
        "cta_white": "DOWNLOAD TOOLKIT - LINK DI BIO",
        "proof": "150+ pemilik UMKM kuliner sudah scale",
        "features": [
            {"num": "SOP", "label": "Sistem\nOperasional"},
            {"num": "HPP", "label": "Kalkulator\nProfit"},
            {"num": "MKT", "label": "Marketing\nF&B Toolkit"},
        ],
    },
    {
        "id": "ai_content_premium",
        "name": "AI Content Premium Pack 4K",
        "hook_dark": "Posting setiap hari tapi follower tidak naik.",
        "hook_white": "Konten Viral Itu Ada Polanya — Ini Polanya.",
        "benefits": [
            "300+ template video TikTok/Reels siap edit",
            "Hook library 200+ pembuka konten yang stop-scroll",
            "Caption formula per niche + hashtag optimizer",
            "Jadwal posting & content calendar 90 hari",
        ],
        "price": "Rp 75.000",
        "original": "Rp 450.000",
        "cta_dark": "BIKIN KONTEN VIRAL - LINK DI BIO",
        "cta_white": "DOWNLOAD PACK KONTEN - LINK DI BIO",
        "proof": "Dipakai 400+ kreator & social media manager",
        "features": [
            {"num": "300+", "label": "Template\nVideo Viral"},
            {"num": "200+", "label": "Hook\nStop-Scroll"},
            {"num": "90H", "label": "Kalender\nKonten Siap"},
        ],
    },
    {
        "id": "kelas_affiliate",
        "name": "Kelas Affiliate Pesugihan TikTok",
        "hook_dark": "Upload 100 video tapi komisi nol.",
        "hook_white": "Sistem Affiliate yang Bikin Komisi Datang Otomatis.",
        "benefits": [
            "Blueprint sistem affiliate TikTok Shop yang convert",
            "Produk pilihan + analisis potensi komisi tertinggi",
            "Script video affiliate yang terbukti viral",
            "Mentoring + update strategi terbaru setiap bulan",
        ],
        "price": "Rp 1.000.000",
        "original": "Rp 2.000.000",
        "cta_dark": "DAFTAR KELAS SEKARANG - LINK DI BIO",
        "cta_white": "CEK CURRICULUM - LINK DI BIO",
        "proof": "Alumni sudah hasilkan Rp 10jt+ dari affiliate",
        "features": [
            {"num": "SYS", "label": "Blueprint\nAffiliate Proven"},
            {"num": "1:1", "label": "Mentoring\nPersonal"},
            {"num": "∞", "label": "Update\nStrategi Bulanan"},
        ],
    },
]


def main():
    print(f"Generating v4 frames (dark + white)...")
    for p in PRODUCTS:
        # Dark
        fname_d = f"{p['id']}_v4_dark.png"
        dark_frame(
            product=p["name"],
            hook=p["hook_dark"],
            benefits=p["benefits"],
            price=p["price"],
            original=p.get("original"),
            cta=p["cta_dark"],
            proof=p.get("proof"),
            features_extra=p.get("features", []),
            fname=fname_d,
        )
        # White
        fname_w = f"{p['id']}_v4_white.png"
        white_frame(
            product=p["name"],
            hook=p["hook_white"],
            benefits=p["benefits"],
            price=p["price"],
            original=p.get("original"),
            cta=p["cta_white"],
            proof=p.get("proof"),
            features_extra=p.get("features", []),
            fname=fname_w,
        )
        print(f"  [{p['id']}] dark + white")
    print(f"\nDone: 16 frames in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
