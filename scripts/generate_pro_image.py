#!/usr/bin/env python3
"""
Generate Professional Hook Image - High Quality
Using Python PIL with better design principles
"""

from PIL import Image, ImageDraw, ImageFont
import os

from pathlib import Path
workspace = Path.home() / ".openclaw" / "workspace"

# Create image with better specifications
width = 1080
height = 1920

# Better color scheme - Professional dark gradient
background_top = (30, 30, 35)    # Dark gray-blue
background_bottom = (15, 15, 18)  # Almost black
accent_color = (255, 107, 107)   # Coral-red (#FF6B6B) - More professional
text_white = (255, 255, 255)
text_gray = (220, 220, 220)

# Create gradient background
img = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(img)

# Simple gradient fill
for y in range(height):
    r = int(background_top[0] + (background_bottom[0] - background_top[0]) * y / height)
    g = int(background_top[1] + (background_bottom[1] - background_top[1]) * y / height)
    b = int(background_top[2] + (background_bottom[2] - background_top[2]) * y / height)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# Try to load professional fonts
font_large = None
font_medium = None
font_small = None

font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
]

for path in font_paths:
    try:
        if os.path.exists(path):
            if "Bold" in path:
                font_large = ImageFont.truetype(path, 160)
                font_medium = ImageFont.truetype(path, 100)
            else:
                font_small = ImageFont.truetype(path, 60)
            break
    except:
        continue

# Fallback
if font_large is None:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Add subtle geometric background element
# Professional accent line
draw.line([(width//2, 150), (width//2, height-150)], fill=accent_color, width=3)

# Draw circle element at top
draw.ellipse([width//2 - 100, 120, width//2 + 100, 320], fill=accent_color)

# Main hook - Center aligned
hook_text = "STOP!"
hook_bbox = draw.textbbox((0, 0), hook_text, font=font_large, anchor="mm")
hook_width = hook_bbox[2] - hook_bbox[0]
hook_x = width // 2
hook_y = height * 0.25

# Draw text with shadow for readability
shadow_offset = 4
for i in range(3):
    offset = shadow_offset - i
    draw.text((hook_x - offset, hook_y - offset), hook_text, fill=(0, 0, 0, 100), font=font_large, anchor="mm")

draw.text((hook_x, hook_y), hook_text, fill=accent_color, font=font_large, anchor="mm")

# Subheading
sub_text = "KONTEN MANUAL MEMAKAN WAKTU"
sub_bbox = draw.textbbox((0, 0), sub_text, font=font_medium, anchor="mm")
sub_width = sub_bbox[2] - sub_bbox[0]
sub_x = width // 2
sub_y = hook_y + 250

# Text shadow
draw.text((sub_x - shadow_offset, sub_y - shadow_offset), sub_text, fill=(0, 0, 0, 80), font=font_medium, anchor="mm")
draw.text((sub_x, sub_y), sub_text, fill=text_white, font=font_medium, anchor="mm")

# Main emphasis
emphasis_text = "4 JAM / POST!"
emphasis_bbox = draw.textbbox((0, 0), emphasis_text, font=font_large, anchor="mm")
emphasis_width = emphasis_bbox[2] - emphasis_bbox[0]
emphasis_x = width // 2
emphasis_y = sub_y + 200

# Shadow
for i in range(3):
    offset = shadow_offset - i
    draw.text((emphasis_x - offset, emphasis_y - offset), emphasis_text, fill=(0, 0, 0, 100), font=font_large, anchor="mm")

draw.text((emphasis_x, emphasis_y), emphasis_text, fill=accent_color, font=font_large, anchor="mm")

# Bottom tagline
tagline_text = "GAK SCALE! MULAI DARI GRATIS"
tagline_bbox = draw.textbbox((0, 0), tagline_text, font=font_small, anchor="mm")
tagline_width = tagline_bbox[2] - tagline_bbox[0]
tagline_x = width // 2
tagline_y = height * 0.75

draw.text((tagline_x, tagline_y), tagline_text, fill=text_gray, font=font_small, anchor="mm")

# Add bottom accent line
draw.line([(width//2 - 150, tagline_y + 80), (width//2 + 150, tagline_y + 80)], fill=accent_color, width=2)

# Add water ripple effect (subtle)
ripple_y = int(height * 0.6)
for i in range(3):
    ripple_width = 200 + i * 100
    ripple_alpha = 30 - i * 10
    ripple_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ripple_draw = ImageDraw.Draw(ripple_layer)
    ripple_draw.ellipse([
        width//2 - ripple_width//2, ripple_y - 50,
        width//2 + ripple_width//2, ripple_y + 50
    ], fill=(*accent_color, ripple_alpha))
    img = Image.alpha_composite(img.convert("RGBA"), ripple_layer)
    img = img.convert("RGB")

# Save image
output_path = workspace / "content" / "samples" / "hook_image_pro.png"
os.makedirs(output_path.parent, exist_ok=True)
img.save(output_path, quality=95)

print(f"✅ Professional hook image saved: {output_path}")
print(f"   Resolution: {width}x{height}")
print(f"   Style: Dark gradient, coral-red accents, professional typography")
print(f"   Elements: Center alignment, shadows, geometric accents, subtle effects")