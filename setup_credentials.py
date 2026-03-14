#!/usr/bin/env python3
"""
Setup Secure Credentials Storage for Social Media Automation
Uses encryption for sensitive data
"""

import json
import getpass
from pathlib import Path
import base64
from cryptography.fernet import Fernet

CREDENTIALS_DIR = Path("/home/openclaw/.openclaw/workspace/.secrets")
CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)

KEY_FILE = CREDENTIALS_DIR / "encryption.key"
CREDENTIALS_FILE = CREDENTIALS_DIR / "credentials.enc"

def generate_key():
    """Generate encryption key"""
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key

def load_key():
    """Load or create encryption key"""
    if KEY_FILE.exists():
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    else:
        return generate_key()

def encrypt_data(data, key):
    """Encrypt credentials"""
    fernet = Fernet(key)
    json_data = json.dumps(data).encode()
    encrypted = fernet.encrypt(json_data)
    return encrypted

def decrypt_data(encrypted_data, key):
    """Decrypt credentials"""
    fernet = Fernet(key)
    json_data = fernet.decrypt(encrypted_data).decode()
    return json.loads(json_data)

def collect_credentials():
    """Collect credentials from user"""
    credentials = {}

    print("="*60)
    print("🔐 SOCIAL MEDIA CREDENTIALS SETUP")
    print("="*60)
    print()
    print("This will setup secure storage for your social media accounts.")
    print("All data will be encrypted and stored locally.")
    print()

    # TikTok
    print("📱 TikTok")
    tiktok_username = input("  Username: ").strip()
    tiktok_password = getpass.getpass("  Password: ")
    credentials['tiktok'] = {
        'username': tiktok_username,
        'password': tiktok_password,
        'platform': 'tiktok'
    }
    print("  ✅ TikTok credentials saved\n")

    # Instagram
    print("📸 Instagram")
    instagram_username = input("  Username: ").strip()
    instagram_password = getpass.getpass("  Password: ")
    credentials['instagram'] = {
        'username': instagram_username,
        'password': instagram_password,
        'platform': 'instagram'
    }
    print("  ✅ Instagram credentials saved\n")

    # Facebook - ask for page URL instead of direct login
    print("📘 Facebook")
    fb_page_url = input("  Page URL: ").strip()
    fb_access_token = getpass.getpass("  Access Token (optional): ")
    credentials['facebook'] = {
        'page_url': fb_page_url,
        'access_token': fb_access_token if fb_access_token else '',
        'platform': 'facebook'
    }
    print("  ✅ Facebook credentials saved\n")

    # Twitter/X
    print("🐦 Twitter/X")
    tw_api_key = input("  API Key: ").strip()
    tw_api_secret = input("  API Secret: ").strip()
    tw_access_token = input("  Access Token: ").strip()
    tw_access_secret = input("  Access Token Secret: ").strip()
    credentials['twitter'] = {
        'api_key': tw_api_key,
        'api_secret': tw_api_secret,
        'access_token': tw_access_token,
        'access_secret': tw_access_secret,
        'platform': 'twitter'
    }
    print("  ✅ Twitter credentials saved\n")

    # YouTube
    print("▶️ YouTube")
    yt_channel_id = input("  Channel ID: ").strip()
    yt_client_id = input("  Client ID: ").strip()
    yt_client_secret = getpass.getpass("  Client Secret: ")
    credentials['youtube'] = {
        'channel_id': yt_channel_id,
        'client_id': yt_client_id,
        'client_secret': yt_client_secret,
        'platform': 'youtube'
    }
    print("  ✅ YouTube credentials saved\n")

    # PostBridge
    print("🌉 PostBridge")
    pb_api_key = input("  API Key (pb_live_xxx): ").strip()
    credentials['postbridge'] = {
        'api_key': pb_api_key,
        'base_url': 'https://api.post-bridge.com/v1',
        'platform': 'postbridge'
    }
    print("  ✅ PostBridge credentials saved\n")

    # LYNK
    print("🔗 LYNK Tracking")
    lynk_base_url = input("  Base URL (default: https://lynk.id/jendralbot): ").strip()
    credentials['lynk'] = {
        'base_url': lynk_base_url if lynk_base_url else 'https://lynk.id/jendralbot',
        'platform': 'lynk'
    }
    print("  ✅ LYNK credentials saved\n")

    return credentials

