---
name: bot-extractor
description: >
  Extract, reverse-engineer, and clone full architecture from any Telegram bot.
  Maps all menus, buttons, callback data, commands, flows, and API endpoints.
  Use when: analyzing competitor bots, cloning bot structures, understanding bot UX flows.
---

# Bot Extractor Skill

## What It Does

Systematically explores a Telegram bot using Telethon user sessions to:
1. **Map full menu tree** — all buttons, callback_data, text responses
2. **Trace all flows** — click every button, follow every path
3. **Extract commands** — /start, /help, /admin, /settings, etc.
4. **Detect tech stack** — backend hints, API providers, webhook patterns
5. **Generate clone blueprint** — full JSON architecture + implementation guide

## Sessions Available

```python
SESSIONS = {
    'paijo': '/home/openclaw/.openclaw/workspace/.vilona/sessions/paijo',           # @codergaboets
    'alwayscuanbos': '/home/openclaw/.openclaw/workspace/.vilona/sessions/alwayscuanbos',  # @alwayscuanbos
}
API_ID = 23913448
API_HASH = '78d168f985edf365a5cd9679a917a0b2'
```

## Usage

```bash
# Full extraction (recommended)
python3 skills/bot-extractor/scripts/bot_extractor.py @botname --session alwayscuanbos

# Quick map (menus only, no deep dive)
python3 skills/bot-extractor/scripts/bot_extractor.py @botname --quick

# Save architecture to file
python3 skills/bot-extractor/scripts/bot_extractor.py @botname --output architecture.json

# Generate clone blueprint
python3 skills/bot-extractor/scripts/bot_extractor.py @botname --blueprint
```

## Case Study: @vidabot_generator_bot

### Architecture Map

```
/start
├── 🖼️ Buat Gambar Model → menu_generate_image
│   └── [Coming Soon] → back_to_main_menu
├── 🎬 Buat Video → menu_generate_video
│   ├── 🖼️📱 Image Portrait → video_i2v_portrait
│   │   └── [Send photo] → bot waits for image input → generates video
│   ├── 🖼️🖥️ Image Landscape → video_i2v_landscape
│   │   └── [Send photo] → generates landscape video
│   ├── 📝📱 Text Portrait → video_t2v_portrait
│   │   └── [Type description] → generates video from text
│   ├── 📝🖥️ Text Landscape → video_t2v_landscape
│   └── 🔙 Kembali → back_to_main_menu
├── 🎬 Shortcut: Image to Video → shortcut_i2v
│   ├── 📱 Portrait (9:16) → shortcut_i2v_portrait
│   ├── 🖥️ Landscape (16:9) → shortcut_i2v_landscape
│   └── 🔙 Kembali → back_to_main_menu
└── 🛠️ Tools Lain → tools_menu
    ├── 🎨 UGC Lipsync AISTUDIO → [no callback_data, likely URL button]
    ├── ✨ UGC Lipsync Ringan → [no callback_data, likely URL button]
    ├── 🖼️ Convert Gambar ke JPG → tools_convert_jpg
    │   └── [Send file as document] → converts to JPG
    └── ◀️ Kembali → back_to_admin_start
```

### User Data Exposed
- Email: `ketananna@yahoo.com`
- Telegram ID: `157228659`

### Tech Stack Analysis
- **Platform**: Telegram Bot (python-telegram-bot or aiogram likely)
- **Video gen**: External AI API (takes 1-5 min per video → cloud inference)
- **Storage**: Files sent directly via Telegram (no CDN exposed)
- **Auth**: Telegram user ID based (no separate login)
- **State management**: Conversation states (bot waits for user input after menu select)
- **Admin panel**: `/admin` command exists but locked (separate admin session)

### Callback Data Patterns
```
menu_*          → main menu navigation
video_*         → video generation flows
shortcut_*      → quick access flows
tools_*         → utility tools
back_to_*       → navigation back
```

### Input Flows Detected
| Flow | Trigger | Expected Input | Output |
|------|---------|----------------|--------|
| I2V Portrait | video_i2v_portrait | Photo (image) | Video 9:16 |
| I2V Landscape | video_i2v_landscape | Photo (image) | Video 16:9 |
| T2V Portrait | video_t2v_portrait | Text description | Video 9:16 |
| T2V Landscape | video_t2v_landscape | Text description | Video 16:9 |
| Convert JPG | tools_convert_jpg | File/document | JPG file |

## Clone Blueprint

To replicate this bot:

```python
# 1. State machine
STATES = {
    'IDLE': 'waiting for menu selection',
    'WAITING_IMAGE': 'user must send photo',
    'WAITING_TEXT': 'user must send text description',
    'WAITING_FILE': 'user must send document',
    'GENERATING': 'AI processing in progress',
}

# 2. Callback handlers
CALLBACKS = {
    'menu_generate_image': show_coming_soon,
    'menu_generate_video': show_video_menu,
    'video_i2v_portrait': start_i2v_flow(ratio='9:16'),
    'video_i2v_landscape': start_i2v_flow(ratio='16:9'),
    'video_t2v_portrait': start_t2v_flow(ratio='9:16'),
    'video_t2v_landscape': start_t2v_flow(ratio='16:9'),
    'shortcut_i2v': show_shortcut_menu,
    'shortcut_i2v_portrait': start_i2v_flow(ratio='9:16'),
    'shortcut_i2v_landscape': start_i2v_flow(ratio='16:9'),
    'tools_menu': show_tools,
    'tools_convert_jpg': start_jpg_convert,
    'back_to_main_menu': show_main_menu,
    'back_to_admin_start': show_tools,  # same as tools for non-admin
}

# 3. Message handlers (by state)
# When state=WAITING_IMAGE → receive photo → call AI API → return video
# When state=WAITING_TEXT → receive text → call AI API → return video
# When state=WAITING_FILE → receive document → convert → return JPG
```

## Extraction Methodology

### Phase 1: Command Discovery
```python
commands = ['/start', '/help', '/admin', '/settings', '/status', 
            '/credits', '/info', '/menu', '/cancel', '/about']
```

### Phase 2: Button Tree Traversal (BFS)
```python
# Start from /start
# For each button with callback_data:
#   - Click it, record response
#   - Extract new buttons from response
#   - Add unseen buttons to queue
# Repeat until queue empty
```

### Phase 3: Input Flow Detection
```python
# After each response, check if bot is waiting for input:
# - "Silakan kirim foto" → WAITING_IMAGE
# - "Silakan ketik" → WAITING_TEXT
# - "Kirim sebagai FILE" → WAITING_FILE
# Record each input state and its trigger
```

### Phase 4: Tech Stack Fingerprinting
```python
# Timing: response time → inference time
# Error messages: reveal framework
# URL buttons: reveal external services
# File naming: reveal storage patterns
# Bot description: /getMyCommands API
```

## Script Reference

| Script | Purpose |
|--------|---------|
| `bot_extractor.py` | Main extraction script |
| `session_manager.py` | Multi-session Telethon pool |
| `bot_cloner.py` | Generate clone from architecture JSON |
