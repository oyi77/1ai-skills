---
name: nomad-scheduler
description: HashiCorp Nomad — job scheduling, task drivers, allocations, scaling, federation
---

## Overview

Nomad is a flexible workload orchestrator for deploying containers, VMs, and standalone applications. Supports multiple task drivers, bin packing, and multi-region federation.

## Capabilities

- Multi-driver task scheduling (Docker, exec, Java, QEMU)
- Job specification in HCL
- Rolling updates and canary deployments
- Multi-region federation
- Autoscaling with external metrics
- Integration with Consul and Vault

## When to Use

- Mixed workloads (containers + non-containerized)
- Simple alternative to Kubernetes
- Multi-region deployments
- Batch job scheduling
- Integration with HashiCorp stack (Consul, Vault)

## Pseudo Code

### Job Specification
```hcl
# web.nomad
job "web" {
  datacenters = ["dc1"]
  type        = "service"

  group "app" {
    count = 3

    network {
      port "http" { to = 8080 }
    }

    service {
      name     = "web"
      port     = "http"
      provider = "consul"

      check {
        type     = "http"
        path     = "/health"
        interval = "10s"
      }
    }

    task "server" {
      driver = "docker"

      config {
        image = "nginx:alpine"
        ports = ["http"]
      }

      resources {
        cpu    = 256
        memory = 256
      }

      template {
        data        = "{{ key \"config/nginx.conf\" }}"
        destination = "local/nginx.conf"
      }

      vault {
        policies = ["web-policy"]
      }
    }
  }

  update {
    max_parallel = 1
    canary       = 1
    auto_revert  = true
  }
}
```

### Commands
```bash
# Run job
nomad job run web.nomad

# Status
nomad job status web
nomad alloc status <alloc-id>

# Scale
nomad job scale web app 5

# Stop
nomad job stop web

# Plan (dry run)
nomad job plan web.nomad

# Regions
nomad server members
nomad job run -region=eu web.nomad
```

## Common Patterns

- **Periodic jobs**: `cron` schedule for batch work
- **Parameterized jobs**: trigger with meta payload
- **Canary deploys**: `canary = 1` for safe rollouts
- **Spread**: distribute across datacenters
- **Affinity/Constraints**: pin to specific nodes
