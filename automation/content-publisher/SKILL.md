---
name: content-publisher
description: Automates drafting and publishing articles to Substack and Medium with SEO optimization, editorial calendars,
  and cross-platform distribution.
domain: automation
author: oyi77
license: Apache-2.0
subdomain: workflow-automation
tags:
- automation
- content
- productivity
- publisher
- seo
- workflow
version: 1.0.0
---
# Content Publisher

## When to Use

**Trigger phrases:**
- "content publisher"
- "Help me with content publisher"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Automates drafting and publishing articles to Substack and Medium with workflow automation.


## When NOT to Use

- For one-off tasks that will never repeat
- When the process requires human judgment at every step
- When the cost of automation exceeds the cost of manual execution


## Overview

Content Publisher automates workflow automation to reduce manual effort and increase reliability.

## Workflow

```python
# Example: Workflow automation
import schedule
import time

def run_workflow():
    data = fetch_data()
    processed = transform(data)
    deliver(processed)

schedule.every().hour.do(run_workflow)
while True:
    schedule.run_pending()
    time.sleep(60)
```

1. **Define triggers** — Set up events or schedules that initiate the automation
2. **Configure inputs** — Specify data sources and parameters
3. **Design pipeline** — Define the sequence of automated steps
4. **Add error handling** — Set up retries, alerts, and fallback paths
5. **Test end-to-end** — Validate the full automation with realistic data
6. **Deploy and monitor** — Activate and track performance


## Code Examples

### Python: Medium Draft
```python
import os, requests

def publish_medium(title, body, tags):
    token = os.environ["MEDIUM_TOKEN"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    user = requests.get("https://api.medium.com/v1/me", headers=headers).json()["data"]["id"]
    payload = {"title": title, "contentFormat": "markdown", "content": body,
               "tags": tags[:5], "publishStatus": "draft"}
    resp = requests.post(f"https://api.medium.com/v1/users/{user}/posts", headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["data"]["url"]
```

### Node.js: WordPress Post
```javascript
export async function publishWP(title, content, tags) {
  const auth = Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString("base64");
  const resp = await fetch(`${process.env.WP_URL}/wp-json/wp/v2/posts`, {
    method: "POST", headers: { Authorization: `Basic ${auth}`, "Content-Type": "application/json" },
    body: JSON.stringify({ title, content, status: "draft", tags }),
  });
  if (!resp.ok) throw new Error(`WP ${resp.status}`);
  return (await resp.json()).link;
}
```

## Configuration

- Set trigger conditions (schedule, webhook, event)
- Define input validation rules
- Configure notification channels for alerts
- Set retry policies and timeout limits

## Best Practices

- Start with simple automations and iterate
- Add logging at every step for debugging
- Use idempotent operations where possible
- Test with edge cases before deploying

## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| Medium 403 Forbidden | Token expired. Regenerate in Settings → Security → Integration tokens. |
| Substack draft missing | Session cookie expires ~24h. Re-authenticate and extract fresh `SUBSTACK_SESSION`. |
| WordPress 401 Unauthorized | Wrong app password or URL. Verify `WP_URL` ends with `/wp-json/wp/v2/`. |
| Cross-post formatting differs | Unsupported Markdown features. Strip footnotes and uncommon extensions before dispatch. |
| Medium tag limit (max 5) | API rejects >5 tags. Truncate to `tags[:5]` in the request payload. |

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Manual is faster for one-off tasks" | One-off tasks become recurring. Automate early, save time later. |
| "I will add error handling later" | You never do. Handle errors from day one. |
| "Automation is overkill" | If you do it twice, automate it. If you do it daily, it is critical infrastructure. |


## Process

1. **Research** — Analyze target audience, competitors, and trending topics
1. **Create** — Generate content following brand guidelines and best practices
1. **Publish & Optimize** — Distribute to target platforms, track performance, iterate

## Monetization

- **Content syndication service** — Offer automated cross-publishing to bloggers and small businesses. Google Doc or Markdown → Substack + Medium + WP.
- **Newsletter arbitrage** — Repurpose top Medium articles to a paid Substack newsletter; auto-forward new Substack posts back to Medium for discovery traffic.
- **SEO content agency** — Combine automated publishing with SEO analysis as a "write once, rank everywhere" retainer service for clients.
- **Publishing templates & scripts** — Sell reusable publishing workflows, editorial calendar templates, and API integration scripts as digital products.

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings