#!/usr/bin/env python3
"""
BerkahKarya Supabase Sync
Pulls data from PostBridge, LYNK, Gumroad → syncs to Supabase
Run: python3 scripts/supabase_sync.py [--full]
"""
import os, sys, json, requests
from datetime import datetime, date
from supabase import create_client

SUPABASE_URL = "https://juoralxnkmfrnpmkiywk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1b3JhbHhua21mcm5wbWtpeXdrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MzM5NjU0MywiZXhwIjoyMDg4OTcyNTQzfQ.ghb9G0EbaYdESNcGfvYOONuAGBtcLWOD8HMacMnLnyI"
PB_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
PB_BASE = "https://api.post-bridge.com/v1"

client = create_client(SUPABASE_URL, SUPABASE_KEY)

def sync_postbridge_posts():
    """Pull PostBridge posts → social_posts table"""
    print("📊 Syncing PostBridge posts...")
    headers = {"Authorization": f"Bearer {PB_KEY}"}
    resp = requests.get(f"{PB_BASE}/posts?limit=100", headers=headers, timeout=15)
    if resp.status_code != 200:
        print(f"  ❌ PostBridge error: {resp.status_code}")
        return 0
    
    posts = resp.json().get("data", [])
    synced = 0
    for p in posts:
        # Map platform from social account
        platform = p.get("platform", "unknown")
        row = {
            "postbridge_id": p.get("id"),
            "platform": platform,
            "caption": p.get("caption", "")[:500] if p.get("caption") else None,
            "status": p.get("status", "draft"),
            "scheduled_at": p.get("scheduled_at"),
            "posted_at": p.get("published_at"),
        }
        try:
            client.table("social_posts").upsert(row, on_conflict="postbridge_id").execute()
            synced += 1
        except Exception as e:
            print(f"  ⚠ Skip {p.get('id','?')[:8]}: {e}")
    
    print(f"  ✅ Synced {synced}/{len(posts)} posts")
    return synced

def sync_postbridge_analytics():
    """Pull analytics → update social_posts views/likes/comments"""
    print("📈 Syncing PostBridge analytics...")
    headers = {"Authorization": f"Bearer {PB_KEY}"}
    try:
        resp = requests.get(f"{PB_BASE}/analytics", headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json().get("data", [])
            updated = 0
            for item in data:
                pb_id = item.get("post_id")
                if pb_id:
                    client.table("social_posts").update({
                        "views": item.get("views", 0),
                        "likes": item.get("likes", 0),
                        "comments": item.get("comments", 0),
                        "shares": item.get("shares", 0),
                    }).eq("postbridge_id", pb_id).execute()
                    updated += 1
            print(f"  ✅ Updated {updated} post analytics")
    except Exception as e:
        print(f"  ⚠ Analytics sync failed: {e}")

def record_cashflow_snapshot(bank_balance_idr=0, revenue_idr=0, expenses_idr=0, notes=""):
    """Record daily cashflow snapshot"""
    today = date.today().isoformat()
    burn_rate = expenses_idr if expenses_idr > 0 else 150000  # default 150K/day estimate
    runway = bank_balance_idr // burn_rate if burn_rate > 0 else 0
    
    row = {
        "date": today,
        "bank_balance_idr": bank_balance_idr,
        "revenue_today_idr": revenue_idr,
        "expenses_today_idr": expenses_idr,
        "burn_rate_daily_idr": burn_rate,
        "runway_days": runway,
        "notes": notes,
    }
    try:
        client.table("cashflow").upsert(row, on_conflict="date").execute()
        print(f"  ✅ Cashflow snapshot: IDR {bank_balance_idr:,} balance, {runway} days runway")
    except Exception as e:
        print(f"  ❌ Cashflow error: {e}")

def record_revenue(source, amount_idr, description="", platform=None, amount_usd=0):
    """Log a revenue entry"""
    row = {
        "date": date.today().isoformat(),
        "source": source,
        "amount_idr": amount_idr,
        "amount_usd": amount_usd,
        "description": description,
        "platform": platform,
    }
    try:
        client.table("revenue").insert(row).execute()
        print(f"  ✅ Revenue logged: {source} IDR {amount_idr:,}")
    except Exception as e:
        print(f"  ❌ Revenue error: {e}")

def get_dashboard():
    """Print current dashboard summary"""
    print("\n📊 === BERKAHKARYA DASHBOARD ===")
    today = date.today().isoformat()
    
    # Today's revenue
    rev = client.table("revenue").select("*").gte("date", today).execute()
    total_rev = sum(r.get("amount_idr", 0) for r in rev.data)
    print(f"  Today's Revenue: IDR {total_rev:,}")
    
    # Posts
    posts = client.table("social_posts").select("status").execute()
    status_count = {}
    for p in posts.data:
        s = p["status"]
        status_count[s] = status_count.get(s, 0) + 1
    print(f"  Posts: {status_count}")
    
    # Talents
    talents = client.table("talents").select("status").execute()
    print(f"  Talents: {len(talents.data)} total")
    
    # Clients
    clients_data = client.table("clients").select("status").execute()
    print(f"  Clients: {len(clients_data.data)} total")
    
    # Latest cashflow
    cf = client.table("cashflow").select("*").order("date", desc=True).limit(1).execute()
    if cf.data:
        c = cf.data[0]
        print(f"  Bank Balance: IDR {c.get('bank_balance_idr',0):,} | Runway: {c.get('runway_days',0)} days")
    print("================================\n")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "sync"
    
    if mode == "sync" or mode == "--full":
        sync_postbridge_posts()
        sync_postbridge_analytics()
        get_dashboard()
    elif mode == "dashboard":
        get_dashboard()
    else:
        print(f"Usage: python3 supabase_sync.py [sync|dashboard|--full]")
