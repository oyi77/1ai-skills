---
name: browser-use
description: Browser automation with AI — Playwright, Puppeteer, browser-use library. Navigate, extract, interact with web pages autonomously
---

## Overview

Browser automation enables AI agents to interact with web pages like humans — navigating, clicking, typing, and extracting data. This skill covers Playwright, Puppeteer, and the browser-use library for autonomous web interaction, including anti-detection techniques.

## Capabilities

- Navigate websites and extract structured data
- Fill forms, click buttons, handle multi-step flows
- Take screenshots and analyze page content
- Handle authentication flows (login, 2FA, CAPTCHAs)
- Manage multiple tabs and browser contexts
- Bypass basic anti-bot detection
- Capture network requests and responses

## When to Use

- Web scraping where APIs aren't available
- Automating repetitive web tasks (form filling, data entry)
- Testing web applications (E2E flows)
- AI agents that need to browse the internet
- Monitoring websites for changes
- Screenshot-based UI testing

## Pseudo Code

### Playwright — Basic Navigation + Extraction
```javascript
const { chromium } = require('playwright');

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
});
const page = await context.newPage();

// Navigate and wait for content
await page.goto('https://example.com', { waitUntil: 'networkidle' });

// Extract data
const title = await page.textContent('h1');
const links = await page.$$eval('a[href]', (els) =>
  els.map(el => ({ text: el.textContent, href: el.href }))
);

// Screenshot
await page.screenshot({ path: 'page.png', fullPage: true });

await browser.close();
```

### Playwright — Form Filling + Login
```javascript
const page = await context.newPage();

// Navigate to login
await page.goto('https://app.example.com/login');

// Fill credentials
await page.fill('input[name="email"]', 'user@example.com');
await page.fill('input[name="password"]', process.env.PASSWORD);
await page.click('button[type="submit"]');

// Wait for navigation after login
await page.waitForURL('**/dashboard');
console.log('Logged in, URL:', page.url());
```

### Playwright — Multi-Tab Handling
```javascript
const context = await browser.newContext();

// Open multiple pages in same context (shares cookies)
const page1 = await context.newPage();
const page2 = await context.newPage();

await page1.goto('https://app.example.com');
await page2.goto('https://api.example.com/docs');

// Switch between tabs
await page1.bringToFront();
```

### Playwright — Network Interception
```javascript
// Intercept API requests
await page.route('**/api/data**', (route) => {
  const response = route.request();
  console.log('API call:', response.url());
  route.continue();
});

// Mock API responses
await page.route('**/api/users', (route) => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{ id: 1, name: 'Test User' }]),
  });
});
```

### Puppeteer — Screenshot Analysis
```javascript
const puppeteer = require('puppeteer');

const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080 });

await page.goto('https://example.com');

// Take screenshot for AI analysis
const screenshot = await page.screenshot({ encoding: 'base64', fullPage: true });

// Send to vision model for analysis
const analysis = await analyzeWithVision(screenshot);
console.log('Page content:', analysis);
```

### browser-use Library (Python)
```python
from browser_use import Agent
from langchain_openai import ChatOpenAI

agent = Agent(
    task="Find the latest blog post on example.com and summarize it",
    llm=ChatOpenAI(model="gpt-4o"),
)

result = await agent.run()
print(result)
```

## Common Patterns

### Wait for Dynamic Content
```javascript
// Wait for specific element
await page.waitForSelector('.results-list', { timeout: 10000 });

// Wait for network idle
await page.waitForLoadState('networkidle');

// Wait for specific response
await page.waitForResponse(resp =>
  resp.url().includes('/api/') && resp.status() === 200
);
```

### Anti-Detection
```javascript
const context = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
  viewport: { width: 1920, height: 1080 },
  locale: 'en-US',
  timezoneId: 'America/New_York',
});

// Stealth plugin
await page.addInitScript(() => {
  Object.defineProperty(navigator, 'webdriver', { get: () => false });
  window.chrome = { runtime: {} };
});
```

### Error Handling
```javascript
try {
  await page.goto('https://example.com', { timeout: 30000 });
  await page.waitForSelector('.content', { timeout: 10000 });
} catch (err) {
  if (err.message.includes('timeout')) {
    console.log('Page took too long to load');
    await page.screenshot({ path: 'error.png' });
  }
  throw err;
} finally {
  await browser.close();
}
```

### Parallel Page Processing
```javascript
const pages = await Promise.all([
  context.newPage(),
  context.newPage(),
  context.newPage(),
]);

await Promise.all(
  pages.map((page, i) => page.goto(`https://example.com/page/${i + 1}`))
);

const results = await Promise.all(
  pages.map(page => page.textContent('h1'))
);
```
