---
name: analyzing-network-traffic-for-incidents
description: 'Analyzes network traffic captures and flow data to identify adversary activity during security incidents, including
  command-and-control communications, lateral movement, data exfiltration, and exploitation attempts. Uses Wireshark, Zeek,
  and NetFlow analysis techniques. Activates for requests involving network traffic analysis, packet capture investigation,
  PCAP analysis, network forensics, C2 traffic detection, or exfiltration detection.

  '
domain: cybersecurity
tags:
- network-forensics
- PCAP-analysis
- Wireshark
- Zeek
- traffic-analysis
subdomain: incident-response
mitre_attack:
- T1071
- T1095
- T1573
- T1572
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- RS.MA-01
- RS.MA-02
- RS.AN-03
- RC.RP-01
---
# Analyzing Network Traffic For Incidents

## Overview

Cybersecurity skill for analyzing network traffic for incidents. Follows industry best practices and security standards.

## When to Use

- SIEM alerts on anomalous network traffic patterns requiring deeper investigation
- C2 beaconing is suspected and needs confirmation through packet-level analysis
- Data exfiltration volume or destination must be quantified from network evidence
- Lateral movement between systems needs to be traced through network connections
- An IDS/IPS alert requires packet-level validation to confirm or dismiss

**Do not use** for host-based forensic analysis (process execution, file system artifacts); use endpoint forensics tools instead.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Full packet capture (PCAP) infrastructure or on-demand capture capability (network tap, SPAN port)
- Wireshark installed on the analysis workstation with appropriate display filters knowledge
- Zeek (formerly Bro) deployed for network metadata generation (conn.log, dns.log, http.log, ssl.log)
- NetFlow/IPFIX collection from network devices for traffic flow analysis
- Network architecture diagram showing VLAN layout, firewall placement, and monitoring points
- Threat intelligence feeds for correlating observed network indicators

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

1. **Scope the Analysis** — Define what network traffic artifacts or data sources to examine and the investigation timeline.
2. **Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.
3. **Extract Key Indicators** — Use incidents to parse and extract relevant network traffic data points from collected artifacts.
4. **Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).
5. **Build Timeline** — Construct a chronological sequence of events related to network traffic.
6. **Document Analysis** — Write findings report with evidence, conclusions, and recommendations.

## Tools

- **incidents** — Primary tool for this skill
- **Forensic Toolkit** — Evidence collection and analysis
- **Timeline Tools** — Chronological event reconstruction
- **Log Analysis Platform** — Centralized log parsing and search

## Verification

- [ ] All network traffic procedures executed completely and documented
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