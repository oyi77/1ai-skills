# Source Code

This directory contains the main source code for the OpenClaw Bot.

## 📁 Structure

```
src/
├── commands/       # Telegram bot commands
├── handlers/       # Event handlers
├── services/       # Business logic services
├── models/         # Data models
├── utils/          # Utility functions
├── middleware/     # Bot middleware
├── config/         # Configuration
├── types/          # TypeScript types
├── routes/         # API routes
└── index.ts        # Entry point
```

## 📖 Modules

### Commands (`commands/`)

Telegram bot command handlers:
- `start.ts` - /start command
- `help.ts` - /help command
- `create.ts` - /create command
- `topup.ts` - /topup command
- `referral.ts` - /referral command
- `profile.ts` - /profile command
- `settings.ts` - /settings command
- `videos.ts` - /videos command
- `subscription.ts` - /subscription command
- `support.ts` - /support command
- `admin/` - Admin commands

### Handlers (`handlers/`)

Event handlers:
- `message.ts` - Message handler
- `callback.ts` - Callback query handler
- `error.ts` - Error handler

### Middleware (`middleware/`)

Bot middleware:
- `session.ts` - Session management
- `rateLimit.ts` - Rate limiting
- `user.ts` - User loading
- `logging.ts` - Request logging

### Config (`config/`)

Configuration modules:
- `database.ts` - Database connection
- `redis.ts` - Redis connection
- `queue.ts` - Queue setup

### Routes (`routes/`)

API routes:
- `health.ts` - Health check endpoints
- `webhook.ts` - Webhook handlers

### Types (`types/`)

TypeScript type definitions:
- `index.ts` - All type definitions

### Utils (`utils/`)

Utility functions:
- `logger.ts` - Logging utility

---

*See [ARCHITECTURE.md](../docs/ARCHITECTURE.md) for detailed architecture documentation*
