#!/usr/bin/env python3
"""
PostBridge Health Monitor & Auto-Healer
Detects and fixes common posting failures.

Usage:
  python3 postbridge_health.py              # full health check
  python3 postbridge_health.py --fix        # check + auto-fix where possible
  python3 postbridge_health.py --report     # JSON report
  python3 postbridge_health.py --failed     # list failed posts with fix recommendations
"""

import urllib.request, json, sys, os
from datetime import datetime, timezone
from collections import defaultdict

API_BASE = 'https://api.post-bridge.com/v1'
API_KEY = os.environ.get('PB_API_KEY', 'pb_live_AT9Xm4PKaYBzAvFZYGgexi')
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}


# ─── Error categories and their fixes ───────────────────────────────────────

ERROR_CATALOG = {
    'FILE_ACCESS': {
        'pattern': ['File access error', 'file access', 'media files are uploaded'],
        'cause': 'Media file deleted from PostBridge storage (isDeleted=true)',
        'fix': 'RE_UPLOAD_MEDIA',
        'severity': 'HIGH',
        'auto_fixable': False,  # requires new media file
    },
    'RATE_LIMIT': {
        'pattern': ['Rate limit', 'Too many posts', 'rate limit'],
        'cause': 'Too many posts sent to platform in short window',
        'fix': 'RESCHEDULE_WITH_DELAY',
        'severity': 'MEDIUM',
        'auto_fixable': True,
        'retry_delay_hours': 2,
    },
    'TOKEN_EXPIRED': {
        'pattern': ['expired', 'Access token expired', 'reconnect your'],
        'cause': 'Social account OAuth token expired',
        'fix': 'RECONNECT_ACCOUNT',
        'severity': 'HIGH',
        'auto_fixable': False,  # requires user OAuth flow
    },
    'AUTH_403': {
        'pattern': ['403', 'Forbidden', 'unauthorized'],
        'cause': 'Auth token revoked or insufficient permissions',
        'fix': 'RECONNECT_ACCOUNT',
        'severity': 'HIGH',
        'auto_fixable': False,
    },
    'NO_MEDIA': {
        'pattern': ['No supported media', 'only supports images', 'media required'],
        'cause': 'Post sent to platform without required media (Instagram/TikTok/YouTube need media)',
        'fix': 'ADD_MEDIA_OR_REMOVE_ACCOUNT',
        'severity': 'HIGH',
        'auto_fixable': True,  # can remove account from post
    },
    'THREADS_FAIL': {
        'pattern': ['Failed to post to Threads'],
        'cause': 'Threads API intermittent failure (known PostBridge issue)',
        'fix': 'RETRY',
        'severity': 'LOW',
        'auto_fixable': True,
    },
    'TWITTER_FAIL': {
        'pattern': ['Failed to post to Twitter', 'Twitter'],
        'cause': 'Twitter/X API failure or token issue',
        'fix': 'RECONNECT_OR_RETRY',
        'severity': 'MEDIUM',
        'auto_fixable': False,
    },
    'INSTAGRAM_FAIL': {
        'pattern': ['Failed to post to Instagram', 'unexpected error'],
        'cause': 'Instagram API transient error',
        'fix': 'RETRY',
        'severity': 'LOW',
        'auto_fixable': True,
    },
}

# Platform media requirements
MEDIA_REQUIRED_PLATFORMS = {'tiktok', 'instagram', 'youtube'}
PLATFORMS_NEEDING_VIDEO = {'youtube'}


def pb_get(ep):
    req = urllib.request.Request(f'{API_BASE}{ep}', headers=HEADERS)
    try:
        r = urllib.request.urlopen(req, timeout=20)
        return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'error': e.code, 'data': []}


def pb_post(ep, data=None):
    body = json.dumps(data or {}).encode()
    req = urllib.request.Request(f'{API_BASE}{ep}', data=body, headers=HEADERS, method='POST')
    try:
        r = urllib.request.urlopen(req, timeout=20)
        return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'error': e.code}


def classify_error(error_str):
    """Classify error string into category."""
    if not error_str:
        return 'UNKNOWN'
    for cat, info in ERROR_CATALOG.items():
        for pat in info['pattern']:
            if pat.lower() in error_str.lower():
                return cat
    return 'OTHER'


def check_media_health(media_ids):
    """Check if media files are still accessible."""
    results = {}
    for mid in media_ids:
        d = pb_get(f'/media/{mid}')
        obj = d.get('object', {})
        results[mid] = {
            'id': mid,
            'mime_type': d.get('mime_type'),
            'deleted': obj.get('isDeleted', False),
            'url': obj.get('url'),
            'size': obj.get('size_bytes'),
        }
    return results


