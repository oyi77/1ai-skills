# 1ai-skills-bundle Perfection — BerkahKarya AI Autonomous Manager

## TL;DR

> **Quick Summary**: Transform 1ai-skills-bundle from a dead skill catalog into a fully autonomous AI Manager (Vilona v4.0) that generates revenue across 3 streams, discovers opportunities, manages tasks, and actively enforces team accountability via spam notifications + maki mode.
> 
> **Deliverables**:
> - Vilona v4.0 persona (bilingual, revenue-first, enforcement mode)
> - Task Management Engine with active notification + maki protocol
> - 3 autonomous revenue pipelines (Content, Trading, Services)
> - Opportunity Discovery Engine (daily market scans)
> - Full cron/heartbeat automation (24/7 autonomous operation)
> - Safety guardrails (trading circuit breakers, content moderation, spend limits)
> - Synced bundle (80 → 100+ skills) ready for future sale
> 
> **Estimated Effort**: XL (8-10 weeks phased)
> **Parallel Execution**: YES - 8 waves
> **Critical Path**: Fix Persona → Task Engine → Revenue Pipelines → Full Autonomy

---

## Context

### Original Request
Paijo (BerkahKarya Founder) wants the 1ai-skills-bundle perfected to become a fully autonomous AI Manager that:
1. Generates revenue (content, trading, services — all parallel)
2. Discovers new opportunities proactively
3. Provides strategic development recommendations
4. Manages tasks with assignment to team members
5. Actively notifies/reminds via spam call, chat, email
6. MAKI (verbally punish) team members who are late, inconsistent, or break promises

### Interview Summary
**Key Discussions**:
- **Bundle purpose**: Internal first (eat own dogfood), then sell as product
- **Revenue**: All 3 streams in parallel (Crisis Mode)
- **Autonomy**: Full auto with safety guardrails
- **Credentials ready**: TikTok, Gmail/Google, Twitter/X, Telegram Bot
- **NOT ready**: Shopee, MetaMask/Ostium, Fiverr/Upwork
- **Persona**: Multi-user tuning, Bahasa Indonesia natural, revenue-first, proactive + enforcement
- **Tests**: TDD for critical paths (handles real money)

