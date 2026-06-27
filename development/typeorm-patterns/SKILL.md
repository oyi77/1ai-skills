---
name: typeorm-patterns
description: TypeORM patterns — entities, repositories, migrations, relations, query builder, active record vs data mapper
domain: development
tags:
- coding
- patterns
- software-engineering
- testing
- typeorm
---


## Overview

TypeORM is a TypeScript ORM for Node.js that supports Active Record and Data Mapper patterns. It works with PostgreSQL, MySQL, SQLite, MongoDB, and more.

## Capabilities

- Entity decorators for schema definition
- Repository and Active Record patterns
- Migration generation and execution
- Query Builder for complex queries
- Relations (one-to-one, one-to-many, many-to-many)
- Subscribers and listeners for event-driven logic
- Connection pooling and replication

## When to Use

- Building TypeScript/Node.js applications with SQL databases
- Want both Active Record and Data Mapper patterns
- Need complex query builder capabilities
- Working with existing database schemas

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The typeorm-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# typeorm-patterns primary flow
input = prepare(raw_data)
result = process(input, config={active, builder, data, entities, mapper})
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


### Entity Definition
```typescript
import { Entity, PrimaryGeneratedColumn, Column, OneToMany, ManyToOne, CreateDateColumn } from 'typeorm';

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  email: string;

  @Column({ nullable: true })
  name: string;

  @OneToMany(() => Post, post => post.author)
  posts: Post[];

  @CreateDateColumn()
  createdAt: Date;
}

@Entity()
export class Post {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  title: string;

  @Column({ nullable: true })
  content: string;

  @ManyToOne(() => User, user => user.posts)
  author: User;
}
```

### Repository Pattern
```typescript
import { AppDataSource } from './data-source';
import { User } from './entity/User';

const userRepo = AppDataSource.getRepository(User);

// CRUD
const user = await userRepo.save({ email: 'alice@example.com', name: 'Alice' });
const users = await userRepo.find({ where: { name: 'Alice' }, relations: ['posts'] });
await userRepo.update({ id: 1 }, { name: 'Updated' });
await userRepo.delete({ id: 1 });

// Query Builder
const result = await userRepo
  .createQueryBuilder('user')
  .leftJoinAndSelect('user.posts', 'post')
  .where('user.email LIKE :email', { email: '%@example.com' })
  .orderBy('user.createdAt', 'DESC')
  .take(10)
  .getMany();
```

### Data Source
```typescript
import { DataSource } from 'typeorm';

export const AppDataSource = new DataSource({
  type: 'postgres',
  host: 'localhost',
  port: 5432,
  username: 'user',
  password: 'pass',
  database: 'mydb',
  entities: [User, Post],
  migrations: ['./migration/*.ts'],
  synchronize: false, // Use migrations in production
});
```

### Migrations
```bash
# Generate migration
npx typeorm migration:generate -d src/data-source.ts src/migration/CreateUser

# Run migrations
npx typeorm migration:run -d src/data-source.ts

# Revert last migration
npx typeorm migration:revert -d src/data-source.ts
```

## Common Patterns

- **Active Record**: `User.find()`, `user.save()` — simpler, less testable
- **Data Mapper**: `repo.find()`, `repo.save(user)` — more testable, more boilerplate
- **Subscribers**: Listen to entity events (beforeInsert, afterUpdate, etc.)
- **Transactions**: `AppDataSource.transaction(async (manager) => { ... })`

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

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |