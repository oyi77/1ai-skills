# MEMORY INDEX - Quick Reference

> Use this to find lessons BEFORE you repeat mistakes
> READ THIS FIRST whenever starting new work

## 🚨 CRITICAL LESSONS (Read Before Any Work)

### Browser Automation
**Issue:** New tabs don't persist, "tab not found" errors
**Solution:** Check `browser tabs` first, reuse existing targetIds
**Location:** `notes/browser-tool-critical-gotchas.md`
**Learned:** March 10, 2026

### Cashflow Tracking
**Issue:** 48+ hours blind, decisions without data
**Solution:** Check bank balance FIRST thing (5 min), document in cashflow/
**Status:** 🚨 STILL CRITICAL - IDR 0 balance
**Learned:** March 9, 2026

### PostBridge API
**Issue:** HTTP 500 looks like rate limit but isn't
**Solution:** Check logs for HTTP status codes, distinguish internal vs external failures
**Learned:** March 8, 2026

### Autonomous Execution
**Issue:** Asking permission for clear-value tasks
**Solution:** Execute autonomously on obvious tasks, report after
**Rule:** Revenue > Permission
**Learned:** March 8, 2026

---

## 📁 Memory Files by Topic

### Browser & Automation
- `notes/browser-tool-critical-gotchas.md` - Tab management workaround
- `MEMORY.md` - Browser tool section

### Cashflow & Revenue
- `cashflow/2026-03-09.md` - IDR 0 confirmed, emergency protocol
- `memory/revenue-opportunity-map.md` - Revenue sources tracking
- `notes/open-loops.md` - Critical blocker tracking

### LYNK & Affiliate
- `memory/lynk_skill_enhancement.md` - Platform learning
- `memory/lynk_product_verification.md` - Product verification attempt
- `memory/lynk_verification_complete.md` - Campaign status confirmed
- Skills: `skills/lynk/` - Full LYNK skill

### Trading
- `memory/2026-03-05.md` - Trading strategy
- `memory/2026-03-06-0900-trading-monitor.md`
- `memory/2026-03-05-trading-monitor.md` (multiple)
- Docs: `.vilona/knowledge/trading/principles.md`

### Marketing & Content
- JENDRALBOT campaign - 100 posts scheduled
- Content generation skills in `skills/content-creator/`
- Social automation in `skills/tiktok-automation/`

### PostBridge API
- Logs: `logs/postbridge_upload_log.txt`
- Retry script: `scripts/retry_postbridge_failed.py`
- Debug: `scripts/debug_postbridge.py`

---

## 🗂️ File Structure

```
~/.openclaw/workspace/
├── MEMORY.md                      # Curated long-term lessons
├── notes/                         # Topic-specific notes
│   ├── browser-tool-critical-gotchas.md
│   ├── open-loops.md
│   └── revenue-opportunity-map.md
├── memory/YYYY-MM-DD.md           # Daily logs (30+ files)
├── cashflow/YYYY-MM-DD.md         # Cashflow tracking
├── logs/                          # System logs
├── skills/                        # Agent skills
│   ├── lynk/
│   ├── content-creator/
│   ├── tiktok-automation/
│   └── [other skills]
└── .vilona/knowledge/             # Deep knowledge base
    └── trading/
```

---

## 🚨 Open Loops (Critical Blockers)

**From `notes/open-loops.md`:**
1. Cashflow blindness (48+ hours) - 🚨 EMERGENCY
2. PostBridge retry needed (if API fails)
3. Revenue tracking setup needed

---

## 💡 Daily Startup Checklist

**Before ANY work, READ in order:**

1. ✅ `SOUL.md` - Who I am, principles
2. ✅ `USER.md` - Who I'm helping
3. ✅ `memory/YYYY-MM-DD.md` - Today's context
4. ✅ `MEMORY.md` - Long-term lessons
5. ✅ `notes/open-loops.md` - Critical blockers
6. ✅ **THIS FILE** - Memory index

**Then:** Check if relevant lessons exist for your task

---

## 🔍 Quick Search Commands

```bash
# Find lessons about browser
grep -r "browser" memory/*.md notes/*.md

# Find LYNK lessons
grep -r "lynk" memory/*.md skills/lynk/*.md

# Find cashflow issues
grep -r "cashflow" memory/*.md cashflow/*.md

# Find open loops
cat notes/open-loops.md
```

---

## 📋 Recent Critical Events

