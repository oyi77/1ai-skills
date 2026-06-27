---
name: security-agent
description: Bug bounty hunter and security auditor. P1-P3 only. Direct execution (subagents refuse security testing).
domain: agents
tags:
- agent
- ai-agent
- automation
- orchestration
- testing
---
# Security Agent

## When to Use

**Trigger phrases:**
- "security agent"
- "Help me with security agent"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

curl -s -m 10 "https://TARGET" > pocs/evidence.html
curl -sI -m 5 "https://TARGET" > pocs/headers.txt

# Screenshots (Playwright)
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://TARGET', timeout=15000)
    page.wait_for_timeout(3000)
    page.screenshot(path='pocs/screenshot.png')
    browser.close()
"
```

## Overview

Security Agent is an AI agent skill for agent orchestration. It enables autonomous execution of complex tasks with minimal human intervention.

## Capabilities

- **Autonomous operation** — Execute multi-step security agent workflows independently
- **Context awareness** — Adapt behavior based on current state and history
- **Error recovery** — Handle failures gracefully with retry and fallback logic
- **Integration** — Connect with external tools and services as needed

## Workflow

1. **Initialize** — Set up the agent context and load required resources
2. **Plan** — Break down the task into executable steps
3. **Execute** — Run each step, monitoring for errors and adapting as needed
4. **Verify** — Validate results against acceptance criteria
5. **Report** — Summarize outcomes and suggest next steps

## Configuration

- Define task objectives and constraints clearly
- Set appropriate timeout and retry limits
- Configure tool access and permissions
- Enable logging for debugging and audit

