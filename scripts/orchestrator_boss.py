#!/usr/bin/env python3
import json
import os
from datetime import datetime

STATE_FILE = "state.json"
DIRECTIVE_FILE = "DIRECTIVE.md"

def assess_kingdom():
    if not os.path.exists(STATE_FILE):
        print("No state found. Run collect_business_state.py first.")
        return

    with open(STATE_FILE, 'r') as f:
        state = json.load(f)

    directives = []
    
    # 🛒 Rule 1: Marketing Push
    views = state['commerce']['postbridge'].get('total_views', 0)
    if views < 5000:
        directives.append(f"🆘 CRITICAL: Kingdom views too low ({views}). Spawn Content Agent to generate 20 more viral hooks immediately.")
    
    # 💰 Rule 2: Treasury Check
    balance = state['treasury'].get('bca_idr', 0)
    if balance < 1000000:
        directives.append(f"⚠️ URGENT: BCA Balance is low (IDR {balance}). Priority on high-conversion affiliate tasks.")

    # 💾 Rule 3: infra Check
    disk = state['infrastructure'].get('disk_used_pct', 0)
    if disk > 90:
        directives.append(f"🚨 ALERT: Disk space critical ({disk}%). RUN disk_cleanup_automation.py now.")

    if directives:
        with open(DIRECTIVE_FILE, 'w') as f:
            f.write(f"# 🚩 AUTO-DIRECTIVE — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("Detected vitality issues. Orchestrate these actions immediately:\n\n")
            for d in directives:
                f.write(f"- {d}\n")
        print(f"Directive generated: {len(directives)} items.")
    else:
        if os.path.exists(DIRECTIVE_FILE):
            os.remove(DIRECTIVE_FILE)
        print("Kingdom healthy. No directives needed.")

if __name__ == "__main__":
    assess_kingdom()
