---
name: firebase-patterns
description: Firebase patterns and integration — Firestore queries, auth flows, cloud functions, security rules, SDK setup, and real-time data. Use when working with firebase patterns, integrating firebase.
domain: development
tags:
- coding
- firebase
- firestore
- auth
- cloud-functions
- realtime
- patterns
- rest-api
- software-engineering
- testing
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
**Trigger phrases:**
- "firebase integration"
- "Integrate Firebase for authentication, Firestore database, Cloud Functions, host"
- "firebase patterns"
- "Firebase patterns — Firestore queries, auth flows, cloud functions, and security"


- Building real-time apps with Firebase
- Need offline-first mobile/web app
- Serverless backend with Cloud Functions
- Social auth integration (Google, Apple, GitHub)

## Workflow

1. **Set up project** - Create Firebase project, add apps
2. **Install SDK** - `npm install firebase` or use modular SDK
3. **Configure auth** - Enable providers, set up sign-in flows
4. **Design data model** - Firestore collections, documents, subcollections
5. **Build queries** - Real-time listeners, compound queries, pagination
6. **Deploy functions** - Cloud Functions for backend logic

## Code Example (JavaScript)

```javascript
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, onSnapshot, query, where } from 'firebase/firestore';
import { getAuth, signInWithPopup, GoogleAuthProvider } from 'firebase/auth';

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

const { user } = await signInWithPopup(auth, new GoogleAuthProvider());

const q = query(collection(db, 'messages'), where('channel', '==', 'general'));
const unsubscribe = onSnapshot(q, (snapshot) => {
  snapshot.docChanges().forEach((change) => {
    if (change.type === 'added') console.log('New message:', change.doc.data());
  });
});
```

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


- For relational data (use PostgreSQL/Supabase)
- For complex queries (Firestore has limited query capabilities)

## Pseudo Code

The firebase-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# firebase-patterns primary flow
input = prepare(raw_data)
result = process(input, config={auth, cloud, firebase, firestore, flows})
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
- [ ] Authentication works with configured providers
- [ ] Firestore queries return correct data
- [ ] Real-time listeners fire on data changes
- [ ] Security rules enforce access control

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |
| "Firestore is just JSON" | Document/subcollection model requires specific data modeling patterns |
| "I will skip security rules" | Without rules, any client can read/write any document |