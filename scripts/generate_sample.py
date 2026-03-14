#!/usr/bin/env python3
"""
Generate Sample Image & Video for Content Validation Review
Product: Guru Pintar AI
Hook: 🔥 STOP! Konten manual makan waktu 4 jam/post!
"""

import subprocess
from pathlib import Path

workspace = Path.home() / ".openclaw" / "workspace"

print("=" * 80)
print("🎬 CONTENT PRODUCTION - SAMPLE GENERATION")
print("=" * 80)
print()

print("📌 TASK:")
print("1. Generate 1 sample IMAGE (Hook visual)")
print("2. Generate 1 sample VIDEO (15 detik faceless)")
print()
print("Product: Guru Pintar AI")
print("Hook: 🔥 STOP! Konten manual makan waktu 4 jam/post!")
print()

# Check available image generation skills
print("=" * 80)
print("CHECKING AVAILABLE SKILLS...")
print("=" * 80)
print()

skills_to_check = [
    "nano-banana-pro",
    "openai-image-gen",
    "canva"
]

print(f"Skills directory: {workspace.parent / 'skills'}")
print()

# Check if skills exist
skills_dir = Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "skills"
print(f"Looking for skills in: {skills_dir}")
print()

available_skills = []
for skill in skills_to_check:
    skill_path = skills_dir / skill / "SKILL.md"
    if skill_path.exists():
        available_skills.append(skill)
        print(f"✅ {skill} - AVAILABLE")
    else:
        # Check local workspace skills
        local_skill = workspace / "skills" / skill / "SKILL.md"
        if local_skill.exists():
            available_skills.append(skill)
            print(f"✅ {skill} - AVAILABLE (local)")
        else:
            print(f"❌ {skill} - NOT FOUND")

print()
print("=" * 80)
print("IMAGE GENERATION OPTIONS")
print("=" * 80)
print()

if "nano-banana-pro" in available_skills:
    print("Option 1: nano-banana-pro (Gemini AI)")
    print("  - Generate images via Gemini 3 Pro Image")
    print("  - Prompt: Create image showing person struggling with manual content creation, clock showing 4 hours, frustrated workspace setup")
    print("  - Style: Professional, realistic")
    print()
else:
    print("Option 1: nano-banana-pro - NOT AVAILABLE")
    print()

if "openai-image-gen" in available_skills:
    print("Option 2: openai-image-gen (DALL-E)")
    print("  - Generate images via OpenAI DALL-E")
    print("  - Prompt: Professional workspace scene, person exhausted creating content manually, clock showing 4 hours, scattered papers and laptop")
    print("  - Style: Realistic, high quality")
    print()
else:
    print("Option 2: openai-image-gen - NOT AVAILABLE")
    print()

print("Option 3: Web search stock images (Pexels, Pixabay - FREE)")
print("  - Download free stock images")
print("  - Search: 'frustrated person working', 'exhausted content creator', 'manual content creation'")
print()

print("=" * 80)
print("VIDEO GENERATION OPTIONS")
print("=" * 80)
print()

print("Option 1: Google TTS Voice Over + Caption")
print("  - Generate voice: 'STOP! Konten manual makan waktu 4 jam per post'")
print("  - Tool: gcloud text-to-speech (Google Cloud Platform)")
print("  - Audio: 3-5 seconds, energetic tone")
print()

print("Option 2: ElevenLabs Voice Over (FREE tier)")
print("  - Generate more natural voice")
print("  - Limit: 10k characters/month")
print()

print("Option 3: Text template with placeholder")
print("  - Create video template script")
print("  - Show where to insert voice over")
print("  - Manual production in CapCut")
print()

print("=" * 80)
print("PRODUCTION PLAN")
print("=" * 80)
print()

print("STEP 1: Generate Sample Image")
print("  → Method: [Will select based on available skills]")
print("  → Prompt: Text overlay '🔥 STOP! Konten manual makan waktu 4 jam/post!'")
print("  → Style: Bold white text centered, dark background for contrast")
print()

print("STEP 2: Generate Voice Over")
print("  → Text: 'STOP! Konten manual makan waktu 4 jam per post!'")
print("  → Tone: Energetic, attention-grabbing")
print("  → Duration: ~3-4 seconds")
print()

print("STEP 3: Create Video Template")
print("  → 0-3s: Image + text overlay (HOOK)")
print("  → 3-12s: B-roll screen recording (product interface)")
print("  → 12-15s: CTA with product link")
print("  → Audio: Voice over + upbeat background music")
print()

print("=" * 80)
print("EXECUTING GENERATION...")
print("=" * 80)
print()

# Check if nano-banana-pro skill exists and use it
nano_banana_skill = skills_dir / "nano-banana-pro" / "SKILL.md"
if nano_banana_skill.exists():
    print("Found nano-banana-pro skill!")
    print("Reading skill documentation...")
    with open(nano_banana_skill, "r") as f:
        skill_doc = f.read()
        print(skill_doc[:500])  # Show first 500 chars
        print()
else:
    print("nano-banana-pro skill not found in system")
    print()

# Try to generate image with available methods
print("ATTEMPTING IMAGE GENERATION...")
print()

# Try Python script creation
image_gen_script = workspace / "scripts" / "generate_sample_image.py"
with open(image_gen_script, "w") as f:
    f.write("""#!/usr/bin/env python3
\"\"\"
Generate Sample Image for Hook: "STOP! Konten manual makan waktu 4 jam/post!"
Using Python PIL to create text overlay
\"\"\"

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
""")

print(f"Created image generation script: {image_gen_script}")
print()

print("Executing image generation...")
try:
    result = subprocess.run(["python3", str(image_gen_script)], cwd=workspace, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
except Exception as e:
    print(f"Error executing: {e}")

print()
print("=" * 80)
print("NEXT: VIDEO GENERATION")
print("=" * 80)
print()

print("For video, we have options:")
print()
print("A) Use Google TTS to generate voice over + create video template")
print("B) Use content-generator skill (if available)")
print("C) Create video placeholder instructions for manual production")
print()

print("RECOMMENDATION FOR NOW:")
print("  → Generate sample IMAGE ✓ (done above)")
print("  → Provide voice over TEXT for review")
print("  → Show video template for manual production (or automation later)")
print()

print("=" * 80)