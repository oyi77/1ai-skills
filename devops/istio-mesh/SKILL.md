---
name: istio-mesh
description: Istio service mesh — traffic management, security, observability for Kubernetes microservices
---

## Overview

Istio provides a service mesh for Kubernetes with traffic management, mutual TLS, and observability. Uses Envoy sidecar proxies for data plane and istiod for control plane.

## Capabilities

- Traffic routing (canary, A/B, mirroring)
- Automatic mTLS between services
- Request-level telemetry (metrics, logs, traces)
- Circuit breaking and retry policies
- Authorization policies
- Multi-cluster federation

## When to Use

- Kubernetes microservice architectures
- Need zero-trust networking with mTLS
- Canary deployments with traffic splitting
- Distributed tracing and service graph
- Fine-grained access control between services

## Pseudo Code

### Traffic Management
```yaml
# VirtualService - canary routing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: web-vs
spec:
  hosts:
    - web
  http:
    - match:
        - headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: web
            subset: canary
    - route:
        - destination:
            host: web
            subset: stable
          weight: 90
        - destination:
            host: web
            subset: canary
          weight: 10
---
# DestinationRule
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: web-dr
spec:
  host: web
  subsets:
    - name: stable
      labels:
        version: v1
    - name: canary
      labels:
        version: v2
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
    circuitBreaker:
      consecutive5xxErrors: 5
```

### mTLS Policy
```yaml
# PeerAuthentication - strict mTLS
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

### Authorization
```yaml
# AuthorizationPolicy
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-policy
spec:
  selector:
    matchLabels:
      app: api
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/default/sa/web"]
      to:
        - operation:
            methods: ["GET"]
            paths: ["/api/*"]
```

### Telemetry
```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-telemetry
spec:
  tracing:
    - providers:
        - name: jaeger
      randomSamplingPercentage: 10
```

## Common Patterns

- **Sidecar injection**: `istio-injection=enabled` namespace label
- **Fault injection**: test resilience with delays/aborts
- **Mirroring**: copy traffic to canary for testing
- **Egress gateway**: control outbound traffic
- **Kiali dashboard**: visualize service graph
