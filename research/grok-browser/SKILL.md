---
name: grok-browser
description: Use Grok's browser capabilities to search the web, analyze pages, and synthesize real-time information. Use when working with grok browser.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
- analysis
- browser
- grok
- investigation
- research
version: 1.0.0
---
# Grok Browser

## When to Use

**Trigger phrases:**
- "grok browser"
- "Help me with grok browser"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Query Grok (grok.com) via Chrome browser automation and copy responses.


## When NOT to Use

- When the answer is already known and documented
- For time-sensitive decisions that cannot wait for thorough research
- When the topic is outside your domain of competence


## Overview

Grok Browser combines x.ai's Grok LLM with real-time web search and browser automation to deliver deep, source-grounded research. Unlike static LLMs limited to training data, Grok can fetch live information from the web, analyze page content, and synthesize findings — making it a powerful tool for competitive intelligence, market research, technical investigation, and trend analysis. The skill supports two operation modes: the **Grok API** (production-grade, reliable, recommended) and **Playwright-based browser automation** (useful as a fallback or for interactive exploration on grok.com).

The full research lifecycle spans question formulation → query dispatch → source collection → cross-referencing → synthesis → delivery. Each query taps Grok's real-time web access through x.ai's API (grok-2-latest model with 128K context window), and the response includes citations to live sources that can be independently verified. This makes the workflow auditable and defensible — critical for professional research output.

Key capabilities include: real-time web search via LLM interface, structured citation extraction, multi-query decomposition for complex topics, browser-based fallback for API-unavailable scenarios, and a configurable output pipeline that can feed into reports, dashboards, or automated alerting systems. The Python and Node.js code examples in this skill cover both API and browser-automation approaches.

## Workflow

```python
# Example: Source evaluation
def evaluate_source(url: str) -> dict:
    return {
        "authority": check_domain_authority(url),
        "currency": get_last_updated(url),
        "objectivity": detect_bias(url),
        "accuracy": cross_reference(url),
    }
```

1. **Define question** — Clarify the research objective
2. **Gather sources** — Collect primary and secondary data
3. **Analyze** — Apply analytical frameworks to findings
4. **Synthesize** — Combine insights into actionable conclusions
5. **Present** — Deliver findings in clear, compelling format
6. **Archive** — Store research for future reference

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

## Code Examples

### Python — Grok API via requests

```python
import os
import requests


def grok_search(query: str, api_key: str | None = None) -> str:
    """Send a research query to Grok and return the response text."""
    key = api_key or os.environ["XAI_API_KEY"]
    resp = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "grok-2-latest",
            "messages": [
                {"role": "system", "content": "You are Grok, a research assistant with real-time web access."},
                {"role": "user", "content": f"Research this topic in depth: {query}"},
            ],
            "temperature": 0.7,
            "max_tokens": 4096,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


# Example
result = grok_search("latest breakthroughs in solid-state batteries 2026")
print(result)
```

### JavaScript / Node.js — Grok API via fetch

```javascript
import { env } from "node:process";

const XAI_API_KEY = env.XAI_API_KEY;

async function grokSearch(query) {
  const resp = await fetch("https://api.x.ai/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${XAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "grok-2-latest",
      messages: [
        { role: "system", content: "You are Grok, a research assistant with real-time web access." },
        { role: "user", content: `Research this topic in depth: ${query}` },
      ],
      temperature: 0.7,
      max_tokens: 4096,
    }),
  });
  if (!resp.ok) throw new Error(`Grok API error: ${resp.status} ${resp.statusText}`);
  const data = await resp.json();
  return data.choices[0].message.content;
}

// Example
const result = await grokSearch("AI agent frameworks comparison 2026");
console.log(result);
```

### Browser Automation (Playwright fallback)

When the API is unavailable or you need to interact with grok.com's chat UI directly:

```python
from playwright.sync_api import sync_playwright


def grok_browser_query(query: str) -> str:
    """Open grok.com in headless Chrome, submit query, return response."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://grok.com")
        page.wait_for_selector("textarea", timeout=15000)
        page.fill("textarea", query)
        page.press("textarea", "Enter")
        page.wait_for_timeout(3000)  # wait for streaming to finish
        result = page.evaluate("() => document.querySelector('.prose')?.innerText || document.body.innerText")
        browser.close()
        return result.strip()
```

**Note:** grok.com's DOM changes frequently — the browser route is a fallback. Prefer the API for production workflows.

