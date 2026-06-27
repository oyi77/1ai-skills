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

## When to Use

- When building Docker container images in CI/CD and needing automated vulnerability scanning before registry push
- When establishing quality gates that prevent images with critical or high CVEs from reaching production
- When compliance requirements mandate vulnerability scanning of all container images before deployment
- When scanning IaC files (Dockerfiles, Kubernetes manifests) alongside container image scanning
- When needing a single tool to scan OS packages, language-specific dependencies, and misconfigurations

**Do not use** for runtime container security monitoring (use Falco), for scanning running containers in production (use runtime agents), or when only scanning application source code without containerization (use SAST tools).

## Prerequisites

- Trivy CLI installed (v0.50+) or access to aquasecurity/trivy-action GitHub Action
- Docker daemon available in CI/CD for building and scanning images
- Container registry credentials for pulling base images and pushing scanned images
- Trivy vulnerability database accessible (downloaded automatically or cached)

## Workflow

1. **Define Objectives** — Clarify the goals and scope for containers.
2. **Gather Resources** — Collect tools, data, and access needed for containers.
3. **Execute Process** — Carry out containers operations methodically.
4. **Verify Quality** — Check results against acceptance criteria.
5. **Document Outcomes** — Record findings, decisions, and next steps.

## Tools

- **trivy in cicd** — Primary tool for this skill
- **Analysis Platform** — Data processing and visualization
- **Collaboration Tools** — Team coordination and knowledge sharing

## Verification

- [ ] All containers procedures executed completely and documented
- [ ] Findings validated against multiple data sources
- [ ] False positives identified and filtered
- [ ] Results documented with evidence and timestamps
- [ ] Recommendations provided with risk-based prioritization
