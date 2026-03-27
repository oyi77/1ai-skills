# 📱 Phone Farm

**URL:** https://phonefarm.aitradepulse.com/

## Features
- Real-time live screen streaming grid
- Tap / swipe / keyboard control directly from browser
- Wake + unlock devices remotely
- Advanced control page (WebSocket)
- Pricing plans (NowPayments integration placeholder)
- pm2 + systemd auto-restart

## Setup
```bash
pip install fastapi uvicorn Pillow aiohttp websockets
pm2 start ecosystem.config.json
pm2 save
pm2 startup
```

## Endpoints
| Route | Description |
|---|---|
| `/dashboard/` | Main dashboard |
| `/control/{serial}` | Remote control (WebSocket scrcpy) |
| `/ws/{serial}` | WebSocket screen stream |
| `/device/{serial}/tap/{x}/{y}` | Tap |
| `/device/{serial}/swipe/{x1}/{y1}/{x2}/{y2}` | Swipe |
| `/device/{serial}/wake` | Wake + unlock |
| `/api/pay` | NowPayments stub |
