#!/usr/bin/env python3
"""
Browser Automation Helper for OpenClaw
Simplified interface for browser actions
"""

import subprocess
import json
import time
from pathlib import Path

WORKSPACE = Path("/home/openclaw/workspace")

class BrowserHelper:
    """Helper for browser automation"""

    def __init__(self):
        self.running = False

    def open(self, url, wait=5):
        """Open URL in browser"""
        result = subprocess.run(
            ['python3', '-c', f'import sys; sys.path.insert(0, "/home/openclaw/.openclaw/workspace/scripts"); from browser_tool import browser_tool; bt = browser_tool(); bt.action_open("{url}")'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return False
        if wait:
            time.sleep(wait)
        return True

    def get_text(self):
        """Get all text from current page"""
        result = subprocess.run(
            ['python3', '-c', 'import sys; sys.path.insert(0, "/home/openclaw/.openclaw/workspace/scripts"); from browser_tool import browser_tool; bt = browser_tool(); print(bt.action_snapshot())'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return ""
        return result.stdout

    def screenshot(self, path):
        """Take screenshot"""
        result = subprocess.run(
            ['python3', '-c', f'import sys; sys.path.insert(0, "/home/openclaw/.openclaw/workspace/scripts"); from browser_tool import browser_tool; bt = browser_tool(); bt.action_screenshot("{path}")'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0

    def close(self):
        """Close browser"""
        result = subprocess.run(
            ['python3', '-c', 'import sys; sys.path.insert(0, "/home/openclaw/.openclaw/workspace/scripts"); from browser_tool import browser_tool; bt = browser_tool(); bt.action_stop()'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0