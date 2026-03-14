#!/usr/bin/env python3
"""
Gumroad → Supabase Sales Sync
Runs every hour via cron. No AI tokens wasted.

Usage:
  python3 gumroad_sync.py          # sync latest sales
  python3 gumroad_sync.py --full   # full historical sync
  python3 gumroad_sync.py --json   # print JSON summary
"""
import argparse, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from supabase import create_client

GUMROAD_TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN", "9QOi8WT_cy7icPITgcU8PvKAz-X-pOBbONyKWFb96LE")
SUPABASE_URL  = "https://juoralxnkmfrnpmkiywk.supabase.co"
SUPABASE_KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1b3JhbHhua21mcm5wbWtpeXdrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MzM5NjU0MywiZXhwIjoyMDg4OTcyNTQzfQ.ghb9G0EbaYdESNcGfvYOONuAGBtcLWOD8HMacMnLnyI"

GUMROAD_BASE  = "https://api.gumroad.com/v2"
AUTH_HEADERS  = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}


def get_products():
    r = requests.get(f"{GUMROAD_BASE}/products", headers=AUTH_HEADERS, timeout=15)
    r.raise_for_status()
    return r.json().get("products", [])


def get_sales(after=None):
    params = {}
    if after:
        params["after"] = after
    all_sales = []
    page = 1
    while True:
        params["page"] = page
        r = requests.get(f"{GUMROAD_BASE}/sales", headers=AUTH_HEADERS, params=params, timeout=15)
        if r.status_code != 200:
            break
        data = r.json()
        sales = data.get("sales", [])
        if not sales:
            break
        all_sales.extend(sales)
        page += 1
        if page > 50:  # safety limit
            break
    return all_sales


def sync_to_supabase(products, sales):
    client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Upsert products
    for p in products:
        client.table("products").upsert({
            "external_id": p["id"],
            "name": p.get("name"),
            "price_usd": p.get("price", 0) / 100,
            "sales_count": p.get("sales_count", 0),
            "platform": "gumroad",
            "url": p.get("short_url") or f"https://dizzuddi.gumroad.com/l/{p.get('custom_permalink','?')}",
        }, on_conflict="external_id").execute()

    # Upsert revenue entries for each sale
    revenue_added = 0
    for sale in sales:
        try:
            sale_date = sale.get("created_at", "")[:10]
            price_cents = sale.get("price", 0)
            price_idr = int(price_cents * 16000 / 100)  # rough USD → IDR

            client.table("revenue").upsert({
                "date": sale_date,
                "source": "gumroad",
                "amount_idr": price_idr,
                "amount_usd": price_cents / 100,
                "product_name": sale.get("product_name"),
                "external_id": sale.get("id"),
                "notes": f"Gumroad sale: {sale.get('email','?')}",
            }, on_conflict="external_id").execute()
            revenue_added += 1
        except Exception as e:
            print(f"  Skip sale {sale.get('id')}: {e}", file=sys.stderr)

    return revenue_added


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_out")
    args = parser.parse_args()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Gumroad sync starting...")

    products = get_products()
    total_sales = sum(p.get("sales_count", 0) for p in products)
    total_revenue_usd = sum(p.get("sales_count", 0) * p.get("price", 0) / 100 for p in products)

    print(f"  Products: {len(products)}")
    for p in products:
        print(f"    {p['name'][:40]} | ${p.get('price',0)/100:.2f} | {p.get('sales_count',0)} sales")

    sales = get_sales()
    print(f"  Sales fetched: {len(sales)}")

    synced = sync_to_supabase(products, sales)
    print(f"  Synced {synced} revenue records to Supabase")

    result = {
        "synced_at": datetime.now(timezone.utc).isoformat(),
        "products": len(products),
        "total_sales": total_sales,
        "total_revenue_usd": round(total_revenue_usd, 2),
        "total_revenue_idr": int(total_revenue_usd * 16000),
        "sales_fetched": len(sales),
        "supabase_synced": synced,
    }

    if total_sales == 0:
        print("  ⚠️  No sales yet")
    else:
        print(f"  💰 Total: {total_sales} sales = ${total_revenue_usd:.2f} (~IDR {result['total_revenue_idr']:,})")

    if args.json_out:
        print(json.dumps(result, indent=2))

    return result


if __name__ == "__main__":
    main()
