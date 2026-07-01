---
name: hunting-for-cobalt-strike-beacons
description: Detect Cobalt Strike beacon network activity using default TLS certificate signatures (serial 8BB00EE), JA3/JA3S/JARM
  fingerprints, HTTP C2 profile pattern matching, beacon jitter analysis, and named pipe detection via Zeek, Suricata, and
  Python PCAP analysis.
domain: cybersecurity
subdomain: threat-hunting
tags:
- cobalt-strike
- beacon
- threat-hunting
- c2
- zeek
- suricata
- ja3
- jarm
- network-forensics
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
- DE.AE-02
- DE.AE-07
- ID.RA-05
---

# Hunting for Cobalt Strike Beacons

## Overview

Cobalt Strike is the most prevalent command-and-control framework used by both red teams and threat actors. Beacon, its primary payload, communicates with team servers using configurable HTTP/HTTPS/DNS profiles that can mimic legitimate traffic. However, default configurations and behavioral patterns remain detectable through TLS certificate analysis (default serial 8BB00EE), JA3/JA3S fingerprinting, beacon interval jitter analysis, and HTTP malleable profile pattern matching. This skill covers building detection capabilities using Zeek network logs, Suricata IDS rules, and Python-based PCAP analysis to identify beacon callbacks in network traffic.


## When to Use
**Trigger phrases:**
- "hunting for cobalt strike beacons"
- "Detect Cobalt Strike beacon network activity using default TLS certificate signa"


- When investigating security incidents that require hunting for cobalt strike beacons
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Zeek 6.0+ with JA3 and HASSH packages installed
- Suricata 7.0+ with Emerging Threats ruleset
- Python 3.9+ with scapy and dpkt libraries
- Network traffic captures (PCAP) or live Zeek logs
- RITA (Real Intelligence Threat Analytics) for beacon scoring
- Threat intelligence feeds with known Cobalt Strike IOCs

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
### Step 1: TLS Certificate Analysis
Detect default Cobalt Strike certificates using JA3S fingerprints, certificate serial numbers, and JARM fingerprints in Zeek ssl.log.

### Step 2: Beacon Interval Analysis
Analyze connection timing patterns to identify regular callback intervals with configurable jitter, characteristic of beacon behavior.

### Step 3: HTTP Profile Detection
Match HTTP request patterns (URI paths, headers, user-agents) against known malleable C2 profiles.

### Step 4: Correlate and Score
Combine multiple indicators (TLS + timing + HTTP profile) into a composite beacon confidence score.

## Expected Output

JSON report containing detected beacon candidates with confidence scores, TLS fingerprints, timing analysis, HTTP profile matches, and recommended response actions.
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