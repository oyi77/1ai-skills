---
name: implementing-endpoint-detection-with-wazuh
description: Deploy and configure Wazuh SIEM/XDR for endpoint detection including agent management, custom decoder and rule
  XML creation, alert querying via the Wazuh REST API, and automated response actions.
domain: cybersecurity
subdomain: security-operations
tags:
- siem
- xdr
- wazuh
- endpoint-detection
- custom-rules
- incident-response
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- GOVERN-1.1
- MEASURE-2.7
- MANAGE-3.1
- MANAGE-2.4
- MEASURE-3.1
nist_csf:
- DE.CM-01
- RS.MA-01
- GV.OV-01
- DE.AE-02
---
# Implementing Endpoint Detection with Wazuh

## Overview

Wazuh is an open-source SIEM and XDR platform for endpoint monitoring, threat detection, and compliance. This skill covers managing agents via the Wazuh REST API, creating custom decoders and rules in XML for organization-specific detections, querying alerts, and testing rule logic using the logtest endpoint.


## When to Use
**Trigger phrases:**
- "implementing endpoint detection with wazuh"
- "Deploy and configure Wazuh SIEM/XDR for endpoint detection including agent manag"


- When deploying or configuring implementing endpoint detection with wazuh capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites

- Wazuh Manager 4.x deployed with API enabled
- Python 3.9+ with `requests` library
- API credentials (username/password for JWT authentication)
- Understanding of Wazuh decoder and rule XML syntax

## Steps

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

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### Step 1: Authenticate to Wazuh API
Obtain JWT token via POST to /security/user/authenticate.

### Step 2: List and Monitor Agents
Query agent status, versions, and last keep-alive via /agents endpoint.

### Step 3: Query Security Alerts
Search alerts by rule ID, severity, agent, or time range.

### Step 4: Test Custom Rules with Logtest
Use the /logtest endpoint to validate decoder and rule logic against sample log lines.

## Expected Output

JSON report with agent inventory, alert statistics, rule coverage, and logtest validation results.
## When NOT to Use

- You need to test the implementation (use performing-* skills)
- Task is about configuring existing tools (use configuring-* skills)
- You need to analyze security events (use analyzing-* skills)
- Task is about building detection rules (use building-* skills)
- You don't have access to the target environment
- Task requires vendor-specific expertise (consult vendor docs)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Acting on threat intelligence without validating source reliability
- Sharing classified or sensitive indicators without proper handling procedures
- Alerting threat actors to detection capabilities through visible response actions
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Results validated against known-good baselines or reference implementations
- Documentation complete enough for another analyst to reproduce findings

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |