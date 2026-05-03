# Super Browser - Unified Browser Automation

## What It Does

Super Browser is the ultimate browser automation framework that combines the best features from 8 top-rated browser skills. Works locally (Chrome/Chromium) or in the cloud (Browserbase) for any web task — scraping, testing, form filling, and more.

## Quick Usage Example

```bash
# Quick automation pattern
browser open url="https://example.com"
browser snapshot
browser click ref="login-btn"
browser type ref="username" text="myuser"
browser click ref="submit"
```

## Key Features

### Environment Selection (Automatic)
- **Cloud**: Browserbase for remote, scalable automation
- **Local**: Auto-detects Chrome/Chromium installations
- Zero configuration — picks best environment automatically

### Core Actions
- `navigate` — Go to URL
- `click` — Click elements by ref
- `type` — Input text into fields
- `snapshot` — Analyze page structure
- `screenshot` — Capture screen
- `pdf` — Export to PDF

### Session Management
- Create/destroy sessions
- Profile management (persist logins)
- Connect to existing tabs
- @refs from snapshot for stable targeting

### Best Practices Built In
- Always observe before acting
- Explicit waits for elements
- Graceful error handling
- Mouse control and drag-and-drop support

## Merged From Top Skills

| Skill | Rating |
|-------|--------|
| agent-browser | 3.672 |
| browser-automation | 3.590 |
| browser-use | 3.538 |
| fast-browser-use | 3.534 |
| stagehand-browser-cli | 3.519 |
| agent-browser-stagehand | 3.531 |

## Version

v1.0.0 — Initial release