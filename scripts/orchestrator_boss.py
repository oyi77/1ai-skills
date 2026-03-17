#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime

STATE_FILE = "state.json"
DIRECTIVE_FILE = "DIRECTIVE.md"

def assessment_action(cmd, label):
    print(f"Executing Mitigation for {label}: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except Exception as e:
        print(f"Action failed: {e}")
        return False

def assess_kingdom():
    # ... (header same as before)
    if not os.path.exists(STATE_FILE):
        print("No state found. Run collect_business_state.py first.")
        return

    with open(STATE_FILE, 'r') as f:
        state = json.load(f)

    directives = []
    
    # 🛒 Rule 1: Marketing Push (Goal: 5000 views)
    views = state['commerce']['postbridge'].get('total_views', 0)
    if views < 5000:
        msg = f"🆘 CRITICAL: Kingdom views too low ({views}). TRIGGERING CONTENT REGENERATION."
        directives.append(msg)
        # Automatic Mitigation: generate fresh plan with killer hooks
        assessment_action("python3 scripts/jendralbot_content_generator.py", "Low Traffic")
    
    # 💰 Rule 2: Treasury Check
    balance = state['treasury'].get('bca_idr', 0)
    if balance < 1000000:
        directives.append(f"⚠️ URGENT: BCA Balance is low (IDR {balance}). Priority on high-conversion affiliate tasks.")

    # 💾 Rule 3: infra Check
    disk = state['infrastructure'].get('disk_used_pct', 0)
    if disk > 90:
        msg = f"🚨 ALERT: Disk space critical ({disk}%). TRIGGERING CLEANUP."
        directives.append(msg)
        # Automatic Mitigation: run cleanup
        assessment_action("python3 scripts/disk_cleanup_automation.py --execute", "Critical Disk")

    if directives:
        with open(DIRECTIVE_FILE, 'w') as f:
            f.write(f"# 🚩 AUTO-DIRECTIVE — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("Detected vitality issues. Orchestrate these actions immediately:\n\n")
            for d in directives:
                f.write(f"- {d}\n")
        
        print("Syncing directives to Paperclip...")
        for d in directives:
            try:
                subprocess.run(f"python3 scripts/openclaw_paperclip_bridge.py create \"{d}\"", shell=True)
            except:
                pass

        print(f"Directive generated: {len(directives)} items.")
    else:
        if os.path.exists(DIRECTIVE_FILE):
            os.remove(DIRECTIVE_FILE)
        print("Kingdom healthy. No directives needed.")

if __name__ == "__main__":
    assess_kingdom()
