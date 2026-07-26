---
name: gate
version: 3.0.0
severity: mandatory
scope: [ship, commit]
pairs-with: [engineering, verification, qa, docs]
description: Pre-ship compliance gate checklist (7 unique gates + cross-refs)
---

# GATE.md — Pre-Ship Checklist
> **READ THIS BEFORE COMMITTING.** Every checklist item REQUIRES real evidence (terminal output, screenshot, response).
> `Bukti` = Evidence. If any field is empty → DO NOT COMMIT. Fill it first.

After these 7 gates, proceed through the per‑file checklists below:

---

## Gates Unique to GATE.md

```
GATE 0: UNDERSTAND INTENT, VERIFY CLAIMS
  - Apa yang user MINTA? (copy exact words)
  - Apa yang user MAU? (tujuan akhir)
  - Apakah solusi yg diminta = solusi terbaik untuk tujuan itu?
    Ya → lanjut. Tidak → "Anda minta X. Saya sarankan Y karena [alasan]. Setuju?"
    Tidak jelas → tanya tujuan
  - Verifikasi klaim user: API jalan? curl. Test pass? run. DB ada? check.
  Bukti: [SAID → WANTS → solution → WHY] + [verified claim: Y/T]

GATE 1: CEK DOMAIN REPO
  - Tugas sesuai repo ini? Kalau tidak → STOP.
  Bukti: [domain repo + apakah task sesuai]

GATE 2: CEK SEBELUM PAKAI
  - Before using any API, function, or config: PROVE it exists. Grep/read/curl if unsure.
  Bukti: [apa yg dipakai + bukti ada]

GATE 3: REVIEW SENDIRI
  - Read own diff. Unnecessary code? Unverified assumptions? Can delete without behavior change?
  Bukti: [review OK / perlu diperbaiki: X]

GATE 4: AGENT REVIEW — COMPLEX only (STANDARD optional)
  - PR uses PRD.md §4 template (Summary, Changes, How to Test, QA Results, Checklist)
  - PR references its issue (Closes #NNN) — no issue ref = BLOCK
  - COMPLEX: fresh-context Reviewer Agent runs REVIEWER.md protocol.
    No self-approval. No merge without APPROVED / APPROVED WITH CONDITIONS.
    CHANGES REQUIRED = fix all BLOCK findings, re-review.
  - STANDARD: peer/self-review with checklist documented
  - TRIVIAL: self-review only
  Bukti: [TRIVIAL] / [STANDARD — checklist done] / [COMPLEX — verdict: APPROVED, PR #X]
GATE 5: PLAYBOOK UPDATE CHECK
  - Did this task change systems, code, or company processes?
    No → skip this gate (explain why in bukti)
    Yes → PLAYBOOK PROTOCOL in RULES.md requires a timeline entry
  - Timeline updated in `~/projects/1ai-playbook/content/playbook/timeline/index.mdx`?
  - Format: date, what, sections affected, files changed, status, why it matters
  Bukti: [skip — no impact] / [updated YYYY-MM-DD — entry content]
GATE 6: PRE-SALE HARDENING (SELLABILITY CHECK)
  - Crash audit: every handler handles errors? NO 500s? NO silent crashes?
  - Noise suppression: debug logs/console.log suppressed? ERR_ERL cleaned?
  - Edge case coverage: empty/null/failure/timeout/concurrent states handled?
  - Evidence pack: screenshots/curl/case study produced with real data?
  - Handover-ready: README, API docs, deployment guide accurate?
  - Value statement: "Ini [thing] melakukan [what] sehingga [who] bisa [benefit]"?
  Bukti: [PASS/FAIL — yang belum: ______]
  Sellable: [YES/NO — jika NO, jangan commit sebelum fixed]
  - Did this task change systems, code, or company processes?
    No → skip this gate (explain why in bukti)
    Yes → PLAYBOOK PROTOCOL in RULES.md requires a timeline entry
  - Timeline updated in `~/projects/1ai-playbook/content/playbook/timeline/index.mdx`?
  - Format: date, what, sections affected, files changed, status, why it matters
  Bukti: [skip — no impact] / [updated YYYY-MM-DD — entry content]
```

---

## Standard Checklist (cross‑refs to core files)

| # | Check | Source |
|---|-------|--------|
| C1 | Compile — zero errors | ENGINEERING.md §6 Step 5 |
| C2 | All tests pass — N/N pass, zero failures | VERIFICATION.md §1 |
| C3 | QA scenarios — ≥2 happy + 2 sad paths per feature | QA.md |
| C4 | Use like real user — browser/send/curl/screenshot | ENGINEERING.md §6.1 |
| C5 | Business logic verification — manual calc vs system | ENGINEERING.md §6.2 |
| C6 | Rollback plan — down script / revert steps / toggle | ENGINEERING.md §6.3 |
| C7 | Feature flag (HIGH‑RISK only) — default OFF | ENGINEERING.md §6.4 |
| C8 | Monitoring verification — logging / alerting / metrics | ENGINEERING.md §6.5 |
| C9 | Update docs — Code ≠ Docs → STOP | DOCS.md |
| C10 | Timeline updated — playbook/timeline/ modified per RULES.md PLAYBOOK PROTOCOL | RULES.md PLAYBOOK PROTOCOL |
| C11 | **Pre-sale hardening — crash audit, noise, edges, evidence, handover, value** | ENGINEERING.md §6.6 |

---

## Status
```
[ ] ALL GATES PASSED — boleh commit
[ ] ADA YANG GAGAL — gate yg belum: _________________________________
```

*GATE.md ini WAJIB dijalankan sebelum setiap commit. Tidak ada pengecualian.*
