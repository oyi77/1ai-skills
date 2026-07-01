---
name: appwrite-patterns
description: Appwrite backend-as-a-service — auth, database, storage, functions, realtime for web/mobile/desktop
domain: development
tags:
- appwrite
- coding
- patterns
- software-engineering
- testing
---


## Overview

Appwrite is an open-source backend-as-a-service platform providing auth, database, storage, functions, and messaging for web, mobile, and Flutter applications. It's self-hostable and has a cloud offering.

## Capabilities

- Authentication (email, phone, OAuth2, anonymous, magic links)
- Database with documents, collections, and relationships
- File storage with antivirus scanning
- Serverless functions (Node, Python, PHP, Ruby, Swift, Dart, Go, .NET, Java, Kotlin, Bun, Deno)
- Realtime subscriptions via WebSocket
- Messaging (push, email, SMS)
- Teams and permissions
- Locale and avatars services

## When to Use
**Trigger phrases:**
- "appwrite patterns"
- "Appwrite backend-as-a-service — auth, database, storage, functions, realtime for"


- Full-featured BaaS without building from scratch
- Flutter/mobile-first applications
- Need self-hosted backend control
- Multi-platform (web, iOS, Android, Flutter) applications

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The appwrite-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# appwrite-patterns primary flow
input = prepare(raw_data)
result = process(input, config={appwrite, auth, backend, database, desktop})
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


### Setup (Web SDK)
```typescript
import { Client, Account, Databases, Storage, Functions } from 'appwrite';

const client = new Client()
  .setEndpoint('https://cloud.appwrite.io/v1')
  .setProject('your-project-id');

const account = new Account(client);
const databases = new Databases(client);
const storage = new Storage(client);
const functions = new Functions(client);
```

### Authentication
```typescript
// Email/password
await account.create(ID.unique(), 'alice@example.com', 'password', 'Alice');
const session = await account.createEmailPasswordSession('alice@example.com', 'password');

// OAuth2
await account.createOAuth2Session('google', 'https://app.com/success', 'https://app.com/fail');

// Magic link
await account.createMagicURLSession(ID.unique(), 'alice@example.com', 'https://app.com/verify');

// Get current user
const user = await account.get();
```

### Database CRUD
```typescript
import { ID, Query } from 'appwrite';

// Create
await databases.createDocument('mydb', 'posts', ID.unique(), {
  title: 'Hello World',
  content: 'My first post',
  author: userId,
});

// Read with queries
const posts = await databases.listDocuments('mydb', 'posts', [
  Query.equal('status', 'published'),
  Query.orderDesc('$createdAt'),
  Query.limit(20),
]);

// Update
await databases.updateDocument('mydb', 'posts', documentId, {
  title: 'Updated Title',
});

// Delete
await databases.deleteDocument('mydb', 'posts', documentId);
```

### Storage
```typescript
// Upload file
const file = await storage.createFile('bucket-id', ID.unique(), fileInput);

// Get file URL
const url = storage.getFileView('bucket-id', fileId);

// Delete file
await storage.deleteFile('bucket-id', fileId);
```

### Realtime
```typescript
// Subscribe to collection changes
client.subscribe('databases.mydb.collections.posts.documents', (response) => {
  console.log(response.events); // ['databases.*.collections.*.documents.*.create']
  console.log(response.payload);
});

// Subscribe to user's own channel
client.subscribe('account', (response) => { /* auth events */ });
```

### Functions
```typescript
// Execute function
const result = await functions.createExecution('function-id', JSON.stringify({ key: 'value' }));
console.log(result.stdout, result.stderr);
```

## Common Patterns

- **Permissions**: Use `Permission.read(Role.user(userId))` for fine-grained access control
- **Relationships**: Use relationship attributes for document linking
- **Migrations**: Use Appwrite CLI (`appwrite push/pull`) for collection schemas
- **Docker**: Self-host with `docker compose up -d`

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