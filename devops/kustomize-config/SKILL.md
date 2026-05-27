---
name: kustomize-config
description: Kustomize Kubernetes configuration — bases, overlays, patches, generators, transformers
---

## Overview

Kustomize is a Kubernetes-native configuration management tool that uses overlays to customize base manifests without templating. Built into `kubectl apply -k`.

## Capabilities

- Base/overlay pattern for environment-specific config
- Strategic merge patches and JSON patches
- ConfigMap/Secret generators from files/env
- Name prefix/suffix and namespace transformers
- Label and annotation transformers
- Resource ordering with hooks

## When to Use

- Multi-environment Kubernetes deployments (dev/staging/prod)
- Customize third-party manifests without forking
- Team wants declarative config without Helm templating
- Integration with GitOps (ArgoCD, Flux)

## Pseudo Code

### Directory Structure
```
base/
  kustomization.yaml
  deployment.yaml
  service.yaml
  configmap.yaml

overlays/
  dev/
    kustomization.yaml
    replica-patch.yaml
  staging/
    kustomization.yaml
  production/
    kustomization.yaml
    hpa.yaml
```

### Base
```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml

configMapGenerator:
  - name: app-config
    literals:
      - ENV=base
      - LOG_LEVEL=info

commonLabels:
  app: myapp
```

### Overlay
```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base
  - hpa.yaml

namePrefix: prod-

configMapGenerator:
  - name: app-config
    behavior: merge
    literals:
      - ENV=production
      - LOG_LEVEL=warn

patches:
  - target:
      kind: Deployment
      name: myapp
    patch: |
      - op: replace
        path: /spec/replicas
        value: 5
      - op: add
        path: /spec/template/spec/containers/0/resources
        value:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "256Mi"
            cpu: "250m"

images:
  - name: myapp
    newTag: v2.1.0
```

### Commands
```bash
# Preview
kubectl kustomize overlays/production/

# Apply
kubectl apply -k overlays/production/

# Build (dry-run)
kustomize build overlays/production/
```

## Common Patterns

- **Strategic merge**: patches merged with existing YAML
- **JSON patch**: precise operations (add/replace/remove)
- **Replacement transformer**: substitute values across resources
- **Components**: reusable pieces mixed into overlays
- **Generator options**: disable hash suffix for ConfigMaps
