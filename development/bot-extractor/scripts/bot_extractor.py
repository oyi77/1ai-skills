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


def build_state_machine(architecture):
    """Build a complete state machine from the bot architecture."""
    states = {}

    menus = architecture.get('menus', {})
    commands = architecture.get('commands', {})
    input_flows = architecture.get('input_flows', [])
    button_map = architecture.get('button_data_map', {})

    # Build state for each menu
    for key, menu in menus.items():
        state_name = key if key != '__root__' else 'MAIN_MENU'
        transitions = {}

        for btn in menu.get('buttons', []):
            if btn['type'] == 'callback' and btn['data']:
                # Find the target menu for this callback
                target_menu = None
                for mk, mv in menus.items():
                    if mv.get('trigger') == btn['data']:
                        target_menu = mk if mk != '__root__' else 'MAIN_MENU'
                        break
                transitions[btn['text']] = {
                    'callback': btn['data'],
                    'next_state': target_menu or 'UNKNOWN',
                }
            elif btn['type'] == 'url':
                transitions[btn['text']] = {
                    'type': 'url',
                    'url': btn['url'],
                    'next_state': state_name,  # stays in same state
                }

        input_state = menu.get('input_state')

        states[state_name] = {
            'trigger': menu.get('trigger'),
            'transitions': transitions,
            'input_state': input_state,
            'timeout_fallback': 'MAIN_MENU' if input_state else None,
            'has_back_button': any(
                kw in (b.get('text') or '').lower()
                for b in menu.get('buttons', [])
                for kw in ['kembali', 'back', 'batal', 'cancel']
            ),
        }

    # Add command-triggered states
    for cmd, data in commands.items():
        if data.get('status') == 'implemented':
            cmd_state = f'CMD_{cmd.lstrip("/").upper()}'
            if cmd_state not in states:
                states[cmd_state] = {
                    'trigger': cmd,
                    'transitions': {},
                    'input_state': data.get('input_state'),
                    'timeout_fallback': 'MAIN_MENU',
                    'has_back_button': False,
                }

    # Detect issues
    issues = {
        'circular_states': [],
        'dead_ends': [],
        'missing_cancel_handlers': [],
    }

    for state_name, state in states.items():
        # Dead ends: states with no transitions and no input state
        if not state['transitions'] and not state['input_state']:
            issues['dead_ends'].append(state_name)

        # Missing cancel: input states without cancel/back
        if state['input_state'] and not state['has_back_button']:
            issues['missing_cancel_handlers'].append(state_name)

        # Circular: state that transitions back to itself
        for trans_name, trans in state['transitions'].items():
            if trans.get('next_state') == state_name:
                issues['circular_states'].append({
                    'state': state_name,
                    'via': trans_name,
                })

    return {
        'states': states,
        'total_states': len(states),
        'issues': issues,
    }


def analyze_payload_patterns(architecture):
    """Analyze input flow requirements and validation hints."""
    input_flows = architecture.get('input_flows', [])
    analyzed = []

    for flow in input_flows:
        prompt = flow.get('prompt', '')
        prompt_lower = prompt.lower()

        requirements = []

        # Size requirements
        size_match = re.search(r'(?:maksimal|max|maximum|up to)\s*(\d+)\s*(?:MB|KB|mb|kb)', prompt)
        if size_match:
            requirements.append(f'max_size: {size_match.group(0)}')

        # Format requirements
        formats = re.findall(r'\b(jpg|jpeg|png|webp|gif|mp4|mp3|pdf|heic|bmp|tiff|avif)\b', prompt_lower)
        if formats:
            requirements.append(f'formats: {", ".join(set(formats))}')

        # Dimension hints
        dim_match = re.search(r'(\d+)\s*[x×]\s*(\d+)', prompt)
        if dim_match:
            requirements.append(f'dimensions: {dim_match.group(0)}')

        # Ratio hints
        ratio_match = re.search(r'(\d+:\d+)', prompt)
        if ratio_match:
            requirements.append(f'ratio: {ratio_match.group(0)}')

        # Send-as hints
        if 'sebagai file' in prompt_lower or 'as document' in prompt_lower or 'sebagai dokumen' in prompt_lower:
            requirements.append('send_as: document (not compressed photo)')

        # Example/template hints
        example_match = re.search(r'(?:contoh|example|e\.g\.)[:.]?\s*["\']?([^"\'\n]{10,80})', prompt_lower)
        if example_match:
            requirements.append(f'example: {example_match.group(1).strip()}')

        analyzed.append({
            **flow,
            'requirements': requirements,
        })

    return analyzed


def analyze_message_formats(architecture):
    """Analyze text formatting patterns in bot messages."""
    menus = architecture.get('menus', {})
    results = {}

    for key, menu in menus.items():
        text = menu.get('text', '')
        if not text:
            continue

        analysis = {
            'length': len(text),
            'line_count': text.count('\n') + 1,
        }

        # Formatting markers
        formatting = []
        if '**' in text:
            formatting.append('bold_markdown')
        if '__' in text:
            formatting.append('italic_markdown')
        if '`' in text:
            formatting.append('code_markdown')
        if '<b>' in text or '<strong>' in text:
            formatting.append('bold_html')
        if '<i>' in text or '<em>' in text:
            formatting.append('italic_html')
        if '<code>' in text:
            formatting.append('code_html')
        analysis['formatting'] = formatting
        analysis['format_type'] = 'MarkdownV2' if any('markdown' in f for f in formatting) else ('HTML' if any('html' in f for f in formatting) else 'plain')

        # Emoji analysis
        emojis = re.findall(r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0000FE00-\U0000FE0F\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0]', text)
        emoji_categories = {}
        for e in emojis:
            cp = ord(e)
            if 0x1F600 <= cp <= 0x1F64F:
                cat = 'emoticons'
            elif 0x1F680 <= cp <= 0x1F6FF:
                cat = 'transport'
            elif 0x1F300 <= cp <= 0x1F5FF:
                cat = 'symbols_pictographs'
            elif 0x2600 <= cp <= 0x27BF:
                cat = 'misc_symbols'
            else:
                cat = 'other'
            emoji_categories[cat] = emoji_categories.get(cat, 0) + 1

        analysis['emojis_used'] = len(emojis)
        analysis['emoji_categories'] = emoji_categories

        # Text structure
        has_header = bool(re.match(r'^[^\n]*\*\*[^\n]+\*\*', text))
        has_bullets = bool(re.search(r'\n[•\-\*]\s', text))
        has_numbered = bool(re.search(r'\n\d+[.)]\s', text))
        has_cta = bool(re.search(r'(?:pilih|klik|tekan|select|click|tap|kirim|send)', text.lower()))

        structure_parts = []
        if has_header:
            structure_parts.append('header')
        if has_bullets or has_numbered:
            structure_parts.append('list')
        if has_cta:
            structure_parts.append('cta')

        analysis['structure'] = 'structured' if len(structure_parts) >= 2 else 'simple'
        analysis['structure_parts'] = structure_parts

        results[key] = analysis

    return results


def detect_bot_personality(architecture):
    """Analyze bot personality from all response texts."""
    menus = architecture.get('menus', {})
    commands = architecture.get('commands', {})

    all_texts = []
    for menu in menus.values():
        if menu.get('text'):
            all_texts.append(menu['text'])
    for cmd in commands.values():
        if cmd.get('text') and cmd.get('status') == 'implemented':
            all_texts.append(cmd['text'])

    combined = ' '.join(all_texts)
    combined_lower = combined.lower()
    total_words = len(combined.split())

    if total_words == 0:
        return {'note': 'No text to analyze'}

    # Language detection
    indo_words = ['silakan', 'pilih', 'kirim', 'kembali', 'batal', 'menu', 'yang', 'dan', 'untuk', 'dengan', 'ini', 'itu', 'sudah', 'belum', 'halo', 'selamat']
    eng_words = ['please', 'select', 'send', 'back', 'cancel', 'menu', 'click', 'choose', 'enter', 'welcome', 'hello']

    indo_count = sum(1 for w in indo_words if w in combined_lower)
    eng_count = sum(1 for w in eng_words if w in combined_lower)
    total_lang = indo_count + eng_count or 1

    indo_ratio = round(indo_count / total_lang, 2)
    eng_ratio = round(eng_count / total_lang, 2)

    if indo_ratio > 0.7:
        language = 'Indonesian'
    elif eng_ratio > 0.7:
        language = 'English'
    else:
        language = 'Mixed'

    # Formality
    formal_markers = ['silakan', 'terima kasih', 'mohon', 'dengan hormat', 'please', 'thank you', 'kindly']
    casual_markers = ['yuk', 'nih', 'dong', 'kak', 'bang', 'hey', 'yo', 'gue', 'lo', 'wkwk', 'hehe']

    formal_count = sum(1 for m in formal_markers if m in combined_lower)
    casual_count = sum(1 for m in casual_markers if m in combined_lower)

    if formal_count > casual_count * 2:
        formality = 'formal'
    elif casual_count > formal_count * 2:
        formality = 'casual'
    else:
        formality = 'semi-formal'

    # Tone
    urgent_words = ['segera', 'sekarang', 'urgent', 'immediately', 'cepat', 'buruan']
    friendly_words = ['halo', 'hai', 'selamat', 'welcome', 'hello', 'hi', 'kak']
    professional_words = ['informasi', 'layanan', 'fitur', 'service', 'feature', 'information']

    urgent = sum(1 for w in urgent_words if w in combined_lower)
    friendly = sum(1 for w in friendly_words if w in combined_lower)
    professional = sum(1 for w in professional_words if w in combined_lower)

    if friendly > professional and friendly > urgent:
        tone = 'friendly'
    elif professional > friendly:
        tone = 'professional'
    elif urgent > 0:
        tone = 'urgent'
    else:
        tone = 'neutral'

    # Emoji density
    emojis = re.findall(r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0000FE00-\U0000FE0F\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0]', combined)
    emoji_per_msg = len(emojis) / max(len(all_texts), 1)

    if emoji_per_msg > 3:
        emoji_density = 'high'
    elif emoji_per_msg > 1:
        emoji_density = 'medium'
    else:
        emoji_density = 'low'

    return {
        'language': language,
        'language_ratio': {'indonesian': indo_ratio, 'english': eng_ratio},
        'formality': formality,
        'formality_scores': {'formal': formal_count, 'casual': casual_count},
        'tone': tone,
        'emoji_density': emoji_density,
        'emoji_per_message': round(emoji_per_msg, 1),
        'total_unique_emojis': len(set(emojis)),
        'avg_message_length': round(total_words / max(len(all_texts), 1), 1),
    }


