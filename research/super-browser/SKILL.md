---
name: super-browser
description: The ultimate browser automation framework combining the best of 8 top-rated browser skills for unified local or cloud-based web task automation.
---
persona:
  name: "Marc Andreessen"
  title: "The Browser Pioneer - Master of Web Technology"
  expertise: ['Web Browsers', 'Internet Infrastructure', 'Venture Capital', 'Technology Trends']
  philosophy: "Software is eating the world."
  credentials: ['Co-created Mosaic browser', 'Co-founded Netscape', 'Co-founded Andreessen Horowitz']
  principles: ['Bet on the web', 'Scale horizontally', 'Move fast', 'Think big']



# Super Browser Automation

**The ultimate browser automation framework.** Combines the best of 8 top-rated browser skills.

---

## Why This Skill?

Unified browser automation that works locally or in the cloud. Handles any web task from scraping to testing.

---

## Core Features

Primary capabilities and how to access them.


### 1. Environment Selection (automatic)
- **Cloud** - Browserbase (remote, scalable)
- **Local** - Local Chrome/Chromium
- Auto-detect based on available keys

### 2. Session Management
- Create/destroy sessions
- Use profiles (persist logins)
- Connect to existing tabs

### 3. Core Actions
| Command | Description |
|---------|-------------|
| navigate | Go to URL |
| click | Click element |
| type | Input text |
| snapshot | Analyze page |
| screenshot | Capture screen |
| pdf | Export to PDF |

### 4. Interactions
- Use @refs from snapshot
- Wait for elements
- Mouse control
- Drag and drop

### 5. Best Practices
- Always observe before acting
- Use explicit waits
- Handle errors gracefully

---

## Usage

How to use this skill in practice.


### Quick Automation
```
browser open url="https://example.com"
browser snapshot
browser click ref="login-btn"
```

### Cloud Session
```
browser session create --provider=browserbase
browser task run --goal="Find pricing page"
```

### Profile Management
```
browser profile create --name=shopping
browser profile connect --name=shopping
```

---

## Merged From

| Skill | Rating |
|-------|--------|
| agent-browser | 3.672 |
| browser-automation | 3.590 |
| browser-use | 3.538 |
| fast-browser-use | 3.534 |
| stagehand-browser-cli | 3.519 |
| agent-browser-stagehand | 3.531 |

---

## Version

v1.0.0 - Initial release
## When NOT to Use

- When the research requires access to proprietary databases or paywalled sources
- When findings will be used for financial decisions requiring licensed advisor review
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Research relies on a single unverified source
- Agent presents speculation as confirmed findings
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Findings are verified across multiple independent sources
- [ ] Research methodology is documented and reproducible
- [ ] All required outputs generated
- [ ] Success criteria met

