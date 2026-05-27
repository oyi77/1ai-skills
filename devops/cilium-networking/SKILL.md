---
name: cilium-networking
description: Cilium eBPF networking — Kubernetes CNI, network policies, load balancing, observability with Hubble
---

## Overview

Cilium provides eBPF-based networking, security, and observability for Kubernetes. Replaces kube-proxy, enforces L3/L4/L7 network policies, and includes Hubble for network visibility.

## Capabilities

- eBPF-based CNI (replaces iptables/kube-proxy)
- L3/L4/L7 network policies
- Transparent encryption (WireGuard/IPsec)
- Hubble observability (flow logs, DNS, metrics)
- BGP for hybrid cloud routing
- Service mesh without sidecars

## When to Use

- Kubernetes networking at scale
- Need L7 network policies (HTTP-aware)
- Transparent encryption between pods
- Deep network observability
- Replacing kube-proxy for performance

## Pseudo Code

### Installation
```bash
# Install with Helm
helm repo add cilium https://helm.cilium.io/
helm install cilium cilium/cilium --namespace kube-system

# Enable Hubble
helm upgrade cilium cilium/cilium --namespace kube-system \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true

# Verify
cilium status
cilium connectivity test
```

### Network Policies (L3/L4)
```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: api-policy
spec:
  endpointSelector:
    matchLabels:
      app: api
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: web
      toPorts:
        - ports:
            - port: "8080"
  egress:
    - toEndpoints:
        - matchLabels:
            app: database
```

### L7 (HTTP) Policy
```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: api-l7
spec:
  endpointSelector:
    matchLabels:
      app: api
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: web
      toPorts:
        - ports:
            - port: "8080"
          rules:
            http:
              - method: "GET"
                path: "/api/v1/.*"
              - method: "POST"
                path: "/api/v1/submit"
```

### Hubble Observability
```bash
# Flow logs
hubble observe --namespace production --verdict DROPPED

# DNS queries
hubble observe --protocol dns

# Service map
hubble ui

# Metrics
hubble metrics list
```

### BGP Peering
```yaml
apiVersion: cilium.io/v2alpha1
kind: CiliumBGPNodeConfig
metadata:
  name: bgp-config
spec:
  nodeSelector:
    matchLabels:
      rack: rack-1
  bgpInstances:
    - localASN: 65000
      peers:
        - peerAddress: "10.0.0.1"
          peerASN: 65001
          peerConfigRef:
            name: tor-router
```

## Common Patterns

- **ClusterMesh**: multi-cluster networking
- **WireGuard encryption**: transparent pod-to-pod encryption
- **Bandwidth manager**: EDT-based rate limiting
- **Host firewall**: protect node endpoints
- **Kube-proxy replacement**: eBPF-based service routing
