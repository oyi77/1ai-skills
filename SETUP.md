# 1ai-skills - Setup Guide

This guide walks you through setting up 1ai-skills.

## Current Status: 80 Skills Complete ✅

## Installation

### Quick Install
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/oyi77/1ai-skills.git
cd 1ai-skills
npm install
```

For detailed agent-specific installation, see INSTALL.md

## User Action Required

### 1. Install Dependencies for Trading Skills
```bash
# For MetaTrader 5
pip install MetaTrader5

# For crypto exchanges
pip install ccxt

# For data analysis
pip install pandas pytz
```

### 2. Configure Environment Variables (Optional)
Create `~/.ai-company/env` with your API keys:
```bash
mkdir -p ~/.ai-company
cat > ~/.ai-company/env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-xxx
BROWSER_USE_API_KEY=bu_xxx
GITHUB_TOKEN=ghp_xxx
EOF
```

### 3. Verify Skills Load
After setup, test with:
```
Load trading skill
Load brainstorming skill
```

## Files Created

| File | Purpose |
|------|---------|
| README.md | Project overview |
| INSTALL.md | Agent-specific installation guide |
| LLM.md | LLM-friendly installation |
| SKILL_INDEX.json | All skills metadata (80 skills) |
| trading/ | Trading skills system |
| + 70+ more skill directories |

## Quick Start

1. Clone: `git clone https://github.com/oyi77/1ai-skills.git`
2. Install: `npm install`
3. Test: "Load trading skill"

---

*Last Updated: 2026-02-17*
