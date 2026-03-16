# 🤖 OpenClaw Bot

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/status-production-green.svg)](STATUS.md)
[![License](https://img.shields.io/badge/license-PROPRIETARY-red.svg)](LICENSE)

> **AI Video Marketing SaaS Platform — Child Bot Architecture**

OpenClaw Bot adalah bot Telegram turunan yang terintegrasi dengan OpenClaw Core System untuk menyediakan layanan pembuatan video marketing AI secara otomatis.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [Support](#support)

---

## 🎯 Overview

OpenClaw Bot memungkinkan pengguna untuk:
- 🎬 Generate video marketing dari foto produk
- 💰 Top-up kredit dengan multiple payment gateway
- 👥 Sistem referral & affiliate 2-tier
- 📊 Dashboard analytics untuk tracking performa
- 🎨 Multi-angle creative generation
- 🔗 Direct publish ke social media

### Tech Stack

| Layer | Technology |
|-------|------------|
| **Runtime** | Node.js 20 LTS |
| **Framework** | Telegraf.js + Fastify |
| **Database** | PostgreSQL 15 (Primary-Replica) |
| **Cache** | Redis Cluster 7.x |
| **Queue** | BullMQ |
| **Storage** | AWS S3 / Cloudflare R2 |
| **AI Pipeline** | GeminiGen.ai API |
| **Payment** | Midtrans (primary) + Tripay (backup) |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TELEGRAM PLATFORM                        │
└───────────────────────┬─────────────────────────────────────┘
                        │ Webhook
┌───────────────────────▼─────────────────────────────────────┐
│                   OPENCLAW BOT                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Bot Core  │  │   Queue     │  │   State Manager     │  │
│  │   (Node.js) │  │   (BullMQ)  │  │   (Redis)           │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
│  PostgreSQL  │ │    Redis    │ │   S3 CDN   │
│  (User Data) │ │  (Session)  │ │  (Assets)  │
└──────────────┘ └─────────────┘ └────────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   OPENCLAW CORE                             │
│         (Parent System - API Integration)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Node.js 20+
- PostgreSQL 15+
- Redis 7+
- Telegram Bot Token

### Installation

```bash
# Clone repository
git clone https://github.com/openclaw/bot.git
cd openclaw-bot

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Run migrations
npm run migrate

# Start development
npm run dev

# Start production
npm run start
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [MASTER_PROMPT.md](docs/MASTER_PROMPT.md) | Complete bot behavior specification |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture & design patterns |
| [API.md](docs/API.md) | API contracts & integration guides |
| [DATABASE.md](docs/DATABASE.md) | Database schema & migrations |
| [SECURITY.md](docs/SECURITY.md) | Security policies & procedures |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Deployment guides & CI/CD |
| [MONITORING.md](docs/MONITORING.md) | Observability & alerting |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues & solutions |

---

## ⚙️ Configuration

### Environment Variables

See [`.env.example`](.env.example) for complete configuration.

```bash
# Core
NODE_ENV=production
BOT_TOKEN=your_telegram_bot_token
WEBHOOK_SECRET=your_webhook_secret
WEBHOOK_URL=https://api.openclaw.ai/webhook

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/openclaw
REDIS_URL=redis://localhost:6379

# AI APIs
GEMINIGEN_API_KEY=xxx
KLING_API_KEY=xxx
RUNWAY_API_KEY=xxx

# Payment
MIDTRANS_SERVER_KEY=xxx
MIDTRANS_CLIENT_KEY=xxx
TRIPAY_API_KEY=xxx

# Storage
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
S3_BUCKET=openclaw-assets
```

### Feature Flags

Feature flags dapat dikonfigurasi via admin dashboard atau environment variables:

```bash
# Enable/disable features
FEATURE_MULTI_ANGLE=true
FEATURE_VOICE_CLONING=true
FEATURE_TEAM_WORKSPACE=false
```

---

## 🚢 Deployment

### Docker

```bash
# Build image
docker build -t openclaw-bot:latest .

# Run container
docker run -d \
  --name openclaw-bot \
  --env-file .env \
  -p 3000:3000 \
  openclaw-bot:latest
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -n openclaw
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment guides.

---

## 📊 Monitoring

### Health Checks

```bash
# Bot health
curl https://api.openclaw.ai/health

# Database health
curl https://api.openclaw.ai/health/db

# Queue status
curl https://api.openclaw.ai/health/queue
```

### Metrics

| Metric | Endpoint | Description |
|--------|----------|-------------|
| `bot_users_active` | `/metrics` | Active users (hourly) |
| `bot_videos_generated` | `/metrics` | Videos generated count |
| `bot_queue_depth` | `/metrics` | Current queue depth |
| `bot_error_rate` | `/metrics` | Error rate percentage |

### Alerts

Alerts dikirim ke Slack/Telegram saat:
- Payment failure rate > 10%
- AI API down > 2 minutes
- Error rate > 5%
- Queue depth > 100

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan kontribusi.

### Development Workflow

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Standards

- ESLint + Prettier
- Conventional Commits
- 80%+ test coverage
- Documentation required for new features

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) untuk riwayat perubahan lengkap.

### Latest Release: v3.0.0

**Major Changes:**
- ✅ Production-grade security hardening
- ✅ Circuit breaker patterns untuk external APIs
- ✅ Comprehensive monitoring & observability
- ✅ Disaster recovery procedures
- ✅ RBAC untuk admin functions
- ✅ Multi-tenant architecture support

---

## 🆘 Support

### Channels

| Channel | Link |
|---------|------|
| Documentation | [docs.openclaw.ai](https://docs.openclaw.ai) |
| Discord | [discord.gg/openclaw](https://discord.gg/openclaw) |
| Email | support@openclaw.ai |
| Telegram | [@openclaw_support](https://t.me/openclaw_support) |

### Emergency Contacts

- **Technical On-Call**: `+62-xxx-xxxx-xxxx`
- **Security Issues**: `security@openclaw.ai`

---

## 📄 License

This project is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

© 2024 OpenClaw. All rights reserved.

---

<p align="center">
  <strong>Made with ❤️ by OpenClaw Team</strong>
</p>
