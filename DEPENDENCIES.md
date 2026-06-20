# 1ai-skills Dependencies

This document lists all external dependencies required by skills in the 1ai-skills repository.

## Quick Install

```bash
# Install MCP tools (cbm + agent-reach) - runs automatically on npm install
npm run postinstall

# Install skill dependencies (optional, for specific skills)
npm run install:deps

# Dry run (see what would be installed)
npm run install:deps:dry-run

# Install specific category
node scripts/install-skill-deps.js python
node scripts/install-skill-deps.js npm
node scripts/install-skill-deps.js brew
```

## Dependency Categories

### MCP Servers (Auto-installed)

**Installed automatically via postinstall:**
- `cbm` (codebase-memory-mcp) — Code intelligence for 158 languages
- `agent-reach` — Universal internet scraper (Twitter, Reddit, YouTube, 35+ platforms)

**Skills using these:** 14 MCP skills, 23 research skills, 45 marketing skills

---

### NPM Packages (Optional)

```bash
npm install -g wscat newman flowise
```

| Package | Used By | Purpose |
|---------|---------|---------|
| `wscat` | automation/websocket-client | WebSocket testing |
| `newman` | development/api-testing | Postman collection runner |
| `flowise` | automation/flowise-builder | Low-code LLM apps |

**Skills:** 9 automation, 17 content (UI frameworks are project-specific)

---

### Python Packages (Optional)

**Note:** Many cybersecurity tools require Python 3.9+ and may conflict with system packages. Use `pipx` for CLI tools or virtual environments for libraries.

#### Cybersecurity Essentials

```bash
# Install via pipx (recommended for CLI tools)
pipx install semgrep trufflehog sqlmap shodan dnstwist oletools sslyze checkov prowler

# Install via pip (libraries)
pip3 install requests scapy impacket pwntools frida-tools volatility3 yara-python pefile boto3
```

| Package | Category | Purpose |
|---------|----------|---------|
| `semgrep` | SAST | Static code analysis |
| `trufflehog` | Secret scanning | Detect credentials in code |
| `sqlmap` | Web security | SQL injection testing |
| `shodan` | Recon | Internet-connected device search |
| `dnstwist` | Phishing | Domain typosquatting detection |
| `impacket` | Network | Windows protocol toolkit |
| `pwntools` | Exploit dev | CTF/binary exploitation |
| `frida-tools` | Mobile | Dynamic instrumentation |
| `volatility3` | Forensics | Memory analysis |
| `scapy` | Network | Packet manipulation |
| `yara-python` | Malware | Pattern matching |
| `pefile` | Malware | PE file analysis |
| `oletools` | Office | Macro analysis |
| `sslyze` | TLS | SSL/TLS scanner |
| `boto3` | Cloud | AWS SDK |
| `checkov` | IaC | Terraform/CloudFormation scanner |
| `prowler` | Cloud | AWS security auditing |

#### Content & Media

```bash
pip3 install moviepy edge-tts faster-whisper
```

| Package | Purpose |
|---------|---------|
| `moviepy` | Video editing |
| `edge-tts` | Text-to-speech |
| `faster-whisper` | Speech-to-text |

#### Utilities

```bash
pip3 install requests jinja2 pyjwt watchdog websockets telethon
```

| Package | Purpose |
|---------|---------|
| `requests` | HTTP client |
| `jinja2` | Template engine |
| `pyjwt` | JWT tokens |
| `watchdog` | File system monitoring |
| `websockets` | WebSocket client |
| `telethon` | Telegram automation |

**Skills:** 253 cybersecurity, 17 content, 9 automation

---

### Homebrew Packages (macOS/Linux, Optional)

```bash
brew install ffmpeg yara trivy semgrep trufflehog git-secrets cosign tfsec terrascan kubeaudit
```

| Package | Category | Purpose |
|---------|----------|---------|
| `ffmpeg` | Media | Video/audio processing |
| `yara` | Malware | Pattern matching |
| `trivy` | Container | Vulnerability scanner |
| `semgrep` | SAST | Static analysis |
| `trufflehog` | Secrets | Credential detection |
| `git-secrets` | Git | Prevent secret commits |
| `cosign` | Supply chain | Container signing |
| `tfsec` | IaC | Terraform security |
| `terrascan` | IaC | Multi-IaC scanner |
| `kubeaudit` | Kubernetes | Security audit |

**Skills:** 38 devops, 33 development, 253 cybersecurity

---

## API Keys (Optional)

Configure in `~/.omp/mcp.json` or environment variables:

| Key | Used By | How to Get |
|-----|---------|------------|
| `OPENAI_API_KEY` | core/ai features | https://platform.openai.com/api-keys |
| `ANTHROPIC_API_KEY` | core/claude features | https://console.anthropic.com |
| `GOOGLE_API_KEY` | core/gemini features | https://makersuite.google.com/app/apikey |
| `GITHUB_TOKEN` | integrations/github | https://github.com/settings/tokens |
| `TWITTER_API_KEY` | marketing/twitter | https://developer.twitter.com |
| `SLACK_API_KEY` | integrations/slack | https://api.slack.com/apps |
| `NOTION_API_KEY` | integrations/notion | https://www.notion.so/my-integrations |
| `STRIPE_API_KEY` | operations/payment | https://dashboard.stripe.com/apikeys |

**Skills:** 32 integrations, 10 productivity, 45 marketing

---

## Skill Statistics

**Total skills:** 1,310  
**Skills with external dependencies:** 301 (23%)

### By Category

| Category | Skills with deps | Total skills | % |
|----------|------------------|--------------|---|
| cybersecurity | 253 | 785 | 32% |
| content | 17 | 55 | 31% |
| automation | 9 | 28 | 32% |
| marketing | 5 | 45 | 11% |
| core | 4 | 42 | 10% |
| productivity | 3 | 10 | 30% |
| integrations | 3 | 32 | 9% |
| research | 2 | 23 | 9% |
| trading | 2 | 20 | 10% |
| operations | 1 | 19 | 5% |
| development | 1 | 83 | 1% |
| meta | 1 | 13 | 8% |

---

## Installation Tips

### For Cybersecurity Skills

Most cybersecurity tools should be installed in isolated environments:

```bash
# Option 1: pipx (recommended for CLI tools)
pipx install tool-name

# Option 2: Virtual environment (for libraries)
python3 -m venv ~/.local/share/security-tools
source ~/.local/share/security-tools/bin/activate
pip install tool-name
```

### For Content/Media Skills

```bash
# FFmpeg is essential for video/audio processing
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Ubuntu/Debian

# Python media packages
pip3 install moviepy edge-tts faster-whisper
```

### For Automation Skills

```bash
# Node.js tools
npm install -g wscat newman flowise

# Telegram bot
pip3 install telethon
```

---

## Troubleshooting

### `externally-managed-environment` error

Use `pipx` or virtual environments instead of system pip:

```bash
# Install pipx
brew install pipx  # macOS
sudo apt install pipx  # Ubuntu

# Install tools with pipx
pipx install tool-name
```

### Permission denied on `/usr/local/bin`

The MCP installer will prompt for sudo when needed. Or install manually:

```bash
sudo install -m 755 binary /usr/local/bin/name
```

### Python module not found after install

Ensure you're using the same Python:

```bash
which python3
python3 --version
python3 -m pip list | grep package-name
```

---

## See Also

- [MCP Servers](mcp/) — Full list of MCP skills
- [Cybersecurity Skills](cybersecurity/AGENTS.md) — 785 security skills by subdomain
- [Contributing](CONTRIBUTING.md) — Add new skills
- [Quick Start](QUICK_START.md) — Get started with 1ai-skills
