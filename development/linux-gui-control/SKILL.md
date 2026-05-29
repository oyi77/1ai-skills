---
name: linux-gui-control
description: Linux GUI Control. Use when relevant to this domain.
persona: |
  name: Linus Torvalds
    title: The Linux Creator - Master of System Control
    expertise:
    - Linux
    - System Programming
    - Git
    - Operating Systems
    philosophy: Talk is cheap. Show me the code.
    credentials:
    - Created Linux kernel
    - Created Git
    - Maintains largest open source project
    principles:
    - Control the system
    - Script everything
    - Prefer command line
    - Automate workflows
---

name: linux-gui-control
description: "Control the Linux desktop GUI using xdotool, wmctrl, and dogtail. Use when you need to interact with non-browser applications, simulate mouse/keyboard input, manage windows, or inspect the UI hierarchy of applications on X11/GNOME. Supports: (1) Clicking/typing in apps, (2) Resizing/moving windows, (3) Extracting text-based UI trees from apps (A11y), (4) Taking screenshots for visual analysis."
---

# Linux GUI Control

This skill provides tools and procedures for automating interactions with the Linux desktop environment.

## Quick Start

Get started with linux-gui-control in three steps.

1. Install dependencies: `pip install -r requirements.txt` or `npm install`
2. Configure settings in `config.yaml` or `.env`
3. Run: `python main.py --mode linux-gui-control` or `npm run dev`

Verify setup:
```bash
python main.py --check-config
python main.py --run
```


### 1. Identify Target Window
Use `wmctrl` to find the exact name of the window you want to control.
```bash
wmctrl -l
```

### 2. Inspect UI Hierarchy
For apps supporting accessibility (GNOME apps, Electron apps with `--force-renderer-accessibility`), use the inspection script to find button names without taking screenshots.
```bash
python3 scripts/inspect_ui.py "<app_name>"
```

### 3. Perform Actions
Use `xdotool` via the helper script for common actions.
```bash
# Activate window
./scripts/gui_action.sh activate "<window_name>"

# Click coordinates
./scripts/gui_action.sh click 500 500

# Type text
./scripts/gui_action.sh type "Hello World"

# Press a key
./scripts/gui_action.sh key "Return"
```

## Workflows

Step-by-step linux-gui-control execution process.

**Step 1: Configure** — Set up targets and parameters in config file.

**Step 2: Execute** — Run the linux-gui-control workflow with configured inputs.

**Step 3: Review** — Analyze outputs and iterate on configuration.

**Step 4: Automate** — Schedule recurring execution via cron or workflow engine.


### Operating an App via Text UI
1. List windows with `wmctrl -l`.
2. Activate the target window.
3. Run `scripts/inspect_ui.py` to get the list of buttons and inputs.
4. Use `xdotool key Tab` and `Return` to navigate, or `click` if coordinates are known.
5. If text-based inspection fails, fallback to taking a screenshot and using vision.

### Forcing Accessibility in Electron Apps
Many modern apps (VS Code, Discord, Cider, Chrome) need a flag to expose their UI tree:
```bash
pkill <app>
nohup <app> --force-renderer-accessibility > /dev/null 2>&1 &
```

## Tool Reference

- **wmctrl**: Window management (list, activate, move, resize).
- **xdotool**: Input simulation (click, type, key, mousemove).
- **dogtail**: UI tree extraction via AT-SPI (Accessibility bus).
- **scrot**: Lightweight screenshot tool.
## When NOT to Use

- When the code change is in a frozen release branch under change management
- When the task requires access to production systems the agent cannot reach
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Code changes are made without running the existing test suite
- Agent does not handle error cases or edge conditions
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] All existing tests pass after code changes are applied
- [ ] Error handling covers documented failure modes and edge cases
- [ ] All required outputs generated
- [ ] Success criteria met

