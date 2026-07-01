---
name: hardening-linux-endpoint-with-cis-benchmark
description: 'Hardens Linux endpoints using CIS Benchmark recommendations for Ubuntu, RHEL, and CentOS to reduce attack surface,
  enforce security baselines, and meet compliance requirements. Use when deploying new Linux servers, remediating audit findings,
  or establishing security baselines for Linux infrastructure. Activates for requests involving Linux hardening, CIS benchmarks
  for Linux, server security baselines, or Linux configuration compliance.

  '
domain: cybersecurity
tags:
- endpoint
- hardening
- linux-security
- CIS-benchmark
- Ubuntu
- RHEL
subdomain: endpoint-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.PS-02
- DE.CM-01
- PR.IR-01
---
# Hardening Linux Endpoint With Cis Benchmark

## Overview

Cybersecurity skill for hardening linux endpoint with cis benchmark. Follows industry best practices and security standards.

## When to Use

**Trigger phrases:**
- "hardening linux endpoint with cis benchmark"
- "Hardening Linux servers (Ubuntu, RHEL, CentOS, Debian) against CIS benchmarks"
- "Automating Linux security baselines using Ansible, OpenSCAP, or shell scripts"
- "Meeting compliance requirements (PCI DSS, HIPAA, SOC 2) for Linux endpoints"


Use this skill when:
- Hardening Linux servers (Ubuntu, RHEL, CentOS, Debian) against CIS benchmarks
- Automating Linux security baselines using Ansible, OpenSCAP, or shell scripts
- Meeting compliance requirements (PCI DSS, HIPAA, SOC 2) for Linux endpoints
- Remediating findings from vulnerability scans or security audits

**Do not use** for Windows hardening (use hardening-windows-endpoint-with-cis-benchmark).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Root or sudo access on target Linux endpoints
- CIS Benchmark PDF for target distribution (from cisecurity.org)
- OpenSCAP or CIS-CAT for automated assessment
- Ansible for enterprise-scale remediation (optional)

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

1. **Define Objectives** — Clarify the goals and scope for linux endpoint.
2. **Gather Resources** — Collect tools, data, and access needed for linux endpoint.
3. **Execute Process** — Carry out linux endpoint operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **cis benchmark** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run hardening linux endpoint with cis benchmark workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All linux endpoint procedures executed completely and documented
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