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

## Pseudo Code

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
