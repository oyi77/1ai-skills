---
name: shopee-optimizer
description: Shopee product management automation - listings, pricing, inventory, and order processing. Use when managing
  Shopee product listings, automating price adjustments based on competitors, syncing inventory across variants, processing
  orders with templates, tracking analytics, generating SEO-optimized content, or bulk uploading products from CSV files.
domain: marketing
tags:
- growth
- marketing
- optimizer
- seo
- shopee
---


# Shopee Optimizer Skill 🛍️

**Production-ready** automation untuk Shopee product management & optimization.

## Overview

Shopee Optimizer provides comprehensive automation for managing Shopee store operations. This skill handles product listings creation and editing, dynamic price monitoring and adjustment, inventory synchronization across product variants, automated order processing using customizable templates, performance analytics tracking, SEO-optimized content generation, and bulk operations for efficient store management. It serves as the single source of truth for all Shopee store operations automation.

## When to Use

- **Product listing automation**: Creating and editing listings in bulk via CSV upload
- **Price monitoring**: Tracking competitor prices and auto-adjusting your own prices
- **Inventory management**: Syncing stock levels across product variants
- **Order processing**: Auto-fulfilling orders using templates and workflows
- **Analytics tracking**: Monitoring views, clicks, conversion rates, and performance
- **SEO optimization**: Auto-generating optimized product titles and descriptions
- **Bulk uploads**: Processing multiple products from CSV or spreadsheet files
- **Competitor tracking**: Following competitor pricing and stock levels

## The Process

- Configure across, adjustments, analytics, automating, automation settings before first use


### Step 1: Authentication Setup

**Configuration**:
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

**Verification**:
1. Verify API credentials in Shopee Open Platform
2. Generate API key with full permissions
3. Test API connection via credentials test endpoint

### Step 2: Product Configuration

**Upload Product CSV**:
```bash
./script.sh --upload csv/products.csv
```

**CSV Format**:
```csv
product_name,description,category_id,price,stock,image_url
"Wireless Mouse","High-precision wireless mouse",123,29.99,50,"https://example.com/image.jpg"
```

**Validation Checklist**:
- [ ] All required columns present
- [ ] Category IDs match current Shopee taxonomy
- [ ] Images accessible and within size limits (max 5MB)
- [ ] Prices are positive numbers with 2 decimal places
- [ ] SKUs are unique if provided

### Step 3: Price Monitoring Setup

**Configure Competitor Tracking**:
```javascript
// Set up competitor monitoring
const competitors = [
  { name: "Store A", url: "https://shopee.com/store-a" },
  { name: "Store B", url: "https://shopee.com/store-b" }
];

// Schedule price checks
setInterval(async () => {
  for (const comp of competitors) {
    const prices = await fetchCompetitorPrices(comp.url);
    await adjustPrices(prices);
  }
}, 3600000); // Check every hour
```

### Step 4: Inventory Sync

**Sync Inventory Across Variants**:
```bash
./script.sh --sync-inventory
```

**Process**:
1. Fetch current stock levels from all variants
2. Compare against configured thresholds
3. Update low-stock products
4. Generate reorder alerts if configured

### Step 5: Order Processing

**Configure Auto-Fulfillment**:
```bash
./script.sh --process-orders --template shipping-template.json
```

**Template Example**:
```json
{
  "name": "Standard Shipping",
  "processing_time": "24h",
  "carrier": "JNE",
  "tracking_format": "JNE-####-####",
  "notification_message": "Your order has been shipped!"
}
```

### Step 6: Analytics Dashboard

**Generate Performance Report**:
```bash
./script.sh --analytics --range 30d
```

**Metrics Tracked**:
- Product views and clicks
- Conversion rates by product
- Average order value
- Top performing categories
- Stock turnover rates

### Step 7: SEO Optimization

**Generate Optimized Content**:
```bash
./script.sh --optimize-seo --products all
```

**SEO Elements Generated**:
- Keyword-rich product titles (100 chars max)
- Meta descriptions (160 chars max)
- Product description summaries
- Tag suggestions for categories

## Common Patterns

**Bulk Product Update**:
```bash
# Export current products
./script.sh --export csv/all-products.csv

# Modify CSV
# ... edit products ...

# Upload updates
./script.sh --upload csv/all-products.csv
```

**Price Maintenance**:
```bash
# Weekly scheduled task
0 0 * * 0 ./script.sh --update-prices --competitor-check --margin-min 0.15
```

**Inventory Alerts**:
```bash
# Check and alert on low stock
./script.sh --check-stock --threshold 10 --alert-admin
```

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Red Flags

- **❌ API rate limits being hit**: Shopee API rate limits exceeded - implement request queuing and backoff
- **❌ Price changes not applying**: Config errors or API authentication issues
- **❌ Inventory sync failures**: API rate limiting or network timeouts
- **❌ Order processing stuck in queue**: Template validation errors or missing data
- **❌ CSV upload fails validation**: Format issues or invalid category IDs
- **❌ Analytics data not updating**: API connection or permissions issues
- **❌ SEO generation returns empty**: Keyword extraction failures or template issues

## Verification

**Connection Tests**:
```bash
# Test API connectivity
./script.sh --test-api

# Verify authentication
./script.sh --verify-credentials
```

**Functional Verification**:

1. **Product Upload Test**:
   ```bash
   # Create test product
   ./script.sh --upload csv/test-product.csv
   
   # Verify in Shopee dashboard
   # Check product appears within 5 minutes
   ```

2. **Inventory Sync Test**:
   ```bash
   # Manually update stock in one variant
   ./script.sh --sync-inventory
   
   # Verify others update within 1 minute
   ```

3. **Order Processing Test**:
   ```bash
   # Simulate test order
   ./script.sh --process-orders --test
   
   # Check order status in dashboard
   ```

**API Endpoint Verification**:
```bash
# Check all endpoints are accessible
./script.sh --check-urls

# Expected output:
# ✓ /api/v2/product/get - OK
# ✓ /api/v2/product/update - OK
# ✓ /api/v2/order/get - OK
# ✓ /api/v2/order/ship - OK
# ✓ /api/v2/shop/get - OK
```

**Data Quality Checks**:
- [ ] All products show correct stock levels
- [ ] Prices match configured pricing rules
- [ ] Orders process without errors
- [ ] Analytics data matches Shopee dashboard
- [ ] SEO content includes relevant keywords

**Output Verification**:
```bash
# After any operation, verify output files
./script.sh --verify-output --file output.json

# Should return:
# ✓ File structure valid
# ✓ All required fields present
# ✓ Data quality checks passed
```

**Quick Health Check**:
```bash
echo "Shopee Optimizer Status"
echo "======================="
echo "API Connection: $(./script.sh --test-api 2>/dev/null && echo '✓ OK' || echo '✗ FAIL')"
echo "Products Count: $(./script.sh --count 2>/dev/null || echo 'Unknown')"
echo "Last Sync: $(date -r last_sync 2>/dev/null || echo 'Never')"
echo "API Rate Limit: $(./script.sh --rate-limit 2>/dev/null || echo 'Unknown')"
```

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
