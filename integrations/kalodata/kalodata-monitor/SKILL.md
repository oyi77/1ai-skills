---
name: kalodata-monitor
description: Scheduled research runs with auto-alerts for NEW viral products. Runs
  on configurable schedule (hourly/daily/weekly), detects new products by comparing
  with previous runs, alerts on revenue threshold crossings, and sends notifications
  via Slack webhook.
metadata:
  model: sonnet
domain: integrations
---

# Kalodata Monitor Skill

Scheduled research automation with intelligent new product detection and Slack alerts.

## Overview

Enables scheduled research automation with intelligent new product detection and Slack alerts. Runs on configurable schedules (hourly/daily/weekly), detects new products by comparing with previous runs, alerts on revenue threshold crossings, and sends notifications via Slack webhook.

## When to Use

- User wants continuous monitoring of TikTok Shop product categories
- User needs automatic detection of NEW products entering the market
- User wants alerts when products cross revenue thresholds
- User prefers Slack notifications for urgent product discoveries
- User needs scheduled research runs without manual intervention

## The Process

1. **Configure monitoring profile** – Set up profile with category, goal, schedule, and Slack webhook
2. **Set alert conditions** – Define revenue thresholds and other alert criteria
3. **Run or schedule monitoring** – Execute profile manually or let it run on schedule
4. **Review alerts** – Check Slack for notifications and new product findings
5. **Take action** – Investigate new products and make business decisions

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Expecting real-time monitoring (this skill runs on scheduled intervals, not streaming)
- Using this for one-time research tasks (use kalodata-research-automation instead)
- Monitoring unrelated categories or markets (stick to TikTok Shop Indonesia)
- Ignoring alert configuration (alerts without thresholds are just noise)

## Verification

- Monitor profile saves without errors and loads on subsequent runs
- New products are correctly detected by comparing with previous run data
- Slack alerts send successfully and appear in configured channel
- Revenue threshold alerts trigger when products cross configured limits
- Scheduled runs execute without manual intervention

## Do Not Use This Skill When

- User only needs one-time research (use kalodata-research-automation)
- User needs real-time product tracking (this is scheduled, not real-time)
- Task is unrelated to TikTok Shop Indonesia market monitoring

## Quick Start
This section covers quick start for the kalodata-monitor skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Basic Usage

```typescript
import { createMonitor, loadMonitorConfig, createProfile } from './index.js';

const config = loadMonitorConfig('./.kalodata-monitor');
const monitor = createMonitor(config);

const profile = createProfile({
  id: 'beauty-trending',
  name: 'Beauty Trending',
  category: 'Beauty',
  goal: 'trending',
  schedule: 'daily',
  slackWebhook: 'https://hooks.slack.com/services/xxx',
});

monitor.saveProfile(profile);
const result = await monitor.runProfile('beauty-trending');
console.log(`Found ${result.newProducts.length} new products`);
```

### CLI Usage

```bash
# Set credentials
export KALODATA_SESSION=your_session
export KALODATA_CF_CLEARANCE=your_cf_clearance

# List profiles
node index.js list

# Add a new monitor
node index.js add "Beauty Trends" Beauty trending daily

# Run a specific profile
node index.js run profile-123

# Run all enabled profiles
node index.js run
```

## Core Features
- Core operation execution with comprehensive error handling
- Input validation and output quality assurance
- Integration with existing workflows and toolchains
- Detailed logging for debugging and audit trails


### 1. Monitor Profiles

Each profile defines what to monitor and when:

```typescript
interface MonitorProfile {
  id: string;
  name: string;
  category: string;      // Product category name or ID
  goal: string;         // Research goal (trending, emerging, etc.)
  schedule: 'hourly' | 'daily' | 'weekly';
  alerts: AlertCondition;
  topProducts?: number; // Default: 20
  slackWebhook?: string;
  enabled?: boolean;
}
```

### 2. Alert Conditions

Configure when to trigger notifications:

```typescript
interface AlertCondition {
  revenueMin?: number;              // Absolute revenue threshold
  revenueGrowthMultiplier?: number;  // Multiplier vs previous run
  opportunityScoreMin?: number;       // Minimum opportunity score (0-100)
  revenueCrosses?: number;            // Alert when crossing this revenue
}
```

### 3. New Product Detection

Automatically compares current run with previous run to identify:
- Products that didn't exist in the last run
- Products crossing revenue thresholds
- Products with rising opportunity scores

### 4. Slack Notifications

Rich Slack messages with:
- Profile summary
- New products list with key metrics
- Revenue threshold crossings
- Click-through to product details

### 5. Data Persistence

Stores in `.kalodata-monitor/` directory:
- `config.json` - All profile configurations
- `{profile-id}.json` - Previous run snapshots for comparison

## Configuration
```json
{
  "enabled": true,
  "autoRun": false,
  "timeout": 30000,
  "retries": 3
}
```

Set environment variables as needed for authentication and endpoints.


### Environment Variables

```bash
KALODATA_SESSION=your_session_cookie
KALODATA_CF_CLEARANCE=your_cf_clearance_token
```

### Profile Configuration

Create monitors via CLI or programmatically:

| Parameter | Description | Required |
|-----------|-------------|----------|
| id | Unique identifier | Yes |
| name | Display name | Yes |
| category | Product category | Yes |
| goal | Research goal | Yes |
| schedule | hourly/daily/weekly | Yes |
| slackWebhook | Slack webhook URL | No |

## CLI Commands

| Command | Description |
|---------|-------------|
| `list` | List all monitor profiles |
| `add <name> <category> <goal> <schedule> [webhook]` | Add new profile |
| `run [profile-id]` | Run profile or all profiles |
| `scheduled` | Run profiles due for their schedule |
| `remove <profile-id>` | Remove a profile |
| `enable <profile-id>` | Enable a profile |
| `disable <profile-id>` | Disable a profile |
| `config` | Show full configuration |

## Examples
```
# Basic usage
invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```


### Daily Beauty Trends Monitor

```bash
node index.js add "Daily Beauty" Beauty trending daily $SLACK_WEBHOOK
```

### Weekly Emerging Products

```bash
node index.js add "Weekly Emerging" Beauty emerging weekly
```

### Hourly High-Opportunity Products

```bash
node index.js add "Hourly High-Opp" Electronics trending hourly
```

## Integration with Research Automation

The monitor uses kalodata-product-research under the hood:

```typescript
const result = await monitor.runProfile(profileId);

// Result contains:
{
  profileId: string,
  products: ProductSnapshot[],      // All products from this run
  newProducts: ProductSnapshot[],    // NEW since last run
  crossedThreshold: ProductSnapshot[], // Products crossing thresholds
  alerts: Alert[],                   // Generated alerts
}
```

## Scheduling

For continuous monitoring, add to cron:

```bash
# Run every hour
0 * * * * cd /path/to/project && node index.js scheduled

# Run daily at 6 AM
0 6 * * * cd /path/to/project && node index.js scheduled
```

## Dependencies

This skill builds on:
- kalodata-product-research: Core research capabilities
- kalodata-research-automation: Full research workflow

## Output Format

CLI output is designed for human readability:

```
📋 Monitor Profiles:

  ✅ Beauty Trending
     Category: Beauty | Goal: trending | Schedule: daily
     Last run: 2/19/2026, 10:30:00 AM

🚀 Running all enabled profiles...

📊 Run Results:
  New products: 5
  Threshold crossings: 2
  Alerts: 3

✅ Slack notification sent successfully
```
