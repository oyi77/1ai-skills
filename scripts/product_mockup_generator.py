#!/usr/bin/env python3
"""
Product Mockup Generator dengan Holink Overlay
Generates branded product images with affiliate link overlay
"""

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random
import math

# === CONFIG ===
OUTPUT_DIR = Path("affiliate_content/mockups")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Brand Colors (BerkahKarya palette)
COLORS = {
    'dark_navy': (26, 26, 46),      # #1A1A2E
    'deep_blue': (22, 33, 62),       # #16213E
    'accent_gold': (226, 183, 20),   # #E2B714
    'accent_blue': (0, 150, 255),    # #0096FF
    'accent_teal': (0, 200, 180),    # #00C8B4
    'accent_orange': (255, 136, 0),  # #FF8800
    'white': (255, 255, 255),
    'light_gray': (200, 200, 200),
}

# Category color mapping
CATEGORY_COLORS = {
    'electronics': ('accent_blue', (0, 100, 200)),
    'home': ('accent_teal', (0, 150, 130)),
    'kitchen': ('accent_orange', (200, 100, 0)),
    'fashion': ('accent_gold', (180, 140, 0)),
    'health': ('accent_teal', (0, 180, 150)),
    'default': ('accent_blue', (0, 100, 200)),
}

def get_fonts():
    """Load fonts with fallbacks"""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    font_regular = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    
    bold_font = None
    regular_font = None
    
    for path in font_paths:
        if Path(path).exists():
            bold_font = path
            break
    
    for path in font_regular:
        if Path(path).exists():
            regular_font = path
            break
    
    return bold_font or font_paths[0], regular_font or font_regular[0]

BOLD_FONT, REGULAR_FONT = get_fonts()

def draw_gradient_background(draw, width, height, color1, color2):
    """Draw vertical gradient"""
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def draw_geometric_elements(draw, width, height, accent_color, seed):
    """Draw decorative geometric elements"""
    random.seed(seed)
    
    # Circles
    for _ in range(5):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(20, 80)
        alpha_color = (*accent_color, 30)
        draw.ellipse([x-r, y-r, x+r, y+r], outline=(*accent_color, 60), width=2)
    
    # Dots pattern
    for _ in range(20):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(3, 8)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(*accent_color, 40))

def draw_text_with_shadow(draw, pos, text, font, fill, shadow_color=(0,0,0)):
    """Draw text with shadow effect"""
    x, y = pos
    # Shadow
    draw.text((x+2, y+2), text, font=font, fill=(*shadow_color, 100))
    # Main text
    draw.text(pos, text, font=font, fill=fill)

def generate_product_mockup(
    product_name: str,
    price: str = None,
    discount: str = None,
    category: str = "default",
    features: list = None,
    output_name: str = None,
):
    """
    Generate branded product mockup with Holink overlay
    
    Args:
        product_name: Product title
        price: Price string (e.g., "Rp 2.499.000")
        discount: Discount text (e.g., "DISKON 50%")
        category: Product category for color scheme
        features: List of feature bullet points
        output_name: Output filename (auto-generated if None)
    """
    
    # Image dimensions (1080x1350 for IG optimal)
    width, height = 1080, 1350
    
    # Get category colors
    accent_name, accent_dark = CATEGORY_COLORS.get(category, CATEGORY_COLORS['default'])
    accent_color = COLORS.get(accent_name, COLORS['accent_blue'])
    
    # Create image with alpha for geometric overlay
    img = Image.new('RGBA', (width, height), COLORS['dark_navy'])
    draw = ImageDraw.Draw(img)
    
    # Background gradient
    draw_gradient_background(draw, width, height, COLORS['dark_navy'], COLORS['deep_blue'])
    
    # Geometric decorations
    geo_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    geo_draw = ImageDraw.Draw(geo_layer)
    draw_geometric_elements(geo_draw, width, height, accent_color, hash(product_name))
    img = Image.alpha_composite(img, geo_layer)
    draw = ImageDraw.Draw(img)
    
    # === TOP BANNER: Holink URL ===
    banner_height = 80
    draw.rectangle([0, 0, width, banner_height], fill=accent_color)
    
    try:
        banner_font = ImageFont.truetype(BOLD_FONT, 36)
    except:
        banner_font = ImageFont.load_default()
    
    holink_text = "🔗 ho.link/racunshopeediskon"
    bbox = draw.textbbox((0, 0), holink_text, font=banner_font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, 20), holink_text, font=banner_font, fill=COLORS['dark_navy'])
    
    # === DISCOUNT BADGE (if provided) ===
    y_offset = banner_height + 40
    if discount:
        try:
            discount_font = ImageFont.truetype(BOLD_FONT, 48)
        except:
            discount_font = ImageFont.load_default()
        
        # Red badge
        badge_width = 350
        badge_height = 70
        badge_x = (width - badge_width) // 2
        draw.rounded_rectangle(
            [badge_x, y_offset, badge_x + badge_width, y_offset + badge_height],
            radius=15,
            fill=(220, 38, 38)  # Red
        )
        bbox = draw.textbbox((0, 0), discount, font=discount_font)
        text_width = bbox[2] - bbox[0]
        draw.text(
            ((width - text_width) // 2, y_offset + 10),
            discount,
            font=discount_font,
            fill=COLORS['white']
        )
        y_offset += badge_height + 40
    
    # === PRODUCT NAME ===
    try:
        title_font = ImageFont.truetype(BOLD_FONT, 56)
        title_font_small = ImageFont.truetype(BOLD_FONT, 44)
    except:
        title_font = title_font_small = ImageFont.load_default()
    
    # Word wrap product name
    words = product_name.split()
    lines = []
    current_line = ""
    max_chars = 18
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if len(test_line) <= max_chars:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    # Use smaller font if too many lines
    use_font = title_font if len(lines) <= 2 else title_font_small
    line_height = 70 if len(lines) <= 2 else 55
    
    for i, line in enumerate(lines[:3]):  # Max 3 lines
        bbox = draw.textbbox((0, 0), line, font=use_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw_text_with_shadow(
            draw,
            (x, y_offset + i * line_height),
            line,
            use_font,
            COLORS['white']
        )
    
    y_offset += len(lines[:3]) * line_height + 40
    
    # === PRICE ===
    if price:
        try:
            price_font = ImageFont.truetype(BOLD_FONT, 72)
        except:
            price_font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), price, font=price_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_offset), price, font=price_font, fill=accent_color)
        y_offset += 100
    
    # === FEATURE BULLETS ===
    if features:
        try:
            feature_font = ImageFont.truetype(REGULAR_FONT, 32)
        except:
            feature_font = ImageFont.load_default()
        
        y_offset += 20
        for i, feature in enumerate(features[:4]):  # Max 4 features
            text = f"✓ {feature}"
            bbox = draw.textbbox((0, 0), text, font=feature_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text(
                (x, y_offset + i * 50),
                text,
                font=feature_font,
                fill=COLORS['light_gray']
            )
        y_offset += len(features[:4]) * 50 + 30
    
    # === PRODUCT VISUAL PLACEHOLDER ===
    # Circular product highlight zone
    center_y = y_offset + 150
    if center_y < height - 250:
        circle_radius = 150
        circle_x = width // 2
        
        # Glow effect
        for r in range(circle_radius + 30, circle_radius, -5):
            alpha = int(30 * (1 - (r - circle_radius) / 30))
            draw.ellipse(
                [circle_x - r, center_y - r, circle_x + r, center_y + r],
                outline=(*accent_color, alpha),
                width=3
            )
        
        # Main circle
        draw.ellipse(
            [circle_x - circle_radius, center_y - circle_radius,
             circle_x + circle_radius, center_y + circle_radius],
            outline=accent_color,
            width=4
        )
        
        # Product icon placeholder
        try:
            icon_font = ImageFont.truetype(REGULAR_FONT, 100)
        except:
            icon_font = ImageFont.load_default()
        
        icon = "📦"
        bbox = draw.textbbox((0, 0), icon, font=icon_font)
        icon_width = bbox[2] - bbox[0]
        draw.text(
            ((width - icon_width) // 2, center_y - 50),
            icon,
            font=icon_font,
            fill=COLORS['white']
        )
    
    # === BOTTOM CTA BANNER ===
    cta_height = 120
    cta_y = height - cta_height
    
    # Gradient overlay at bottom
    for y in range(100):
        alpha = int(200 * (y / 100))
        draw.line([(0, cta_y - 100 + y), (width, cta_y - 100 + y)], 
                  fill=(COLORS['dark_navy'][0], COLORS['dark_navy'][1], COLORS['dark_navy'][2], alpha))
    
    draw.rectangle([0, cta_y, width, height], fill=accent_dark)
    
    try:
        cta_font = ImageFont.truetype(BOLD_FONT, 40)
        cta_small = ImageFont.truetype(REGULAR_FONT, 24)
    except:
        cta_font = cta_small = ImageFont.load_default()
    
    # CTA text
    cta_text = "KLIK LINK DI BIO 👆"
    bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    text_width = bbox[2] - bbox[0]
    draw.text(
        ((width - text_width) // 2, cta_y + 20),
        cta_text,
        font=cta_font,
        fill=COLORS['white']
    )
    
    # Holink reminder
    reminder = "ho.link/racunshopeediskon"
    bbox = draw.textbbox((0, 0), reminder, font=cta_small)
    text_width = bbox[2] - bbox[0]
    draw.text(
        ((width - text_width) // 2, cta_y + 75),
        reminder,
        font=cta_small,
        fill=COLORS['light_gray']
    )
    
    # === SAVE ===
    img = img.convert('RGB')
    
    if not output_name:
        safe_name = "".join(c if c.isalnum() else "_" for c in product_name[:30])
        output_name = f"{safe_name}.jpg"
    
    output_path = OUTPUT_DIR / output_name
    img.save(output_path, quality=95)
    print(f"✅ Generated: {output_path} ({output_path.stat().st_size // 1024}KB)")
    
    return output_path


def generate_from_holink_products():
    """Generate mockups for all Holink products"""
    
    # Load product data
    holink_path = Path("skills/shopee-affiliate-promo/data/holink_structured.json")
    if not holink_path.exists():
        print(f"❌ Product data not found: {holink_path}")
        return []
    
    with open(holink_path) as f:
        products = json.load(f)
    
    generated = []
    
    # Category detection keywords
    category_keywords = {
        'electronics': ['tv', 'smart', 'vacuum', 'kipas', 'blender', 'mesin', 'oven', 'speaker'],
        'home': ['rak', 'lemari', 'kursi', 'meja', 'tempat', 'storage'],
        'kitchen': ['panci', 'wajan', 'kompor', 'dapur', 'masak'],
        'health': ['air purifier', 'dehumidifier', 'health', 'kesehatan'],
        'fashion': ['sepatu', 'baju', 'tas', 'fashion'],
    }
    
    def detect_category(name):
        name_lower = name.lower()
        for cat, keywords in category_keywords.items():
            if any(kw in name_lower for kw in keywords):
                return cat
        return 'default'
    
    for i, product in enumerate(products[:20]):  # First 20 products
        name = product.get('name', f'Product {i+1}')
        url = product.get('url', '')
        
        # Extract price if in name
        price = None
        discount = None
        
        if 'Rp' in name:
            # Try to extract price
            import re
            price_match = re.search(r'Rp\s*[\d.,]+', name)
            if price_match:
                price = price_match.group()
        
        # Random discount for visual appeal
        if random.random() > 0.5:
            discount = f"DISKON {random.choice([30, 40, 50, 60])}%"
        
        category = detect_category(name)
        
        # Generate features based on category
        features_by_cat = {
            'electronics': ['Garansi Resmi', 'Hemat Listrik', 'Kualitas Premium'],
            'home': ['Material Kokoh', 'Desain Modern', 'Mudah Dipasang'],
            'kitchen': ['Food Grade', 'Anti Lengket', 'Tahan Panas'],
            'health': ['Bebas Kuman', 'Udara Bersih', 'Hemat Energi'],
            'default': ['Best Seller', 'Kualitas Terjamin', 'Gratis Ongkir'],
        }
        
        features = features_by_cat.get(category, features_by_cat['default'])
        
        output_name = f"mockup_{i+1:02d}_{category}.jpg"
        
        try:
            path = generate_product_mockup(
                product_name=name[:50],  # Truncate long names
                price=price,
                discount=discount,
                category=category,
                features=features,
                output_name=output_name,
            )
            generated.append(path)
        except Exception as e:
            print(f"❌ Failed: {name[:30]}... - {e}")
    
    return generated


if __name__ == "__main__":
    print("🎨 Generating Product Mockups with Holink Overlay...")
    print(f"📁 Output: {OUTPUT_DIR.absolute()}")
    print()
    
    generated = generate_from_holink_products()
    
    print()
    print(f"📊 Total generated: {len(generated)} mockups")
    print(f"📁 Location: {OUTPUT_DIR.absolute()}")