def generate_weakness_report(architecture):
    """Auto-generate competitive weaknesses from extraction data."""
    weaknesses = []

    commands = architecture.get('commands', {})
    menus = architecture.get('menus', {})
    input_flows = architecture.get('input_flows', [])
    dead_buttons = architecture.get('dead_buttons', [])
    url_buttons = architecture.get('url_buttons', [])
    ux = architecture.get('ux_score', {})

    # Missing standard commands
    standard_commands = {'/help': 'Help system', '/cancel': 'Cancel handler', '/settings': 'User settings', '/support': 'Support contact'}
    for cmd, purpose in standard_commands.items():
        if commands.get(cmd, {}).get('status') == 'not_implemented':
            weaknesses.append({
                'type': 'missing_feature',
                'detail': f'No {cmd} command ({purpose})',
                'severity': 'high' if cmd in ['/help', '/cancel'] else 'medium',
            })

    # Dead buttons
    if dead_buttons:
        weaknesses.append({
            'type': 'dead_buttons',
            'detail': f'{len(dead_buttons)} unresponsive buttons: {[db.get("label") for db in dead_buttons[:3]]}',
            'severity': 'high',
        })

    # UX friction: deep menus without shortcuts
    max_depth = max((m.get('depth', 0) for m in menus.values()), default=0)
    if max_depth > 3:
        weaknesses.append({
            'type': 'ux_friction',
            'detail': f'Deep menu structure (depth {max_depth}) without shortcuts',
            'severity': 'medium',
        })

    # Missing onboarding (if /start just shows menu without welcome)
    start = menus.get('__root__', {})
    start_text = start.get('text', '').lower()
    if not any(w in start_text for w in ['selamat datang', 'welcome', 'tutorial', 'panduan', 'guide']):
        weaknesses.append({
            'type': 'missing_onboarding',
            'detail': 'No clear onboarding or welcome tutorial for new users',
            'severity': 'low',
        })

    # Input flows without clear error handling
    for flow in input_flows:
        prompt = flow.get('prompt', '').lower()
        if not any(w in prompt for w in ['batal', 'cancel', 'salah', 'error', 'ulang', 'retry']):
            weaknesses.append({
                'type': 'missing_error_handling',
                'detail': f'Input flow "{flow.get("state")}" at {" > ".join(flow.get("path", []))} has no visible error/cancel guidance',
                'severity': 'medium',
            })

    # All commands redirect to same menu (lazy catch-all)
    impl_texts = set()
    for cmd, data in commands.items():
        if data.get('status') == 'implemented':
            impl_texts.add(data.get('text', '')[:100])
    if len(impl_texts) == 1 and len([c for c in commands.values() if c.get('status') == 'implemented']) > 2:
        weaknesses.append({
            'type': 'lazy_routing',
            'detail': 'All implemented commands return identical response (catch-all pattern)',
            'severity': 'medium',
        })

    # No multimedia
    if not architecture.get('media_types_observed'):
        weaknesses.append({
            'type': 'no_multimedia',
            'detail': 'Bot uses text-only responses with no photos/videos/documents',
            'severity': 'low',
        })

    return weaknesses


