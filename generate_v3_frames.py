#!/usr/bin/env python3
"""
Hook Frame Generator v3 — Properly Designed
Research-based: Indonesian high-converting social media creatives
Two variants: dark tech + clean white
Product-specific copy, no generic "CUAN!" hooks
"""

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path("/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/jendralbot_assets/hook_frames_v3")
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
    return re.sub(r'[^\x20-\x7E\u00C0-\u024F]', '', text).strip()

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


def dark_frame(product, hook, benefits, price, original, cta, proof, fname):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), "#0A0A0A")
    d = ImageDraw.Draw(img)
    A = "#00D4FF"

    # Grid
    for x in range(0, W, 60):
        d.line([(x,0),(x,H)], fill="#111111", width=1)
    for y in range(0, H, 60):
        d.line([(0,y),(W,y)], fill="#111111", width=1)

    # Top bar
    d.rectangle([0,0,W,6], fill=A)

    # Hook headline
    y = 60
    fh = gf("bold", 68)
    fh_s = gf("bold", 52)
    h_text = clean(hook).upper()
    lines = wrap(d, h_text, fh, W-100)
    if len(lines) > 2:
        lines = wrap(d, h_text, fh_s, W-100)
        fh = fh_s
    for line in lines[:3]:
        d.text((54,y), line, font=fh, fill="#FFFFFF")
        y += text_h(d, line, fh) + 14

    y += 18
    d.line([(54,y),(280,y)], fill=A, width=3)
    y += 22

    # Product name
    fp = gf("bold", 30)
    d.text((54,y), clean(product).upper(), font=fp, fill=A)
    y += text_h(d, product, fp) + 28

    # Benefits — all items, bigger font
    fb = gf("regular", 30)
    for b in benefits[:5]:
        bc = clean(b)
        if not bc:
            continue
        rr(d, [54,y+3,86,y+33], 5, A)
        d.text((61,y+5), "OK", font=gf("bold",18), fill="#000000")
        blines = wrap(d, bc, fb, W-120)
        for bl in blines[:2]:
            d.text((96,y), bl, font=fb, fill="#CCCCCC")
            y += text_h(d, bl, fb) + 6
        y += 6

    y += 12

    # Social proof
    if proof:
        sp = clean(proof)
        fsp = gf("regular", 23)
        spw = d.textbbox((0,0), sp, font=fsp)[2] + 40
        rr(d, [54,y,54+spw,y+38], 6, "#1A2A1A", "#00AA44", 1)
        d.text((74,y+8), sp, font=fsp, fill="#00CC55")
        y += 52

    y += 12

    # Stat boxes — directly after content
    stats = [("HEMAT", "75%"), ("AKSES", "SEUMUR HIDUP"), ("UPDATE", "GRATIS")]
    bw = (W - 108 - 36) // 3
    fsl = gf("regular", 18)
    fsv = gf("bold", 30)
    stat_h = 82
    box_y = min(y, H - 196 - stat_h - 20)  # don't overflow into price zone
    for i, (label, val) in enumerate(stats):
        bx = 54 + i * (bw + 18)
        rr(d, [bx, box_y, bx+bw, box_y+stat_h], 10, "#161616", A, 1)
        d.text((bx+12, box_y+8), label, font=fsl, fill="#888888")
        d.text((bx+12, box_y+34), val, font=fsv, fill=A)

    # Price area
    py = H - 196
    d.rectangle([0,py-16,W,H], fill="#111111")
    d.line([(0,py-16),(W,py-16)], fill=A, width=2)

    if original:
        fo = gf("regular", 26)
        orig_c = clean(original)
        d.text((54,py), orig_c, font=fo, fill="#666666")
        bb = d.textbbox((54,py), orig_c, font=fo)
        d.line([(54,(bb[1]+bb[3])//2),(bb[2],(bb[1]+bb[3])//2)], fill="#FF4444", width=2)

    fp2 = gf("bold", 70)
    d.text((54, py + (28 if original else 0)), clean(price), font=fp2, fill="#FFFFFF")

    # Discount badge
    rr(d, [W-175,py,W-18,py+54], 8, "#FF4444")
    fd = gf("bold", 24)
    d.text((W-163,py+13), "HEMAT 75%", font=fd, fill="#FFFFFF")

    # CTA
    cy = H-96
    rr(d, [54,cy,W-54,cy+68], 12, A)
    fc = gf("bold", 29)
    cta_c = clean(cta)
    cx = (W - d.textbbox((0,0),cta_c,font=fc)[2]) // 2
    d.text((cx,cy+18), cta_c, font=fc, fill="#000000")

    img.save(str(OUTPUT_DIR/fname), "PNG", quality=95)


ACCENT_MAP = {
    "jobmagnet": "#FF6B35",
    "ai_ad": "#7B2FBE",
    "food": "#FF6B35",
    "sellpix": "#0066FF",
    "ai_creative": "#00B4D8",
    "mesin": "#F77F00",
    "guru": "#2D6A4F",
    "belanja": "#E63946",
    "kelas": "#023E8A",
    "ai_content": "#6A0572",
}

def white_frame(product, hook, benefits, price, original, cta, proof, fname):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(img)

    A = "#1A1A2E"
    for k, v in ACCENT_MAP.items():
        if k in fname.lower():
            A = v
            break

    # Header band
    d.rectangle([0,0,W,190], fill=A)

    # Hook — white on dark header
    fh = gf("bold", 56)
    fh_s = gf("bold", 44)
    h_text = clean(hook)
    lines = wrap(d, h_text, fh, W-100)
    if len(lines) > 2:
        lines = wrap(d, h_text, fh_s, W-100)
        fh = fh_s
    y = 32
    for line in lines[:2]:
        d.text((54,y), line, font=fh, fill="#FFFFFF")
        y += text_h(d, line, fh) + 10

    # Product name
    y = 208
    fpn = gf("bold", 36)
    plines = wrap(d, clean(product), fpn, W-108)
    for line in plines[:2]:
        d.text((54,y), line, font=fpn, fill=A)
        y += text_h(d, line, fpn) + 8
    y += 14

    d.line([(54,y),(W-54,y)], fill="#EEEEEE", width=2)
    y += 22

    # Benefits — all items, bigger font
    fb = gf("regular", 30)
    for b in benefits[:5]:
        bc = clean(b)
        if not bc:
            continue
        rr(d, [54,y+3,86,y+33], 14, A)
        d.text((62,y+5), "OK", font=gf("bold",18), fill="#FFFFFF")
        blines = wrap(d, bc, fb, W-130)
        for bl in blines[:2]:
            d.text((100,y), bl, font=fb, fill="#1A1A1A")
            y += text_h(d, bl, fb) + 6
        y += 6

    y += 12

    # Social proof
    if proof:
        sp = clean(proof)
        fsp = gf("regular", 23)
        spw = d.textbbox((0,0), sp, font=fsp)[2] + 50
        rr(d, [54,y,54+spw,y+40], 8, "#F0FFF4", "#00AA44", 2)
        d.text((74,y+9), sp, font=fsp, fill="#006633")
        y += 54

    y += 12

    # Stat boxes — directly after content
    A2 = A
    stats = [("HEMAT", "75%"), ("AKSES", "SEUMUR HIDUP"), ("UPDATE", "GRATIS")]
    bw = (W - 108 - 36) // 3
    fsl = gf("regular", 18)
    fsv = gf("bold", 28)
    stat_h = 82
    box_y = min(y, H - 196 - stat_h - 20)
    for i, (label, val) in enumerate(stats):
        bx = 54 + i * (bw + 18)
        rr(d, [bx, box_y, bx+bw, box_y+stat_h], 10, "#F5F5F5", "#DDDDDD", 1)
        d.text((bx+12, box_y+8), label, font=fsl, fill="#AAAAAA")
        d.text((bx+12, box_y+32), val, font=fsv, fill=A2)

    # Price area
    py = H - 196
    d.rectangle([0,py-14,W,H], fill="#F8F8F8")
    d.line([(0,py-14),(W,py-14)], fill="#EEEEEE", width=2)

    if original:
        fo = gf("regular", 26)
        orig_c = clean(original)
        d.text((54,py), orig_c, font=fo, fill="#BBBBBB")
        bb = d.textbbox((54,py), orig_c, font=fo)
        d.line([(54,(bb[1]+bb[3])//2),(bb[2],(bb[1]+bb[3])//2)], fill="#FF4444", width=3)

    fp2 = gf("bold", 70)
    d.text((54, py + (30 if original else 0)), clean(price), font=fp2, fill=A)

    rr(d, [W-175,py+5,W-18,py+55], 8, "#FF4444")
    fd = gf("bold", 24)
    d.text((W-163,py+15), "HEMAT 75%", font=fd, fill="#FFFFFF")

    cy = H-96
    rr(d, [54,cy,W-54,cy+68], 12, A)
    fc = gf("bold", 29)
    cta_c = clean(cta)
    cx = (W - d.textbbox((0,0),cta_c,font=fc)[2]) // 2
    d.text((cx,cy+18), cta_c, font=fc, fill="#FFFFFF")

    img.save(str(OUTPUT_DIR/fname), "PNG", quality=95)


PRODUCTS = [
    {
        "id": "jobmagnet_ai",
        "name": "JobMagnet AI",
        "hook_d": "Kirim 50 lamaran, 0 respons?",
        "hook_w": "CV kamu diabaikan HRD? Ini kenapa.",
        "benefits": ["CV ATS-friendly yang lolos screening otomatis","Template cover letter 20+ industri","Strategi LinkedIn dapat tawaran kerja","Interview prep dengan AI mock session"],
        "proof": "Dipakai 500+ jobseeker Indonesia",
        "price": "Rp 75.000",
        "orig": "Rp 299.000",
        "cta": "AKSES SEKARANG - LINK DI BIO",
    },
    {
        "id": "ai_ad_engine",
        "name": "AI Creative & Ad Engine",
        "hook_d": "Iklan kamu buang uang tanpa hasil?",
        "hook_w": "Competitor pakai AI untuk iklan. Kamu?",
        "benefits": ["Generate 10 variasi iklan dalam 5 menit","Hook formula yang terbukti convert","Targeting strategy FB & TikTok Ads","A/B testing template untuk ROAS 3x"],
        "proof": "ROAS rata-rata 3.2x dari pengguna aktif",
        "price": "Rp 75.000",
        "orig": "Rp 499.000",
        "cta": "UPGRADE IKLANMU - CEK BIO",
    },
    {
        "id": "guru_pintar_ai",
        "name": "Guru Pintar AI",
        "hook_d": "Ngajar masih manual? Sudah ada AI-nya.",
        "hook_w": "1 tool ini ganti 4 platform edukasi.",
        "benefits": ["Buat modul dan kurikulum otomatis dengan AI","Sistem quiz dan penilaian auto-generated","Template kelas online siap pakai","Dashboard progress siswa real-time"],
        "proof": "200+ guru dan instruktur aktif pakai",
        "price": "Rp 75.000",
        "orig": "Rp 250.000",
        "cta": "COBA GRATIS - LINK DI BIO",
    },
    {
        "id": "food_menu_ai",
        "name": "Food Menu AI Studio",
        "hook_d": "Foto menu jelek = pelanggan kabur.",
        "hook_w": "Resto sebelah pakai AI untuk menu viral.",
        "benefits": ["Foto menu profesional tanpa kamera mahal","Desain menu digital untuk GoFood GrabFood","Deskripsi produk yang bikin ngiler","Template 50+ jenis kuliner Indonesia"],
        "proof": "500+ UMKM kuliner sudah pakai",
        "price": "Rp 75.000",
        "orig": "Rp 350.000",
        "cta": "UPGRADE MENUMU - CEK BIO",
    },
    {
        "id": "sellpix_ai",
        "name": "SellPix AI",
        "hook_d": "Foto produk jelek bunuh konversimu.",
        "hook_w": "Seller terbaik Shopee pakai ini.",
        "benefits": ["Background remover + studio foto virtual","Template listing Shopee Tokopedia yang convert","Bulk edit 100 foto dalam 10 menit","Optimasi gambar untuk TikTok Shop"],
        "proof": "1.000+ seller marketplace aktif pakai",
        "price": "Rp 75.000",
        "orig": "Rp 399.000",
        "cta": "FOTO PRODUK PRO - LINK DI BIO",
    },
    {
        "id": "mesin_cetak",
        "name": "Mesin Cetak Bisnis Kuliner",
        "hook_d": "Bisnis kuliner stagnan? Ini solusinya.",
        "hook_w": "Warung sebelah omzetnya 3x. Ini caranya.",
        "benefits": ["Sistem order dan manajemen stok otomatis","Strategi pricing untuk margin maksimal","Template menu viral untuk sosial media","Blueprint buka cabang dengan sistem franchise"],
        "proof": "Omzet naik rata-rata 40% dalam 30 hari",
        "price": "Rp 75.000",
        "orig": "Rp 300.000",
        "cta": "SCALE BISNIS KULINER - CEK BIO",
    },
    {
        "id": "ai_content_premium",
        "name": "AI Content Premium Pack 4K",
        "hook_d": "Konten kamu kalah dari yang pakai AI.",
        "hook_w": "Kreator top Indonesia sudah pakai ini.",
        "benefits": ["1000+ template konten siap posting","Viral hook library 200+ headline proven","Auto-generate caption Instagram TikTok YouTube","Batch schedule 30 hari konten dalam 1 jam"],
        "proof": "Kreator aktif dengan 100K+ followers pakai",
        "price": "Rp 75.000",
        "orig": "Rp 399.000",
        "cta": "CONTENT OTOMATIS - LINK DI BIO",
    },
    {
        "id": "kelas_affiliate",
        "name": "Kelas Affiliate Pesugihan TikTok",
        "hook_d": "TikTok bisa jadi mesin uang. Kamu tau caranya?",
        "hook_w": "Cara dapat Rp 10juta dari TikTok tanpa produk.",
        "benefits": ["Strategi affiliate TikTok Shop yang terbukti","Cara pilih produk high-commission untuk promote","Script video yang convert ke penjualan","Automasi konten affiliate 24 jam nonstop"],
        "proof": "Alumni berhasil dapat Rp 5-50juta per bulan",
        "price": "Rp 1.000.000",
        "orig": "Rp 2.000.000",
        "cta": "DAFTAR KELAS - LINK DI BIO",
    },
]

print("Generating v3 frames (dark + white)...")
total = 0
for p in PRODUCTS:
    dark_frame(p["name"], p["hook_d"], p["benefits"], p["price"], p["orig"], p["cta"], p["proof"], f"{p['id']}_dark.png")
    white_frame(p["name"], p["hook_w"], p["benefits"], p["price"], p["orig"], p["cta"], p["proof"], f"{p['id']}_white.png")
    total += 2
    print(f"  [{total//2}/{len(PRODUCTS)}] {p['name']}: dark + white")

print(f"\nDone: {total} frames in {OUTPUT_DIR}")
