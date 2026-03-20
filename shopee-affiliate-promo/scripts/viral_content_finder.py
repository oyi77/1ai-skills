#!/usr/bin/env python3
"""
Viral Content Finder & Downloader for Shopee Affiliate
- Search viral videos by product keywords
- Download from TikTok, IG, YouTube, Facebook
- Filter by views/likes
- Prepare for remake
"""

import os
import json
import subprocess
import re
from datetime import datetime

BASE_DIR = os.path.expanduser("~/.openclaw/workspace/skills/shopee-affiliate-promo")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# Product keywords for searching viral content
PRODUCT_KEYWORDS = {
    'vacuum': ['vacuum cleaner viral', 'vacuum wireless tiktok', 'vacuum cordless review'],
    'sepeda_listrik': ['sepeda listrik viral', 'e-bike review indonesia', 'sepeda listrik murah'],
    'tv_smart': ['smart tv murah', 'tv android review', 'tv 4k terbaik'],
    'amplop_lebaran': ['amplop lebaran aesthetic', 'amplop thr viral', 'amplop lebaran 2026'],
    'kitchen': ['alat dapur viral', 'kitchen gadget tiktok', 'peralatan masak murah'],
    'home_decor': ['dekorasi rumah aesthetic', 'home decor viral', 'hiasan dinding murah'],
}

def search_tiktok(keyword, limit=5):
    """Search TikTok for viral videos (using web scraping approach)"""
    # TikTok search URL format
    search_url = f"https://www.tiktok.com/search/video?q={keyword.replace(' ', '%20')}"
    
    print(f"🔍 TikTok search: {keyword}")
    print(f"   URL: {search_url}")
    
    # For now, return the search URL - actual scraping needs browser
    return {'platform': 'tiktok', 'keyword': keyword, 'search_url': search_url}

def search_youtube(keyword, limit=5):
    """Search YouTube for product review videos"""
    try:
        cmd = [
            'yt-dlp',
            f'ytsearch{limit}:{keyword}',
            '--flat-playlist',
            '--dump-json',
            '--no-warnings'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    data = json.loads(line)
                    videos.append({
                        'id': data.get('id'),
                        'title': data.get('title', '')[:50],
                        'url': f"https://youtube.com/watch?v={data.get('id')}",
                        'view_count': data.get('view_count', 0),
                        'platform': 'youtube'
                    })
                except:
                    pass
        
        # Sort by views
        videos.sort(key=lambda x: x.get('view_count', 0), reverse=True)
        return videos[:limit]
    
    except Exception as e:
        print(f"   Error: {e}")
        return []

def download_video(url, output_name):
    """Download video with yt-dlp"""
    output_path = os.path.join(DOWNLOADS_DIR, f"{output_name}.mp4")
    
    cmd = [
        'yt-dlp',
        url,
        '-o', output_path,
        '-f', 'best[height<=720]',  # Max 720p for size
        '--no-playlist',
        '--quiet'
    ]
    
    try:
        subprocess.run(cmd, timeout=120, check=True)
        if os.path.exists(output_path):
            return output_path
    except Exception as e:
        print(f"   Download error: {e}")
    
    return None

def find_viral_content(category='vacuum', limit=3):
    """Find viral content for a product category"""
    keywords = PRODUCT_KEYWORDS.get(category, [f'{category} viral'])
    
    all_videos = []
    
    for keyword in keywords[:2]:  # First 2 keywords
        print(f"\n🔍 Searching: {keyword}")
        
        # YouTube search
        yt_videos = search_youtube(keyword, limit=limit)
        for v in yt_videos:
            print(f"   📺 YT: {v['title'][:40]}... ({v.get('view_count', 0):,} views)")
        all_videos.extend(yt_videos)
        
        # TikTok search (returns URL for manual/browser search)
        tt_info = search_tiktok(keyword)
    
    return all_videos

def main():
    print("=" * 60)
    print("🎬 VIRAL CONTENT FINDER - Shopee Affiliate")
    print("=" * 60)
    
    results = {}
    
    for category in ['vacuum', 'amplop_lebaran', 'kitchen']:
        print(f"\n📦 Category: {category.upper()}")
        videos = find_viral_content(category, limit=3)
        results[category] = videos
    
    # Save results
    output_file = os.path.join(BASE_DIR, 'data', 'viral_content.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Found {sum(len(v) for v in results.values())} videos")
    print(f"📁 Saved to: viral_content.json")
    
    # Download top video from each category
    print("\n📥 Downloading top videos...")
    for cat, videos in results.items():
        if videos:
            top = videos[0]
            print(f"   Downloading: {top['title'][:40]}...")
            path = download_video(top['url'], f"{cat}_top")
            if path:
                print(f"   ✅ Saved: {path}")

if __name__ == "__main__":
    main()
