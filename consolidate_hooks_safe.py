#!/usr/bin/env python3
"""
Consolidate all viral TikTok hooks into master file (with error handling)
"""

import json
from pathlib import Path

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
OUTPUT_FILE = WORKSPACE / "output" / "all_viral_hooks_master.json"

# Product configurations
products = {
    "Belanja Duit Balik": {
        "file": WORKSPACE / "temp" / "viral_hooks_belanja.json",
        "price": "FREE",
        "lynk": "https://lynk.id/jendralbot/6821op5e24kn"
    },
    "Guru Pintar AI": {
        "file": WORKSPACE / "temp" / "viral_hooks_guru_pintar.json",
        "price": "IDR 75,000",
        "lynk": "https://lynk.id/jendralbot/guru-pintar-ai"
    },
    "Studio Marketplace Pro": {
        "file": WORKSPACE / "temp" / "viral_hooks_studio_marketplace.json",
        "price": "IDR 75,000",
        "lynk": "https://lynk.id/jendralbot/emne05mm7v25"
    },
    "Mesin Cetak Bisnis Kulinermu": {
        "file": WORKSPACE / "temp" / "viral_hooks_mesin_kuliner.json",
        "price": "IDR 75,000",
        "lynk": "https://lynk.id/jendralbot/mesin-cetak-bisnis-kulinermu"
    },
    "AI Content Pro Seller": {
        "file": WORKSPACE / "output" / "viral-tiktok-hooks-ai-content-pro.json",
        "price": "IDR 89,000",
        "lynk": "https://lynk.id/jendralbot/ai-content-pro-seller"
    },
    "Starter AI Content 4K": {
        "file": WORKSPACE / "viral_hooks_starter_4k.json",
        "price": "IDR 49,000",
        "lynk": "https://lynk.id/jendralbot/n2o3p4q5r6s7"
    }
}

master_data = []
total_hooks = 0

for product_name, config in products.items():
    if not config["file"].exists():
        print(f"✗ {product_name}: FILE NOT FOUND {config['file']}")
        continue

    try:
        with open(config["file"], 'r') as f:
            data = json.load(f)

        # Extract hooks (handle different formats)
        hooks = data.get("hooks", []) if "hooks" in data else data
        hook_count = len(hooks)

        master_data.append({
            "product": product_name,
            "price": config["price"],
            "lynk": config["lynk"],
            "total_hooks": hook_count,
            "hooks": hooks
        })

        total_hooks += hook_count
        print(f"✓ {product_name}: {hook_count} hooks")

    except json.JSONDecodeError as e:
        print(f"✗ {product_name}: BROKEN JSON at line {e.lineno}: {e.msg}")
        print(f"  File: {config['file']}")
    except Exception as e:
        print(f"✗ {product_name}: ERROR - {e}")

# Save master file
OUTPUT_FILE.parent.mkdir(exist_ok=True)
with open(OUTPUT_FILE, 'w') as f:
    json.dump(master_data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*50}")
print(f"TOTAL HOOKS CONSOLIDATED: {total_hooks}")
print(f"MASTER FILE: {OUTPUT_FILE}")
print(f"{'='*50}")