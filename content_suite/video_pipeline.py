#!/usr/bin/env python3
"""
Video Generation Pipeline — Full Fallback Chain
================================================
Order (best → most reliable):
  1. GeminiGenAI   — AI-generated video from text prompt (imagen 3 / veo)
  2. BytePlus       — Seedance i2v (image-to-video) or t2v (text-to-video)
  3. Remotion       — Programmatic animation (React-based, multi-slide)
  4. FFmpeg         — Ken Burns on multi-slide PNG sequence (always works)

Multi-slide concept:
  Slide 0: Hook/Headline (attention)
  Slide 1: Point 1 card (value)
  Slide 2: Point 2 card (value)
  Slide 3: Point 3 card (value)
  Slide 4: CTA / product close (conversion)
  
  Each slide = 3-4 sec → total 15-20 sec video

Usage:
  python3 video_pipeline.py --persona trading-finance --headline "5 Kesalahan Fatal Trader"
  python3 video_pipeline.py --batch
  python3 video_pipeline.py --method ffmpeg --persona fashion-lifestyle

Author: Vilona / BerkahKarya
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time, re
from pathlib import Path
from datetime import datetime
from typing import Optional

WORKSPACE  = Path("/home/openclaw/.openclaw/workspace")
CS_DIR     = WORKSPACE / "content_suite"
OUTPUT_DIR = CS_DIR / "output"
PERSONA_DB = CS_DIR / "personas/persona_database.json"

sys.path.insert(0, str(CS_DIR))

# ── Env ───────────────────────────────────────────────────────────────────────
BYTEPLUS_KEY = os.getenv("BYTEPLUS_API_KEY", "cac5cfc1-e30f-47bb-b8b8-e861ffda28ea")
GEMINI_KEY   = os.getenv("GEMINI_API_KEY", "")
BYTEPLUS_BASE= "https://ark.ap-southeast.bytepluses.com/api/v3"

BYTEPLUS_MODELS = {
    "i2v_lite": "seedance-1-0-lite-i2v-250428",
    "t2v_lite": "seedance-1-0-lite-t2v-250428",
    "pro":      "seedance-1-0-pro-250528",
}


# ═══════════════════════════════════════════════════════════════════════════════
# MULTI-SLIDE IMAGE GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

def generate_slides(persona_id: str, headline: str, points: list[str],
                    product: str = None, date_str: str = None) -> list[Path]:
    """
    Generate 5 slide images for video sequence.
    Returns list of PNG paths in order.
    """
    from persona_visual_engine import PersonaVisualEngine
    from PIL import Image, ImageDraw, ImageFont
    import math

    engine = PersonaVisualEngine()
    persona = engine.personas.get(persona_id, {})
    theme   = engine.PERSONA_THEME.get(persona_id, engine.PERSONA_THEME["_default"]) \
              if hasattr(engine, 'PERSONA_THEME') else {}

    date_str = date_str or datetime.now().strftime("%Y%m%d")
    slides_dir = OUTPUT_DIR / date_str / "slides" / persona_id
    slides_dir.mkdir(parents=True, exist_ok=True)

    slide_paths = []

    # Slide 0: Full hook frame (existing engine)
    s0 = engine.generate_hook_frame(
        persona_id=persona_id, headline=headline,
        points=points[:3], product_name=product,
        output_filename=f"slide_0_hook.png"
    )
    # Move to slides dir
    import shutil
    s0_dest = slides_dir / "slide_0_hook.png"
    shutil.copy(s0, s0_dest)
    slide_paths.append(s0_dest)

    # Slides 1-3: Individual point cards (close-up on each point)
    from persona_visual_engine import PERSONA_THEME, BK_WHITE, fnt
    W, H = 1080, 1920  # 9:16 for these slides

    theme_data = PERSONA_THEME.get(persona_id, PERSONA_THEME["_default"])
    pri = theme_data["pri"]
    acc = theme_data["acc"]
    bg1 = theme_data["bg1"]
    bg2 = theme_data["bg2"]

    for i, point in enumerate(points[:3], 1):
        img  = Image.new("RGB", (W, H), bg1)
        draw = ImageDraw.Draw(img, "RGBA")

        # Gradient
        for y in range(H):
            r = int(bg1[0]+(bg2[0]-bg1[0])*y/H)
            g = int(bg1[1]+(bg2[1]-bg1[1])*y/H)
            b = int(bg1[2]+(bg2[2]-bg1[2])*y/H)
            draw.line([(0,y),(W,y)], fill=(r,g,b))

        # Top brand bar
        draw.rectangle([(0,0),(W,70)], fill=(*pri,255))
        draw.text((54,20), "BERKAH KARYA", font=fnt(32,bold=True), fill=BK_WHITE)
        draw.rectangle([(0,67),(W,70)], fill=(*acc,200))

        # Big point number (centered, large)
        num_font = fnt(220, bold=True)
        draw.text((W//2, H//2-350), str(i), font=num_font,
                  fill=(*acc,40), anchor="mt")

        # Point number badge
        draw.ellipse([(W//2-60, H//2-250),(W//2+60, H//2-130)],
                     fill=(*acc,200))
        draw.text((W//2, H//2-190), str(i), font=fnt(80,bold=True),
                  fill=(20,20,20) if sum(acc)>400 else BK_WHITE, anchor="mm")

        # Point text — big and centered
        clean = re.sub(r'^[\U0001F300-\U0001FFFF\U00002600-\U000027BF\s]+', '', point).strip()
        p_font = fnt(62, bold=True)
        words = clean.split()
        lines, line = [], ""
        for w in words:
            test = (line+" "+w).strip()
            if draw.textbbox((0,0), test, font=p_font)[2] <= W-120:
                line = test
            else:
                if line: lines.append(line)
                line = w
        if line: lines.append(line)

        total_h = len(lines) * 78
        start_y = H//2 - total_h//2 + 20
        for li, ln in enumerate(lines[:4]):
            draw.text((W//2, start_y + li*78), ln,
                      font=p_font, fill=BK_WHITE, anchor="mt")

        # Divider
        div_y = H//2 + total_h//2 + 40
        draw.rectangle([(W//2-60, div_y),(W//2+60, div_y+4)], fill=(*acc,180))

        # Progress dots
        dot_y = H - 200
        total_dots = 5
        for d_i in range(total_dots):
            cx = W//2 + (d_i - total_dots//2) * 40
            if d_i == i:
                draw.ellipse([(cx-12,dot_y-12),(cx+12,dot_y+12)], fill=(*acc,255))
            else:
                draw.ellipse([(cx-7,dot_y-7),(cx+7,dot_y+7)], fill=(*BK_WHITE,60))

        # Footer
        draw.rectangle([(0,H-52),(W,H)], fill=(*pri,255))
        draw.text((54, H-36), "Digital Growth Agency", font=fnt(22),
                  fill=(*BK_WHITE,140))

        sname = f"slide_{i}_point{i}.png"
        out = slides_dir / sname
        img.save(out, "PNG", optimize=True)
        slide_paths.append(out)

    # Slide 4: CTA close (high-contrast, product focus)
    img = Image.new("RGB", (W, H), pri)
    draw = ImageDraw.Draw(img, "RGBA")

    # Radial-ish gradient using concentric rects
    for ring in range(0, min(W,H)//2 - 10, 30):
        alpha = max(5, 80 - ring//5)
        x0,y0 = ring, ring
        x1,y1 = W-ring, H-ring
        if x1>x0 and y1>y0:
            draw.rectangle([(x0,y0),(x1,y1)], outline=(*acc,alpha), width=2)

    draw.text((W//2, H//2-320), "✅", font=fnt(160,bold=True),
              fill=(*acc,255), anchor="mt")
    draw.text((W//2, H//2-130), "Dapatkan Sekarang!", font=fnt(72,bold=True),
              fill=BK_WHITE, anchor="mt")
    if product:
        draw.text((W//2, H//2-30), product, font=fnt(52),
                  fill=(*acc,230), anchor="mt")

    draw.text((W//2, H//2+120), "berkahkarya.org", font=fnt(48,bold=True),
              fill=BK_WHITE, anchor="mt")
    draw.text((W//2, H//2+190), "Link ada di bio 👆", font=fnt(42),
              fill=(*BK_WHITE,200), anchor="mt")

    # Geometric decoration
    for ring in range(3):
        r = 120 + ring*60
        cx, cy = W//2, H//2-200
        draw.ellipse([(cx-r,cy-r),(cx+r,cy+r)], outline=(*acc,40+ring*20), width=2)

    draw.rectangle([(0,H-52),(W,H)], fill=(0,0,0,100))
    draw.text((W//2, H-36), "@berkahkarya • berkahkarya.org",
              font=fnt(24), fill=(*BK_WHITE,160), anchor="mt")

    s4 = slides_dir / "slide_4_cta.png"
    img.save(s4, "PNG", optimize=True)
    slide_paths.append(s4)

    return slide_paths


# ═══════════════════════════════════════════════════════════════════════════════
# METHOD 1: GeminiGenAI
# ═══════════════════════════════════════════════════════════════════════════════

def try_geminigen(headline: str, persona_id: str, slides: list[Path],
                  out_path: Path) -> Optional[Path]:
    """Try Gemini image-to-video (Veo 2 / Imagen 3)."""
    if not GEMINI_KEY:
        print("  [GeminiGen] ⏭️  No GEMINI_API_KEY")
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)

        print("  [GeminiGen] 🎬 Trying Veo 2 image-to-video...")

        # Use hook slide as seed image
        prompt = (
            f"Create a smooth 15-second vertical video (9:16) based on this image. "
            f"Topic: {headline}. "
            f"Add subtle motion: gentle zoom in, floating particles. "
            f"Professional Indonesian social media style. No text changes."
        )

        # Try Veo 2 via files API
        img_file = genai.upload_file(str(slides[0]), mime_type="image/png")
        model = genai.GenerativeModel("veo-2.0-generate-001")
        result = model.generate_content([prompt, img_file])

        if result and hasattr(result, 'video'):
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, 'wb') as f:
                f.write(result.video)
            print(f"  [GeminiGen] ✅ {out_path.name}")
            return out_path

    except Exception as e:
        print(f"  [GeminiGen] ❌ {type(e).__name__}: {str(e)[:120]}")
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# METHOD 2: BytePlus Seedance
# ═══════════════════════════════════════════════════════════════════════════════

def _byteplus_headers():
    return {
        "Authorization": f"Bearer {BYTEPLUS_KEY}",
        "Content-Type": "application/json",
    }

def _byteplus_poll(task_id: str, timeout: int = 180) -> Optional[str]:
    """Poll BytePlus task until done. Returns video URL or None."""
    import requests
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(
            f"{BYTEPLUS_BASE}/contents/generations/tasks/{task_id}",
            headers=_byteplus_headers(), timeout=15
        )
        if not r.ok:
            print(f"  [BytePlus] Poll error {r.status_code}")
            return None
        data = r.json()
        status = data.get("status", "")
        if status == "succeeded":
            # Extract video URL from response
            content = data.get("content", {})
            videos = content.get("video_urls", []) or \
                     [v.get("url") for v in content.get("videos", []) if v.get("url")]
            return videos[0] if videos else None
        elif status in ("failed", "cancelled"):
            err = data.get("error", {}).get("message", "unknown")
            print(f"  [BytePlus] Task {status}: {err}")
            return None
        print(f"  [BytePlus] Status: {status}... waiting 5s")
        time.sleep(5)
    print("  [BytePlus] ⏱️  Timeout")
    return None

def _download_video(url: str, out_path: Path) -> Path:
    """Download video from URL to path."""
    import requests
    out_path.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=120, stream=True)
    with open(out_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return out_path

def try_byteplus_i2v(slides: list[Path], headline: str, out_path: Path,
                     model: str = "i2v_lite") -> Optional[Path]:
    """BytePlus Seedance image-to-video."""
    import requests, base64

    print(f"  [BytePlus] 🎬 Trying Seedance i2v ({BYTEPLUS_MODELS[model]})...")

    # Encode hook image as base64
    img_path = slides[0]  # hook slide
    with open(img_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()

    prompt = (
        f"{headline}. "
        "Cinematic zoom in slowly, subtle floating particles, professional motion. "
        "Vertical 9:16 format, Indonesian social media style."
    )

    payload = {
        "model": BYTEPLUS_MODELS[model],
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
            {"type": "text", "text": prompt},
        ],
        "ratio": "9:16",
    }

    try:
        r = requests.post(
            f"{BYTEPLUS_BASE}/contents/generations/tasks",
            headers=_byteplus_headers(),
            json=payload, timeout=30
        )
        if not r.ok:
            print(f"  [BytePlus i2v] ❌ {r.status_code}: {r.text[:200]}")
            return None

        task_id = r.json().get("id")
        print(f"  [BytePlus i2v] Task: {task_id}")
        video_url = _byteplus_poll(task_id, timeout=180)
        if video_url:
            path = _download_video(video_url, out_path)
            size_mb = path.stat().st_size / 1e6
            print(f"  [BytePlus i2v] ✅ {path.name} ({size_mb:.1f} MB)")
            return path
    except Exception as e:
        print(f"  [BytePlus i2v] ❌ {type(e).__name__}: {str(e)[:120]}")
    return None

def try_byteplus_t2v(headline: str, persona_id: str, out_path: Path) -> Optional[Path]:
    """BytePlus Seedance text-to-video (no image needed)."""
    import requests

    print(f"  [BytePlus t2v] 🎬 Trying Seedance t2v...")
    persona_db = json.loads(PERSONA_DB.read_text()) if PERSONA_DB.exists() else {}
    personas = {p["persona_id"]: p for p in persona_db.get("personas", [])}
    niche = personas.get(persona_id, {}).get("niche", "digital marketing")

    prompt = (
        f"Professional Indonesian social media video about {niche}. "
        f"Topic: {headline}. "
        "Modern minimal style, dark background with blue accents, "
        "text appears with smooth animations, 9:16 vertical format. "
        "Clean corporate look, engaging motion graphics."
    )

    payload = {
        "model": BYTEPLUS_MODELS["t2v_lite"],
        "content": [{"type": "text", "text": prompt}],
        "ratio": "9:16",
    }

    try:
        r = requests.post(
            f"{BYTEPLUS_BASE}/contents/generations/tasks",
            headers=_byteplus_headers(),
            json=payload, timeout=30
        )
        if not r.ok:
            print(f"  [BytePlus t2v] ❌ {r.status_code}: {r.text[:200]}")
            return None

        task_id = r.json().get("id")
        print(f"  [BytePlus t2v] Task: {task_id}")
        video_url = _byteplus_poll(task_id, timeout=180)
        if video_url:
            path = _download_video(video_url, out_path)
            size_mb = path.stat().st_size / 1e6
            print(f"  [BytePlus t2v] ✅ {path.name} ({size_mb:.1f} MB)")
            return path
    except Exception as e:
        print(f"  [BytePlus t2v] ❌ {type(e).__name__}: {str(e)[:120]}")
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# METHOD 3: Remotion
# ═══════════════════════════════════════════════════════════════════════════════

REMOTION_PROJ = CS_DIR / "remotion_project"

def _ensure_remotion_project(slides: list[Path], persona_id: str,
                              headline: str, acc_hex: str = "#2563EB"):
    """Create/update Remotion project for rendering."""
    REMOTION_PROJ.mkdir(parents=True, exist_ok=True)

    # package.json
    pkg = {
        "name": "berkahkarya-video",
        "version": "1.0.0",
        "scripts": {"build": "remotion render"},
        "dependencies": {"remotion": "^4.0.0", "@remotion/cli": "^4.0.0"}
    }
    (REMOTION_PROJ / "package.json").write_text(json.dumps(pkg, indent=2))

    # Slide timing config
    slides_config = []
    for i, s in enumerate(slides):
        import shutil
        dest = REMOTION_PROJ / f"slide_{i}.png"
        shutil.copy(s, dest)
        slides_config.append({"file": f"./slide_{i}.png", "duration": 75})  # 75 frames = 3sec @25fps

    total_frames = sum(s["duration"] for s in slides_config)

    # Root composition
    root_tsx = f"""