**March 10, 2026 (04:00):**
- LYNK products verified ACTIVE (was concerned they weren't)
- Browser tool lesson documented (tab management bug)
- Campaign ready to launch (42 posts 08:00-11:30)

**March 9, 2026 (15:50):**
- Cashflow confirmed IDR 0 🚨
- Emergency protocol activated
- Revenue generation = 100% priority

**March 8, 2026 (evening):**
- PostBridge HTTP 500 outage resolved
- 42 failed posts rescheduled successfully
- Autonomous execution lesson learned

**March 7, 2026:**
- Weekend protocol created (cashflow, marketing, trading)
- 100 Instagram posts campaign launched (JENDRALBOT)
- Disk cleanup (14.7 GB freed, 91% → 76%)

---

## ⚠️ Common Mistakes Pattern

### Pattern 1: Not Reading Memory First
**Symptoms:** Repeating old mistakes, user frustration
**Fix:** Create this index → Read before work

### Pattern 2: Assuming Instead of Verifying
**Symptoms:** "Products not activated" (was wrong)
**Fix:** Always verify with actual data

### Pattern 3: Planning Without Execution
**Symptoms:** 0% action, 0% revenue, 100% planning
**Fix:** Execute first, analyze later

---

## 🎯 Skills Available (Quick Reference)

### Core Skills
- **lynk** - Affiliate link management
- **content-creator** - Social media content generation
- **tiktok-automation** - Automated posting
- **trading** - XAUUSD trading
- **analytics-dashboard** - Revenue tracking

### Infrastructure
- **github** - Operations via gh CLI
- **healthcheck** - Security & system checks
- **obsidian** - Knowledge management

---

## 🔐 Important Credentials (Locations)

**LYNK:**
- Email: ketananna@yahoo.com
- Password: See `.vilona/secrets/lynk.md` (if exists)
- Dashboard: https://lynk.id/dashboard

**PostBridge:**
- API Key: `pb_live_AT9Xm4PKaYBzAvFZYGgexi`
- Account ID: 47681

**Telegram:**
- Bot Token: `8581574594:AAGzrA9DGjzJx3Ak2D6P3NhoQyXyskpMF2Q`
- User ID: 5220170786

---

## 📊 Campaign Status

**JENDRALBOT Affiliate:**
- Products: 9 active (2 FREE, 7 paid)
- Price Range: FREE - IDR 2M
- Posts Scheduled: 100 (42 launching March 10, 08:00-11:30)
- Revenue Estimate: IDR 150K-4.5M/week
- Expected First Revenue: 24-48 hours after launch

**XAUUSD Trading:**
- Strategy: Asia 7-candle breakout
- Win Rate: 61.4%
- Profit Factor: 4.1
- Entry Time: 15:00 UTC+7
- Status: Paper trading, not automated yet

---

## 📈 Key Metrics

**Cashflow:** IDR 0 (March 9, 2026 - 🚨 CRITICAL)
**Disk:** 76% (26 GB free) - SAFE
**Revenue Gap:** 0.0 hours - OK
**PostBridge:** Working - OK

---

## 🔗 Quick Links

- LYNK Dashboard: https://lynk.id/dashboard
- PostBridge API: https://api.post-bridge.com/v1
- GitHub Repo: https://github.com/openclaw/openclaw
- Community: https://discord.com/invite/clawd

---

**Last Updated:** March 10, 2026, 04:05 UTC+7
**Purpose:** Prevent repeating mistakes by having quick access to all lessons
**Usage:** READ THIS before starting ANY task, then check relevant sections

---

## ✅ Maintenance Tasks

- [ ] Update INDEX.md after each major lesson learned
- [ ] Consolidate duplicate memory files
- [ ] Remove outdated memory entries
- [ ] Add new lessons to relevant sections
- [ ] Cross-reference between MEMORY.md and INDEX.md
## 2026-03-12: No Redundant Files
**Location:** MEMORY.md, AGENTS.md
**Trigger:** Creating new scripts without checking existing
**Rule:** ALWAYS search memory + skills BEFORE creating ANY new file
**Key Files:** sequential_video_generator.py, multi_stage_i2v.py, berkah_viral_automation.py

## 2026-03-12: Skill Organization (CRITICAL)
**Rule:** ALL skills in 1ai-skills/, symlink to workspace/skills/
**Location:** MEMORY.md
**Categories:** content, marketing, sales, automation, research, productivity, trading, core
