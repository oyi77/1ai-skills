#!/usr/bin/env python3
"""
Bot Extractor v2 — Reverse-engineer any Telegram bot's full architecture.

Improvements over v1:
  - Better input state detection (Indonesian + English patterns)
  - Full command probing with response timing
  - Retry on FloodWait / errors (max 3 retries)
  - URL button detection (external links)
  - Media type detection (photo/video/document/audio)
  - Context-aware sub-menu navigation (not always resetting to /start)
  - UX scoring with breakdown
  - Comprehensive summary in output JSON

Usage:
  python3 bot_extractor.py @botname --session alwayscuanbos
  python3 bot_extractor.py @botname --quick --output arch.json
  python3 bot_extractor.py @botname --blueprint
"""

import asyncio
import json
import sys
import argparse
import time
import re
from collections import deque
from telethon import TelegramClient
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.tl.types import (
    KeyboardButtonCallback,
    KeyboardButtonUrl,
    KeyboardButton,
    MessageMediaPhoto,
    MessageMediaDocument,
)
from telethon.errors import FloodWaitError

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
    '/panel', '/dashboard', '/profile', '/account',
    '/language', '/lang', '/premium', '/upgrade', '/plan',
    '/history', '/balance', '/refer', '/invite', '/support',
]

# Input state patterns — extended for Indonesian
INPUT_STATE_PATTERNS = {
    'WAITING_IMAGE': [
        'kirim foto', 'send photo', 'kirim gambar', 'upload photo',
        'silakan foto', 'foto yang', 'gambar yang', 'kirimkan foto',
        'lampirkan foto', 'upload gambar', 'send image', 'attach photo',
    ],
    'WAITING_TEXT': [
        'ketik deskripsi', 'type description', 'silakan ketik',
        'masukkan teks', 'enter text', 'tulis deskripsi', 'deskripsikan',
        'tuliskan', 'ketikkan prompt', 'type your prompt', 'input text',
        'masukkan prompt', 'tulis prompt', 'silakan tulis',
    ],
    'WAITING_FILE': [
        'kirim sebagai file', 'send as document', 'kirim dokumen',
        'upload file', 'kirim file', 'sebagai dokumen', 'format file',
        'send as file', 'sebagai file', 'kirimkan file',
    ],
    'WAITING_VIDEO': [
        'kirim video', 'send video', 'upload video', 'silakan video',
    ],
    'WAITING_AUDIO': [
        'kirim audio', 'send audio', 'kirim suara', 'upload audio',
    ],
    'WAITING_INPUT': [
        'silakan masukkan', 'please enter', 'ketikkan', 'type your',
        'masukkan', 'silahkan masukkan', 'input your', 'enter your',
    ],
}

MAX_RETRIES = 3
SLOW_THRESHOLD_MS = 2000  # responses slower than this suggest async/AI backend


def detect_input_state(text):
    """Detect if bot is waiting for user input."""
    if not text:
        return None
    text_lower = text.lower()
    for state, patterns in INPUT_STATE_PATTERNS.items():
        if any(p in text_lower for p in patterns):
            return state
    return None


def detect_media_type(msg):
    """Detect what media type a message contains."""
    if not msg or not msg.media:
        return None
    if isinstance(msg.media, MessageMediaPhoto):
        return 'photo'
    if isinstance(msg.media, MessageMediaDocument):
        doc = msg.media.document
        if doc and doc.mime_type:
            mime = doc.mime_type
            if mime.startswith('video/'):
                return 'video'
            if mime.startswith('audio/'):
                return 'audio'
            if mime.startswith('image/'):
                return 'image_file'
            return 'document'
        return 'document'
    return 'other'


