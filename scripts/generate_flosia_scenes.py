#!/usr/bin/env python3
"""
Generate Flosia TikTok product review scene images using NVIDIA NIM"""
import asyncio
import aiohttp
import base64
import os
from pathlib import Path

NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY')

BASE_URL = "https://ai.api.nvidia.com/v1/genai"
MODEL = "black-forest-labs/flux.1-dev"

prompts = [
    "Indonesian woman 25-30 years old (modern casual style), holding Flosia detergent bottle 1.5L Anti-Bakteri, smiling at camera, clean bright Indonesian living room with laundry, natural lighting from window, 9:16 vertical format, Instagram aesthetic, professional product photography, warm friendly expression, bottle features clearly visible",
    "Same Indonesian woman pouring Flosia detergent from 1.5L bottle onto dirty clothes in laundry basket, close-up action shot, demonstrating product texture, natural light, 9:16 vertical, Instagram aesthetic, professional product photography",
    "Same Indonesian woman using Flosia detergent to clean stained white shirt, showing detergent working, before/after contrast implied, bright laundry room setting, sunlight, 9:16 vertical, Instagram aesthetic, professional product photography",
    "Same Indonesian woman holding clean bright white shirt, satisfied happy expression, showing cleaning result, Flosia detergent bottle visible nearby, clean laundry room background, natural light, 9:16 vertical, Instagram aesthetic, professional product photography",
    "Same Indonesian woman holding Flosia detergent bottle close-up, pointing to product features with thumb up, friendly educational pose, clean background, professional studio lighting, 9:16 vertical, Instagram aesthetic, product photography",
    "Same Indonesian woman doing pointing gesture to shopping cart, smile to camera, CTA pose, Flosia bottle in other hand, clean bright background, professional lighting, 9:16 vertical, Instagram aesthetic, call-to-action commercial photography"
]

async def main():
    print("="*80)
    print("🎨 FLOSIA TIKTOK SCENES - NVIDIA NIM GENERATION")
    print("="*80)
    
    url = f"{BASE_URL}/{MODEL}"
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    output_dir = Path.home() / ".openclaw" / "workspace" / "content" / "samples" / "flosia-scenes"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    saved_files = []
    
    for i, prompt_text in enumerate(prompts, 1):
        print(f"\n{'='*80}")
        print(f"Scene {i}/6: Generating...")
        print(f"{'='*80}")
        print(f"Prompt: {prompt_text[:100]}...")
        
        payload = {"prompt": prompt_text}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        
                        if "artifacts" in data and len(data["artifacts"]) > 0:
                            artifact = data["artifacts"][0]
                            image_base64 = artifact.get("base64")
                            
                            if image_base64:
                                image_data = base64.b64decode(image_base64)
                                
                                save_path = output_dir / f"flosia_scene{i}.png"
                                with open(save_path, "wb") as f:
                                    f.write(image_data)
                                
                                file_size_kb = len(image_data) / 1024
                                saved_files.append(str(save_path))
                                
                                print(f"✅ SUCCESS: {save_path}")
                                print(f"   Size: {file_size_kb:.1f} KB")
                            else:
                                print(f"❌ No image data in response")
                        else:
                            print(f"❌ Unexpected response: {data}")
                    else:
                        error_text = await resp.text()
                        print(f"❌ API Error HTTP {resp.status}: {error_text}")
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    print(f"\n{'='*80}")
    print(f"SUMMARY: {len(saved_files)}/6 scenes generated")
    print(f"{'='*80}")
    
    if saved_files:
        print("Files generated:")
        for f in saved_files:
            print(f"  - {f}")
    else:
        print("No files generated due to errors")

if __name__ == "__main__":
    asyncio.run(main())
