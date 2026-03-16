# Monitoring

This directory contains monitoring and observability configuration.

## 📁 Files

| File/Directory | Description |
|----------------|-------------|
| `prometheus.yml` | Prometheus configuration |
| `grafana/` | Grafana dashboards and datasources |

## 🔧 Components

### Prometheus

Prometheus collects metrics from the bot and stores them for querying.

**Port**: 9090

**Metrics Endpoint**: `/metrics`

### Grafana

Grafana visualizes metrics from Prometheus in dashboards.

**Port**: 3002 (default)

**Default Login**: admin/admin

## 📊 Dashboards

| Dashboard | Description |
|-----------|-------------|
| `openclaw-bot.json` | Main bot metrics dashboard |

### Key Metrics

- Active Users
- Videos Generated
- Queue Depth
- Error Rate
- API Latency

## 🚀 Running Monitoring Stack

```bash
# Start with monitoring
docker-compose --profile monitoring up -d

# Access services
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3002
```

## 📝 Adding Custom Metrics

1. Add metric collection in code
2. Expose via `/metrics` endpoint
3. Add to Prometheus configuration
4. Create/update Grafana dashboard

---

*See [MONITORING.md](../docs/MONITORING.md) for detailed documentation*
