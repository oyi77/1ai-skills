---
name: deploying-palo-alto-prisma-access-zero-trust
description: 'Deploying Palo Alto Networks Prisma Access for SASE-based zero trust network access using GlobalProtect agents,
  ZTNA Connectors, security policy enforcement, and integration with Strata Cloud Manager for unified security management.

  '
domain: cybersecurity
tags:
- prisma-access
- palo-alto
- ztna
- sase
- globalprotect
- strata-cloud-manager
- zero-trust
subdomain: zero-trust-architecture
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- GOVERN-1.1
- MEASURE-2.7
- MANAGE-3.1
nist_csf:
- PR.AA-01
- PR.AA-05
- PR.IR-01
- GV.PO-01
---
# Deploying Palo Alto Prisma Access Zero Trust

## When to Use

- When implementing enterprise-grade SASE with integrated ZTNA, SWG, CASB, and FWaaS
- When replacing both VPN and branch office firewalls with cloud-delivered security
- When needing advanced threat prevention (WildFire, DNS Security) for remote access traffic
- When deploying zero trust for both mobile users and remote network (branch) connections
- When integrating ZTNA with existing Palo Alto NGFW infrastructure via Strata Cloud Manager

**Do not use** for small organizations (< 200 users) where simpler ZTNA solutions suffice, for environments requiring only web application access without full network security, or when budget constraints preclude enterprise SASE licensing.

## Prerequisites

- Prisma Access license (Business Premium or equivalent)
- Strata Cloud Manager (SCM) tenant configured
- GlobalProtect agent for endpoint deployment
- ZTNA Connector VM: 4 vCPU, 8GB RAM, 128GB disk (VMware, AWS, Azure, or GCP)
- Identity provider: Okta, Entra ID, Ping Identity (SAML 2.0)
- Palo Alto Cortex Data Lake for log storage

## Workflow

1. **Define Objectives** — Clarify the goals and scope for palo alto prisma access zero trust.
2. **Gather Resources** — Collect tools, data, and access needed for palo alto prisma access zero trust.
3. **Execute Process** — Carry out palo alto prisma access zero trust operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All palo alto prisma access zero trust procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
