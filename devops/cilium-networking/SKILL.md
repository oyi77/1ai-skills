---
name: cilium-networking
description: Cilium eBPF networking — Kubernetes CNI, network policies, load balancing, observability with Hubble
domain: devops
tags:
- ci-cd
- cilium
- devops
- infrastructure
- kubernetes
- networking
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
**Trigger phrases:**
- "cilium networking"
- "Cilium eBPF networking — Kubernetes CNI, network policies, load balancing, obser"


- Kubernetes networking at scale
- Need L7 network policies (HTTP-aware)
- Transparent encryption between pods
- Deep network observability
- Replacing kube-proxy for performance

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The cilium-networking workflow follows a standard pipeline pattern.

Core flow:
```
# cilium-networking primary flow
input = prepare(raw_data)
result = process(input, config={balancing, cilium, ebpf, hubble, kubernetes})
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

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |