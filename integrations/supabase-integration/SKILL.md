---
name: supabase-integration
description: Integrate Supabase for authentication, database, storage, and real-time subscriptions. Build full-stack applications with Postgres, Row Level Security, and Edge Functions. Use when integrateing supabase for authentication, database, storage, and real-time subscriptions. build.
domain: integrations
tags:
- database
- supabase
- postgres
- auth
- realtime
- storage
---

# Supabase Integration

## When to Use

**Trigger phrases:**
- "supabase integration"
- "When building apps with Supabase as backend (auth + DB + storage)"
- "When implementing Row Level Security (RLS) policies"
- "When using real-time subscriptions for live data"


- When building apps with Supabase as backend (auth + DB + storage)
- When implementing Row Level Security (RLS) policies
- When using real-time subscriptions for live data
- When deploying Edge Functions for serverless logic

## When NOT to Use

- For simple CRUD without auth (use direct PostgreSQL)
- For non-Postgres databases (use their specific skills)

## Overview

Full Supabase integration covering authentication, Postgres database, file storage, real-time subscriptions, and Edge Functions.

## Workflow

1. **Set up project** - Create Supabase project, get API keys
2. **Install SDK** - `npm install @supabase/supabase-js`
3. **Configure auth** - Email/password, OAuth providers, magic links
4. **Define schema** - Tables, RLS policies, triggers
5. **Build queries** - Select, insert, update, delete with filters
6. **Add real-time** - Subscribe to table changes

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "RLS is optional" | Without RLS, any authenticated user can access any data |
| "I will add auth later" | Retrofitting auth is 10x harder than building with it from day one |

## Code Example (TypeScript)

```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);

const { data: { user } } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123',
});

const { data: posts } = await supabase
  .from('posts')
  .select('*, author:profiles(*)')
  .eq('status', 'published')
  .order('created_at', { ascending: false });
```


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run supabase integration workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] Auth flow works (signup, login, logout)
- [ ] RLS policies enforce access control
- [ ] Queries return correct data
- [ ] Real-time subscriptions fire on changes

