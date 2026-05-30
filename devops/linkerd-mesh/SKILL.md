---
name: linkerd-mesh
description: Linkerd service mesh — lightweight Kubernetes mesh, mTLS, traffic splitting, observability
---


## Overview

Linkerd is a lightweight, security-first service mesh for Kubernetes. Adds automatic mTLS, observability, and traffic management with minimal resource overhead via Rust-based proxy.

## Capabilities

- Automatic mTLS for all meshed traffic
- Traffic splitting for canary deployments
- Per-route metrics and dashboards
- Retry and timeout policies
- Multi-cluster communication
- CLI and dashboard for observability

## When to Use

- Kubernetes needing simple service mesh
- Want mTLS without complex configuration
- Canary deployments with traffic splitting
- Need lightweight alternative to Istio
- Multi-cluster setups

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The linkerd-mesh workflow follows a standard pipeline pattern.

Core flow:
```
# linkerd-mesh primary flow
input = prepare(raw_data)
result = process(input, config={kubernetes, lightweight, linkerd, mesh, mtls})
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


### Installation
```bash
# Install CLI
curl -fsL https://run.linkerd.io/install | sh

# Install control plane
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -

# Install viz extension
linkerd viz install | kubectl apply -f -

# Inject sidecar
kubectl get deploy -o yaml | linkerd inject - | kubectl apply -f -

# Check mesh status
linkerd check
```

### Traffic Split (Canary)
```yaml
apiVersion: split.smi-spec.io/v1alpha4
kind: TrafficSplit
metadata:
  name: web-canary
spec:
  service: web
  backends:
    - service: web-stable
      weight: 90
    - service: web-canary
      weight: 10
```

### Retry and Timeout
```yaml
apiVersion: policy.linkerd.io/v1beta1
kind: Server
metadata:
  name: web
spec:
  podSelector:
    matchLabels:
      app: web
  port: 8080
---
apiVersion: policy.linkerd.io/v1beta1
kind: Server
metadata:
  name: web-timeout
spec:
  podSelector:
    matchLabels:
      app: web
  port: 8080
  proxyProtocol:
    timeout: 30s
```

### Observability
```bash
# Dashboard
linkerd viz dashboard

# Top routes
linkerd viz top deploy/web

# Stats
linkerd stat deploy

# Tap live traffic
linkerd viz tap deploy/web

# Edges (connections)
linkerd viz edges deploy
```

## Common Patterns

- **Mutual TLS**: automatic, no config needed
- **Traffic split**: SMI-compatible canary routing
- **Gateway API**: HTTPRoute for advanced routing
- **Multi-cluster**: linked clusters share trust domain
- **Extensions**: jaeger, viz, multicluster

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