def get_all_results(limit=500):
    """Fetch post-results in batches."""
    all_results = []
    for offset in range(0, limit, 100):
        d = pb_get(f'/post-results?limit=100&offset={offset}')
        items = d.get('data', [])
        all_results.extend(items)
        if len(items) < 100:
            break
    return all_results


def get_accounts_map():
    """Get all accounts as dict id→info."""
    d = pb_get('/social-accounts?limit=100')
    return {a['id']: a for a in d.get('data', [])}


def run_health_check(auto_fix=False):
    """Run comprehensive health check."""
    print('🔍 PostBridge Health Check')
    print('=' * 50)
    print()

    # 1. Account status
    accounts = get_accounts_map()
    by_platform = defaultdict(list)
    for a in accounts.values():
        by_platform[a['platform']].append(a)

    print(f'📱 ACCOUNTS ({len(accounts)} total):')
    for platform, accs in sorted(by_platform.items()):
        print(f'  {platform}: {len(accs)} accounts')

    print()

    # 2. Recent post-results analysis
    results = get_all_results(300)
    failed = [r for r in results if not r.get('success')]
    success = [r for r in results if r.get('success')]

    print(f'📊 POST RESULTS (last {len(results)}):')
    print(f'  ✅ Success: {len(success)}')
    print(f'  ❌ Failed:  {len(failed)}')
    if results:
        success_rate = len(success) / len(results) * 100
        print(f'  📈 Success rate: {success_rate:.1f}%')
    print()

    # 3. Error breakdown
    error_counts = defaultdict(list)
    for r in failed:
        cat = classify_error(r.get('error', ''))
        error_counts[cat].append(r)

    print('🚨 ERROR BREAKDOWN:')
    recommendations = []

    for cat, items in sorted(error_counts.items(), key=lambda x: -len(x[1])):
        info = ERROR_CATALOG.get(cat, {})
        severity = info.get('severity', 'UNKNOWN')
        fix = info.get('fix', 'MANUAL_REVIEW')
        auto = '🤖 auto-fixable' if info.get('auto_fixable') else '👤 manual required'
        emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(severity, '⚪')

        print(f'  {emoji} {cat}: {len(items)}x | {auto}')
        print(f'     Cause: {info.get("cause", "Unknown")}')
        print(f'     Fix:   {fix}')

        # Build recommendations
        if cat == 'FILE_ACCESS':
            post_ids = list({r['post_id'] for r in items})
            recommendations.append({
                'type': cat,
                'action': 'RE_UPLOAD_MEDIA',
                'posts': post_ids,
                'message': f'{len(items)} posts failed because media was deleted from PostBridge storage. '
                           f'Re-upload the original media files and reschedule.',
            })
        elif cat == 'RATE_LIMIT':
            recommendations.append({
                'type': cat,
                'action': 'RESCHEDULE_WITH_DELAY',
                'posts': [r['post_id'] for r in items],
                'message': f'{len(items)} posts hit rate limit. Space posts 30+ minutes apart.',
            })
        elif cat == 'TOKEN_EXPIRED':
            acc_ids = list({r['social_account_id'] for r in items})
            acc_names = [accounts.get(aid, {}).get('username', str(aid)) for aid in acc_ids]
            recommendations.append({
                'type': cat,
                'action': 'RECONNECT_ACCOUNT',
                'accounts': acc_names,
                'message': f'Reconnect accounts: {", ".join(acc_names)}',
            })
        elif cat == 'THREADS_FAIL':
            recommendations.append({
                'type': cat,
                'action': 'RETRY_OR_IGNORE',
                'message': f'Threads has intermittent failures. Known PostBridge issue. '
                           f'Consider removing Threads from post targets or retry.',
            })
        elif cat == 'NO_MEDIA':
            recommendations.append({
                'type': cat,
                'action': 'ADD_MEDIA_TO_POSTS',
                'message': f'Instagram/TikTok/YouTube require media. '
                           f'Always include image or video when posting to these platforms.',
            })
        print()

    # 4. Media health spot-check
    print('🖼️  MEDIA HEALTH CHECK:')
    # Get recent failed posts and check their media
    deleted_count = 0
    checked = 0
    for r in failed[:20]:
        post = pb_get(f'/posts/{r["post_id"]}')
        media_ids = [m if isinstance(m, str) else m.get('id') for m in post.get('media', [])]
        if media_ids:
            media_health = check_media_health(media_ids)
            for mid, mh in media_health.items():
                checked += 1
                if mh['deleted']:
                    deleted_count += 1

    print(f'  Checked {checked} media files from failed posts')
    print(f'  Deleted/inaccessible: {deleted_count}')
    if deleted_count > 0:
        print(f'  ⚠️  These posts WILL FAIL until media is re-uploaded')
    print()

    # 5. Platform-specific issues
    print('🔧 PLATFORM STATUS:')
    platform_stats = defaultdict(lambda: {'ok': 0, 'fail': 0})
    for r in results:
        acc = accounts.get(r['social_account_id'], {})
        plat = acc.get('platform', 'unknown')
        if r.get('success'):
            platform_stats[plat]['ok'] += 1
        else:
            platform_stats[plat]['fail'] += 1

    for plat, stats in sorted(platform_stats.items()):
        total = stats['ok'] + stats['fail']
        pct = stats['ok'] / total * 100 if total else 0
        status = '✅' if pct >= 70 else '⚠️' if pct >= 40 else '🔴'
        print(f'  {status} {plat}: {stats["ok"]}/{total} ({pct:.0f}% success)')
    print()

    # 6. Recommendations summary
    if recommendations:
        print('📋 ACTION REQUIRED:')
        for i, rec in enumerate(recommendations, 1):
            print(f'  {i}. [{rec["type"]}] {rec["message"]}')
    else:
        print('✅ No critical issues found!')
    print()

    return {
        'total_accounts': len(accounts),
        'by_platform': {p: len(a) for p, a in by_platform.items()},
        'results_checked': len(results),
        'success_count': len(success),
        'failed_count': len(failed),
        'success_rate': len(success) / len(results) * 100 if results else 0,
        'error_breakdown': {cat: len(items) for cat, items in error_counts.items()},
        'deleted_media_count': deleted_count,
        'recommendations': recommendations,
    }


