---
name: super-browser
description: Use when the ultimate browser automation framework combining the best
  of 8 top-rated browser skills for unified local or cloud-based web task automation.
  Use when working with super browser.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
- analysis
- browser
- investigation
- research
- super
version: 1.0.0
category: research
---

# Super Browser

## When to Use

**Trigger phrases:**
- "super browser"
- "Help me with super browser"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


**The ultimate browser automation framework.** Combines the best of 8 top-rated browser skills.

---


## When NOT to Use

- When the answer is already known and documented
- For time-sensitive decisions that cannot wait for thorough research
- When the topic is outside your domain of competence


## Overview

Super Browser enables thorough investigation with structured methodology.

Super Browser is a comprehensive browser automation framework for AI agents, combining stealth browsing, multi-page orchestration, network interception, and cross-platform execution. It unifies the capabilities of Playwright (Python) and Puppeteer (Node.js) under a single methodology, enabling agents to navigate JavaScript-heavy SPAs, extract structured data from dynamic content, bypass bot detection with fingerprint rotation, and persist authentication state across sessions.

The framework covers the full automation lifecycle: browser provisioning and configuration, stealth hardening against fingerprinting and CAPTCHA, reliable selectors with smart waiting strategies, network request interception for API-level data extraction, session management with cookie/localStorage persistence, and error recovery with retry logic. It supports headless execution for CI/CD pipelines, headed mode for visual debugging, and remote browser orchestration via CDP (Chrome DevTools Protocol) for cloud deployments.

Key capabilities include: cross-browser support (Chromium, Firefox, WebKit), mobile viewport emulation, file upload/download handling, multi-tab and iframe context switching, WebSocket interception, PDF and screenshot generation, and integration with stealth plugins to avoid Cloudflare Turnstile, reCAPTCHA, and bot management platforms. Whether used for regression testing, web scraping, social media automation, or e-commerce monitoring, Super Browser provides a battle-tested foundation for production browser automation.


## Workflow

```python
# Example: Automated browser task with error handling
async def safe_navigate(page, url, retries=3):
    for attempt in range(retries):
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            return True
        except Exception as e:
            if attempt == retries - 1:
                raise
            await page.wait_for_timeout(2000 * (attempt + 1))
    return False
```

1. **Target definition** — Identify the URL, selectors, and data points needed. Decide between static content (DOM) and dynamic content (XHR/fetch interception).
2. **Browser launch** — Start Chromium/Firefox with appropriate args: headless mode, proxy, stealth flags, and viewport configuration.
3. **Navigation and wait** — Navigate with explicit wait conditions (`networkidle`, `domcontentloaded`). Wait for key elements before interacting.
4. **Interaction** — Click, type, scroll, and submit forms as needed. Use `page.keyboard`, `page.mouse`, and `page.evaluate` for complex interactions.
5. **Data capture** — Extract text content, attributes, screenshots, PDFs, and network response bodies. Store in structured format (dict, JSON, CSV).
6. **Session management** — Handle cookies, localStorage, and authentication state. Reuse sessions across runs via storage state persistence.
7. **Cleanup** — Close the browser context and browser instance. Release temporary files and report any unhandled errors.

## Network Interception

```python
# Python — intercept and inspect API responses
async def intercept_api(page):
    responses = []
    page.on("response", lambda resp: responses.append({
        "url": resp.url,
        "status": resp.status,
        "json": resp.json() if "application/json" in resp.headers.get("content-type", "") else None
    }) if resp.status >= 400 else None)
    await page.goto("https://example.com")
    return responses
```

```javascript
// JavaScript — block images and fonts for speed
await page.setRequestInterception(true);
page.on('request', (req) => {
    if (['image', 'font', 'media'].includes(req.resourceType()))
        req.abort();
    else
        req.continue();
});
```


## Source Evaluation

- **Authority** — Is the source credible and expert?
- **Currency** — Is the information recent and relevant?
- **Objectivity** — Is there bias or conflict of interest?
- **Accuracy** — Can claims be verified independently?

## Output Format

- Executive summary (1-2 paragraphs)
- Key findings (bullet points)
- Detailed analysis (sections with evidence)
- Recommendations (actionable next steps)
- Sources and methodology

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "First result is good enough" | Deep research finds better answers. Keep digging. |
| "I do not need to verify sources" | Unverified sources lead to wrong conclusions. Always cross-check. |
| "Research is a one-time thing" | Markets change. Research needs to be continuous, not one-off. |
| "A single user agent and viewport is fine" | Sites fingerprint browser properties. Rotate user agents, viewport dimensions, and screen properties per session. |
| "Headless mode is undetectable" | Modern bot detectors identify headless Chromium via navigator.webdriver and missing Chrome extensions. Use stealth plugins. |
| "wait_for(seconds) is reliable enough" | Fixed sleeps are brittle and slow. Use explicit wait conditions (wait_for_selector, wait_for_url, wait_for_function) instead. |



## Code Examples

### Python (Playwright)

