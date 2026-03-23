# 🛍️ Shopee Affiliate Promo Automation

## ✅ Yang Sudah Di-Setup

### 1. Akun Tersimpan
| Platform | Akun | Status |
|----------|------|--------|
| Shopee Affiliate | griyadalaman | ✅ Ready |
| Shopee Affiliate | kak_niluh (Meta Ads) | ✅ Ready |
| Facebook | ID: 100056956485990 | ✅ Ready |
| Holink | ho.link/racunshopeediskon | ✅ Ready |
| PostBridge | 83 accounts | ✅ Ready |

### 2. File Yang Dibuat
```
skills/shopee-affiliate-promo/
├── SKILL.md              # Dokumentasi skill
├── README.md             # File ini
├── config.json           # Konfigurasi semua akun
├── templates/
│   └── captions.json     # Template caption viral
├── scripts/
│   ├── add_product.py    # Tambah produk
│   └── post_to_social.py # Post ke sosmed
└── data/
    └── products.json     # List produk (sample)
```

### 3. Holink Setup
- URL: https://ho.link/racunshopeediskon
- Header: "🛍️ PRODUK SHOPEE TERLARIS"
- 1 Web Link (sample)

---

## 🚀 Cara Pakai

### Step 1: Tambah Produk
Buka Shopee Affiliate Dashboard, pilih produk, copy affiliate link:
```bash
cd ~/.openclaw/workspace/skills/shopee-affiliate-promo
python3 scripts/add_product.py "https://shope.ee/xxxxx" "Nama Produk" "99000" "gadget"
```

### Step 2: Post ke Social Media
```bash
python3 scripts/post_to_social.py --platform facebook --account "WARZ"
```

### Step 3: Update Holink
Buka https://app.holink.com/links dan tambah link produk baru.

---

## 📱 Akun PostBridge Tersedia

### Facebook (38 akun)
- WARZ, Mavigadget house, MrBeast, LankyBox, dll

### Instagram (11 akun)
- berkahkaryadigitalproduct, riviewprodukcek, nyamiresepdapur, dll

### TikTok (11 akun)
- bkjaya00, riviewprodukfashionjujur, massehatyuk, dll

### YouTube (9 akun)
- Resep Dapur Nyami, Diskon Hunter, dll

---

## 📝 Template Caption Viral

10 hook yang tersedia:
1. "🔥 DISKON GILA! {product} cuma Rp{price}!"
2. "⚠️ Jangan beli {product} sebelum liat ini..."
3. "Shopee ERROR?! {product} harga Rp{price} aja!"
4. "Lagi cari {category}? Ini rekomendasi terbaik!"
5. "REVIEW JUJUR: {product} worth it gak sih?"
... dan 5 lagi di templates/captions.json

---

## ⚠️ Yang Perlu Dilakukan Manual

1. **Tambah produk asli** - Buka affiliate.shopee.co.id, generate affiliate link, tambah ke products.json
2. **Update Holink** - Tambah link produk ke ho.link/racunshopeediskon
3. **Pilih akun posting** - Tentukan akun mana yang mau dipakai untuk promosi

---

## 💡 Tips Income Besar

1. **Volume**: 50-100 post/hari across multiple akun
2. **High Ticket**: Fokus produk komisi tinggi (elektronik, gadget, fashion)
3. **Viral Hook**: Pakai template caption yang sudah disediakan
4. **Multi-Platform**: Post ke FB + IG + TikTok + YouTube
5. **Konsisten**: Posting di jam prime time (07:00, 12:00, 19:00)

---

*Created: 2026-03-13*
*By: Vilona AI*
