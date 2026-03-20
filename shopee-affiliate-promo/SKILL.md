# Shopee Affiliate Promo Automation

Automate Shopee affiliate product promotion across Facebook, Instagram, TikTok via PostBridge.

## Quick Start

```bash
# 1. Add products to promote
python3 scripts/add_product.py "https://shopee.co.id/product/xxx/yyy" "Nama Produk" "99000"

# 2. Generate captions
python3 scripts/generate_captions.py

# 3. Post to social media
python3 scripts/post_to_social.py --platform facebook --account "WARZ"
```

## Accounts Connected

### Shopee Affiliate
- **griyadalaman** (ID: 11392860738) - For organic promo
- **kak_niluh** (ID: 11317960507) - For Meta Ads

### Holink
- URL: https://ho.link/racunshopeediskon
- Email: grahainsanmandiri@gmail.com

### PostBridge (83 accounts)
- Facebook: 38 accounts
- Instagram: 11 accounts  
- TikTok: 11 accounts
- YouTube: 9 accounts
- Threads: 12 accounts

## Workflow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Add Product │ ──► │ Generate     │ ──► │ Post via    │
│ (manual/API)│     │ Caption+Link │     │ PostBridge  │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Update       │
                    │ Holink       │
                    └──────────────┘
```

## Content Types

1. **Slideshow** - Product images carousel
2. **AI Video** - Generated from product info
3. **Review UGC** - Buyer reviews/comments
4. **Random Mix** - Combination for variety

## Caption Templates

See `templates/captions.json` for viral caption formulas.