## Setup & Configuration

### API Key

1. Sign in at [x.ai](https://x.ai) and navigate to the API keys section.
2. Create a new API key with the "Grok" scope.
3. Set it as an environment variable:

```bash
export XAI_API_KEY="xai-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Install Dependencies

**Python:**
```bash
pip install requests
# For browser automation fallback:
pip install playwright && playwright install chromium
```

**Node.js:**
```bash
npm install node-fetch       # Node < 18: polyfill
# or use native fetch (Node 18+)
npm install playwright       # for browser automation (optional)
```

### Verify Setup

```bash
curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"grok-2-latest","messages":[{"role":"user","content":"Hello"}],"max_tokens":50}' \
  | jq .
```

## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| `XAI_API_KEY` not found | Verify `echo $XAI_API_KEY` returns a value. Add to `.bashrc`/`.zshrc` or `.env` file with `export XAI_API_KEY=...` |
| HTTP 401 Unauthorized | Key may be expired or scoped incorrectly. Regenerate at [x.ai/api-keys](https://x.ai/api-keys) |
| HTTP 429 Rate Limited | Free tier: ~10 req/min. Add `time.sleep(6)` between calls or upgrade to Pro. Use exponential backoff on retry |
| HTTP 500 / timeout | Grok API may be degraded. Retry with backoff (2s, 4s, 8s). Switch to browser fallback as backup |
| Context window exceeded | Grok-2 supports 128K tokens. Chunk long research topics into sub-queries (3–5 focused questions) |
| browser automation finds no selector | grok.com changes frequently. Run `page.content()` to inspect current DOM. Prefer API for reliability |
| Response truncated | Increase `max_tokens` (default 4096, max 131072). Request `stream: false` for full response in one shot |

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "First result is good enough" | Deep research finds better answers. Keep digging. |
| "I do not need to verify sources" | Unverified sources lead to wrong conclusions. Always cross-check. |
| "Research is a one-time thing" | Markets change. Research needs to be continuous, not one-off. |
| "Browser automation is production-ready" | grok.com DOM changes constantly. Use the API for reliable automation. |
| "One query is enough" | Complex research needs multiple focused sub-queries for depth. |
| "The API response is the final answer" | Always cross-reference Grok's output against primary sources before acting on it. |


## Process

1. **Set up environment** — Install dependencies (`pip install requests` / `npm install node-fetch`), export `XAI_API_KEY`, verify connectivity with a test query.
2. **Formulate research question** — Decompose broad topics into 3–5 specific, answerable sub-questions. Each gets its own Grok query for focused results.
3. **Execute queries** — Dispatch queries to Grok API (preferred) or browser automation. Collect raw responses with source citations. Retry failed queries with exponential backoff.
4. **Synthesize findings** — Cross-reference Grok responses against known sources. Resolve contradictions, flag confidence levels, and extract actionable conclusions.
5. **Deliver and archive** — Format output per Output Format section. Store raw responses and final report for future reference and reproducibility.

## Verification

- [ ] Grok API returns valid JSON response for a test query
- [ ] API key is loaded from `XAI_API_KEY` env var (not hardcoded)
- [ ] Python and Node.js code examples execute without error
- [ ] Rate-limit handling tested (burst of 10+ rapid queries)
- [ ] Browser-automation fallback confirmed working (if using Playwright variant)
- [ ] Research output cross-referenced with at least one independent source
- [ ] Context window budget verified for long research queries
- [ ] Timeout configured appropriately for 30s+ research responses

## Monetization

- **Research-as-a-Service** — Offer automated Grok-powered deep research reports for startups, VCs, and executives at $200–$500/report. Grok's real-time web access makes it ideal for competitive landscaping, market sizing, and due diligence.
- **Browser automation SaaS** — Build a headless Grok query scheduler that emails daily research digests to subscribers. Charge $29–$99/month for recurring reports on custom topics.
- **Competitive intelligence feed** — Use Grok to monitor competitor announcements, product launches, and sentiment shifts. Sell weekly briefs to businesses in competitive industries (crypto, SaaS, e-commerce).
- **Content research engine** — Power a content marketing agency with Grok-sourced data and insights. Retainers at $1K+/month for ongoing research-backed blog posts, white papers, and social content.
- **API wrapper / middleware** — Package the Grok API into a simpler REST interface with caching, rate-limit handling, and multi-query batching. Sell as a micro-SaaS or open-source with paid enterprise features.