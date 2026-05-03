#!/usr/bin/env python3
"""
TikTok OAuth Flow Generator for PostBridge

Flow:
1. Script generates TikTok OAuth URL via PostBridge dashboard (browser)
2. Sends URL to user via Telegram
3. User opens URL on device with TikTok logged in → authorizes
4. PostBridge receives callback → account connected
5. Script verifies new connection

Usage:
  python3 tiktok_oauth_flow.py connect    # generate connect URL (new account)
  python3 tiktok_oauth_flow.py refresh    # generate refresh URL (existing accounts)
  python3 tiktok_oauth_flow.py status     # check TikTok connection status
"""

import sys
import urllib.request
import json
import time
import subprocess

API_KEY = 'REDACTED_POSTBRIDGE_KEY'
HEADERS = {'Authorization': f'Bearer {API_KEY}'}
DASHBOARD_TARGET_ID = 'C790D362929990FB49CE42759445D632'

# PostBridge OAuth URL pattern (for reference/manual use)
# TikTok OAuth goes through: tiktok.com/login → tiktok.com/v2/auth/authorize → post-bridge.com/api/tiktok-auth/callback
# state=<uuid> for new connect, state=refresh_<uuid> for token refresh
# client_key: REDACTED_API_KEY (PostBridge TikTok app)
# scopes: user.info.basic, video.list, video.upload, video.publish


def get_tiktok_accounts():
    """Fetch current TikTok accounts via API."""
    req = urllib.request.Request(
        'https://api.post-bridge.com/v1/social-accounts?limit=100',
        headers=HEADERS
    )
    d = json.loads(urllib.request.urlopen(req, timeout=15).read())
    return [a for a in d.get('data', []) if a.get('platform') == 'tiktok']


def browser_eval(js):
    """Run JS in PostBridge browser tab via openclaw browser tool."""
    # Use openclaw browser CDP
    import urllib.parse
    cmd = f"""python3 -c "
import urllib.request, json
ws = 'http://localhost:18810'
req = urllib.request.Request(ws + '/json/list')
tabs = json.loads(urllib.request.urlopen(req).read())
target = next((t for t in tabs if '{DASHBOARD_TARGET_ID}' in t.get('id','')), None)
if not target:
    print('Tab not found')
else:
    # Send CDP Runtime.evaluate
    import websocket
    ws_url = target['webSocketDebuggerUrl']
    print('Target found:', target['url'][:50])
"
    """
    result = subprocess.run(['bash', '-c', cmd], capture_output=True, text=True)
    return result.stdout.strip()


def print_instructions(url, mode='connect'):
    """Print instructions for user."""
    print()
    print('=' * 60)
    print(f'📱 TIKTOK OAUTH URL GENERATED — {mode.upper()} MODE')
    print('=' * 60)
    print()
    print('Send this URL to user to open on device with TikTok logged in:')
    print()
    print(url)
    print()
    print('Steps for user:')
    print('1. Open the URL above in browser that is logged into TikTok')
    print('2. Log in to the TikTok account you want to connect')
    print('3. Click "Authorize" when TikTok asks for permissions')
    print('4. PostBridge will automatically receive the connection')
    print('5. Tell us when done — we will verify the connection')
    print()
    print('Permissions requested:')
    print('  - user.info.basic (read profile)')
    print('  - video.list (see videos)')
    print('  - video.upload (upload videos)')
    print('  - video.publish (publish/schedule)')
    print('=' * 60)


def cmd_status(args):
    """Check current TikTok connection status."""
    accounts = get_tiktok_accounts()
    print(f'=== TIKTOK ACCOUNTS ({len(accounts)}/10 connected) ===')
    for a in accounts:
        print(f'  @{a.get("username","?")} | ID:{a.get("id")} | status:{a.get("status","?")}')

    if len(accounts) < 10:
        missing = 10 - len(accounts)
        print(f'\n⚠️  {missing} accounts missing — need reconnect')
    else:
        print('\n✅ All 10 TikTok accounts connected')


def cmd_get_url(mode='connect'):
    """
    Generate OAuth URL by intercepting PostBridge browser navigation.

    This requires the PostBridge dashboard tab to be open in the browser.
    The script guides the user through the process.
    """
    print(f'Getting TikTok OAuth URL for mode: {mode}')
    print()
    print('MANUAL STEPS (automated version coming):')
    print('1. Open PostBridge dashboard at: https://www.post-bridge.com/dashboard/connections')
    print('2. Scroll to TikTok section')

    if mode == 'connect':
        print('3. Click "Connect Tiktok" button')
        print('4. In the modal that appears, click "Connect" button')
        print('5. Copy the URL from the browser address bar (tiktok.com/login?...)')
        print('6. Send that URL via Telegram to user')
    else:
        print('3. Click "Refresh TikTok" button')
        print('4. Copy the URL from browser address bar (tiktok.com/login?...&state=refresh_...)')
        print('5. Send that URL via Telegram to user')

    print()
    print('OAuth URL Pattern:')
    print('https://www.tiktok.com/login?lang=en&enter_from=dev_REDACTED_API_KEY')
    print('  &redirect_url=...tiktok.com/v2/auth/authorize...')
    print('  &state=<uuid>            ← new connect')
    print('  &state=refresh_<uuid>    ← token refresh')
    print()
    print('callback: https://www.post-bridge.com/api/tiktok-auth/callback')
    print('client_key: REDACTED_API_KEY')


def cmd_verify(args):
    """Verify TikTok connection after OAuth."""
    print('Checking TikTok accounts (waiting 5 seconds for PostBridge to process)...')
    time.sleep(5)
    accounts = get_tiktok_accounts()
    print(f'Connected TikTok accounts: {len(accounts)}')
    for a in accounts:
        print(f'  @{a.get("username","?")} | {a.get("id")}')
    return accounts


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else 'status'

    if cmd == 'status':
        cmd_status(args[1:])
    elif cmd == 'connect':
        cmd_get_url('connect')
    elif cmd == 'refresh':
        cmd_get_url('refresh')
    elif cmd == 'verify':
        cmd_verify(args[1:])
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
