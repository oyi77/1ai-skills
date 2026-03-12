# TOOLS.md - Tool Configuration & Notes

> Document tool-specific configurations, gotchas, and credentials here.

---

## 🌐 Browser Tool (browser)

**Status:** ⚠️ Known Bug - Tab Management Issue

**Configuration:**
```
Profile: openclaw
Browser: Vivaldi (Chromium-based)
CDP Port: 18800
Location: /home/openclaw/.openclaw/browser/openclaw/user-data
```

**🚨 CRITICAL GOTCHA - New Tabs Don't Persist:**
- New tabs created with `browser open` become invalid/deatched within seconds
- TargetIds from new tabs fail immediately with "tab not found" error
- EXISTING tabs from previous sessions remain valid indefinitely

**✅ WORKAROUND - Always Check Existing Tabs First:**
```bash
# Step 1: List all existing tabs
browser tabs

# Step 2: Find your target page in the output
# Look for matching URL or title

# Step 3: Use the existing targetId
browser snapshot {existing-targetId}  # SUCCESS

# Navigate if needed
browser navigate {existing-targetId} https://new-url.com
```

**❌ ANTI-PATTERN - Never Do This:**
```bash
# Don't open new tab unless absolutely necessary
browser open openclaw https://url.com
targetId = {returned-id}

# Delay, then use targetId → FAILS
sleep(5)
browser snapshot targetId  # ERROR: tab not found
```

**When to Open New Tab:**
- Only when target page doesn't exist in tabs list
- When you need fresh session (no existing cookies)
- When you have authentication conflicts

**If You Must Open New Tab:**
- Use IMMEDIATELY (no waiting/delay)
- Don't save targetId for reuse later
- Re-check tabs before next operation

**Key TargetIds (for LYNK work):**
```
LYNK Profile: DCE5D44ECC64A4B6244E28F796792E7D
LYNK Register: 288E7E5ECCA0F1D05E1A393622549FE0
```

**Documentation:** See `notes/browser-tool-critical-gotchas.md` for full details

---

## 🔍 Brave Search API (web_search)

**Status:** ⚠️ Issue - Rate limited

**Configuration:**
```
Plan: Free
Rate Limit: 1 request/second
Quota: 2,000 requests/month
Current Usage: 20/2000 (1%)
```

**Gotchas:**
- Rate limit can be hit easily with batched searches
- Error 429: "Request rate limit exceeded for plan"
- Workaround: Implement request batching/delay or upgrade plan

**Common Operations:**
```python
# Single search
web_search(query="test", count=5)

# Batch searches - add delay
for query in queries:
    result = web_search(query=query, count=5)
    time.sleep(2)  # Rate limit delay
```

---

## 💹 Trading: Ostium Broker (trading_monitor.py)

**Status:** ❌ Not configured

**Configuration:**
```python
broker_config = {
    'api_key': '',
    'api_secret': '',
    'account_id': '',
    'paper_mode': True
}
```

**Gotchas:**
- Python SDK needs installation
- Authentication required before paper trading
- Paper trading must be activated first
- Live trading requires separate account

**Required Setup:**
1. Install Ostium Python SDK
2. Configure API credentials
3. Test paper trading connection
4. Verify order placement works

**Files:**
- `/home/openclaw/.openclaw/workspace/scripts/trading_monitor.py` (template created)
- Documentation in `.vilona/knowledge/trading/principles.md`

---

## 📡 PostBridge API (UPDATED March 12, 2026)

**Status:** ✅ Working - Full API access confirmed

**API Reference:** https://api.post-bridge.com/reference
**Base URL:** https://api.post-bridge.com/v1
**API Key:** pb_live_AT9Xm4PKaYBzAvFZYGgexi
**Rate Limit:** 10 requests/second/key
**Auth:** Bearer token

