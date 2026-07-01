---
name: k8s-deploy
description: K8S Deploy. Use when working with k8s deploy in devops domain.
domain: devops
tags:
- ci-cd
- deploy
- devops
- infrastructure
- k8s
- kubernetes
---
# K8S Deploy

## When to Use

**Trigger phrases:**
- "k8s deploy"
- "Help me with k8s deploy"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- For infrastructure that will be decommissioned within a week
- When the team lacks access to the target environment
- When the change requires downtime that cannot be scheduled


## Overview

K8S Deploy manages infrastructure management with reliability and scalability.

## Workflow

```yaml
# Example: GitHub Actions CI
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: pip install -e ".[test]"
      - run: pytest --cov
```

1. **Define infrastructure** — Specify resources and configuration
2. **Version control** — Store all configurations in Git
3. **Automate deployment** — CI/CD pipeline for consistent releases
4. **Monitor** — Set up observability (metrics, logs, traces)
5. **Respond** — Incident response procedures and runbooks
6. **Optimize** — Performance tuning and cost management

## Configuration

- Environment variables for secrets and config
- Infrastructure as Code (Terraform, Pulumi, CloudFormation)
- Container orchestration (Docker, Kubernetes)
- CI/CD pipeline (GitHub Actions, GitLab CI, ArgoCD)

## Reliability Checklist

- [ ] Health checks configured
- [ ] Auto-scaling policies defined
- [ ] Backup and recovery tested
- [ ] Rollback procedure documented
- [ ] Monitoring alerts configured

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings