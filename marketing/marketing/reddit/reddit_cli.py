#!/usr/bin/env python3
"""
reddit-cli — Reddit automation for OpenClaw
Routes API calls through browser CDP (bypasses Cloudflare TLS fingerprinting)
Auth: uses browser session cookies + modhash (no OAuth token needed)
"""
import argparse, sys, os, json, re, time
import websocket

CDP = "http://127.0.0.1:18810"
UA = 'openclaw-reddit-cli/1.0'

def get_reddit_tab():
    """Get an existing Reddit tab (for cookie/modhash auth only, not for API calls)"""
    import urllib.request
    r = urllib.request.urlopen(f"{CDP}/json", timeout=5)
    tabs = json.loads(r.read())
    for t in tabs:
        if t.get('type') == 'page' and 'reddit.com' in t.get('url', ''):
            return t['id']
    for t in tabs:
        if t.get('type') == 'page':
            return t['id']
    return None

def open_blank_tab():
    """Open a dedicated blank tab for API calls — isolation from other agents"""
    import urllib.request
    # Use Target.createTarget CDP command via /json/new
    r = urllib.request.urlopen(f"{CDP}/json/new?about:blank", timeout=5)
    tab = json.loads(r.read())
    return tab['id']

def close_tab(target_id):
    import urllib.request
    try:
        req = urllib.request.Request(f"{CDP}/json/close/{target_id}", method='GET')
        urllib.request.urlopen(req, timeout=5)
    except:
        pass

def navigate_tab_to_reddit(target_id):
    """Navigate blank tab to reddit.com to get session cookies"""
    cdp_eval(target_id, "window.location.href", await_promise=False)
    # Just need cookies — navigate to reddit to get them
    import urllib.request, time
    ws_url = f"ws://127.0.0.1:18810/devtools/page/{target_id}"
    ws = websocket.create_connection(ws_url, timeout=10, suppress_origin=True)
    ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://www.reddit.com/api/me.json"}}))
    time.sleep(2)
    ws.close()

def cdp_eval(target_id, expression, await_promise=True):
    ws_url = f"ws://127.0.0.1:18810/devtools/page/{target_id}"
    ws = websocket.create_connection(ws_url, timeout=20, suppress_origin=True)
    ws.send(json.dumps({
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {"expression": expression, "awaitPromise": await_promise, "returnByValue": True}
    }))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == 1:
            ws.close()
            result = msg.get('result', {}).get('result', {})
            if result.get('type') == 'string':
                return result.get('value', '')
            return result.get('value', '')
    ws.close()
    return ''

def get_auth(target_id):
    """
    Get modhash + username by opening a DEDICATED reddit tab.
    Does NOT rely on any existing tab — safe for parallel use.
    """
    import urllib.request, time

    # Open a fresh tab, navigate to reddit /api/me.json
    req = urllib.request.Request(f"{CDP}/json/new", method='PUT')
    r = urllib.request.urlopen(req, timeout=5)
    auth_tab = json.loads(r.read())['id']
    time.sleep(0.3)

    ws_url = f"ws://127.0.0.1:18810/devtools/page/{auth_tab}"
    ws = websocket.create_connection(ws_url, timeout=10, suppress_origin=True)

    # Navigate to reddit.com/api/me.json — session cookies auto-sent
    ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://www.reddit.com/api/me.json"}}))
    time.sleep(2)  # wait for page load

    # Extract JSON from page body
    ws.send(json.dumps({"id":2,"method":"Runtime.evaluate","params":{
        "expression": "document.body && document.body.innerText",
        "returnByValue": True
    }}))
    msg = json.loads(ws.recv())  # might get nav event first
    while msg.get('id') != 2:
        msg = json.loads(ws.recv())
    ws.close()

    # Clean up auth tab
    try: urllib.request.urlopen(f"{CDP}/json/close/{auth_tab}", timeout=3)
    except: pass

    text = msg.get('result',{}).get('result',{}).get('value','')
    try:
        d = json.loads(text)
        data = d.get('data', {})
        return data.get('name'), data.get('modhash', '')
    except:
        return None, ''

