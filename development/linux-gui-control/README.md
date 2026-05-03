# Linux GUI Control

Control the Linux desktop GUI using xdotool, wmctrl, and dogtail.

## What It Does

This skill enables automation of Linux desktop applications through:
- Window management (list, activate, resize, move)
- Input simulation (mouse clicks, keyboard typing, key presses)
- UI hierarchy inspection via accessibility (AT-SPI)
- Screenshot capture for visual analysis

## Quick Usage Example

```bash
# 1. Find the window you want to control
wmctrl -l
# Output: 0x02a00001  workstation  Gedit

# 2. Activate the window
./scripts/gui_action.sh activate "Gedit"

# 3. Type text
./scripts/gui_action.sh type "Hello World"

# 4. Save the file
./scripts/gui_action.sh key "Ctrl+s"
```

## Key Features

- ✅ Control any X11/GNOME application
- ✅ Simulate mouse and keyboard input
- ✅ Inspect UI hierarchies without screenshots (A11y support)
- ✅ Window management (activate, resize, move)
- ✅ Works with Electron apps (requires `--force-renderer-accessibility`)
- ✅ Take screenshots for visual analysis

## Requirements

- xdotool (input simulation)
- wmctrl (window management)
- dogtail (UI tree extraction)
- scrot (screenshots)
- AT-SPI accessibility framework