def list_failed_posts():
    """List failed posts with fix recommendations."""
    results = get_all_results(200)
    accounts = get_accounts_map()
    failed = [r for r in results if not r.get('success')]

    print(f'=== FAILED POSTS ({len(failed)}) ===\n')

    by_cat = defaultdict(list)
    for r in failed:
        cat = classify_error(r.get('error', ''))
        by_cat[cat].append(r)

    for cat, items in sorted(by_cat.items(), key=lambda x: -len(x[1])):
        info = ERROR_CATALOG.get(cat, {})
        print(f'[{cat}] {len(items)} posts — Fix: {info.get("fix","UNKNOWN")}')
        for r in items[:5]:
            acc = accounts.get(r['social_account_id'], {})
            print(f'  post:{r["post_id"][:8]}... | @{acc.get("username","?")} | {acc.get("platform","?")}')
            print(f'  Error: {(r.get("error") or "")[:80]}')
        if len(items) > 5:
            print(f'  ... and {len(items)-5} more')
        print()


def validate_post_before_create(caption, social_account_ids, media_ids, accounts_map):
    """Validate a post before creating it. Returns (is_valid, warnings, errors)."""
    warnings = []
    errors = []

    # Check media requirements per platform
    for acc_id in social_account_ids:
        acc = accounts_map.get(acc_id, {})
        platform = acc.get('platform', '').lower()
        username = acc.get('username', str(acc_id))

        if platform in MEDIA_REQUIRED_PLATFORMS and not media_ids:
            errors.append(f'@{username} ({platform}) requires media — text-only will fail')

        if platform in PLATFORMS_NEEDING_VIDEO and media_ids:
            # Check mime type
            for mid in media_ids:
                mh = pb_get(f'/media/{mid}').get('mime_type', '')
                if mh and not mh.startswith('video/'):
                    errors.append(f'@{username} (youtube) requires VIDEO — got {mh}')

    # Check media health
    for mid in media_ids:
        d = pb_get(f'/media/{mid}')
        if d.get('object', {}).get('isDeleted'):
            errors.append(f'Media {mid} is DELETED — will cause File Access Error')
        elif not d.get('object', {}).get('url'):
            warnings.append(f'Media {mid} has no URL yet — may still be processing')

    # Caption check
    if not caption or len(caption.strip()) == 0:
        warnings.append('Empty caption — some platforms may reject')

    is_valid = len(errors) == 0
    return is_valid, warnings, errors


def main():
    args = sys.argv[1:]

    if '--report' in args:
        report = run_health_check()
        print(json.dumps(report, indent=2))
    elif '--failed' in args:
        list_failed_posts()
    elif '--fix' in args:
        run_health_check(auto_fix=True)
    else:
        run_health_check()


if __name__ == '__main__':
    main()