def browser_api(target_id, method, path, data=None, params=None, modhash=None):
    """Make Reddit API call through browser fetch (uses session cookies automatically)"""
    qs = ''
    if params:
        import urllib.parse
        qs = '?' + urllib.parse.urlencode({k:v for k,v in params.items() if v is not None})

    body_js = 'null'
    headers_extra = ''
    if data:
        import urllib.parse
        body_str = urllib.parse.urlencode(data)
        body_js = json.dumps(body_str)
        headers_extra = f"'Content-Type': 'application/x-www-form-urlencoded',"
    if modhash:
        headers_extra += f"'X-Modhash': {json.dumps(modhash)},"

    expr = f"""(async()=>{{
        try {{
            const r = await fetch('https://www.reddit.com{path}{qs}', {{
                method: '{method.upper()}',
                credentials: 'include',
                headers: {{ {headers_extra} 'User-Agent': 'openclaw/1.0' }},
                body: {body_js}
            }});
            const txt = await r.text();
            return JSON.stringify({{status: r.status, body: txt}});
        }} catch(e) {{ return JSON.stringify({{error: e.message}}); }}
    }})()"""

    val = cdp_eval(target_id, expr)
    result = json.loads(val)
    if 'error' in result:
        print(f"❌ Fetch error: {result['error']}", file=sys.stderr); sys.exit(1)
    if result['status'] >= 400:
        print(f"❌ HTTP {result['status']}: {result['body'][:300]}", file=sys.stderr); sys.exit(1)
    body = result['body']
    try:
        return json.loads(body)
    except:
        return {'raw': body}

def cmd_me(args, target, user, modhash):
    d = browser_api(target, 'GET', '/api/me.json')
    u = d.get('data', d)
    print(f"👤 u/{u.get('name')} | Karma: {u.get('total_karma',0):,} | Premium: {u.get('is_gold',False)}")

def cmd_post(args, target, user, modhash):
    sub = args.subreddit.lstrip('r/')
    kind = 'link' if args.link else 'self'
    payload = {
        'sr': sub, 'kind': kind, 'title': args.title,
        'resubmit': 'true', 'nsfw': 'false', 'api_type': 'json'
    }
    if kind == 'self': payload['text'] = args.body or ''
    else: payload['url'] = args.link

    d = browser_api(target, 'POST', '/api/submit', data=payload, modhash=modhash)
    json_data = d.get('json', d)
    errors = json_data.get('errors', [])
    if errors:
        print(f"❌ Error: {errors}", file=sys.stderr); sys.exit(1)
    url = json_data.get('data', {}).get('url', '')
    print(f"✅ Posted to r/{sub}!")
    if url: print(f"🔗 {url}")

def cmd_comment(args, target, user, modhash):
    match = re.search(r'/comments/([a-z0-9]+)', args.post_url)
    if not match: print("❌ Invalid post URL", file=sys.stderr); sys.exit(1)
    d = browser_api(target, 'POST', '/api/comment', modhash=modhash, data={
        'thing_id': f't3_{match.group(1)}', 'text': args.body, 'api_type': 'json'
    })
    json_data = d.get('json', d)
    errors = json_data.get('errors', [])
    if errors: print(f"❌ {errors}", file=sys.stderr); sys.exit(1)
    print("✅ Comment posted!")

def cmd_reply(args, target, user, modhash):
    cid = args.comment_id
    match = re.search(r't1_([a-z0-9]+)', cid) or re.search(r'([a-z0-9]+)$', cid)
    thing_id = f"t1_{match.group(1)}" if match else cid
    d = browser_api(target, 'POST', '/api/comment', modhash=modhash, data={
        'thing_id': thing_id, 'text': args.body, 'api_type': 'json'
    })
    json_data = d.get('json', d)
    errors = json_data.get('errors', [])
    if errors: print(f"❌ {errors}", file=sys.stderr); sys.exit(1)
    print("✅ Reply posted!")

def cmd_search(args, target, user, modhash):
    sub = args.subreddit.lstrip('r/')
    d = browser_api(target, 'GET', f'/r/{sub}/search.json',
                    params={'q': args.query, 'limit': args.limit, 'sort': args.sort, 'restrict_sr': 1})
    posts = d.get('data', {}).get('children', [])
    print(f"🔍 r/{sub} — '{args.query}' ({args.sort}):\n")
    for i, p in enumerate(posts, 1):
        pd = p['data']
        print(f"  {i}. [{pd.get('score',0):+}] {pd['title']}")
        print(f"     https://reddit.com{pd['permalink']}\n")

