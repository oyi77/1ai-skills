---
name: firebase-patterns
description: Firebase patterns — Firestore queries, auth flows, cloud functions, and security rules
---

## Overview

Firebase-specific patterns for building scalable applications. Covers Firestore data modeling, security rules, Cloud Functions, and auth flows.

## Capabilities

- Design Firestore data models for efficient queries
- Write security rules for fine-grained access control
- Build Cloud Functions for serverless backends
- Implement Firebase Auth with social providers
- Use Firebase Storage for file uploads

## When to Use

- Building real-time apps with Firebase
- Need offline-first mobile/web app
- Serverless backend with Cloud Functions
- Social auth integration (Google, Apple, GitHub)

## Pseudo Code

### Firestore Data Model
```javascript
// Denormalized for query efficiency
{
  "users/user1": {
    "name": "John",
    "postCount": 42
  },
  "users/user1/posts/post1": {
    "title": "Hello",
    "createdAt": timestamp
  }
}
```

### Security Rules
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read: if request.auth != null;
      allow write: if request.auth.uid == userId;
    }
  }
}
```

## Common Patterns

- **Denormalize for reads**: Duplicate data to avoid subcollection queries
- **Security rules as tests**: Write rules first, then build features
- **Batch writes**: Use batched writes for multi-document operations
- **Offline persistence**: Enable for mobile apps by default
