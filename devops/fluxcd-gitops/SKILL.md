---
name: fluxcd-gitops
description: Flux CD GitOps — source controllers, kustomize/helm controllers, image automation, notifications
---

## Overview

Flux CD is a GitOps toolkit for Kubernetes using source, kustomize, helm, and notification controllers. Declarative CRDs manage the entire delivery pipeline.

## Capabilities

- Source controllers (Git, OCI, Helm repos, S3)
- Kustomize and Helm release controllers
- Image automation (scan repos, update manifests)
- Alert providers (Slack, Discord, PagerDuty)
- Multi-tenancy with impersonation
- Dependency management between resources

## When to Use

- Kubernetes GitOps without a separate UI
- Prefer CRD-only approach over Application objects
- Need image automation (auto-update on new images)
- Multi-tenant clusters with namespace isolation

## Pseudo Source

### GitRepository
```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: fleet
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/fleet
  ref:
    branch: main
  secretRef:
    name: github-credentials
```

### Kustomization
```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: fleet
  path: ./apps/myapp/production
  prune: true
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: myapp
      namespace: production
  timeout: 5m
  dependsOn:
    - name: infrastructure
```

### HelmRelease
```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: nginx
  namespace: production
spec:
  interval: 10m
  chart:
    spec:
      chart: nginx
      sourceRef:
        kind: HelmRepository
        name: bitnami
      version: "15.x.x"
  values:
    replicaCount: 3
    service:
      type: ClusterIP
```

### Image Automation
```yaml
# Scan image repos
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata:
  name: myapp
spec:
  image: ghcr.io/org/myapp
  interval: 5m
---
# Update policy
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: myapp
spec:
  imageRepositoryRef:
    name: myapp
  policy:
    semver:
      range: ">=2.0.0 <3.0.0"
```

### Notifications
```yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Alert
metadata:
  name: on-call
spec:
  providerRef:
    name: slack
  eventSeverity: info
  eventSources:
    - kind: Kustomization
      name: '*'
```

## Common Patterns

- **Bootstrapping**: `flux bootstrap github --owner=org --repository=fleet`
- **Multi-tenancy**: namespace isolation with service account impersonation
- **OCI sources**: store manifests as OCI artifacts
- **SOPS secrets**: encrypted secrets in Git with Mozilla SOPS
