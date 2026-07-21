---
name: registry
version: 1.0.0
severity: mandatory
scope: [all]
description: Central rule registry — all governed rules with metadata, priority, and relationships
---

# REGISTRY.md — Rule Registry

> Central index of all governed rules. Every rule has an ID, priority, severity, status, and testable assertions.
> The `1ai rules` command reads this file as its primary data source.

---

## R-RULE-001

**ID:** R-RULE-001
**Name:** Read First, Then Write
**File:** RULES.md#L18
**Priority:** 10
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Every file edit is preceded by reading the file
- Rule checker detects files edited without being read
**Relationships:** pairs-with: R-ENG-001; overlaps: R-ENG-002

---

## R-RULE-002

**ID:** R-RULE-002
**Name:** Don't Lie — Proof Required
**File:** RULES.md#L23
**Priority:** 10
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Every completion claim has terminal output or screenshot proof
- "Should work" or "tested" are not accepted as evidence
**Relationships:** pairs-with: R-GATE-001

---

## R-SEC-003

**ID:** R-SEC-003
**Name:** Security Response Protocol
**File:** SECURITY.md
**Priority:** 10
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Security issues are stopped immediately and reviewed
- Critical issues fixed before continuing work

---

## R-ENG-001

**ID:** R-ENG-001
**Name:** Source lib/paths.sh for Canonical Paths
**File:** ENGINEERING.md
**Priority:** 9
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- All new scripts source lib/paths.sh
- Scripts use canonical paths from shared library

---

## R-GATE-001

**ID:** R-GATE-001
**Name:** Evidence-First Claims
**File:** GATE.md
**Priority:** 9
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- All completion claims backed by terminal output or observable evidence
- No unverified assertions about code behavior
**Relationships:** pairs-with: R-RULE-002

---

## R-GATE-002

**ID:** R-GATE-002
**Name:** Smoke Test Verification
**File:** GATE.md
**Priority:** 9
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Behavioral changes verified by running specific test or scenario
- Smoke tests validate the change before claiming completion
**Relationships:** requires: R-VER-001

---

## R-GATE-005

**ID:** R-GATE-005
**Name:** No Partial Delivery
**File:** GATE.md
**Priority:** 9
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Deliverables complete end-to-end before yield
- No stubs, mocks, TODO placeholders, or reduced scope masked as done
**Relationships:** pairs-with: R-ENG-005

---

## R-RULE-003

**ID:** R-RULE-003
**Name:** Check Before Using
**File:** RULES.md#L26
**Priority:** 9
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Every API, function, or config is verified with grep/read/curl before use
- No assumption about availability without verification
**Relationships:** overlaps: R-RULE-001

---

## R-RULE-004

**ID:** R-RULE-004
**Name:** Right Repo
**File:** RULES.md#L29
**Priority:** 9
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Verify the task matches the current repo before starting work
- Stop and notify if task is outside domain

---

## R-RULE-005

**ID:** R-RULE-005
**Name:** Code Must Run
**File:** RULES.md#L32
**Priority:** 9
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Code compiles with zero errors
- All tests pass (N/N pass, zero failures)
**Relationships:** overlaps: R-VER-001

---

## R-RULE-007

**ID:** R-RULE-007
**Name:** Verify Business Logic
**File:** RULES.md#L38
**Priority:** 9
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Calculate expected result manually
- Compare system output with manual calculation — fix if different
**Relationships:** refines: R-VER-002

---

## R-SEC-001

**ID:** R-SEC-001
**Name:** No Hardcoded Secrets
**File:** SECURITY.md
**Priority:** 9
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- No API keys, passwords, or tokens hardcoded in source
- All secrets use environment variables or secret manager

---

## R-VER-001

**ID:** R-VER-001
**Name:** Test-Driven Verification
**File:** VERIFICATION.md
**Priority:** 9
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Every test defends an observable contract
- Tests detect a plausible bug — not just plumbing or defaults
**Relationships:** pairs-with: R-QA-001

---

## R-ENG-002

**ID:** R-ENG-002
**Name:** Shellcheck Compliance (-S style)
**File:** ENGINEERING.md
**Priority:** 8
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- All scripts pass shellcheck -S style --rcfile .shellcheckrc
- Shellcheck warnings are resolved before commit

