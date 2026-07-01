---
name: scanning-containers-with-trivy-in-cicd
description: 'This skill covers integrating Aqua Security''s Trivy scanner into CI/CD pipelines for comprehensive container
  image vulnerability detection. It addresses scanning Docker images for OS package and application dependency CVEs, detecting
  misconfigurations in Dockerfiles, scanning filesystem and git repositories, and establishing severity-based quality gates
  that block deployment of vulnerable images.

  '
domain: cybersecurity
tags:
- devsecops
- cicd
- trivy
- container-security
- vulnerability-scanning
- secure-sdlc
subdomain: devsecops
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- GV.SC-07
- ID.IM-04
- PR.PS-04
---
# Scanning Containers With Trivy In Cicd

## Overview

Cybersecurity skill for scanning containers with trivy in cicd. Follows industry best practices and security standards.

## When to Use
**Trigger phrases:**
- "scanning containers with trivy in cicd"
- "This skill covers integrating Aqua Security''s Trivy scanner into CI/CD pipeline"


- When building Docker container images in CI/CD and needing automated vulnerability scanning before registry push
- When establishing quality gates that prevent images with critical or high CVEs from reaching production
- When compliance requirements mandate vulnerability scanning of all container images before deployment
- When scanning IaC files (Dockerfiles, Kubernetes manifests) alongside container image scanning
- When needing a single tool to scan OS packages, language-specific dependencies, and misconfigurations

**Do not use** for runtime container security monitoring (use Falco), for scanning running containers in production (use runtime agents), or when only scanning application source code without containerization (use SAST tools).


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope


## Prerequisites

- Trivy CLI installed (v0.50+) or access to aquasecurity/trivy-action GitHub Action
- Docker daemon available in CI/CD for building and scanning images
- Container registry credentials for pulling base images and pushing scanned images
- Trivy vulnerability database accessible (downloaded automatically or cached)

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

1. **Define Objectives** — Clarify the goals and scope for containers.
2. **Gather Resources** — Collect tools, data, and access needed for containers.
3. **Execute Process** — Carry out containers operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **trivy in cicd** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run scanning containers with trivy in cicd workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All containers procedures executed completely and documented
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