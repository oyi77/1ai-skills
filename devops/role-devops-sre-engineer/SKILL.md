---
name: role-devops-sre-engineer
description: Use when orchestrating infrastructure as code, CI/CD pipelines, container
  orchestration, zero-downtime deployments, observability metrics, and site reliability
  engineering.
domain: devops
author: oyi77
version: 1.0.0
category: devops
tags:
- devops
- sre
- infrastructure
- docker
- terraform
- ci-cd
- kubernetes
- observability
license: MIT
subdomain: devops-sre
---

## Overview

The `role-devops-sre-engineer` skill directs cloud infrastructure provisioning, deployment automation, container lifecycle management, and production reliability engineering. Rather than treating operations as manual shell commands or unstructured scripts, this role establishes an automated infrastructure-as-code foundation, automated CI/CD pipelines with rollback guarantees, zero-downtime database and application deployments, and deep observability telemetry (metrics, logs, traces, and SLO alerts).

```
[Phase 1: IaC & Environment Topology] ──► [Phase 2: Build & Packaging] ──► [Phase 3: CI/CD Pipeline Gates]
                                                                                        │
               [Phase 5: Observability & SRE] ◄── [Phase 4: Zero-Downtime Rollout] ◄────┘
```

The DevOps and SRE engineer ensures infrastructure reproducibility, eliminates manual drift, and protects system availability through automated health gates and rollback automation.

## When to Use

- When designing, provisioning, or modifying cloud infrastructure with Terraform, OpenTofu, or Ansible.
- When creating, hardening, or optimizing Docker container images and multi-stage build workflows.
- When configuring automated CI/CD pipelines (GitHub Actions, GitLab CI) with lint, test, and security gates.
- When executing zero-downtime database schema migrations or blue-green/canary application deployments.
- When deploying Kubernetes manifests, Helm charts, and ingress routing controllers.
- When implementing Prometheus metrics, Grafana dashboards, structured logging, and SLO alert thresholds.

## When NOT to Use

- When writing business domain application logic or database entity models (use `development/role-software-engineer`).
- When conducting penetration testing or dynamic security exploitation sweeps (use `cybersecurity/role-security-engineer`).
- When profiling and tuning complex SQL database query plans (use `data/role-data-engineer`).
- When designing UI/UX frontend styling and client components (use `content/role-ui-ux-designer`).

## Deterministic Dispatch Matrix

| Operational Goal / Infrastructure Challenge | Delegated Child Skill | Primary Operational Artifact |
|---|---|---|
| Provisioning and state management for cloud resources (AWS/GCP/Azure) | `devops/terraform-iac` | Declarative Terraform modules, plan audits, drift mitigation |
| Container image packaging, layer caching, and multi-stage optimization | `devops/docker` | Hardened, minimal non-root Dockerfiles with build cache |
| Automating test-and-deploy pipelines with status checks and gates | `devops/ci-cd-pipeline` | GitHub Actions / GitLab CI workflows with rollback triggers |
| Non-blocking DDL migrations, Expand/Contract schema evolution | `development/zero-downtime-migration-audit` | Non-locking migration scripts (`CONCURRENTLY`, dual-writing) |
| Kubernetes packaging, parameterization, and cluster deployment | `devops/helm-charts` | Versioned Helm charts, templated values, release manifests |
| Server configuration management, OS hardening, fleet orchestration | `devops/ansible-automation` | Idempotent Ansible playbooks and inventory configurations |
| Distributed tracing, metric collection, dashboards, and SLO alerting | `devops/observability` | Prometheus alert rules, Grafana dashboards, OpenTelemetry config |

## Workflow

### Phase 1: Infrastructure as Code & Topology Modeling

1. Model all cloud infrastructure declaratively using `devops/terraform-iac`.
2. Ensure state files are stored in remote encrypted backends with distributed state locking.
3. Execute `terraform plan` and audit for unintended destructive resource replacements before applying.

### Phase 2: Hermetic Container Packaging

1. Package services using multi-stage Docker builds via `devops/docker`.
2. Enforce non-root user execution, pin dependency versions, and minimize attack surface.
3. Eliminate secrets and build artifacts from final runtime images.

### Phase 3: CI/CD Pipeline & Quality Gates

1. Define hermetic build, test, and release pipelines using `devops/ci-cd-pipeline`.
2. Scaffold automated quality gates: type checking, unit tests, security scans, and image vulnerability audits.
3. Configure immutable release tags and verifiable artifact digests.

