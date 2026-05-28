#!/usr/bin/env python3
"""
Remotion Batch Renderer - Render multiple animations

Usage:
    python3 batch_render.py --config <config.json> --parallel <count>

Author: Vilona (BerkahKarya AI)
Date: 2026-03-17
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import concurrent.futures

# Remotion project directory
REMOTION_PROJECT = Path.home() / ".openclaw" / "workspace" / "remotion-project"

# Output directory
OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "output" / "remotion_videos"

def render_animation(animation_config, output_path):
    """Render single animation"""
    
    composition_name = animation_config.get("template", "default")
    
    # Create config JSON
    config_path = REMOTION_PROJECT / f"config_{composition_name}.json"
    with open(config_path, 'w') as f:
        json.dump(animation_config, f, indent=2)
    
    # Run Remotion render command
    cmd = [
        "npx", "remotion", "render", composition_name,
        "--config", str(REMOTION_PROJECT / "remotion.config.js"),
        "--output", str(output_path)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            cwd=REMOTION_PROJECT,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max per render
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "composition": composition_name,
                "output": str(output_path),
                "duration": animation_config.get("duration", 0)
            }
        else:
            return {
                "success": False,
                "composition": composition_name,
                "error": result.stderr,
                "returncode": result.returncode
            }
    
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "composition": composition_name,
            "error": "Timeout (5 minutes exceeded)"
        }
    except Exception as e:
        return {
            "success": False,
            "composition": composition_name,
            "error": str(e)
        }

def batch_render(config_path, parallel=1):
    """Batch render multiple animations"""
    
    # Load batch config
    with open(config_path, 'r') as f:
        batch_config = json.load(f)
    
    animations = batch_config.get("animations", [])
    
    if not animations:
        print("❌ No animations found in config")
        return
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"🎬 Batch Rendering {len(animations)} animations")
    print(f"   Parallel: {parallel}")
    print(f"   Output: {OUTPUT_DIR}")
    print()
    
    # Render animations
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = {}
        
        for i, animation in enumerate(animations):
            output_path = OUTPUT_DIR / f"animation_{i:03d}.mp4"
            future = executor.submit(render_animation, animation, output_path)
            futures[future] = animation
        
        # Collect results
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            
            if result["success"]:
                print(f"  ✅ {result['composition']} → {result['output']}")
            else:
                print(f"  ❌ {result['composition']} → {result.get('error', 'Unknown error')}")
    
    # Summary
    success_count = sum(1 for r in results if r["success"])
    failed_count = len(results) - success_count
    
    print()
    print("="*70)
    print("📊 BATCH RENDER SUMMARY")
    print("="*70)
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📈 Success Rate: {round(success_count/len(results)*100, 1)}%")
    print(f"⏱️ Total Time: Varies by animation length")
    print(f"📂 Output: {OUTPUT_DIR}")

def main():
    """Main entry point"""
    
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nBatch config format:")
        print(json.dumps({
            "animations": [
                {
                    "type": "kinetic_typo",
                    "template": "scale-in",
                    "text": "Hello World",
                    "duration": 3
                },
                {
                    "type": "data_viz",
                    "animation": "counter",
                    "start": 0,
                    "end": 10000,
                    "duration": 5
                }
            ]
        }, indent=2))
        sys.exit(1)
    
    # Parse arguments
    config_path = None
    parallel = 1
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "--config" and i + 1 < len(sys.argv):
            config_path = sys.argv[i + 1]
            i += 2
        elif arg == "--parallel" and i + 1 < len(sys.argv):
            parallel = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1
    
    if not config_path:
        print("❌ --config is required")
        sys.exit(1)
    
    if not Path(config_path).exists():
        print(f"❌ Config file not found: {config_path}")
        sys.exit(1)
    
    # Run batch render
    batch_render(config_path, parallel)

if __name__ == "__main__":
    main()
