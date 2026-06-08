---
name: consul-connect
description: Consul Connect service mesh — service-to-service encryption, intentions,
  sidecar proxies, gateways
domain: devops
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

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The consul-connect workflow follows a standard pipeline pattern.

Core flow:
```
# consul-connect primary flow
input = prepare(raw_data)
result = process(input, config={connect, consul, encryption, gateways, intentions})
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
