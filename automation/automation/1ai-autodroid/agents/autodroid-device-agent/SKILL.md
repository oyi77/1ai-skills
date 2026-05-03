---
persona:
  name: "Domain Expert"
  title: "Master of Autodroid Device Agent"
  expertise: ['Agents Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']

---

# autodroid-device-agent Skill

Full Android device control via ADB. Covers info, screen, power, connectivity, audio, files, apps, input, notifications, and system settings. Exposes a FastAPI server on port 8772.

## Commands

| Command | Description |
|---------|-------------|
| `info` | Full device info JSON |
| `battery` | Battery level + status |
| `apps [--installed\|--system]` | List packages |
| `screenshot [--out PATH]` | Capture screen |
| `screenrecord [--duration 10] [--out PATH]` | Record screen |
| `brightness [--level 0-255\|--auto]` | Set brightness |
| `rotation [--mode 0\|1\|2\|3\|auto]` | Set rotation |
| `lock` | Lock screen |
| `unlock [--pin PIN]` | Wake + unlock |
| `wake` | Wake screen |
| `wifi [--on\|--off]` | Toggle WiFi |
| `wifi-connect --ssid S --password P` | Connect to WiFi |
| `mobile-data [--on\|--off]` | Toggle mobile data |
| `airplane [--on\|--off]` | Toggle airplane mode |
| `bluetooth [--on\|--off]` | Toggle Bluetooth |
| `volume [--level 0-15] [--stream ringtone\|music\|alarm]` | Set volume |
| `flashlight [--on\|--off]` | Toggle flashlight |
| `photo [--out PATH]` | Take photo |
| `video [--duration 5] [--out PATH]` | Record video |
| `call --number PHONE` | Make phone call |
| `sms --to PHONE --text MSG` | Send SMS |
| `sms-read [--count 10]` | Read SMS inbox |
| `contacts [--query NAME]` | List/search contacts |
| `push --src PATH --dst PATH` | Push file to device |
| `pull --src PATH --dst PATH` | Pull file from device |
| `ls [--path /sdcard/]` | List files |
| `rm --path PATH` | Delete file |
| `mkdir --path PATH` | Create directory |
| `install --apk PATH` | Install APK |
| `uninstall --package PKG` | Uninstall app |
| `launch --package PKG` | Launch app |
| `stop --package PKG` | Force stop app |
| `clear-data --package PKG` | Clear app data |
| `permissions --package PKG` | List permissions |
| `tap --x X --y Y` | Tap coordinates |
| `swipe --x1 X --y1 Y --x2 X2 --y2 Y2` | Swipe gesture |
| `key --code CODE` | Send keyevent |
| `text --value TEXT` | Type text |
| `clipboard --text TEXT` | Set clipboard |
| `notifications` | Read notifications |
| `gps [--on\|--off]` | Toggle location |
| `font-scale [--scale 1.0]` | Set font scale |
| `timezone [--tz Asia/Jakarta]` | Set timezone |
| `date-time [--dt "YYYY-MM-DD HH:MM:SS"]` | Set date/time |
| `server [--port 8772]` | Start FastAPI server |

## Usage

```bash
# Get full device info
python3 scripts/device_agent.py info --device SGZTONV4OBL74TJZ

# Battery status
python3 scripts/device_agent.py battery

# Take screenshot
python3 scripts/device_agent.py screenshot --out /tmp/screen.png

# Unlock with PIN
python3 scripts/device_agent.py unlock --pin 1234

# Send a tap
python3 scripts/device_agent.py tap --x 360 --y 800

# Install APK
python3 scripts/device_agent.py install --apk /tmp/app.apk

# Start server
python3 scripts/device_agent.py server --port 8772
```

## Device Requirements

- ADB connected and authorized
- App installed: system (no specific app required)
- Serial: SGZTONV4OBL74TJZ (or set via `--device`)
- Android 9+ recommended

## Server API (port 8772)

Start with: `python3 scripts/device_agent.py server --port 8772`
Docs at: `http://localhost:8772/docs`

## Output Format

All commands return JSON. Example `battery`:

```json
{
  "ok": true,
  "level": 87,
  "status": "charging",
  "temperature": 28.5,
  "voltage": 4200
}
```

## AI Interceptor

Integrated for prompt enhancement and quality scoring.
