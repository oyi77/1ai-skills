---
name: implementing-network-traffic-baselining
description: Build network traffic baselines from NetFlow/IPFIX data using Python pandas for statistical analysis, z-score
  anomaly detection, and hourly/daily traffic pattern profiling
domain: cybersecurity
subdomain: network-security
tags:
- netflow
- ipfix
- traffic-analysis
- baselining
- anomaly-detection
- pandas
- network-monitoring
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-03
- PR.DS-02
---

# Implementing Network Traffic Baselining

## Overview

Network traffic baselining establishes normal communication patterns by analyzing historical NetFlow/IPFIX data to create statistical profiles of expected behavior. This skill uses Python pandas to compute hourly and daily traffic distributions, per-host byte/packet counts, protocol ratios, and top-N talker profiles. Anomalies are detected using z-score thresholds and IQR (interquartile range) outlier methods, enabling SOC analysts to identify deviations such as data exfiltration spikes, beaconing patterns, and unusual port usage.


## When to Use
**Trigger phrases:**
- "implementing network traffic baselining"
- "Build network traffic baselines from NetFlow/IPFIX data using Python pandas for "


- When deploying or configuring implementing network traffic baselining capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites

- NetFlow v5/v9 or IPFIX flow data exported as CSV or JSON
- Python 3.8+ with pandas and numpy libraries
- Historical flow data (minimum 7 days recommended for baseline)

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

1. Ingest NetFlow/IPFIX records from CSV or JSON exports
2. Compute hourly and daily traffic volume distributions (bytes, packets, flows)
3. Build per-source-IP baseline profiles with mean, median, standard deviation
4. Calculate protocol and port distribution baselines
5. Apply z-score anomaly detection to identify statistical outliers
6. Flag flows exceeding IQR-based thresholds as potential anomalies
7. Generate baseline report with anomaly alerts

## Expected Output

JSON report containing traffic baselines (hourly/daily profiles), per-host statistics, detected anomalies with z-scores, and top talker rankings with deviation indicators.
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
- Capturing traffic on networks without authorization or privacy considerations
- Leaving packet captures containing sensitive data unencrypted on disk
- Deploying inline blocking rules without testing for false positives first
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Captures verified as complete with no dropped packets
- Detection rules tested against known-benign traffic for false positive rate
- Alert thresholds validated and tuned to reduce noise

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |