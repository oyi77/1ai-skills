#!/usr/bin/env python3
"""
Simple Telegram Sender - Send messages to user via OpenClaw
"""

import json
import os
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
PENDING_DIR = BASE_DIR / 'temp' / 'pending_messages'

def send_pending_messages():
    """Send all pending messages to Telegram"""

    if not PENDING_DIR.exists():
        return 0

    sent_count = 0
    for msg_file in sorted(PENDING_DIR.glob('*.txt')):
        try:
            with open(msg_file, 'r') as f:
                message = f.read()

            # Read metadata
            meta_file = msg_file.with_suffix('.json')
            if meta_file.exists():
                with open(meta_file, 'r') as f:
                    meta = json.load(f)
                    urgent = meta.get('urgent', False)
            else:
                urgent = False

            # Send via message tool (would be called from session)
            print(f"📤 Message: {message[:100].replace(chr(10), ' ')}...")
            print(f"   Urgent: {urgent}")
            print(f"   File: {msg_file.name}")
            print()

            sent_count += 1

        except Exception as e:
            print(f"❌ Error reading {msg_file}: {e}")

    return sent_count

if __name__ == "__main__":
    count = send_pending_messages()
    print(f"Total pending messages: {count}")