---
name: pocketbase-patterns
description: PocketBase — single-file backend with SQLite, realtime subscriptions,
  auth, file storage, custom JS extensions
domain: development
---


## Overview

PocketBase is an open-source backend consisting of an embedded SQLite database with realtime subscriptions, auth, file storage, and a REST API — all in a single Go binary. It supports custom JS/TS extensions via the built-in JS VM.

## Capabilities

- Single binary, zero dependencies
- SQLite embedded with WAL mode
- REST API auto-generated from collections
- Realtime via SSE (Server-Sent Events)
- Built-in auth (email/password, OAuth2 providers)
- File storage with S3 or local filesystem
- Custom JS/TS hooks and API routes
- Admin dashboard UI
- Go extensions for advanced customization

## When to Use

- Rapid prototyping and MVPs
- Small to medium applications
- Self-hosted backend-as-a-service alternative
- Want to avoid complex infrastructure

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The pocketbase-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# pocketbase-patterns primary flow
input = prepare(raw_data)
result = process(input, config={auth, backend, custom, extensions, file})
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


### Setup
```bash
# Download and run
wget https://github.com/pocketbase/pocketbase/releases/latest/download/pocketbase_linux_amd64.zip
unzip pocketbase_linux_amd64.zip
./pocketbase serve --http=0.0.0.0:8090
```

### Collections (via Admin UI or API)
```javascript
// REST API - Create record
const response = await fetch('http://localhost:8090/api/collections/posts/records', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Hello World',
    content: 'My first post',
    author: userId,
  }),
});
```

### SDK Usage
```typescript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://localhost:8090');

// Auth
await pb.collection('users').authWithPassword('alice@example.com', 'password');
await pb.collection('users').authWithOAuth2({ provider: 'google' });

// CRUD
const records = await pb.collection('posts').getList(1, 20, {
  filter: 'status = "published" && author.name ~ "Alice"',
  sort: '-created',
  expand: 'author',
});

const record = await pb.collection('posts').getOne(recordId);
await pb.collection('posts').create({ title: 'New Post', author: userId });
await pb.collection('posts').update(recordId, { title: 'Updated' });
await pb.collection('posts').delete(recordId);
```

### Realtime
```typescript
// Subscribe to collection changes
pb.collection('posts').subscribe('*', (e) => {
  console.log(e.action); // 'create', 'update', 'delete'
  console.log(e.record);
});

// Subscribe to single record
pb.collection('posts').subscribe(recordId, (e) => { /* ... */ });

// Unsubscribe
pb.collection('posts').unsubscribe();
```

### Custom Hooks (pb_hooks/)
```javascript
// pb_hooks/on_record_create.pb.js
onRecordCreateRequest((e) => {
  e.record.set('status', 'draft');
  e.next();
});

// Custom API route
routerAdd('GET', '/api/stats', (c) => {
  const total = $app.dao().findCollectionByNameOrId('posts').totalRecords;
  return c.json(200, { total });
});
```

## Common Patterns

- **Migrations**: Export/import collections JSON via admin dashboard
- **Backups**: `./pocketbase backup` creates zip of DB + files
- **Docker**: Use official PocketBase Docker image
- **S3 storage**: Configure in admin dashboard for production file storage

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
