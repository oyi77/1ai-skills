#!/usr/bin/env python3
"""
PostBridge API Wrapper — BerkahKarya
Usage: python3 postbridge_api.py [command] [args]

Commands:
  accounts                  — list all connected accounts
  accounts tiktok           — list TikTok accounts only
  analytics                 — show analytics summary
  analytics sync            — trigger analytics refresh
  posts [status]            — list posts (status: scheduled/posted/failed/draft)
  post-results              — show recent post results with success/fail
  post-create <caption>     — create a draft post (edit to add accounts)
  failed-analysis           — analyze failure patterns
"""

import urllib.request, urllib.error
import json, sys, os
from datetime import datetime, timezone

API_BASE = 'https://api.post-bridge.com/v1'
API_KEY = os.environ.get('PB_API_KEY', 'pb_live_AT9Xm4PKaYBzAvFZYGgexi')

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Platform → account IDs mapping
PLATFORM_ACCOUNTS = {
    'tiktok': [
        'bkjaya00', 'catatanoperator', 'sehatseraiphari',
        'riviewprodukfashionjujur', 'drlifehacks1', 'divasehatsetiaphari',
        'massehatyuk', 'nugrohopratama5', 'baimwongdiskon', 'clinicguru'
    ],
    'instagram': [
        'algoexperthub', 'favisoraanggraeni', 'chayangkasih', 'bkjayautama',
        'riviewprodukcek', 'ardanardiawan', 'nyamiresepdapur', 'ameliacintaimoet',
        'emake.nok', 'riviewprodukaffiliate', 'berkahkaryadigitalproduct',
        'berkahkaryadigitalmarketing'
    ],
    'youtube': [
        'Algo Expert Hub', 'dengan tatapan', 'berkah karya digital agency',
        'BK METAL', 'Mak e Nok', 'Chill Work Zone Lofi', 'Resep Dapur Nyami',
        'grahaelektroniktws', 'Diskon Hunter', 'Mak E Nok'
    ]
}


def pb_request(method, endpoint, data=None):
    url = f'{API_BASE}{endpoint}'
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        r = urllib.request.urlopen(req, timeout=20)
        return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f'HTTP {e.code}: {e.read().decode()[:200]}', file=sys.stderr)
        sys.exit(1)


def pb_get(endpoint):
    return pb_request('GET', endpoint)


def pb_post(endpoint, data=None):
    return pb_request('POST', endpoint, data or {})


def get_all_accounts():
    """Fetch all social accounts."""
    result = []
    offset = 0
    while True:
        d = pb_get(f'/social-accounts?limit=100&offset={offset}')
        items = d.get('data', [])
        result.extend(items)
        if offset + 100 >= d.get('meta', {}).get('total', 0) or not items:
            break
        offset += 100
    return result


def accounts_by_platform(accounts, platform=None):
    if platform:
        return [a for a in accounts if a.get('platform', '').lower() == platform.lower()]
    by_p = {}
    for a in accounts:
        p = a.get('platform', '?')
        by_p.setdefault(p, []).append(a)
    return by_p


def cmd_accounts(args):
    accounts = get_all_accounts()
    platform = args[0] if args else None

    if platform:
        filtered = accounts_by_platform(accounts, platform)
        print(f'=== {platform.upper()} ACCOUNTS ({len(filtered)}) ===')
        for a in filtered:
            print(f'  ID:{a["id"]} | @{a.get("username","?")} | status:{a.get("status","?")}')
    else:
        by_p = accounts_by_platform(accounts)
        print(f'=== ALL ACCOUNTS ({len(accounts)}) ===')
        for p, accs in sorted(by_p.items()):
            print(f'\n{p.upper()} ({len(accs)}):')
            for a in accs:
                print(f'  ID:{a["id"]} | @{a.get("username","?")}')


def cmd_analytics(args):
    if args and args[0] == 'sync':
        print('Triggering analytics sync...')
        resp = pb_post('/analytics/sync')
        triggered = resp.get('triggered', [])
        print(f'Syncing: {[t["platform"] for t in triggered]}')
        return

    all_items = []
    offset = 0
    while True:
        d = pb_get(f'/analytics?limit=100&offset={offset}')
        items = d.get('data', [])
        all_items.extend(items)
        if offset + 100 >= d.get('meta', {}).get('total', 0) or not items:
            break
        offset += 100

    by_platform = {}
    for item in all_items:
        p = item.get('platform', '?')
        if p not in by_platform:
            by_platform[p] = {'posts': 0, 'views': 0, 'likes': 0, 'comments': 0, 'shares': 0}
        by_platform[p]['posts'] += 1
        by_platform[p]['views'] += item.get('view_count', 0)
        by_platform[p]['likes'] += item.get('like_count', 0)
        by_platform[p]['comments'] += item.get('comment_count', 0)
        by_platform[p]['shares'] += item.get('share_count', 0)

    print(f'=== ANALYTICS SUMMARY ({len(all_items)} tracked posts) ===')
    for p, s in sorted(by_platform.items(), key=lambda x: -x[1]['views']):
        avg_views = s['views'] / s['posts'] if s['posts'] else 0
        print(f'\n{p.upper()}:')
        print(f'  Posts: {s["posts"]} | Views: {s["views"]:,} | Avg: {avg_views:.0f}')
        print(f'  Likes: {s["likes"]} | Comments: {s["comments"]} | Shares: {s["shares"]}')

    # Top 5 posts
    top = sorted(all_items, key=lambda x: -x.get('view_count', 0))[:5]
    print('\n=== TOP 5 POSTS ===')
    for t in top:
        print(f'  {t["platform"]} | {t.get("view_count",0):,} views | {t.get("like_count",0)} likes | id:{t.get("platform_post_id","?")}')


