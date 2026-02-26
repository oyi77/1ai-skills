---
name: kalodata-integrations
description: Multi-platform integrations for Kalodata research. Connect Shopify for product listings, Notion for research reports, and Slack for alerts + daily digests. CLI-friendly with config-based API key management.
metadata:
  model: sonnet
---

# Kalodata Integrations Skill

Multi-platform connections for Kalodata research automation.

## Use This Skill When

- User wants to create Shopify product listings from TikTok Shop research
- User needs to save research reports to Notion databases
- User wants Slack alerts for new products and daily digests
- User prefers CLI-based integration management
- User needs secure API key configuration (not hardcoded)

## Do Not Use This Skill When

- User only needs basic research (use kalodata-product-research)
- User needs real-time monitoring (use kalodata-monitor)
- Task is unrelated to Kalodata/TikTok Shop research

## Quick Start

### Configuration

Create a `.kalodata-integrations` config directory:

```bash
mkdir -p ~/.kalodata-integrations
```

Create `config.json` with your API credentials:

```json
{
  "shopify": {
    "shopUrl": "your-store.myshopify.com",
    "accessToken": "your_admin_api_access_token"
  },
  "notion": {
    "apiKey": "your_notion_api_key",
    "databaseId": "your_research_reports_database_id"
  },
  "slack": {
    "webhookUrl": "https://hooks.slack.com/services/xxx/xxx/xxx",
    "defaultChannel": "#research-alerts"
  }
}
```

Or use environment variables:

```bash
export SHOPIFY_SHOP_URL=your-store.myshopify.com
export SHOPIFY_ACCESS_TOKEN=your_token
export NOTION_API_KEY=your_notion_key
export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx
```

### Basic Usage

```typescript
import { createIntegrations, loadConfig } from './index.js';

const config = loadConfig();
const integrations = createIntegrations(config);

// Shopify: Create product listing from research
const listing = await integrations.shopify.createListing({
  title: 'Trending Beauty Product',
  description: 'High-demand TikTok viral product',
  price: 29.99,
  images: ['https://example.com/image.jpg'],
  tags: ['viral', 'beauty', 'trending']
});

// Notion: Save research report
const page = await integrations.notion.createResearchReport({
  title: 'Beauty Category Analysis',
  category: 'Beauty',
  products: researchProducts,
  insights: analysis,
  date: new Date()
});

// Slack: Send alert
await integrations.slack.sendAlert({
  type: 'new_product',
  product: { name: 'Viral Lip Gloss', revenue: 15000 },
  channel: '#alerts'
});

// Slack: Send daily digest
await integrations.slack.sendDigest({
  date: new Date(),
  totalProducts: 45,
  newProducts: 12,
  topPerformers: topProducts,
  channel: '#daily-digest'
});
```

### CLI Usage

```bash
# Set up configuration
node index.js config --set shopify --url your-store.myshopify.com --token your_token
node index.js config --set notion --key your_key --database your_db_id
node index.js config --set slack --webhook https://hooks.slack.com/xxx

# Shopify operations
node index.js shopify list
node index.js shopify create --title "Product Name" --price 29.99 --description "Description"

# Notion operations
node index.js notion list
node index.js notion create --title "Research Report" --category "Beauty"

# Slack operations
node index.js slack alert --message "New trending product found!"
node index.js slack digest

# Run all integrations
node index.js sync
```

## Core Features

### 1. Shopify Integration

Create product listings from TikTok Shop research data:

```typescript
interface ShopifyConfig {
  shopUrl: string;
  accessToken: string;
}

interface ProductListing {
  title: string;
  description: string;
  price: number;
  compareAtPrice?: number;
  images: string[];
  tags: string[];
  vendor?: string;
  productType?: string;
  status?: 'active' | 'draft' | 'archived';
  variants?: {
    price: number;
    compareAtPrice?: number;
    inventoryQuantity?: number;
    sku?: string;
  }[];
}
```

**Methods:**
- `createListing(product)` - Create new product
- `updateListing(id, updates)` - Update existing product
- `deleteListing(id)` - Remove product
- `listProducts(options)` - List products with filters
- `getProduct(id)` - Get single product details

### 2. Notion Integration

Save and organize research reports in Notion:

```typescript
interface NotionConfig {
  apiKey: string;
  databaseId: string;
}

interface ResearchReport {
  title: string;
  category: string;
  products: ProductSnapshot[];
  insights: string;
  date: Date;
  tags?: string[];
  opportunityScore?: number;
}
```

**Methods:**
- `createResearchReport(report)` - Create new report page
- `updateReport(pageId, updates)` - Update existing report
- `listReports(options)` - List reports with filters
- `getReport(pageId)` - Get single report
- `searchReports(query)` - Search reports by keyword

### 3. Slack Integration

Send alerts and daily digests:

```typescript
interface SlackConfig {
  webhookUrl: string;
  defaultChannel?: string;
}

interface AlertOptions {
  type: 'new_product' | 'threshold_cross' | 'opportunity' | 'custom';
  product?: ProductSnapshot;
  message?: string;
  channel?: string;
  urgency?: 'high' | 'normal' | 'low';
}

interface DigestOptions {
  date: Date;
  totalProducts: number;
  newProducts: number;
  topPerformers: ProductSnapshot[];
  categoryBreakdown?: Record<string, number>;
  channel?: string;
}
```

**Methods:**
- `sendAlert(options)` - Send immediate alert
- `sendDigest(options)` - Send daily digest
- `sendMessage(message, channel)` - Send custom message
- `formatProductCard(product)` - Format product for Slack
- `testConnection()` - Verify webhook works

## Configuration

### Config File Location

Default: `~/.kalodata-integrations/config.json`

Or specify custom path:
```bash
export KALOADATA_INTEGRATIONS_CONFIG=/path/to/config.json
```

### Config Schema

```typescript
interface IntegrationsConfig {
  shopify?: ShopifyConfig;
  notion?: NotionConfig;
  slack?: SlackConfig;
  defaults?: {
    productStatus?: 'active' | 'draft';
    digestSchedule?: 'daily' | 'weekly';
    alertUrgency?: 'high' | 'normal' | 'low';
  };
}
```

### Environment Variable Priority

Environment variables override config file values:

| Config Field | Environment Variable |
|--------------|---------------------|
| shopify.shopUrl | SHOPIFY_SHOP_URL |
| shopify.accessToken | SHOPIFY_ACCESS_TOKEN |
| notion.apiKey | NOTION_API_KEY |
| notion.databaseId | NOTION_DATABASE_ID |
| slack.webhookUrl | SLACK_WEBHOOK_URL |

## CLI Commands

### Configuration

| Command | Description |
|---------|-------------|
| `config` | Show current configuration |
| `config --set <platform> [options]` | Set credentials for platform |
| `config --validate` | Validate all credentials |

### Shopify

| Command | Description |
|---------|-------------|
| `shopify list` | List all products |
| `shopify create [options]` | Create new product listing |
| `shopify update <id> [options]` | Update product |
| `shopify delete <id>` | Delete product |

### Notion

| Command | Description |
|---------|-------------|
| `notion list` | List research reports |
| `notion create [options]` | Create new report |
| `notion search <query>` | Search reports |
| `notion get <pageId>` | Get report details |

### Slack

| Command | Description |
|---------|-------------|
| `slack alert [options]` | Send immediate alert |
| `slack digest` | Send daily digest |
| `slack test` | Test Slack connection |

### Integration

| Command | Description |
|---------|-------------|
| `sync` | Run full sync: research → Shopify + Notion |
| `sync shopify` | Sync products to Shopify |
| `sync notion` | Save reports to Notion |

## Examples

### Create Product from Research

```bash
node index.js shopify create \
  --title "Viral LED Mask" \
  --price 45.99 \
  --description "TikTok trending beauty product" \
  --tags "viral,beauty,trending" \
  --images "https://example.com/mask.jpg"
```

### Save Research Report

```bash
node index.js notion create \
  --title "Weekly Beauty Analysis" \
  --category "Beauty" \
  --products "45" \
  --insights "Strong upward trend in skincare"
```

### Send Alert

```bash
node index.js slack alert \
  --type "new_product" \
  --product-name "Lip Plumper" \
  --revenue "25000" \
  --urgency "high"
```

### Full Sync Workflow

```bash
# Export credentials
export SHOPIFY_SHOP_URL=your-store.myshopify.com
export SHOPIFY_ACCESS_TOKEN=your_token
export NOTION_API_KEY=your_key
export SLACK_WEBHOOK_URL=https://hooks.slack.com/xxx

# Run full sync
node index.js sync
```

## Output Format

CLI output is designed for human readability:

```
🔗 Kalodata Integrations

📋 Configuration:
   ✅ Shopify: your-store.myshopify.com
   ✅ Notion: Connected to Research Database
   ✅ Slack: #research-alerts

🛍️ Shopify:
   Created product: Viral LED Mask (gid://shopify/1234567890)

📓 Notion:
   Created report: Weekly Beauty Analysis (page_id: abc123)

📣 Slack:
   Alert sent successfully to #research-alerts

✅ Full sync completed in 2.3s
```

## Dependencies

This skill integrates with:
- kalodata-product-research: Core research data
- kalodata-monitor: Monitoring and alerts
- kalodata-research-automation: Full workflow

## Error Handling

All integrations include error handling:

```typescript
try {
  await integrations.shopify.createListing(product);
} catch (error) {
  if (error.code === 'SHOPIFY_AUTH_ERROR') {
    console.error('Invalid Shopify credentials');
  } else if (error.code === 'SHOPIFY_RATE_LIMIT') {
    // Retry with backoff
  }
}
```

## Rate Limits

- Shopify: 40 requests/second (API), 2 requests/second (GraphQL)
- Notion: 3 requests/second
- Slack: 1 request/second per webhook

The integration handles rate limiting automatically with exponential backoff.
