---
name: bot-extractor
description: >
  Extract, clone, and improve any Telegram bot. Maps full architecture (menus,
  callbacks, commands, flows, input states), fingerprints tech stack, generates
  clone blueprint, and produces improvement recommendations.
  Use when: reverse-engineering competitor bots, cloning bot structures,
  auditing own bots, generating implementation code from any bot.
---
persona:
  name: "Domain Expert"
  title: "Master of Bot Extractor"
  expertise: ['Automation Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']



# Bot Extractor Skill

## Three Modes

| Mode | Command | Output |
|------|---------|--------|
| **Extract** | `--mode extract` | Full JSON architecture map |
| **Clone** | `--mode clone` | Python bot code ready to deploy |
| **Improve** | `--mode improve` | UX audit + improvement suggestions |

## Quick Start

```bash
# Extract any bot
python3 skills/bot-extractor/scripts/bot_extractor.py @targetbot

# Full extract + clone blueprint
python3 skills/bot-extractor/scripts/bot_extractor.py @targetbot --mode clone --output my_clone/

# UX improvement audit
python3 skills/bot-extractor/scripts/bot_extractor.py @targetbot --mode improve

# Use specific session
python3 skills/bot-extractor/scripts/bot_extractor.py @targetbot --session paijo
```

## Sessions Pool

```python
SESSIONS = {
    'paijo':          '/home/openclaw/.openclaw/workspace/.vilona/sessions/paijo',          # @codergaboets
    'alwayscuanbos':  '/home/openclaw/.openclaw/workspace/.vilona/sessions/alwayscuanbos',  # @alwayscuanbos
}
API_ID = 23913448
API_HASH = 'REDACTED_MD5_SECRET'
```

Add more sessions:
```bash
python3 scripts/telethon_add_session.py list              # list sessions
python3 scripts/telethon_add_session.py request-code +62xxx  # request OTP
python3 scripts/telethon_add_session.py add <name> <phone> <otp> [2fa_password]
```

---

## Mode: EXTRACT

Maps every reachable node of a bot via BFS traversal.

**What it captures:**
- All `/commands` and their responses
- Every inline button + `callback_data`
- Sub-menu trees (unlimited depth)
- Input flow states (WAITING_IMAGE / TEXT / FILE / VIDEO)
- User data exposed in bot messages (email, phone, ID)
- URL buttons → external service hints
- Response timing → processing type (sync vs async AI)

**Output JSON schema:**
```json
{
  "bot": "@targetbot",
  "extracted_at": "...",
  "user_data": { "email": "...", "telegram_id": "..." },
  "commands": {
    "/start": { "text": "...", "buttons": [...], "input_state": null },
    "/help": { "text": "...", "buttons": [...] }
  },
  "menus": {
    "__root__": { "trigger": "/start", "text": "...", "buttons": [...] },
    "Menu A": { "trigger": "cb_a", "text": "...", "buttons": [...], "depth": 1 },
    "Menu A > Sub B": { "trigger": "cb_b", "text": "...", "depth": 2 }
  },
  "input_flows": [
    { "trigger": "cb_x", "state": "WAITING_IMAGE", "path": ["Menu", "Sub"] }
  ],
  "button_data_map": { "cb_a": "Button Label", "cb_b": "Sub Label" },
  "tech_hints": {
    "framework": "aiogram",
    "max_processing_min": 5,
    "external_urls": ["https://api.openai.com/..."]
  }
}
```

---

## Mode: CLONE

Generates a working Python bot from extracted architecture.

**Output structure:**
```
output_dir/
├── bot.py              # Main bot entry point
├── handlers/
│   ├── commands.py     # /start, /help, etc.
│   ├── callbacks.py    # All inline button handlers
│   └── messages.py     # Input state handlers
├── keyboards/
│   └── menus.py        # All InlineKeyboardMarkup definitions
├── states.py           # FSM state definitions
├── config.py           # Token, API keys placeholders
└── requirements.txt    # Dependencies
```

**Example generated handler:**
```python
# handlers/callbacks.py (auto-generated)

@router.callback_query(F.data == "menu_generate_video")
async def handle_menu_generate_video(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        "🎬 **Buat Video**\n\nPilih mode dan rasio video:",
        reply_markup=video_menu_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "video_i2v_portrait")
async def handle_video_i2v_portrait(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(GenerateStates.WAITING_IMAGE)
    await callback.message.edit_text(
        "🎬 **Image-to-Video** 📱\n\n🖼️ Silakan kirim foto:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
```

