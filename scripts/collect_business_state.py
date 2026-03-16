#!/usr/bin/env python3
import requests
import json
import os
import subprocess
import re
from datetime import datetime

# Configuration
POSTBRIDGE_API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
POSTBRIDGE_BASE_URL = "https://api.post-bridge.com/v1"
STATE_FILE = "state.json"

def get_postbridge_analytics():
    print("Fetching PostBridge Analytics...")
    headers = {"Authorization": f"Bearer {POSTBRIDGE_API_KEY}"}
    try:
        r = requests.get(f"{POSTBRIDGE_BASE_URL}/analytics?limit=100", headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json().get("data", [])
            total_views = sum(item.get("view_count", 0) for item in data)
            total_likes = sum(item.get("like_count", 0) for item in data)
            return {
                "total_views": total_views,
                "total_likes": total_likes,
                "post_count": len(data)
            }
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Failed to fetch"}

def get_bca_balance():
    print("Checking BCA Balance (calling bca_balance_v2.py)...")
    try:
        result = subprocess.check_output(["python3", "scripts/bca_balance_v2.py"], stderr=subprocess.STDOUT).decode()
        # Clean the whole result to find numbers
        # Format can be 1.762.179,37 or 1,762,179.37
        matches = re.findall(r"💰\s*(?:IDR\s*)?([0-9\.,]+)", result)
        if matches:
            raw = matches[-1].strip()
            # If it ends with a dot followed by 2 digits, it's US format. 
            # If it ends with a comma followed by 2 digits, it's ID format.
            if re.search(r",\d{2}$", raw):
                clean = raw.replace(".", "").replace(",", ".")
            elif re.search(r"\.\d{2}$", raw):
                clean = raw.replace(",", "")
            else:
                # No decimals, just remove all separators
                clean = raw.replace(".", "").replace(",", "")
            return float(clean)
    except Exception as e:
        print(f"BCA Parsing Error: {e} | Raw input: {matches[-1] if 'matches' in locals() and matches else 'None'}")
    return 0.0

def get_system_health():
    print("Checking System Health...")
    # Disk usage
    st = os.statvfs('/')
    free = (st.f_bavail * st.f_frsize) / (1024 * 1024 * 1024)
    total = (st.f_blocks * st.f_frsize) / (1024 * 1024 * 1024)
    used_pct = ((total - free) / total) * 100
    
    return {
        "disk_used_pct": round(used_pct, 2),
        "disk_free_gb": round(free, 2),
        "status": "HEALTHY" if used_pct < 95 else "CRITICAL"
    }

def collect_all():
    state = {
        "timestamp": datetime.now().isoformat(),
        "commerce": {
            "postbridge": get_postbridge_analytics(),
            "lynk_clicks": 0, # Placeholder until scraper integrated
            "revenue_est": 0
        },
        "treasury": {
            "bca_idr": get_bca_balance()
        },
        "infrastructure": get_system_health()
    }
    
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"State saved to {STATE_FILE}")
    return state

if __name__ == "__main__":
    collect_all()
