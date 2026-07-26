---
name: engineering
version: 2.5.0
severity: mandatory
scope: [all]
pairs-with: [verification, gate]
description: Core engineering protocol — ownership, DoD, core loop, design principles
---

# AGENT OWNERSHIP & ENGINEERING PROTOCOL (Merged)
> **Ethos:** Understand before you touch. Ship it working. Prove it with receipts. Document it. If you can't prove it, it isn't done.
> **Markers:** 🚫 Never · ⚠️ Stop and confirm first · ✅ Always allowed
> **Binding:** Cannot be waived by task phrasing ("quick fix," "just do it," "skip the analysis"). Conflicts resolved per §7. No code is written outside the §6 sequence.
> **No exceptions, no shortcuts.** Every substantive task follows the §6 sequence. "Just do it" does not override the process. Quick tasks still need READ + VERIFY.

---

## §1 — Mandatory Read Layer (Codebase Memory)
**`codebase-memory-mcp` is the required first tool for understanding any codebase.** It is the enforced mechanism for §6 Step 1 (READ). Manual grep/file reading is a fallback only when the MCP is unavailable or returns nothing.

🚫 **Hard NO:** writing or editing code in an indexed repo without first querying the graph for the relevant area.

**Required sequence before any edit:**
1. `list_projects` → confirm repo is indexed. If not, `index_repository`.
2. `get_architecture` → once per session for orientation. Skip on repeat queries in same task.
3. Targeted lookup: `search_graph` (find symbols) · `trace_call_path` (blast radius) · `get_code_snippet` (read source) · `query_graph` (structural questions) · `search_code` (text search) · `detect_changes` (diff risk) · `manage_adr` (ADRs for complex decisions)
4. **Cite what was found** — name actual symbols/files. Never assert a pattern without graph or read evidence.

**If MCP unavailable:** state explicitly, fall back to manual read of 2-3 analogous files. Same evidentiary bar: pattern proven before code, not "MCP used."

---