def cmd_posts(args):
    status = args[0] if args else None
    ep = '/posts?limit=20'
    if status:
        ep += f'&status={status}'
    d = pb_get(ep)
    posts = d.get('data', [])
    total = d.get('meta', {}).get('total', 0)
    label = status or 'all'
    print(f'=== POSTS [{label.upper()}] (showing {len(posts)}/{total}) ===')
    for p in posts:
        sched = p.get('scheduled_at', '')[:16] if p.get('scheduled_at') else 'no date'
        cap = (p.get('caption') or '')[:60].replace('\n', ' ')
        accs = len(p.get('social_accounts', []))
        print(f'  {sched} | {p["status"]} | {accs} accs | {cap}...')


def cmd_post_results(args):
    d = pb_get('/post-results?limit=100')
    results = d.get('data', [])
    success = [r for r in results if r.get('success')]
    failed = [r for r in results if not r.get('success')]

    print(f'=== POST RESULTS (latest 100) ===')
    print(f'Success: {len(success)} | Failed: {len(failed)}')

    errors = {}
    for r in failed:
        e = (r.get('error') or 'unknown')[:80]
        errors[e] = errors.get(e, 0) + 1

    if errors:
        print('\nTop Errors:')
        for e, n in sorted(errors.items(), key=lambda x: -x[1]):
            print(f'  [{n}x] {e}')


def cmd_failed_analysis(args):
    d = pb_get('/post-results?limit=200')
    results = d.get('data', [])
    failed = [r for r in results if not r.get('success')]

    by_account = {}
    for r in failed:
        acc_id = r.get('social_account_id', '?')
        err = (r.get('error') or 'unknown')[:60]
        if acc_id not in by_account:
            by_account[acc_id] = []
        by_account[acc_id].append(err)

    print(f'=== FAILURE ANALYSIS ({len(failed)} failed) ===')
    for acc_id, errs in sorted(by_account.items(), key=lambda x: -len(x[1]))[:10]:
        print(f'\nAccount {acc_id} ({len(errs)} failures):')
        unique_errs = list(set(errs))
        for e in unique_errs[:3]:
            print(f'  - {e}')


def cmd_media_upload(args):
    """Usage: media-upload <filepath>"""
    if not args:
        print('Usage: media-upload <filepath>')
        return

    filepath = args[0]
    if not os.path.exists(filepath):
        print(f'File not found: {filepath}')
        return

    ext = filepath.rsplit('.', 1)[-1].lower()
    mime_map = {'mp4': 'video/mp4', 'mov': 'video/quicktime',
                'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png'}
    mime = mime_map.get(ext, 'application/octet-stream')
    size = os.path.getsize(filepath)

    print(f'Requesting upload URL ({mime}, {size:,} bytes)...')
    resp = pb_post('/media/create-upload-url', {'mime_type': mime, 'file_size': size})
    upload_url = resp.get('upload_url')
    media_id = resp.get('id')

    if not upload_url:
        print('Failed to get upload URL:', resp)
        return

    print(f'Uploading to S3... media_id: {media_id}')
    with open(filepath, 'rb') as f:
        data = f.read()
    req = urllib.request.Request(upload_url, data=data, method='PUT',
                                  headers={'Content-Type': mime})
    urllib.request.urlopen(req, timeout=120)
    print(f'✅ Upload complete! media_id: {media_id}')
    return media_id


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    cmd = args[0]
    rest = args[1:]

    commands = {
        'accounts': cmd_accounts,
        'analytics': cmd_analytics,
        'posts': cmd_posts,
        'post-results': cmd_post_results,
        'failed-analysis': cmd_failed_analysis,
        'media-upload': cmd_media_upload,
    }

    if cmd in commands:
        commands[cmd](rest)
    else:
        print(f'Unknown command: {cmd}')
        print(__doc__)


if __name__ == '__main__':
    main()
