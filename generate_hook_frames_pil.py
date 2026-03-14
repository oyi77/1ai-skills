#!/usr/bin/env python3
"""
BerkahKarya Hook Frame Generator v2.0
Fixed: text wrapping by pixel width, emoji removal, modern design
"""

import json, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PRODUCTS_FILE = "/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/jendralbot_products.json"
OUTPUT_DIR = Path("/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/jendralbot_assets/hook_frames")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── CLEAN COLORS (no emoji in text) ──────────────────────────────────────────
PALETTES = {
    "energy":  {"bg": ["#FF416C", "#FF4B2B"], "accent": "#FFD700", "text": "#FFFFFF", "sub": "#FFE5E5"},
    "trust":   {"bg": ["#1A1A2E", "#16213E"], "accent": "#00D4FF", "text": "#FFFFFF", "sub": "#B0C4DE"},
    "growth":  {"bg": ["#11998E", "#38EF7D"], "accent": "#FFFFFF", "text": "#0D2B1E", "sub": "#1A5240"},
    "premium": {"bg": ["#0F0C29", "#302B63"], "accent": "#FFD700", "text": "#FFFFFF", "sub": "#C0A96A"},
}

HOOKS = ["GILA!", "PARAH!", "WOW!", "CEK INI!", "VIRAL!", "AUTO!", "CUAN!", "KAGET?"]

def load_products():
    with open(PRODUCTS_FILE) as f:
        return json.load(f)['products']

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def create_gradient(width, height, c1, c2):
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    r1,g1,b1 = hex_to_rgb(c1)
    r2,g2,b2 = hex_to_rgb(c2)
    for y in range(height):
        t = y / height
        r,g,b = int(r1*(1-t)+r2*t), int(g1*(1-t)+g2*t), int(b1*(1-t)+b2*t)
        draw.line([(0,y),(width,y)], fill=(r,g,b))
    return img

