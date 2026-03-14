# 🗺️ FIX GOOGLE MAPS PLACES API (NEW) - STEP BY STEP

## Problem:
API key kamu pakai **Legacy API** yang udah deprecated.

## Solution:
Switch ke **Places API (New)** - ini modern dan punya fitur lebih banyak.

---

## 📋 STEP-BY-STEP GUIDE (2 menit):

### STEP 1: Buka Google Cloud Console
```
https://console.cloud.google.com/
```

### STEP 2: Pilih Project Kamu
- Kalau belum punya project, klik "Create Project"
- Beri nama (misal: "LeadGenMachine")
- Klik "Create"

### STEP 3: Enable Places API (New)
1. Di menu kiri, klik: **"APIs & Services"** → **"Library"**
2. Search: **"Places API"**  ← PENTING!
3. Cari: **"Places API"** (BUKAN "Places Library - Legacy")
4. Klik tombol **"Enable"**
5. Tunggu beberapa detik sampai di-aktifkan

💡 **Tips:** Kalau ada versi "New" atau "v2", pilih yang itu!

### STEP 4: Buat API Key
1. Klik: **"APIs & Services"** → **"Credentials"**
2. Klik tombol **"+ Create Credentials"**
3. Pilih **"API key"**
4. Copy API key yang muncul
5. Klik: **"Restrict key"** (opsional tapi recommended)
6. **Application restrictions:**
   - Pilih: **"IP addresses"**
   - Tambah IP kamu (kalau tahu) atau pilih "None"
7. **API restrictions:**
   - Cari: **"Places API"**
   - Centang: **"Places API"**
   - Klik **"Save"**

### STEP 5: Simpan API Key
Kamu punya API key seperti ini:
```
AIzaSyBu... (lama dengan karakter lain)
```

---

## 🚀 CARA KASIH TAU KE SYSTEM (3 opsi):

### OPTION 1: Environment Variable (RECOMMENDED)
```bash
# Di terminal:
export GOOGLE_MAPS_API_KEY="AIzaSyBu...KAMUBARU"

# Atau tambahkan ke ~/.zshrc atau ~/.bashrc:
echo 'export GOOGLE_MAPS_API_KEY="AIzaSyBu...KAMUBARU"' >> ~/.zshrc
source ~/.zshrc
```

### OPTION 2: Save ke File
```bash
# Buat file:
echo "AIzaSyBu...KAMUBARU" > ~/.credentials/google_places_api_new.txt

# Atau:
echo "AIzaSyBu...KAMUBARU" > ~/.openclaw/google_maps_api_key.txt
```

### OPTION 3: Update OpenClaw Config
```bash
# Update ~/.openclaw.json:
{
  "google_places_api_key": "AIzaSyBu...KAMUBARU",
  "google_maps_api_key": "AIzaSyBu...KAMUBARU",
  "credentials": {
    "google_places": "AIzaSyBu...KAMUBARU",
    "google_maps": "AIzaSyBu...KAMUBARU"
  }
}
```

---

## ✅ TES APA API KEY WORKS:

```bash
# Test via curl (ganti dengan API key kamu):
curl -s "https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurant%20in%20Jakarta&key=AIzaSyBu...KAMUBARU" | python3 -m json.tool | head -20
```

Kalau berhasil, kamu should see restaurants data.

---

## ⚠️ PERINGATAN:

1. **JANGAN share API key ini dengan siapapun!**
2. **API Key punya quota** - cek di Google Cloud Console → "APIs & Services" → "Quotas"
3. **Places API (New) punya 1,000 free requests/day**

---

## 🎯 KASIH TAU KE AKU:

Setelah kamu fix, reply ke aku dengan:
1. API key baru kamu (aku akan simpan secure)
2. Atau "API key uda dipasang" kalau kamu sudah setup via option 1/2/3

Aku akan:
- ✅ Baca API key baru
- ✅ Fix script untuk pakai Places API (New)
- ✅ Test real scraping
- ✅ Deploy FULL campaign dengan real data
- ✅ Send emails otomatis
- ✅ Post ke social media otomatis
- ✅ Setup tracking
- ✅ Bisa kamu jalanin tanpa usaha!

---

**Sekarang, fix API key dulu, kasih tau ke aku.** 👍