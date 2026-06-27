---
name: implementing-security-chaos-engineering
description: 'Implements security chaos engineering experiments that deliberately disable or degrade security controls to
  verify detection and response capabilities. Tests WAF bypass, firewall rule removal, log pipeline disruption, and EDR disablement
  scenarios using boto3 and subprocess. Use when validating SOC detection coverage and resilience.

  '
domain: cybersecurity
tags:
- implementing
- security
- chaos
- engineering
subdomain: security-operations
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- DE.CM-01
- RS.MA-01
- GV.OV-01
- DE.AE-02
---
# Implementing Security Chaos Engineering

## When to Use

- When deploying or configuring implementing security chaos engineering capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites

- Familiarity with security operations concepts and tools
- Access to a test or lab environment for safe execution
- Python 3.8+ with required dependencies installed
- Appropriate authorization for any testing activities

## Workflow

1. **Assess Requirements** — Evaluate current environment and define security chaos engineering implementation requirements.
2. **Design Architecture** — Plan the security chaos engineering architecture, including components, integrations, and data flows.
3. **Configure Components** — Set up and configure each security chaos engineering component according to best practices.
4. **Test Integration** — Validate that all components work together. Run functional and security tests.
5. **Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.
6. **Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.

## Tools

- **Configuration Management** — Infrastructure as code and automation
- **Monitoring Stack** — Observability and alerting
- **Documentation Platform** — Runbooks and architecture docs

## Verification

- [ ] All security chaos engineering procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