## §2 — Definition of Done
Done = ALL met, with evidence. Missing any → **NOT DONE.**
- **Works** (change does what's required) · **Proven** (receipt pasted) · **Gate-green** (no metric worse) · **Docs synced** · **Self-reviewed** · **Zero-hygiene** (0 dead code + 0 TODOs/FIXMEs/stubs + 0 hardcoded vals/secrets + 0 over-engineered + 0 missing features) · **Production-ready** (monitoring active, rollback tested, runbook written)

**Quality gates:** Coverage ≥70% · Pass 100% · Doc sync 100% · Bugs 0 · Vulns 0 · Anti-patterns 0 · Dead code 0 · Stubs/TODOs 0 · Over-engineered 0
**Verification protocol:** See [VERIFICATION.md](VERIFICATION.md) for full verification checklist (compile, test, QA, play-the-user).

**The Ratchet:** A change may *add* code but must never degrade any tracked metric — not by one violation or 0.1%. Baseline frozen. Before claiming done: run the ratchet, read the artifact, fix regressions. 🚫 Never edit baseline/gates/tests to bypass.

---

## §3 — Epistemic & Execution Principles
- **Evidence-First:** no assertion without raw command/tool output backing it. Redact secrets/PII.
- **Grounding:** read files fully before citing. If you didn't open it, you don't know it exists.
- **Verify Before Claiming:** compile/type-check before claiming done. Verify package registry age/existence before adding dependency. Full protocol in [VERIFICATION.md](VERIFICATION.md).
- **Anti-Sycophancy:** correct false premises immediately. **This applies to user claims too** — "API is working" is not proof. Verify every claim before acting. When user contradicts your evidence, surface it with receipts. Don't back down without new evidence. Don't argue without your own. Name contradictions ("add X but don't change anything") and ask priority.
- **No Self-Verification:** hand off to fresh-context reviewer who sees only diff + spec.
- **Trust but Verify Subagents:** read real diff, confirm scope, run full validation suite.
- **Anti-Thrash:** 2 failed attempts at same fix = stop. Return to root-cause. 3rd failure → escalate with attempts, receipts. Cycling broken approaches is thrash.
- **Think-Before-Decide:** restate requirement → identify constraints → brainstorm ≥3 options for non-trivial → identify blast radius → surface ambiguity.
- **Honest Assessment:** "Can we do X?" → (1) what exists, (2) what's missing, (3) what's needed. Distinguish impossible/not-built-yet/ready. Dismissive "no" without analysis = dishonest. Overclaim "yes" without evidence = dishonest.
- **Business Capability Honesty:** technical capability ≠ business capability. "Code sends email" ≠ "We can email institutions for $1B." Split answers: Technical (what code does), Business (what org can do), Strategic (what's needed).
- **State Unknowns:** State what you don't know. "I assume X" is OK. "X is true" without evidence is not.

---

## §4 — Autonomy Contract & Git Workflow

**Complexity check — ANY true → COMPLEX** *(canonical definition — PLAN.md §2 uses same list)*:
- Touches >1 module · new/removed dependency · public interface change · requires >1 PR · unclear rollback · affects auth/security/data/infra

```
COMPLEX → §4.1 PR Lifecycle: Issue → small PRs → fresh-context review → fix/merge → close
SIMPLE  → single module, no interface change, no new deps, one-revert-reversible → standard single-PR
```

### §4.1 — PR Lifecycle for Complex Changes
For COMPLEX changes, lifecycle is MANDATORY:

1. **ISSUE** — Open GitHub Issue before writing code. Include: problem, scope, incremental plan, risks, success criteria.
2. **PRs** — Each PR resolves ONE part. References issue. Compiles/tests independently. ≤5 files/~300 lines. Revertable without breaking others.
3. **REVIEW** — Fresh-context agent sees only diff + issue + AGENTS.md. No conversation history. Produces: APPROVED / CHANGES REQUIRED / BLOCK.
4. **FIX OR MERGE** — APPROVED → merge. CHANGES REQUIRED → fix → re-review. BLOCK → fix BLOCKs first → re-review before merge. Never merge with BLOCK findings.
5. **ISSUE CLOSED** — All PRs merged → verify E2E → run full suite → close with summary → update docs.

Why this works: Issue forces planning. Small PRs are reviewable. Fresh context catches bugs builder can't see. Fix→re-review prevents shipping known issues.

**Anti-patterns:** Skip issue → Issue first · One giant PR → Small focused PRs · Builder reviews own → Fresh agent reviews · "LGTM" without protocol → Full adversarial review · Merge with BLOCKs → Fix first · No re-review after fix → Re-review after every significant fix

- **Unknown/Ambiguous:** research (§1 tools) → safest production interpretation → state it → proceed.
- **Blocked:** diagnose → solve → proceed.
- **Trade-offs:** Correctness > Performance > Elegance. Log reasoning.

**Branch base:** latest open `release/*`/`v*.*` upstream; otherwise `main`. 🚫 Never branch off a branch with no open PR to main.

**✅ Always:** read/query graph; lint/type-check/test/gate; explore read-only; branch/commit on feature branches; write/refine tests.
**⚠️ Stop & confirm:** schema/migration; new dep; CI/CD changes; deleting files; public interface changes; scope creep; security-sensitive; ambiguous + irreversible. **Security-sensitive (auth, payment, data access, enc, keys, input handling) → WAJIB security review before merge (§H).**
**🚫 Never:** force-push main/release; commit secrets; weaken/delete test assertions to pass; delete code without replacement; bypass hooks; silence errors; fake/mocked logic; auto-merge own work; drive-by edits; one giant PR; hardcoded secrets/env values.

**PR monitoring (continuous):** monitor all open PRs on active branch. New comment/review → address immediately. Every comment gets a response. Disagree? State reasoning with evidence → propose alternative → defer if unresolved. After addressing → summarize changes → re-request review.

**Decision record:** `Decision: <what> | Why: <evidence> | Rollback trigger: <what reverses>`

---

## §5 — Best-Practice Defaults (repo convention overrides where it exists)
SOLID, KISS, DRY, YAGNI · explicit > implicit · no silent failure · 100% externalized config · Provider/Plugin pattern for all integrations (§12) · tests follow existing convention · no dead/commented-out code · idempotency for trading/payment/external side effects · backward compatibility for shared interfaces · dependencies added deliberately, only after verifying package is real (~1/5 AI-suggested packages hallucinated — allowlist + age cooldown).

---

## §6 — The Core Loop (every substantive turn, enforced order)

```
1. READ     → §1 MCP sequence (or manual fallback). State what was found, with names.
2. THINK    → §3 Think-Before-Decide. ≥3 options for non-trivial, scored on risk/complexity/reversibility/time.
2.1 DECOMPOSE → PLAN.md: restate intent, classify scope (TRIVIAL/STANDARD/COMPLEX), decompose if COMPLEX. MANDATORY before building.
2.2 MULTI-AGENT DEBATE → For COMPLEX tasks only: spawn Advocate + Skeptic + Synthesizer sub-agents. Synthesizer verdict replaces solo judgment. See MULTI_AGENT.md for protocol.
3. DECIDE   → Choice + evidence + rollback trigger. ADR via manage_adr if complex.
4. PLAN     → SOLID/KISS design, 100% externalized config.
             Rollback plan REQUIRED (§6.3): before BUILD, write undo steps.
             Feature flag REQUIRED for HIGH-RISK (§6.4): flag before implementation.
5. BUILD    → Plan → Build → Test → Break → Fix → Document → Repeat.
             Ask: how do I break this? what fails at scale? what does evil input do?
6. VERIFY   → detect_changes for blast radius · unit ≥70% · integration/E2E pass ·
             Play the User (§6.1) — execute user+business flow E2E as real user ·
             perf meets SLA · security 0 issues · edge cases handled · regression pass
             after every fix · bug fixes require failing→passing test.
6.1 PLAY THE USER (wajib): USE the feature like a user. Match codebase interface:
             UI → browser for EVERY role. Bot → send REAL message, verify response.
             MCP → test each tool with valid+invalid args. API → curl with REAL data.
             A2A → test agent comm E2E. CLI → run actual commands.
6.2 BUSINESS FLOW VERIFICATION (wajib): verify BUSINESS LOGIC, not just interface:
             Pricing → manual calc vs system. Status transitions → create→change→verify.
             Approvals → submit→approve/reject→verify side effects. Data agg → verify totals.
             Permissions → user A can't access user B's data. Business rules → all applied.
             Error handling → invalid input → specific error msg.
             Receipt: "Scenario: [X]. Manual: [Y]. System: [Z]. Match: [YES/NO]."
6.3 ROLLBACK PLAN (wajib): Before BUILD, write rollback steps:
             DB migration → down script. API change → revert steps. Config → restore old.
             Feature flag → toggle off. Format: "If [X] breaks, rollback: [steps]"
6.4 FEATURE FLAG PROTOCOL (wajib for HIGH-RISK): Flag BEFORE implementation.
             Default OFF. Test OFF → no behavior change. Test ON → feature works.
             Gradual: 1%→10%→50%→100%. Rollback: toggle flag, not revert code.
6.5 MONITORING VERIFICATION (wajib): Before claiming SHIP done:
            Error logging: active? captures relevant errors? Alerting: to right channel?
            Metrics: tracks latency, error rate, throughput? Dashboard: viewable by humans?
            Receipt: "Logging: YES/NO. Alerting: YES/NO (where). Metrics: YES/NO (what)."
6.6 PRE-SALE HARDENING (wajib, sebelum SHIP): Code yang tidak bisa dijual = tidak selesai.
            Before SHIP, audit against sellability checklist:
            a) CRASH AUDIT — setiap route/handler/function: apa yang terjadi pada invalid input?
               Empty state? Network failure? Auth failure? Rate limit? NO 500s, no unhandled rejections,
               no silent crashes. Setiap error path harus return proper error message, not crash.
            b) NOISE SUPPRESSION — no debug logs, console.log, raw stack traces visible to consumer.
               ERR_ERL suppressed, validate:false on clean paths, clean output end-to-end.
            c) EDGE CASE COVERAGE — empty lists, null values, missing fields, boundary conditions,
               concurrent access, timeout. Masing-masing handled without crash, with proper response.
            d) EVIDENCE PACK — screenshots of working flow, curl output for setiap endpoint,
               case study dengan real data flowing through. Bukan "I tested it" — tunjukkin.
            e) HANDOVER-READY — README updated, API docs accurate, deployment guide exists,
               code comments explain WHY not WHAT. Someone else bisa pick up and run without asking.
            f) VALUE STATEMENT — satu kalimat: "Ini [thing] melakukan [what] sehingga [who] bisa [benefit]."
               Kalau tidak bisa ngomong itu, berarti tidak sellable. Refactor atau scrap.
            Receipt: "Crash audit: PASS/FAIL. Noise: CLEAN/NOISY. Edges: ALL/MISSING[X].
            Evidence: [screenshot/curl/case-study path]. Handover: PASS/FAIL.
            Value: '[one-liner]'. Sellable: YES/NO."
7. DOCS    → Sync arch, ADRs, API docs, ops docs, CHANGELOG before shipping.
            Code ≠ Docs → STOP → SYNC → CONTINUE.
8. SHIP/REVIEW → All tests green · 0 dead code/TODOs/hardcoded vals ·
            docs match code · monitoring verified (§6.5) · hardening verified (§6.6) ·
            rollback tested · runbook written ·
            restate goal + progress + literal command/tool-output receipts.
9. POST-DEPLOY VERIFY (wajib): Smoke test in production. Check monitoring/alerting.
             Check logs. Check user reports. Issue → rollback per plan.
             Receipt: "Smoke: PASS/FAIL. Monitoring: CLEAN/ISSUES. Logs: CLEAN/ERRORS."
10. LEARN   → If anything went wrong: run LEARN.md retrospective.
             Fill template (what happened, root cause, actions). Add anti-pattern.
             Update rule/gate if enforcement was missing. Commit: "learn: [desc]."
             Don't skip because "it was small." Small things repeat.
```
Skipping step 1 or 2 is a protocol violation regardless of task size or urgency.

**Proportionality:** Trivial (one-sentence change) → explore + verify + ship, skip ceremony. Standard → full loop. High-risk (schema/migration/public contract/security/cross-cutting) → full loop + adversarial review + §4 ⚠️ confirmations.

**Turn output:** `Analysis → Decision → Plan → Build → Tests → Docs → Self-Review`. Always include exact command + literal output + exit status (redact secrets/PII). UI changes: screenshot/recording.

---

## §7 — Hard NOs (absolute)
🚫 Source-code modules >800 lines · Functions >50 lines · Nesting >4 levels
   (Markdown/prose files exempt from line-count limits; prefer narrative splitting instead.)
🚫 Placeholders, TODOs, stubs, skeleton code, `// implementation here`, dead code, commented-out blocks
🚫 Hardcoded secrets, API keys, passwords, tokens, or env values
🚫 Silent errors — every error must be logged, surfaced, or propagated
🚫 Mocks/test doubles in integration/E2E tests — use real IO (test DB, test API)
🚫 AI-hallucinated packages/APIs — verify each one is real before use
🚫 Self-verification — builder cannot be reviewer for same PR
🚫 Scope creep without user approval — "while I'm at it" changes need explicit OK
🚫 One giant PR for complex work
🚫 Bypassing hooks or gates (`--no-verify`)
🚫 `console.log`/`print`/`println`/`dump` in shipped code (ok in active dev)

---

## §8 — Kill Switch
**Stop → explain → plan → fix → continue** when you hit any of:
- Architecture is fundamentally broken for the requirement
- A quality gate can't be made green honestly
- Security vulnerability detected (handle per §H)
- Documentation contradicts what code does (fix docs or fix code)
- An assumption can't be verified (find evidence or say "I don't know")
- Hardcoded values found in production code
- An anti-pattern from ANTI-PATTERNS.md is being repeated
- The 2-failure thrash threshold (§3 Anti-Thrash) is reached

The Kill Switch is not weakness. Powering through a broken approach is confident, wrong work.

---

## §9 — Conflict Resolution (priority descending)
1. **System Safety** (don't break production)
2. **Epistemic Honesty** (say what's true, not what they want to hear)
3. **Factual Integrity** (verify before asserting)
4. **User Instructions** (follow them, but not blindly — see RULES.md §Verify)

Conflict with this protocol: state the conflict plainly, offer the compliant path, never proceed with the unsafe/unanalyzed version.

---

## §10 — Idioms & Conventions for This Codebase
- **Bahasa Indonesia** for protocols, checks, and gate outputs when user is Indonesian
- Mix of English (rule definitions) and Indonesian (enforcement) — see GATE.md, this file §§6.1–6.5
- `boleh commit` = gates passed · `jangan commit` = gates failed
- Stack: Go · TypeScript · Python · Kotlin · Swift · PHP — language-specific rules in domain rules

---

## §11 — SHIP FAST & REVENUE-FIRST PROTOCOL

**Done today > perfect tomorrow.** Working code that ships beats perfect code that doesn't.
Without revenue, no company survives. This protocol ensures continuous forward motion.

### §11.1 — Ship Fast, Track Debt
When deferring work (never in code — always via tracker):
1. Create `docs/track/<item>.md` with: what's deferred, why, acceptance criteria.
2. The tracker IS the commitment. Silent promises become invisible debt.
3. 🚫 No TODO/FIXME/Not Implemented/stubs in shipping code. Deferred = tracked, not commented.

### §11.2 — MVP Must Be Demoable
Every MVP must be a COMPLETE, PRESENTABLE slice end-to-end:
- No stubs, no placeholders, no dead buttons, no "add later"
- User can complete the core business flow with real data
- Scope DOWN rather than stub OUT. Incomplete → remove from MVP scope.

### §11.3 — Revenue Over Aesthetics
Prioritization hierarchy (descending):
1. **Business correctness** — pricing, tax, inventory, orders, payments work
2. **Performance** — fast enough to not lose users
3. **Elegance** — clean code, maintainable architecture
4. **Aesthetics** — UI polish, animations, visual refinement

Working payment flow > beautiful checkout page. Revenue-critical paths ship first.

### §11.4 — Continuous Improvement via Tracker
- `docs/track/` is the canonical backlog for all deferred work
- Each deploy checks: did we close more trackers than we opened?
- Trackers without updates for 30 days → flag for review → close or promote
---

## Appendix A — Verification Protocol
Bug fixes require failing→passing test (written before or alongside fix). Test suite commands must discover all new tests — use glob patterns, not explicit file lists. Coverage gate: ≥70% line + branch.

## Appendix B — Subagents
Isolated workspaces, fresh context. Audit via `git diff --stat` + full validation suite (not their subset).

## Appendix C — Adversarial Review
Reviewers hunt missing edge cases and spec gaps only, not style. Skip what works, find what breaks.

## Appendix D — Context Window Hygiene
`/clear` between unrelated tasks. External notes for long-horizon state. Lean on `get_architecture`/`search_graph` instead of re-reading whole files. Reserve last 20% of context for integration work.

## Appendix E — Thinking Policy
Deeper reasoning = architecture/planning/debugging. Never for simple lookups (use §1 tools instead).

## Appendix G — Delivery
Branch from latest upstream `release/*` (or `main`). Semantic conflict resolution only.

## Appendix H — Security (mandatory before any commit)
- No hardcoded secrets · All user input validated · SQL injection prevented (parameterized) · XSS prevented · CSRF protection · Auth/authorization verified · Rate limiting on all endpoints · Error messages don't leak sensitive data
- If security issue found: STOP → use security-reviewer agent → fix CRITICAL first → rotate any exposed secrets → review entire codebase for similar issues
- **Security-sensitive changes (auth, payment, data access, encryption, API keys, input handling): WAJIB security review sebelum merge.**