def extract_buttons(msg):
    """Extract all buttons from a message, distinguishing callback vs URL vs text."""
    buttons = []
    if not msg or not msg.buttons:
        return buttons
    for row in msg.buttons:
        for btn in row:
            if hasattr(btn, 'data') and btn.data:
                btn_info = {
                    'text': btn.text,
                    'type': 'callback',
                    'data': btn.data.decode() if isinstance(btn.data, bytes) else btn.data,
                    'url': None,
                }
            elif hasattr(btn, 'url') and btn.url:
                btn_info = {
                    'text': btn.text,
                    'type': 'url',
                    'data': None,
                    'url': btn.url,
                }
            else:
                btn_info = {
                    'text': btn.text,
                    'type': 'text',
                    'data': None,
                    'url': None,
                }
            buttons.append(btn_info)
    return buttons


def extract_user_data(text):
    """Extract user data from bot responses."""
    data = {}
    if not text:
        return data
    email = re.search(r'[\w.+-]+@[\w-]+\.\w+', text)
    if email:
        data['email'] = email.group(0)
    tid = re.search(r'(?:ID|id)[:\s`]+(\d{6,12})', text)
    if tid:
        data['telegram_id'] = tid.group(1)
    phone = re.search(r'\+?6[2-9]\d{8,12}', text)
    if phone:
        data['phone'] = phone.group(0)
    return data


def fingerprint_tech(responses, timing_data):
    """Guess tech stack from bot behavior and response timings."""
    hints = {}
    all_text = ' '.join(r.get('text', '') or '' for r in responses)

    # Framework hints from text
    if 'aiogram' in all_text.lower():
        hints['framework'] = 'aiogram'
    elif 'python-telegram-bot' in all_text.lower():
        hints['framework'] = 'python-telegram-bot'

    # Processing time mentions
    timing_match = re.search(r'(\d+)\s*menit', all_text)
    if timing_match:
        hints['max_processing_min'] = int(timing_match.group(1))

    # External URLs in text
    url_patterns = re.findall(r'https?://[^\s\'"<>]+', all_text)
    if url_patterns:
        hints['external_urls'] = list(set(url_patterns))[:20]

    # Response timing analysis
    if timing_data:
        times = [t for t in timing_data if t > 0]
        if times:
            avg_ms = sum(times) / len(times)
            hints['avg_response_time_ms'] = round(avg_ms, 1)
            hints['max_response_time_ms'] = round(max(times), 1)
            hints['min_response_time_ms'] = round(min(times), 1)
            slow_count = sum(1 for t in times if t > SLOW_THRESHOLD_MS)
            if slow_count > len(times) * 0.3:
                hints['estimated_backend'] = 'async_ai'
            else:
                hints['estimated_backend'] = 'sync'

    return hints


