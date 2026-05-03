#!/usr/bin/env python3
"""
PostBridge Smart Post Creator
Validates and creates posts with automatic error prevention.

Usage:
  python3 postbridge_smart_post.py --caption "..." --accounts tiktok,instagram --media /path/to/video.mp4
  python3 postbridge_smart_post.py --caption "..." --accounts all_tiktok --text-only-fallback
  python3 postbridge_smart_post.py --dry-run --caption "..." --accounts tiktok
"""

import urllib.request, json, os, sys, argparse, time
from datetime import datetime, timezone, timedelta

API_BASE = 'https://api.post-bridge.com/v1'
API_KEY = os.environ.get('PB_API_KEY', 'REDACTED_POSTBRIDGE_KEY')
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}

# Platforms that REQUIRE media
MEDIA_REQUIRED = {'tiktok', 'instagram', 'youtube'}
# Platforms that need VIDEO specifically
VIDEO_REQUIRED = {'youtube'}
# Platforms that accept text-only
TEXT_OK = {'facebook', 'threads', 'twitter', 'linkedin', 'bluesky', 'pinterest'}

# Known TikTok account IDs (BerkahKarya)
TIKTOK_ACCOUNTS = [48335, 48336, 48337, 48338, 48372, 48373, 48374, 49642, 49659, 49663]
INSTAGRAM_ACCOUNTS = [49682, 49676, 49810]  # known IG accounts


def pb_get(ep):
    req = urllib.request.Request(f'{API_BASE}{ep}', headers=HEADERS)
    try:
        return json.loads(urllib.request.urlopen(req, timeout=20).read())
    except Exception as e:
        return {'error': str(e)}


