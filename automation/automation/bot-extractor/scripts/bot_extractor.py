#!/usr/bin/env python3
"""
Bot Extractor — Reverse-engineer any Telegram bot's full architecture.

Usage:
  python3 bot_extractor.py @botname --session alwayscuanbos
  python3 bot_extractor.py @botname --quick --output arch.json
  python3 bot_extractor.py @botname --blueprint
"""

import asyncio, json, sys, argparse, time, re
from collections import deque
from telethon import TelegramClient
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.tl.types import KeyboardButtonCallback, KeyboardButtonUrl, KeyboardButton

API_ID = 23913448
API_HASH = '78d168f985edf365a5cd9679a917a0b2'
SESSIONS = {
    'paijo': '/home/openclaw/.openclaw/workspace/.vilona/sessions/paijo',
    'alwayscuanbos': '/home/openclaw/.openclaw/workspace/.vilona/sessions/alwayscuanbos',
}

# Commands to probe
PROBE_COMMANDS = [
    '/start', '/help', '/admin', '/settings', '/status',
    '/credits', '/info', '/menu', '/about', '/cancel',
    '/panel', '/dashboard', '/profile', '/account'
]

# Input state patterns
INPUT_STATE_PATTERNS = {
    'WAITING_IMAGE': ['kirim foto', 'send photo', 'kirim gambar', 'upload photo', 'silakan foto'],
    'WAITING_TEXT': ['ketik deskripsi', 'type description', 'silakan ketik', 'masukkan teks', 'enter text'],
    'WAITING_FILE': ['kirim sebagai file', 'send as document', 'kirim dokumen', 'upload file'],
    'WAITING_VIDEO': ['kirim video', 'send video', 'upload video'],
    'WAITING_INPUT': ['silakan masukkan', 'please enter', 'ketikkan', 'type your'],
}


def detect_input_state(text):
    """Detect if bot is waiting for user input."""
    if not text:
        return None
    text_lower = text.lower()
    for state, patterns in INPUT_STATE_PATTERNS.items():
        if any(p in text_lower for p in patterns):
            return state
    return None


def extract_buttons(msg):
    """Extract all buttons from a message."""
    buttons = []
    if not msg or not msg.buttons:
        return buttons
    for row in msg.buttons:
        for btn in row:
            btn_info = {
                'text': btn.text,
                'type': 'callback' if hasattr(btn, 'data') and btn.data else 'url' if hasattr(btn, 'url') and btn.url else 'text',
                'data': btn.data.decode() if hasattr(btn, 'data') and btn.data else None,
                'url': btn.url if hasattr(btn, 'url') else None,
            }
            buttons.append(btn_info)
    return buttons


def extract_user_data(text):
    """Extract user data from bot responses."""
    data = {}
    if not text:
        return data
    # Email
    email = re.search(r'[\w.+-]+@[\w-]+\.\w+', text)
    if email:
        data['email'] = email.group(0)
    # Telegram ID
    tid = re.search(r'(?:ID|id)[:\s`]+(\d{6,12})', text)
    if tid:
        data['telegram_id'] = tid.group(1)
    # Phone
    phone = re.search(r'\+?6[2-9]\d{8,12}', text)
    if phone:
        data['phone'] = phone.group(0)
    return data


def fingerprint_tech(responses):
    """Guess tech stack from bot behavior."""
    hints = {}
    all_text = ' '.join(r.get('text', '') or '' for r in responses)

    # Framework hints
    if 'aiogram' in all_text.lower():
        hints['framework'] = 'aiogram'
    elif 'python-telegram-bot' in all_text.lower():
        hints['framework'] = 'python-telegram-bot'

    # Processing time (video generation)
    timing_match = re.search(r'(\d+)\s*menit', all_text)
    if timing_match:
        hints['max_processing_min'] = int(timing_match.group(1))

    # External services in URL buttons
    url_patterns = re.findall(r'https?://[^\s\'"]+', all_text)
    if url_patterns:
        hints['external_urls'] = list(set(url_patterns))[:10]

    return hints


