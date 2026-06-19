---
name: polymarket-analyst
description: "Analyze Polymarket prediction markets for expected value, market inefficiencies, and trading opportunities."
domain: research
---
persona:
  name: "Domain Expert"
  title: "Master of Polymarket Analyst"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Polymarket Analyst

Analyze Polymarket predictions, calculate expected value, and identify trading opportunities.

## Required Tools

Tools and dependencies needed before using this skill.


### MCP Servers

```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@firecrawl/mcp-server"],
      "env": { "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}" }
    },
    "exa": {
      "command": "npx",
      "args": ["-y", "@exa/mcp-server"],
      "env": { "EXA_API_KEY": "${EXA_API_KEY}" }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" }
    }
  }
}
```

## Authentication

Authentication setup required for external service access.


### Setup

1. **Firecrawl** (Web Scraping)
   ```bash
   export FIRECRAWL_API_KEY="your-key"
   ```

2. **Exa** (AI Search)
   ```bash
   export EXA_API_KEY="your-key"
   ```

3. **Slack** (Alerts)
   ```bash
   export SLACK_BOT_TOKEN="xoxb-your-token"
   ```

## Pseudo Code

Implementation patterns for common use cases with this skill.


### Example 1: Market Discovery and Filtering

```typescript
// 1. Fetch trending markets
const markets = await polymarket.getMarkets({
  limit: 100,
  status: "open"
});

// 2. Filter by liquidity
const liquid = markets.filter(m => m.volume > 50000);

// 3. Get news context for each
for (const market of liquid.slice(0, 20)) {
  const news = await exa.search(market.question, {
    numResults: 3,
    category: "news"
  });
  
  console.log(`${market.question}: ${news.length} related articles`);
}
```

### Example 2: Calculate Implied Probability and EV

```typescript
// 1. Get current price
const price = await polymarket.getPrice(marketId); // e.g., 0.30

// 2. Calculate implied probability
const impliedProb = price; // 30%

// 3. Calculate expected value
function calculateEV(price, trueProb, fee = 0.02) {
  const netWin = (1 - fee) - price;
  const netLoss = -price;
  return (trueProb * netWin) + ((1 - trueProb) * netLoss);
}

// 4. Assess opportunity
const trueProb = 0.45; // Your estimate
const ev = calculateEV(price, trueProb);

if (ev > 0.05) {
  console.log(`Strong buy! EV: ${(ev * 100).toFixed(1)}%`);
}
```

### Example 3: Watchlist Monitoring with Alerts

```typescript
// 1. Load watchlist
const watchlist = await notion.query("Polymarket Watchlist");

// 2. Monitor each market
for (const market of watchlist) {
  const current = await polymarket.getPrice(market.id);
  const change = Math.abs(current - market.targetPrice);
  
  // Alert on significant movement
  if (change > market.threshold) {
    await slack.alert({
      channel: "#trading-alerts",
      text: `🚨 ${market.question} moved ${change * 100}% to ${current * 100}%`
    });
  }
}
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `polymarket markets --volume 50000` | List liquid markets |
| `polymarket price <market-id>` | Get current price |
| `polymarket analyze <market-id>` | Full EV analysis |

## Error Handling

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `AUTH_001` | Invalid API key | Check keys |
| `API_001` | Polymarket API error | Retry later |
| `DATA_001` | Insufficient data | Skip market |

## Common Patterns

Reusable patterns that appear frequently when applying this skill.


### EV Calculation with Fees

```typescript
function calculateEV(price, estimatedProb, fee = 0.02) {
  const spread = fee * price;
  const effectivePrice = price + spread;
  
  const winReturn = 1 - effectivePrice;
  const lossReturn = -effectivePrice;
  
  return (estimatedProb * winReturn) + ((1 - estimatedProb) * lossReturn);
}
```

### Position Sizing

```typescript
function calculatePositionSize(bankroll, ev, kellyFraction = 0.25) {
  const fraction = (ev * kellyFraction) / 1;
  return bankroll * fraction;
}
```

---
*Skill v2.0 - Polymarket Analyst*

## When NOT to Use

- When the prediction market analysis is used for financial advice requiring licensing
- When the markets involve prohibited categories in the user's jurisdiction
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Probability estimates are not calibrated against historical outcomes
- Agent does not account for liquidity and market maker spreads
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Probability estimates are calibrated against historical resolution data
- [ ] Liquidity and spread costs are factored into expected value calculations
- [ ] All required outputs generated
- [ ] Success criteria met