def cmd_hot(args, target, user, modhash):
    sub = args.subreddit.lstrip('r/')
    d = browser_api(target, 'GET', f'/r/{sub}/hot.json', params={'limit': args.limit})
    posts = d.get('data', {}).get('children', [])
    print(f"🔥 r/{sub} hot:\n")
    for i, p in enumerate(posts, 1):
        pd = p['data']
        print(f"  {i}. [{pd.get('score',0):,}⬆] {pd['title']}")
        print(f"     {pd.get('num_comments',0)} comments | https://reddit.com{pd['permalink']}")

def cmd_inbox(args, target, user, modhash):
    d = browser_api(target, 'GET', '/message/inbox.json', params={'limit': args.limit})
    msgs = d.get('data', {}).get('children', [])
    print(f"📬 Inbox ({len(msgs)}):\n")
    for m in msgs:
        md = m['data']
        print(f"  From: u/{md.get('author','[deleted]')} | {md.get('subject','reply')}")
        print(f"  {md.get('body','')[:150]}")
        print(f"  https://reddit.com{md.get('context','')}\n")

def cmd_upvote(args, target, user, modhash):
    match = re.search(r'/comments/([a-z0-9]+)', args.target) or re.search(r'^([a-z0-9]+)$', args.target)
    if not match: print("❌ Invalid target", file=sys.stderr); sys.exit(1)
    browser_api(target, 'POST', '/api/vote', modhash=modhash,
                data={'id': f't3_{match.group(1)}', 'dir': '1'})
    print("✅ Upvoted!")

def main():
    p = argparse.ArgumentParser(description='reddit-cli: Reddit via browser CDP')
    s = p.add_subparsers(dest='cmd')

    pp = s.add_parser('post', help='Submit text/link post')
    pp.add_argument('subreddit'); pp.add_argument('--title', required=True)
    pp.add_argument('--body', default=''); pp.add_argument('--link'); pp.add_argument('--flair')

    pc = s.add_parser('comment', help='Comment on post')
    pc.add_argument('post_url'); pc.add_argument('--body', required=True)

    pr = s.add_parser('reply', help='Reply to comment')
    pr.add_argument('comment_id'); pr.add_argument('--body', required=True)

    ps = s.add_parser('search', help='Search subreddit')
    ps.add_argument('subreddit'); ps.add_argument('--query', required=True)
    ps.add_argument('--limit', type=int, default=10)
    ps.add_argument('--sort', default='relevance', choices=['relevance','hot','top','new'])

    ph = s.add_parser('hot', help='Hot posts')
    ph.add_argument('subreddit'); ph.add_argument('--limit', type=int, default=10)

    s.add_parser('me', help='Account info')

    pi = s.add_parser('inbox', help='Show inbox')
    pi.add_argument('--limit', type=int, default=10)

    pu = s.add_parser('upvote', help='Upvote a post')
    pu.add_argument('target')

    args = p.parse_args()
    if not args.cmd: p.print_help(); sys.exit(0)

    # Auth via dedicated temp tab (no dependency on existing tabs)
    user, modhash = get_auth(None)
    if not user:
        print("❌ Not logged into Reddit. Visit reddit.com in the OpenClaw browser.", file=sys.stderr); sys.exit(1)

    print(f"[auth: u/{user}]")

    # Open a DEDICATED tab pre-loaded on reddit.com — safe for parallel use
    import urllib.request as _ur, time as _time
    req = _ur.Request(f"{CDP}/json/new", method='PUT')
    api_target = json.loads(_ur.urlopen(req, timeout=5).read())['id']
    _time.sleep(0.3)
    # Navigate to reddit.com so session cookies are available for fetch()
    _ws = websocket.create_connection(
        f"ws://127.0.0.1:18810/devtools/page/{api_target}", timeout=10, suppress_origin=True)
    _ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://www.reddit.com"}}))
    _time.sleep(1.5)
    _ws.close()

    try:
        dispatch = {
            'me': cmd_me, 'post': cmd_post, 'comment': cmd_comment, 'reply': cmd_reply,
            'search': cmd_search, 'hot': cmd_hot, 'inbox': cmd_inbox, 'upvote': cmd_upvote
        }
        dispatch[args.cmd](args, api_target, user, modhash)
    finally:
        close_tab(api_target)  # always clean up

if __name__ == '__main__':
    main()
