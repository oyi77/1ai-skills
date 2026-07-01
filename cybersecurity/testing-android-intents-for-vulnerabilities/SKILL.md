---
name: testing-android-intents-for-vulnerabilities
description: 'Tests Android inter-process communication (IPC) through intents for vulnerabilities including intent injection,
  unauthorized component access, broadcast sniffing, pending intent hijacking, and content provider data leakage. Use when
  assessing Android app attack surface through exported components, testing intent-based data flows, or evaluating IPC security.
  Activates for requests involving Android intent security, IPC testing, exported component analysis, or Drozer assessment.

  '
domain: cybersecurity
tags:
- mobile-security
- android
- intents
- ipc-security
- owasp-mobile
- penetration-testing
subdomain: mobile-security
author: mahipal
version: 1.0.0
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.AA-05
- ID.RA-01
- DE.CM-09
---
# Testing Android Intents For Vulnerabilities

## Overview

Cybersecurity skill for testing android intents for vulnerabilities. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "testing android intents for vulnerabilities"
- "Assessing Android app exported activities, services, receivers, and content prov"
- "Testing for intent injection and unauthorized component invocation"
- "Evaluating broadcast receiver security for sensitive data exposure"


Use this skill when:
- Assessing Android app exported activities, services, receivers, and content providers
- Testing for intent injection and unauthorized component invocation
- Evaluating broadcast receiver security for sensitive data exposure
- Performing IPC-focused penetration testing on Android applications

**Do not use** on production devices without explicit authorization.


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Rooted Android device or emulator with ADB
- Drozer agent installed on target device (`drozer agent.apk`)
- Drozer console on host (`pip install drozer`)
- Target APK decompiled with apktool for AndroidManifest.xml analysis
- Frida for runtime intent monitoring

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

1. **Reconnaissance** — Gather information about the target related to android intents. Identify attack surface.
2. **Vulnerability Identification** — Enumerate potential android intents weaknesses using automated and manual techniques.
3. **Exploit Development/Selection** — Use vulnerabilities to identify and test android intents vulnerabilities.
4. **Execution** — Execute the android intents test in a controlled manner with proper authorization.
5. **Post-Exploitation** — Document the impact and extent of successful exploitation.
6. **Reporting** — Write detailed findings with reproduction steps, impact assessment, and remediation guidance.

## Tools

- **vulnerabilities** — Primary tool for this skill
- **Vulnerability Scanner** — Automated weakness identification
- **Exploitation Framework** — Controlled exploitation testing
- **Reporting Tool** — Findings documentation and tracking


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All android intents procedures executed completely and documented
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