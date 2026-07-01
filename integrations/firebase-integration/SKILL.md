---
name: firebase-integration
description: Integrate Firebase for authentication, Firestore database, Cloud Functions, hosting, and push notifications. Build real-time mobile and web applications. Use when integrateing firebase for authentication, firestore database, cloud functions, hosting, and.
domain: integrations
tags:
- firebase
- firestore
- auth
- cloud-functions
- realtime
- hosting
---

# Firebase Integration

## When to Use
**Trigger phrases:**
- "firebase integration"
- "Integrate Firebase for authentication, Firestore database, Cloud Functions, host"


- When building real-time mobile or web apps with Firebase
- When implementing Firebase Authentication (Google, Apple, email)
- When using Firestore for NoSQL document database
- When deploying Cloud Functions for serverless backend logic

## When NOT to Use

- For relational data (use PostgreSQL/Supabase)
- For complex queries (Firestore has limited query capabilities)

## Overview

Full Firebase integration covering Authentication, Firestore, Cloud Functions, Hosting, Cloud Storage, and Push Notifications.

## Workflow

1. **Set up project** - Create Firebase project, add apps
2. **Install SDK** - `npm install firebase` or use modular SDK
3. **Configure auth** - Enable providers, set up sign-in flows
4. **Design data model** - Firestore collections, documents, subcollections
5. **Build queries** - Real-time listeners, compound queries, pagination
6. **Deploy functions** - Cloud Functions for backend logic

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Firestore is just JSON" | Document/subcollection model requires specific data modeling patterns |
| "I will skip security rules" | Without rules, any client can read/write any document |

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


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run firebase integration workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] Authentication works with configured providers
- [ ] Firestore queries return correct data
- [ ] Real-time listeners fire on data changes
- [ ] Security rules enforce access control

