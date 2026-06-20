---
name: computer-use
description: Computer use agents — desktop automation, screen reading, mouse/keyboard control, GUI interaction for AI agents
domain: agents
tags:
- ai-agent
- automation
- computer
- orchestration
- use
---

## Overview

Computer use enables AI agents to interact with desktop applications through screen capture, OCR, and input simulation. This skill covers desktop automation patterns using PyAutoGUI, xdotool, AppleScript, and Anthropic's computer-use API for autonomous GUI interaction.

## Capabilities

- Capture screenshots and analyze them with vision models
- Simulate mouse clicks, drags, and keyboard input
- Read screen content via OCR (Tesseract, EasyOCR)
- Manage windows (focus, resize, move, minimize)
- Record and replay GUI workflows
- Handle multi-monitor setups
- Implement safety boundaries to prevent destructive actions

## When to Use

- Automating desktop applications that have no API
- Testing GUI applications
- AI agents that need to control the computer
- Automating workflows across multiple apps
- Accessibility tools and screen readers
- RPA (Robotic Process Automation) tasks

## Pseudo Code

Implementation patterns for common use cases with this skill.


### Screenshot + Vision Analysis
```python
import pyautogui
import base64
from io import BytesIO

# Capture screen
screenshot = pyautogui.screenshot()
buffer = BytesIO()
screenshot.save(buffer, format='PNG')
img_base64 = base64.b64encode(buffer.getvalue()).decode()

# Send to vision model for analysis
response = vision_model.analyze(
    image=img_base64,
    prompt="Describe what's on screen. List all clickable elements with their coordinates."
)

# Parse coordinates and click
for element in response.elements:
    if element.type == "button" and element.text == "Submit":
        pyautogui.click(element.x, element.y)
```

### PyAutoGUI — Mouse + Keyboard
```python
import pyautogui
import time

# Safety: move mouse to corner to abort
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5  # 0.5s between actions

# Mouse
pyautogui.click(100, 200)          # Click at (100, 200)
pyautogui.doubleClick(300, 400)    # Double-click
pyautogui.rightClick(500, 600)     # Right-click
pyautogui.drag(100, 0, duration=1) # Drag 100px right
pyautogui.scroll(3)                # Scroll up 3 units

# Keyboard
pyautogui.typewrite('Hello World', interval=0.05)
pyautogui.hotkey('cmd', 'c')       # Cmd+C (copy)
pyautogui.hotkey('ctrl', 'shift', 'esc')  # Task manager
pyautogui.press('enter')

# Find and click image on screen
location = pyautogui.locateOnScreen('button.png', confidence=0.8)
if location:
    pyautogui.click(pyautogui.center(location))
```

### AppleScript (macOS)
```python
import subprocess

def run_applescript(script):
    result = subprocess.run(
        ['osascript', '-e', script],
        capture_output=True, text=True
    )
    return result.stdout.strip()

# Open app
run_applescript('tell application "Safari" to activate')

# Get window info
run_applescript('''
    tell application "System Events"
        tell process "Safari"
            get position of window 1
            get size of window 1
        end tell
    end tell
''')

# Click menu item
run_applescript('''
    tell application "System Events"
        tell process "Safari"
            click menu item "New Window" of menu "File" of menu bar 1
        end tell
    end tell
''')
```

### xdotool (Linux)
```bash
# Get active window
xdotool getactivewindow

# Move and resize window
xdotool getactivewindow windowmove 0 0 windowsize 1920 1080

# Type text
xdotool type "Hello World"

# Key combos
xdotool key ctrl+c
xdotool key alt+Tab

# Click at coordinates
xdotool mousemove 500 300 click 1
```

### Window Management
```python
import subprocess
import platform

def focus_window(app_name):
    if platform.system() == 'Darwin':
        subprocess.run(['osascript', '-e',
            f'tell application "{app_name}" to activate'])
    elif platform.system() == 'Linux':
        subprocess.run(['wmctrl', '-a', app_name])

def get_window_list():
    if platform.system() == 'Darwin':
        result = subprocess.run(['osascript', '-e',
            'tell application "System Events" to get name of every process whose visible is true'],
            capture_output=True, text=True)
        return result.stdout.strip().split(', ')
    elif platform.system() == 'Linux':
        result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)
        return result.stdout.strip().split('\n')
```

### OCR Screen Reading
```python
import pyautogui
import pytesseract
from PIL import Image

# Screenshot region
region = (100, 200, 400, 300)  # x, y, width, height
screenshot = pyautogui.screenshot(region=region)

# OCR
text = pytesseract.image_to_string(screenshot)
print("Screen text:", text)

# Find text location
data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
for i, word in enumerate(data['text']):
    if word.strip():
        x, y = data['left'][i], data['top'][i]
        print(f"'{word}' at ({x}, {y})")
```

