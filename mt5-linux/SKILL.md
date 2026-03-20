# MT5 Linux — Docker Management Skill

## Overview
Manage MetaTrader 5 on Linux via Docker containers. 1 container = 1 account. Data on /mnt/data.

## Key Files
- **docker-compose:** `/mnt/data/mt5/docker-compose.yml`
- **env:** `/mnt/data/mt5/.env`
- **data dirs:** `/mnt/data/mt5/account{1,2,3}/`

## Port Reference
| Container     | noVNC | Python API |
|--------------|-------|------------|
| mt5-account1 | 6091  | 18901      |
| mt5-account2 | 6092  | 18902      |
| mt5-account3 | 6093  | 18903      |
| native (existing) | 6081 | 18812   |

## Common Commands

### Start/Stop
```bash
cd /mnt/data/mt5
docker compose up -d mt5-account1        # start 1 account
docker compose up -d                      # start all
docker compose stop mt5-account1         # stop 1
docker compose down                       # stop all
docker compose restart mt5-account1      # restart
```

### Logs & Status
```bash
docker compose ps                          # status all
docker compose logs -f mt5-account1       # live logs
docker stats mt5-account1                 # resource usage
```

### Shell access
```bash
docker exec -it mt5-account1 bash
```

### Pull latest image (before first run)
```bash
docker pull lprett/mt5linux:mt5-installed
```

## Python API Usage
```python
from mt5linux import MetaTrader5

# Account 1
mt5 = MetaTrader5(host="localhost", port=18901)
mt5.initialize()

# Account 2
mt5 = MetaTrader5(host="localhost", port=18902)
mt5.initialize()

# Basic usage
mt5.terminal_info()
mt5.account_info()
mt5.shutdown()
```

## Cloudflare Tunnel Setup
Tunnel ID: `0621c8e9-edab-448f-9434-17807b184c35`

To expose mt5.aitradepulse.com:
1. Go to: https://one.dash.cloudflare.com → Zero Trust → Access → Tunnels
2. Find tunnel `0621c8e9...`
3. Public Hostnames → Add hostname:
   - Subdomain: `mt5`
   - Domain: `aitradepulse.com`
   - Service: `http://localhost:6091`
4. Save → restart cloudflared: `sudo systemctl restart cloudflared`

## CRITICAL BEST PRACTICES

### 1. 1 Account = 1 Container (ABSOLUTE RULE)
- MT5 uses file locks on its data directory
- Running 2 accounts in 1 terminal = data corruption
- Each container has isolated Wine prefix → no conflicts

### 2. Data on /mnt/data ONLY
- System disk (/) = 110GB, already 92% full
- /mnt/data = 916GB, only 4% used
- ALL MT5 data via volume mount to /mnt/data/mt5/accountN/

### 3. Never Expose Python Port Publicly
- Port 18812 (MT5 server) = raw TCP, no auth
- Only accessible from localhost or VPN
- noVNC (6081) goes through Cloudflare → has VNC password

### 4. VNC Password
- Set in /mnt/data/mt5/.env → VNC_PASSWORD
- Default is BerkahKarya2026! — change if needed
- Required to access via browser

### 5. Container Naming Convention
- Format: `mt5-<account-name>` or `mt5-account<N>`
- Never reuse container names for different accounts

### 6. Volume Mount Path (IMPORTANT)
MT5 stores data at this Wine path inside container:
`/root/.wine/drive_c/users/root/AppData/Roaming/MetaQuotes`

Mount your host dir there:
```yaml
volumes:
  - /mnt/data/mt5/accountN:/root/.wine/drive_c/users/root/AppData/Roaming/MetaQuotes
```

### 7. restart: unless-stopped
- Ensures MT5 auto-restarts after server reboot
- Use `unless-stopped` not `always` (allows manual stop)

### 8. Adding New Account
```bash
# 1. Create data dir
mkdir -p /mnt/data/mt5/account4

# 2. Add service to docker-compose.yml
# Copy account3 block, change:
#   - container_name: mt5-account4
#   - ports: 6094:6081, 18904:18812
#   - volume: account4:/root/...

# 3. Start it
cd /mnt/data/mt5
docker compose up -d mt5-account4
```

## Troubleshooting

### Container won't start
```bash
docker compose logs mt5-account1
# Common: port conflict — check with: ss -tlnp | grep 609
```

### MT5 not connecting (Python)
```bash
# Check if port is open:
nc -z localhost 18901 && echo "open" || echo "closed"
# If closed: check container is running and MT5 terminal is logged in via VNC first
```

### VNC blank screen
```bash
# Restart the container
docker compose restart mt5-account1
```

### Image pull fails
```bash
# Use the pre-installed image tag:
docker pull lprett/mt5linux:mt5-installed
# NOT: lprett/mt5linux:latest (that one needs manual MT5 install)
```

## Native MT5 (existing, non-Docker)
There's already a native MT5 running:
- noVNC: http://localhost:6081
- Python: localhost:18812
- Running as root via Wine directly (not Docker)
- DO NOT interfere with this unless migrating

To see status: `ps aux | grep terminal64`
