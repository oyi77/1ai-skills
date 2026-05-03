# AutoDroid Automation Suite — Deployment Guide

## Cloud Services (DO NOT run locally)

| Service | URL | Platform | Notes |
|---------|-----|----------|-------|
| 1proxy Backend | https://helpful-alignment-production-2ae5.up.railway.app | Railway | Free proxy rotation, cold start ~15-30s |
| PostBridge | https://api.post-bridge.com/v1 | PostBridge Cloud | Social media posting |

## Local Setup (ADB device only)

```bash
# 1. Connect Android device via ADB over WiFi
adb connect <device-ip>:8775

# 2. Verify connection
adb devices

# 3. Run specific agent
cd automation/autodroid-kling-agent
python3 scripts/kling_agent.py
```

## Environment Variables

```bash
# Cloud proxy (already on Railway — do NOT run locally)
export ONEPROXY_API_URL="https://helpful-alignment-production-2ae5.up.railway.app"

# PostBridge
export POSTBRIDGE_API_KEY="pb_live_AT9Xm4PKaYBzAvFZYGgexi"

# ADB device
export ANDROID_DEVICE_SERIAL="SGZTONV4OBL74TJZ"
export ADB_PORT="8775"
```

## Agent Quick Start

```bash
# Kling — generate video
python3 automation/autodroid-kling-agent/scripts/kling_agent.py generate --prompt "sunrise over mountains"

# Account generator (uses Railway 1proxy automatically)
python3 automation/autodroid-kling-agent/kling_api/kling_account_generator.py --count 5

# Instagram — post
python3 automation/autodroid-instagram-agent/scripts/instagram_agent.py post --media /path/to/video.mp4

# TikTok — upload
python3 automation/autodroid-tiktok-agent/scripts/tiktok_agent.py upload --video /path/to/video.mp4
```

## Run All Tests

```bash
cd automation
python3 run_all_tests.py
```