import {{Composition}} from 'remotion';
import {{SlideShow}} from './SlideShow';

export const RemotionRoot: React.FC = () => {{
  return (
    <Composition
      id="BerkahKaryaVideo"
      component={{SlideShow}}
      durationInFrames={{{total_frames}}}
      fps={{25}}
      width={{1080}}
      height={{1920}}
      defaultProps={{{{
        slides: {json.dumps([str(REMOTION_PROJ / f"slide_{i}.png") for i in range(len(slides))])},
        accentColor: "{acc_hex}",
        headline: {json.dumps(headline)},
      }}}}
    />
  );
}};
"""
    (REMOTION_PROJ / "Root.tsx").write_text(root_tsx)

    # SlideShow component
    slideshow_tsx = """
import {Img, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

interface Props {
  slides: string[];
  accentColor: string;
  headline: string;
}

export const SlideShow: React.FC<Props> = ({slides, accentColor}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const slideDuration = 75; // frames per slide
  const currentSlide = Math.min(Math.floor(frame / slideDuration), slides.length - 1);
  const slideFrame = frame % slideDuration;

  const scale = interpolate(slideFrame, [0, slideDuration], [1, 1.06], {extrapolateRight: 'clamp'});
  const opacity = interpolate(slideFrame, [0, 8, slideDuration-8, slideDuration], [0, 1, 1, 0]);

  return (
    <div style={{width: '100%', height: '100%', overflow: 'hidden', background: '#0a0a1a'}}>
      <div style={{transform: `scale(${scale})`, opacity, transformOrigin: 'center center', width: '100%', height: '100%'}}>
        <Img src={slides[currentSlide]} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </div>
    </div>
  );
};
"""
    (REMOTION_PROJ / "SlideShow.tsx").write_text(slideshow_tsx)
    return REMOTION_PROJ, total_frames

def try_remotion(slides: list[Path], headline: str, persona_id: str,
                 out_path: Path) -> Optional[Path]:
    """Render multi-slide video using Remotion."""
    print("  [Remotion] 🎬 Trying programmatic render...")

    acc_hex = "#2563EB"  # default BK blue
    try:
        proj, total_frames = _ensure_remotion_project(slides, persona_id, headline, acc_hex)

        # Install deps
        subprocess.run(["npm", "install", "--prefix", str(proj)],
                       capture_output=True, timeout=60)

        out_path.parent.mkdir(parents=True, exist_ok=True)

        result = subprocess.run(
            ["npx", "remotion", "render", "BerkahKaryaVideo", str(out_path)],
            cwd=str(proj), capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0 and out_path.exists():
            size_mb = out_path.stat().st_size / 1e6
            print(f"  [Remotion] ✅ {out_path.name} ({size_mb:.1f} MB)")
            return out_path
        else:
            print(f"  [Remotion] ❌ {result.stderr[-300:]}")
    except Exception as e:
        print(f"  [Remotion] ❌ {type(e).__name__}: {str(e)[:120]}")
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# METHOD 4: FFmpeg multi-slide (always works)
# ═══════════════════════════════════════════════════════════════════════════════

def try_ffmpeg_multislide(slides: list[Path], out_path: Path,
                          fps: int = 25, slide_sec: int = 4) -> Optional[Path]:
    """
    Concatenate multiple slides with crossfade transitions.
    Each slide: zoom in slowly for slide_sec seconds.
    Transition: crossfade 0.5s between slides.
    """
    print(f"  [FFmpeg] 🎬 Multi-slide render ({len(slides)} slides × {slide_sec}s)...")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Build filter_complex for multi-slide with crossfade
    # Each slide: scale → pad to 9:16 → zoompan → fade
    input_args = []
    for s in slides:
        input_args += ["-loop", "1", "-t", str(slide_sec + 1), "-i", str(s)]

    # Each slide processed: scale to 1080 wide, pad to 1080x1920, zoompan, fade
    filter_parts = []
    for i in range(len(slides)):
        zoom_factor = 1.0 + (0.08 / (slide_sec * fps)) * fps  # ≈ 1.0016 per frame
        f = (
            f"[{i}:v]"
            f"scale=1080:-1,"
            f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"setsar=1,"
            f"zoompan="
            f"z='min(zoom+0.001,1.08)':"
            f"x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':"
            f"d={slide_sec*fps}:s=1080x1920:fps={fps},"
            f"fade=t=in:st=0:d=0.4,"
            f"fade=t=out:st={slide_sec-0.4}:d=0.4,"
            f"trim=duration={slide_sec}"
            f"[v{i}]"
        )
        filter_parts.append(f)

    # Concat all slides
    concat_inputs = "".join(f"[v{i}]" for i in range(len(slides)))
    filter_parts.append(f"{concat_inputs}concat=n={len(slides)}:v=1:a=0[out]")
    filter_complex = ";".join(filter_parts)

    cmd = (
        input_args +
        ["-filter_complex", filter_complex,
         "-map", "[out]",
         "-c:v", "libx264", "-preset", "fast", "-crf", "23",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart",
         "-y", str(out_path)]
    )

    try:
        result = subprocess.run(
            ["ffmpeg"] + cmd,
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0 and out_path.exists():
            size_mb = out_path.stat().st_size / 1e6
            print(f"  [FFmpeg] ✅ {out_path.name} ({size_mb:.1f} MB)")
            return out_path
        else:
            print(f"  [FFmpeg] ❌ {result.stderr[-400:]}")
    except Exception as e:
        print(f"  [FFmpeg] ❌ {type(e).__name__}: {str(e)[:120]}")
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════════

def generate_video(
    persona_id: str,
    headline: str,
    points: list[str] = None,
    product: str = None,
    method: str = "auto",   # auto | gemini | byteplus | remotion | ffmpeg
    date_str: str = None,
) -> Optional[Path]:
    """
    Full fallback chain video generator.
    Returns Path to final video or None if all methods fail.
    """
    from persona_visual_engine import PersonaVisualEngine, DEFAULT_POINTS
    engine = PersonaVisualEngine()
    pts = points or DEFAULT_POINTS.get(persona_id, DEFAULT_POINTS["entertainment-engagement"])
    persona = engine.personas.get(persona_id, {})
    product = product or (persona.get("primary_product") or "").replace("-"," ").title() or None
    date_str = date_str or datetime.now().strftime("%Y%m%d")

    vid_dir = OUTPUT_DIR / date_str / "videos"
    vid_dir.mkdir(parents=True, exist_ok=True)
    safe_hl = headline[:30].replace(" ","_").replace("/","-")
    base_name = f"{persona_id}_{safe_hl}_{date_str}"

    print(f"\n🎬 Generating video: {persona_id}")
    print(f"   Headline: {headline}")
    print(f"   Method:   {method}")

    # Step 1: Generate 5 slides
    print("\n📸 Generating slides...")
    slides = generate_slides(persona_id, headline, pts, product, date_str)
    print(f"   ✅ {len(slides)} slides ready")

    # Step 2: Try methods in order
    out_path = vid_dir / f"{base_name}.mp4"
    result = None

    if method in ("auto", "gemini"):
        result = try_geminigen(headline, persona_id, slides, vid_dir / f"{base_name}_gemini.mp4")
        if result: return result
        if method == "gemini": return None

    if method in ("auto", "byteplus"):
        result = try_byteplus_i2v(slides, headline, vid_dir / f"{base_name}_byteplus_i2v.mp4")
        if result: return result
        # i2v failed, try t2v
        result = try_byteplus_t2v(headline, persona_id, vid_dir / f"{base_name}_byteplus_t2v.mp4")
        if result: return result
        if method == "byteplus": return None

    if method in ("auto", "remotion"):
        result = try_remotion(slides, headline, persona_id, vid_dir / f"{base_name}_remotion.mp4")
        if result: return result
        if method == "remotion": return None

    # Always available fallback
    if method in ("auto", "ffmpeg"):
        result = try_ffmpeg_multislide(slides, out_path)
        if result: return result

    print(f"\n❌ All methods failed for {persona_id}")
    return None


def batch_generate(method: str = "auto", date_str: str = None):
    """Generate videos for all personas with plans today."""
    date_str = date_str or datetime.now().strftime("%Y-%m-%d").replace("-","")
    plan_file = OUTPUT_DIR / datetime.now().strftime("%Y-%m-%d") / "plan.json"
    if not plan_file.exists():
        print(f"No plan found: {plan_file}")
        return []

    plans = json.loads(plan_file.read_text())
    results = []
    for plan in plans:
        pid = plan["persona_id"]
        hl  = plan["headline"]
        try:
            vid = generate_video(pid, hl, method=method, date_str=date_str)
            if vid:
                results.append({"persona_id": pid, "video": str(vid)})
                print(f"✅ {pid}: {vid.name}")
        except Exception as e:
            print(f"❌ {pid}: {e}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Generation Pipeline")
    parser.add_argument("--persona", default="trading-finance")
    parser.add_argument("--headline", default="5 Kesalahan Fatal Trader Pemula")
    parser.add_argument("--method", default="auto",
                        choices=["auto","gemini","byteplus","remotion","ffmpeg"])
    parser.add_argument("--batch", action="store_true")
    args = parser.parse_args()

    if args.batch:
        batch_generate(method=args.method)
    else:
        vid = generate_video(
            persona_id=args.persona,
            headline=args.headline,
            method=args.method,
        )
        if vid:
            print(f"\n🎬 Final video: {vid}")
        else:
            print("\n❌ Failed to generate video")