def compute_ux_score(architecture):
    """Compute a UX quality score for the bot."""
    score = 0
    max_score = 100
    breakdown = {}
    issues = []
    strengths = []

    menus = architecture.get('menus', {})
    commands = architecture.get('commands', {})
    input_flows = architecture.get('input_flows', [])
    dead_buttons = architecture.get('dead_buttons', [])
    url_buttons = architecture.get('url_buttons', [])

    # 1. Has /start with buttons (20 pts)
    root = menus.get('__root__', {})
    if root.get('buttons'):
        score += 20
        breakdown['start_menu'] = 20
        strengths.append('Clear main menu with buttons on /start')
    else:
        breakdown['start_menu'] = 0
        issues.append('No buttons on /start — poor discoverability')

    # 2. Multiple commands implemented (15 pts)
    impl_cmds = [c for c in commands.values() if c.get('status') == 'implemented']
    if len(impl_cmds) >= 3:
        breakdown['commands'] = 15
        score += 15
        strengths.append(f'{len(impl_cmds)} commands implemented')
    elif len(impl_cmds) >= 1:
        breakdown['commands'] = 8
        score += 8
    else:
        breakdown['commands'] = 0
        issues.append('No commands detected beyond /start')

    # 3. Input flows exist (15 pts)
    if len(input_flows) >= 3:
        breakdown['input_flows'] = 15
        score += 15
        strengths.append(f'{len(input_flows)} input flows detected')
    elif len(input_flows) >= 1:
        breakdown['input_flows'] = 8
        score += 8
    else:
        breakdown['input_flows'] = 0
        issues.append('No input flows detected — bot may be view-only')

    # 4. No dead buttons (15 pts)
    if not dead_buttons:
        breakdown['no_dead_buttons'] = 15
        score += 15
        strengths.append('No dead buttons found')
    else:
        penalty = min(15, len(dead_buttons) * 5)
        breakdown['no_dead_buttons'] = max(0, 15 - penalty)
        score += max(0, 15 - penalty)
        issues.append(f'{len(dead_buttons)} dead/unresponsive buttons')

    # 5. Menu depth (10 pts) — deeper = more features
    depths = [m.get('depth', 0) for m in menus.values()]
    max_depth = max(depths) if depths else 0
    if max_depth >= 3:
        breakdown['menu_depth'] = 10
        score += 10
        strengths.append(f'Menu depth {max_depth} — rich navigation')
    elif max_depth >= 2:
        breakdown['menu_depth'] = 7
        score += 7
    else:
        breakdown['menu_depth'] = 3
        score += 3

    # 6. Has back buttons for navigation (10 pts)
    back_count = sum(
        1 for m in menus.values()
        for b in m.get('buttons', [])
        if any(kw in (b.get('text') or '').lower() for kw in ['kembali', 'back', 'batal', 'cancel'])
    )
    if back_count >= 3:
        breakdown['navigation'] = 10
        score += 10
        strengths.append('Good back-button navigation')
    elif back_count >= 1:
        breakdown['navigation'] = 5
        score += 5
    else:
        breakdown['navigation'] = 0
        issues.append('No back buttons — user may get stuck')

    # 7. Response speed (10 pts)
    avg_time = architecture.get('tech_hints', {}).get('avg_response_time_ms', 0)
    if avg_time and avg_time < 1000:
        breakdown['speed'] = 10
        score += 10
        strengths.append(f'Fast responses ({avg_time:.0f}ms avg)')
    elif avg_time and avg_time < 3000:
        breakdown['speed'] = 6
        score += 6
    else:
        breakdown['speed'] = 2
        score += 2

    # 8. External services / URL buttons (5 pts)
    if url_buttons:
        breakdown['external_links'] = 5
        score += 5
        strengths.append(f'{len(url_buttons)} external service links')
    else:
        breakdown['external_links'] = 0

    return {
        'score': min(score, max_score),
        'max_score': max_score,
        'breakdown': breakdown,
        'issues': issues,
        'strengths': strengths,
    }


