---
name: observability
description: Observability stack — Prometheus, Grafana, Loki, OpenTelemetry. Metrics, logs, traces, alerting, SLO monitoring
---

## Overview

Observability provides visibility into system behavior through metrics, logs, and traces. Use when setting up monitoring, designing dashboards, configuring alerts, investigating incidents, or tracking SLOs.

## Capabilities

- Collect metrics with Prometheus and OpenTelemetry
- Aggregate logs with Loki and Fluentd
- Trace distributed requests with Jaeger/Tempo
- Design Grafana dashboards and alerts
- Define and track SLOs (Service Level Objectives)
- Correlate metrics, logs, and traces for root cause analysis

## When to Use

- Setting up monitoring for new services
- Designing dashboards for operational visibility
- Configuring alerting rules and escalation
- Investigating production incidents
- Tracking reliability against SLOs

## Pseudo Code

### Prometheus configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'my-app'
    static_configs:
      - targets: ['app:8080']
    metrics_path: /metrics

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
```

### Alert rules
```yaml
# alerts.yml
groups:
  - name: app-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.instance }}"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
```

### Grafana dashboard (JSON model)
```json
{
  "panels": [
    {
      "title": "Request Rate",
      "type": "timeseries",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total[5m])) by (status)",
          "legendFormat": "{{status}}"
        }
      ]
    },
    {
      "title": "Latency P99",
      "type": "stat",
      "targets": [
        {
          "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))"
        }
      ]
    }
  ]
}
```

### OpenTelemetry instrumentation
```python
# Python auto-instrumentation
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("http.method", "GET")
    # ... operation code
```

### Loki log queries (LogQL)
```logql
# Filter by level
{job="my-app"} |= "error" | logfmt | level="error"

# Rate of errors
rate({job="my-app"} |= "error" [5m])

# Parse JSON logs
{job="my-app"} | json | status >= 500 | line_format "{{.message}}"
```

### SLO definition
```yaml
# slo.yaml
service: my-api
slo:
  - name: availability
    target: 99.9
    sli: |
      sum(rate(http_requests_total{status!~"5.."}[30d]))
      /
      sum(rate(http_requests_total[30d]))
    window: 30d

  - name: latency
    target: 95
    sli: |
      sum(rate(http_request_duration_seconds_bucket{le="0.5"}[30d]))
      /
      sum(rate(http_request_duration_seconds_count[30d]))
    window: 30d
```

## Common Patterns

### Three pillars correlation
```
Metrics (what's wrong) → Logs (why) → Traces (where)
Grafana: click metric → see logs → trace request
```

### Alert fatigue reduction
```
- Alert on symptoms, not causes
- Use SLO-based alerting (burn rate)
- Multi-window, multi-burn-rate alerts
- Deduplicate with Alertmanager routing
```

### Observability stack (self-hosted)
```
Prometheus (metrics) + Grafana (dashboards)
Loki (logs) + Promtail/Fluentd (log collection)
Tempo/Jaeger (traces) + OpenTelemetry Collector
```
