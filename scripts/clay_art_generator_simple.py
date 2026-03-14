#!/usr/bin/env python3
"""
Clay Art Video Generator - Simplified
Fixed version without Unicode errors
"""

import json
from pathlib import Path

PRODUCTS = {
    "starter_ai_content": {
        "name": "Starter AI Content", "price": "Rp 49.000", "link": "https://lynk.id/jendralbot/xlymwzj2jylv",
        "mode": "review", "tone": "Edukatif", "hashtags": "#AIcontent #clayart #starter #AIindonesia"
    },
    "ai_content_pro": {
        "name": "AI Content Pro", "price": "Rp 89.000", "link": "https://lynk.id/jendralbot/d70eo2x45em5",
        "mode": "review", "tone": "Productivity", "hashtags": "#AIcontent #professional #clayart #AIautomation"
    },
    "guru_pintar_ai": {
        "name": "Guru Pintar AI", "price": "GRATIS", "link": "https://lynk.id/jendralbot/6821op5e24kn",
        "mode": "story", "tone": "Edukatif", "hashtags": "#free #AItraining #clayart #belajarAI #gratis"
    }
}

def build_clay_prompt(subject, lighting, camera, is_review=False):
    """Build clay prompt"""
    if is_review:
        return f"""{subject}
placed inside clay art diorama environment
handmade plasticine background
visible fingerprint marks on clay
smooth matte clay surface
{lighting}
{camera}
diorama world, mini scale
8k resolution, sharp focus
soft bokeh clay background"""
    else:
        return f"""{subject}
clay art style, handmade plasticine sculpture
stop-motion animation, polymer clay
visible fingerprint marks
rich saturated clay colors
{lighting}
{camera}
diorama world, whimsical atmosphere
ultra detailed, 8k resolution
sharp focus, soft bokeh background"""

def generate_scenes(product_key):
    """Generate scenes for product"""
    product = PRODUCTS[product_key]
    mode = product["mode"]
    
    scenes = []
    
    if mode == "story":
        # Story scenes
        scenes.append({
            "num": 1, "title": "Intro", "duration": "5s", "narrative": f"Apa rahasia {product['name']}?",
            "visual": f"Clay character muncul", "caption": f"Apa itu {product['name']}?",
            "prompt": build_clay_prompt("Clay book character with glow", "Indoor", "Tokoh", False),
            "animasi": "Slow glow"
        })
        
        scenes.append({"num": 2, "title": "Problem", "duration": "7s", "narrative": "Banyak orang punya masalah...",
            "visual": "Clay characters frustrated", "caption": "Kamu juga?",
            "prompt": build_clay_prompt("Clay people worried", "Sore", "Tokoh", False), "animasi": "Frustrated movement"
        })
        
        scenes.append({"num": 3, "title": "Discovery", "duration": "8s", "narrative": f"Temukan {product['name']}!",
            "visual": "Clay character discovers product", "caption": "Lho! Apa ini?",
            "prompt": build_clay_prompt("Clay character finding product", "Sore", "Tokoh", False), "animasi": "Discovery glow"
        })
        
        scenes.append({"num": 4, "title": "Transform", "duration": "10s", "narrative": f"{product['name']} mengubah semua!",
            "visual": "Clay world happy & bright", "caption": "Semua berubah!",
            "prompt": build_clay_prompt("Happy clay world celebrating", "Siang", "Bangunan", False), "animasi": "Celebration wide shot"
        })
        
        scenes.append({"num": 5, "title": "CTA", "duration": "5s", "narrative": f"Cek {product['link']} sekarang!",
            "visual": "Clay character shows link", "caption": f"Cek {product['link']}!",
            "prompt": build_clay_prompt("Clay character pointing to signboard", "Indoor", "Tokoh", False), "animasi": "Pointing bounce"
        })
    else:
        # Review scenes
        scenes.append({"num": 1, "title": "Hook", "duration": "3s", "narrative": "STOP! Ribet bikin konten?",
            "visual": f"REALISTIC {product['name']} in clay env", "caption": "BERHENTI!",
            "prompt": build_clay_prompt(f"REALISTIC {product['name']} product original, NOT clay", "Malam", "Close detail", True), "animasi": "Product close-up"
        })
        
        scenes.append({"num": 2, "title": "Problem", "duration": "8s", "narrative": "Manual editing makan waktu...",
            "visual": "Clay person frustrated with laptop", "caption": "Capek ribet!",
            "prompt": build_clay_prompt("Clay person with clay laptop", "Indoor", "Tokoh", True), "animasi": "Frustrated movement"
        })
        
        scenes.append({"num": 3, "title": "Solution", "duration": "8s", "narrative": f"Ada {product['name']}!",
            "visual": f"REALISTIC {product['name']} in clay office", "caption": "Ada solusinya!",
            "prompt": build_clay_prompt(f"REALISTIC {product['name']} in bright clay office", "Siang", "Bangunan", True), "animasi": "Product reveal"
        })
        
        scenes.append({"num": 4, "title": "Benefits", "duration": "10s", "narrative": f"{product['name']} save waktu, hemat!",
            "visual": "Clay people happy with product", "caption": "Kamu bisa!",
            "prompt": build_clay_prompt("Clay people celebrating with REALISTIC product", "Sore", "Bangunan", True), "animasi": "Group celebration"
        })
        
        scenes.append({"num": 5, "title": "CTA", "duration": "5s", "narrative": f"Cek {product['name']} cuma {product['price']}!",
            "visual": "REALISTIC product with price tag", "caption": f"Cek {product['link']}!",
            "prompt": build_clay_prompt(f"REALISTIC {product['name']} with clay price tag", "Indoor", "Close detail", True), "animasi": "Product pulse"
        })
    
    return scenes