**Endpoints:**
- `GET /v1/analytics` — View counts, likes, comments, shares
- `POST /v1/analytics/sync` — Trigger analytics refresh (TikTok/YouTube/Instagram)
- `GET /v1/posts` — List all posts (filter by platform/status)
- `POST /v1/posts` — Create post (needs: caption, scheduled_at, social_accounts[], media[])
- `GET /v1/post-results` — Check success/failure of each post
- `GET /v1/social-accounts` — Connected accounts
- `POST /v1/media/create-upload-url` — Upload media for posts

**🚨 CRITICAL: Instagram posts REQUIRE media (images/videos)**
- 26 posts FAILED with: "No supported media files found"
- ALWAYS include media[] when posting to Instagram
- Upload media first via /media/create-upload-url, then attach media_id to post

**Connected Accounts (12 total):**
- TikTok: 7 accounts
- Instagram: 1 account (berkahkaryadigitalproduct)
- Facebook: 4 accounts

**Full reference:** `notes/postbridge-api-reference.md`

---

## 📈 Marketing: LYNK Dashboard

**Status:** ✅ Working - Account exists

**Configuration:**
```
Dashboard: https://lynk.id/jendralbot
Status: Active
Campaign: JENDRALBOT (6 products)
Affiliate Links: All active
```

**Gotchas:**
- Manual upload required to platforms (no automation yet)
- Tracking must be manual (check dashboard every 2-3 hours)
- URL: https://lynk.id/jendralbot

**Common Operations:**
```bash
# Check daily
1. Visit https://lynk.id/jendralbot
2. Note views, clicks, conversions
3. Calculate revenue generated
```

**Campaign Details:**
- 6 products (1 FREE, 5 paid IDR 49K-89K)
- 54 posts ready across TikTok/IG/YouTube
- Expected time to first revenue: 24-48 hours after upload

---

## 🧠 Vector Database (vector_db_startup.py)

**Status:** ✅ Working - Multiple engines active

**Configuration:**
```python
Auto-load via: /home/openclaw/.openclaw/workspace/vector_db_startup.py

Available Tools:
- vector_search(query, top_k=5)  # Semantic search
- vector_index(content, title, source)  # Index documents
- vector_chunk(text, max_tokens=500)  # Smart chunking
- vector_detect_language(text)  # Auto ID/EN detection
- vector_status()  # Check status
```

**Engines:**
- ZVec: Fast, English only
- PageIndex: Page-based indexing
- Ruvector: Russian/Indonesian

**Location:**
- Storage: ~/.openclaw/vector-cache/
- Size: ~2MB total

**Gotchas:**
- PageIndex/Ruvector: 'persist()' method not supported (API incompatibility)
- Workaround: Skip persist step or use different method

---

## 💰 Cashflow Tracking (cashflow_tracker_template.md)

**Status:** Template created, NOT implemented

**Configuration:**
```
Template: /home/openclaw/.openclaw/workspace/cashflow_tracker_template.md
Required Data: Bank balances, burn rate, expenses
```

**Gotchas:**
- CRITICAL: Bank balance check NEVER done in 33+ hours
- Must be FIRST priority in crisis mode
- Manual tracking required (scripts/cashflow_monitor.py not created)

**Common Operations:**
```markdown
# Daily entry format:
Date: YYYY-MM-DD
Cash Balance Start: IDR ________
Revenue Today: Trading IDR ____, Marketing IDR ____
Expenses Today: IDR ________
Cash Balance End: IDR ________
```

---

## 🚨 Revenue Gap Detection (revenue_gap_detector.py)

**Status:** ✅ Operational - Crisis mode active

**Configuration:**
```
Script: scripts/revenue_gap_detector.py
Config: config/revenue_gap_config.json
Log: logs/revenue_gaps.log
Schedule: Every 2 hours via cron
```

**Alert Tiers:**
- WARNING: Gap > 4 hours (⚠️)
- CRITICAL: Gap > 8 hours (🚨)
- EMERGENCY: Gap > 12 hours (🆘)

**Gotchas:**
- PostBridge API requires localhost:8080 (may not be running)
- Trading logs must exist at configured path
- Uses conservative 12-hour fallback if no activity detected
- Exit codes for monitoring: 0=OK, 1=WARNING, 2=CRITICAL/EMERGENCY, 3=Error

