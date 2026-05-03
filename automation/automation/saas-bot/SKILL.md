---
name: saas-bot
description: OpenClaw Video Studio SaaS bot — Telegram + GeminiGen AI media generation + FFmpeg video production. Manages video creation, scene chaining, image generation, and Telegram delivery via Telegraf.
---
persona:
  name: "Domain Expert"
  title: "Master of Saas Bot"
  expertise: ['Automation Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']



# OpenClaw Video Studio — SaaS Bot

AI Video Marketing SaaS Platform — Telegram bot with GeminiGen AI media generation.

## Project

**Location:** `/home/openclaw/.openclaw/workspace/projects/openclaw-saas-bot/`
**Stack:** TypeScript + Node.js, Telegraf.js, Fastify, PostgreSQL/Prisma, Redis/BullMQ
**Port:** 3000
**Main:** `dist/index.js`

## Quick Start

```bash
# Development
cd /home/openclaw/.openclaw/workspace/projects/openclaw-saas-bot
pnpm dev

# Production build
pnpm build && pnpm start:prod

# Health check
pnpm health-check
```

## Architecture

```
src/
├── index.ts              # Main: Fastify + Telegraf
├── commands/             # Bot commands (create, videos, etc.)
├── handlers/             # Event handlers
├── services/
│   ├── geminigen.service.ts   # Video gen + extend with ref_image
│   ├── image.service.ts        # Image generation /generate_image
│   ├── video-generation.service.ts  # Scene orchestration
│   └── video.service.ts        # Credit costs, storyboard templates
├── routes/               # Fastify REST routes
├── middleware/           # Auth, rate limiting
└── config/              # DB, Redis, Queue init
```

## Key Commands

| Command | Description |
|---------|-------------|
| `/create` | Start video creation flow |
| `/videos` | List user's videos |
| `/grok` | Chat with AI (free via OpenRouter) |
| `/help` | Show all commands |

## /grok — Free AI Chat

Uses Grok-Api server (free LLM via grok.com reverse-engineering).

**Usage:**
- `/grok <question>` — Ask anything
- `/grok --model grok-4 <question>` — Use specific model
- `/grok --clear` — Clear conversation context

**Models:** grok-3-auto, grok-3-fast, grok-4, grok-4-mini-thinking-tahoe

**Setup:** Grok-Api server must be running at http://localhost:6969

## Environment Variables

Required in `.env`:
- `BOT_TOKEN` — Telegram bot token
- `DATABASE_URL` — PostgreSQL connection string
- `REDIS_URL` — Redis connection string
- `GEMINIGEN_API_KEY` — GeminiGen API key (from workspace/config/geminigen_api.json)
- `GEMINIGEN_API_BASE` — `https://api.geminigen.ai/uapi/v1`
- `PORT` — Server port (default: 3000)

## API Endpoints

- `GET /health` — Health check
- `POST /webhook/telegram` — Telegram webhook
- `POST /admin/retry-video/:id` — Retry failed video generation

## Database

PostgreSQL via Prisma ORM. Run migrations:
```bash
pnpm migrate:dev   # Development
pnpm migrate:prod  # Production
pnpm db:seed       # Seed initial data
pnpm db:studio     # Open Prisma Studio
```

## Scripts

```bash
pnpm setup       # Initial setup
pnpm deploy      # Deploy script
pnpm backup      # Backup DB + uploads
pnpm docker:build && pnpm docker:run  # Docker deployment
```

## GeminiGen API — Verified Working

**Image Generation** ✅
- `POST /uapi/v1/generate_image` (FormData)
- Fields: `prompt`, `model=nano-banana-pro`, `style=Photorealistic`, `output_format=jpeg`, `resolution=1K`, `aspect_ratio=portrait`
- Poll: `GET /uapi/v1/history/{uuid}`
- Response: `generated_image[0].image_url`

**Video Generation** ✅
- `POST /uapi/v1/video-gen/grok` (FormData)
- ONLY fields: `prompt`, `model=grok-3`, `aspect_ratio=portrait|landscape|square`, `duration=6|10|15`
- **CRITICAL**: Do NOT include `resolution=480p` or `mode=custom`

**Video Extend (Scene Chaining)** ✅
- `POST /uapi/v1/video-extend/grok` (FormData)
- Fields: `prompt`, `ref_history={uuid}`, `ref_image=@file.png` (multipart!)
- ref_image must be last frame PNG extracted via ffmpeg