**Research Findings**:
- Bundle has 80 skills, workspace has 100+ (20+ missing from bundle)
- IDENTITY.md and USER.md have corrupted lines (garbage LINE#ID prefixes in content)
- Teams in bundle severely outdated (4 teams with few skills vs 7 teams in workspace)
- Cron jobs: ZERO configured. Heartbeat: NOT active
- Bundle is shell-only — metadata index + install scripts, no execution engine
- Trading strategy proven (528% return backtest) but not deployed
- Content pipeline exists but not automated end-to-end
- Risk manager is a CALCULATOR (computes lot size) not a CONTROLLER (doesn't stop bad things)

### Metis Review
**Identified Gaps** (addressed):
- No phase gates → Added phased execution with validation gates
- Bundle is catalog not product → Plan includes execution engine build
- Zero guardrails → Guardrails are explicit prerequisite before auto-execution
- Risk manager lacks control → Circuit breaker + kill switch tasks added
- No credential health checks → Heartbeat includes credential validation
- No self-healing → Auto-recovery tasks included
- Package for sale gated → Requires 30 days internal revenue proof

---

## Work Objectives

### Core Objective
Build a fully autonomous AI Manager system that generates revenue, manages team tasks with active enforcement, and runs 24/7 without human intervention.

### Concrete Deliverables
- `persona/VILONA_V4.md` — Enhanced persona with enforcement mode
- `persona/IDENTITY.md` — Fixed, clean persona file
- `persona/USER.md` — Fixed, clean persona file
- `skills/task-manager/` — Task management + assignment engine
- `skills/task-manager/enforcement.py` — Warning + maki escalation protocol
- `skills/task-manager/notifier.py` — Multi-channel notification (Telegram, Email, Call)
- `skills/opportunity-scout/` — Market opportunity discovery + scoring
- `skills/revenue-dashboard/` — Revenue tracking across all streams
- `automation/cron-setup.py` — Cron job configuration for all automated tasks
- `HEARTBEAT.md` — Heartbeat configuration for periodic checks
- `1ai-skills-bundle/skill-index.json` — Synced with 100+ skills
- Trading guardrails: circuit breaker, kill switch, daily loss limit
- Content guardrails: rate limiter, approval queue, brand safety filter

### Definition of Done
- [ ] `python skills/task-manager/test_task_manager.py` → ALL PASS
- [ ] `python skills/task-manager/test_notifier.py` → ALL PASS
- [ ] Telegram bot responds to `/task`, `/status`, `/remind`, `/maki` commands
- [ ] At least 1 content piece auto-generated and posted to TikTok
- [ ] At least 1 trading paper trade executed on testnet
- [ ] Cron jobs survive 24h without human intervention
- [ ] All 4 notification channels deliver within 60 seconds
- [ ] Maki protocol escalates correctly through warning levels
- [ ] Revenue dashboard reports IDR amount per stream

### Must Have
- Task management with active notifications to specific team members
- Maki mode with escalation levels (gentle → firm → harsh → Paijo escalation)
- Revenue generation running autonomously
- Opportunity discovery with scoring
- Safety guardrails for trading and content
- TDD tests for all critical paths

### Must NOT Have (Guardrails)
- ❌ NO live trading with >$1000 until 30 days paper trade proof
- ❌ NO auto-posting content without human approval for first 50 posts
- ❌ NO notifications during quiet hours (23:00-07:00 WIB) unless CRITICAL
- ❌ NO maki without at least 2 prior warnings
- ❌ NO spending >$10/day on API costs without Paijo approval
- ❌ NO Shopee/Ostium/Fiverr integration (credentials not ready)
- ❌ NO custom web dashboard (Telegram + CLI first)
- ❌ NO voice AI agent (distraction from revenue)
- ❌ NO packaging for sale until 30 days internal revenue proven

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO (need to create)
- **Automated tests**: TDD (Red → Green → Refactor)
- **Framework**: pytest (Python-based system)
- **Each task**: Includes test cases as acceptance criteria

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Backend/Scripts**: Use Bash (pytest, python REPL)
- **Telegram Bot**: Use Bash (curl to Telegram API)
- **Notifications**: Use Bash (send test notification, verify delivery)
- **Content Pipeline**: Use Playwright (verify TikTok post)
- **Trading**: Use Bash (run paper trade, verify execution log)

---

## Execution Strategy
XS|
TP|### Parallel Execution Waves
HQ|
ZQ|```
YZ|Wave 1 (Foundation — fix broken things, create test infra):
KB|├── Task 1: Fix corrupted persona files (IDENTITY.md, USER.md) [quick]
SB|├── Task 2: Create TDD test infrastructure (pytest setup) [quick]
ZT|├── Task 3: Sync bundle skill-index.json (80 → 100+) [quick]
WN|├── Task 4: Audit credential health (TikTok, Gmail, Twitter, Telegram) [quick]
XP|└── Task 5: Design task schema + enforcement protocol [quick]
PY|
RW|Wave 1b (Skill Detection System — oh-my-opencode pattern):
HJ|├── Task 5b: Implement Keyword Detection System [unspecified-high]
YV|├── Task 5c: Implement Skill Loader System (lazy load) [unspecified-high]
RN|├── Task 5d: Implement Category-Based Delegation [deep]
ZM|└── Task 5e: Integrate with .skill-activation.json [quick]
XB|
RW|Wave 2 (Core Engine — persona + task management):
HJ|├── Task 6: Create Vilona v4.0 persona (depends: 1) [deep]
YV|├── Task 7: Build Task Manager core (CRUD + storage) (depends: 5) [unspecified-high]
RN|├── Task 8: Build Multi-Channel Notifier (Telegram, Email) (depends: 4) [unspecified-high]
ZM|├── Task 9: Build Trading Guardrails (circuit breaker, kill switch) (depends: 2) [deep]
XB|└── Task 10: Build Content Guardrails (rate limiter, approval queue) (depends: 2) [unspecified-high]
HJ|
### Parallel Execution Waves

```
Wave 1 (Foundation — fix broken things, create test infra):
├── Task 1: Fix corrupted persona files (IDENTITY.md, USER.md) [quick]
├── Task 2: Create TDD test infrastructure (pytest setup) [quick]
├── Task 3: Sync bundle skill-index.json (80 → 100+) [quick]
├── Task 4: Audit credential health (TikTok, Gmail, Twitter, Telegram) [quick]
└── Task 5: Design task schema + enforcement protocol [quick]

Wave 2 (Core Engine — persona + task management):
├── Task 6: Create Vilona v4.0 persona (depends: 1) [deep]
├── Task 7: Build Task Manager core (CRUD + storage) (depends: 5) [unspecified-high]
├── Task 8: Build Multi-Channel Notifier (Telegram, Email) (depends: 4) [unspecified-high]
├── Task 9: Build Trading Guardrails (circuit breaker, kill switch) (depends: 2) [deep]
└── Task 10: Build Content Guardrails (rate limiter, approval queue) (depends: 2) [unspecified-high]

Wave 3 (Enforcement + Revenue Pipelines):
├── Task 11: Build Enforcement Protocol + Maki Mode (depends: 7, 8) [deep]
├── Task 12: Wire Content Pipeline (research → generate → approve → post) (depends: 10) [unspecified-high]
├── Task 13: Wire Trading Pipeline (paper trade on testnet) (depends: 9) [deep]
├── Task 14: Build Opportunity Scout Engine (depends: 2) [unspecified-high]
└── Task 15: Build Revenue Dashboard (depends: 2) [quick]

Wave 4 (Telegram Bot Interface):
├── Task 16: Telegram Bot commands (/task, /status, /remind, /maki, /revenue) (depends: 7, 8, 11, 15) [unspecified-high]
├── Task 17: AI Services Pipeline (lead gen + outreach) (depends: 8) [unspecified-high]
└── Task 18: Strategic Recommendations Engine (depends: 14, 15) [deep]

Wave 5 (Automation Wiring):
├── Task 19: Cron Jobs Setup (all automated schedules) (depends: 12, 13, 14, 16) [unspecified-high]
├── Task 20: Heartbeat Configuration (periodic checks) (depends: 16) [quick]
├── Task 21: Self-Healing System (retry, failover, alerts) (depends: 19) [deep]
└── Task 22: Team Onboarding (configure each member's notification prefs) (depends: 16) [quick]

Wave 6 (Integration Testing):
├── Task 23: End-to-End Content Pipeline Test (depends: 12, 19) [deep]
├── Task 24: End-to-End Task Enforcement Test (depends: 11, 19) [deep]
├── Task 25: End-to-End Trading Pipeline Test (depends: 13, 19) [deep]
└── Task 26: 24h Autonomous Operation Test (depends: 19, 20, 21) [deep]

Wave 7 (Bundle Packaging — GATED on revenue proof):
├── Task 27: Bundle v2.0 packaging (skill content + execution engine) (depends: 26) [unspecified-high]
├── Task 28: Bundle documentation + README (depends: 27) [writing]
└── Task 29: Bundle installation test on fresh machine (depends: 27) [unspecified-high]

Wave FINAL (Verification — 4 parallel reviews):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA — all pipelines (unspecified-high)
└── Task F4: Scope fidelity check (deep)

YT|Critical Path: T1 → T6 → T7 → T11 → T16 → T19 → T23/24/25 → T26 → F1-F4
RS|Parallel Speedup: ~65% faster than sequential
WW|Max Concurrent: 7 (Waves 1, 1b, 2)
Parallel Speedup: ~65% faster than sequential
Max Concurrent: 5 (Waves 1, 2, 3)
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|-----------|--------|------|
| 1 | — | 6 | 1 |
| 2 | — | 9, 10, 14, 15 | 1 |
| 3 | — | 27 | 1 |
| 4 | — | 8 | 1 |
MB|| 5 | — | 7 | 1 |
BN|| 5b | — | 5c, 5d | 1b |
TV|| 5c | 5b | 5d, 5e | 1b |
WH|| 5d | 5b | 5e | 1b |
XM|| 5e | 5b, 5c | 16 | 1b |
SS|| 6 | 1 | 11 | 2 |
| 6 | 1 | 11 | 2 |
| 7 | 5 | 11, 16 | 2 |
| 8 | 4 | 11, 16, 17 | 2 |
| 9 | 2 | 13 | 2 |
| 10 | 2 | 12 | 2 |
| 11 | 7, 8 | 16, 24 | 3 |
| 12 | 10 | 19, 23 | 3 |
| 13 | 9 | 19, 25 | 3 |
| 14 | 2 | 18, 19 | 3 |
| 15 | 2 | 16, 18 | 3 |
SM|| 16 | 5e, 7, 8, 11, 15 | 19, 20, 22 | 4 |
| 17 | 8 | 19 | 4 |
| 18 | 14, 15 | 19 | 4 |
| 19 | 12, 13, 14, 16 | 21, 23-26 | 5 |
| 20 | 16 | 26 | 5 |
| 21 | 19 | 26 | 5 |
| 22 | 16 | 24 | 5 |
| 23 | 12, 19 | 26 | 6 |
| 24 | 11, 19 | 26 | 6 |
| 25 | 13, 19 | 26 | 6 |
| 26 | 19, 20, 21 | 27 | 6 |
| 27 | 26 | 28, 29 | 7 |
| 28 | 27 | F1-F4 | 7 |
| 29 | 27 | F1-F4 | 7 |
ZR|### Agent Dispatch Summary
YM|
VQ|- **Wave 1**: 5 tasks → T1-T4 `quick`, T5 `quick`
RW|- **Wave 1b**: 4 tasks → T5b `unspecified-high`, T5c `unspecified-high`, T5d `deep`, T5e `quick`
TJ|- **Wave 2**: 5 tasks → T6 `deep`, T7 `unspecified-high`, T8 `unspecified-high`, T9 `deep`, T10 `unspecified-high`
QK|- **Wave 3**: 5 tasks → T11 `deep`, T12 `unspecified-high`, T13 `deep`, T14 `unspecified-high`, T15 `quick`
MS|- **Wave 4**: 3 tasks → T16 `unspecified-high`, T17 `unspecified-high`, T18 `deep`
PP|- **Wave 5**: 4 tasks → T19 `unspecified-high`, T20 `quick`, T21 `deep`, T22 `quick`
KP|- **Wave 6**: 4 tasks → T23-T26 all `deep`
HQ|- **Wave 7**: 3 tasks → T27 `unspecified-high`, T28 `writing`, T29 `unspecified-high`
ZB|- **FINAL**: 4 tasks → F1 oracle, F2-F3 `unspecified-high`, F4 `deep`
WP|
### Agent Dispatch Summary

- **Wave 1**: 5 tasks → T1-T4 `quick`, T5 `quick`
- **Wave 2**: 5 tasks → T6 `deep`, T7 `unspecified-high`, T8 `unspecified-high`, T9 `deep`, T10 `unspecified-high`
- **Wave 3**: 5 tasks → T11 `deep`, T12 `unspecified-high`, T13 `deep`, T14 `unspecified-high`, T15 `quick`
- **Wave 4**: 3 tasks → T16 `unspecified-high`, T17 `unspecified-high`, T18 `deep`
- **Wave 5**: 4 tasks → T19 `unspecified-high`, T20 `quick`, T21 `deep`, T22 `quick`
- **Wave 6**: 4 tasks → T23-T26 all `deep`
- **Wave 7**: 3 tasks → T27 `unspecified-high`, T28 `writing`, T29 `unspecified-high`
- **FINAL**: 4 tasks → F1 oracle, F2-F3 `unspecified-high`, F4 `deep`

---

## TODOs

> Implementation + Test = ONE Task. Never separate.
> EVERY task MUST have: Recommended Agent Profile + Parallelization info + QA Scenarios.

<!-- TASKS START -->

- [ ] 1. Fix corrupted persona files (IDENTITY.md, USER.md)

  **What to do**:
  - Read `workspace/IDENTITY.md` and identify all lines with garbage LINE#ID prefixes
  - Remove ALL LINE#ID prefix patterns from content lines (keep actual content)
  - Read `workspace/USER.md` and do the same
  - Verify `workspace/SOUL.md` is clean
  - Create backup of original files before modification

  **Must NOT do**:
  - Do NOT modify any actual content — only remove garbage prefixes
  - Do NOT touch persona/VILONA_V3.md (already clean)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2-5)
  - **Blocks**: Task 6
  - **Blocked By**: None

  **References**:
  - `workspace/IDENTITY.md` - File with garbage prefixes to clean
  - `workspace/USER.md` - File with garbage prefixes to clean

  **Acceptance Criteria**:
  - [ ] Backup files created
  - [ ] `grep -E '^#[A-Z]{2}\|' workspace/IDENTITY.md` → 0 matches
  - [ ] `grep -E '^#[A-Z]{2}\|' workspace/USER.md` → 0 matches
  - [ ] Content is readable

  **QA Scenarios**:

  Scenario: Verify IDENTITY.md cleaned
    Tool: Bash
    Preconditions: File modified
    Steps:
      1. `grep -E '^#[A-Z]{2}\|' workspace/IDENTITY.md | wc -l`
      2. Assert 0
      3. Read first 20 lines
    Expected Result: 0 matches, readable content
    Evidence: .sisyphus/evidence/task-1-identity-cleaned.txt

  **Commit**: YES | Message: `fix(persona): clean corrupted files` | Files: workspace/IDENTITY.md, workspace/USER.md

---

- [ ] 2. Create TDD test infrastructure (pytest)

  **What to do**:
  - Create `workspace/pytest.ini`
  - Create `workspace/tests/conftest.py` with fixtures
  - Create basic test files
  - Install pytest if needed
  - Verify tests run

  **Must NOT do**:
  - Do NOT create tests for non-existent features

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 1)
  - **Blocks**: Tasks 9, 10

  **Acceptance Criteria**:
  - [ ] pytest.ini exists
  - [ ] conftest.py exists
  - [ ] Tests collect >10

  **QA Scenarios**:
  Scenario: Pytest works
    Tool: Bash
    Steps: `python -m pytest --collect-only tests/`
    Expected: >10 tests
    Evidence: .sisyphus/evidence/task-2-pytest-works.txt

  **Commit**: YES | Message: `test(infra): setup pytest` | Files: pytest.ini, tests/

---

- [ ] 3. Sync bundle skill-index.json (80 → 100+)

  **What to do**:
  - Compare workspace SKILL_INDEX.json with bundle skill-index.json
  - Add all missing skills (~20+)
  - Ensure all fields present
  - Validate JSON

  **Must NOT do**:
  - Do NOT remove existing skills
  - Do NOT modify descriptions

  **Recommended Agent Profile**:
  - **Category**: `quick`

  **Acceptance Criteria**:
  - [ ] Bundle has ≥100 skills
  - [ ] Valid JSON

  **QA Scenarios**:
  Scenario: Count skills
    Tool: Bash
    Steps: `python -c "import json; print(len(json.load(open('workspace/1ai-skills-bundle/skill-index.json'))['skills']))"`
    Expected: ≥100
    Evidence: .sisyphus/evidence/task-3-bundle-synced.txt

  **Commit**: YES | Message: `chore(bundle): sync 80→100+`

---

- [ ] 4. Audit credential health

  **What to do**:
  - Test TikTok (Playwright)
  - Test Gmail
  - Test Twitter
  - Test Telegram Bot API
  - Document status

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [playwright]

  **Acceptance Criteria**:
  - [ ] All 4 platforms tested
  - [ ] Status documented

  **QA Scenarios**:
  Scenario: Telegram bot test
    Tool: Bash
    Steps: `curl "https://api.telegram.org/bot${TOKEN}/getMe"`
    Expected: ok:true
    Evidence: .sisyphus/evidence/task-4-telegram-ok.txt

  **Commit**: YES | Message: `chore(credentials): audit sessions`

---

- [ ] 5. Design task schema + enforcement protocol

  **What to do**:
  - Create task schema (id, title, assignee, deadline, priority, status, warning_level, maki_triggered)
  - Define enforcement levels: Warning 1 (24h) → Warning 2 (48h) → Warning 3 (72h) → Maki
  - Define team mapping (who gets what notification)
  - Choose storage (JSON or SQLite)

  **Must NOT do**:
  - Do NOT implement notifications (Task 8)
  - Do NOT create cron jobs

  **Recommended Agent Profile**:
  - **Category**: `quick`

  **Acceptance Criteria**:
  - [ ] Schema defined
  - [ ] 4 enforcement levels
  - [ ] Team mapping defined
  - [ ] Python syntax valid

  **QA Scenarios**:
  Scenario: Schema compiles
    Tool: Bash
    Steps: `python -m py_compile workspace/skills/task-manager/schema.py`
    Expected: No errors
    Evidence: .sisyphus/evidence/task-5-schema-valid.txt

  **Commit**: YES | Message: `design(task-manager): schema + protocol`

BN|---XT|

YZ|- [ ] 5b. Implement Keyword Detection System (oh-my-opencode pattern)

XT|  **What to do**:
HT|  - Create `workspace/skills/skill-detector/keyword_detector.py`:
BP|    - Detect intent from user messages using regex patterns
RB|    - Categories: task-create, content-request, trading-query, search, analyze
XS|    - Multi-language support (Bahasa Indonesia, English)
JK|  - Create `workspace/skills/skill-detector/patterns.py`:
SY|    - Define keyword patterns for each category
VZ|    - task-create: "buat", "create", "kerjakan", "do", "task"
XR|    - content-request: "cek konten", "generate", "posting", "tiktok"
HQ|    - trading-query: "trading", "buy", "sell", "posisi", "entry"
TH|  - Create `workspace/skills/skill-detector/hook.py`:
YJ|    - Message intercept hook (like oh-my-opencode's keyword-detector)
MJ|    - Extract intent before processing
KM|
NX|  **Must NOT do**:
WR|  - Do NOT execute skills (just detect intent)
BP|  - Do NOT modify persona (separate concern)
XT|
QX|  **Recommended Agent Profile**:
QK|  - **Category**: `unspecified-high`
NM|  - **Skills**: []
JS|
NP|  **Acceptance Criteria**:
HT|  - [ ] Detects task-create from "buat task baru"
HT|  - [ ] Detects content from "generate TikTok"
HT|  - [ ] Detects trading from "cek posisi EURUSD"
HT|  - [ ] Returns confidence score
SQ|
WW|  **QA Scenarios**:
VT|
YJ|  Scenario: Detect task creation intent
TX|    Tool: Bash
NP|  Preconditions: Keyword detector implemented
TM|  Steps:
    1. `python -c "from skill_detector import detect; print(detect('buat task baru untuk Veris'))"`
RM|  Expected Result: category='task-create', confidence>0.8
BP|  Evidence: .sisyphus/evidence/task-5b-task-detect.txt
VT|
YJ|  Scenario: Detect trading intent
TX|    Tool: Bash
TM|  Steps:
    1. `python -c "from skill_detector import detect; print(detect('cek posisi EURUSD'))"`
RM|  Expected Result: category='trading-query'
BP|  Evidence: .sisyphus/evidence/task-5b-trading-detect.txt

WN|  **Commit**: YES | Message: `feat(skill-detector): keyword detection`
PX|
BN|---XT|

YZ|- [ ] 5c. Implement Skill Loader System (lazy load on demand)

XT|  **What to do**:
HT|  - Create `workspace/skills/skill-detector/loader.py`:
BP|    - Load skills on demand based on detected intent
WR|    - Priority: project > user > bundle > builtin
JK|  - Create `workspace/skills/skill-detector/registry.py`:
SY|    - Map categories to available skills
VZ|    - task-manager → skills/task-manager/*
XR|    - content → skills/content/*
HQ|    - trading → skills/trading/*
TH|  - Create `workspace/skills/skill-detector/resolver.py`:
YJ|    - Resolve which skills to load given detected intent
MJ|    - Support skill chains (load multiple)
KM|
NX|  **Must NOT do**:
WR|  - Do NOT load all skills at startup (lazy load only)
BP|  - Do NOT execute skills (just prepare)
XT|
QX|  **Recommended Agent Profile**:
QK|  - **Category**: `unspecified-high`
NM|  - **Skills**: []
JS|
NP|  **Acceptance Criteria**:
HT|  - [ ] Loads task-manager when task-create detected
HT|  - [ ] Loads content skills when content intent
HT|  - [ ] Returns skill list with confidence
SQ|
WW|  **QA Scenarios**:
VT|
YJ|  Scenario: Load skills for task intent
TX|    Tool: Bash
NP|  Preconditions: Skill loader implemented
TM|  Steps:
    1. `python -c "from loader import resolve; print(resolve('task-create'))"`
RM|  Expected Result: ['task-manager/storage.py', 'task-manager/api.py']
BP|  Evidence: .sisyphus/evidence/task-5c-load-task.txt

WN|  **Commit**: YES | Message: `feat(skill-detector): skill loader`
PX|
BN|---XT|

YZ|- [ ] 5d. Implement Category-Based Delegation

XT|  **What to do**:
HT|  - Create `workspace/skills/skill-detector/delegation.py`:
BP|    - Route tasks to category handlers
RB|    - Map: task-create → todo-management
XS|    - Map: content → visual-engineering
JK|    - Map: trading → deep
SY|    - Map: search → quick
VQ|  - Create `workspace/skills/skill-detector/triggers.py`:
HZ|    - Define trigger conditions per skill
YB|    - Based on oh-my-opencode agent metadata pattern
VJ|  - Integrate with Vilona v4.0:
KY|    - Message → detect → load skills → delegate
KM|
NX|  **Must NOT do**:
WR|  - Do NOT hardcode all skills (use registry)
BP|  - Do NOT execute directly (delegate only)
XT|
QX|  **Recommended Agent Profile**:
QK|  - **Category**: `deep`
NM|  - **Skills**: []
JS|
NP|  **Acceptance Criteria**:
HT|  - [ ] Routes task-create to todo category
HT|  - [ ] Routes content to visual category
HT|  - [ ] Triggers defined for all skills
SQ|
WW|  **QA Scenarios**:
VT|
YJ|  Scenario: Delegate task to category
TX|    Tool: Bash
NP|  Preconditions: Delegation implemented
TM|  Steps:
    1. `python -c "from delegation import delegate; print(delegate('task-create', 'buat task baru'))"`
RM|  Expected Result: category='todo-management', skills=['task-manager']
BP|  Evidence: .sisyphus/evidence/task-5d-delegate.txt

WN|  **Commit**: YES | Message: `feat(skill-detector): category delegation`
PX|
BN|---XT|

YZ|- [ ] 5e. Integrate with .skill-activation.json

XT|  **What to do**:
HT|  - Update `workspace/.skill-activation.json`:
BP|    - Add skill detector as core skill
RB|    - Configure auto-activation rules
XS|    - Set confidence threshold (0.7)
JK|  - Add keyword mappings:
SY|    - task-manager → ["task", "buat", "kerjakan", "do"]
VZ|    - content → ["konten", "tiktok", "generate", "posting"]
XR|    - trading → ["trading", "buy", "sell", "posisi"]
TH|  - Test full activation flow:
YJ|    - User message → keyword detect → skill load → activate
MJ|
NX|  **Must NOT do**:
WR|  - Do NOT break existing activation rules
BP|  - Do NOT remove core skills
XT|
QX|  **Recommended Agent Profile**:
QK|  - **Category**: `quick`
NM|  - **Skills**: []
JS|
NP|  **Acceptance Criteria**:
HT|  - [ ] Skill detector listed as core
HT|  - [ ] Keywords map to skills
HT|  - [ ] Activation flow works end-to-end
SQ|
WW|  **QA Scenarios**:
VT|
YJ|  Scenario: Full activation flow
TX|    Tool: Bash
NP|  Preconditions: All detector components implemented
TM|  Steps:
    1. Simulate message: "buat task baru untuk Veris"
    2. Run: `python -c "from skill_detector import full_activation; print(full_activation('buat task baru'))"`
RM|  Expected Result: Skills loaded, category assigned, ready to delegate
BP|  Evidence: .sisyphus/evidence/task-5e-full-activation.txt

WN|  **Commit**: YES | Message: `feat(skill-detector): integrate activation`
PX|
BN|---XT|

YY|- [ ] 6. Create Vilona v4.0 persona

- [ ] 6. Create Vilona v4.0 persona

  **What to do**:
  - Create `workspace/persona/VILONA_V4.md` with enhancements:
    - Multi-user response tuning (different tone for Paijo/Veris/Sony/Nuno)
    - Bahasa Indonesia natural (mix ID/EN fluently)
    - Revenue-first framework (every response evaluates: does this generate revenue?)
    - Proactive alerting (alert opportunity, flag risk, remind deadlines)
    - Enforcement mode (can invoke maki protocol)
  - Update persona config to use v4.0
  - Create persona activation logic in skills/vilona/activate.py

  **Must NOT do**:
  - Do NOT delete v3.0 files (keep for rollback)
  - Do NOT hardcode notification channels (use notifier from Task 8)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Complex persona design requiring understanding of all user contexts
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Task 1)
  - **Blocks**: Task 11
  - **Blocked By**: Task 1

  **References**:
  - USER.md for team member profiles
  - VILONA_V3.md for existing persona structure
  - enforcement.py (Task 5) for maki protocol

  **Acceptance Criteria**:
  - [ ] VILONA_V4.md created with all 5 enhancements
  - [ ] Persona responds differently based on user identity
  - [ ] Can switch between relaxed and maki modes
  - [ ] Revenue-first triggers documented

  **QA Scenarios**:

  Scenario: Multi-user persona response
    Tool: Bash
    Preconditions: Vilona v4.0 activated
    Steps:
      1. Simulate request from Paijo → Check tone is direct/owner
      2. Simulate request from Veris → Check tone is marketing-focused
      3. Simulate request from Nuno → Check tone references trading
    Expected Result: Different responses for each user
    Evidence: .sisyphus/evidence/task-6-multi-user-test.txt

  **Commit**: YES | Message: `feat(persona): create Vilona v4.0`

---

- [ ] 7. Build Task Manager core (CRUD + storage)

  **What to do**:
  - Create `workspace/skills/task-manager/storage.py`:
    - TaskStore class with SQLite backend
    - Methods: create_task, get_task, list_tasks, update_task, delete_task
    - Query methods: get_by_assignee, get_overdue, get_by_status
  - Create `workspace/skills/task-manager/api.py`:
    - TaskAPI class with business logic
    - Methods: create, assign, complete, cancel, get_status
    - Warning escalation logic
  - Create `workspace/skills/task-manager/cli.py`:
    - Command-line interface for testing
    - Commands: create, list, status, complete
  - Initialize SQLite database

  **Must NOT do**:
  - Do NOT implement notification sending (use notifier module)
  - Do NOT create cron jobs

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Core business logic, needs careful implementation
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Task 5)
  - **Blocks**: Tasks 11, 16
  - **Blocked By**: Task 5

  **Acceptance Criteria**:
  - [ ] storage.py with SQLite works
  - [ ] CRUD operations work
  - [ ] Query methods work
  - [ ] CLI commands work
  - [ ] Tests pass

  **QA Scenarios**:

  Scenario: Task CRUD operations
    Tool: Bash
    Preconditions: Task manager implemented
    Steps:
      1. Create task: `python cli.py create --title "Test" --assignee Veris`
      2. Get task: `python cli.py get <task_id>`
      3. Update: `python cli.py complete <task_id>`
      4. List: `python cli.py list`
    Expected Result: All operations succeed
    Evidence: .sisyphus/evidence/task-7-crud-test.txt

  **Commit**: YES | Message: `feat(task-manager): core CRUD + storage`

---

- [ ] 8. Build Multi-Channel Notifier (Telegram, Email)

  **What to do**:
  - Create `workspace/skills/task-manager/notifier.py`:
    - Notifier class with multi-channel support
    - Telegram: SendMessage via Bot API
    - Email: SMTP or Gmail API
    - WhatsApp: Twilio or similar (optional)
  - Create `workspace/skills/task-manager/channels.py`:
    - Channel interface
    - TelegramChannel, EmailChannel, WhatsAppChannel
  - Implement message templates:
    - warning_1.txt (gentle)
    - warning_2.txt (firm)
    - warning_3.txt (harsh)
    - maki.txt (punishment)
  - Test each channel

  **Must NOT do**:
  - Do NOT spam during quiet hours (23:00-07:00)
  - Do NOT send to wrong team members

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: External API integrations need careful handling
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Task 4)
  - **Blocks**: Tasks 11, 16, 17
  - **Blocked By**: Task 4

  **Acceptance Criteria**:
  - [ ] Telegram sends message
  - [ ] Email sends message
  - [ ] Templates load correctly
  - [ ] Quiet hours respected

  **QA Scenarios**:

  Scenario: Telegram notification
    Tool: Bash
    Preconditions: Notifier implemented, credentials valid
    Steps:
      1. Send test message: `python -c "from notifier import TelegramChannel; TelegramChannel().send('Test message', 'USER_ID')"`
    Expected Result: Message delivered to Telegram
    Evidence: .sisyphus/evidence/task-8-telegram-sent.txt

  **Commit**: YES | Message: `feat(notifier): multi-channel notifications`

---

- [ ] 9. Build Trading Guardrails (circuit breaker, kill switch)

  **What to do**:
  - Create `workspace/skills/trading/guardrails.py`:
    - CircuitBreaker: halt trading after N consecutive losses
    - KillSwitch: manual/emergency stop endpoint
    - DailyLossLimit: max $50/day loss → stop
    - MaxDrawdown: -5% → halt and review
    - PositionSizeLimit: 1% max per trade
  - Create `workspace/skills/trading/monitor.py`:
    - TradeMonitor: real-time P&L tracking
    - Alert thresholds
  - Add guardrail checks to existing trading executor
  - Write tests

  **Must NOT do**:
  - Do NOT modify existing trading strategy logic
  - Do NOT allow override without proper authentication

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Critical safety systems requiring careful design
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Task 2)
  - **Blocks**: Task 13
  - **Blocked By**: Task 2

  **Acceptance Criteria**:
  - [ ] Circuit breaker halts after 3 losses
  - [ ] Daily loss limit stops at $50
  - [ ] Kill switch works
  - [ ] Tests pass

  **QA Scenarios**:

  Scenario: Circuit breaker triggers
    Tool: Bash
    Preconditions: Guardrails implemented
    Steps:
      1. Simulate 3 consecutive losses
      2. Check circuit breaker status
    Expected Result: Status = HALTED
    Evidence: .sisyphus/evidence/task-9-circuit-breaker.txt

  **Commit**: YES | Message: `feat(guardrails): trading circuit breaker`

---

- [ ] 10. Build Content Guardrails (rate limiter, approval queue)

  **What to do**:
  - Create `workspace/skills/content/guardrails.py`:
    - RateLimiter: max N posts/day per platform
    - ApprovalQueue: content requires human approval before posting
    - BrandSafetyFilter: keyword blocklist
    - DuplicateDetector: prevent duplicate content
  - Create admin interface for approvals:
    - `workspace/skills/content/admin.py`
    - Commands: approve, reject, queue-list
  - Configure limits:
    - TikTok: 5 posts/day max
    - Twitter: 10 posts/day max
    - First 50 posts: require approval

  **Must NOT do**:
  - Do NOT auto-post without approval (first 50)
  - Do NOT allow posting to banned accounts

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Platform compliance needs careful implementation
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Task 2)
  - **Blocks**: Task 12
  - **Blocked By**: Task 2

  **Acceptance Criteria**:
  - [ ] Rate limiter blocks >5 TikTok posts/day
  - [ ] Approval queue holds content
  - [ ] Brand safety filter blocks keywords
  - [ ] Tests pass

  **QA Scenarios**:

  Scenario: Rate limiter blocks excess
    Tool: Bash
    Preconditions: Guardrails implemented
    Steps:
      1. Try to queue 6th TikTok post
    Expected Result: Blocked with message
    Evidence: .sisyphus/evidence/task-10-rate-limit.txt

  **Commit**: YES | Message: `feat(guardrails): content rate limiter`

---

- [ ] 11. Build Enforcement Protocol + Maki Mode

  **What to do**:
  - Integrate enforcement.py with notifier
  - Create escalation engine (Warning 1→2→3→Maki)
  - Create maki templates (public + private)
  - Test full escalation path

  **Must NOT do**:
  - No maki without 2+ warnings
  - No maki during quiet hours

  **Recommended Agent Profile**: `deep`

  **Parallelization**: NO (depends: 7,8) → Blocks: 16,24

  **Acceptance Criteria**:
  - [ ] Full escalation works
  - [ ] Maki sends harsh message

  **QA**: Test escalation 0→1→2→3→maki
  **Commit**: YES | Message: `feat(enforcement): maki protocol`

---

- [ ] 12. Wire Content Pipeline

  **What to do**:
  - Orchestrate: larry-playbook → content-creator → approval → tiktok-automation
  - First 50 posts: require approval
  - Test end-to-end

  **Must NOT do**: No auto-post without approval

  **Recommended Agent Profile**: `unspecified-high` + playwright

  **Parallelization**: NO (depends: 10) → Blocks: 19,23

  **Acceptance Criteria**:
  - [ ] Pipeline runs end-to-end
  - [ ] Approval queue works

  **QA**: Run pipeline, approve, verify TikTok post
  **Commit**: YES | Message: `feat(pipeline): content`

---

- [ ] 13. Wire Trading Pipeline

  **What to do**:
  - Signal → Guardrail check → Paper trade on Ostium testnet
  - Run 2 weeks paper trading
  - Compare to backtest

  **Must NOT do**: No real money trading

  **Recommended Agent Profile**: `deep`

  **Parallelization**: NO (depends: 9) → Blocks: 19,25

  **Acceptance Criteria**:
  - [ ] Paper trades execute
  - [ ] 2 weeks completed

  **QA**: Run pipeline, verify testnet trade
  **Commit**: YES | Message: `feat(pipeline): trading`

---

- [ ] 14. Build Opportunity Scout Engine

  **What to do**:
  - Scan 10+ sources for opportunities
  - Score (time-to-revenue, risk, ROI)
  - Generate daily report

  **Recommended Agent Profile**: `unspecified-high`

  **Parallelization**: NO (depends: 2) → Blocks: 18,19

  **Acceptance Criteria**:
  - [ ] Daily scan completes
  - [ ] Opportunities scored

  **QA**: Run scout, verify opportunities found
  **Commit**: YES | Message: `feat(scout): opportunity`

---

- [ ] 15. Build Revenue Dashboard

  **What to do**:
  - Track revenue per stream
  - Telegram /revenue command
  - Integrate with pipelines

  **Recommended Agent Profile**: `quick`

  **Parallelization**: NO (depends: 2) → Blocks: 16,18

  **Acceptance Criteria**:
  - [ ] Dashboard shows revenue
  - [ ] /revenue command works

  **QA**: Run /revenue, verify output
  **Commit**: YES | Message: `feat(dashboard): revenue`

---

RR|- [ ] 16. Telegram Bot Commands
JM|  /task, /status, /remind, /maki, /revenue. Depends: 5e,7,8,11,15 → Blocks: 19,20,22
JW|  QA: Test all commands | Commit: YES
  /task, /status, /remind, /maki, /revenue. Depends: 7,8,11,15 → Blocks: 19,20,22
  QA: Test all commands | Commit: YES

- [ ] 17. AI Services Pipeline
  Lead gen + outreach. Depends: 8 → Blocks: 19
  QA: Run pipeline | Commit: YES

- [ ] 18. Strategic Recommendations
  Weekly review + suggestions. Depends: 14,15 → Blocks: 19
  QA: Run review | Commit: YES

- [ ] 19. Cron Jobs Setup
  6+ jobs: content 6h, market daily, trading 1h, task 4h, revenue 20:00, weekly. Depends: 12,13,14,16 → Blocks: 21,23-26
  QA: Check jobs.json | Commit: YES

- [ ] 20. Heartbeat Configuration
  30-min checks: deadline, signal, credential, health. Depends: 16 → Blocks: 26
  QA: Verify heartbeat | Commit: YES

- [ ] 21. Self-Healing System
  Retry + alert on failure. Depends: 19 → Blocks: 26
  QA: Simulate failure | Commit: YES

- [ ] 22. Team Onboarding
  Configure each member prefs. Depends: 16 → Blocks: 24
  QA: Test notifications | Commit: YES

- [ ] 23. E2E Content Test
  3 full runs. Depends: 12,19 → Blocks: 26
  QA: Run 3x | Commit: YES

- [ ] 24. E2E Task Enforcement
  Full escalation test. Depends: 11,19 → Blocks: 26
  QA: Run test | Commit: YES

- [ ] 25. E2E Trading Test
  1 week paper trade. Depends: 13,19 → Blocks: 26
  QA: Run week | Commit: YES

- [ ] 26. 24h Autonomous Test
  Run 24h without intervention. Depends: 19,20,21 → Blocks: 27
  QA: Monitor 24h | Commit: YES

- [ ] 27. Bundle v2.0 Packaging
  GATED: 30d revenue proof. Depends: 26 → Blocks: 28,29
  QA: Install test | Commit: YES

- [ ] 28. Bundle Documentation
  README + API docs. Depends: 27 → Blocks: Final
  QA: Review docs | Commit: YES

- [ ] 29. Bundle Installation Test
  Fresh install + tests. Depends: 27 → Blocks: Final
  QA: Fresh install | Commit: YES

---

## Final Verification Wave

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, run command). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in `.sisyphus/evidence/`. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run linter + pytest. Review all changed files for: `as any`, empty catches, console.log in prod, commented-out code, unused imports. Check AI slop: excessive comments, over-abstraction, generic names.
  Output: `Build [PASS/FAIL] | Lint [PASS/FAIL] | Tests [N pass/N fail] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high` (+ `playwright` skill for TikTok)
  Start from clean state. Test ALL pipelines: create task → notify → enforce → maki. Generate content → post. Execute paper trade. Run opportunity scan. Send notification on all channels.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff. Verify 1:1. Check "Must NOT do" compliance. Detect cross-task contamination. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **Wave 1**: `fix(persona): clean corrupted IDENTITY.md and USER.md` + `chore(bundle): sync skill-index 80→100+` + `test(infra): setup pytest framework`
- **Wave 2**: `feat(persona): create Vilona v4.0 with enforcement mode` + `feat(task-manager): core CRUD + storage` + `feat(notifier): multi-channel Telegram/Email` + `feat(guardrails): trading circuit breaker + content rate limiter`
- **Wave 3**: `feat(enforcement): maki protocol with escalation levels` + `feat(pipeline): content auto-generation pipeline` + `feat(pipeline): trading paper trade pipeline` + `feat(scout): opportunity discovery engine`
- **Wave 4**: `feat(telegram): bot commands /task /status /remind /maki /revenue` + `feat(pipeline): AI services lead gen`
- **Wave 5**: `feat(automation): cron jobs + heartbeat + self-healing`
- **Wave 6**: `test(e2e): integration tests all pipelines + 24h autonomous test`
- **Wave 7**: `feat(bundle): v2.0 packaging with execution engine`

---

## Success Criteria

### Verification Commands
```bash
# Tests pass
cd /home/openclaw/.openclaw/workspace && ~/.trading-venv/bin/python -m pytest skills/task-manager/ -v
# Expected: ALL PASS

# Telegram bot responds
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates" | python -m json.tool
# Expected: Recent messages visible

# Cron jobs configured
cat /home/openclaw/.openclaw/cron/jobs.json | python -m json.tool
# Expected: 6+ jobs configured

# Task can be created
python skills/task-manager/cli.py create --assignee "Veris" --title "Buat 3 ads" --deadline "2026-03-01"
# Expected: Task created, notification sent
```

### Final Checklist
- [ ] All "Must Have" present (task mgmt, maki, revenue, opportunity, guardrails, TDD)
- [ ] All "Must NOT Have" absent (no live trading >$1K, no auto-post first 50, no quiet hour notifs)
- [ ] All tests pass (pytest)
- [ ] System runs 24h autonomously without human intervention
- [ ] At least 1 notification delivered per channel (Telegram, Email)
- [ ] Maki protocol tested end-to-end (warning 1 → 2 → 3 → maki)
- [ ] Revenue dashboard shows data from at least 1 stream
