---
name: sequelize-patterns
description: Sequelize ORM patterns — models, associations, migrations, transactions,
  hooks, TypeScript support
domain: development
---


## Overview

Sequelize is a promise-based Node.js ORM for PostgreSQL, MySQL, MariaDB, SQLite, and Microsoft SQL Server. It features solid transaction support, relations, eager/lazy loading, read replication, and more.

## Capabilities

- Model definition with TypeScript decorators or define()
- Associations: hasOne, hasMany, belongsTo, belongsToMany
- Migrations with sequelize-cli
- Transactions (managed and unmanaged)
- Hooks (beforeCreate, afterUpdate, etc.)
- Scopes for reusable query fragments
- Eager/lazy loading with include
- Read replication and connection pooling

## When to Use

- Node.js applications needing a mature, well-documented ORM
- Multi-database support (PostgreSQL, MySQL, SQLite, MSSQL)
- Need complex associations and eager loading
- Existing JavaScript codebase (Sequelize has strong JS support)

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The sequelize-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# sequelize-patterns primary flow
input = prepare(raw_data)
result = process(input, config={associations, hooks, migrations, models, patterns})
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


### Model Definition
```typescript
import { DataTypes, Model } from 'sequelize';
import sequelize from './connection';

class User extends Model {
  declare id: number;
  declare email: string;
  declare name: string;
}

User.init({
  id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
  email: { type: DataTypes.STRING, unique: true, allowNull: false },
  name: { type: DataTypes.STRING },
}, { sequelize, modelName: 'user' });
```

### Associations
```typescript
User.hasMany(Post, { foreignKey: 'authorId' });
Post.belongsTo(User, { foreignKey: 'authorId' });
User.belongsToMany(Role, { through: 'UserRoles' });
Role.belongsToMany(User, { through: 'UserRoles' });
```

### Queries
```typescript
// Create
const user = await User.create({ email: 'alice@example.com', name: 'Alice' });

// Find with eager loading
const users = await User.findAll({
  where: { name: { [Op.like]: '%Alice%' } },
  include: [{ model: Post, as: 'posts' }],
  order: [['createdAt', 'DESC']],
  limit: 10,
});

// Update
await User.update({ name: 'Updated' }, { where: { id: 1 } });

// Delete
await User.destroy({ where: { id: 1 } });
```

### Transactions
```typescript
// Managed transaction
await sequelize.transaction(async (t) => {
  const user = await User.create({ email: 'bob@example.com' }, { transaction: t });
  await Post.create({ title: 'Hello', authorId: user.id }, { transaction: t });
});
```

### Hooks
```typescript
User.addHook('beforeCreate', async (user) => {
  user.email = user.email.toLowerCase();
});
```

### Scopes
```typescript
User.addScope('active', { where: { isActive: true } });
User.addScope('withPosts', { include: [{ model: Post }] });

const activeUsers = await User.scope('active').findAll();
```

## Common Patterns

- **Migrations**: `npx sequelize-cli migration:generate --name create-users`
- **Seeders**: `npx sequelize-cli seed:generate --name demo-users`
- **TypeScript**: Use `declare` for model attributes, `init()` for schema
- **Connection pooling**: Configure `pool` option in Sequelize constructor

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit
