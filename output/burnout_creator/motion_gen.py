#!/usr/bin/env python3
"""Generate motion graphic scenes using Pillow + FFmpeg"""

import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap

FFMPEG = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"
OUT = "/home/openclaw/.openclaw/workspace/output/burnout_creator"
os.makedirs(f"{OUT}/clips", exist_ok=True)
os.makedirs(f"{OUT}/frames", exist_ok=True)

W, H = 1080, 1920

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_text_centered(draw, text, y, font, color=(255,255,255), shadow=True):
    """Draw text centered horizontally"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    if shadow:
        # Shadow
        draw.text((x+4, y+4), text, font=font, fill=(0,0,0,160))
    draw.text((x, y), text, font=font, fill=color)

def create_scene3(duration=7):
    """Masalahnya: SISTEM. - kinetic typography"""
    print("  [Scene 3] Creating motion graphic...")
    frames_dir = f"{OUT}/frames/scene3"
    os.makedirs(frames_dir, exist_ok=True)

    fps = 30
    total_frames = duration * fps

    font_sub  = load_font(FONT_BOLD, 80)
    font_main = load_font(FONT_BOLD, 160)

    for i in range(total_frames):
        t = i / fps
        img = Image.new("RGB", (W, H), (8, 8, 8))
        draw = ImageDraw.Draw(img)

        # Subtle vignette effect
        for r in range(min(W, H)//2, 0, -20):
            alpha = int(180 * (1 - r/(min(W,H)/2)))
            draw.ellipse([(W//2-r, H//2-r), (W//2+r, H//2+r)],
                         outline=(20,20,20), width=2)

        # "Masalahnya:" fades in at t=1
        alpha1 = max(0.0, min(1.0, (t - 1.0) / 1.0))
        if alpha1 > 0:
            color1 = (int(255*alpha1), int(255*alpha1), int(255*alpha1))
            draw_text_centered(draw, "Masalahnya:", H//2 - 200, font_sub, color1)

        # "SISTEM." fades in at t=2.5, golden color
        alpha2 = max(0.0, min(1.0, (t - 2.5) / 1.0))
        if alpha2 > 0:
            color2 = (int(255*alpha2), int(215*alpha2), 0)
            draw_text_centered(draw, "SISTEM.", H//2 - 20, font_main, color2, shadow=True)

        # Save frame
        frame_path = f"{frames_dir}/frame_{i:05d}.jpg"
        img.save(frame_path, quality=92)

    # Convert frames to video
    out_path = f"{OUT}/clips/scene_3_video.mp4"
    cmd = [
        FFMPEG, "-y",
        "-framerate", "30",
        "-i", f"{frames_dir}/frame_%05d.jpg",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-pix_fmt", "yuv420p",
        out_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"  [Scene 3] ✅ {out_path}")
    return out_path


def create_scene4(duration=10):
    """AI Workflow screen mockup"""
    print("  [Scene 4] Creating screen mockup...")
    frames_dir = f"{OUT}/frames/scene4"
    os.makedirs(frames_dir, exist_ok=True)

    fps = 30
    total_frames = duration * fps

    font_title = load_font(FONT_BOLD, 64)
    font_item  = load_font(FONT_REG, 54)
    font_tag   = load_font(FONT_BOLD, 70)

    items = [
        ("✂  Auto cut silence", 1.5, (255,255,255)),
        ("📝  Auto subtitle", 3.5, (255,255,255)),
        ("🤖  Script struktur", 5.5, (255,255,255)),
    ]

    for i in range(total_frames):
        t = i / fps
        img = Image.new("RGB", (W, H), (16, 16, 22))
        draw = ImageDraw.Draw(img)

        # Top bar / header bg
        draw.rectangle([(0, 150), (W, 300)], fill=(25, 25, 40))

        # Header text
        alpha_h = max(0.0, min(1.0, (t - 0.3) / 0.8))
        if alpha_h > 0:
            draw_text_centered(draw, "AI Workflow", 195,
                               font_title, (int(79*alpha_h), int(195*alpha_h), int(247*alpha_h)))

        # Items
        for idx, (text, start, color) in enumerate(items):
            alpha = max(0.0, min(1.0, (t - start) / 0.8))
            if alpha > 0:
                y = 480 + idx * 170
                # Card background
                card_alpha = int(60 * alpha)
                draw.rectangle([(80, y-20), (W-80, y+80)],
                               fill=(40, 40, 60), outline=(60, 60, 100), width=2)
                c = (int(color[0]*alpha), int(color[1]*alpha), int(color[2]*alpha))
                draw.text((130, y+8), text, font=font_item, fill=c)

        # Bottom success tag
        alpha_tag = max(0.0, min(1.0, (t - 7.5) / 0.8))
        if alpha_tag > 0:
            c_tag = (int(129*alpha_tag), int(199*alpha_tag), int(132*alpha_tag))
            draw_text_centered(draw, "Upload lagi ✅", H - 380, font_tag, c_tag)

        frame_path = f"{frames_dir}/frame_{i:05d}.jpg"
        img.save(frame_path, quality=90)

    out_path = f"{OUT}/clips/scene_4_video.mp4"
    cmd = [
        FFMPEG, "-y",
        "-framerate", "30",
        "-i", f"{frames_dir}/frame_%05d.jpg",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-pix_fmt", "yuv420p",
        out_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"  [Scene 4] ✅ {out_path}")
    return out_path


def create_scene6(duration=6):
    """End card: clean minimal CTA"""
    print("  [Scene 6] Creating end card...")
    frames_dir = f"{OUT}/frames/scene6"
    os.makedirs(frames_dir, exist_ok=True)

    fps = 30
    total_frames = duration * fps

    font_line1 = load_font(FONT_REG, 72)
    font_cta   = load_font(FONT_BOLD, 100)

    for i in range(total_frames):
        t = i / fps
        img = Image.new("RGB", (W, H), (10, 10, 10))
        draw = ImageDraw.Draw(img)

        # Subtle horizontal divider
        if t > 1.5:
            div_alpha = min(1.0, (t - 1.5) / 0.5)
            div_color = (int(80*div_alpha), int(80*div_alpha), int(80*div_alpha))
            draw.rectangle([(200, H//2 - 40), (W-200, H//2 - 36)], fill=div_color)

        # "Mau workflow" line 1
        a1 = max(0.0, min(1.0, (t - 0.5) / 0.7))
        if a1 > 0:
            c1 = (int(255*a1), int(255*a1), int(255*a1))
            draw_text_centered(draw, "Mau workflow", H//2 - 250, font_line1, c1)

        # "+ toolsnya?" line 2
        a2 = max(0.0, min(1.0, (t - 0.9) / 0.7))
        if a2 > 0:
            c2 = (int(255*a2), int(255*a2), int(255*a2))
            draw_text_centered(draw, "+ toolsnya?", H//2 - 130, font_line1, c2)

        # "→ Cek Bio" golden CTA
        a3 = max(0.0, min(1.0, (t - 2.0) / 0.8))
        if a3 > 0:
            c3 = (int(255*a3), int(215*a3), 0)
            draw_text_centered(draw, "→ Cek Bio", H//2 + 80, font_cta, c3)

        frame_path = f"{frames_dir}/frame_{i:05d}.jpg"
        img.save(frame_path, quality=92)

    out_path = f"{OUT}/clips/scene_6_video.mp4"
    cmd = [
        FFMPEG, "-y",
        "-framerate", "30",
        "-i", f"{frames_dir}/frame_%05d.jpg",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-pix_fmt", "yuv420p",
        out_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"  [Scene 6] ✅ {out_path}")
    return out_path


if __name__ == "__main__":
    print("✏️  Generating motion graphics with Pillow...")
    create_scene3(7)
    create_scene4(10)
    create_scene6(6)
    print("✅ All motion graphics done!")
