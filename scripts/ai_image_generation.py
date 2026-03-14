#!/usr/bin/env python3
"""
Generate Professional Hook Image using AI
Using nano-banana-pro (Gemini AI) or openai-image-gen (DALL-E)
"""

import subprocess
import json
from pathlib import Path

workspace = Path.home() / ".openclaw" / "workspace"

print("=" * 80)
print("🎨 AI IMAGE GENERATION - PROFESSIONAL STYLE")
print("=" * 80)
print()

# Professional prompt based on top-performing TikTok hooks
prompt = """Professional TikTok hook image for content creator education.

Visual Style:
- Modern, clean, professional design
- Dark gradient background: dark blue-gray to black
- Coral-red (#FF6B6B) or gold/yellow accent color for emphasis
- High contrast for readability

Typography:
- Bold, modern sans-serif font
- Center alignment
- Large, impactful headline text
- Text shadows for depth & readability
- Clear hierarchy

Content:
- Main headline: "STOP!" in large, bold, impactful font (coral-red or gold)
- Subheading: "KONTEN MANUAL MEMAKAN WAKTU"
- Emphasis: "4 JAM / POST!" in large, bold text
- Tagline: "GAK SCALE! MULAI DARI GRATIS" or similar

Layout:
- Vertical 9:16 format (1080x1920)
- Text centered vertically and horizontally
- Clean, uncluttered design
- Plenty of white space around text (dark background makes white text pop)
- Balanced composition

Vibe:
- Professional yet energetic
- Authoritative but approachable
- Inspiring & motivational
- Trustworthy brand feel

Quality:
- High resolution
- Sharp, clear text
- No blurry elements
- Professional photography or illustration
- Subtle gradient or texture in background
"""

print("PROMPT:")
print("-" * 80)
print(prompt)
print()

print("=" * 80)
print("GENERATION OPTIONS")
print("=" * 80)
print()

# Check available skills
print("Attempting to use nano-banana-pro (Gemini AI)...")
print()

# Try to read nano-banana-pro skill
nano_banana_skill = Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "skills" / "nano-banana-pro" / "SKILL.md"

if nano_banana_skill.exists():
    print("✅ nano-banana-pro skill found!")
    print()
    with open(nano_banana_skill, "r") as f:
        content = f.read()

    print("=" * 80)
    print("NANO-BANANA-PRO USAGE")
    print("=" * 80)
    print()

    # Extract key usage info
    print("To generate image with nano-banana-pro:")
    print()
    print("1. Install: uv is installed (already available)")
    print("2. Set environment: export GEMINI_API_KEY=[your_key]")
    print("3. Run: nano-banana --prompt '[your prompt]' --output hook_image_pro.png")
    print()

    # Write prompt to file for easy copy-paste
    prompt_file = workspace / "content" / "samples" / "hook_prompt.txt"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    with open(prompt_file, "w") as f:
        f.write(prompt)

    print(f"Prompt saved to: {prompt_file}")
    print()
    print("=" * 80)
    print("COMMAND TO RUN:")
    print("=" * 80)
    print()
    print(f"nano-banana --prompt '$(cat {prompt_file})' --output hook_image_pro.png")
    print()
    print("OR copy-paste prompt manually")
    print()
    print("=" * 80)
    print("ALTERNATIVE: openai-image-gen (DALL-E)")
    print("=" * 80)
    print()
    print("Available skill: openai-image-gen")
    print("Usage: Similar pattern, need OpenAI API key")
    print()

    print("=" * 80)
    print("QUICK START OPTIONS:")
    print("=" * 80)
    print()
    print("A) Generate with nano-banana-pro (Gemini AI)")
    print("   - Requires: GEMINI_API_KEY in environment")
    print("   - Command: 'openai-image-gen --prompt [prompt] --output output.png'")
    print()
    print("B) Generate with openai-image-gen (DALL-E)")
    print("   - Requires: OPENAI_API_KEY in environment")
    print("   - Command: 'openai-image-gen --prompt [prompt] --output output.png'")
    print()
    print("C) Use online tools")
    print("   - Canva (manual design, more control)")
    print("   - Remove.bg background remover")
    print("   - Text overlays in Photoshop/CapCut")
    print()

    print("=" * 80)
    print("RECOMMENDATION FOR NOW:")
    print("=" * 80)
    print()
    print("Since image viewing is temporarily unavailable, try this:")
    print()
    print("1. Use Canva (online) to design manually:")
    print("   - Open Canva")
    print("   - Search: 'TikTok hook template' or 'Instagram story template'")
    print("   - Use text overlay: 'STOP! // KONTEN MANUAL MEMAKAN WAKTU // 4 JAM/POST! // GAK SCALE'")
    print("   - Export as PNG (1080x1920)")
    print()
    print("2. OR wait for image model to reset and try AI generation again")
    print()
    print("3. OR provide specific style requirements and I'll create better manual template")
    print()

    print("=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print()
    print("1. Review prompt above - is it accurate?")
    print("2. Choose generation method (AI or manual)")
    print("3. Generate image and share for review")
    print("4. Approve → batch production!")
    print()
    print("=" * 80)

else:
    print("❌ nano-banana-pro skill not found")
    print()
    print("Alternative: Use openai-image-gen or Canva")
    print()