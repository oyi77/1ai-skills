---
name: supabase-patterns
description: Supabase patterns — Row Level Security, edge functions, real-time subscriptions, and auth integration
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

## Pseudo Code

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
