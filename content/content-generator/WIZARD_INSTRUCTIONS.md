# Content Wizard — Agent Instructions
## Updated Flow (PM Optimized)
```
User kirim foto → Vision detect (FIXED ✅) → Pilih kategori/style/format
→ Generate image → Quality Gate (preview dulu) → User approve
→ I2V animate → Tambah BGM otomatis → Kirim hasil
```

## Kapan Aktifkan Wizard?
Aktifkan wizard ketika:
- User kirim **foto produk** tanpa instruksi spesifik
- User bilang "generate foto/video produk" 
- User tanya "bisa buatin konten untuk..."

## Flow Handler

### Step 1 — User kirim foto produk
```python
# 1. Jalankan vision detector
from vision_detector import detect_product
detected = detect_product(image_path)

# 2. Init wizard
from content_wizard import handle_image
result = handle_image(image_path, chat_id, detected)

# 3. Kirim ke Telegram dengan inline buttons
message(action="send", target=chat_id, message=result["text"], buttons=result["buttons"])
```

### Step 2 — User tap button (callback)
Callback format: `wiz:cat:minuman`, `wiz:style:splash`, `wiz:fmt:video_15s`, `wiz:generate`
```python
from content_wizard import handle_callback
result = handle_callback(callback_data, chat_id)

if result["action"] == "message":
    message(action="send", ..., buttons=result["buttons"])
elif result["action"] == "generate":
    # Kirim "lagi dimasak" message dulu
    # Jalankan generator di background
    run_generator(chat_id)
```

### Step 3 — Generate
```python
from content_wizard import get_final_prompt
config = get_final_prompt(chat_id)

# config berisi:
# - image_prompt: prompt siap pakai
# - i2v_prompt: animation prompt
# - image_model: model yang tepat
# - image_path: foto asli user
# - format: foto/video_15s/video_30s/tiktok_60s
```

## Tone Bahasa (User-Friendly!)
- ✅ "Hei! Foto produknya udah aku terima nih 🎉"
- ✅ "Hampir jadi! Gas generate? 🚀"  
- ✅ "Lagi dimasak nih... bentar ya! 🔥"
- ✅ "Mantap! Hasilnya udah keluar nih 🎉"
- ❌ JANGAN: "Silakan masukkan parameter", "Proses sedang berjalan"

## Contoh Full Response
Saat user kirim gambar:
> "Hei! Foto produknya udah aku terima nih 🎉
> Kayaknya ini **Minuman** ya? Kalau bener langsung lanjut,
> kalau salah pilih kategori di bawah 👇"
> [✅ Bener!] [🍔 Makanan] [💄 Beauty] ...

Saat generate selesai:
> "Nah, ini dia hasilnya! ✨
> Suka sama hasilnya? Mau coba style lain atau format beda?"
> [🔄 Coba Style Lain] [📤 Format Lain] [✅ Simpan]