def strip_emoji(text):
    """Remove emoji characters that break DejaVu font rendering"""
    import re
    emoji_pattern = re.compile(
        "[\U00010000-\U0010ffff"
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\u2600-\u26FF\u2700-\u27BF"
        "\ufe0f\u20e3]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text).strip()

def wrap_text_by_width(draw, text, font, max_width):
    """Wrap text based on PIXEL width, not char count"""
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = ' '.join(current + [word])
        bbox = draw.textbbox((0,0), test, font=font)
        if bbox[2] > max_width and current:
            lines.append(' '.join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(' '.join(current))
    return lines

def add_shadow_text(draw, pos, text, font, color, shadow_offset=3, shadow_color=(0,0,0,100)):
    """Draw text with drop shadow"""
    x, y = pos
    draw.text((x+shadow_offset, y+shadow_offset), text, font=font, fill=(0,0,0,128))
    draw.text((x, y), text, font=font, fill=color)

def create_hook_frame(product, style="energy"):
    """Create professional hook frame"""
    name = strip_emoji(product['name'])
    price = product.get('price', 0)
    is_paid = product.get('is_paid', False)
    
    if is_paid and isinstance(price, (int, float)) and price > 0:
        price_text = f"IDR {price:,}"
        cta_text = "AMBIL SEKARANG"
    else:
        price_text = "GRATIS"
        cta_text = "AMBIL GRATIS"
    
    palette = PALETTES[style]
    W, H = 1080, 1080  # Square for Facebook/Instagram (not vertical to avoid cutoff)
    
    # Background
    bg = create_gradient(W, H, palette["bg"][0], palette["bg"][1])
    
    # Subtle texture overlay
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    for i in range(0, W, 60):
        for j in range(0, H, 60):
            if (i + j) % 120 == 0:
                ImageDraw.Draw(overlay).rectangle([i,j,i+30,j+30], fill=(255,255,255,8))
    bg.paste(Image.alpha_composite(Image.new('RGBA', (W,H), (0,0,0,0)), overlay), mask=overlay)
    
    draw = ImageDraw.Draw(bg)
    
    # Fonts
    FONT_PATH = "/usr/share/fonts/truetype/dejavu/"
    try:
        f_bold = lambda s: ImageFont.truetype(FONT_PATH + "DejaVuSans-Bold.ttf", s)
        f_reg  = lambda s: ImageFont.truetype(FONT_PATH + "DejaVuSans.ttf", s)
        hook_font    = f_bold(110)
        title_font   = f_bold(60)
        body_font    = f_reg(44)
        price_font   = f_bold(72)
        cta_font     = f_bold(48)
        small_font   = f_reg(30)
    except:
        hook_font = title_font = body_font = price_font = cta_font = small_font = ImageFont.load_default()
    
    accent = palette["accent"]
    txt    = palette["text"]
    sub    = palette["sub"]
    
    margin = 60
    max_text_w = W - 2*margin
    y = 80
    
    # ── HOOK word (top accent) ─────────────────────────────────────────────
    hook = random.choice(HOOKS)
    hook_bbox = draw.textbbox((0,0), hook, font=hook_font)
    hook_w = hook_bbox[2] - hook_bbox[0]
    hx = (W - hook_w) // 2
    # Accent background pill
    pad = 20
    draw.rounded_rectangle([hx-pad, y-pad//2, hx+hook_w+pad, y+hook_bbox[3]+pad//2], 
                            radius=16, fill=accent)
    draw.text((hx, y), hook, font=hook_font, fill=palette["bg"][0])
    y += hook_bbox[3] + 60
    
    # ── Divider line ───────────────────────────────────────────────────────
    draw.line([(margin, y), (W-margin, y)], fill=accent, width=3)
    y += 30
    
    # ── Product name (wrapped by pixel width) ─────────────────────────────
    name_lines = wrap_text_by_width(draw, name, title_font, max_text_w)
    for line in name_lines[:3]:  # max 3 lines
        bbox = draw.textbbox((0,0), line, font=title_font)
        lw = bbox[2] - bbox[0]
        lx = (W - lw) // 2
        add_shadow_text(draw, (lx, y), line, title_font, txt)
        y += bbox[3] - bbox[1] + 12
    y += 30
    
    # ── Feature bullets (clean text, no emoji) ─────────────────────────────
    features = [
        "Hemat waktu & tenaga",
        "Hasil lebih profesional",
        "Cocok untuk pemula & pro",
    ]
    for feat in features:
        bullet = f"+ {feat}"
        bbox = draw.textbbox((0,0), bullet, font=body_font)
        bw = bbox[2] - bbox[0]
        bx = (W - bw) // 2
        draw.text((bx, y), bullet, font=body_font, fill=sub)
        y += bbox[3] - bbox[1] + 8
    y += 40
    
    # ── Divider ────────────────────────────────────────────────────────────
    draw.line([(margin, y), (W-margin, y)], fill=accent, width=2)
    y += 30
    
    # ── Price ──────────────────────────────────────────────────────────────
    price_bbox = draw.textbbox((0,0), price_text, font=price_font)
    pw = price_bbox[2] - price_bbox[0]
    px = (W - pw) // 2
    draw.text((px, y), price_text, font=price_font, fill=accent)
    y += price_bbox[3] - price_bbox[1] + 20
    
    # ── CTA Button ─────────────────────────────────────────────────────────
    cta_bbox = draw.textbbox((0,0), cta_text, font=cta_font)
    cta_w = cta_bbox[2] - cta_bbox[0]
    cta_h = cta_bbox[3] - cta_bbox[1]
    btn_w = min(cta_w + 80, max_text_w)
    btn_h = cta_h + 30
    btn_x = (W - btn_w) // 2
    btn_y = y
    draw.rounded_rectangle([btn_x, btn_y, btn_x+btn_w, btn_y+btn_h], 
                            radius=20, fill=accent)
    ctx = (W - cta_w) // 2
    draw.text((ctx, btn_y + 15), cta_text, font=cta_font, fill=palette["bg"][0])
    y = btn_y + btn_h + 30
    
    # ── Bottom: "Link di bio" ──────────────────────────────────────────────
    footer = "Cek link di bio / caption"
    fbbox = draw.textbbox((0,0), footer, font=small_font)
    fw = fbbox[2] - fbbox[0]
    draw.text(((W-fw)//2, H-60), footer, font=small_font, fill=sub)
    
    return bg


def generate_all_frames(products):
    styles = list(PALETTES.keys())
    results = []
    for i, product in enumerate(products):
        pid = product['id']
        style = styles[i % len(styles)]
        img = create_hook_frame(product, style)
        out = OUTPUT_DIR / f"{pid}_{style}.png"
        img.save(str(out), quality=95)
        results.append({"product_id": pid, "path": str(out), "style": style})
        print(f"  ✅ {pid} [{style}] → {out.name}")
    return results


if __name__ == "__main__":
    products = load_products()
    print(f"Generating frames for {len(products)} products...")
    results = generate_all_frames(products)
    print(f"\nDone: {len(results)} frames in {OUTPUT_DIR}")
