---
name: implementing-attack-surface-management
description: 'Implements external attack surface management (EASM) using Shodan, Censys, and ProjectDiscovery tools (subfinder,
  httpx, nuclei) for asset discovery, subdomain enumeration, service fingerprinting, and exposure scoring. Includes a weighted
  risk scoring algorithm based on OWASP attack surface analysis methodology and the Relative Attack Surface Quotient (RSQ).
  Use when building continuous ASM programs or performing external reconnaissance for security assessments.

  '
domain: cybersecurity
tags:
- attack-surface
- reconnaissance
- shodan
- censys
- subfinder
- nuclei
- asset-discovery
subdomain: offensive-security
version: '1.0'
author: mukul975
license: Apache-2.0
nist_csf:
- ID.RA-01
- GV.OV-02
- DE.AE-07
---
# Implementing Attack Surface Management

## When to Use

- When building an external attack surface management (EASM) program from scratch
- When performing authorized external reconnaissance for penetration testing engagements
- When continuously monitoring organizational exposure across internet-facing assets
- When scoring and prioritizing external attack surface risks for remediation
- When integrating multiple discovery tools into an automated ASM pipeline

## Prerequisites

- Python 3.8+ with requests, shodan, censys libraries installed
- Shodan API key (free tier provides 100 queries/month)
- Censys API ID and Secret (free tier available)
- ProjectDiscovery tools installed: subfinder, httpx, nuclei
- Go 1.21+ for building ProjectDiscovery tools from source
- Appropriate authorization for all external scanning activities
- Target domains and IP ranges with written scope documentation

## Workflow

1. **Assess Requirements** — Evaluate current environment and define attack surface management implementation requirements.
2. **Design Architecture** — Plan the attack surface management architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up and configure each attack surface management component according to best practices.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs

## Verification

- [ ] All attack surface management procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