async def extract_bot(bot_username, session_name='alwayscuanbos', quick=False, verbose=True):
    """Main extraction function with retries, timing, context navigation."""
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
        print(f'[*] Extracting {bot_username} as @{me.username}')
        print('=' * 60)

    architecture = {
        'bot': bot_username,
        'extracted_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'extracted_by': f'@{me.username}',
        'extractor_version': 'v2',
        'user_data': {},
        'commands': {},
        'menus': {},
        'input_flows': [],
        'dead_buttons': [],
        'url_buttons': [],
        'media_types_observed': set(),
        'tech_hints': {},
        'button_data_map': {},
    }

    timing_data = []
    all_responses = []

    # -- Helper: send message with timing + retry --
    async def send_and_wait(text, delay=2.5):
        """Send text to bot and return response with timing."""
        for attempt in range(MAX_RETRIES):
            try:
                t0 = time.monotonic()
                await client.send_message(bot_username, text)
                await asyncio.sleep(delay)
                msgs = await client.get_messages(bot_username, limit=5)
                t1 = time.monotonic()
                elapsed_ms = (t1 - t0 - delay) * 1000  # subtract sleep

                # Find the bot's latest response (skip our own messages)
                for m in msgs:
                    if m.sender_id != me.id:
                        timing_data.append(max(0, elapsed_ms))
                        return m, max(0, elapsed_ms)

                # Fallback: return first message
                timing_data.append(max(0, elapsed_ms))
                return msgs[0], max(0, elapsed_ms)
            except FloodWaitError as e:
                wait = e.seconds + 2
                if verbose:
                    print(f'  [!] FloodWait {e.seconds}s, waiting {wait}s... (attempt {attempt+1})')
                await asyncio.sleep(wait)
            except Exception as e:
                if verbose:
                    print(f'  [!] Error sending "{text}": {e} (attempt {attempt+1})')
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(2)
                else:
                    return None, 0
        return None, 0

    # -- Helper: click callback with timing + retry --
    async def click_and_wait(msg_id, data, delay=2.5):
        """Click a callback button and return response with timing."""
        for attempt in range(MAX_RETRIES):
            try:
                t0 = time.monotonic()
                await client(GetBotCallbackAnswerRequest(
                    peer=bot_username, msg_id=msg_id, data=data
                ))
                await asyncio.sleep(delay)
                msgs = await client.get_messages(bot_username, limit=5)
                t1 = time.monotonic()
                elapsed_ms = (t1 - t0 - delay) * 1000

                for m in msgs:
                    if m.sender_id != me.id:
                        timing_data.append(max(0, elapsed_ms))
                        return m, max(0, elapsed_ms)

                timing_data.append(max(0, elapsed_ms))
                return msgs[0], max(0, elapsed_ms)
            except FloodWaitError as e:
                wait = e.seconds + 2
                if verbose:
                    print(f'  [!] FloodWait {e.seconds}s, waiting {wait}s...')
                await asyncio.sleep(wait)
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    if verbose:
                        print(f'  [!] Callback error: {e} (retry {attempt+1})')
                    await asyncio.sleep(1.5)
                else:
                    if verbose:
                        print(f'  [!] Callback failed after {MAX_RETRIES} attempts: {e}')
                    return None, 0
        return None, 0

    # ============================
    # Phase 1: Command Discovery
    # ============================
    if verbose:
        print('\n[Phase 1] Command Discovery')
        print('-' * 40)

    for cmd in PROBE_COMMANDS:
        msg, resp_ms = await send_and_wait(cmd, delay=1.8)
        if not msg:
            continue

        resp_text = msg.text or ''
        media_type = detect_media_type(msg)

        # Detect if bot didn't handle the command
        is_echo = resp_text.strip() == cmd
        is_empty = not resp_text and not msg.buttons and not msg.media
        not_handled = is_echo or is_empty

        btns = extract_buttons(msg)
        user_data = extract_user_data(resp_text)
        input_state = detect_input_state(resp_text)

        if media_type:
            architecture['media_types_observed'].add(media_type)

        cmd_entry = {
            'text': resp_text[:500],
            'buttons': btns,
            'input_state': input_state,
            'response_time_ms': round(resp_ms, 1),
            'media_type': media_type,
            'status': 'not_implemented' if not_handled else 'implemented',
        }
        architecture['commands'][cmd] = cmd_entry
        architecture['user_data'].update(user_data)
        all_responses.append({'cmd': cmd, 'text': resp_text})

        if verbose:
            status_tag = 'SKIP' if not_handled else 'OK'
            preview = resp_text[:70].replace('\n', ' ')
            timing_tag = f' ({resp_ms:.0f}ms)' if resp_ms else ''
            print(f'  {cmd}: [{status_tag}]{timing_tag} {preview}{"..." if len(resp_text)>70 else ""}')

    # ============================
    # Phase 2: BFS Menu Tree with Context Navigation
    # ============================
    if verbose:
        print(f'\n[Phase 2] Menu Tree Traversal (BFS)')
        print('-' * 40)

    visited_callbacks = set()
    queue = deque()

    # Seed from /start
    start_msg, _ = await send_and_wait('/start', delay=2.0)
    if not start_msg:
        print('[!] Could not get /start response, aborting')
        await client.disconnect()
        return architecture

    start_btns = extract_buttons(start_msg)
    start_text = start_msg.text or ''
    architecture['menus']['__root__'] = {
        'trigger': '/start',
        'text': start_text[:500],
        'buttons': start_btns,
        'input_state': detect_input_state(start_text),
        'depth': 0,
        'path': [],
        'media_type': detect_media_type(start_msg),
    }

    # Track which msg_id corresponds to which context for contextual clicking
    # context_map: callback_data -> (parent_msg_id, parent_callback)
    context_map = {}

    for btn in start_btns:
        if btn['type'] == 'callback' and btn['data']:
            queue.append({
                'callback': btn['data'],
                'label': btn['text'],
                'depth': 1,
                'path': [btn['text']],
                'parent_msg_id': start_msg.id,
                'parent_callback': None,  # root level
            })
        elif btn['type'] == 'url' and btn['url']:
            architecture['url_buttons'].append({
                'text': btn['text'],
                'url': btn['url'],
                'depth': 0,
                'path': [],
            })

    # BFS traversal
    max_depth = 5 if not quick else 2
    while queue:
        item = queue.popleft()
        cb = item['callback']
        label = item['label']
        depth = item['depth']
        path = item['path']
        parent_msg_id = item['parent_msg_id']
        parent_callback = item.get('parent_callback')

        if cb in visited_callbacks:
            continue
        visited_callbacks.add(cb)
        architecture['button_data_map'][cb] = label

        if depth > max_depth:
            continue

        if verbose:
            indent = '  ' * depth
            print(f'  {indent}[{label}] -> {cb}')

        # -- Context-aware navigation --
        # Try clicking from the parent message first
        resp, resp_ms = await click_and_wait(parent_msg_id, cb.encode(), delay=2.0)

        # If that failed, reset to /start and try from root
        if not resp:
            if verbose:
                print(f'  {indent}  (context lost, resetting to /start)')
            start_msg, _ = await send_and_wait('/start', delay=1.5)
            if start_msg:
                # If this button is deeper than 1, we need to navigate through parents
                if parent_callback:
                    parent_resp, _ = await click_and_wait(start_msg.id, parent_callback.encode(), delay=1.5)
                    if parent_resp:
                        resp, resp_ms = await click_and_wait(parent_resp.id, cb.encode(), delay=2.0)
                else:
                    resp, resp_ms = await click_and_wait(start_msg.id, cb.encode(), delay=2.0)

        if not resp:
            architecture['dead_buttons'].append({
                'callback': cb,
                'label': label,
                'path': path,
                'reason': 'no_response',
            })
            continue

        resp_text = resp.text or ''
        resp_btns = extract_buttons(resp)
        input_state = detect_input_state(resp_text)
        media_type = detect_media_type(resp)

        if media_type:
            architecture['media_types_observed'].add(media_type)

        # Store in architecture
        menu_key = ' > '.join(path)
        architecture['menus'][menu_key] = {
            'trigger': cb,
            'text': resp_text[:500],
            'buttons': resp_btns,
            'input_state': input_state,
            'depth': depth,
            'path': path,
            'response_time_ms': round(resp_ms, 1),
            'media_type': media_type,
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

        # Check for buttons without callback data (dead buttons)
        for btn in resp_btns:
            if btn['type'] == 'callback' and not btn['data']:
                architecture['dead_buttons'].append({
                    'callback': None,
                    'label': btn['text'],
                    'path': path + [btn['text']],
                    'reason': 'no_callback_data',
                })

        # Add child buttons to queue
        for btn in resp_btns:
            if btn['type'] == 'callback' and btn['data'] and btn['data'] not in visited_callbacks:
                queue.append({
                    'callback': btn['data'],
                    'label': btn['text'],
                    'depth': depth + 1,
                    'path': path + [btn['text']],
                    'parent_msg_id': resp.id,
                    'parent_callback': cb,
                })
            elif btn['type'] == 'url' and btn['url']:
                architecture['url_buttons'].append({
                    'text': btn['text'],
                    'url': btn['url'],
                    'depth': depth,
                    'path': path,
                })

    # ============================
    # Phase 3: Tech Fingerprinting
    # ============================
    if verbose:
        print(f'\n[Phase 3] Tech Stack Analysis')
        print('-' * 40)

    architecture['tech_hints'] = fingerprint_tech(all_responses, timing_data)

    # Convert set to list for JSON serialization
    architecture['media_types_observed'] = sorted(architecture['media_types_observed'])

    # ============================
    # Phase 4: Summary + UX Score
    # ============================
    impl_cmds = [c for c, d in architecture['commands'].items() if d.get('status') == 'implemented']
    not_impl_cmds = [c for c, d in architecture['commands'].items() if d.get('status') == 'not_implemented']
    depths = [m.get('depth', 0) for m in architecture['menus'].values()]

    architecture['summary'] = {
        'total_menus': len(architecture['menus']),
        'total_callbacks': len(visited_callbacks),
        'total_input_flows': len(architecture['input_flows']),
        'dead_buttons': [db['label'] for db in architecture['dead_buttons']],
        'url_buttons': [ub['text'] for ub in architecture['url_buttons']],
        'deepest_level': max(depths) if depths else 0,
        'commands_implemented': impl_cmds,
        'commands_not_implemented': not_impl_cmds,
        'estimated_backend': architecture['tech_hints'].get('estimated_backend', 'unknown'),
        'avg_response_time_ms': architecture['tech_hints'].get('avg_response_time_ms', 0),
        'media_types_observed': architecture['media_types_observed'],
    }

    architecture['ux_score'] = compute_ux_score(architecture)

    if verbose:
        s = architecture['summary']
        ux = architecture['ux_score']
        print(f'\n[Phase 4] Results')
        print('=' * 60)
        print(f'  Commands implemented:     {len(impl_cmds)} {impl_cmds}')
        print(f'  Commands not implemented: {len(not_impl_cmds)} {not_impl_cmds}')
        print(f'  Menu nodes:               {s["total_menus"]}')
        print(f'  Unique callbacks:         {s["total_callbacks"]}')
        print(f'  Input flows:              {s["total_input_flows"]}')
        print(f'  Dead buttons:             {s["dead_buttons"]}')
        print(f'  URL buttons:              {s["url_buttons"]}')
        print(f'  Deepest level:            {s["deepest_level"]}')
        print(f'  Media types:              {s["media_types_observed"]}')
        print(f'  Avg response time:        {s["avg_response_time_ms"]:.0f}ms')
        print(f'  Estimated backend:        {s["estimated_backend"]}')
        print(f'  UX Score:                 {ux["score"]}/{ux["max_score"]}')
        print(f'  User data:                {architecture["user_data"]}')
        if ux['issues']:
            print(f'  Issues:')
            for issue in ux['issues']:
                print(f'    - {issue}')
        if ux['strengths']:
            print(f'  Strengths:')
            for s in ux['strengths']:
                print(f'    + {s}')

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

    for cmd, data in architecture['commands'].items():
        if data.get('status') == 'not_implemented':
            continue
        blueprint['commands'].append({
            'command': cmd,
            'handler': f'handle_{cmd.lstrip("/")}_command',
            'response': data['text'][:100],
            'has_keyboard': bool(data['buttons']),
        })

    for cb, label in architecture['button_data_map'].items():
        menu = next((m for m in architecture['menus'].values() if m.get('trigger') == cb), {})
        blueprint['callback_handlers'].append({
            'callback_data': cb,
            'label': label,
            'handler': f'handle_{cb.lower().replace("-","_")}',
            'response_type': menu.get('input_state') or 'menu',
            'has_sub_menu': bool(menu.get('buttons')),
        })

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
    parser = argparse.ArgumentParser(description='Bot Architecture Extractor v2')
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

    output_data = architecture
    if args.blueprint:
        blueprint = generate_blueprint(architecture)
        output_data = {'architecture': architecture, 'blueprint': blueprint}
        if not args.quiet:
            print('\n[Blueprint]')
            print(json.dumps(blueprint, indent=2, ensure_ascii=False))

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f'\nSaved to {args.output}')
    else:
        print('\n[Full Architecture]')
        print(json.dumps(output_data, indent=2, ensure_ascii=False)[:8000])


if __name__ == '__main__':
    asyncio.run(main())
