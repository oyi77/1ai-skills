---
name: gate
version: 2.5.0
severity: mandatory
scope: [ship, commit]
pairs-with: [engineering, verification]
description: Pre-ship compliance gate checklist (15 gates)
---

# GATE.md — Pre-Ship Checklist
> **READ THIS BEFORE COMMITTING.** Every checklist item REQUIRES real evidence (terminal output, screenshot, response).
> `Bukti` = Evidence. If any field is empty → DO NOT COMMIT. Fill it first.

---

```
GATE 0: UNDERSTAND INTENT, VERIFY CLAIMS
  - Apa yang user MINTA? (copy exact words)
  - Apa yang user MAU? (tujuan akhir)
  - Apakah solusi yg diminta = solusi terbaik untuk tujuan itu?
    Ya → lanjut. Tidak → "Anda minta X. Saya sarankan Y karena [alasan]. Setuju?"
    Tidak jelas → tanya tujuan
  - Verifikasi klaim user: API jalan? curl. Test pass? run. DB ada? check.
  Bukti: [SAID → WANTS → solution → WHY] + [verified claim: Y/T]

GATE 1: BACA CODEBASE
  - Baca file yg akan diubah. Pahami cara kerja yg sudah ada.
  Bukti: [apa yg dibaca + apa yg dipahami]

GATE 2: CEK DOMAIN REPO
  - Tugas sesuai repo ini? Kalau tidak → STOP.
  Bukti: [domain repo + apakah task sesuai]

GATE 3: CEK SEBELUM PAKAI
  - Sebelum pakai API/function/config, BUKTIKAN ada. Kalau ragu → grep/read/curl.
  Bukti: [apa yg dipakai + bukti ada]

GATE 4: COMPILE
  - Jalankan compiler/type-checker. Output: zero errors.
  Bukti: [paste output]

GATE 5: TEST SAAT BUILD
  - Saat nulis kode, langsung jalankan test. Gagal → langsung fix.
  Bukti: [paste output]

GATE 6: SEMUA TEST LULUS
  - Jalankan SEMUA test (unit+integration). N/N pass, zero failures.
  Bukti: [paste output dgn jumlah pass/fail]

GATE 7: QA SCENARIOS — HAPPY + SAD PATH
  - Tulis skenario QA: minimal 2 happy path + 2 sad path per fitur.
  - Happy: input valid, flow normal, edge case yg HARUS jalan.
  - Sad: input invalid, data null/kosong, auth gagal, dependency mati.
  - Setiap skenario HARUS punya: precondition, steps, expected, actual, PASS/FAIL.
  - Jalankan semua skenario. Paste hasil NYATA — bukan expected.
  - Deliver QA report INLINE di chat. Simpan ke docs/qa/QA_REPORT_[feature].md juga.
  - Gap/fitur TIDAK BOLEH ditutup sampai semua skenario = PASS.
  Bukti: [QA report inline — N happy PASS, N sad PASS, verdict: ALL PASS]

GATE 8: PAKAI SEPERTI USER NYATA
  - Buka browser / kirim pesan / panggil API — seperti user sungguhan.
  - UI: browser, klik semua tombol. Bot: kirim pesan NYATA. API: curl data NYATA.
  - MCP: test semua tool dgn data benar+salah. Screenshot/record.
  Bukti: [screenshot / curl response / terminal output]

GATE 9: VERIFIKASI LOGIKA BISNIS
  - Hitung expected result MANUAL. Jalankan sistem. Bandingkan.
  - Beda → BUG. Fix sebelum commit.
  Bukti: [Skenario: X. Manual: Y. System: Z. Match: YES/NO]

GATE 10: TULIS ROLLBACK PLAN
  - DB: down script. API: revert steps. Config: restore. Flag: toggle off.
  Bukti: [Kalau X rusak, rollback: langkah-langkah]

GATE 11: FEATURE FLAG (HIGH-RISK only — HIGH-RISK = auth changes, data migrations, external API integrations, or any change that cannot be rolled back by reverting a single file)
  - Flag SEBELUM implementasi. Default OFF. Test OFF: no change. Test ON: works.

GATE 12: MONITORING BERGUNA
  - Error logging: ada? tangkap error penting? Alerting: ada? channel benar?
  - Metrics: ada? track latency, error rate? Dashboard: bisa lihat manusia?
  Bukti: [logging: Y/T, alerting: Y/T (where), metrics: Y/T (what)]

GATE 13: REVIEW SENDIRI
  - Baca ulang diff. Ada kode tdk perlu? Asumsi belum terbukti? Bisa hapus tanpa ubah behavior?
  Bukti: [review OK / perlu diperbaiki: X]

GATE 14: UPDATE DOKUMENTASI
  - Ubah kode → update docs. Code ≠ Docs → STOP.
  Bukti: [docs updated: YA — file: X]

GATE 15: AGENT REVIEW — MANDATORY FOR COMPLEX, RECOMMENDED FOR STANDARD
  - PR description uses ~/.1ai/core/PRD.md §4 template (Summary, Changes, How to Test, QA Results, Checklist)
  - PR references its issue (Closes #NNN) — no issue reference = BLOCK
  - COMPLEX: fresh-context Reviewer Agent runs core/REVIEWER.md protocol in full
    → No self-approval. No merge without APPROVED or APPROVED WITH CONDITIONS verdict.
    → CHANGES REQUIRED = fix all BLOCK findings, then re-review before merge.
  - STANDARD: peer review or self-review with REVIEWER.md §2 checklist documented
  - TRIVIAL: self-review, no reviewer agent required
  Bukti: [TRIVIAL — self-review OK] OR [STANDARD — checklist done] OR [COMPLEX — verdict: APPROVED, PR #X]
```

---

## Status
```
[ ] SEMUA GATE LULUS — boleh commit
[ ] ADA YANG GAGAL — gate yg belum: _________________________________
```

---

*GATE.md ini WAJIB dijalankan sebelum setiap commit. Tidak ada pengecualian.*
