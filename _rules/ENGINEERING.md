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
            ==========================================================================
            Sebelum SHIP, jalankan 6 audit berikut. Setiap audit WAJIB produce receipt.
            Kalau salah satu FAIL → HARDEN dulu, baru SHIP.

            ──────────────────────────────────────────────────────────────────────
            AUDIT A: CRASH AUDIT (setiap endpoint/handler/function)
            ──────────────────────────────────────────────────────────────────────
            Goal: NO 500s, NO unhandled rejections, NO silent crashes.
            Cara: Abuse setiap entry point seperti attacker:

            [API Routes]   curl -X POST dengan body kosong
                           curl -X POST dengan JSON invalid (trailing comma, string instead of int)
                           curl -X POST dengan field missing
                           curl -X POST dengan tipe salah (string di field number)
                           curl dengan auth token expired / missing
                           curl dengan rate-limit abuse (30x in 1s)
                           curl ke route yang不存在 (404 handling)
            [Functions]    Call with null/undefined/none
                           Call with empty string/list/dict
                           Call with out-of-range values
                           Call with concurrent invocations
            [CLI Tools]    Run tanpa args
                           Run dengan arg salah
                           Run dengan path tidak ada

            ✅ LULUS: setiap test return error message (bukan crash/500).
                      Error message: specific, human-readable, no stack trace leaked.
            ❌ GAGAL: 500 Internal Server Error, unhandled TypeError/ReferenceError,
                      Promise rejection tanpa catch, silent try/except yang swallow error.

            Receipt template:
            ```
            CRASH AUDIT:
            Endpoint        | Test                  | Result     | Error msg
            ----------------|-----------------------|------------|-------------------------
            POST /orders    | empty body            | 400        | "body: required"
            POST /orders    | invalid JSON          | 400        | "body: invalid JSON"
            POST /orders    | missing user_id       | 400        | "user_id: required"
            GET /orders/xxx | nonexistent id        | 404        | "order not found"
            GET /orders     | expired token         | 401        | "token expired"
            GET /orders     | no auth header        | 401        | "authorization required"
            Verdict: PASS / FAIL (n unhandled crashes)
            ```

            ──────────────────────────────────────────────────────────────────────
            AUDIT B: NOISE SUPPRESSION (clean output)
            ──────────────────────────────────────────────────────────────────────
            Goal: Zero debug artifacts visible to consumer.
            Cara:
            1. Grep all source files for noise:
               `grep -rn 'console\.log\|print(\|println\|fmt\.Print\|puts\|p DEBUG\|logger\.Debug\|console\.error' src/ --include='*.py' --include='*.js' --include='*.ts' --include='*.go' --include='*.rs' | grep -v test/ | grep -v vendor/`
            2. Cek production output: jalankan app → tangkap stdout/stderr → pastikan tidak ada
               debug noise, raw stack trace, atau log yang seharusnya cuma untuk dev.
            3. Cek error responses: pastikan error message ke user tidak mengandung:
               - Internal path (/var/www/... /home/user/...)
               - Stack trace
               - Query/command text
               - Environment variable names
               - Database detail (table name, column name)

            ✅ LULUS: output ke consumer = intended response only.
                      DEBUG-level log hanya ke file/stdout, NEVER ke HTTP response.
            ❌ GAGAL: `{"error": "TypeError: Cannot read property 'x' of undefined at /app/server.js:42"}`
                      `validate:true` / `ERR_ERL` visible in production responses.
                      `console.log("user data:", user)` left in shipped code.

            Receipt template:
            ```
            NOISE AUDIT:
            Noise grep          : 0 matches (or N matches — all in test/ or handled)
            Production stdout   : CLEAN — only [expected output]
            Error responses     : CLEAN — no paths, traces, or internals leaked
            Verdict: CLEAN / NOISY (fix: _____)
            ```

            ──────────────────────────────────────────────────────────────────────
            AUDIT C: EDGE CASE MATRIX
            ──────────────────────────────────────────────────────────────────────
            Goal: Setiap state boundary handled gracefully.
            Audit matrix — apply to setiap function/route yang relevan:

            | Edge case               | What to test                                              |
            |-------------------------|-----------------------------------------------------------|
            | Empty input             | [], {}, "", null, undefined, 0                            |
            | Missing field           | Payload tanpa field wajib                                  |
            | Wrong type              | String di number field, number di string field             |
            | Boundary                | Max int, min int, max length, 0 items, 1 item, N items     |
            | Duplicate              | Submit data yang sama 2x                                 |
            | Concurrent             | 2 requests bersamaan ke resource yang sama                  |
            | Timeout                 | Dependency slow/offline — apakah handler timeout graceful? |
            | State order             | Approve→Submit vs Submit→Approve — semua urutan?          |
            | Invalid state transit   | Cancel already-cancelled order, delete already-deleted     |
            | Auth mismatch           | User A akses data User B                                    |

            Untuk setiap edge case:
            - Catat input → expected output → actual output → verdict
            - Kalau actual ≠ expected → ini BUG → fix sebelum SHIP

            Receipt template:
            ```
            EDGE CASE MATRIX:
            Feature/Route | Edge              | Expected          | Actual            | Verdict
            --------------|-------------------|-------------------|-------------------|---------
            POST /orders  | empty body        | 400 + error msg   | 400 + error msg   | PASS
            POST /orders  | duplicate submit  | 409 "already exists" | 500 crash      | ❌ FAIL
            Verdict: ALL PASS / N EDGES FAIL (fix: _____)
            ```

            ──────────────────────────────────────────────────────────────────────
            AUDIT D: EVIDENCE PACK
            ──────────────────────────────────────────────────────────────────────
            Goal: Bisa tunjukkin ke calon buyer bahwa ini kerja.
            Wajib produce 3 artifacts:

            d1) SCREENSHOTS (untuk UI/Web):
                - Screenshot setiap flow step (before → after)
                - Annotate dengan arrow/circle untuk highlight
                - Simpan di `docs/evidence/screenshots/`

            d2) CURL RECEIPTS (untuk API/Backend):
                - Setiap endpoint: curl command + response (status + body)
                - Include happy path + 1 error path per endpoint
                - Simpan di `docs/evidence/curl/`

            d3) CASE STUDY (untuk calon buyer):
                Format minimal:
                ```markdown
                # Case Study: [Feature Name]
                ## Problem
                [What problem does this solve? 2-3 kalimat]

                ## Solution
                [How does it work? Key architecture decisions]

                ## Real Data Flow
                ```
                [Input] → [System Process] → [Output]
                - Input: [what goes in]
                - Process: [what happens internally]
                - Output: [what comes out — include screenshot/curl]
                ```

                ## Business Impact
                - [Metric X]: [before] → [after]
                - [Metric Y]: [before] → [after]

                ## How to Verify
                [Exact steps someone else can follow to see it working]
                ```

            ✅ LULUS: screenshots ada, curl receipts ada, case study written with real data.
            ❌ GAGAL: "I tested it, trust me" / "it works on my machine" / no evidence files.

            Receipt template:
            ```
            EVIDENCE PACK:
            Screenshots : N files at docs/evidence/screenshots/
            Curl receipts: N files at docs/evidence/curl/
            Case study  : docs/evidence/case-study-[feature].md
            Verdict: COMPLETE / MISSING (_____)
            ```

            ──────────────────────────────────────────────────────────────────────
            AUDIT E: HANDOVER-READY CHECK
            ──────────────────────────────────────────────────────────────────────
            Goal: Someone else bisa clone repo + run tanpa tanya.
            Checklist:

            [ ] README.md exists dan mencakup:
                - Apa ini? (one-liner)
                - Prerequisites (language, database, API keys, env vars)
                - Quick Start (clone → install → configure → run — exact commands)
                - Architecture (diagram atau text — main components + data flow)
            [ ] API docs accurate (OpenAPI, README, atau docstrings):
                - Setiap endpoint tercantum dengan request/response format
                - Error codes documented
            [ ] Deployment guide exists:
                - Production vs development config
                - Env vars list (template .env.example)
                - Persistence (DB setup, migrations)
                - Health check endpoint
            [ ] Code comments explain WHY not WHAT:
                - `# Retry 3x because external API is eventually consistent` ✓
                - `# Loop through items` ✗ (code already shows WHAT)
            [ ] No sensitive data in code:
                - No hardcoded keys/passwords/tokens
                - .env.example uses placeholder values
                - .gitignore includes .env, secrets, logs

            Receipt template:
            ```
            HANDOVER CHECK:
            README           : EXISTS / MISSING
            API docs         : COMPLETE / PARTIAL / MISSING
            Deployment guide : EXISTS / MISSING
            Code comments    : WHY-based / WHAT-based / MISSING
            Secrets in code  : 0 leaks (or N leaks — fix before ship)
            Verdict: PASS / FAIL (fix: _____)
            ```

            ──────────────────────────────────────────────────────────────────────
            AUDIT F: VALUE STATEMENT
            ──────────────────────────────────────────────────────────────────────
            Goal: Satu kalimat yang bikin calon buyer ngerti kenapa ini berharga.

            Formula: "Ini [THING] melakukan [WHAT] sehingga [WHO] bisa [BENEFIT]."

            Contoh:
            - ✅ "Ini automated trading bot melakukan eksekusi order berdasarkan signal
                 sehingga trader bisa profit tanpa monitor layar 24 jam."
            - ✅ "Ini API gateway melakukan validasi + routing request
                 sehingga developer bisa deploy microservices tanpa manage auth sendiri."
            - ❌ "Ini API untuk trading." (terlalu umum — gak jelas value-nya)
            - ❌ "Ini bot." (gak ngasih tau apa yang bot ini lakukan)

            Kalau tidak bisa bikin value statement yang jelas dalam 1 kalimat:
            ➤ Berarti kamu sendiri tidak paham apa yang kamu buat.
            ➤ STOP. Refactor atau scrap. Jangan SHIP code yang tidak paham value-nya.

            Receipt template:
            ```
            VALUE STATEMENT:
            "Ini [_________] melakukan [_________] sehingga [_________] bisa [_________]."
            Sellable: YES / NO (if NO, stop and rethink)
            ```

            ──────────────────────────────────────────────────────────────────────
            MASTER RECEIPT (wajib di copy-paste ke SHIP output):
            ──────────────────────────────────────────────────────────────────────
            ```
            ╔══════════════════════════════════════════════════════════╗
            ║      PRE-SALE HARDENING — MASTER RECEIPT                ║
            ╠══════════════════════════════════════════════════════════╣
            ║ A. Crash audit  : PASS / FAIL (n crashes)              ║
            ║ B. Noise        : CLEAN / NOISY                        ║
            ║ C. Edge cases   : ALL PASS / N FAIL                    ║
            ║ D. Evidence pack: COMPLETE / MISSING                   ║
            ║ E. Handover     : PASS / FAIL                          ║
            ║ F. Value        : "[statement]"                        ║
            ╠══════════════════════════════════════════════════════════╣
            ║ SELLABLE: YES / NO                                     ║
            ╚══════════════════════════════════════════════════════════╝
            ```
            Jika SELLABLE = NO → DON'T SHIP. Harden dulu.
            Jika SELLABLE = YES → proceed ke §7 DOCS.
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