def generate_script(product_key):
    """Generate complete script"""
    product = PRODUCTS[product_key]
    scenes = generate_scenes(product_key)
    duration = sum([int(s["duration"][:-1]) for s in scenes])
    
    divider = "=" * 80
    script = divider + "\n"
    script += "RINGKASAN PROYEK\n"
    script += divider + "\n"
    script += f"Topik: {product['name']} ({product['price']})\n"
    script += f"Style: Clay Art / Plasticine Diorama\n"
    script += f"Duration: {duration}s\n"
    script += "Platform: TikTok / Instagram Reels / YouTube Shorts\n"
    script += f"Tone: {product['tone']}\n\n"
    
    script += divider + "\n"
    script += "SCENE BREAKDOWN\n"
    script += divider + "\n\n"
    
    for scene in scenes:
        script += divider + "\n"
        script += f"SCENE {scene['num']} - {scene['title']} - {scene['duration']}\n"
        script += divider + "\n"
        script += f"Narrative: {scene['narrative']}\n"
        script += f"Visual: {scene['visual']}\n"
        script += f"Caption: {scene['caption']}\n"
        script += f"Clay Prompt: {scene['prompt']}\n"
        script += f"Animation: {scene['animasi']}\n\n"
    
    script += divider + "\n"
    script += "MUSIC & AUDIO\n"
    script += divider + "\n"
    script += "Music: Upbeat and playful\n"
    script += "Tone: Whimsical and charming\n"
    script += "Tempo: 100-120 BPM\n"
    script += "Voice: Friendly character voice\n\n"
    
    script += divider + "\n"
    script += "NARRATION\n"
    script += divider + "\n"
    for scene in scenes:
        script += scene['narrative'] + " "
    script += "\n\n"
    
    script += divider + "\n"
    script += "PRODUCTION GUIDE\n"
    script += divider + "\n"
    script += "1. Generate images using clay prompts (NVIDIA/Gemini)\n"
    script += "2. Create video with FFmpeg or AI tools\n"
    script += f"3. Duration: {duration}s, 9:16 format\n"
    script += f"4. Link: {product['link']}\n"
    script += f"5. Hashtags: {product['hashtags']}\n"
    script += divider
    
    return script

def main():
    print("CLAY ART VIDEO GENERATOR")
    print("=" * 60)
    print()
    
    workspace = Path.home() / ".openclaw" / "workspace"
    all_scripts = {}
    
    for product_key in PRODUCTS:
        script = generate_script(product_key)
        all_scripts[product_key] = {"product": PRODUCTS[product_key], "script": script}
        
        output_file = workspace / f"clay_{product_key}_script.txt"
        output_file.write_text(script)
        print(f"Generated: clay_{product_key}_script.txt")
    
    all_output = workspace / "clay_all_scripts.json"
    with open(all_output, "w") as f:
        json.dump(all_scripts, f, indent=2)
    
    print()
    print("=" * 60)
    print("DONE!")
    print("=" * 60)
    print(f"Products: {len(PRODUCTS)}")
    print(f"Story mode: 1 (guru_pintar_ai)")
    print(f"Review mode: 2 paid products")
    print()
    print("Next: Review scripts & generate images!")

if __name__ == "__main__":
    main()