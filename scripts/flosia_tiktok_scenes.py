#!/usr/bin/env python3
"""
Generate 6 Scene Images for Flosia Deterjen Snappy 1.5L Anti-Bakteri TikTok Video
Using NVIDIA NIM flux.1-dev model
"""

import asyncio
import aiohttp
import base64
import os
from pathlib import Path

# Get API key
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY')
if not NVIDIA_API_KEY:
    print("❌ ERROR: NVIDIA_API_KEY not found")
    exit(1)

# NVIDIA NIM Configuration
BASE_URL = "https://ai.api.nvidia.com/v1/genai"
MODEL = "black-forest-labs/flux.1-dev"

# Scene prompts for Flosia Deterjen TikTok
SCENES = [
    {
        "id": 1,
        "prompt": """Modern Indonesian female, 25-30 years old, wearing casual modest clothing (hijab or modest outfit), holding up a slightly dirty white t-shirt with a concerned expression, bright natural daylight streaming through window, Indonesian home interior with modern furniture, clean minimalist style, professional photography, warm golden hour lighting, soft depth of field, no logos, authentic Indonesian setting""",
        "filename": "flosia_scene1_dirty_laundry.png"
    },
    {
        "id": 2,
        "prompt": """Modern Indonesian female, 25-30 years old, holding a yellow liquid laundry detergent bottle labeled "Flosia Snappy" in her hands, examining the product with interest, modern clean bathroom or laundry room backdrop, bright natural lighting, professional product photography, soft shadows, no brand logos visible except the yellow bottle, warm inviting atmosphere, Indonesian setting""",
        "filename": "flosia_scene2_product_showcase.png"
    },
    {
        "id": 3,
        "prompt": """Modern Indonesian female, 25-30 years old, carefully pouring yellow liquid laundry detergent from yellow bottle into washing machine drawer, close-up shot showing the liquid flowing, clean modern washing machine in background, bright studio lighting, sharp focus on hands and detergent, professional photography, no visible logos, warm clean aesthetic, Indonesian home laundry room""",
        "filename": "flosia_scene3_using_detergent.png"
    },
    {
        "id": 4,
        "prompt": """Modern Indonesian female, 25-30 years old, opening a washing machine door to reveal clean bright white clothes inside, fresh and clean impression, steam slight visible, bright white blue lighting symbolizing cleanliness, modern washing machine, professional photography, high contrast, hygienic clean aesthetic, no logos, Indonesian home setting, uplifting positive atmosphere""",
        "filename": "flosia_scene4_clean_result.png"
    },
    {
        "id": 5,
        "prompt": """Modern Indonesian female, 25-30 years old, holding up fresh clean white clothes against bright sunlight, big genuine smile showing satisfaction, clothes look pristine and white, outdoor Indonesian patio or balcony background with plants, golden hour lighting, professional portrait photography, soft bokeh background, no logos, warm happy atmosphere, triumphant feeling""",
        "filename": "flosia_scene5_satisfaction.png"
    },
    {
        "id": 6,
        "prompt": """Modern Indonesian female, 25-30 years old, standing confidently with hands on hips, satisfied expression with a thumbs up gesture, behind her a laundry basket filled with neatly folded bright clean clothes, warm natural lighting, Indonesian home interior, professional lifestyle photography, clean modern aesthetic, no logos, accomplished feeling, call-to-action gesture""",
        "filename": "flosia_scene6_call_to_action.png"
    }
]

async def generate_image(session, model, prompt, filename):
    """Generate single image using NVIDIA NIM."""

    url = f"{BASE_URL}/{model}"
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt
    }
    
    try:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                
                if "artifacts" in data and len(data["artifacts"]) > 0:
                    artifact = data["artifacts"][0]
                    image_base64 = artifact.get("base64")
                    
                    if image_base64:
                        # Decode and save
                        image_data = base64.b64decode(image_base64)
                        output_dir = Path.home() / ".openclaw" / "workspace" / "flosia-tiktok-scenes"
                        output_dir.mkdir(parents=True, exist_ok=True)
                        
                        file_path = output_dir / filename
                        with open(file_path, "wb") as f:
                            f.write(image_data)
                        
                        return {
                            "success": True,
                            "file_path": str(file_path),
                            "filename": filename,
                            "size_kb": len(image_data) / 1024
                        }
                else:
                    return {"success": False, "error": "No image data"}
            else:
                error_text = await resp.text()
                return {"success": False, "error": f"HTTP {resp.status}: {error_text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    """Generate all 6 scene images."""

    print("="*80)
    print("🎬 FLOSIA DETERJEN TIKTok - 6 SCENE IMAGES")
    print("="*80)
    print()
    print("Product: Flosia Deterjen Snappy 1.5L Anti-Bakteri")
    print("Model: Modern Indonesian Female (25-30 years old)")
    print("API: NVIDIA NIM flux.1-dev")
    print()
    print("="*80)

    async with aiohttp.ClientSession() as session:
        results = []
        
        for i, scene in enumerate(SCENES, 1):
            print(f"\n📸 Scene {i}/{6}: {scene['filename']}")
            print("-"*80)
            print(f"   Prompt length: {len(scene['prompt'])} chars")
            
            result = await generate_image(session, MODEL, scene['prompt'], scene['filename'])
            results.append(result)
            
            if result.get("success"):
                print(f"   ✅ SUCCESS: {result['file_path']}")
                print(f"   💾 Size: {result['size_kb']:.1f} KB")
            else:
                print(f"   ❌ FAILED: {result.get('error')}")
            
            # Rate limiting delay
            if i < 6:
                print(f"   ⏳ Waiting 2s before next scene...")
                await asyncio.sleep(2)

    print("\n" + "="*80)
    print("📊 GENERATION SUMMARY")
    print("="*80)

    success_count = sum(1 for r in results if r.get("success"))
    fail_count = len(results) - success_count

    print(f"\n✅ Successful: {success_count}/6")
    print(f"❌ Failed: {fail_count}/6")

    if success_count > 0:
        print(f"\n📁 Output directory: {Path.home() / '.openclaw' / 'workspace' / 'flosia-tiktok-scenes'}")
        print(f"\n📸 Generated files:")
        for result in results:
            if result.get("success"):
                print(f"   ✅ {result['filename']} ({result['size_kb']:.1f} KB)")

    print("\n" + "="*80)

    return success_count == 6

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted")
        exit(2)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(3)