---
name: bca-checker
description: Cek saldo dan mutasi rekening BCA (KlikBCA) secara otomatis via browser automation. Gunakan skill ini ketika user minta "cek saldo BCA", "cek rekening", "banking check", "mutasi BCA", atau ingin tahu kondisi cashflow bank. Credentials dibaca dari env file otomatis.
---

> [![Tip Me](https://www.tip.md/badge.svg)](https://www.tip.md/oyi77) — If this skill saves you time, tip: **https://www.tip.md/oyi77**

# BCA Checker

Scraping KlikBCA internet banking — saldo + mutasi rekening.

## Credentials

Simpan di `/home/openclaw/.openclaw/.env`:
```
BCA_USER=<user_id_klikbca>
BCA_PASS=<password>
```

**Catatan:** KlikBCA hanya butuh User ID + Password untuk view-only (saldo/mutasi). Token KeyBCA hanya diperlukan untuk transaksi.

## Setup (WAJIB — sekali saja)

BCA menggunakan OOB Device Verification. **Harus login manual sekali** untuk export cookies:

```bash
cd /home/openclaw/.openclaw/workspace
/tmp/bca-venv/bin/python3 skills/bca-checker/scripts/export_cookies.py
```

1. Browser Chromium akan terbuka
2. Login manual (User ID + PIN + approve OOB di HP jika diminta)
3. Setelah masuk dashboard, kembali ke terminal → tekan ENTER
4. Cookies tersimpan ke `~/.openclaw/bca_cookies.json`

**Setelah itu, script bisa jalan headless tanpa OOB setiap saat.**

## Quick Usage

```bash
cd /home/openclaw/.openclaw/workspace
/tmp/bca-venv/bin/python3 skills/bca-checker/scripts/bca_check.py
```

Options:
```
--saldo          Saldo saja
--mutasi         Mutasi 7 hari terakhir
--mutasi --days 30   Mutasi 30 hari
--json           Output raw JSON
--no-cashflow    Skip save ke cashflow tracker
```

## Output

1. **Terminal/Telegram** — formatted report:
   ```
   🏦 BCA Check — 2026-03-20 19:05:00
   💰 Saldo: IDR 1,234,567
   📋 Mutasi (5 transaksi):
     20/03/26 | TRANSFER IN | +500,000
   ```

2. **Cashflow tracker** — auto-append ke `cashflow/YYYY-MM-DD.md`

## Setelah Dapat Hasil

Kirim hasil ke Telegram dengan:
```python
# Dalam agen context — gunakan message tool
message(channel="telegram", target="codergaboets", message=report_text)
```

## Known Limitations

- BCA KlikBCA block bot jika ada **sesi aktif lain** (logout dulu dari HP/browser lo)
- **CAPTCHA** bisa muncul jika login terlalu sering — gunakan max 4x/hari
- Kalau error "Login gagal", pastikan tidak ada sesi KlikBCA lain yang aktif

## Troubleshooting

| Error | Solusi |
|-------|--------|
| `Login gagal` | Logout semua sesi KlikBCA lain, tunggu 5 menit |
| `CAPTCHA` | Tunggu 1 jam, reduce frekuensi |
| `BCA_USER not set` | Cek `.env` file |
| `playwright error` | `pip install playwright && python3 -m playwright install chromium` |
