#!/usr/bin/env python3
"""
Simple Credentials Setup - No Encryption Required
For immediate testing and setup
"""

import json
from pathlib import Path
import os

CREDENTIALS_DIR = Path("/home/openclaw/.openclaw/workspace/.secrets")
CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)

CREDENTIALS_FILE = CREDENTIALS_DIR / "credentials.json"

def collect_credentials():
    """Collect credentials from environment or user input"""
    credentials = {}

    print("="*60)
    print("🔐 CREDENTIALS SETUP (SIMPLE MODE)")
    print("="*60)
    print()
    print("Checking environment variables...\n")

    # TikTok
    tiktok_username = os.getenv('TIKTOK_USERNAME')
    tiktok_password = os.getenv('TIKTOK_PASSWORD')

    if tiktok_username and tiktok_password:
        print("📱 TikTok: Found in environment variables")
        credentials['tiktok'] = {
            'username': tiktok_username,
            'password': tiktok_password,
            'platform': 'tiktok'
        }
    else:
        print("📱 TikTok: Not set in environment")
        credentials['tiktok'] = {
            'username': '',
            'password': '',
            'platform': 'tiktok',
            'note': 'Set TIKTOK_USERNAME and TIKTOK_PASSWORD environment variables'
        }

    # Instagram
    instagram_username = os.getenv('INSTAGRAM_USERNAME')
    instagram_password = os.getenv('INSTAGRAM_PASSWORD')

    if instagram_username and instagram_password:
        print("📸 Instagram: Found in environment variables")
        credentials['instagram'] = {
            'username': instagram_username,
            'password': instagram_password,
            'platform': 'instagram'
        }
    else:
        print("📸 Instagram: Not set in environment")
        credentials['instagram'] = {
            'username': '',
            'password': '',
            'platform': 'instagram',
            'note': 'Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables'
        }

    # Facebook
    fb_page_url = os.getenv('FACEBOOK_PAGE_URL')
    fb_access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')

    if fb_page_url or fb_access_token:
        print("📘 Facebook: Found in environment variables")
        credentials['facebook'] = {
            'page_url': fb_page_url or '',
            'access_token': fb_access_token or '',
            'platform': 'facebook'
        }
    else:
        print("📘 Facebook: Not set in environment")
        credentials['facebook'] = {
            'page_url': '',
            'access_token': '',
            'platform': 'facebook',
            'note': 'Set FACEBOOK_PAGE_URL and FACEBOOK_ACCESS_TOKEN environment variables'
        }

    # PostBridge
    pb_api_key = os.getenv('POSTBRIDGE_API_KEY')

    if pb_api_key:
        print("🌉 PostBridge: Found in environment variables")
        credentials['postbridge'] = {
            'api_key': pb_api_key,
            'base_url': 'https://api.post-bridge.com/v1',
            'platform': 'postbridge'
        }
    else:
        print("🌉 PostBridge: Not set in environment")
        credentials['postbridge'] = {
            'api_key': 'pb_live_AFm842jzqKVNjREpJH8hTi',  # Default from MOVA campaign
            'base_url': 'https://api.post-bridge.com/v1',
            'platform': 'postbridge',
            'note': 'Set POSTBRIDGE_API_KEY environment variable'
        }

    # Twitter
    tw_api_key = os.getenv('TWITTER_API_KEY')
    tw_api_secret = os.getenv('TWITTER_API_SECRET')
    tw_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    tw_access_secret = os.getenv('TWITTER_ACCESS_SECRET')

    if all([tw_api_key, tw_api_secret]):
        print("🐦 Twitter: Found in environment variables")
        credentials['twitter'] = {
            'api_key': tw_api_key,
            'api_secret': tw_api_secret,
            'access_token': tw_access_token or '',
            'access_secret': tw_access_secret or '',
            'platform': 'twitter'
        }
    else:
        print("🐦 Twitter: Not set in environment")
        credentials['twitter'] = {
            'api_key': '',
            'api_secret': '',
            'access_token': '',
            'access_secret': '',
            'platform': 'twitter',
            'note': 'Set TWITTER_API_KEY and TWITTER_API_SECRET environment variables'
        }

    # YouTube
    yt_channel_id = os.getenv('YOUTUBE_CHANNEL_ID')
    yt_client_id = os.getenv('YOUTUBE_CLIENT_ID')
    yt_client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')

    if all([yt_channel_id, yt_client_id]):
        print("▶️ YouTube: Found in environment variables")
        credentials['youtube'] = {
            'channel_id': yt_channel_id,
            'client_id': yt_client_id,
            'client_secret': yt_client_secret or '',
            'platform': 'youtube'
        }
    else:
        print("▶️ YouTube: Not set in environment")
        credentials['youtube'] = {
            'channel_id': '',
            'client_id': '',
            'client_secret': '',
            'platform': 'youtube',
            'note': 'Set YOUTUBE_CHANNEL_ID and YOUTUBE_CLIENT_ID environment variables'
        }

    return credentials

def save_credentials(credentials):
    """Save credentials to file"""
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f, indent=2)
    print(f"\n✅ Credentials saved to: {CREDENTIALS_FILE}")

def create_env_template():
    """Create .env template file"""
    env_file = CREDENTIALS_DIR / ".env.template"

    template = """
# Social Media Credentials Setup
# Copy this file to .env and fill in your credentials

# TikTok
TIKTOK_USERNAME=your_tiktok_username
TIKTOK_PASSWORD=your_tiktok_password

# Instagram
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# Facebook
FACEBOOK_PAGE_URL=https://facebook.com/your-page
FACEBOOK_ACCESS_TOKEN=your_access_token

# Twitter/X
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret

# YouTube
YOUTUBE_CHANNEL_ID=your_channel_id
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret

# PostBridge
POSTBRIDGE_API_KEY=pb_live_your_api_key
"""

    with open(env_file, 'w') as f:
        f.write(template)

    print(f"📝 Created .env template: {env_file}")

def main():
    print("="*60)
    print("🔐 SIMPLE CREDENTIALS SETUP")
    print("="*60)
    print()

    credentials = collect_credentials()

    save_credentials(credentials)
    create_env_template()

    print("\n" + "="*60)
    print("ℹ️  SETUP INSTRUCTIONS")
    print("="*60)
    print()
    print("To set your credentials:")
    print()
    print("Option 1 - Environment Variables (Recommended):")
    print("  1. Copy .env.template to .env")
    print("  2. Fill in your credentials")
    print("  3. Run: source .env (before running scripts)")
    print()
    print("Option 2 - Direct File Edit:")
    print("  1. Edit: credentials.json")
    print("  2. Add your credentials")
    print("  3. Save the file")
    print()
    print("Option 3 - Interactive Setup:")
    print("  1. Run: python setup_credentials.py (with encryption)")
    print()
    print("⚠️  Security Note:")
    print("  - Never commit credentials to Git")
    print("  - Add .secrets/ to .gitignore")
    print("  - Use environment variables in production")

if __name__ == "__main__":
    main()