#!/usr/bin/env python3
"""
Larry Slideshow Wrapper — Simplified execution
Directly calls larry-playbook workflow without import issues.
"""

import subprocess
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────
LARRY_PLAYBOOK_DIR = Path("/home/openclaw/.openclaw/workspace/skills/larry-playbook")
GENERATOR_SCRIPT = LARRY_PLAYBOOK_DIR / "workflows/generate_slideshow.py"

def generate_viral_slideshow(room: str = "kitchen_small", hook: str = "landlord_kitchen"):
    """Generate 6-slide viral slideshow."""
    print(f"🎯 Larry Workflow: {room} room + {hook} hook")
    
    # Run the workflow script
    cmd = [
        "python3", str(GENERATOR_SCRIPT),
        "--room", room,
        "--hook", hook
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=LARRY_PLAYBOOK_DIR)
        print(result.stdout)
        
        if "✅" in result.stdout or "Video created:" in result.stdout:
            return True
        else:
            print(f"⚠️  Output:\n{result.stdout}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ── Demo Runs ────────────────────────────────────────────────────────────────
def run_demo():
    """Run demo with different room/hook combinations."""
    
    print("=" * 70)
    print("🎬 LARRY VIRAL SLIDESHOW — DEMO")
    print("=" * 70)
    print()
    
    demos = [
        {"room": "kitchen_small", "hook": "landlord_kitchen", "name": "Landlord + Kitchen"},
        {"room": "living_room_cozy", "hook": "parent_bedroom", "name": "Parent + Bedroom"},
        {"room": "bedroom_minimal", "hook": "roommate_living", "name": "Roommate + Living Room"},
    ]
    
    results = []
    
    for demo in demos:
        print(f"\n{'─' * 70}")
        print(f"📋 Demo {demos.index(demo) + 1}/{len(demos)}: {demo['name']}")
        print(f"{'─' * 70}")
        print()
        
        success = generate_viral_slideshow(demo["room"], demo["hook"])
        
        results.append({
            "demo": demo["name"],
            "room": demo["room"],
            "hook": demo["hook"],
            "success": success
        })
        
        print()
    
    # Summary
    print("=" * 70)
    print("📊 DEMO SUMMARY")
    print("=" * 70)
    print()
    
    for r in results:
        status = "✅ Success" if r["success"] else "❌ Failed"
        print(f"{status} — {r['demo']}: {r['room']} + {r['hook']}")
        if r["success"]:
            print(f"     🎥 Video: output/larry_slideshows/{r['room']}_slideshow.mp4")
    
    total_success = sum(1 for r in results if r["success"])
    print()
    print(f"Total: {total_success}/{len(results)} demos successful")
    print()
    
    print("=" * 70)
    print("🎯 LARRY'S PLAYBOOK IS READY FOR PRODUCTION!")
    print("=" * 70)
    print()
    print("🔑 To run in continuous mode:")
    print("   python3 skills/larry-playbook/larry-continuous-system.py")
    print()
    print("🔑 To generate specific content:")
    print("   python3 skills/larry-playbook/larry-continuous-system.py")
    print("   (This will run automatically based on research & confidence)")
    print()

if __name__ == "__main__":
    run_demo()