---

## Mode: IMPROVE

Audits extracted architecture and generates improvement recommendations.

**Audit criteria:**
| Check | Good | Bad |
|-------|------|-----|
| Menu depth | ≤ 3 levels | > 3 (too deep) |
| Buttons per row | 2-3 | 1 (wastes space) or 5+ (cluttered) |
| Back buttons | Every menu has one | Dead ends |
| Error handling | /cancel works | Stuck states |
| CTA clarity | Clear action text | Vague labels |
| Onboarding | /start has tutorial | Drops user cold |
| Commands coverage | /help exists | Only /start |

**Sample improvement output:**
```
🔍 UX AUDIT: @vidabot_generator_bot

Score: 72/100

Issues:
  🔴 [CRITICAL] "UGC Lipsync" buttons have no callback_data (dead buttons)
  🟡 [MEDIUM]  /help command not implemented (echo only)
  🟡 [MEDIUM]  No /cancel command during input states
  🟢 [GOOD]    Consistent back navigation on all menus
  🟢 [GOOD]    Clear input prompts for image/text flows

Recommendations:
  1. Fix dead buttons → add actual handlers for UGC Lipsync
  2. Add /help with feature list
  3. Add /cancel that works in any state
  4. Add progress indicator during video generation (currently generic text)
  5. Add /status command to check ongoing generations
```

---

## Extraction Methodology (BFS)

```
1. COMMAND DISCOVERY
   Send all probe commands → record responses
   Probe list: /start /help /admin /settings /status /credits /info /menu /panel /cancel

2. BUTTON TREE (BFS)
   Queue = [/start buttons]
   While queue not empty:
     Pop callback_data
     Click it (from /start context)
     Record response + sub-buttons
     Add unseen sub-buttons to queue

3. INPUT FLOW DETECTION
   After each click, check for input waiting patterns:
   - "kirim foto/send photo" → WAITING_IMAGE
   - "ketik/type" → WAITING_TEXT
   - "kirim file/send document" → WAITING_FILE

4. TECH FINGERPRINTING
   - Response time < 500ms → sync/simple
   - Response time > 2s → async/AI backend
   - URL buttons → external APIs
   - Error message patterns → framework detection
   - File naming conventions → storage patterns

5. USER DATA COLLECTION
   - Regex scan all responses for email, phone, ID, name
```

---

## Case Studies

### @vidabot_generator_bot (extracted 2026-03-21)

**Architecture:**
```
/start (4 main menus)
├── Buat Gambar Model → COMING SOON
├── Buat Video (4 sub-modes: I2V/T2V × Portrait/Landscape)
│   └── Each → input flow (WAITING_IMAGE or WAITING_TEXT)
├── Shortcut I2V (2 sub-modes: Portrait/Landscape)
└── Tools Lain
    ├── UGC Lipsync × 2 (DEAD BUTTONS - no callback)
    └── Convert JPG (WAITING_FILE)
```

**Key findings:**
- Email registered: `ketananna@yahoo.com`
- Video generation: 1-5 minutes (cloud AI inference)
- Dead buttons: UGC Lipsync (callback_data = None)
- Missing: /help, /cancel, /status
- Tech: Likely aiogram or python-telegram-bot, async AI backend

**Clone estimate:** ~300 lines Python + AI API integration

---

## Automated Workflow (Vilona can run this)

```python
# Step 1: Extract
arch = await extract_bot('@targetbot', session='alwayscuanbos')

# Step 2: Save
save_json(arch, 'skills/bot-extractor/references/targetbot_arch.json')

# Step 3: Generate clone
generate_clone(arch, output_dir='projects/targetbot_clone/')

# Step 4: Improve
audit = generate_improvement_report(arch)
print(audit)
```

## Script Reference

| Script | Description |
|--------|-------------|
| `bot_extractor.py` | Main extraction + clone + improve engine |
| `session_manager.py` | Add/list/test Telethon sessions |
| `bot_cloner.py` | Generate full Python bot from architecture JSON |
| `bot_auditor.py` | UX audit + improvement recommendations |

## References

```
skills/bot-extractor/references/
├── vidabot_generator_bot_arch.json    # @vidabot_generator_bot full architecture
└── [future extracted bots here]
```
