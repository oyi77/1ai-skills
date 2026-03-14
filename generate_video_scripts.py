#!/usr/bin/env python3
"""
Generate Video Scripts for TikTok/Instagram Reels
15-30 second viral scripts
"""

import json
from pathlib import Path

PRODUCTS_FILE = "/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/jendralbot_products.json"
OUTPUT_DIR = Path("/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/jendralbot_assets/video_scripts")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_products():
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
        return data['products']

def create_video_script(product):
    """Create viral video script for product"""
    name = product['name']
    price = product.get('price', 0) if product.get('is_paid') else "GRATIS"
    hook = product.get('hook_template', '')
    url = product['url']

    # Generate 3 script variations
    scripts = []

    # Script 1: Shock Value
    script1 = f"""
VIDEO SCRIPT: {name} - Shock Value Style
Duration: 15-20 seconds

[0-3s] HOOK
🎵 Trending audio
📱 Show hook frame with "GILA!"
Voice: "Gila gila gila! Kamu gak bakal percaya ini!"

[3-8s] PROBLEM
📱 Show frustration emoji/text
Voice: "Capek {product.get('pain_points', ['solusi'])[0] if product.get('pain_points') else 'mencari solusi'}?"

[8-13s] SOLUTION
📱 Show product demo/screenshots
Voice: "{name} ini jawabannya!"

[13-20s] BENEFIT + CTA
📱 Show result/price tag + Link
Voice: "Cuma {price if isinstance(price, int) else 'GRATIS'}! Link di bio, auto cuan!"
"""

    # Script 2: Problem-Solution
    script2 = f"""
VIDEO SCRIPT: {name} - Problem-Solution Style
Duration: 20-25 seconds

[0-5s] HOOK + PROBLEM
🎵 Energetic music
📱 Show "Susah banget!" text
Voice: "Sumpah susah banget {product.get('pain_points', ['cari solusi'])[0]}!"

[5-12s] AGITATION
📱 Show frustration montage
Voice: "Udah coba ini itu, tetep hasil nol capek sendiri!"

[12-18s] SOLUTION
📱 Reveal product with "AH!" moment
Voice: "Sampe nemu {name}..."
Voice: "Langsung kerja!"

[18-25s] BENEFIT + CTA
📱 Show benefit + Link
Voice: "{product.get('benefits', ['Auto result'])[0]}! Cuma {price if isinstance(price, int) else 'GRATIS'}! Link in bio!"
"""

    # Script 3: Results/Proof
    script3 = f"""
VIDEO SCRIPT: {name} - Results Style
Duration: 25-30 seconds

[0-5s] HOOK
🎵 Uplifting music
📱 Show before/after
Voice: "Before masalah, solusinya gini!"

[5-15s] STORY
📱 Show journey/process
Voice: "Dulu {product.get('pain_points', ['susah'])[0]}..."
Voice: "Lalu nemu {name}..."

[15-22s] RESULT
📱 Show positive outcome/metrics
Voice: "{product.get('benefits', ['Auto cuan'])[0]}! Langsung!"

[22-30s] CTA + URGENCY
📱 Show price + "LIMITED!" tag
Voice: "Cuma {price if isinstance(price, int) else 'GRATIS'}! Promo gilaaaa! Link in bio sekarang!"
"""

    return [
        {'style': 'shock', 'script': script1, 'duration': '15-20s'},
        {'style': 'problem', 'script': script2, 'duration': '20-25s'},
        {'style': 'results', 'script': script3, 'duration': '25-30s'}
    ]

def save_scripts(products):
    """Save all scripts to files"""
    all_scripts = []

    for product in products:
        product_id = product['id']
        name = product['name']

        print(f"📦 Creating scripts for: {name}")

        scripts = create_video_script(product)

        for script_data in scripts:
            style = script_data['style']
            script = script_data['script']

            filename = f"{product_id}_{style}_script.txt"
            filepath = OUTPUT_DIR / filename

            with open(filepath, 'w') as f:
                f.write(script)

            print(f"  ✅ Saved: {filename} ({script_data['duration']})")

            all_scripts.append({
                'product': name,
                'product_id': product_id,
                'style': style,
                'duration': script_data['duration'],
                'filename': filename,
                'path': str(filepath)
            })

    return all_scripts

def save_scripts_log(all_scripts):
    """Save scripts log"""
    log_file = OUTPUT_DIR / "scripts_log.json"

    with open(log_file, 'w') as f:
        json.dump(all_scripts, f, indent=2)

    print(f"\n📝 Scripts log saved to: {log_file}")

def main():
    print("="*60)
    print("🎬 GENERATING VIDEO SCRIPTS")
    print("="*60)
    print()

    products = load_products()
    print(f"📦 Found {len(products)} products")
    print()

    all_scripts = save_scripts(products)
    save_scripts_log(all_scripts)

    print("\n" + "="*60)
    print("✅ VIDEO SCRIPT GENERATION COMPLETE")
    print("="*60)
    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"🎬 Total scripts: {len(all_scripts)}")
    print()
    print("Next steps:")
    print("1. Record videos using these scripts")
    print("2. Or use AI video generators (CapCut, Canva)")
    print("3. Reference generated hook frames")

if __name__ == "__main__":
    main()