## Common Patterns

Reusable patterns that appear frequently when applying this skill.


### Safety Boundaries
```python
# Define safe zones and dangerous actions
BLOCKED_ACTIONS = [
    "rm -rf",
    "format",
    "delete all",
    "sudo",
]

def safe_click(x, y, screen_width, screen_height):
    if x < 0 or y < 0 or x > screen_width or y > screen_height:
        raise ValueError(f"Click ({x},{y}) outside screen bounds")
    pyautogui.click(x, y)

def safe_type(text):
    for blocked in BLOCKED_ACTIONS:
        if blocked.lower() in text.lower():
            raise ValueError(f"Blocked dangerous input: {blocked}")
    pyautogui.typewrite(text, interval=0.05)
```

### Workflow Recording + Replay
```python
import json
import time

def record_workflow(steps_file):
    """Record mouse/keyboard actions for replay"""
    steps = []
    print("Recording... Press Ctrl+C to stop")
    try:
        while True:
            x, y = pyautogui.position()
            steps.append({'type': 'move', 'x': x, 'y': y, 'time': time.time()})
            time.sleep(0.1)
    except KeyboardInterrupt:
        with open(steps_file, 'w') as f:
            json.dump(steps, f)
        print(f"Saved {len(steps)} steps")

def replay_workflow(steps_file, speed=1.0):
    """Replay recorded actions"""
    with open(steps_file) as f:
        steps = json.load(f)
    for step in steps:
        if step['type'] == 'move':
            pyautogui.moveTo(step['x'], step['y'])
        elif step['type'] == 'click':
            pyautogui.click(step['x'], step['y'])
        time.sleep(0.1 / speed)
```

### Multi-Monitor Support
```python
from screeninfo import get_monitors

monitors = get_monitors()
for m in monitors:
    print(f"Monitor {m.name}: {m.width}x{m.height} at ({m.x}, {m.y})")

# Screenshot specific monitor
def screenshot_monitor(index):
    m = monitors[index]
    return pyautogui.screenshot(region=(m.x, m.y, m.width, m.height))
```

## When NOT to Use

- When the target application has a CLI or API (prefer structured interfaces over GUI)
- When the task can be done with keyboard shortcuts alone (no screen reading needed)
- When running in a headless environment without a display server (use Xvfb or skip)
- When the GUI application has accessibility bindings (use AT-SPI, AX API instead of pixel clicking)
- When the task requires sub-second precision (GUI automation has inherent latency)
- When destructive actions (file deletion, system changes) lack a confirmation step

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Clicking coordinates is reliable enough" | Screen resolution, DPI scaling, and window position change coordinates. Use image recognition or element identification instead of raw coordinates. |
| "I do not need a safety failsafe" | PyAutoGUI's failsafe (mouse to corner) exists because GUI automation can type dangerous commands into any focused window. Always enable it. |
| "OCR is good enough for reading the screen" | OCR struggles with small fonts, styled text, and overlapping elements. Vision models with screenshots are more reliable for complex UIs. |
| "Recording and replaying is the same as automation" | Recorded workflows break on any UI change (window resize, theme change, dialog popup). Parameterized automation is more resilient. |
| "I will handle multi-monitor later" | Multi-monitor setups change coordinate origins. Screeninfo detection must happen at runtime, not hardcoded. |
| "AppleScript can do everything on macOS" | AppleScript is powerful for native apps but fails on Electron apps, web content, and cross-platform code. Combine with xdotool/PyAutoGUI for full coverage. |

## Red Flags

- Hardcoded screen coordinates (breaks across different resolutions/DPI)
- No failsafe enabled (PyAutoGUI can type into any focused window)
- No delay between actions (too fast for UI to respond)
- Destructive commands without confirmation dialog (rm, delete, format)
- OCR without verifying recognition accuracy (wrong characters, misread text)
- No screenshot on failure (impossible to debug what went wrong)
- Running on production servers without display isolation (Xvfb)
- Sending keystrokes to the wrong window (focus not verified)

## Verification

After implementing computer use automation, confirm:

- [ ] Failsafe enabled (PyAutoGUI.FAILSAFE = True or equivalent)
- [ ] Delays between actions are appropriate for the target application
- [ ] Element identification uses robust methods (not raw coordinates)
- [ ] Destructive actions have explicit confirmation step before execution
- [ ] Screenshots captured before and after critical actions (audit trail)
- [ ] Multi-monitor setup detected at runtime (not hardcoded coordinates)
- [ ] OCR results validated against expected text (not trusted blindly)
- [ ] Error handling covers window-not-found, element-not-clickable, and timeout
- [ ] Works in headless mode (Xvfb) if needed for CI/server environments
- [ ] Cleanup releases all input handles and restores window state

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
