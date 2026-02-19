# gateway-doctor

PM2-based gateway health monitoring with PowerShell 7 Preview.

## Philosophy

- **PowerShell 7 Preview** = faster, better performance
- **PM2** = native process management + auto-restart
- **Node.js script** = reliable orchestration

## How It Works

1. Check if port **18789** is listening using PowerShell 7 Preview:
   ```powershell
   Get-NetTCPConnection -LocalPort 18789 -State Listen | ConvertTo-Json
   ```
2. If listening → log "healthy" and exit
3. If dead → PM2 restart:
   - `pm2 restart openclaw-gateway`
   - Fallback: `pm2 start` if not registered

## PM2 Setup

First, register OpenClaw gateway with PM2:

```bash
pm2 start "C:\Users\EX PC\AppData\Roaming\npm\node_modules\openclaw\bin\openclaw.js" --name openclaw-gateway -- serve
pm2 save
pm2 startup
```

## PowerShell Preview

Uses PowerShell 7 Preview for better performance:
```
C:\Program Files\PowerShell\7-preview\pwsh.exe
```

## Files

| File | Purpose |
|------|---------|
| `gateway-health.js` | Main script (Node.js) |
| `gateway-health.log` | Log file (appended) |

## Cron Setup

**Command:**
```
node "C:\Users\EX PC\.openclaw\gateway-health.js"
```

**Check results:**
```powershell
Get-Content "C:\Users\EX PC\.openclaw\gateway-health.log" -Tail 10
```

## Manual Run

```bash
node "C:\Users\EX PC\.openclaw\gateway-health.js"
```

## PM2 Commands

| Command | Action |
|---------|--------|
| `pm2 status` | List all processes |
| `pm2 restart openclaw-gateway` | Restart gateway |
| `pm2 logs openclaw-gateway` | View gateway logs |
| `pm2 monit` | Real-time dashboard |

## When to Use

- Periodic health checks (1 min interval)
- User reports lag
- After system sleep/resume
- Gateway unresponsive
