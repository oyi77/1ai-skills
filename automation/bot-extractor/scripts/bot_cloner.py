#!/usr/bin/env python3
"""
Bot Cloner — Generate working Python bot code from extracted architecture JSON.

Usage:
  python3 bot_cloner.py architecture.json --output ./my_bot/
  python3 bot_cloner.py architecture.json --framework aiogram
  python3 bot_cloner.py architecture.json --framework ptb  # python-telegram-bot
"""

import json, sys, os, argparse
from pathlib import Path


def slugify(text):
    """Convert text to valid Python identifier."""
    import re
    return re.sub(r'[^a-z0-9_]', '_', text.lower().strip()).strip('_')


def generate_aiogram_bot(arch: dict, output_dir: str):
    """Generate aiogram 3.x bot from architecture."""
    outpath = Path(output_dir)
    outpath.mkdir(parents=True, exist_ok=True)
    (outpath / 'handlers').mkdir(exist_ok=True)
    (outpath / 'keyboards').mkdir(exist_ok=True)

    bot_name = arch['bot'].lstrip('@')
    menus = arch.get('menus', {})
    callbacks = arch.get('button_data_map', {})
    input_flows = arch.get('input_flows', [])
    commands = arch.get('commands', {})

    # --- config.py ---
    config = f'''# config.py — Generated for {arch["bot"]}
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
BOT_NAME = "{bot_name}"

# Add your AI/API credentials here
# AI_API_KEY = "..."
'''
    (outpath / 'config.py').write_text(config)

    # --- states.py ---
    states_set = set()
    for flow in input_flows:
        states_set.add(flow['state'])

    states_code = '''from aiogram.fsm.state import State, StatesGroup

class BotStates(StatesGroup):
'''
    if states_set:
        for s in sorted(states_set):
            states_code += f'    {s} = State()\n'
    else:
        states_code += '    IDLE = State()\n'

    (outpath / 'states.py').write_text(states_code)

    # --- keyboards/menus.py ---
    kb_code = '''from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def make_keyboard(buttons: list[tuple]) -> InlineKeyboardMarkup:
    """buttons: list of (text, callback_data) tuples, None data = back button"""
    rows = []
    for text, data in buttons:
        rows.append([InlineKeyboardButton(text=text, callback_data=data or "noop")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

'''
    # Generate keyboard functions per menu
    for menu_key, menu_data in menus.items():
        fn_name = 'keyboard_root' if menu_key == '__root__' else f'keyboard_{slugify(menu_key)}'
        btns = menu_data.get('buttons', [])
        if not btns:
            continue

        kb_code += f'def {fn_name}() -> InlineKeyboardMarkup:\n'
        kb_code += '    return InlineKeyboardMarkup(inline_keyboard=[\n'
        for btn in btns:
            data = btn.get('data') or 'noop'
            text = btn['text'].replace("'", "\\'")
            kb_code += f'        [InlineKeyboardButton(text=\'{text}\', callback_data=\'{data}\')],\n'
        kb_code += '    ])\n\n'

    (outpath / 'keyboards' / 'menus.py').write_text(kb_code)
    (outpath / 'keyboards' / '__init__.py').write_text('')

    # --- handlers/commands.py ---
    cmd_code = '''from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.menus import keyboard_root

router = Router()

'''
    for cmd, data in commands.items():
        fn_name = f'handle_{slugify(cmd.lstrip("/"))}'
        text = (data.get('text') or '').replace('"', '\\"').replace('\n', '\\n')[:300]
        has_kb = bool(data.get('buttons'))

        cmd_code += f'@router.message(Command("{cmd.lstrip("/")}"))\n'
        cmd_code += f'async def {fn_name}(message: Message):\n'
        if cmd == '/start' and has_kb:
            cmd_code += f'    await message.answer(\n'
            cmd_code += f'        "{text}",\n'
            cmd_code += f'        reply_markup=keyboard_root(),\n'
            cmd_code += f'        parse_mode="Markdown"\n'
            cmd_code += f'    )\n\n'
        else:
            cmd_code += f'    await message.answer("{text}", parse_mode="Markdown")\n\n'

    (outpath / 'handlers' / 'commands.py').write_text(cmd_code)

    # --- handlers/callbacks.py ---
    cb_code = '''from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import BotStates
import keyboards.menus as kb

router = Router()

@router.callback_query(F.data == "noop")
async def handle_noop(callback: CallbackQuery):
    await callback.answer("Coming soon!", show_alert=True)

'''
    # Input flow triggers
    flow_triggers = {f['trigger']: f for f in input_flows}

    for cb_data, label in callbacks.items():
        fn_name = f'handle_{slugify(cb_data)}'
        menu = next((m for m in menus.values() if m.get('trigger') == cb_data), {})
        text = (menu.get('text') or label).replace('"', '\\"').replace('\n', '\\n')[:300]
        kb_fn = f'kb.keyboard_{slugify(cb_data)}' if cb_data in [m.get('trigger') for m in menus.values()] else None
        is_input_flow = cb_data in flow_triggers

        cb_code += f'@router.callback_query(F.data == "{cb_data}")\n'
        cb_code += f'async def {fn_name}(callback: CallbackQuery, state: FSMContext):\n'
        cb_code += f'    await callback.answer()\n'

        if is_input_flow:
            flow = flow_triggers[cb_data]
            state_name = flow['state']
            cb_code += f'    await state.set_state(BotStates.{state_name})\n'

        if kb_fn and menu.get('buttons'):
            cb_code += f'    await callback.message.edit_text(\n'
            cb_code += f'        "{text}",\n'
            try:
                kb_actual = f'kb.keyboard_{slugify(cb_data)}()'
                cb_code += f'        reply_markup={kb_actual},\n'
            except:
                pass
            cb_code += f'        parse_mode="Markdown"\n'
            cb_code += f'    )\n\n'
        else:
            cb_code += f'    await callback.message.edit_text("{text}", parse_mode="Markdown")\n\n'

    (outpath / 'handlers' / 'callbacks.py').write_text(cb_code)

    # --- handlers/messages.py (input state handlers) ---
    msg_code = '''from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import BotStates

router = Router()

# TODO: Implement your AI/processing logic in each handler below

'''
    for flow in input_flows:
        state = flow['state']
        fn_name = f'handle_{slugify(state)}_input'
        expected = state.replace('WAITING_', '').lower()

        msg_code += f'@router.message(BotStates.{state})\n'
        msg_code += f'async def {fn_name}(message: Message, state: FSMContext):\n'

        if state == 'WAITING_IMAGE':
            msg_code += '    if not message.photo:\n'
            msg_code += '        await message.reply("❌ Kirim foto ya, bukan teks.")\n'
            msg_code += '        return\n'
            msg_code += '    photo = message.photo[-1]  # Highest resolution\n'
            msg_code += '    await message.reply("⏳ Memproses gambar...")\n'
            msg_code += '    # TODO: Call your AI API here\n'
            msg_code += '    # result = await generate_video_from_image(photo.file_id)\n'
            msg_code += '    # await message.reply_video(result)\n'
        elif state == 'WAITING_TEXT':
            msg_code += '    text = message.text\n'
            msg_code += '    await message.reply("⏳ Memproses teks...")\n'
            msg_code += '    # TODO: Call your AI API here\n'
            msg_code += '    # result = await generate_video_from_text(text)\n'
            msg_code += '    # await message.reply_video(result)\n'
        elif state == 'WAITING_FILE':
            msg_code += '    if not message.document:\n'
            msg_code += '        await message.reply("❌ Kirim sebagai FILE/DOKUMEN ya.")\n'
            msg_code += '        return\n'
            msg_code += '    doc = message.document\n'
            msg_code += '    await message.reply("⏳ Mengkonversi file...")\n'
            msg_code += '    # TODO: Download and convert file\n'
            msg_code += '    # result = await convert_to_jpg(doc.file_id)\n'
        else:
            msg_code += f'    # Handle {expected} input\n'
            msg_code += '    await message.reply("⏳ Memproses...")\n'
            msg_code += '    # TODO: Add your processing logic here\n'

        msg_code += '    await state.clear()\n\n'

    (outpath / 'handlers' / 'messages.py').write_text(msg_code)
    (outpath / 'handlers' / '__init__.py').write_text('')

    # --- bot.py (main entry) ---
    bot_main = f'''#!/usr/bin/env python3
"""
{bot_name} Bot — Auto-generated by bot-extractor skill
Source: {arch["bot"]}
Generated: {arch.get("extracted_at", "unknown")}
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import commands, callbacks, messages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Register routers
    dp.include_router(commands.router)
    dp.include_router(callbacks.router)
    dp.include_router(messages.router)

    logger.info("Bot starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
'''
    (outpath / 'bot.py').write_text(bot_main)

    # --- requirements.txt ---
    reqs = '''aiogram>=3.0.0
aiohttp>=3.8.0
python-dotenv>=1.0.0
'''
    (outpath / 'requirements.txt').write_text(reqs)

    print(f'✅ Bot generated at: {output_dir}')
    print(f'   Files: {[f.name for f in outpath.rglob("*.py")]}')
    print(f'\nNext steps:')
    print(f'  1. Set BOT_TOKEN in {output_dir}/config.py')
    print(f'  2. Implement AI logic in {output_dir}/handlers/messages.py')
    print(f'  3. pip install -r {output_dir}/requirements.txt')
    print(f'  4. python3 {output_dir}/bot.py')


