# WORKFLOW_AUTO.md - Automated Workflows

_This file defines automated workflows that run periodically or on specific triggers._

## 🤖 Active Workflows

### 1. ChromaDB Re-index (Daily)

**Trigger:** Daily cron (every 6 hours)
**Purpose:** Keep ChromaDB knowledge base synchronized with latest skills, memory, and context

**Command:**
```bash
cd /home/openclaw/.openclaw/workspace
~/.trading-venv/bin/python openclaw_chroma_global.py index-all
```

**When to run:**
- After creating new skills
- After updating memory files
- After editing context files (SOUL.md, USER.md, etc.)

---

### 2. Trading Strategy Backtests (Periodic)

**Trigger:** Manual or weekly
**Purpose:** Run backtests on all strategies to track performance over time

**Command:**
```bash
cd /home/openclaw/.openclaw/workspace/skills/1ai-skills/trading
~/.trading-venv/bin/python run_backtests_with_path.py
```

**Strategies to test:**
- XAUUSD Asia 7-Candle Breakout (PROVEN)
- Holy Grail Strategy (to be developed)
- Kumo Breakout Strategy (to be developed)
- Momentum Elder Strategy (to be developed)
- Volume Momentum Strategy (to be developed)

**Pairs:** XAUUSD, GBPUSD, EURUSD, USDJPY, BTCUSDT, ETHUSDT, SOLUSDT

---

### 3. Memory Maintenance (Weekly)

**Trigger:** Weekly cron (every Sunday)
**Purpose:** Review daily memory files and update MEMORY.md with distilled insights

**Command:** (Manual)
- Read all `memory/YYYY-MM-DD.md` files from past week
- Identify significant events, decisions, lessons
- Update `MEMORY.md` with curated wisdom
- Archive old daily files if needed

---

### 4. Heartbeat Checks (Every 30 minutes)

**Trigger:** User heartbeat message
**Purpose:** Proactive checks for important items

**Checklist:**
- [ ] Email inbox (urgent messages?)
- [ ] Calendar (upcoming events in 24-48h?)
- [ ] Notifications (Twitter/social mentions?)
- [ ] Weather (if going out today?)

**When to reach out:**
- Important email arrived
- Calendar event coming up (<2h)
- Something interesting found
- It's been >8h since last message

**When to stay quiet (HEARTBEAT_OK):**
- Late night (23:00-08:00) unless urgent
- Human is clearly busy
- Nothing new since last check
- Just checked <30 minutes ago

---

### 5. Trading Strategy Comparison (Daily)

**Trigger:** Daily cron (after backtests complete)
**Purpose:** Generate comparison report of all strategy performance

**Command:**
```bash
cd /home/openclaw/.openclaw/workspace
~/.trading-venv/bin/python compare_strategies.py
```

**Output:** `berkahkarya_quant_daily_report.md`

**Metrics to compare:**
- Win Rate
- Net PNL
- Profit Factor
- Max Drawdown
- Total Trades
- Sharpe Ratio

---

## 📋 Workflow States

### Workflow: ChromaDB Re-index

**Status:** ✅ Active (manual for now)

**Last Run:** 2026-02-23 06:47

**Next Run:** Manual trigger or scheduled via cron

**Configuration:**
```bash
# Add to crontab (optional)
0 */6 * * * /home/openclaw/.trading-venv/bin/python /home/openclaw/.openclaw/workspace/openclaw_chroma_global.py index-all
```

---

### Workflow: Trading Backtests

**Status:** ⏸️ Paused (waiting for strategy development)

**Proven Strategy:** XAUUSD Asia 7-Candle Breakout
- Win Rate: 61.4%
- Net PNL: +$528 (+528%)
- Profit Factor: 4.1
- Max Drawdown: 0.5%

**Next Steps:**
1. Develop simplified versions of other strategies
2. Run comprehensive backtests
3. Generate comparison report
4. Deploy best performers to live trading

