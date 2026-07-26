---
name: supabase-patterns
description: Supabase patterns — Row Level Security, edge functions, real-time subscriptions, auth integration, setup, and configuration. Use when working with supabase patterns.
domain: development
tags:
- coding
- patterns
- software-engineering
- supabase
- testing
- database
- postgres
- auth
- realtime
- storage
---


## Overview

Supabase-specific patterns for building secure, real-time applications. Covers RLS policies, edge functions, real-time, storage, and auth.

## Capabilities

- Implement Row Level Security (RLS) for multi-tenant data
- Write Supabase Edge Functions for serverless logic
- Set up real-time subscriptions for live data
- Integrate Supabase Auth with social providers
- Use Supabase Storage for file uploads

## When to Use
**Trigger phrases:**
- "supabase patterns"
- "Supabase patterns — Row Level Security, edge functions, real-time subscriptions,"


- Building multi-tenant SaaS with Supabase
- Need real-time features (live updates, presence)
- Serverless backend with Edge Functions
- File storage and CDN for user uploads

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The supabase-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# supabase-patterns primary flow
input = prepare(raw_data)
result = process(input, config={auth, edge, functions, integration, level})
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


### Row Level Security
```sql
-- Users can only see their own data
CREATE POLICY "users_own_data" ON orders
  FOR ALL USING (auth.uid() = user_id);

-- Team members can see team data
CREATE POLICY "team_access" ON projects
  FOR SELECT USING (
    team_id IN (SELECT team_id FROM team_members WHERE user_id = auth.uid())
  );
```

### Edge Function
```typescript
// supabase/functions/hello/index.ts
Deno.serve(async (req) => {
  const { name } = await req.json()
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!
  )
  const { data } = await supabase.from('greetings').insert({ name })
  return new Response(JSON.stringify(data))
})
```

### Real-time Subscription
```typescript
const channel = supabase
  .channel('orders')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'orders' }, handleUpdate)
  .subscribe()
```

## Common Patterns

- **RLS always on**: Enable RLS on every table — no exceptions
- **Edge Functions for webhooks**: Process Stripe, email events serverlessly
- **Real-time for collaboration**: Use presence and broadcast for multi-user features


## Setup and Configuration

### Project Setup

1. **Create a Supabase project** — Start a new project in the Supabase dashboard, then copy the project URL and anon key.
2. **Install the SDK** — `npm install @supabase/supabase-js`
3. **Configure auth** — Enable email/password, OAuth providers (Google, GitHub), or magic links in the Supabase dashboard.
4. **Define schema** — Create tables, enable Row Level Security, write RLS policies, set up triggers.
5. **Build queries** — Use the Supabase client for select, insert, update, delete with chained filters.
6. **Add real-time** — Subscribe to table changes with Supabase Realtime channels.

### Client Initialization

```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
```

### Auth Example

```typescript
const { data: { user } } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123',
});
```

### Query with Joins

```typescript
const { data: posts } = await supabase
  .from('posts')
  .select('*, author:profiles(*)')
  .eq('status', 'published')
  .order('created_at', { ascending: false });
```

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
- [ ] Auth flow works (signup, login, logout)
- [ ] RLS policies enforce access control
- [ ] Queries return correct data
- [ ] Real-time subscriptions fire on changes

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
| "RLS is optional" | Without RLS, any authenticated user can access any data. |
| "I will add auth later" | Retrofitting auth is 10x harder than building with it from day one. |