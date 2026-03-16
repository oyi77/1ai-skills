# Database Schema

This directory contains the Prisma schema and database configuration.

## 📁 Files

| File | Description |
|------|-------------|
| `schema.prisma` | Database schema definition |
| `migrations/` | Database migration files |
| `seed.ts` | Database seeding script |

## 🔄 Common Commands

```bash
# Generate Prisma client
npm run db:generate

# Run migrations
npm run migrate:dev      # Development
npm run migrate:prod     # Production

# Check migration status
npm run migrate:status

# Open Prisma Studio
npm run db:studio

# Seed database
npm run db:seed
```

## 📊 Schema Overview

### Models

| Model | Description |
|-------|-------------|
| `User` | User accounts and profiles |
| `Transaction` | Payment transactions |
| `Video` | Generated videos |
| `Commission` | Affiliate commissions |
| `Subscription` | User subscriptions |
| `AuditLog` | Audit trail |

## 🔗 Relationships

```
User
├── Transactions (1:N)
├── Videos (1:N)
├── Commissions (1:N)
└── Subscriptions (1:N)
```

---

*See [DATABASE.md](../docs/DATABASE.md) for detailed documentation*
