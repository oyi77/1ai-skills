#!/usr/bin/env python3
"""Generate python-telegram-bot v20+ bot from architecture JSON."""

import json
import os
import sys
import textwrap


def load_architecture(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_func_name(s):
    """Convert string to valid Python function name."""
    name = s.lstrip("/").replace("-", "_").replace(" ", "_").replace(".", "_")
    name = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
    if name and name[0].isdigit():
        name = "cmd_" + name
    return name.lower() or "unknown"


def safe_state_name(s):
    if not s:
        return None
    return s.upper().replace(" ", "_").replace("-", "_")


def generate_bot_py(arch):
    """Generate main bot.py with ApplicationBuilder."""
    bot_name = arch.get("bot", "my_bot")
    commands = arch.get("commands", {})
    menus = arch.get("menus", {})
    input_flows = arch.get("input_flows", [])

    has_callbacks = bool(menus)
    has_messages = bool(input_flows)
    has_conversation = bool(input_flows)

    imports = [
        'import logging',
        'from telegram.ext import ApplicationBuilder, CommandHandler',
    ]
    if has_callbacks:
        imports.append('from telegram.ext import CallbackQueryHandler')
    if has_conversation:
        imports.append('from telegram.ext import ConversationHandler, MessageHandler, filters')
    if has_messages and not has_conversation:
        imports.append('from telegram.ext import MessageHandler, filters')

    imports.append('')
    imports.append('from handlers.commands import *')
    if has_callbacks:
        imports.append('from handlers.callbacks import *')
    if has_messages:
        imports.append('from handlers.messages import *')

    # Collect states for ConversationHandler
    states = set()
    for flow in input_flows:
        st = safe_state_name(flow.get("state"))
        if st:
            states.add(st)

    state_consts = ""
    if states:
        state_consts = "\n# Conversation states\n"
        for i, st in enumerate(sorted(states)):
            state_consts += f"{st} = {i}\n"

    # Build command handlers
    cmd_lines = []
    for cmd in commands:
        fn = safe_func_name(cmd)
        cmd_lines.append(f'    app.add_handler(CommandHandler("{fn}", cmd_{fn}))')

    # Build callback handler or conversation handler
    conv_lines = []
    callback_lines = []

    if has_conversation and states:
        # Build ConversationHandler with entry points from menus and states from input flows
        entry_points = []
        if menus:
            entry_points.append("CallbackQueryHandler(callback_handler)")
        for cmd in commands:
            fn = safe_func_name(cmd)
            if any(commands[cmd].get("input_state") for _ in [1]):
                pass  # handled via conversation

        state_handlers = {}
        for flow in input_flows:
            st = safe_state_name(flow.get("state"))
            if st:
                state_handlers.setdefault(st, [])

        conv_states = "{\n"
        for st in sorted(states):
            handler_name = f"handle_{st.lower()}"
            conv_states += f"        {st}: [MessageHandler(filters.ALL, {handler_name})],\n"
        conv_states += "    }"

        conv_lines = [
            "    conv_handler = ConversationHandler(",
            "        entry_points=[CallbackQueryHandler(callback_handler)],",
            f"        states={conv_states},",
            "        fallbacks=[CommandHandler('cancel', cmd_cancel)],",
            "    )",
            "    app.add_handler(conv_handler)",
        ]
    elif has_callbacks:
        callback_lines = ["    app.add_handler(CallbackQueryHandler(callback_handler))"]

    code = f'''#!/usr/bin/env python3
"""{bot_name} — generated with bot_cloner_ptb.py (python-telegram-bot v20+)."""

{chr(10).join(imports)}
{state_consts}

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
{chr(10).join(cmd_lines) if cmd_lines else "    pass  # no commands detected"}

{chr(10).join(conv_lines)}
{chr(10).join(callback_lines)}

    logger.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
'''
    return code


def generate_commands_py(arch):
    """Generate handlers/commands.py."""
    commands = arch.get("commands", {})
    input_flows = arch.get("input_flows", [])

    lines = [
        '"""Command handlers."""',
        '',
        'from telegram import Update',
        'from telegram.ext import ContextTypes',
        '',
    ]

    # Generate keyboard imports if any command has buttons
    has_buttons = any(commands[c].get("buttons") for c in commands)
    if has_buttons:
        lines.insert(3, 'from keyboards.menus import build_keyboard')
        lines.insert(4, '')

    for cmd, data in commands.items():
        fn = safe_func_name(cmd)
        text = data.get("text", f"Handler for {cmd}")
        text_escaped = text.replace('"', '\\"').replace("\n", "\\n")
        buttons = data.get("buttons", [])

        lines.append(f'async def cmd_{fn}(update: Update, context: ContextTypes.DEFAULT_TYPE):')
        lines.append(f'    """{cmd} command handler."""')

        if buttons:
            btn_data = json.dumps(buttons, ensure_ascii=False)
            lines.append(f'    keyboard = build_keyboard({btn_data})')
            lines.append(f'    await update.message.reply_text("{text_escaped}", reply_markup=keyboard)')
        else:
            lines.append(f'    await update.message.reply_text("{text_escaped}")')
        lines.append('')

    # Add cancel handler
    lines.append('async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):')
    lines.append('    """Cancel conversation."""')
    lines.append('    await update.message.reply_text("Operation cancelled.")')
    lines.append('    from telegram.ext import ConversationHandler')
    lines.append('    return ConversationHandler.END')
    lines.append('')

    return "\n".join(lines)


def generate_callbacks_py(arch):
    """Generate handlers/callbacks.py with ConversationHandler states."""
    menus = arch.get("menus", {})
    input_flows = arch.get("input_flows", [])

    # Collect states
    states = set()
    for flow in input_flows:
        st = safe_state_name(flow.get("state"))
        if st:
            states.add(st)

    lines = [
        '"""Callback query handlers."""',
        '',
        'from telegram import Update',
        'from telegram.ext import ContextTypes',
        'from keyboards.menus import build_keyboard',
        '',
    ]

    # Import states from bot.py if needed
    if states:
        state_imports = ", ".join(sorted(states))
        lines.append(f'# Import states — these are defined in bot.py')
        lines.append(f'# from bot import {state_imports}')
        lines.append('')
        # Define locally to avoid circular import
        for i, st in enumerate(sorted(states)):
            lines.append(f'{st} = {i}')
        lines.append('')

    lines.append('async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):')
    lines.append('    """Route callback queries to appropriate handlers."""')
    lines.append('    query = update.callback_query')
    lines.append('    await query.answer()')
    lines.append('    data = query.data')
    lines.append('')

    if not menus:
        lines.append('    await query.edit_message_text(f"Received: {data}")')
        lines.append('')
        return "\n".join(lines)

    first = True
    for menu_key, menu_data in menus.items():
        trigger = menu_data.get("trigger", menu_key)
        text = menu_data.get("text", f"Menu: {menu_key}")
        text_escaped = text.replace('"', '\\"').replace("\n", "\\n")
        buttons = menu_data.get("buttons", [])
        input_state = menu_data.get("input_state")

        kw = "if" if first else "elif"
        lines.append(f'    {kw} data == "{trigger}":')

        if buttons:
            btn_data = json.dumps(buttons, ensure_ascii=False)
            lines.append(f'        keyboard = build_keyboard({btn_data})')
            lines.append(f'        await query.edit_message_text("{text_escaped}", reply_markup=keyboard)')
        else:
            lines.append(f'        await query.edit_message_text("{text_escaped}")')

        if input_state:
            st = safe_state_name(input_state)
            if st:
                lines.append(f'        return {st}')

        first = False

    if not first:
        lines.append('    else:')
        lines.append('        await query.edit_message_text(f"Unknown action: {data}")')

    lines.append('')
    return "\n".join(lines)


def generate_messages_py(arch):
    """Generate handlers/messages.py for input flow states."""
    input_flows = arch.get("input_flows", [])

    states = set()
    for flow in input_flows:
        st = safe_state_name(flow.get("state"))
        if st:
            states.add(st)

    lines = [
        '"""Message handlers for conversation states."""',
        '',
        'from telegram import Update',
        'from telegram.ext import ContextTypes, ConversationHandler',
        '',
    ]

    if not states:
        lines.append('# No input flows detected')
        lines.append('')
        return "\n".join(lines)

    for st in sorted(states):
        handler_name = f"handle_{st.lower()}"
        # Find matching flow for prompt
        prompt = ""
        for flow in input_flows:
            if safe_state_name(flow.get("state")) == st:
                prompt = flow.get("prompt", "")
                break

        lines.append(f'async def {handler_name}(update: Update, context: ContextTypes.DEFAULT_TYPE):')
        lines.append(f'    """Handle {st} input state."""')

        if "IMAGE" in st or "VIDEO" in st or "FILE" in st:
            lines.append('    # Process media input')
            lines.append(f'    if update.message.photo:')
            lines.append(f'        file = await update.message.photo[-1].get_file()')
            lines.append(f'    elif update.message.document:')
            lines.append(f'        file = await update.message.document.get_file()')
            lines.append(f'    elif update.message.video:')
            lines.append(f'        file = await update.message.video.get_file()')
            lines.append(f'    else:')
            lines.append(f'        await update.message.reply_text("Please send the required media.")')
            lines.append(f'        return {st}')
            lines.append(f'    # TODO: process file')
            lines.append(f'    await update.message.reply_text("Media received! Processing...")')
        else:
            lines.append(f'    text = update.message.text')
            lines.append(f'    if not text:')
            lines.append(f'        await update.message.reply_text("Please send a text message.")')
            lines.append(f'        return {st}')
            lines.append(f'    # TODO: process text input')
            lines.append(f'    await update.message.reply_text(f"Received: {{text}}")')

        lines.append('    return ConversationHandler.END')
        lines.append('')

    return "\n".join(lines)


def generate_menus_py(arch):
    """Generate keyboards/menus.py."""
    code = '''"""Keyboard builders."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_keyboard(buttons):
    """Build InlineKeyboardMarkup from button list.

    Each button: {"text": "label", "type": "callback|url", "data": "...", "url": "..."}
    """
    keyboard = []
    row = []
    for btn in buttons:
        text = btn.get("text", "?")
        btn_type = btn.get("type", "callback")

        if btn_type == "url" and btn.get("url"):
            row.append(InlineKeyboardButton(text, url=btn["url"]))
        else:
            data = btn.get("data", text)
            row.append(InlineKeyboardButton(text, callback_data=data))

        # Max 3 buttons per row
        if len(row) >= 3:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard) if keyboard else None
'''
    return code


def generate_requirements():
    return "python-telegram-bot>=20.0\n"


def generate_bot(arch_path, output_dir):
    """Generate full PTB v20 bot from architecture JSON."""
    print(f"[*] Loading architecture: {arch_path}")
    arch = load_architecture(arch_path)

    bot_name = arch.get("bot", "bot")
    print(f"[*] Generating PTB v20 bot for: {bot_name}")

    # Create directories
    os.makedirs(os.path.join(output_dir, "handlers"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "keyboards"), exist_ok=True)

    files = {
        "bot.py": generate_bot_py(arch),
        "handlers/__init__.py": "",
        "handlers/commands.py": generate_commands_py(arch),
        "handlers/callbacks.py": generate_callbacks_py(arch),
        "handlers/messages.py": generate_messages_py(arch),
        "keyboards/__init__.py": "",
        "keyboards/menus.py": generate_menus_py(arch),
        "requirements.txt": generate_requirements(),
    }

    for fname, content in files.items():
        fpath = os.path.join(output_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [+] {fname}")

    print(f"\n[DONE] Bot generated in {output_dir}/")
    print(f"  1. Set BOT_TOKEN in bot.py")
    print(f"  2. pip install -r requirements.txt")
    print(f"  3. python3 bot.py")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 bot_cloner_ptb.py architecture.json [--output ./ptb_bot/]")
        sys.exit(1)

    arch_path = sys.argv[1]
    output_dir = "./ptb_bot"

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_dir = sys.argv[idx + 1]

    generate_bot(arch_path, output_dir)


if __name__ == "__main__":
    main()
