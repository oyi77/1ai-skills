---
name: analyzing-command-and-control-communication
description: 'Analyzes malware command-and-control (C2) communication protocols to understand beacon patterns, command structures,
  data encoding, and infrastructure. Covers HTTP, HTTPS, DNS, and custom protocol C2 analysis for detection development and
  threat intelligence. Activates for requests involving C2 analysis, beacon detection, C2 protocol reverse engineering, or
  command-and-control infrastructure mapping.

  '
domain: cybersecurity
tags:
- malware
- C2
- command-and-control
- beacon
- protocol-analysis
subdomain: malware-analysis
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- DE.AE-02
- RS.AN-03
- ID.RA-01
- DE.CM-01
---
# Analyzing Command And Control Communication

## Overview

Cybersecurity skill for analyzing command and control communication. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "analyzing command and control communication"
- "Analyzes malware command-and-control (C2) communication protocols to understand "


- Reverse engineering a malware sample has revealed network communication that needs protocol analysis
- Building network-level detection signatures for a specific C2 framework (Cobalt Strike, Metasploit, Sliver)
- Mapping C2 infrastructure including primary servers, fallback domains, and dead drops
- Analyzing encrypted or encoded C2 traffic to understand the command set and data format
- Attributing malware to a threat actor based on C2 infrastructure patterns and tooling

**Do not use** for general network anomaly detection; this is specifically for understanding known or suspected C2 protocols from malware analysis.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- PCAP capture of malware network traffic (from sandbox, network tap, or full packet capture)
- Wireshark/tshark for packet-level analysis
- Reverse engineering tools (Ghidra, dnSpy) for understanding C2 code in the malware binary
- Python 3.8+ with `scapy`, `dpkt`, and `requests` for protocol analysis and replay
- Threat intelligence databases for C2 infrastructure correlation (VirusTotal, Shodan, Censys)
- JA3/JA3S fingerprint databases for TLS-based C2 identification

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

1. **Scope the Analysis** — Define what command and control communication artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Parse and extract relevant command and control communication data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to command and control communication.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search


## Process

1. **Scope** — Define research questions, identify data sources, set time boundaries
1. **Gather** — Collect data from primary sources, APIs, and public records
1. **Synthesize** — Analyze findings, identify patterns, produce actionable report

## Verification

- [ ] All command and control communication procedures executed completely and documented
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