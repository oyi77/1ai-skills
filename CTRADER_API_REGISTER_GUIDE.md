# REGISTER APLIKASI CTRADER OPEN API - STEP-BY-STEP

## 🎯 TUJUAN
Dapatkan credentials untuk automated trading 24/7 dengan cTrader API:
- client_id
- client_secret
- access_token
- account_id

---

## 📋 STEP 1: LOGIN KE CTRADER ID

### **Option A: Pakai akun Fusion Markets Anda**
1. Buka: https://id.ctrader.com/
2. Klik "Login" atau "Sign In"
3. Pilih login method:
   - **Option 1:** Login dengan cTrader ID
   - **Option 2:** Login dengan akun broker (Fusion Markets)

### **Option B: Daftar akun cTrader ID baru (jika belum punya)**
1. Buka: https://id.ctrader.com/register
2. Isi:
   - Email: [email Anda]
   - Password: [password baru]
   - Confirm Password: [password baru]
3. Klik "Register"
4. Verify email Anda

---

## 📋 STEP 2: BUKA CTRADER OPEN API DASHBOARD

1. Buka: https://openapi.ctrader.com/apps
2. Jika belum login, Anda akan di-redirect ke login page
3. Login dengan cTrader ID atau akun Fusion Markets

---

## 📋 STEP 3: CREATE NEW APPLICATION

1. Di Open API Dashboard, cari tombol:
   - "Create New Application" atau
   - "Add Application" atau
   - "+" icon
2. Klik tombol tersebut

---

## 📋 STEP 4: ISI DETAIL APLIKASI

### **Form Fields:**

**Application Name:**
- Isi dengan: `BerkahKaryaQuant-Automated` atau nama lain
- Ini nama aplikasi Anda untuk API access

**Application Type:**
- Pilih: `Web` atau `Backend` (bukan Mobile)

**Redirect URI:**
- Isi dengan: `http://localhost:8080` atau `https://example.com/callback`
- Ini URL untuk OAuth callback (bisa bebas untuk demo)

**Description:**
- Isi dengan: `Automated trading bot for XAUUSD Asia 7-Candle Breakout Strategy`

**Scopes/Permissions:**
- Pastikan untuk cek semua yang di-perlukan:
  - ✅ Read account information
  - ✅ Read orders and positions
  - ✅ Place orders
  - ✅ Cancel orders
  - ✅ Read market data
  - ✅ Read historical data

3. Klik "Create" atau "Save"

---

## 📋 STEP 5: SIMPAN CREDENTIALS

Setelah aplikasi dibuat, Anda akan dapat:

### **DARI DASHBOARD:**
```
Client ID:     [panjang string alfanumerik]
Client Secret: [panjang string alfanumerik]
Redirect URI:   http://localhost:8080
```

**SALIN SEMUA INI KE TEMPAT AMAN!**
- Jangan bagikan ke orang lain
- Simpan di file atau password manager

---

## 📋 STEP 6: GENERATE ACCESS TOKEN

### **Option A: Pakai OAuth Flow (Recommended)**

1. Buka URL OAuth authorization:
   ```
   https://id.ctrader.com/my/settings/openapi/grantingaccess/?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI
   ```

2. Replace:
   - `YOUR_CLIENT_ID` → Client ID dari dashboard
   - `YOUR_REDIRECT_URI` → Redirect URI yang Anda set

3. Login jika diminta

4. Grant permissions jika diminta

5. Redirect ke URL Anda dengan authorization code

6. Exchange authorization code untuk access token:
   ```bash
   curl -X POST 'https://openapi.ctrader.com/apps/token' \
     -H 'Accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
       "grant_type": "authorization_code",
       "code": "AUTHORIZATION_CODE",
       "client_id": "YOUR_CLIENT_ID",
       "client_secret": "YOUR_CLIENT_SECRET",
       "redirect_uri": "YOUR_REDIRECT_URI"
     }'
   ```

7. Response:
   ```json
   {
     "access_token": "long-string-here",
     "refresh_token": "long-string-here",
     "expires_in": 604800,
     "token_type": "Bearer"
   }
   ```

### **Option B: Pakai ctrader_sdk Auto-Generate**

Script `asia7c_automated.py` punya method `get_access_token()` yang bisa auto-generate.