def estimate_clone_difficulty(architecture):
    """Estimate difficulty of cloning this bot."""
    breakdown = {}

    menus = architecture.get('menus', {})
    input_flows = architecture.get('input_flows', [])
    url_buttons = architecture.get('url_buttons', [])
    tech = architecture.get('tech_hints', {})
    commands = architecture.get('commands', {})

    menu_count = len(menus)
    flow_count = len(input_flows)
    unique_urls = set(ub.get('url', '') for ub in url_buttons)
    backend = tech.get('estimated_backend', 'sync')
    impl_count = sum(1 for c in commands.values() if c.get('status') == 'implemented')

    # Scoring
    breakdown['menu_complexity'] = 2 if menu_count > 20 else (1.5 if menu_count > 10 else (1 if menu_count > 5 else 0.5))
    breakdown['input_integrations'] = 3 if flow_count > 5 else (2 if flow_count > 2 else (1 if flow_count > 0 else 0))
    breakdown['external_integrations'] = 2 if len(unique_urls) > 5 else (1.5 if len(unique_urls) > 2 else (1 if len(unique_urls) > 0 else 0))
    breakdown['backend_complexity'] = 2 if backend == 'async_ai' else 1
    breakdown['command_scope'] = min(1, round(impl_count / 10, 1))

    score = round(min(sum(breakdown.values()), 10), 1)

    # Estimate hours
    estimated_hours = round(
        20 +  # base bot skeleton
        menu_count * 0.5 +
        flow_count * 4 +
        len(unique_urls) * 2 +
        impl_count * 1
    )

    challenges = [c for c in [
        f'{flow_count} input flows requiring AI/processing backends' if flow_count > 0 else None,
        f'{len(unique_urls)} external service integrations' if unique_urls else None,
        'Async AI backend detected - needs queue/webhook system' if backend == 'async_ai' else None,
        f'{menu_count} menu nodes to replicate' if menu_count > 10 else None,
    ] if c]

    return {
        'score': score,
        'max_score': 10,
        'breakdown': breakdown,
        'estimated_hours': estimated_hours,
        'estimated_days': round(estimated_hours / 8),
        'key_challenges': challenges,
    }