---

### Workflow: Memory Maintenance

**Status:** ✅ Active (weekly)

**Last Review:** 2026-02-23

**Next Review:** 2026-03-02

**Procedure:**
1. Read `memory/2026-02-*.md` files
2. Extract significant insights
3. Update `MEMORY.md` with distilled wisdom
4. Remove outdated info

---

### Workflow: Heartbeat Checks

**Status:** ✅ Active

**Last Check:** 2026-02-23 06:47

**Check Interval:** Every 30 minutes (triggered by user)

**Tracking File:** `memory/heartbeat-state.json`

---

## 🔄 Trigger Types

### 1. Cron Triggers

Automated, time-based triggers:

```bash
# Example crontab entries
0 */6 * * *     # Every 6 hours (ChromaDB re-index)
0 0 * * 0       # Weekly (Sundays at midnight - Memory maintenance)
0 8 * * *       # Daily at 8 AM (Trading backtests)
```

---

### 2. Manual Triggers

User-initiated triggers:

```
User: "run backtests now"
→ Execute trading backtest workflow

User: "reindex chroma"
→ Execute ChromaDB re-index workflow

User: "check heartbeat"
→ Execute heartbeat check workflow
```

---

### 3. Event Triggers

Automatic triggers based on file changes:

```python
# Example: Auto-index when skill is modified
if file_modified("skills/xyz/SKILL.md"):
    run_workflow("chroma_reindex")

# Example: Auto-backup when memory is updated
if file_modified("memory/YYYY-MM-DD.md"):
    run_workflow("memory_backup")
```

---

## 🎯 Next Steps

### Immediate (Today)

1. ✅ Create WORKFLOW_AUTO.md ← DONE
2. [ ] Set up ChromaDB auto-index cron (optional)
3. [ ] Test heartbeat check workflow

### Short-term (This Week)

1. [ ] Complete strategy development (Holy Grail, Kumo, etc.)
2. [ ] Run comprehensive backtests
3. [ ] Generate daily comparison reports
4. [ ] Set up weekly memory maintenance

### Long-term (This Month)

1. [ ] Implement event-driven triggers
2. [ ] Set up automated backups
3. [ ] Create workflow dashboard
4. [ ] Monitor workflow performance

---

## 📊 Workflow Metrics

Track workflow execution to optimize:

```json
{
  "chroma_reindex": {
    "last_run": "2026-02-23T06:47:00Z",
    "duration_seconds": 5.2,
    "status": "success",
    "items_indexed": 90
  },
  "trading_backtest": {
    "last_run": "2026-02-23T02:51:00Z",
    "duration_seconds": 240.5,
    "status": "partial",
    "strategies_tested": 1,
    "strategies_failed": 38
  },
  "heartbeat_check": {
    "last_run": "2026-02-23T06:47:00Z",
    "duration_seconds": 0.5,
    "status": "success",
    "alerts": 0
  }
}
```

---

## 🔧 Workflow Management

### Add New Workflow

1. Define workflow purpose and trigger
2. Write command/script
3. Test manually
4. Add to this file
5. Schedule via cron or event trigger

### Remove Workflow

1. Mark as "Inactive" in this file
2. Remove cron entry (if applicable)
3. Archive old workflow data

### Modify Workflow

1. Update workflow definition
2. Test changes
3. Update this file
4. Deploy changes

---

## 📝 Notes

- All workflows should be idempotent (safe to run multiple times)
- Workflows should log output to appropriate files
- Workflows should handle errors gracefully
- Workflows should report status to user

---

## 🚀 Automation Goals

**Current State:** Manual workflows, some semi-automated

**Target State:** Fully automated, event-driven workflows

**Benefits:**
- Reduced manual intervention
- Faster response to changes
- Better knowledge base synchronization
- Proactive monitoring and alerts

---

*Last Updated: 2026-02-23*
*Author: OpenClaw*
