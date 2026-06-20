---
name: consul-service-mesh
description: HashiCorp Consul — service discovery, health checking, KV store, service mesh, intentions
domain: devops
tags:
- ci-cd
- consul
- devops
- infrastructure
- mesh
- service
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

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The consul-service-mesh workflow follows a standard pipeline pattern.

Core flow:
```
# consul-service-mesh primary flow
input = prepare(raw_data)
result = process(input, config={checking, consul, discovery, hashicorp, health})
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
