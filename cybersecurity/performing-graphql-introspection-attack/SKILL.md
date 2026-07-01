---
name: performing-graphql-introspection-attack
description: Performs GraphQL introspection attacks to extract the full API schema including types, queries, mutations, subscriptions,
  and field definitions from GraphQL endpoints. The tester uses introspection queries to map the attack surface, identifies
  sensitive fields and mutations, tests for query depth and complexity limits, and exploits GraphQL-specific vulnerabilities
  including batching attacks, alias-based brute force, and nested query DoS.
domain: cybersecurity
tags:
- api-security
- graphql
- introspection
- schema-extraction
- query-abuse
subdomain: api-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
---
# Performing Graphql Introspection Attack

## Overview

Cybersecurity skill for performing graphql introspection attack. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "performing graphql introspection attack"
- "Performs GraphQL introspection attacks to extract the full API schema including "


- Testing GraphQL endpoints for exposed introspection that reveals the complete API schema
- Mapping the attack surface of a GraphQL API to identify sensitive queries, mutations, and types
- Testing for GraphQL-specific vulnerabilities including query depth abuse, batching attacks, and field-level authorization
- Assessing GraphQL implementations where introspection is disabled but schema can be reconstructed through error messages
- Evaluating defenses against resource exhaustion through deeply nested or complex GraphQL queries

**Do not use** without written authorization. Schema extraction and query abuse testing can impact service availability.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Written authorization specifying the GraphQL endpoint and testing scope
- Burp Suite Professional with InQL extension (v6.1+) for automated schema analysis
- Python 3.10+ with `requests` and `gql` libraries
- GraphQL Voyager or GraphQL Playground for schema visualization
- Clairvoyance tool for schema reconstruction when introspection is disabled
- Wordlists for GraphQL field and type name brute-forcing


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

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

1. **Plan Operations** — Define objectives, scope, and success criteria for graphql introspection attack operations.
2. **Prepare Environment** — Set up tools, access, and data sources required for graphql introspection attack.
3. **Execute Core Workflow** — Perform the graphql introspection attack operations following established procedures.
4. **Validate Results** — Verify that results meet quality standards and objectives.
5. **Report Findings** — Document results, observations, and recommendations.
6. **Follow Up** — Track remediation actions and verify fixes where applicable.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All graphql introspection attack procedures executed completely and documented
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