Tapi perlu set credentials dulu:
```python
CONFIG = {
    "client_id": "YOUR_CLIENT_ID",        # ← Masukkan dari dashboard
    "client_secret": "YOUR_CLIENT_SECRET",  # ← Masukkan dari dashboard
    "access_token": None,                  # ← Bot akan auto-generate
    "account_id": "YOUR_ACCOUNT_ID"        # ← Dapat dari step 7
}
```

---

## 📋 STEP 7: GET ACCOUNT ID

### **Cara 1: Dari Fusion Markets cTrader Webtrader**
1. Login ke: https://fusionmarkets.com/Platforms/cTrader-Webtrader
2. Cek bagian "Accounts" atau "Settings"
3. Cari "Account ID" atau "Account Number"
4. Copy angka tersebut

### **Cara 2: Dari API Setelah Connect**
Jika sudah connect ke API, bisa dapat dari response `get_account_information()`

---

## 📋 STEP 8: UPDATE CONFIG DI SCRIPT

Buka file: `/home/openclaw/.openclaw/workspace/asia7c_automated.py`

Cari bagian CONFIG dan update:
```python
CONFIG = {
    "broker": "Fusion Markets",
    "server": "FusionMarkets-Demo",
    "symbol": "XAUUSD",
    "timeframe": "H1",
    "timezone": "Asia/Jakarta",
    "asia_session_start": "07:00",
    "asia_session_end": "15:00",
    "candles_count": 7,
    "range_filter_pips": 5,
    "rr_ratio": 2.0,
    "risk_per_trade": 0.01,
    "max_trades_per_day": 3,
    "lot_size": 0.01,

    # ← UPDATE INI:
    "client_id": "COPY_CLIENT_ID_DARI_STEP5",
    "client_secret": "COPY_CLIENT_SECRET_DARI_STEP5",
    "access_token": "AUTO_GENERATE_DARI_BOT",  # Biarkan None
    "account_id": "COPY_ACCOUNT_ID_DARI_STEP7",
}
```

---

## 📋 STEP 9: RUN AUTOMATED TRADING

Setelah credentials di-set, jalankan:

```bash
cd /home/openclaw/.openclaw/workspace
~/.trading-venv/bin/python asia7c_automated.py
```

Bot akan:
1. Connect ke cTrader API
2. Download market data XAUUSD H1
3. Execute XAUUSD Asia 7-Candle Breakout strategy
4. Place orders automatically
5. Track positions
6. Journal semua trades
7. Berjalan 24/7 tanpa stop

---

## ⚠️  PENTING

### **Security:**
- ❌ JANGAN share credentials
- ✅ Simpan di tempat aman
- ✅ Use environment variables jika production

### **Token Refresh:**
- Access token expire (biasanya 7 hari / 604800 detik)
- Bot harus refresh token secara berkala
- ctrader_sdk punya method untuk auto-refresh

### **Demo vs Real:**
- Pastikan menggunakan DEMO account untuk paper trading
- CREDENTIALS demo sama dengan live account
- Beda hanya di account_id

---

## 🆘 TROUBLESHOOTING

### **Problem: "Invalid Client ID/Secret"**
- Check apakah copy dari dashboard dengan benar
- Pastikan tidak ada extra space/character

### **Problem: "Authorization Failed"**
- Pastikan redirect URI match dengan yang di-set
- Cek apakah scopes/permissions di-grant

### **Problem: "Token Expired"**
- Refresh access token dengan refresh token
- Atau generate new authorization code

### **Problem: "Account ID Not Found"**
- Pastikan account ID benar
- Cek di Fusion Markets cTrader Webtrader
- Pastikan account masih aktif

---

## ✅ CHECKLIST

Sebelum run automated trading:

- [ ] Register aplikasi di cTrader Open API
- [ ] Simpan Client ID dan Client Secret
- [ ] Generate atau akan generate Access Token
- [ ] Dapatkan Account ID dari Fusion Markets
- [ ] Update CONFIG di asia7c_automated.py
- [ ] Test connection ke API
- [ ] Verify account balance (harus ~$10,000 demo)
- [ ] Jalankan bot
- [ ] Monitor first few trades
- [ ] Verify journaling working

---

## 📚 REFERENCE

- cTrader Open API: https://help.ctrader.com/open-api/
- Python SDK: https://help.ctrader.com/open-api/python-SDK/python-sdk-index/
- App Registration: https://help.ctrader.com/open-api/api-application/
- Authentication: https://help.ctrader.com/open-api/account-authentication/

---

**READY TO AUTOMATE!** 🚀
