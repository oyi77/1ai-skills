---
name: envoy-proxy
description: Envoy proxy — L4/L7 filtering, load balancing, circuit breaking, observability, extensibility
---

## Overview

Envoy is a high-performance L4/L7 proxy designed for microservice architectures. Provides advanced load balancing, rate limiting, circuit breaking, and rich observability via stats, logging, and tracing.

## Capabilities

- HTTP/1.1, HTTP/2, gRPC, TCP proxying
- Advanced load balancing (round robin, ring hash, least request)
- Rate limiting and circuit breaking
- Extensible via Lua/Wasm filters
- Built-in stats, logging, and distributed tracing
- xDS API for dynamic configuration

## When to Use

- Service mesh data plane (Istio, Consul Connect)
- API gateway / edge proxy
- gRPC load balancing
- Canary routing and traffic shifting
- Need rich observability metrics

## Pseudo Code

### Static Configuration
```yaml
# envoy.yaml
static_resources:
  listeners:
    - name: listener_0
      address:
        socket_address: { address: 0.0.0.0, port_value: 8080 }
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: ingress_http
                route_config:
                  virtual_hosts:
                    - name: backend
                      domains: ["*"]
                      routes:
                        - match: { prefix: "/" }
                          route:
                            cluster: service_cluster
                            timeout: 30s
                            retry_policy:
                              retry_on: "5xx"
                              num_retries: 3
                http_filters:
                  - name: envoy.filters.http.router

  clusters:
    - name: service_cluster
      type: STRICT_DNS
      lb_policy: LEAST_REQUEST
      load_assignment:
        cluster_name: service_cluster
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address: { address: service1, port_value: 8080 }
              - endpoint:
                  address:
                    socket_address: { address: service2, port_value: 8080 }
      circuit_breakers:
        thresholds:
          - max_connections: 100
            max_pending_requests: 50
            max_requests: 200
```

### Rate Limiting
```yaml
http_filters:
  - name: envoy.filters.http.local_ratelimit
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
      stat_prefix: rate_limit
      token_bucket:
        max_tokens: 100
        tokens_per_fill: 10
        fill_interval: 1s
```

### Health Checking
```yaml
clusters:
  - name: backend
    health_checks:
      - timeout: 5s
        interval: 10s
        unhealthy_threshold: 3
        healthy_threshold: 2
        http_health_check:
          path: "/healthz"
```

## Common Patterns

- **Circuit breaking**: prevent cascade failures
- **Retry policies**: automatic retry on 5xx/connect failures
- **Shadow traffic**: mirror requests for testing
- **Fault injection**: simulate errors for chaos testing
- **Wasm filters**: custom logic without recompiling Envoy