def generate_flowchart(architecture):
    """Generate mermaid.js graph TD flowchart from bot architecture."""
    lines = ['graph TD']

    menus = architecture.get('menus', {})
    input_flows = architecture.get('input_flows', [])
    url_buttons = architecture.get('url_buttons', [])

    node_map = {}
    counter = [0]

    def node_id(name):
        if name not in node_map:
            counter[0] += 1
            node_map[name] = f'N{counter[0]}'
        return node_map[name]

    def safe_label(text, max_len=40):
        return text.replace('"', "'").replace('\n', ' ')[:max_len]

    # Root
    root_id = node_id('__root__')
    lines.append(f'    {root_id}["/start"]')

    # Input states set for parallelogram detection
    input_state_triggers = set(f['trigger'] for f in input_flows)

    for key, menu in menus.items():
        if key == '__root__':
            continue

        nid = node_id(key)
        label = safe_label(key)
        trigger = menu.get('trigger', '')

        if trigger in input_state_triggers:
            # Parallelogram for input states
            state = menu.get('input_state', 'INPUT')
            lines.append(f'    {nid}[/"{label}\\n[{state}]"/]')
        elif menu.get('buttons'):
            # Rectangle for menus
            lines.append(f'    {nid}["{label}"]')
        else:
            # Stadium for outputs/dead ends
            lines.append(f'    {nid}(["{label}"])')

        # Connect to parent
        path = menu.get('path', [])
        if len(path) <= 1:
            lines.append(f'    {root_id} --> {nid}')
        else:
            parent_path = path[:-1]
            parent_key = parent_path[0] if len(parent_path) == 1 else ' > '.join(parent_path)
            # Find best parent
            if parent_key in node_map:
                lines.append(f'    {node_map[parent_key]} --> {nid}')
            else:
                # Try finding by first path element
                for mk in menus:
                    if mk == parent_path[0] or mk.endswith(parent_path[-1] if len(parent_path) > 0 else ''):
                        if mk in node_map:
                            lines.append(f'    {node_map[mk]} --> {nid}')
                            break
                else:
                    lines.append(f'    {root_id} --> {nid}')

    # URL buttons as dotted connections
    seen_urls = set()
    for ub in url_buttons:
        url_text = ub.get('text', 'Link')
        url = ub.get('url', '')
        if url in seen_urls:
            continue
        seen_urls.add(url)
        uid = node_id(f'url_{url}')
        label = safe_label(url_text, 35)
        lines.append(f'    {uid}>"{label}"]')

        path = ub.get('path', [])
        if path:
            parent_key = path[0] if len(path) == 1 else ' > '.join(path)
            if parent_key in node_map:
                lines.append(f'    {node_map[parent_key]} -.-> {uid}')

    return '\n'.join(lines)


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

    # ============================
    # Phase 5: Advanced Analysis
    # ============================
    if verbose:
        print(f'\n[Phase 5] Advanced Analysis')
        print('-' * 40)

    architecture['state_machine'] = build_state_machine(architecture)
    if verbose:
        sm = architecture['state_machine']
        print(f'  States: {sm["total_states"]}')
        print(f'  Dead ends: {sm["issues"]["dead_ends"]}')
        print(f'  Missing cancel: {sm["issues"]["missing_cancel_handlers"]}')

    architecture['input_flows'] = analyze_payload_patterns(architecture)

    architecture['format_analysis'] = analyze_message_formats(architecture)

    architecture['bot_personality'] = detect_bot_personality(architecture)
    if verbose:
        bp = architecture['bot_personality']
        print(f'  Language: {bp.get("language")} | Tone: {bp.get("tone")} | Formality: {bp.get("formality")}')
        print(f'  Emoji density: {bp.get("emoji_density")} ({bp.get("emoji_per_message")} per msg)')

    architecture['weakness_report'] = generate_weakness_report(architecture)
    if verbose:
        wr = architecture['weakness_report']
        print(f'  Weaknesses found: {len(wr)}')
        for w in wr[:3]:
            print(f'    [{w["severity"]}] {w["detail"]}')

    architecture['clone_difficulty'] = estimate_clone_difficulty(architecture)
    if verbose:
        cd = architecture['clone_difficulty']
        print(f'  Clone difficulty: {cd["score"]}/{cd["max_score"]}')
        print(f'  Estimated: {cd["estimated_hours"]}h ({cd["estimated_days"]} days)')

    architecture['mermaid_flowchart'] = generate_flowchart(architecture)

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

    # Clone difficulty estimation
    input_flows_count = len(architecture.get('input_flows', []))
    url_buttons_count = len(architecture.get('url_buttons', []))
    tech = architecture.get('tech_fingerprint', {})
    has_async_backend = tech.get('estimated_backend') == 'async_ai'

    difficulty_score = min(10, max(1,
        2  # base complexity
        + min(3, input_flows_count)  # more input flows = harder
        + min(2, url_buttons_count // 3)  # external integrations
        + (3 if has_async_backend else 0)  # async/AI backend is hard
    ))
    estimated_dev_hours = input_flows_count * 8 + url_buttons_count * 4 + 40

    blueprint['clone_difficulty'] = {
        'score': difficulty_score,
        'estimated_dev_hours': estimated_dev_hours,
        'factors': {
            'input_flows': input_flows_count,
            'url_buttons': url_buttons_count,
            'async_backend': has_async_backend,
        },
    }

    return blueprint


async def main():
    parser = argparse.ArgumentParser(description='Bot Architecture Extractor v2')
    parser.add_argument('bot', help='Bot username (e.g. @mybot)')
    parser.add_argument('--session', default='alwayscuanbos', help='Session name to use')
    parser.add_argument('--quick', action='store_true', help='Quick mode (depth 2 only)')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--blueprint', action='store_true', help='Generate clone blueprint')
    parser.add_argument('--quiet', action='store_true', help='Suppress verbose output')
    parser.add_argument('--flowchart', action='store_true', help='Generate mermaid flowchart')
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

    if args.flowchart:
        flowchart = generate_flowchart(architecture if not args.blueprint else output_data.get('architecture', architecture))
        if not args.quiet:
            print('\n[Mermaid Flowchart]')
            print(flowchart)
        # Save flowchart
        fc_path = (args.output or f'{args.bot.lstrip("@")}_flowchart.md').replace('.json', '_flowchart.md')
        with open(fc_path, 'w') as f:
            f.write(f'# Flowchart: {args.bot}\n\n```mermaid\n{flowchart}\n```\n')
        print(f'Flowchart saved to {fc_path}')

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f'\nSaved to {args.output}')
    else:
        print('\n[Full Architecture]')
        print(json.dumps(output_data, indent=2, ensure_ascii=False)[:8000])


if __name__ == '__main__':
    asyncio.run(main())