**Common Operations:**
```bash
# Manual run
cd /home/openclaw/.openclaw/workspace
python3 scripts/revenue_gap_detector.py

# Setup cron (auto-configured via setup script)
./scripts/setup_revenue_gap_detector.sh

# View logs
tail -f logs/revenue_gaps.log
tail -f logs/revenue_gaps_cron.log
```

**Data Sources:**
1. PostBridge API - Social media posts (TikTok/IG/YouTube)
2. Trading logs - XAUUSD trade executions
3. Cashflow files - Manual sales recorded
4. LYNK dashboard - Affiliate conversions (manual check)

**Integration Notes:**
- Alerts automatically saved to daily memory: memory/YYYY-MM-DD.md
- JSON logs preserved in: logs/revenue_gaps.log
- Cron logs at: logs/revenue_gaps_cron.log
- Exit codes trigger monitoring/alerting systems

**Documentation:** REVENUE_GAP_DETECTOR.md (comprehensive guide)

---

## 🚨 Revenue Gap Detection - STANDALONE (revenue_gap_detector_standalone.py) ✅ NEW

**Status:** ✅ Created and tested - Works WITHOUT PostBridge API

**Why Created:**
- Original `revenue_gap_detector.py` depends on PostBridge API (localhost:8080)
- When PostBridge is DOWN (HTTP 500), monitoring system also BREAKS
- Crisis mode: MUST have monitoring even when infrastructure is broken

**Configuration:**
```
Script: scripts/revenue_gap_detector_standalone.py
Config: Built into script (no external config file)
Log: logs/revenue_gaps.log (same as original)
Dependencies: NONE (pure Python, no APIs)
```

**Alert Tiers:**
- WARNING: Gap > 4 hours (⚠️)
- CRITICAL: Gap > 8 hours (🚨)
- EMERGENCY: Gap > 12 hours (🆘)

**Data Sources (Local Files Only):**
1. Trading logs: `.vilona/knowledge/trading/trading_log.json`
2. Cashflow files: `cashflow/*.md` (glob pattern)
3. Memory files: `memory/YYYY-MM-DD.md` (recent updates)
4. Manual tracking: `memory/revenue_tracking.md` (if exists)

**Key Features:**
- ✅ Works without PostBridge API
- ✅ Uses file modification times and content parsing
- ✅ Same exit codes (0=OK, 1=WARNING, 2=CRITICAL/EMERGENCY)
- ✅ Same log format (compatible with original)
- ✅ Falls back to 24 hours if no activity found

**Common Operations:**
```bash
# Manual run
cd ~/.openclaw/.openclaw/workspace
python3 scripts/revenue_gap_detector_standalone.py

# Expected output:
# Gap: 24.0 hours | Source: no_activity
# Level: EMERGENCY
# Exit code: 2 (CRITICAL)

# Add to cron (replaces or supplements original):
# crontab -e
# 0 */2 * * * cd ~/.openclaw/workspace && python3 scripts/revenue_gap_detector_standalone.py >> logs/revenue_gaps_cron.log 2>&1
```

**Comparison vs Original:**

| Feature | Original | Standalone |
|---------|----------|------------|
| Dependency | PostBridge API | None (local files) |
| Works when PostBridge down? | ❌ NO | ✅ YES |
| Accuracy for social posts | High (API data) | Medium (file timestamps) |
| Accuracy for trading | High (log parsing) | High (log parsing) |
| Reliability in crisis | Low (single point failure) | High (infrastructure-independent) |

**Recommendation for Crisis Mode:**
- Use standalone detector as PRIMARY (infrastructure-independent)
- Original detector as SECONDARY (more accurate when PostBridge up)
- Run both via cron — whichever works provides data

**Documentation:** Integrated into REVENUE_GAP_DETECTOR.md

---

## 📈 Sunday Trading Automation (sunday_candle_tracker.py, sunday_decision_generator.py) ✅ NEW

**Status:** ✅ Created and tested - Protocol C execution automated

**Purpose:**
Automate Sunday Protocol C execution (XAUUSD 7-candle breakout strategy) without requiring broker connection

