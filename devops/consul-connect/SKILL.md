---
name: consul-connect
description: Consul Connect service mesh — service-to-service encryption, intentions, sidecar proxies, gateways
---

## Overview

Consul Connect provides service-to-service authorization and encryption via mutual TLS. Services register with Consul, get sidecar proxies, and communicate securely through the mesh.

## Capabilities

- Service registration and discovery
- Sidecar proxy (Envoy) for mTLS
- Intentions for service-to-service authorization
- Mesh gateway for cross-datacenter communication
- Terminating gateway for external service access
- Health checking and monitoring

## When to Use

- Microservices need secure communication without code changes
- Implementing zero-trust networking between services
- Cross-datacenter service mesh deployment
- Need service discovery with health checking

## Pseudo Code

### Service Registration
```hcl
# service.hcl
service {
  name = "web"
  port = 8080
  connect {
    sidecar_service {
      proxy {
        upstreams {
          destination_name = "api"
          local_bind_port  = 9090
        }
      }
    }
  }
  check {
    http     = "http://localhost:8080/health"
    interval = "10s"
  }
}
```

### Intentions (Authorization)
```bash
# Allow web to talk to api
consul intention create web api

# Deny all traffic to admin by default
consul intention create -deny '*' admin

# List intentions
consul intention list
```

### Mesh Gateway (Cross-DC)
```hcl
# mesh-gateway.hcl
connect {
  enabled = true
}
ports {
  grpc = 8502
}
```

## Common Patterns

- **Sidecar injection**: Use `consul connect envoy -sidecar-for web` or K8s injector
- **Upstream config**: Define upstream services in sidecar proxy config
- **Intention precedence**: Specific > wildcard; allow > deny at same precedence
- **Health checks**: Always define checks for automatic traffic routing
- **Transparent proxy**: K8s only — route all traffic through mesh automatically
