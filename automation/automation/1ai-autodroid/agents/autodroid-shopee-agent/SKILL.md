---
persona:
  name: "Domain Expert"
  title: "Master of Autodroid Shopee Agent"
  expertise: ['Agents Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']

---

# autodroid-shopee-agent Skill

Control Shopee Indonesia app (com.shopee.id) via ADB + UIAutomation. Supports browse, search, orders, cart, login, registration, product interaction, reviews, and a FastAPI server on port 8767.

## Commands

| Command | Description |
|---------|-------------|
| `status` | Check Shopee app + device status |
| `open` | Launch Shopee app |
| `orders` | View order list |
| `search --query TEXT` | Search for products |
| `product --query TEXT` | Open product detail |
| `cart` | View cart |
| `like` | Like current product |
| `review --text TEXT [--rating 1-5]` | Post product review |
| `login --username U --password P` | Log in to Shopee |
| `register --phone PHONE --password P` | Register new account |
| `screenshot [--out PATH]` | Capture screen |
| `server [--port 8767]` | Start FastAPI server |

## Usage

```bash
# Check app status
python3 scripts/shopee_agent.py status --device SGZTONV4OBL74TJZ

# Open Shopee
python3 scripts/shopee_agent.py open

# Search products
python3 scripts/shopee_agent.py search --query "baju batik"

# View orders
python3 scripts/shopee_agent.py orders

# Take screenshot
python3 scripts/shopee_agent.py screenshot --out /tmp/shopee.png

# Login
python3 scripts/shopee_agent.py login --username user@email.com --password secret

# Start server mode
python3 scripts/shopee_agent.py server --port 8767
```

## Device Requirements

- ADB connected and authorized
- App installed: com.shopee.id (Shopee Indonesia)
- Serial: SGZTONV4OBL74TJZ (or set via `--device`)
- Android 9+ recommended

## Server API (port 8767)

Start with: `python3 scripts/shopee_agent.py server --port 8767`
Docs at: `http://localhost:8767/docs`

## Notes

- Onboarding popups (Lewati/Skip/Tutup) are auto-dismissed
- Screenshots saved to `~/.openclaw/workspace/downloads/`
- Login supports phone number or email

## AI Interceptor

Integrated for prompt enhancement and quality scoring.
