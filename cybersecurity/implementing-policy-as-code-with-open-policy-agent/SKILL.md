---
name: implementing-policy-as-code-with-open-policy-agent
description: 'This skill covers implementing Open Policy Agent (OPA) and Gatekeeper for policy-as-code enforcement in Kubernetes
  and CI/CD pipelines. It addresses writing Rego policies, deploying OPA Gatekeeper as a Kubernetes admission controller,
  testing policies in development, and integrating policy evaluation into deployment pipelines.

  '
domain: cybersecurity
tags:
- devsecops
- cicd
- opa
- gatekeeper
- policy-as-code
- kubernetes
- secure-sdlc
subdomain: devsecops
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- GOVERN-1.1
- MEASURE-2.7
- MANAGE-3.1
nist_csf:
- PR.PS-01
- GV.SC-07
- ID.IM-04
- PR.PS-04
---
# Implementing Policy As Code With Open Policy Agent

## Overview

Cybersecurity skill for implementing policy as code with open policy agent. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "implementing policy as code with open policy agent"
- "This skill covers implementing Open Policy Agent (OPA) and Gatekeeper for policy"


- When enforcing organizational security policies across Kubernetes clusters programmatically
- When requiring admission control that blocks non-compliant resources from being created
- When implementing policy governance that can be version-controlled, tested, and audited
- When standardizing security rules across multiple clusters and environments
- When needing a flexible policy engine that extends beyond Kubernetes to APIs and CI/CD

**Do not use** for vulnerability scanning (use Trivy/Checkov), for runtime threat detection (use Falco), or for network policy enforcement (use Kubernetes NetworkPolicy or Calico).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Kubernetes cluster with admin access for Gatekeeper installation
- Helm for Gatekeeper deployment
- OPA CLI or conftest for local policy testing
- Rego knowledge for policy authoring

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

1. **Assess Requirements** — Evaluate current environment and define policy as code implementation requirements.
2. **Design Architecture** — Plan the policy as code architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up open policy agent for policy as code according to vendor best practices and security guidelines.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **open policy agent** — Primary tool for this skill
- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All policy as code procedures executed completely and documented
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