---

## R-ENG-003

**ID:** R-ENG-003
**Name:** New Files Only
**File:** ENGINEERING.md
**Priority:** 8
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Create new files only; never overwrite except bin/1ai and Makefile
- Existing work is preserved unless explicitly stated otherwise

---

## R-ENG-004

**ID:** R-ENG-004
**Name:** No Git Operations
**File:** ENGINEERING.md
**Priority:** 8
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- No git operations in framework scripts
- Main agent handles commits externally

---

## R-ENG-005

**ID:** R-ENG-005
**Name:** No TODO/FIXME Stubs
**File:** ENGINEERING.md
**Priority:** 8
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Every file must be real, working code
- No TODO/FIXME placeholders shipped as complete work

---

## R-GATE-003

**ID:** R-GATE-003
**Name:** Rollback Plan
**File:** GATE.md
**Priority:** 8
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Changes include documented rollback procedures
- Rollback tested or verified before deployment

---

## R-QA-001

**ID:** R-QA-001
**Name:** Test Infrastructure
**File:** QA.md
**Priority:** 8
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Test runner exists and is executable
- Makefile has test targets for running the suite

---

## R-RULE-006

**ID:** R-RULE-006
**Name:** Test Like a Real User
**File:** RULES.md#L35
**Priority:** 8
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Open browser, send messages, call APIs — like a real user
- For MCP tests: verify response with both valid and invalid data
**Relationships:** requires: R-QA-001

---

## R-RULE-008

**ID:** R-RULE-008
**Name:** Write Rollback Plan
**File:** RULES.md#L41
**Priority:** 8
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Before build, document how to revert changes
- Database: migration rollback; API: version revert; Config: restore
**Relationships:** pairs-with: R-GATE-003

---

## R-SEC-002

**ID:** R-SEC-002
**Name:** Input Validation at Boundaries
**File:** SECURITY.md
**Priority:** 8
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- All user input validated before processing
- No data from external sources is trusted implicitly

---

## R-VER-002

**ID:** R-VER-002
**Name:** Behavior over Implementation
**File:** VERIFICATION.md
**Priority:** 8
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Tests verify behavior, boundaries, invariants, not source text
- Tests are deterministic, isolated, and pass full-suite-safe

---

## R-ENG-006

**ID:** R-ENG-006
**Name:** Defer Protocol
**File:** ENGINEERING.md
**Priority:** 7
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Incomplete items documented in docs/track/<item>.md
- Deferred items are tracked, not silently dropped

---

## R-ENG-007

**ID:** R-ENG-007
**Name:** SCRIPT_DIR Convention
**File:** ENGINEERING.md
**Priority:** 7
**Severity:** advisory
**Status:** active
**Category:** general
**Assertions:**
- All scripts declare SCRIPT_DIR with canonical pattern
- Functions use lowercase_with_underscores

---

## R-ENG-008

**ID:** R-ENG-008
**Name:** Main Dispatch Pattern
**File:** ENGINEERING.md
**Priority:** 7
**Severity:** advisory
**Status:** active
**Category:** general
**Assertions:**
- Scripts have a main dispatch at bottom: main "$@"
- Consistent entry point pattern across all scripts

---

## R-ENG-009

**ID:** R-ENG-009
**Name:** Exit Code Constants
**File:** ENGINEERING.md
**Priority:** 7
**Severity:** advisory
**Status:** active
**Category:** general
**Assertions:**
- Scripts source lib/exit-codes.sh for E_* constants
- Exit codes use named constants, not bare integers

---

## R-GATE-004

**ID:** R-GATE-004
**Name:** Checklist Sign-off
**File:** GATE.md
**Priority:** 7
**Severity:** advisory
**Status:** active
**Category:** general
**Assertions:**
- Pre-commit checklist reviewed before claiming completion
- Unchecked items block the commit
**Relationships:** refines: R-RULE-009

---

## R-QA-002