def generate_improvement_report(arch: dict) -> str:
    """Generate UX improvement audit report."""
    report = [f'🔍 UX AUDIT: {arch["bot"]}', '=' * 40, '']
    score = 100
    issues = []
    goods = []

    menus = arch.get('menus', {})
    callbacks = arch.get('button_data_map', {})
    commands = arch.get('commands', {})
    input_flows = arch.get('input_flows', [])

    # Check: /help exists
    if '/help' not in commands or commands['/help'].get('text','').strip() == '/help':
        issues.append(('MEDIUM', '/help command not implemented'))
        score -= 10
    else:
        goods.append('/help command exists')

    # Check: /cancel exists
    if '/cancel' not in commands:
        issues.append(('MEDIUM', 'No /cancel command for input states'))
        score -= 10
    else:
        goods.append('/cancel command exists')

    # Check: dead buttons (no callback_data)
    dead = []
    for menu_key, menu in menus.items():
        for btn in menu.get('buttons', []):
            if not btn.get('data') and not btn.get('url'):
                dead.append(f'{btn["text"]} in {menu_key}')
    if dead:
        issues.append(('CRITICAL', f'Dead buttons (no action): {dead}'))
        score -= 20

    # Check: back buttons
    menus_without_back = []
    for menu_key, menu in menus.items():
        if menu_key == '__root__':
            continue
        btns = menu.get('buttons', [])
        has_back = any('back' in (b.get('data') or '').lower() or
                      'kembali' in b.get('text','').lower() or
                      'cancel' in (b.get('data') or '').lower()
                      for b in btns)
        if not has_back and btns:
            menus_without_back.append(menu_key)
    if menus_without_back:
        issues.append(('MEDIUM', f'Menus without back button: {len(menus_without_back)}'))
        score -= 5
    else:
        goods.append('All menus have back navigation')

    # Check: menu depth
    max_depth = max((m.get('depth', 0) for m in menus.values()), default=0)
    if max_depth > 3:
        issues.append(('MEDIUM', f'Menu too deep: {max_depth} levels (recommend ≤3)'))
        score -= 10
    else:
        goods.append(f'Good menu depth: {max_depth} levels')

    # Check: onboarding
    start = menus.get('__root__', {})
    start_text = start.get('text', '')
    if len(start_text) < 50:
        issues.append(('LOW', 'Thin onboarding text — add feature overview in /start'))
        score -= 5
    else:
        goods.append('Good onboarding text in /start')

    # Check: input flow clarity
    for flow in input_flows:
        prompt = flow.get('prompt', '')
        if len(prompt) < 30:
            issues.append(('LOW', f'Vague input prompt in {flow["trigger"]}'))
            score -= 3

    # Build report
    report.append(f'Score: {max(0, score)}/100\n')

    if issues:
        report.append('Issues Found:')
        for sev, msg in sorted(issues, key=lambda x: ['CRITICAL','MEDIUM','LOW'].index(x[0])):
            icon = {'CRITICAL': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}[sev]
            report.append(f'  {icon} [{sev}] {msg}')

    if goods:
        report.append('\nGood Practices:')
        for g in goods:
            report.append(f'  ✅ {g}')

    report.append('\nRecommendations:')
    for i, (sev, msg) in enumerate(issues, 1):
        report.append(f'  {i}. Fix: {msg}')

    return '\n'.join(report)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('architecture', help='Path to architecture JSON file')
    parser.add_argument('--output', default='./generated_bot', help='Output directory')
    parser.add_argument('--framework', default='aiogram', choices=['aiogram', 'ptb'])
    parser.add_argument('--improve', action='store_true', help='Generate improvement report only')
    args = parser.parse_args()

    with open(args.architecture) as f:
        arch = json.load(f)

    if args.improve:
        print(generate_improvement_report(arch))
    else:
        if args.framework == 'aiogram':
            generate_aiogram_bot(arch, args.output)
        else:
            print('PTB (python-telegram-bot) generator coming soon. Use --framework aiogram for now.')
