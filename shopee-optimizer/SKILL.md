---
name: shopee-optimizer
description: Shopee product management automation - listings, pricing, inventory, and order processing
---

# Shopee Optimizer Skill 🛍️

**Production-ready** automation untuk Shopee product management & optimization.

## 🎯 Features

- **Product listing automation** - Create/edit listings in bulk
- **Price monitoring** - Track competitor prices & auto-adjust
- **Stock management** - Sync inventory across variants
- **Order processing** - Auto-fulfill orders with templates
- **Analytics tracking** - Views, clicks, conversion rates
- **SEO optimization** - Auto-generate optimized titles & descriptions

## 📦 Files

```
shopee-optimizer/
├── SKILL.md              # This file
├── script.sh             # Main automation (cross-platform)
├── script.ps1            # Windows PowerShell version
├── config.json           # Configuration (shop details, pricing rules)
├── templates/            # Listing templates
└── assets/               # Product images, logos
```

## 🔧 Setup

### 1. Configure Credentials

Edit `config.json`:
```json
{
  "shop": {
    "shopId": "your-shop-id",
    "apiKey": "your-shopee-api-key",
    "partnerId": "your-partner-id",
    "secret": "your-secret"
  },
  "pricing": {
    "autoAdjust": true,
    "minMargin": 0.15,
    "competitorCheckInterval": 3600
  },
  "inventory": {
    "lowStockThreshold": 10,
    "autoReorder": false
  }
}
```

### 2. Run the Skill

```bash
# List all products (Linux/macOS)
./script.sh --list

# Update prices based on competitors
./script.sh --update-prices

# Bulk upload products from CSV
./script.sh --upload csv/products.csv

# Generate SEO-optimized listings
./script.sh --optimize-seo
```

**Windows (PowerShell):**
```powershell
.\script.ps1 -List
.\script.ps1 -UpdatePrices
```

## 🔄 How It Works

### Flow:
1. **Authenticate** - Connect to Shopee Open Platform API
2. **Fetch data** - Get current products, orders, analytics
3. **Analyze** - Check competitor prices, stock levels, performance
4. **Optimize** - Apply pricing rules, update listings
5. **Sync** - Update inventory, process orders
6. **Report** - Generate performance summary

## 📊 API Endpoints Used

- `/api/v2/product/get` - Fetch product list
- `/api/v2/product/update` - Update product info
- `/api/v2/order/get` - Fetch orders
- `/api/v2/order/ship` - Mark as shipped
- `/api/v2/shop/get` - Shop analytics

## 🛠️ Troubleshooting

### API Rate Limit?

Shopee API has rate limits. The skill automatically:
- Queues requests
- Retries with exponential backoff
- Logs rate limit status

### Product Upload Failed?

- Check image formats (JPG, PNG, max 5MB)
- Verify category IDs match Shopee's taxonomy
- Ensure required fields are filled

## ⚠️ Warnings

- **API Limits**: Respect Shopee's rate limits (varies by endpoint)
- **Price Wars**: Don't engage in race-to-bottom pricing
- **Data Accuracy**: Verify auto-generated content before publishing

## 🚀 Next Steps

Planned improvements:
- [ ] AI-powered product description generation
- [ ] Image optimization & compression
- [ ] Multi-shop management
- [ ] Integration with suppliers for auto-reorder
- [ ] Chatbot for customer inquiries

---
**Berkah Karya** ⚡ | Part of 1ai-skills collection