**ID:** R-QA-002
**Name:** Layer-Based Testing
**File:** QA.md
**Priority:** 7
**Severity:** recommended
**Status:** active
**Category:** general
**Assertions:**
- Testing follows layer-based protocol with evidence requirements
- Full QA cycle before pre-release or major changes

---

## R-RULE-009

**ID:** R-RULE-009
**Name:** Self-Review
**File:** RULES.md#L44
**Priority:** 7
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Read own diff before committing
- Remove unnecessary code; verify assumptions

---

## R-RULE-010

**ID:** R-RULE-010
**Name:** Update Documentation
**File:** RULES.md#L47
**Priority:** 7
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Code changes require documentation updates
- No commit if docs are not updated

---

## R-VER-003

**ID:** R-VER-003
**Name:** Coverage Threshold
**File:** VERIFICATION.md
**Priority:** 7
**Severity:** recommended
**Status:** active
**Category:** general
**Assertions:**
- Tests maintain 80%+ coverage on modified code
- Critical paths have dedicated test coverage

---

## R-DEP-001

**ID:** R-DEP-001
**Name:** Deprecation Notice
**File:** DEPRECATION.md
**Priority:** 6
**Severity:** advisory
**Status:** active
**Category:** general
**Assertions:**
- Deprecated features have clear migration path or notice
- Deprecation is communicated before removal

---

## R-RULE-011

**ID:** R-RULE-011
**Name:** SOLID Principles
**File:** RULES.md#L50-60
**Priority:** 6
**Severity:** recommended
**Status:** active
**Category:** general
**Assertions:**
- Single responsibility per class/function
- Open for extension, closed for modification
- Depend on abstractions, not implementations

---

## R-RULE-012

**ID:** R-RULE-012
**Name:** Provider/Plugin Pattern
**File:** RULES.md#L70
**Priority:** 6
**Severity:** recommended
**Status:** active
**Category:** general
**Assertions:**
- All external integrations use interface + implementation pattern
- No hardcoded providers; inject via config

---

## R-ANT-001

**ID:** R-ANT-001
**Name:** Growing catalog of AI agent failure modes — discovered from 
**File:** core/ANTI-PATTERNS.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Growing catalog of AI agent failure modes — discovered from real incidents
- Location: core/ANTI-PATTERNS.md

---

## R-COM-001

**ID:** R-COM-001
**Name:** Communication rules, channels, cadence, and escalation
**File:** core/COMMS.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Communication rules, channels, cadence, and escalation
- Location: core/COMMS.md

---

## R-COS-001

**ID:** R-COS-001
**Name:** Cost classification, attribution, unit economics, and cloud/
**File:** core/COST.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Cost classification, attribution, unit economics, and cloud/AI spend governance
- Location: core/COST.md

---

## R-CPL-001

**ID:** R-CPL-001
**Name:** Regulatory compliance scope, audit trail, GDPR/PDPA checklis
**File:** core/COMPLIANCE.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Regulatory compliance scope, audit trail, GDPR/PDPA checklists, data subject rights, and breach noti...
- Location: core/COMPLIANCE.md

---

## R-CST-001

**ID:** R-CST-001
**Name:** Cost Tracking
**File:** core/COST_TRACKING.md
**Priority:** 5
**Severity:** advisory
**Status:** active
**Category:** general
**Assertions:**
- Cost Tracking
- Location: core/COST_TRACKING.md

---

## R-CUS-001

**ID:** R-CUS-001
**Name:** Customer operations — tiers, support SLA, escalation, feedba
**File:** core/CUSTOMER.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Customer operations — tiers, support SLA, escalation, feedback, churn, data rules, refunds, and comm...
- Location: core/CUSTOMER.md

---

## R-DAT-001

**ID:** R-DAT-001
**Name:** Data classification, retention, deletion, backup, access con
**File:** core/DATA.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Data classification, retention, deletion, backup, access control, breach response, and agent data hy...
- Location: core/DATA.md

---

## R-DEC-001

**ID:** R-DEC-001
**Name:** Decision authority thresholds, approval flows, and reversibi
**File:** core/DECISION.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Decision authority thresholds, approval flows, and reversibility
- Location: core/DECISION.md

---

## R-DEP-002

**ID:** R-DEP-002
**Name:** Graceful Phase-Out
**File:** DEPRECATION.md
**Priority:** 5
**Severity:** advisory
**Status:** active
**Category:** general
**Assertions:**
- Deprecated APIs maintain backward compatibility for one cycle
- Removal only after grace period expires

---

## R-DOC-001

**ID:** R-DOC-001
**Name:** Full-stack codebase documentation template (AI & human reada
**File:** core/DOCS.md
**Priority:** 5
**Severity:** recommended
**Status:** active
**Category:** general
**Assertions:**
- Full-stack codebase documentation template (AI & human readable)
- Location: core/DOCS.md

---

## R-DTM-001

**ID:** R-DTM-001
**Name:** Canonical documentation templates — feature matrix, gap anal
**File:** core/DOC_TEMPLATES.md
**Priority:** 5
**Severity:** recommended
**Status:** active
**Category:** general
**Assertions:**
- Canonical documentation templates — feature matrix, gap analysis, competitor files, decision logs, Q...
- Location: core/DOC_TEMPLATES.md

---

## R-ETH-001

**ID:** R-ETH-001
**Name:** Agent behavioral boundaries, escalation conditions, and huma
**File:** core/ETHICS.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Agent behavioral boundaries, escalation conditions, and human override
- Location: core/ETHICS.md

---

## R-FIN-001

**ID:** R-FIN-001
**Name:** Budget approval, spending limits, invoicing, and revenue tra
**File:** core/FINANCE.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Budget approval, spending limits, invoicing, and revenue tracking
- Location: core/FINANCE.md

---

## R-HES-001

**ID:** R-HES-001
**Name:** Human Escalation
**File:** core/HUMAN_ESCALATION.md
**Priority:** 5
**Severity:** advisory
**Status:** active
**Category:** general
**Assertions:**
- Human Escalation
- Location: core/HUMAN_ESCALATION.md

---

## R-HIR-001

**ID:** R-HIR-001
**Name:** How to add, retire, and manage agents and human collaborator
**File:** core/HIRING.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- How to add, retire, and manage agents and human collaborators
- Location: core/HIRING.md

---

## R-INC-001

**ID:** R-INC-001
**Name:** Incident severity levels, response protocol, war room, and p
**File:** core/INCIDENT.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Incident severity levels, response protocol, war room, and postmortem
- Location: core/INCIDENT.md

---

## R-LEG-001

**ID:** R-LEG-001
**Name:** Legal risk, IP ownership, OSS compliance, privacy, contracts
**File:** core/LEGAL.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Legal risk, IP ownership, OSS compliance, privacy, contracts, and escalation protocol for AI-operate...
- Location: core/LEGAL.md

---

## R-LRN-001

**ID:** R-LRN-001
**Name:** Retrospective and rule update protocol — turning incidents i
**File:** core/LEARN.md
**Priority:** 5
**Severity:** recommended
**Status:** active
**Category:** general
**Assertions:**
- Retrospective and rule update protocol — turning incidents into permanent fixes
- Location: core/LEARN.md

---

## R-MAG-001

**ID:** R-MAG-001
**Name:** Multi-agent collaboration protocol — Advocate, Skeptic, Synt
**File:** core/MULTI_AGENT.md
**Priority:** 5
**Severity:** recommended
**Status:** active
**Category:** general
**Assertions:**
- Multi-agent collaboration protocol — Advocate, Skeptic, Synthesizer roles for research and brainstor...
- Location: core/MULTI_AGENT.md

---

## R-MEM-001

**ID:** R-MEM-001
**Name:** Memory
**File:** core/MEMORY.md
**Priority:** 5
**Severity:** advisory
**Status:** active
**Category:** general
**Assertions:**
- Memory
- Location: core/MEMORY.md

---

## R-MSN-001

**ID:** R-MSN-001
**Name:** Company vision, mission, values, and north star
**File:** core/MISSION.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Company vision, mission, values, and north star
- Location: core/MISSION.md

---

## R-OKR-001

**ID:** R-OKR-001
**Name:** Quarterly objectives, key results, KPIs, and work alignment
**File:** core/OKR.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Quarterly objectives, key results, KPIs, and work alignment
- Location: core/OKR.md

---

## R-ONB-001

**ID:** R-ONB-001
**Name:** First session checklist for any new agent or human — must co
**File:** core/ONBOARDING.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- First session checklist for any new agent or human — must complete before first task
- Location: core/ONBOARDING.md

---

## R-PLN-001

**ID:** R-PLN-001
**Name:** Task decomposition, scoping, and planning — the gap between 
**File:** core/PLAN.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Task decomposition, scoping, and planning — the gap between "I have a task" and "I'm writing code"
- Location: core/PLAN.md

---

## R-PRD1-001

**ID:** R-PRD1-001
**Name:** PRD creation, atomic issue breakdown, and PR description sta
**File:** core/PRD.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- PRD creation, atomic issue breakdown, and PR description standard
- Location: core/PRD.md

---

## R-PRD2-001

**ID:** R-PRD2-001
**Name:** Feature lifecycle protocol — intake through deprecation, sco
**File:** core/PRODUCT.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Feature lifecycle protocol — intake through deprecation, scope control, flags, metrics, and backlog ...
- Location: core/PRODUCT.md

---

## R-PRF-001

**ID:** R-PRF-001
**Name:** Agent performance measurement, authority changes, improvemen
**File:** core/PERFORMANCE.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Agent performance measurement, authority changes, improvement protocols, and role lifecycle governan...
- Location: core/PERFORMANCE.md

---

## R-REL-001

**ID:** R-REL-001
**Name:** Versioning, changelog, deployment checklist, and rollback pr
**File:** core/RELEASE.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Versioning, changelog, deployment checklist, and rollback protocol
- Location: core/RELEASE.md

---

## R-REV-001

**ID:** R-REV-001
**Name:** Adversarial fresh-context review protocol
**File:** core/REVIEWER.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Adversarial fresh-context review protocol
- Location: core/REVIEWER.md

---

## R-ROL-001

**ID:** R-ROL-001
**Name:** Every role, authority level, and responsibility
**File:** core/ROLES.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Every role, authority level, and responsibility
- Location: core/ROLES.md

---

## R-RUN-001

**ID:** R-RUN-001
**Name:** Daily health checks, failure procedures, scaling, rotation, 
**File:** core/RUNBOOK.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Daily health checks, failure procedures, scaling, rotation, and operational log requirements for AI-...
- Location: core/RUNBOOK.md

---

## R-SME-001

**ID:** R-SME-001
**Name:** Subagent Memory
**File:** core/SUBAGENT_MEMORY.md
**Priority:** 5
**Severity:** advisory
**Status:** active
**Category:** general
**Assertions:**
- Subagent Memory
- Location: core/SUBAGENT_MEMORY.md

---

## R-SRP-001

**ID:** R-SRP-001
**Name:** Org-wide agent OS — competitive research, strategic planning
**File:** core/SURPASS.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Org-wide agent OS — competitive research, strategic planning, implementation, and continuous surpass...
- Location: core/SURPASS.md

---

## R-STR-001

**ID:** R-STR-001
**Name:** Session Tracing
**File:** core/SESSION_TRACING.md
**Priority:** 5
**Severity:** advisory
**Status:** active
**Category:** general
**Assertions:**
- Session Tracing
- Location: core/SESSION_TRACING.md

---

## R-VEN-001

**ID:** R-VEN-001
**Name:** Vendor registry, selection criteria, dependency risk, SLA mo
**File:** core/VENDOR.md
**Priority:** 5
**Severity:** mandatory
**Status:** active
**Category:** general
**Assertions:**
- Vendor registry, selection criteria, dependency risk, SLA monitoring, renewal, offboarding
- Location: core/VENDOR.md

---

## Version History

| Version | Date       | Author | Summary             |
|---------|------------|--------|---------------------|
| 1.0.0   | 2026-07-14 | 1ai    | Initial rule registry with all core files cataloged |

## Coverage

- **Total core files:** 44
- **Files with sub-rule entries:** 7
- **Files with summary entries:** 35
- **Total rule entries:** 70
- **Coverage status:** 100% — all core governed files represented