**Components:**

### 1. Candle Tracker (`scripts/sunday_candle_tracker.py`)
- Tracks 15-minute candles from 07:00-14:00 UTC+7
- Queries public price APIs (currently unreliable)
- Auto-calculates range at 14:50
- Generates entry decision at 15:00
- **Note:** Live API access variable - manual input method preferred

### 2. Decision Generator (`scripts/sunday_decision_generator.py`)
- Takes manual candle data as input
- Auto-calculates 7-candle range
- Applies decision matrix (< 5 pips = NO ENTRY, >= 5 pips = ENTRY)
- Generates formatted decision report
- **Advantage:** Works reliably without APIs, just math

### 3. Decision Template (`temp/sunday-decision-template-2026-03-08.md`)
- Ready-to-fill worksheet
- Clear input fields for 7 highs and 7 lows
- Includes decision matrix reference
- Execution checklist included

**Common Operations:**

```bash
# At 14:50 UTC+7, use decision generator:
cd ~/.openclaw/workspace
python3 scripts/sunday_decision_generator.py
# Enter 7 highs and 7 lows when prompted
# Decision automatically generated

# Or use the manual template:
nano temp/sunday-decision-template-2026-03-08.md
# Fill in values, then run generator

# View final decision:
cat temp/sunday-decision-2026-03-08-final.md
```

**Decision Matrix:**

| Range (pips) | Qualification | Action |
|--------------|---------------|--------|
| < 5 pips | ❌ Too small | NO ENTRY |
| >= 5 pips | ✅ Qualified | ENTRY READY |

**Test Result:**
- Input: 7 candles (sample data)
- Range: 17.00 pips
- Decision: ENTRY QUALIFIED ✅
- Report generated successfully

**Integration Notes:**
- Works WITHOUT broker connection (documentation-only mode)
- Complements existing worksheet (`temp/sunday-trading-prep-2026-03-08.md`)
- Execution time: 2-3 minutes to enter data and get decision
- Output: Comprehensive decision report saved to temp/

**Documentation:** Weekend Breakthrough Protocol (`weekend_breakthrough_protocol.md`)

---

## ⏰ Weekend Protocol (weekend_breakthrough_protocol.md)

**Status:** ✅ Created - Ready to execute

**Configuration:**
```
Protocol: /home/openclaw/.openclaw/workspace/weekend_breakthrough_protocol.md
Timeline: Saturday March 7 09:00 - Sunday March 8 23:00
Total Hours: 6.5 hours Saturday execution
```

**Protocols:**
- Protocol A: Emergency cashflow (Saturday 09:00-10:00, 1 hour)
- Protocol B: Weekend marketing push (Saturday 10:30-15:30, 5 hours)
- Protocol C: Sunday trading prep (Sunday 07:00-15:00)
- Protocol D: Monday morning prep (March 10)

**Gotchas:**
- Saturday 09:00-09:15 bank check is NON-NEGOTIABLE
- Upload 162 posts (TikTok 54, IG 54, YouTube 54) by Saturday evening
- LYNK monitoring every 3 hours throughout weekend

---

## 📝 Documentation Updates

**Files Updated Last Session:**
- MEMORY.md - Added crisis context, March 6 pattern recognition
- notes/open-loops.md - Documented 3 critical emergency loops
- scripts/trading_monitor.py - Template created
- cashflow_tracker_template.md - Template created
- weekend_breakthrough_protocol.md - Weekend execution plan created

---

## Writing Preferences

- Crisis mode: Direct, urgent, NO fluff
- Metrics: Always quantify opportunities (IDR 0 vs potential)
- Decisions: Document confidence levels (1-10)
- Documentation: Comprehensive but searchable (headers, sections)

---

## What Goes Here

- Tool configurations and settings
- Credential locations (not the credentials themselves!)
- Gotchas and workarounds discovered
- Common commands and patterns
- Integration notes

## Why Separate?

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

---

*Last updated: 2026-03-07 02:50*
*Review periodicallly for new tool configurations*
