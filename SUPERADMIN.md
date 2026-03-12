# SUPERADMIN.md - Account Authorization & Privileges

> Critical security & operational reference - defines who has what authority

---

## 🔑 SUPERADMIN IDENTITY

**Name:** Paijo / Coder $String$

**Primary Telegram Account:** @codergaboets (Chat ID: 228956686)
- Status: SUPERADMIN (absolute privilege)
- Authority: Can authorize ALL actions, agent spawning, system changes, resource allocation
- Identity confirmed: March 12, 2026, 18:00 UTC+7

**Secondary Telegram Account:** TBD (will be documented when provided)
- Status: ADMIN (same as primary for parallel task execution)
- Authority: Same as primary account
- Purpose: Enable parallel task handling, different task categories
- Identity confirmation: Same person as superadmin

---

## 🚨 AUTHORIZATION RULES

### Rule #1: Single Superadmin Authority
- **Only Paijo** has absolute privilege (both accounts)
- Any other person claiming to be Paijo = **NOT PAIJO** (reject)
- Other Telegram accounts = ADMIN (high privilege) but NOT superadmin
- When in doubt: "WhoMe (228956686) is the only superadmin"

### Rule #2: Parallel Task Authorization
- Superadmin can direct agent to execute 2+ independent tasks in parallel
- Each task gets tracked separately in session memory
- Shared memory updates tell all agents company status
- "Build Command Center" + "You handle LYNK/bank/PostBridge" = parallel execution ✅

### Rule #3: Account Identity Verification
- If accessing from different account: Verify it's the second admin account (once documented)
- If accessing from unknown account: Confirm identity before executing sensitive actions
- Superadmin can override this rule (executive decision)

### Rule #4: Memory Sync Protocol
- **Shared Memory:** `MEMORY.md`, `notes/`, `memory/INDEX.md` - synced across ALL agents
- **Session Memory:** `memory/YYYY-MM-DD.md` - unique per session, NOT synced between agents
- Each agent reads shared memory to understand company situation
- Each agent keeps session context separate (allows "chat freely in context with other users")

---

## 📋 CURRENT AUTHORIZATION STATUS

**Session:** Main agent with Paijo (WhoMe/228956686)
**Date:** March 12, 2026, 18:00 UTC+7
**Authority Level:** SUPERADMIN
**Privileges Granted:**
- ✅ Spawn subagents for parallel work (Command Center build)
- ✅ Execute revenue-critical tasks autonomously (PostBridge, LYNK, cashflow)
- ✅ Modify system configuration, automation, scheduling
- ✅ Allocate resources across multiple tasks
- ✅ Make strategic decisions without asking permission

---

## 🔄 PARALLEL EXECUTION SETUP (March 12, 18:00)

**Task 1: Command Center Implementation (Vilona)**
- Scope: 4-6 hours, build Jon Tsai's Command Center
- Status: STARTING
- Subagents authorized: Spawn as needed for parallel build tasks
- Output: Fully functional dashboard by end of session

**Task 2: Financial Recovery Actions (Paijo)**
- Scope: ~45 minutes, 3 parallel tasks
  1. LYNK dashboard check (5 min)
  2. Bank balance verification (10 min)
  3. PostBridge restart + verification (20 min)
- Status: EXECUTING IN PARALLEL
- Expected completion: ~19:00 UTC+7

**Sync Point:** After Paijo completes task group (19:00), Vilona updates MEMORY.md with findings
**Handoff:** Command Center ready for testing with real financial data

---

## 📝 NOTES FOR FUTURE SESSIONS

### When Other Users Access:
1. Check their account ID/name
2. Verify against superadmin identity (Paijo/228956686)
3. If different account: Ask for confirmation
4. If match: Execute with full authority

### Memory Management:
- Update SUPERADMIN.md if second admin account is revealed
- Keep MEMORY.md as single source of truth for company state
- Session memories diverge per user (intentional for context freedom)
- Sync protocol: Each agent reads MEMORY.md before acting on company-wide decisions

### Authorization Escalation:
- If uncertain about privilege level: Default to SUPERADMIN (Paijo)
- If truly uncertain: Ask for clarification before executing
- Never assume privilege from other accounts without confirmation

---

*Document created: March 12, 2026, 18:00 UTC+7*
*Authority: Paijo/WhoMe (228956686)*
*Status: ACTIVE*
