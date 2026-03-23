#!/usr/bin/env python3
"""
Content Scraper & Cross-Poster
- Scrape Shopee product images
- Scrape Shopee review images  
- Strip metadata for uniqueness
- Cross-post between platforms
"""

import os
import re
import json
import requests
import hashlib
from PIL import Image
from io import BytesIO
from datetime import datetime

OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/skills/shopee-affiliate-promo/media")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def strip_metadata(image_bytes):
    """Remove EXIF and other metadata from image"""
    img = Image.open(BytesIO(image_bytes))
    
    # Create new image without metadata
    data = list(img.getdata())
    img_no_meta = Image.new(img.mode, img.size)
    img_no_meta.putdata(data)
    
    # Save to bytes
    output = BytesIO()
    img_no_meta.save(output, format='JPEG', quality=92)
    return output.getvalue()

def get_shopee_product_images(product_url):
    """Extract product images from Shopee URL"""
    # Extract shop_id and item_id from URL
    # Format: shopee.co.id/product-name-i.{shop_id}.{item_id}
    match = re.search(r'i\.(\d+)\.(\d+)', product_url)
    if not match:
        # Try alternate format
        match = re.search(r'/(\d+)/(\d+)', product_url)
    
    if not match:
        return []
    
    shop_id, item_id = match.groups()
    
    # Shopee API endpoint
    api_url = f"https://shopee.co.id/api/v4/item/get?itemid={item_id}&shopid={shop_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': 'https://shopee.co.id/'
    }
    
    try:
        resp = requests.get(api_url, headers=headers, timeout=10)
        data = resp.json()
        
        if 'data' not in data:
            return []
        
        item = data['data']
        images = []
        
        # Main images
        for img_hash in item.get('images', []):
            img_url = f"https://cf.shopee.co.id/file/{img_hash}"
            images.append(img_url)
        
        return images[:5]  # Max 5 images
    except Exception as e:
        print(f"Error: {e}")
        return []

def download_and_clean(url, filename):
    """Download image, strip metadata, save locally"""
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        
        # Strip metadata
        clean_bytes = strip_metadata(resp.content)
        
        # Save
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(clean_bytes)
        
        return filepath
    except Exception as e:
        print(f"Download error: {e}")
        return None

def process_products_from_csv():
    """Process all products from CSV and download images"""
    import csv
    
    csv_path = os.path.expanduser("~/.openclaw/workspace/skills/shopee-affiliate-promo/data/holink_import.csv")
    
    results = []
    
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            link = row.get('Link Affiliate', '')
            name = row.get('Nama Produk', f'product_{i}')[:30]
            
            # Clean filename
            safe_name = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')
            
            print(f"[{i+1}] Processing: {name[:40]}...")
            
            # Try to get images
            images = get_shopee_product_images(link)
            
            if images:
                # Download first image
                img_file = download_and_clean(images[0], f"{safe_name}_{i}.jpg")
                if img_file:
                    results.append({
                        'product': name,
                        'link': link,
                        'image': img_file,
                        'source_url': images[0]
                    })
                    print(f"   ✅ Saved: {img_file}")
            else:
                print(f"   ⚠️ No images found")
            
            # Limit for testing
            if i >= 20:
                break
    
    # Save results
    results_path = os.path.join(OUTPUT_DIR, 'scraped_images.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Saved {len(results)} images")
    return results

if __name__ == "__main__":
    print("🔄 Shopee Product Image Scraper")
    print("=" * 50)
    process_products_from_csv()
