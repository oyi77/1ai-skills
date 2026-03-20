# 1AI Tools Inventory
> Semua tools yang dibutuhkan oleh BerkahKarya AI (Vilona) untuk beroperasi penuh.
> Last updated: 2026-03-21

---

## 🔧 System / Infrastructure

| Tool | Install | Purpose |
|------|---------|---------|
| `openclaw` | npm install -g openclaw | Main AI agent runtime |
| `omniroute` | npm install -g omniroute | LLM router (local, port 20128) |
| `cloudflared` | apt install cloudflared | Tunnel: ai.aitradepulse.com → local |
| `nvidia-driver` | apt install nvidia-driver | GTX 1660 SUPER (no freeze) |
| `systemd services` | — | omniroute, openclaw-gateway, cloudflared |

---

## 🐦 Social Media / Research

| Tool | Install | Purpose |
|------|---------|---------|
| `twitter-cli` | pip install twitter-cli | X/Twitter read+write, no API key needed |
| `xurl` | brew install xdevplatform/tap/xurl | X API v2 official (write actions) |
| `opencli` | npm install -g @jackwener/opencli | CLI for any website via Chrome session (Antigravity, YouTube, X, dll) |
| `wacli` | (openclaw skill) | WhatsApp automation |

---

## 🤖 AI / LLM Tools

| Tool | Install | Purpose |
|------|---------|---------|
| `claude` | npm install -g @anthropic-ai/claude-code | Claude Code CLI (coding agent) |
| `codex` | npm install -g @openai/codex | OpenAI Codex CLI (coding agent) |
| `omniroute` | npm install -g omniroute | Local LLM router (80+ models) |
| `gemini` | (openclaw skill) | Gemini CLI |
| `notebooklm-py` | pip install notebooklm-py | Google NotebookLM automation |

---

## 📊 Data / Finance

| Tool | Install | Purpose |
|------|---------|---------|
| `yfinance` | pip install yfinance | Financial data (XAUUSD, DXY, stocks) |
| `duckduckgo-search` | pip install duckduckgo-search | Web search (no API key) |
| `openai` (python) | pip install openai | OpenAI-compatible API client |
| `requests` | pip install requests | HTTP client |
| `sqlite3` | built-in | OmniRoute DB, local storage |

---

## 🎬 Content / Media

| Tool | Install | Purpose |
|------|---------|---------|
| `ffmpeg` | apt install ffmpeg | Video processing |
| PostBridge API | (API key: pb_live_AT9Xm4PKaYBzAvFZYGgexi) | Social media posting automation |
| NanoBanana API | (openclaw skill) | AI image generation |

---

## 🛠️ Dev Tools

| Tool | Install | Purpose |
|------|---------|---------|
| `gh` | apt install gh | GitHub CLI |
| `git` | built-in | Version control |
| `bun` | install via bun.com | TypeScript runtime (for Dexter) |
| `python3` | built-in | Python scripts |
| `node` / `npm` | built-in | Node.js ecosystem |
| `pip` | built-in | Python package manager |

---

## 🔑 Credentials / Auth (location)

| Service | Location | Expires |
|---------|----------|---------|
| Google (NotebookLM) | `~/.notebooklm_playwright.json` | ~May 14 2026 |
| Twitter/X | `~/.bashrc` (env vars) | ~Mar 2027 |
| Antigravity (71 accounts) | OmniRoute DB: `~/.omniroute/storage.sqlite` | ~2027 |
| PostBridge | TOOLS.md + env | — |
| GitHub | `~/.config/gh/hosts.yml` | — |
| OmniRoute API Key | `~/.openclaw/openclaw.json` | — |
| Antigravity client_secret | `/etc/systemd/system/omniroute.service` env | — |

---

## 📦 Python Packages (pip)

```bash
pip install --break-system-packages \
  notebooklm-py \
  twitter-cli \
  yfinance \
  openai \
  duckduckgo-search \
  requests
```

---

## 📦 NPM Global Packages

```bash
npm install -g \
  openclaw \
  omniroute \
  @jackwener/opencli \
  @anthropic-ai/claude-code
```

---

## 🔄 Restore Checklist (Fresh Install)

```bash
# 1. System packages
sudo apt install -y nvidia-driver cloudflared ffmpeg gh git

# 2. NPM globals
npm install -g openclaw omniroute @jackwener/opencli @anthropic-ai/claude-code

# 3. Python packages
pip install --break-system-packages notebooklm-py twitter-cli yfinance openai duckduckgo-search requests

# 4. Configure OmniRoute service
sudo cp omniroute.service /etc/systemd/system/
sudo systemctl enable --now omniroute

# 5. Add Antigravity secret to service
sudo sed -i '/Environment=PATH=/a Environment=ANTIGRAVITY_OAUTH_CLIENT_SECRET=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' /etc/systemd/system/omniroute.service
sudo systemctl daemon-reload && sudo systemctl restart omniroute

# 6. Set Twitter env vars in ~/.bashrc
# TWITTER_AUTH_TOKEN=<from backup>
# TWITTER_CT0=<from backup>

# 7. Restore Google cookies to ~/.notebooklm_playwright.json

# 8. Clone workspace + skills
git clone https://github.com/oyi77/1ai-workspace.git
git clone https://github.com/oyi77/1ai-skills.git
```