def save_credentials(credentials, key):
    """Save encrypted credentials"""
    encrypted = encrypt_data(credentials, key)
    with open(CREDENTIALS_FILE, 'wb') as f:
        f.write(encrypted)
    print(f"✅ Encrypted credentials saved to: {CREDENTIALS_FILE}")

def test_credentials(credentials):
    """Test if credentials are valid"""
    print("\n" + "="*60)
    print("🧪 CREDENTIALS VALIDATION")
    print("="*60)
    print()

    for platform, data in credentials.items():
        print(f"📱 {platform.upper()}")
        required_fields = {
            'tiktok': ['username', 'password'],
            'instagram': ['username', 'password'],
            'facebook': ['page_url'],
            'twitter': ['api_key', 'api_secret', 'access_token', 'access_secret'],
            'youtube': ['channel_id', 'client_id', 'client_secret'],
            'postbridge': ['api_key'],
            'lynk': ['base_url']
        }

        for field in required_fields.get(platform, []):
            if field in data and data[field]:
                print(f"  ✅ {field}: Set")
            else:
                print(f"  ⚠️  {field}: Missing (optional)")
        print()

def create_credentials_summary():
    """Create a README about credentials"""
    readme = CREDENTIALS_DIR / "README.md"

    content = """#🔐 Social Media Credentials

This directory contains encrypted credentials for social media automation.

## Files

- `encryption.key` - Encryption key (DO NOT SHARE)
- `credentials.enc` - Encrypted credentials file
- `README.md` - This file

## Platforms

Currently configured:
- 📱 TikTok
- 📸 Instagram
- 📘 Facebook
- 🐦 Twitter/X
- ▶️ YouTube
- 🌉 PostBridge
- 🔗 LYNK

## Security

- All passwords are encrypted using Fernet symmetric encryption
- Encryption key stored separately
- Never commit .enc files to version control
- Add this directory to .gitignore

## Usage

```python
from cryptography.fernet import Fernet

# Load key
with open('encryption.key', 'rb') as f:
    key = f.read()

# Load and decrypt credentials
with open('credentials.enc', 'rb') as f:
    encrypted = f.read()

fernet = Fernet(key)
decrypted = fernet.decrypt(encrypted).decode()
credentials = json.loads(decrypted)

# Use credentials
tiktok_username = credentials['tiktok']['username']
```

## Regenerating Credentials

To update or reset credentials:
```bash
python setup_credentials.py
```

## Backup

Backup both `encryption.key` and `credentials.enc` to a secure location.
"""

    with open(readme, 'w') as f:
        f.write(content)

    print(f"📝 Created README: {readme}")

def main():
    print("="*60)
    print("🔐 SECURE CREDENTIALS SETUP")
    print("="*60)
    print()

    # Load or create encryption key
    key = load_key()
    print("✅ Encryption key ready\n")

    # Check if credentials already exist
    if CREDENTIALS_FILE.exists():
        print("⚠️  Credentials file already exists!")
        overwrite = input("Overwrite? (no): ").strip().lower()
        if overwrite != 'yes':
            print("❌ Setup cancelled")
            return

    # Collect credentials
    credentials = collect_credentials()

    # Save credentials
    save_credentials(credentials, key)

    # Test credentials
    test_credentials(credentials)

    # Create README
    create_credentials_summary()

    print("="*60)
    print("✅ CREDENTIALS SETUP COMPLETE")
    print("="*60)
    print()
    print("📁 Credentials directory: {CREDENTIALS_DIR}")
    print("🔒 All data encrypted")
    print()
    print("Next steps:")
    print("1. Backup encryption.key and credentials.enc")
    print("2. Run test automation to verify connections")
    print("3. Start posting using automation scripts")

if __name__ == "__main__":
    main()