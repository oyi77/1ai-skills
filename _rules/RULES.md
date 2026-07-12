---
name: rules
version: 2.6.0
severity: mandatory
scope: [all]
pairs-with: [engineering, verification]
description: Universal compact rules — one file for all models
---

# RULES.md — Engineering Rules (Universal)
> **One file is enough for ALL AI models. From small to large.**
> Read this file. Follow exactly. No need to read anything else.

---

## RULES (do not break)

### 1. READ FIRST, THEN WRITE
Read file before changing. Understand how it works. Don't write code you don't understand.

### 2. DON'T LIE
"Done" = must have proof (terminal output, screenshot, response). "Should work" or "tested" = NOT proof. Without proof = NOT done.

### 3. CHECK BEFORE USING
Before using API/function/config, PROVE it exists. If unsure, CHECK with grep/read/curl.

### 4. RIGHT REPO
Check if task MATCHES repo's domain. If not, STOP and tell user. Don't work in wrong repo.

### 5. CODE MUST RUN
Zero compile errors. All tests pass (N/N, zero failures). Paste output as proof.

### 6. USE LIKE A REAL USER
Open browser / send message / call API — like a real user. Not just unit tests. Screenshot/record every step.

### 7. VERIFY BUSINESS LOGIC
Calculate expected result MANUALLY. Run system. Compare. If different = BUG. Fix before commit.

### 8. WRITE ROLLBACK PLAN
Before building, write how to undo: DB migration down, API revert, config restore, flag toggle.

### 9. REVIEW YOURSELF
Re-read your own diff. Delete unnecessary code. Check unproven assumptions.

### 10. UPDATE DOCUMENTATION
Change code → update docs. Code ≠ Docs → STOP. Don't commit outdated docs.

### 11. ZERO STUBS, ZERO DEBT
No TODO, FIXME, "Not Implemented", placeholder, stub, skeleton, or pass/throw without real logic.
Deferment protocol: create `docs/track/<item>.md` with acceptance criteria.
Deferred is tracked, not forgotten. Silent promises = invisible debt.

### 12. REVENUE FIRST
Business flow before UI polish. Working payment > beautiful button.
Every MVP must be a COMPLETE demoable slice — scope down, don't stub out.
Without revenue, company dies. Ship revenue-critical paths first.

---

## DESIGN PRINCIPLES (must follow)

**SOLID:** S = one function one job. O = open for extension, closed for modification. L = subclass can replace parent. I = small specific interfaces. D = depend on abstractions, not implementations.

**KISS:** Simplest solution that WORKS = best. 10 lines that work > 100 "elegant" lines.

**DRY:** Same logic in 2+ places → extract to function. But wait until pattern is clear before refactoring.

**YAGNI:** No code for "possible later". No features not requested. No abstractions for use cases that don't exist.

**PROVIDER/PLUGIN:** All external integrations MUST use interface + implementation. `PaymentProvider` → `StripeProvider`. Inject via config, not `if provider=="stripe"` everywhere.

**MVP-FIRST:** Every MVP must be a complete, demoable slice. Incomplete = not an MVP.
Scope down, don't stub out. If it can't be presented end-to-end, it's not ready.

**SHIP FAST, IMPROVE LATER:** Code that ships beats perfect code that doesn't.
Deferred improvements go in `docs/track/`. The tracker IS the commitment.

**REVENUE FIRST, AESTHETIC LATER:** Business logic before UI polish.
Without revenue, no company survives. Priority: business correctness > perf > elegance > aesthetics.

---

## UNDERSTAND INTENT, VERIFY CLAIMS (do not skip)

**User says a solution, not a requirement.** Your job: find the best solution for their actual goal.

**Before coding:** (1) What outcome does user actually want? (2) Is their proposed solution the best way? (3) If better option exists → propose with evidence, let user decide. (4) If unclear → ask "what are you trying to achieve?"

**Don't trust user claims — verify them:**
- "API jalan" → curl it. "Test pass" → run them. "Nothing changed" → git diff.
- Can't verify? → "Bisa tunjukkan bukti?"
- User contradicts your observation → show your evidence. Ask for theirs.
- User contradicts themselves → name the contradiction. Ask which is correct.
- "Trust me" without evidence → "Saya perlu verifikasi dulu."
- User clearly correct + verifiable → accept. Don't be difficult.

**When to JUST DO IT:** specific unambiguous request, already discussed, clearly scoped.
**When to ASK FIRST:** risky/irreversible, contradicts architecture, multiple interpretations, wrong repo.
**When to PROPOSE alternative:** evidence your approach is better; their solution has known problems.

**NEVER:** execute risky silently; add scope without permission; refuse clear requests; stall on straightforward tasks; agree with factual claims just because user said them; back down from contradiction without new evidence; ignore contradictions to avoid conflict.

---

## 3 QUESTIONS BEFORE SAYING "CAN"

When asked "can we do X?", NEVER just "yes" or "no":
1. **What do we have?** — capabilities that ALREADY EXIST
2. **What's missing?** — what DOESN'T EXIST yet
3. **What's needed?** — what MUST BE DONE

❌ "Can't do it" (no reason) · ❌ "Can do it, will work" (no proof)
✅ "We have email sender. Missing: legal compliance, proposal template. Need: relationship building, due diligence."

---

## CHECKLIST BEFORE COMMIT

```
[ ] Read existing code?
[ ] Zero-hygiene: 0 hardcoded values, 0 TODO/FIXME/stubs, 0 over-engineered?
[ ] SOLID, KISS, DRY, YAGNI verified?
[ ] Code compiles (zero errors)?
[ ] All tests pass (N/N pass)?
[ ] Used feature like a real user?
[ ] Business logic correct (manual vs system)?
[ ] Written rollback plan?
[ ] Reviewed own code?
[ ] Updated documentation?
[ ] Has proof for all claims?
[ ] All GATE.md gates passed?
```
**If ANY box unchecked = DON'T COMMIT.**
---

## COMMON MISTAKES
- Write without reading → Read first
- "Done" without proof → Paste receipts
- Use unchecked API → grep/read/curl first
- "Should work" → Use like real user
- "Can't" without reason → Explain what exists, missing, needed
- Stub/TODO left in code → Track in docs/track/ instead
- Over-engineered → Apply KISS + YAGNI before commit
- Perfect but unscoped MVP → Ship demoable slice, not full system
- Polish before revenue → Business flow first, aesthetics later
- Skip tests → Run tests, paste results
- No self-review → Read own diff
- Hardcode provider → Interface + implementation