### Phase 4: Zero-Downtime Deployment & Canary Rollout

1. For database modifications, dispatch to `development/zero-downtime-migration-audit` to execute the Expand/Contract pattern.
2. Deploy applications to Kubernetes clusters using parameterized charts via `devops/helm-charts`.
3. Configure blue-green or canary release strategies with automated health probes (`livenessProbe`, `readinessProbe`).
4. Enforce automated rollback triggers if error rates spike during rollout.

### Phase 5: Observability, SRE & Fleet Hardening

1. Scaffold metric scraping, log aggregation, and trace sampling using `devops/observability`.
2. Define Service Level Objectives (SLOs) and Error Budgets for latency, availability, and throughput.
3. Configure automated fleet configuration and security patching with `devops/ansible-automation`.

## Anti-Rationalization

| DevOps Excuse | Flawed Rationalization | Required SRE Discipline |
|---|---|---|
| "I will configure the server manually via SSH" | "It's faster than writing an Ansible playbook or Terraform." | Manual changes create snowflake servers and untracked drift. Every change must be codified in IaC. |
| "Deploying with `latest` tag is fine" | "It always pulls the most recent build automatically." | Mutable tags cause non-deterministic deployments and break rollbacks. Pin explicit commit SHAs or semantic tags. |
| "We don't need health checks for internal services" | "If the pod crashes, Kubernetes restarts it anyway." | Crash loops without readiness probes route traffic to broken pods. Configure explicit liveness and readiness endpoints. |
| "Run a quick `ALTER TABLE` during off-peak hours" | "It will only lock the table for a few seconds." | Table locks during peak spikes cause cascading connection pool exhaustion. Use non-blocking DDL and Expand/Contract. |
| "Alert on every CPU spike over 80%" | "We want to know whenever the server is working hard." | Non-actionable alerts cause alert fatigue. Alert strictly on user-impacting symptoms (latency, 5xx errors, breach of SLO). |

## Implementation Examples

### Infrastructure Deployment & Canary Health Gate (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="production"
DEPLOYMENT="payment-service"
CANARY_URL="https://canary.example.com/healthz"

echo "=== Step 1: Deploying Helm Canary Release ==="
helm upgrade --install "$DEPLOYMENT-canary" ./charts/payment \
    --namespace "$NAMESPACE" \
    --set replicaCount=1 \
    --set canary.enabled=true \
    --wait --timeout=120s

echo "=== Step 2: Validating Canary Health Probes ==="
STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$CANARY_URL" || echo "000")

if [ "$STATUS_CODE" -ne 200 ]; then
    echo "ERROR: Canary health check failed with HTTP $STATUS_CODE! Triggering rollback..."
    helm rollback "$DEPLOYMENT-canary" --namespace "$NAMESPACE"
    exit 1
fi

echo "SUCCESS: Canary healthy. Proceeding with full cluster rollout."
helm upgrade --install "$DEPLOYMENT" ./charts/payment \
    --namespace "$NAMESPACE" \
    --wait --timeout=300s
```

### Automated Terraform Drift Detector (Python)

```python
import subprocess
import json
import sys

def check_terraform_drift(working_dir: str = ".") -> bool:
    """Executes terraform plan and verifies zero unplanned resource drift."""
    print(f"Checking Terraform drift in {working_dir}...")
    
    cmd = ["terraform", "plan", "-detailed-exitcode", "-no-color"]
    res = subprocess.run(cmd, cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Detailed exit codes: 0 = No changes, 1 = Error, 2 = Succeeded with changes present
    if res.returncode == 0:
        print("SUCCESS: Infrastructure is clean. Zero drift detected.")
        return True
    elif res.returncode == 2:
        print("WARNING: Infrastructure drift detected! Changes are pending:")
        print(res.stdout)
        return False
    else:
        print(f"ERROR: Terraform plan failed!\n{res.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    print("Terraform drift detector initialized.")
```

## Verification Checklist

- [ ] All infrastructure defined in version-controlled declarative IaC modules.
- [ ] Container images built using multi-stage non-root profiles with pinned versions.
- [ ] CI/CD pipeline enforces automated lint, test, and security verification gates.
- [ ] Zero-downtime database migrations validated with non-blocking DDL statements.
- [ ] Health and readiness probes configured for automated container traffic routing.
- [ ] Observability metrics, structured logging, and SLO alert triggers established.
