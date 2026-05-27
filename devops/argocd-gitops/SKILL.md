---
name: argocd-gitops
description: ArgoCD GitOps — declarative continuous delivery, application sync, drift detection, multi-cluster
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

## Pseudo Code

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
