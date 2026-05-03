# Affiliate Master

Full-stack affiliate marketing automation for OpenClaw agents. Generate, track, and optimize affiliate links with FTC-compliant disclosures.

## What It Does

AffiliateMaster handles the entire affiliate marketing workflow from link generation to revenue tracking, with built-in FTC compliance.

## Quick Usage Example

```bash
# Install skill
clawhub install affiliate-master

# Edit config file
~/.openclaw/skills/affiliate-master/config.json

// Use JavaScript API
const products = await affiliateMaster.searchProduct('wireless headphones');
const link = await affiliateMaster.generateLink({
  network: 'amazon',
  product: products[0]
});

// Enhance content with affiliate links
const enhanced = await affiliateMaster.enhanceContent(content, {
  autoInsert: true,
  disclosurePlacement: 'top'
});
```

## Key Features

- 🔗 Multi-network support (Amazon, ShareASale, CJ, Impact)
- 📊 Click tracking and analytics dashboard
- ✅ Automatic FTC disclosure injection
- 📝 Platform-specific formatting (blog, social, email)
- ⚡ Link shortening and branding
- 🚀 Auto-detect affiliate link opportunities
- 🔍 Compliance audit logs

## Category

**Marketing / Monetization / Affiliate**

## Keywords

affiliate marketing, FTC compliance, revenue tracking