```python
import asyncio
from playwright.async_api import async_playwright

async def scrape_page(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")
        title = await page.title()
        screenshot = await page.screenshot(full_page=True)
        links = await page.eval_on_selector_all(
            "a[href]",
            "els => els.map(e => ({text: e.innerText, href: e.href}))"
        )
        await browser.close()
        return {"title": title, "links": links, "screenshot_size": len(screenshot)}

result = asyncio.run(scrape_page("https://example.com"))
print(f"Title: {result['title']}, Links found: {len(result['links'])}")
```

### JavaScript (Puppeteer)

```javascript
import puppeteer from 'puppeteer';

async function scrapePage(url) {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });
    await page.goto(url, { waitUntil: 'networkidle0' });

    const title = await page.title();
    const links = await page.evaluate(() =>
        Array.from(document.querySelectorAll('a[href]')).map(a => ({
            text: a.innerText,
            href: a.href
        }))
    );
    const screenshot = await page.screenshot({ fullPage: true });

    await browser.close();
    return { title, links, screenshot: screenshot.length };
}

scrapePage('https://example.com')
    .then(data => console.log(data))
    .catch(err => console.error(err));
```

## Setup & Configuration

### Python Installation

```bash
pip install playwright
playwright install chromium          # Download Chromium browser binary
playwright install-deps chromium     # Install system dependencies (Linux)
```

### Node.js Installation

```bash
npm install puppeteer                 # Bundles Chromium by default
npm install puppeteer-core            # Use with existing browser binary
npx puppeteer browsers install chrome # Download browser separately
```

### Advanced Configuration

```python
# playwright_stealth.py — Stealth plugin for anti-detection
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def stealth_browser():
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()
    await stealth_async(page)
    return page, browser
```

```javascript
// puppeteer-extra with stealth plugin
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
```

## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| `TimeoutError: waiting for selector` | Replace `page.wait_for(5000)` with `page.wait_for_selector("css=...", timeout=10000)`. Use `wait_until="networkidle"` on navigation calls. |
| Browser fails to launch in CI/headless | Install missing system deps via `playwright install-deps chromium`. On Docker use `mcr.microsoft.com/playwright` as base image. |
| Site detects automation and blocks | Use `playwright-stealth` or `puppeteer-extra-plugin-stealth`. Rotate user agents, viewports, and add random mouse movements between steps. |
| Memory grows unbounded over time | Always call `await browser.close()` in a `finally` block. Limit concurrency with a semaphore. Create one context per task, not per navigation. |
| Page navigation returns NS_ERROR_CONNECTION_REFUSED | Check proxy configuration. Set `ignore_https_errors=True` for self-signed certs. Pass `--proxy-server` in Chromium launch args. |
| Popup windows and new tabs not captured | Handle with a `page.on("popup")` listener before the trigger action. Close unexpected pages in a background task. |
| Session cookies not persisting between runs | Use `browser_context.storage_state(path="state.json")` to save and `browser.new_context(storage_state="state.json")` to restore. |

## Monetization

1. **Headless browser API service** — Offer a paid API for website screenshots, PDF generation, and structured data extraction. Tiered pricing per 1,000 requests with caching and concurrency limits.
2. **E-commerce intelligence** — Build automated price monitoring, stock checking, and competitor analysis dashboards for online retailers. Monthly subscription per tracked product catalog.
3. **Social media automation** — Develop and sell account management bots (content scheduling, auto-engagement, analytics) for agencies managing 50+ client accounts across platforms.
4. **Regression testing SaaS** — Provide visual regression testing: compare full-page screenshots across deploys, alert on UI drift, integrate with GitHub Actions and GitLab CI.
5. **Web scraping consulting** — Build custom data pipelines for real estate listings, job boards, product catalogs, and market research. One-time build fee plus monthly maintenance retainer.

## Process

1. **Environment setup** — Install Playwright/Puppeteer, configure proxy and stealth options, set viewport and user agent.
2. **Script development** — Write navigation flows with explicit waits, network interception, and DOM extraction logic.
3. **Dry-run validation** — Execute against a test URL with headless mode off to visually verify behavior against live DOM.
4. **Stealth hardening** — Enable stealth plugins, rotate fingerprints, add random delays between actions to avoid bot detection.
5. **Data extraction** — Collect screenshots, PDFs, network logs, and structured data from page content via selectors and JS evaluation.
6. **Error recovery** — Implement retry loops, fallback selectors, and graceful degradation for flaky elements and timeouts.
7. **Delivery** — Format extracted data (JSON, CSV, screenshots) and document any anomalies encountered during runs.

## Verification

- [ ] Playwright/Puppeteer scripts execute without errors on target URLs
- [ ] Element selectors validated against actual DOM, not stale snapshots
- [ ] Network interception captures all expected requests and responses
- [ ] Screenshots and PDFs render correctly across target viewport sizes
- [ ] Error handling covers timeouts, navigation failures, and missing elements
- [ ] Session cookies and localStorage persist correctly across navigations
- [ ] Stealth measures verified against fingerprinting detection sites
- [ ] Scripts handle modals, popups, and unexpected dialogs gracefully