#!/usr/bin/env python3
"""
Generate Sample Image for Hook: "STOP! Konten manual makan waktu 4 jam/post!"
Using Python PIL to create text overlay
"""

from PIL import Image, ImageDraw, ImageFont
import os

from pathlib import Path
workspace = Path.home() / ".openclaw" / "workspace"

# Create image
width = 1080
height = 1920
background_color = (0, 0, 0, 255)  # Black background

img = Image.new("RGBA", (width, height), background_color)
draw = ImageDraw.Draw(img)

# Try to load a font, use default if not available
try:
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
except:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Hook text (centered)
hook_text = "🔥 STOP!"
text_width, text_height = draw.textsize(hook_text, font=font_large) if hasattr(draw, 'textsize') else (600, 100)
x = (width - text_width) / 2
y = height * 0.2
draw.text((x, y), hook_text, fill=(255, 69, 0), font=font_large, anchor="mm")  # Orange-red

# Subheading
sub_text = "Konten manual makan waktu"
text_width2, text_height2 = draw.textsize(sub_text, font=font_medium) if hasattr(draw, 'textsize') else (800, 70)
x2 = (width - text_width2) / 2
y2 = y + 200
draw.text((x2, y2), sub_text, fill=(255, 255, 255), font=font_medium, anchor="mm")  # White

# Time
time_text = "4 JAM / POST!"
text_width3, text_height3 = draw.textsize(time_text, font=font_large) if hasattr(draw, 'textsize') else (600, 100)
x3 = (width - text_width3) / 2
y3 = y2 + 150
draw.text((x3, y3), time_text, fill=(255, 69, 0), font=font_large, anchor="mm")  # Orange-red

# Save image
output_path = workspace / "content" / "samples" / "hook_image.png"
os.makedirs(output_path.parent, exist_ok=True)
img.save(output_path)

print(f"✅ Image saved: {output_path}")
