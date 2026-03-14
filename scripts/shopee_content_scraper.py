#!/usr/bin/env python3
"""
Shopee Content Scraper & Auto Poster
- Scrape product images/videos from Shopee reviews
- Create content for TikTok/IG
- Auto post to PostBridge with affiliate links
"""

import json
import os
import re
import requests
import subprocess
import time
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Config
POSTBRIDGE_API = "pb_live_AFm842jzqKVNjREpJH8hTi"
HOLINK_URL = "ho.link/racunshopeediskon"
OUTPUT_DIR = Path.home() / ".openclaw/workspace/affiliate_content/products"
PRODUCTS_FILE = Path.home() / ".openclaw/workspace/skills/shopee-affiliate-promo/data/holink_structured.json"

# Category account mapping
CATEGORY_ACCOUNTS = {
    "affiliate_shopee": [48374, 48336, 48337, 49644, 49612, 49614, 47690, 49611, 49609, 45675, 45697]
}

def load_products():
    """Load products from JSON"""
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
    return [p for p in data if p.get('type') == 'product' and p.get('url')]

def extract_shopee_id(url):
    """Extract shop_id and item_id from Shopee URL"""
    # Follow redirect to get real URL
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        final_url = r.url
        # Extract IDs from URL like /product/123/456 or /shop/123/item/456
        match = re.search(r'/product/(\d+)/(\d+)', final_url)
        if match:
            return match.group(1), match.group(2)
        match = re.search(r'i\.(\d+)\.(\d+)', final_url)
        if match:
            return match.group(1), match.group(2)
    except:
        pass
    return None, None

def create_caption(product):
    """Create viral caption for product"""
    captions = [
        f"🔥 {product['title'][:50]}...\n\n✨ Diskon GEDE!\n🛒 {HOLINK_URL}\n\n#shopee #viral #diskon #racunshopee",
        f"😱 Harga segini?! {product['title'][:40]}...\n\n💰 Buruan checkout!\n👉 {HOLINK_URL}\n\n#shopee #murah #viral",
        f"⭐ BEST SELLER! {product['title'][:40]}...\n\n📦 Ready stock\n🛒 {HOLINK_URL}\n\n#bestseller #shopee #recommended",
        f"💝 Wajib punya! {product['title'][:40]}...\n\n🔥 Promo terbatas\n👇 {HOLINK_URL}\n\n#promo #shopee #viral",
    ]
    return random.choice(captions)

def post_to_postbridge(caption, media_path=None):
    """Post content to PostBridge"""
    headers = {
        "Authorization": f"Bearer {POSTBRIDGE_API}",
        "Content-Type": "application/json"
    }
    
    now = datetime.now(timezone.utc)
    schedule_time = now + timedelta(hours=random.randint(1, 48), minutes=random.randint(0, 59))
    
    payload = {
        "caption": caption,
        "social_accounts": CATEGORY_ACCOUNTS["affiliate_shopee"],
        "scheduled_at": schedule_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    try:
        r = requests.post(
            "https://api.post-bridge.com/v1/posts",
            headers=headers,
            json=payload,
            timeout=15
        )
        return r.status_code in [200, 201]
    except:
        return False

def main():
    """Main automation loop"""
    products = load_products()
    print(f"📦 Loaded {len(products)} products")
    
    posted = 0
    failed = 0
    
    for i, product in enumerate(products[:20]):  # Process first 20 for now
        print(f"\n[{i+1}/{len(products)}] {product['title'][:50]}...")
        
        # Create caption with affiliate link context
        caption = create_caption(product)
        
        # Post to PostBridge
        if post_to_postbridge(caption):
            posted += 1
            print(f"  ✅ Posted")
        else:
            failed += 1
            print(f"  ❌ Failed")
        
        # Rate limit
        time.sleep(0.5)
    
    print(f"\n📊 Results: {posted} posted, {failed} failed")
    
    # Check total
    r = requests.get(
        "https://api.post-bridge.com/v1/posts?limit=1",
        headers={"Authorization": f"Bearer {POSTBRIDGE_API}"}
    )
    print(f"📦 Total posts: {r.json().get('meta', {}).get('total', 0)}")

if __name__ == "__main__":
    main()
