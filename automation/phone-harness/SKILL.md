---
name: phone-harness
description: Use when an agent needs to control a real phone — iPhone via Mac iPhone
  Mirroring or Android via adb (open apps, tap, type, swipe, OCR the screen). Android
  path runs on this Linux workstation (adb), targets phonefarm devices. iOS path needs
  macOS + iPhone Mirroring. Use for phonefarm device debugging, OTP/2FA flows, or
  one-off device QA when adapters don't cover the flow.
domain: automation
author: oyi77
license: MIT
subdomain: device-automation
tags:
- adb
- android
- automation
- device-control
- ocr
- phonefarm
- phone
- uiautomator
version: 1.0.0
category: automation
---

# Phone Harness

## When to Use

**Trigger phrases:**
- "control my phone"
- "tap on the phone"
- "read the phone screen"
- "install/use phone-harness"

- One-off phone actions adapters don't cover: OTP/2FA prompts, Settings toggles,
  account switches, uninstalls, first-run dialogs
- Debugging a phonefarm device state (what app is foreground, what's on screen)
- Wiring a new farm workflow before promoting it into a phonefarm adapter
- Verifying an adapter change against a real device by hand

## When NOT to Use

- Anything doable via web/API — leave the phone alone (phonefarm adapters first)
- Recurring production farm workflows → implement in `1ai-phonefarm` adapters
  (`adapters/<platform>/mobile_adapter.py`), not ad-hoc harness scripts
- Tasks needing multi-touch (pinch), camera, or Face ID — unsupported
- iOS flows on this box — no macOS here; Linux workstation = Android-only

## Workflow

1. Install once (Android focus for this workstation):
   ```bash
   git clone https://github.com/ShawnPana/phone-harness ~/.phone-harness
   cd ~/.phone-harness && pip install -e .
   # or: read install.md in the repo and follow it
   phone-harness --doctor   # verify adb + device chain
   ```
2. Set Android default (this box has no macOS/iPhone Mirroring):
   ```bash
   phone-harness config set platform android
   ```
3. Drive the device (helpers pre-imported):
   ```python
# task: dismiss a first-run dialog on the farm device
# step: OCR, tap the right label, verify
open_app("chrome"); wait_stable()
tap_ui("Got it")          # label from accessibility tree — exact, no misreads
   ```
4. Verify after every action — adb reports nothing about outcomes; a tap on
   empty space "succeeds". Use `wait_for_app(...)`, `wait_for_text(...)`, or
   one `ocr()` check. Batch only steps already watched working.
5. Keep the phone awake for long tasks: `phone-harness android awake --bg`,
   then `phone-harness android rest` at the end.

Key helpers: `ocr()`, `ui()`, `find_nodes()`, `tap_ui()`, `tap_text()`,
`screenshot()`, `open_app()`, `back()`, `current_app()`, `list_apps()`,
`swipe()`, `scroll()`, `type_text()`, `press()`.

## Anti-Rationalization Table

| Rationalization | Reality |
|-----------------|---------|
| "The tap returned success" | adb always reports success; verify screen state changed |
| "I'll tap Connect/Continue myself" | Connection/unlock is the user's job; STOP and ask |
| "I'll type the PIN" | Never type a PIN; ask the user to unlock |
| "Screenshot pixel coords are fine for tap()" | iOS only: convert via `image_point()`; Android is 1:1 |
| "One big batch is faster" | Unverified batches fail silently; batch only proven steps |
| "uiautomator dump is stuck" | Known hang on React/WebView screens; use timeout + OCR fallback |

## Verification

- [ ] `phone-harness --doctor` passes
- [ ] `adb devices` shows target device
- [ ] Named what should change before acting; verified it changed after
- [ ] No settings/messages/purchases without explicit user approval

## Code Example

```bash
PHONE_HARNESS_PLATFORM=android phone-harness <<'PY'
# task: confirm TikTok is foregrounded on the farm device
# step: launch, wait, read current app
open_app("com.zhiliaoapp.musically")
wait_stable()
print(current_app())
PY
```

## Ecosystem Notes (1ai-phonefarm)

- Farm adapters already own `screencap`/`uiautomator`/`input` plumbing
  (`adapters/*/mobile_adapter.py`, `backend/services/screen_assertions.py`) —
  prefer them for production flows.
- phonefarm `adapters/tiktok/ocr.py` (tesseract-based) predates this skill for
  OCR; phone-harness OCR uses the accessibility tree on Android — cheaper and
  exact where a tree exists, tesseract where custom rendering wins.
- Skill is generic-purpose; register farm-specific flows in the phonefarm repo,
  not here.