def pb_post(ep, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(f'{API_BASE}{ep}', data=body, headers=HEADERS, method='POST')
    try:
        return json.loads(urllib.request.urlopen(req, timeout=20).read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        return {'error': e.code, 'message': err_body}


def get_all_accounts():
    """Fetch all accounts, return as dict id→account."""
    d = pb_get('/social-accounts?limit=100')
    return {a['id']: a for a in d.get('data', [])}


def validate_media(media_id):
    """Check if media is accessible."""
    d = pb_get(f'/media/{media_id}')
    obj = d.get('object', {})
    if obj.get('isDeleted'):
        return False, 'DELETED — media was removed from PostBridge storage'
    if not obj.get('url'):
        return False, 'NO_URL — media may still be processing'
    mime = d.get('mime_type', '')
    return True, mime


def upload_media(filepath):
    """Upload a media file to PostBridge."""
    if not os.path.exists(filepath):
        print(f'❌ File not found: {filepath}')
        return None

    ext = filepath.rsplit('.', 1)[-1].lower()
    mime_map = {
        'mp4': 'video/mp4', 'mov': 'video/quicktime', 'avi': 'video/avi',
        'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png',
        'gif': 'image/gif', 'webp': 'image/webp'
    }
    mime = mime_map.get(ext, 'application/octet-stream')
    size = os.path.getsize(filepath)

    print(f'📤 Uploading {os.path.basename(filepath)} ({mime}, {size:,} bytes)...')

    # Get signed upload URL
    resp = pb_post('/media/create-upload-url', {'mime_type': mime, 'file_size': size})
    if 'error' in resp:
        print(f'❌ Failed to get upload URL: {resp}')
        return None

    upload_url = resp.get('upload_url')
    media_id = resp.get('id')

    if not upload_url:
        print(f'❌ No upload URL in response: {resp}')
        return None

    # Upload to S3
    with open(filepath, 'rb') as f:
        data = f.read()
    req = urllib.request.Request(upload_url, data=data, method='PUT',
                                  headers={'Content-Type': mime})
    urllib.request.urlopen(req, timeout=120)

    print(f'✅ Uploaded! media_id: {media_id}')
    return media_id


def filter_accounts_for_post(account_ids, accounts_map, has_media, media_mime=None):
    """
    Filter accounts based on media availability.
    Returns (valid_accounts, removed_accounts, warnings)
    """
    valid = []
    removed = []
    warnings = []

    is_video = media_mime and media_mime.startswith('video/')
    is_image = media_mime and media_mime.startswith('image/')

    for acc_id in account_ids:
        acc = accounts_map.get(acc_id, {})
        platform = acc.get('platform', '').lower()
        username = acc.get('username', str(acc_id))

        # Check media requirements
        if platform in MEDIA_REQUIRED and not has_media:
            removed.append(acc_id)
            warnings.append(f'⚠️  Removed @{username} ({platform}) — requires media, got text-only')
            continue

        if platform in VIDEO_REQUIRED and has_media and not is_video:
            removed.append(acc_id)
            warnings.append(f'⚠️  Removed @{username} ({platform}) — requires VIDEO, got {media_mime}')
            continue

        valid.append(acc_id)

    return valid, removed, warnings


def create_post(caption, account_ids, media_ids=None, scheduled_at=None,
                dry_run=False, verbose=True):
    """
    Create a validated post with error prevention.

    Returns: (success, post_id_or_error, warnings)
    """
    accounts_map = get_all_accounts()
    warnings = []
    errors = []

    # Validate media
    has_media = bool(media_ids)
    media_mime = None
    valid_media_ids = []

    for mid in (media_ids or []):
        ok, info = validate_media(mid)
        if ok:
            valid_media_ids.append(mid)
            media_mime = info  # mime type
        else:
            errors.append(f'❌ Media {mid}: {info}')

    if media_ids and not valid_media_ids:
        return False, 'All media files are invalid/deleted', errors

    if media_ids and len(valid_media_ids) < len(media_ids):
        warnings.append(f'⚠️  {len(media_ids) - len(valid_media_ids)} media files skipped (invalid)')

    # Filter accounts based on media
    valid_accounts, removed_accounts, filter_warnings = filter_accounts_for_post(
        account_ids, accounts_map, bool(valid_media_ids), media_mime
    )
    warnings.extend(filter_warnings)

    if not valid_accounts:
        return False, 'No valid accounts after filtering', warnings

    # Build post payload
    payload = {
        'caption': caption,
        'social_accounts': valid_accounts,
    }

    if valid_media_ids:
        payload['media'] = [{'id': mid} for mid in valid_media_ids]

    if scheduled_at:
        payload['scheduled_at'] = scheduled_at
    else:
        # Default: post in 5 minutes
        future = datetime.now(timezone.utc) + timedelta(minutes=5)
        payload['scheduled_at'] = future.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Show preview
    if verbose:
        print('\n📝 POST PREVIEW:')
        print(f'   Caption: {caption[:100]}...' if len(caption) > 100 else f'   Caption: {caption}')
        print(f'   Accounts: {len(valid_accounts)} ({len(removed_accounts)} removed)')
        print(f'   Media: {len(valid_media_ids)} files')
        print(f'   Scheduled: {payload["scheduled_at"]}')
        if warnings:
            print('\n⚠️  WARNINGS:')
            for w in warnings:
                print(f'   {w}')

    if dry_run:
        print('\n🔍 DRY RUN — post not created')
        print(f'   Would post to {len(valid_accounts)} accounts')
        return True, 'DRY_RUN', warnings

    # Create post
    if verbose:
        print('\n🚀 Creating post...')

    resp = pb_post('/posts', payload)

    if 'error' in resp or 'id' not in resp:
        return False, f'API error: {resp}', warnings

    post_id = resp['id']
    if verbose:
        print(f'✅ Post created! ID: {post_id}')

    return True, post_id, warnings


def post_to_all_tiktok(caption, media_filepath=None, scheduled_at=None, dry_run=False):
    """Quick helper: post to all 10 TikTok accounts."""
    media_ids = []
    if media_filepath:
        mid = upload_media(media_filepath)
        if not mid:
            print('❌ Media upload failed')
            return False
        media_ids = [mid]
    elif not media_filepath:
        print('⚠️  No media provided — TikTok requires media. Post will fail!')
        print('   Pass --media <filepath> to include media.')
        return False

    success, result, warnings = create_post(
        caption=caption,
        account_ids=TIKTOK_ACCOUNTS,
        media_ids=media_ids,
        scheduled_at=scheduled_at,
        dry_run=dry_run,
    )
    return success


def post_to_text_platforms(caption, scheduled_at=None, dry_run=False):
    """Post text-only to FB/Threads/Twitter/LinkedIn."""
    accounts_map = get_all_accounts()
    text_account_ids = [
        aid for aid, acc in accounts_map.items()
        if acc.get('platform', '').lower() in TEXT_OK
    ]

    print(f'📢 Posting text to {len(text_account_ids)} accounts (FB/Threads/Twitter/LinkedIn)')

    success, result, warnings = create_post(
        caption=caption,
        account_ids=text_account_ids,
        media_ids=None,
        scheduled_at=scheduled_at,
        dry_run=dry_run,
    )
    return success


def main():
    parser = argparse.ArgumentParser(description='PostBridge Smart Post Creator')
    parser.add_argument('--caption', type=str, help='Post caption')
    parser.add_argument('--caption-file', type=str, help='Read caption from file')
    parser.add_argument('--media', type=str, help='Path to media file to upload')
    parser.add_argument('--media-id', type=str, help='Existing PostBridge media ID')
    parser.add_argument('--accounts', type=str, default='all_tiktok',
                        help='Comma-separated account IDs, or: all_tiktok, all_text, all')
    parser.add_argument('--scheduled-at', type=str, help='ISO datetime UTC (e.g. 2026-03-22T08:00:00Z)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without creating')
    parser.add_argument('--delay-minutes', type=int, default=5,
                        help='Minutes from now to schedule (default 5)')
    args = parser.parse_args()

    # Get caption
    caption = args.caption
    if args.caption_file:
        with open(args.caption_file) as f:
            caption = f.read().strip()
    if not caption:
        print('❌ --caption or --caption-file required')
        sys.exit(1)

    # Get media
    media_ids = []
    if args.media:
        mid = upload_media(args.media)
        if not mid:
            sys.exit(1)
        media_ids = [mid]
    elif args.media_id:
        media_ids = [args.media_id]

    # Get accounts
    accounts_map = get_all_accounts()
    if args.accounts == 'all_tiktok':
        account_ids = [aid for aid, a in accounts_map.items() if a['platform'] == 'tiktok']
    elif args.accounts == 'all_text':
        account_ids = [aid for aid, a in accounts_map.items() if a['platform'] in TEXT_OK]
    elif args.accounts == 'all':
        account_ids = list(accounts_map.keys())
    else:
        account_ids = [int(x.strip()) for x in args.accounts.split(',') if x.strip()]

    # Scheduled at
    scheduled_at = args.scheduled_at
    if not scheduled_at:
        future = datetime.now(timezone.utc) + timedelta(minutes=args.delay_minutes)
        scheduled_at = future.strftime('%Y-%m-%dT%H:%M:%SZ')

    success, result, warnings = create_post(
        caption=caption,
        account_ids=account_ids,
        media_ids=media_ids or None,
        scheduled_at=scheduled_at,
        dry_run=args.dry_run,
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
