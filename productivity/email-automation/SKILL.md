---
name: email-automation
description: Automate email workflows, templates, and campaigns with Gmail integration
category: productivity
tags: [email, automation, gmail, productivity, mcp]
---

# Email Automation

Automate email workflows, create templates, and manage campaigns using Gmail and MCP integrations.

## Overview

This skill provides comprehensive email automation capabilities including template management, bulk sending, tracking, and integration with CRM systems.

## Capabilities

### Email Templates
- Create reusable email templates
- Variable substitution and personalization
- HTML and plain text support
- Template versioning

### Bulk Operations
- Send personalized bulk emails
- Schedule email campaigns
- Track open and click rates
- Manage unsubscribes

### Workflow Automation
- Auto-respond to specific emails
- Filter and label incoming mail
- Forward based on rules
- Archive and cleanup

### Integration
- Sync with CRM systems
- Connect to marketing platforms
- Export analytics data
- Webhook notifications

## MCP Integration

### Nineteen Blocks Sales Automation
Comprehensive sales automation integrating Gmail, Google Sheets, Streak CRM, Notion, and Google Drive.

**Features**:
- Email tracking and analytics
- CRM synchronization
- Document automation
- Multi-tool workflow integration

## Usage Examples

### Send Personalized Campaign
```
Send a personalized email campaign to all leads in "Q1 Prospects" spreadsheet:
- Subject: "Exclusive Offer for {{company_name}}"
- Use template: "product-launch"
- Track opens and clicks
- Schedule for Monday 9 AM
```

### Auto-Respond Setup
```
Create an auto-responder for support@company.com:
- Trigger: New email with subject containing "urgent"
- Response: Use "urgent-support-template"
- CC: support-team@company.com
- Create ticket in tracking system
```

## Best Practices

1. **Compliance**: Follow CAN-SPAM and GDPR regulations
2. **Deliverability**: Maintain good sender reputation
3. **Testing**: A/B test subject lines and content
4. **Segmentation**: Target specific audience segments
5. **Analytics**: Track and optimize campaign performance

## Requirements

- Gmail or Google Workspace account
- API credentials
- MCP server configured
- Email sending limits understood

## Related Skills

- `productivity/google-workspace` - Google Workspace integration
- `sales/sales-strategy` - Sales email campaigns
- `marketing/marketing-strategy` - Marketing automation
