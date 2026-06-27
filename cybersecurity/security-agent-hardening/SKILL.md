---
name: security-agent-hardening
description: Secure AI agents against prompt injection, jailbreaking, data exfiltration, and supply chain attacks. Implement
  guardrails, sandboxing, and monitoring for safe autonomous operation.
domain: cybersecurity
tags:
- agent-security
- prompt-injection
- guardrails
- sandboxing
- llm-security
- ai-safety
---
# Security Agent Hardening

## Overview

Cybersecurity skill for security agent hardening. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "Harden this agent against attacks"
- "Implement guardrails for autonomous agents"
- "Prevent prompt injection in my system"
- "Sandbox agent execution"
- "Audit agent security"
- "Secure LLM applications"

**Use cases:**
- Production AI agent deployment
- Customer-facing chatbots
- Autonomous code generation
- Multi-agent systems
- Tool-using agents (MCP, function calling)

**When NOT to use:**
- Internal research agents with no external input
- Fully human-in-the-loop systems
- Agents without tool access


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Access to relevant log sources and security tools
- Understanding of agent hardening fundamentals
- Appropriate permissions for data access and tool operation

## Workflow

```python
# Example: IOC detection
import re

IOC_PATTERNS = {
    "ip": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "domain": r"\b[a-z0-9-]+\.[a-z]{2,}\b",
    "hash_md5": r"\b[a-f0-9]{32}\b",
    "hash_sha256": r"\b[a-f0-9]{64}\b",
}

def extract_iocs(text: str) -> dict:
    return {k: re.findall(v, text) for k, v in IOC_PATTERNS.items()}
```

1. **Define Objectives** — Clarify the goals and scope for agent hardening.
2. **Gather Resources** — Collect tools, data, and access needed for agent hardening.
3. **Execute Process** — Carry out agent hardening operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All agent hardening procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |