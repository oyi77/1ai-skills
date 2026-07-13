---
name: gate
version: 3.0.0
severity: mandatory
scope: [ship, commit]
pairs-with: [engineering, verification, qa, docs]
description: Pre-ship compliance gate checklist (5 unique gates + cross-refs)
---

# GATE.md — Pre-Ship Checklist
> **READ THIS BEFORE COMMITTING.** Every checklist item REQUIRES real evidence (terminal output, screenshot, response).
> `Bukti` = Evidence. If any field is empty → DO NOT COMMIT. Fill it first.

After these 5 gates, proceed through the per‑file checklists below:

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

---

## Status
```
[ ] ALL GATES PASSED — boleh commit
[ ] ADA YANG GAGAL — gate yg belum: _________________________________
```

*GATE.md ini WAJIB dijalankan sebelum setiap commit. Tidak ada pengecualian.*
