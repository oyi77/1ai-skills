from PIL import Image, ImageDraw, ImageFont
import os

width = 1080
height = 1920
img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
except:
    font = ImageFont.load_default()

def draw_text_centered(text, y_pos, color):
    # Old PIL versions used textsize
    if hasattr(draw, 'textbbox'):
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    else:
        w, h = draw.textsize(text, font=font)
    
    x = (width - w) / 2
    # Shadow
    draw.text((x+4, y_pos+4), text, font=font, fill=(0,0,0,180))
    # Main text
    draw.text((x, y_pos), text, font=font, fill=color)

draw_text_centered("STOP PLANNING.", height/2 - 100, (255, 255, 255, 255))
draw_text_centered("START EXECUTING.", height/2 + 100, (255, 165, 0, 255))

img.save("/home/openclaw/.openclaw/workspace/output/test_results/overlay.png")
print("✅ Overlay image created")
