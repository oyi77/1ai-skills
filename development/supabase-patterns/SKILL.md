---
name: supabase-patterns
description: Supabase patterns — Row Level Security, edge functions, real-time subscriptions,
  and auth integration
domain: development
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
