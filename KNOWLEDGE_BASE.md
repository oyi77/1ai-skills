# Business Kingdom Knowledge Base (Core Stack)

This document is the authoritative reference for the current OpenClaw "Business Kingdom" infrastructure. It maps the scattered components into a unified system.

## 🏛️ Core Architecture: Chain of Command
The system is built on specialized "islands" of automation, orchestrated by OpenClaw.

1.  **Commander (OpenClaw Main Agent)**: 
    - Role: Goal-setting and high-level decision making.
    - Identity: Vilona (General Manager & Business Development).
    - Status: **Operational.**
2.  **Middle Management (Workflow Center / Paperclip)**:
    - **Paperclip**: Task management and revenue tracking. Port `:3100`.
    - **Workflow Center**: Real-time monitoring and setting AI behavior thresholds. Port `:19527`.
3.  **Operations Engine (n8n)**:
    - Role: Webhooks, complex data transformations, and scheduled workflows.
    - Status: **Awaiting better OpenClaw integration.**
4.  **Worker Fleet (Scripts/Skills)**:
    - Located in: `~/scripts/` and `~/1ai-skills-bundle/`.
    - Capabilities: Content generation, video editing, social posting.

## 🔧 Infrastructure Details

### 📡 Communications & Posting (PostBridge)
- **API Status**: Operational. 
- **Endpoint**: `https://api.post-bridge.com/v1`
- **Analytics**: Supported via `/v1/analytics`. Requires periodic sync.
- **Rules**: Instagram posts MUST have media.

### 💰 Cashflow & Banking
- **BCA Tracking**: Automated via `scripts/bca_balance_v2.py`.
- **LYNK tracking**: Automated via `scripts/lynk_monitor.py` (Browser-based).
- **Consolidated State**: Draft in `scripts/central_state_monitor.py`.

### 💾 Storage & Environment
- **Disk Usage**: 89-91% (Critical zone is >95%). Cleanup script: `scripts/disk_cleanup_automation.py`.
- **Operating System**: Kali Linux.
- **Working Directory**: `/home/openclaw/.openclaw/workspace`.

## ⚙️ The "Perfect Architecture" Blueprint
To reach full autonomous revenue generation, the stack must transition from **Task-Based** to **Goal-Based**.

### Goal: Autonomous Revenue Loop
1.  **Watcher** (scripts): Detects shifts in `state.json` (e.g., balance drop or view spike).
2.  **Planner** (OpenClaw): Receives alert, consults logic in `AGENTS.md`.
3.  **Executors** (n8n/Skills): Spawned via `sessions_spawn` to generate content or trade.
4.  **Reporter** (Telegram): Notifies Coder $String$ of actions taken and results.

## 📂 Critical Folder Inventory
- `1ai-skills-bundle/`: Core library of reusable AI skills.
- `scripts/`: Implementation scripts for daily operations.
- `memory/`: Durable session logs and lessons learned.
- `notes/`: Business strategy and market research intelligence.

---
*Updated: 2026-03-17 00:30 UTC+7 by Vilona*
