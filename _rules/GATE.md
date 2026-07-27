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
GATE 6: PRE-SALE HARDENING (SELLABILITY CHECK) — WAJIB ENGINEERING.md §6.6
  - Kerjain 6 audit dari ENGINEERING.md §6.6:
    A. Crash audit     → abuse setiap entry point: empty body, invalid JSON, missing fields,
                         expired token, rate-limit abuse. NO 500s, NO silent crashes.
                         Receipt: crash audit table (endpoint × test × result × error msg)
    B. Noise audit     → grep console.log/print/DEBUG dari src/
                         cek production output: no stack traces, no internal paths, no ERR_ERL
                         Receipt: "Noise grep: 0 matches. Stdout: CLEAN. Errors: CLEAN."
    C. Edge case matrix → empty/null/duplicate/concurrent/timeout/invalid state transition
                         Receipt: edge case table (feature × edge × expected × actual × verdict)
    D. Evidence pack   → screenshots (UI) + curl receipts (API) + case study (docs/evidence/)
                         Receipt: "Screenshots: N files. Curl: N files. Case study: [path]"
    E. Handover check  → README exists + API docs + deployment guide + WHY comments + no secrets
                         Receipt: "README: YES. API docs: COMPLETE. Deploy guide: YES. Secrets: 0"
    F. Value statement → "Ini [thing] melakukan [what] sehingga [who] bisa [benefit]"
                         Receipt: value statement one-liner
  - MASTER RECEIPT (wajib):
    ╔══════════════════════════════════════════════╗
    ║ Crash: PASS/FAIL  Noise: CLEAN/NOISY        ║
    ║ Edges: ALL/N_FAIL Evidence: COMPLETE/MISSING ║
    ║ Handover: PASS/FAIL Value: [statement]       ║
    ║ SELLABLE: YES / NO                           ║
    ╚══════════════════════════════════════════════╝
  Bukti: [paste MASTER RECEIPT]
  Sellable: [YES/NO — jika NO, jangan commit sebelum fixed]
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
