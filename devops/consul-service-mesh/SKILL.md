---
name: consul-service-mesh
description: HashiCorp Consul — service discovery, health checking, KV store, service mesh, intentions
---

## Overview

Consul provides service discovery, health checking, KV store, and secure service mesh (Connect) for microservice architectures. Supports multi-datacenter federation.

## Capabilities

- Service registration and DNS-based discovery
- HTTP/TCP/gRPC health checking
- Distributed KV store for configuration
- Connect service mesh with mTLS
- Intention-based access control
- Multi-datacenter federation

## When to Use

- Microservice architectures needing service discovery
- Dynamic environments with frequent deployments
- Zero-trust networking with mTLS between services
- Centralized configuration management
- Multi-cloud or hybrid infrastructure

## Pseudo Code

### Service Registration
```hcl
# service.hcl
service {
  name    = "web"
  port    = 8080
  tags    = ["v2", "primary"]

  check {
    http     = "http://localhost:8080/health"
    interval = "10s"
    timeout  = "3s"
  }
}
```

### KV Store Operations
```bash
# Write
consul kv put config/database/host db.example.com
consul kv put config/database/port 5432

# Read
consul kv get config/database/host

# Tree
consul kv get -recurse config/

# Watch for changes
consul watch -type=keyprefix -prefix=config/ /opt/update-config.sh
```

### Connect Service Mesh
```hcl
# Proxy sidecar
service {
  name = "api"
  port = 8080

  connect {
    sidecar_service {
      proxy {
        upstreams {
          destination_name = "database"
          local_bind_port  = 5432
        }
      }
    }
  }
}
```

### Intentions (Access Control)
```bash
# Allow web to talk to api
consul intention create web api

# Deny all by default
consul intention create -deny '*' '*'

# List intentions
consul intention list
```

## Common Patterns

- **DNS interface**: `web.service.consul` resolves to service IPs
- **Prepared queries**: advanced DNS routing with failover
- **Agentless**: services register via HTTP API or config file
- **Consul Template**: render configs from KV + service data
- **Watches**: trigger actions on data changes
