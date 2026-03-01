# 1ai-Skills-Bundle Perfection — Autonomous AI Manager

## Overview

This is the BerkahKarya AI Autonomous Manager system - a fully autonomous AI Manager that generates revenue across 3 streams, discovers opportunities, manages tasks, and actively enforces team accountability.

## Features

### Core Systems
- **Vilona v4.0 Persona** - Bilingual (Indonesian/English), revenue-first, enforcement mode
- **Task Manager** - Full CRUD with SQLite backend, assignment, deadlines, priority
- **Multi-Channel Notifier** - Telegram, Email, WhatsApp notifications
- **MAKI Protocol** - Escalation: Warning 1 → 2 → 3 → MAKI mode

### Revenue Pipelines
- **Content Pipeline** - Research → Generate → Approve → Post with guardrails
- **Trading Pipeline** - Paper trading with circuit breakers and kill switches
- **AI Services Pipeline** - Lead generation and outreach automation
- **Revenue Dashboard** - Real-time tracking across all streams

### Automation
- **Cron Jobs** - 7 automated jobs (content, market scan, trading, tasks, revenue, weekly review)
- **Heartbeat** - 30-minute health checks (deadlines, signals, credentials, system)
- **Self-Healing** - Retry logic with exponential backoff, recovery strategies

### Intelligence
- **Opportunity Scout** - Market scanning and scoring
- **Strategic Recommendations** - Weekly analysis and actionable insights

### Interfaces
- **Telegram Bot** - Commands: /task, /status, /remind, /maki, /revenue
- **Team Onboarding** - Per-member notification preferences

## Installation

```bash
# Clone the workspace
cd /home/openclaw/.openclaw/workspace

# Run tests
python -m pytest tests/ -v

# Start heartbeat
python -m automation.heartbeat

# Run cron jobs
python -m automation.cron_setup
```

## Quick Start

```python
# Task Manager
from skills.task_manager.api import TaskAPI
api = TaskAPI()
task = api.create(title="New Task", assignee="Veris", deadline="2026-03-01")

# Revenue Dashboard
from skills.revenue_dashboard.dashboard import RevenueDashboard
dashboard = RevenueDashboard()
revenue = dashboard.get_total()

# Telegram Bot
from skills.telegram_bot.commands import BotCommands
bot = BotCommands()
bot.handle_command("/help", [], "User")
```

## Module Structure

```
skills/
├── task-manager/         # Task CRUD, enforcement, notifications
├── telegram-bot/         # Bot commands
├── revenue-dashboard/    # Revenue tracking
├── content/              # Content pipeline with guardrails
├── trading/              # Trading pipeline with guardrails
├── ai-services/          # Lead generation
├── opportunity-scout/     # Market scanning
└── strategic-recommendations/  # Weekly analysis

automation/
├── cron_setup.py         # Cron job configuration
├── heartbeat.py          # Health monitoring
├── self_healing.py      # Auto-recovery
└── team_onboarding.py    # Team preferences
```

## Tests

```bash
# Run all tests
pytest tests/ -v

# E2E tests
pytest tests/e2e_*.py -v
```

## Revenue Streams

1. **Content** - TikTok, social media automation
2. **Trading** - Paper trading with live signals
3. **Services** - AI services lead generation

## Safety Guardrails

- Trading: Circuit breaker, kill switch, daily loss limit
- Content: Rate limiter, approval queue, brand safety
- Notifications: Quiet hours (23:00-07:00)

## License

BerkahKarya AI - Internal Use First, Then Sale
