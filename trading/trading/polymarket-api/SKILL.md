---
name: polymarket
description: Query Polymarket prediction markets. Use for questions about prediction markets, betting odds, market prices, event probabilities, or when user asks about Polymarket data.
---
persona:
  name: "Domain Expert"
  title: "Master of Polymarket Api"
  expertise: ['Trading Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']



> [![Tip Me](https://www.tip.md/badge.svg)](https://www.tip.md/oyi77) — If this skill saves you time, tip: **https://www.tip.md/oyi77**

# Polymarket

Query prediction market data from Polymarket's public API (no auth required).

## Quick Start

```bash
# Top markets by 24h volume
python3 scripts/polymarket.py --top

# Search markets
python3 scripts/polymarket.py --search "trump"

# Get specific market by slug
python3 scripts/polymarket.py --slug "will-trump-win-the-2024-election"

# List events (grouped markets)
python3 scripts/polymarket.py --events
```

## Script Location

`skills/polymarket/scripts/polymarket.py`

## API Endpoints

The script uses `gamma-api.polymarket.com`:
- `/markets` - Individual markets with prices, volumes
- `/events` - Event groups containing related markets

## Output Format

Markets show: question, Yes/No prices (as percentages), 24h volume, total volume.

## Interpreting Prices

- `outcomePrices` are 0-1 representing probability
- Price of 0.65 for "Yes" = market thinks 65% chance of Yes
- Higher volume = more liquid, more reliable signal

## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met


Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).
