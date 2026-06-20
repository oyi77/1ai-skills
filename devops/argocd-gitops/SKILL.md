---
name: argocd-gitops
description: ArgoCD GitOps — declarative continuous delivery, application sync, drift detection, multi-cluster
domain: devops
tags:
- argocd
- ci-cd
- devops
- gitops
- infrastructure
---


## Overview

ArgoCD is a declarative GitOps continuous delivery tool for Kubernetes. Monitors Git repos for changes and automatically syncs desired state to clusters with drift detection.

## Capabilities

- Declarative application management via CRDs
- Automatic sync on Git changes
- Drift detection and correction
- Multi-cluster management
- Sync waves for ordering
- SSO, RBAC, and audit logging

## When to Use

- GitOps-based Kubernetes deployments
- Multi-cluster or multi-environment management
- Need visibility into deployment status
- Want automatic drift correction
- Compliance requirements for audit trails

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The argocd-gitops workflow follows a standard pipeline pattern.

Core flow:
```
# argocd-gitops primary flow
input = prepare(raw_data)
result = process(input, config={application, argocd, cluster, continuous, declarative})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Application CRD
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/k8s-manifests.git
    targetRevision: main
    path: apps/myapp/overlays/production
    kustomize:
      images:
        - myapp:v2.1.0
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Sync Waves (Ordering)
```yaml
# Phase 1: CRDs
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-2"

# Phase 2: Database
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-1"

# Phase 3: Application
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "0"
```

### ApplicationSet (Multi-env)
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp
spec:
  generators:
    - list:
        elements:
          - env: dev
            cluster: https://dev-cluster
          - env: staging
            cluster: https://staging-cluster
          - env: prod
            cluster: https://prod-cluster
  template:
    metadata:
      name: 'myapp-{{env}}'
    spec:
      source:
        path: 'apps/myapp/overlays/{{env}}'
      destination:
        server: '{{cluster}}'
```

### CLI
```bash
# Sync
argocd app sync myapp

# Diff
argocd app diff myapp

# Rollback
argocd app rollback myapp 1

# List
argocd app list

# History
argocd app history myapp
```

## Common Patterns

- **Sync windows**: restrict sync times (e.g., business hours only)
- **Resource hooks**: PreSync, PostSync, SyncFail hooks
- **Health checks**: custom health assessment for CRDs
- **Notifications**: Slack/Email on sync status changes
- **App of Apps**: single app manages other apps

## How to Use

1. Define infrastructure as code (Terraform, CloudFormation, Pulumi)
2. Review changes through PR process before applying
3. Configure monitoring and alerting for critical paths
4. Set up secrets management (Vault, AWS Secrets Manager, etc.)
5. Document runbooks for deployment, rollback, and incident response
6. Test disaster recovery procedures regularly

## Red Flags

- **Infrastructure changes without review**: Unreviewed changes cause outages — use PRs for infra code
- **No rollback strategy**: Every deployment needs a tested rollback plan before it runs
- **Secrets in configuration files**: Secrets in YAML/JSON get committed to version control
- **Missing monitoring and alerting**: Without monitoring, outages go undetected until users report them
- **No documentation for runbooks**: Without runbooks, on-call engineers waste time re-discovering procedures

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