async def extract_bot(bot_username, session_name='alwayscuanbos', quick=False, verbose=True):
    """Main extraction function."""
    session_path = SESSIONS.get(session_name)
    if not session_path:
        print(f'Unknown session: {session_name}. Available: {list(SESSIONS.keys())}')
        return None

    client = TelegramClient(session_path, API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print(f'Session {session_name} not authorized')
        await client.disconnect()
        return None

    me = await client.get_me()
    if verbose:
        print(f'🔍 Extracting {bot_username} as @{me.username}')
        print('=' * 50)

    architecture = {
        'bot': bot_username,
        'extracted_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'extracted_by': f'@{me.username}',
        'user_data': {},
        'commands': {},
        'menus': {},
        'input_flows': [],
        'tech_hints': {},
        'button_data_map': {},
    }

    async def send_and_wait(text, delay=2.5):
        await client.send_message(bot_username, text)
        await asyncio.sleep(delay)
        return (await client.get_messages(bot_username, limit=3))[0]

    async def click_and_wait(msg_id, data, delay=2.5):
        try:
            await client(GetBotCallbackAnswerRequest(
                peer=bot_username, msg_id=msg_id, data=data
            ))
            await asyncio.sleep(delay)
            return (await client.get_messages(bot_username, limit=2))[0]
        except Exception as e:
            return None

    all_responses = []

    # Phase 1: Command discovery
    if verbose:
        print('\n📋 Phase 1: Command Discovery')
    
    for cmd in PROBE_COMMANDS:
        msg = await send_and_wait(cmd, delay=1.5)
        resp_text = msg.text or ''
        
        # Skip if bot just echoed the command (not handled)
        if resp_text.strip() == cmd or not resp_text:
            continue
        
        btns = extract_buttons(msg)
        user_data = extract_user_data(resp_text)
        input_state = detect_input_state(resp_text)
        
        architecture['commands'][cmd] = {
            'text': resp_text[:500],
            'buttons': btns,
            'input_state': input_state,
        }
        architecture['user_data'].update(user_data)
        all_responses.append({'cmd': cmd, 'text': resp_text})
        
        if verbose:
            print(f'  {cmd}: {resp_text[:80].replace(chr(10)," ")}{"..." if len(resp_text)>80 else ""}')

    # Phase 2: BFS Button Tree
    if verbose:
        print('\n🌳 Phase 2: Menu Tree Traversal (BFS)')

    visited_callbacks = set()
    queue = deque()

    # Seed from /start
    start_msg = await send_and_wait('/start')
    start_btns = extract_buttons(start_msg)
    architecture['menus']['__root__'] = {
        'trigger': '/start',
        'text': start_msg.text[:500] if start_msg.text else '',
        'buttons': start_btns,
        'input_state': detect_input_state(start_msg.text),
    }

    for btn in start_btns:
        if btn['data'] and btn['data'] not in visited_callbacks:
            queue.append({
                'callback': btn['data'],
                'label': btn['text'],
                'depth': 1,
                'path': [btn['text']],
            })

    # BFS traversal
    while queue:
        item = queue.popleft()
        cb = item['callback']
        label = item['label']
        depth = item['depth']
        path = item['path']

        if cb in visited_callbacks:
            continue
        visited_callbacks.add(cb)
        architecture['button_data_map'][cb] = label

        if quick and depth > 2:
            continue

        if verbose:
            print(f'  {"  "*depth}[{label}] → {cb}')

        # Reset to start then navigate to this callback
        start_msg = await send_and_wait('/start', delay=1.5)
        resp = await click_and_wait(start_msg.id, cb.encode(), delay=2)

        if not resp:
            # Try from parent context - just click from start
            continue

        resp_text = resp.text or ''
        resp_btns = extract_buttons(resp)
        input_state = detect_input_state(resp_text)

        # Store in architecture
        menu_key = ' > '.join(path)
        architecture['menus'][menu_key] = {
            'trigger': cb,
            'text': resp_text[:500],
            'buttons': resp_btns,
            'input_state': input_state,
            'depth': depth,
            'path': path,
        }

        # Record input flows
        if input_state:
            architecture['input_flows'].append({
                'trigger': cb,
                'path': path,
                'state': input_state,
                'prompt': resp_text[:200],
            })

        all_responses.append({'cb': cb, 'text': resp_text})
        user_data = extract_user_data(resp_text)
        architecture['user_data'].update(user_data)

        # Add new buttons to queue
        for btn in resp_btns:
            if btn['data'] and btn['data'] not in visited_callbacks:
                queue.append({
                    'callback': btn['data'],
                    'label': btn['text'],
                    'depth': depth + 1,
                    'path': path + [btn['text']],
                })

    # Phase 3: Tech fingerprinting
    if verbose:
        print('\n🔬 Phase 3: Tech Stack Analysis')
    architecture['tech_hints'] = fingerprint_tech(all_responses)

    # Phase 4: Summary
    if verbose:
        print(f'\n✅ Extraction Complete!')
        print(f'   Commands found: {len(architecture["commands"])}')
        print(f'   Menu nodes: {len(architecture["menus"])}')
        print(f'   Unique callbacks: {len(visited_callbacks)}')
        print(f'   Input flows: {len(architecture["input_flows"])}')
        print(f'   User data: {architecture["user_data"]}')
        if architecture['tech_hints']:
            print(f'   Tech hints: {architecture["tech_hints"]}')

    await client.disconnect()
    return architecture


def generate_blueprint(architecture):
    """Generate a clone implementation blueprint."""
    blueprint = {
        'description': f'Clone blueprint for {architecture["bot"]}',
        'generated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'states': [],
        'commands': [],
        'callback_handlers': [],
        'message_handlers': [],
        'recommended_stack': 'python-telegram-bot v20+ or aiogram 3.x',
    }

    # Commands
    for cmd, data in architecture['commands'].items():
        blueprint['commands'].append({
            'command': cmd,
            'handler': f'handle_{cmd.lstrip("/")}_command',
            'response': data['text'][:100],
            'has_keyboard': bool(data['buttons']),
        })

    # Callbacks
    for cb, label in architecture['button_data_map'].items():
        menu = next((m for m in architecture['menus'].values() if m.get('trigger') == cb), {})
        blueprint['callback_handlers'].append({
            'callback_data': cb,
            'label': label,
            'handler': f'handle_{cb.lower().replace("-","_")}',
            'response_type': menu.get('input_state') or 'menu',
            'has_sub_menu': bool(menu.get('buttons')),
        })

    # Input flows
    for flow in architecture['input_flows']:
        blueprint['message_handlers'].append({
            'state': flow['state'],
            'trigger': flow['trigger'],
            'path': flow['path'],
            'expected_input': flow['state'].replace('WAITING_', '').lower(),
            'handler': f'handle_{flow["state"].lower()}_input',
        })

    return blueprint


async def main():
    parser = argparse.ArgumentParser(description='Bot Architecture Extractor')
    parser.add_argument('bot', help='Bot username (e.g. @mybot)')
    parser.add_argument('--session', default='alwayscuanbos', help='Session name to use')
    parser.add_argument('--quick', action='store_true', help='Quick mode (depth 2 only)')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--blueprint', action='store_true', help='Generate clone blueprint')
    parser.add_argument('--quiet', action='store_true', help='Suppress verbose output')
    args = parser.parse_args()

    architecture = await extract_bot(
        args.bot,
        session_name=args.session,
        quick=args.quick,
        verbose=not args.quiet
    )

    if not architecture:
        sys.exit(1)

    # Output
    output_data = architecture
    if args.blueprint:
        blueprint = generate_blueprint(architecture)
        output_data = {'architecture': architecture, 'blueprint': blueprint}
        print('\n📐 CLONE BLUEPRINT:')
        print(json.dumps(blueprint, indent=2, ensure_ascii=False))

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f'\n💾 Saved to {args.output}')
    else:
        print('\n📊 FULL ARCHITECTURE:')
        print(json.dumps(output_data, indent=2, ensure_ascii=False)[:5000])


if __name__ == '__main__':
    asyncio.run(main())
