---
name: kustomize-config
description: Kustomize Kubernetes configuration — bases, overlays, patches, generators,
  transformers
domain: devops
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

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The kustomize-config workflow follows a standard pipeline pattern.

Core flow:
```
# kustomize-config primary flow
input = prepare(raw_data)
result = process(input, config={bases, config, configuration, generators, kubernetes})
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
