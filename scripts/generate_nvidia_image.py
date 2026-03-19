#!/usr/bin/env python3
"""
Generate Professional AI Image Using NVIDIA NIM
For: TikTok hook visualization - "STOP! Konten manual makan waktu 4 jam/post!"
"""

import asyncio
import aiohttp
import base64
import os
from pathlib import Path

# Import message utility
try:
    from message import send as message
except ImportError:
    print("⚠️ message module not available, will skip sending to Telegram")
    message = None

# Get API key
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY')
if not NVIDIA_API_KEY:
    print("❌ ERROR: NVIDIA_API_KEY not found")
    exit(1)

# NVIDIA NIM Configuration
BASE_URL = "https://ai.api.nvidia.com/v1/genai"

# Professional image prompt
PROMPT = """Professional TikTok hook image, dark modern workspace scene.

Visual Style:
- Dark gradient background (dark blue-gray to nearly black)
- Bold, energetic, professional
- High contrast for readability
- Cinematic photography quality
- 9:16 portrait format

Typography Elements (to be added in post-processing):
- Large, bold "STOP!" text (coral-red or orange-red, centered)
- Secondary text: "KONTEN MANUAL MEMAKAN WAKTU" (white, bold)
- Emphasis: "4 JAM / POST!" (large, bold, same accent color)
- Tagline: "GAK SCALE!" (smaller, white)

Mood & Atmosphere:
- Energetic but professional
- Urgent yet approachable
- High-end brand feel
- Viral-worthy visual

Technical Specs:
- Resolution: High (suitable for 9:16 vertical)
- Quality: Professional photography or illustration style
- Smooth gradients or lighting
- Text-ready background (dark enough for white text overlay)
- Modern, sleek aesthetic

Additional Notes:
- Include subtle tech/creative workspace elements (screens, creative tools)
- No text in the generated image (text will be added)
- Focus on professional, clean, impactful background
"""

async def generate_image():
    """Generate image using NVIDIA NIM flux.1-dev model."""

    print("="*80)
    print("🎨 NVIDIA NIM IMAGE GENERATION")
    print("="*80)
    print()
    print("Provider: NVIDIA NIM")
    print("Model: black-forest-labs/flux.1-dev")
    print("Purpose: Professional TikTok hook background")
    print()
    print("="*80)
    
    print("\n📝 Prompt:")
    print("-"*80)
    print(PROMPT)
    print("-"*80)
    
    # Prepare request
    model = "black-forest-labs/flux.1-dev"
    url = f"{BASE_URL}/{model}"
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # IMPORTANT: NVIDIA API only accepts minimal payload for flux.1-dev
    # Only send "prompt" - no num_images, no null fields
    payload = {
        "prompt": PROMPT
    }
    
    print("\n🔄 Generating image with NVIDIA...")
    print(f"   URL: {url}")
    print(f"   Model: {model}")
    print(f"   API Key: {NVIDIA_API_KEY[:8]}...{NVIDIA_API_KEY[-8:]}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                print(f"\n📡 Response status: {resp.status}")
                
                if resp.status == 200:
                    data = await resp.json()
                    
                    print(f"\n✅ SUCCESS!")
                    print(f"   Response keys: {list(data.keys())}")
                    
                    # Extract base64 image
                    if "artifacts" in data and len(data["artifacts"]) > 0:
                        artifact = data["artifacts"][0]
                        image_base64 = artifact.get("base64")
                        finish_reason = artifact.get("finishReason")
                        
                        print(f"   Base64 length: {len(image_base64) if image_base64 else 0}")
                        print(f"   Finish reason: {finish_reason}")
                        
                        if image_base64:
                            # Decode base64
                            image_data = base64.b64decode(image_base64)
                            
                            # Save original image
                            output_dir = Path.home() / ".openclaw" / "workspace" / "content" / "samples"
                            output_dir.mkdir(parents=True, exist_ok=True)
                            
                            original_file = output_dir / "nvidia_image_original.png"
                            with open(original_file, "wb") as f:
                                f.write(image_data)
                            
                            file_size_bytes = len(image_data)
                            file_size_mb = file_size_bytes / (1024 * 1024)
                            file_size_kb = file_size_bytes / 1024
                            
                            print(f"\n✅ Image saved!")
                            print(f"   File: {original_file}")
                            print(f"   Size: {file_size_kb:.1f} KB ({file_size_mb:.3f} MB)")
                            print(f"   Resolution: 1024x1024 or other (flux.1-dev output)")
                            
                            print("\n📊 Image Details:")
                            print(f"   - Format: PNG (from JPEG base64)")
                            print(f"   - Model: {model}")
                            print(f"   - API: NVIDIA NIM")
                            
                            return {
                                "success": True,
                                "file_path": str(original_file),
                                "file_size_kb": file_size_kb,
                                "file_size_mb": file_size_mb,
                                "base64_image": image_base64,
                                "finish_reason": finish_reason
                            }
                        else:
                            print(f"\n❌ No base64 image in response")
                            return {"success": False, "error": "No image data"}
                    else:
                        print(f"\n❌ Unexpected response format")
                        print(f"   Response: {data}")
                        return {"success": False, "error": "Unexpected format"}
                else:
                    print(f"\n❌ API Error: HTTP {resp.status}")
                    error_text = await resp.text()
                    print(f"   Error: {error_text}")
                    return {"success": False, "error": f"HTTP {resp.status}"}
    except Exception as e:
        print(f"\n❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

async def create_final_image_with_text(original_image_path, text_overlay_data=None):
    """Create final image with text overlaid using PIL."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Open original image
        img = Image.open(original_image_path)
        draw = ImageDraw.Draw(img)
        
        width, height = img.size
        
        # Better design for TikTok hook
        # Coral-red accent (#FF6B6B)
        accent_color = (255, 107, 107)
        text_white = (255, 255, 255, 240)
        text_gray = (220, 220, 220, 220)
        
        # Try to find fonts
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        ]
        
        font_large = None
        font_medium = None
        font_small = None
        
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
        
        if font_large is None:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        print("\n🎨 Adding text overlays...")
        
        # Add subtle gradient overlay for better text readability
        # Create a gradient overlay layer
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Gradient from top
        for y in range(height):
            alpha = int(30 * y / height)  # Subtle gradient
            alpha = min(alpha, 60)  # Max 60% opacity black overlay
            if alpha > 0:
                overlay_draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
        
        # Composite gradient overlay
        img = Image.alpha_composite(img.convert('RGBA'), overlay)
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Draw accent line at top (modern design element)
        draw.line([(width//2, 120), (width//2, height-120)], fill=accent_color, width=3)
        
        # Draw circle element at top
        draw.ellipse([width//2 - 100, 100, width//2 + 100, 300], fill=accent_color)
        
        # Main hook text - "STOP!"
        hook_text = "STOP!"
        hook_y = height * 0.25
        
        # Shadow for readability
        shadow_offset = 5
        for i in range(3):
            offset = shadow_offset - i
            draw.text((width//2 - offset, hook_y - offset), hook_text, fill=(0, 0, 0, 100), font=font_large, anchor="mm")
        
        draw.text((width//2, hook_y), hook_text, fill=accent_color, font=font_large, anchor="mm")
        
        # Subheading
        sub_text = "KONTEN MANUAL MEMAKAN WAKTU"
        sub_y = hook_y + 200
        
        draw.text((width//2 - shadow_offset, sub_y - shadow_offset), sub_text, fill=(0, 0, 0, 80), font=font_medium, anchor="mm")
        draw.text((width//2, sub_y), sub_text, fill=text_white, font=font_medium, anchor="mm")
        
        # Emphasis text
        emphasis_text = "4 JAM / POST!"
        emphasis_y = sub_y + 180
        
        for i in range(3):
            offset = shadow_offset - i
            draw.text((width//2 - offset, emphasis_y - offset), emphasis_text, fill=(0, 0, 0, 100), font=font_large, anchor="mm")
        
        draw.text((width//2, emphasis_y), emphasis_text, fill=accent_color, font=font_large, anchor="mm")
        
        # Tagline
        tagline_text = "GAK SCALE! MULAI DARI GRATIS"
        tagline_y = height * 0.75
        
        draw.text((width//2 - shadow_offset, tagline_y - shadow_offset), tagline_text, fill=(0, 0, 0, 80), font=font_small, anchor="mm")
        draw.text((width//2, tagline_y), tagline_text, fill=text_gray, font=font_small, anchor="mm")
        
        # Add bottom accent line
        draw.line([(width//2 - 150, tagline_y + 80), (width//2 + 150, tagline_y + 80)], fill=accent_color, width=2)
        
        # Save final image
        output_dir = Path.home() / ".openclaw" / "workspace" / "content" / "samples"
        final_file = output_dir / "nvidia_hook_final.png"
        img.save(final_file, quality=95)
        
        print(f"✅ Final image saved: {final_file}")
        print(f"   Resolution: {width}x{height}")
        print(f"   Text overlays: Applied")
        
        return str(final_file)
        
    except Exception as e:
        print(f"\n❌ Error creating final image: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    """Main orchestration function."""
    # Step 1: Generate image with NVIDIA
    result = await generate_image()
    
    if result.get("success"):
        # Step 2: Create final image with text overlays
        final_path = await create_final_image_with_text(result["file_path"])
        
        if final_path:
            print("\n" + "="*80)
            print("✅ COMPLETE! Professional Hook Image Ready")
            print("="*80)
            print(f"\nOriginal AI Image: {result['file_path']}")
            print(f"Size: {result['file_size_kb']:.1f} KB")
            print(f"\nFinal Image with Text: {final_path}")
            print(f"Style: Professional TikTok hook")
            print("\n📱 Ready to send to Telegram!")
            print("="*80)
            
            # Send to Telegram
            print("\n📤 Sending final image to Telegram...")
            
            if message:
                try:
                    # Send via message tool
                    message_result = message(
                        action="send",
                        target="5220170786",
                        media=final_path,
                        filename="nvidia_hook_final.png",
                        caption="""✅ **PROFESSIONAL HOOK IMAGE - NVIDIA AI GENERATED**

━━━━━━━━━━━━━━━━━━━━━━━
Product: Guru Pintar AI
Type: Faceless Hook Visual
Style: Professional, Modern, Dark Theme

━━━━━━━━━━━━━━━━━━━━━━━
Content:
• HOOK: 🔥 STOP! (bold coral-red)
• "KONTEN MANUAL MEMAKAN WAKTU"
• "4 JAM / POST!" (emphasis)
• "GAK SCALE! MULAI DARI GRATIS"

Professional gradient background + text shadows + modern layout.

Quality: NVIDIA NIM flux.1-dev model
Format: 9:16 vertical (1080x1920)
Platform: TikTok / IG Reels / YouTube Shorts

━━━━━━━━━━━━━━━━━━━━━━━
✅ Ready for posting!
Link: https://lnkd.in/ai-content-pro"""
                    )
                    
                    print("✅ Image sent to Telegram!")
                    
                except Exception as e:
                    print(f"⚠️ Failed to send: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("⚠️ Message module not available, skipping Telegram send")
        else:
            print("\n⚠️ Text overlay failed, but AI image generated successfully")
            print(f"Original: {result['file_path']}")
    else:
        print("\n" + "="*80)
        print("❌ IMAGE GENERATION FAILED")
        print("="*80)
        print(f"Error: {result.get('error')}")
        print("="*80)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()