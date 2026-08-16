---
name: supabase-mcp
description: Use when mCP server for Supabase databases. Query tables, manage auth,
  and handle storage through standardized protocol. Use when working with supabase
  mcp.
domain: mcp
author: oyi77
license: Apache-2.0
subdomain: mcp
tags:
- mcp
- mcp-server
- model-context-protocol
- supabase
- tool-integration
version: 1.0.0
category: mcp
---


# Supabase Mcp

## When to Use

**Trigger phrases:**
- "supabase mcp"
- "Help me with supabase mcp"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- When a simpler HTTP client would suffice
- For internal tools that do not need cross-platform compatibility
- When the tool is used by a single agent in a single context


## Overview

Supabase is an open-source Firebase alternative that provides a full suite of backend services built on PostgreSQL, including authentication, real-time subscriptions, object storage, and serverless Edge Functions. The Supabase MCP server bridges these capabilities into AI agent workflows, enabling agents to query databases, manage auth users, upload and retrieve storage objects, and invoke Edge Functions through standardized Model Context Protocol tools.

The platform's foundation is PostgreSQL with automatic Row Level Security (RLS) — every database operation can be scoped to the authenticated user through policies written in plain SQL. Supabase manages database migrations through a version-controlled SQL migration system, provides a RESTful API layer (PostgREST) generated automatically from your schema, and exposes GraphQL through pg_graphql.

Beyond the database, Supabase handles user authentication via email/password, magic links, OAuth providers (Google, GitHub, Discord, and others), and multi-factor authentication. The Realtime engine broadcasts database changes over WebSocket connections, Storage manages files in S3-compatible buckets with RLS integration, and Edge Functions execute TypeScript/Deno code at the edge with cold starts under 50ms.


## Architecture

- **PostgreSQL Database** — Managed Postgres with pgvector, full-text search, automatic backups, and point-in-time recovery
- **PostgREST API** — Auto-generated RESTful API from your database schema with row-level security enforcement
- **GoTrue Auth** — Built-in authentication with email/password, OAuth, magic links, and MFA support
- **Realtime Engine** — WebSocket-based real-time subscriptions using PostgreSQL replication slots
- **Storage** — S3-compatible object storage with RLS policy integration for file access control
- **Edge Functions** — Deno-based serverless functions with global deployment and low-latency execution
- **MCP Server** — Model Context Protocol layer exposing query, auth, storage, and function invocation tools to AI agents


## Setup

Install the Supabase client SDK:

```bash
# Python
pip install supabase

# Node.js
npm install @supabase/supabase-js
```

Add the Supabase MCP server to your client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-supabase"],
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "your-service-role-key"
      }
    }
  }
}
```

Initialize the client in your application:

```python
from supabase import create_client, Client

url = "https://your-project.supabase.co"
key = "your-supabase-anon-key"  # or service_role key for admin
supabase: Client = create_client(url, key)
```

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-supabase-anon-key'
)
```


## Configuration

- `SUPABASE_URL` — Project URL from Dashboard Settings (e.g., `https://abc123.supabase.co`)
- `SUPABASE_ANON_KEY` — Client-safe anon/public key for browser and mobile SDKs
- `SUPABASE_SERVICE_ROLE_KEY` — Server-only key that bypasses RLS; never expose in client code
- `SUPABASE_DB_PASSWORD` — Direct database connection password for schema migrations and admin tasks
- **Connection pooling** — Use Supavisor on port `6543` (transaction mode) or `6543?mode=session` for production workloads
- **Custom SMTP** — Configure in Auth → Settings for branded auth emails and password resets


## Integration

The Supabase MCP server integrates with Claude Desktop, Cursor, and any MCP-compatible client. Exposed tools and resources include:

- **Tools:** `query_database`, `execute_sql`, `manage_auth_user`, `storage_upload`, `storage_list`, `invoke_edge_function`
- **Resource URIs:** `supabase://{project}/tables`, `supabase://{project}/table/{name}/rows`
- **Real-time:** `supabase://{project}/realtime/{table}` for live data subscriptions
- **Transport:** stdio for local clients, HTTP for remote access over SSE


## Workflow

1. **Project initialization** — Create a new Supabase project via Dashboard or CLI (`supabase init`), select database region and pricing tier.
2. **Schema design** — Define tables, primary keys, foreign keys, and indexes using the SQL Editor or local migration files in `supabase/migrations/`.
3. **Row Level Security** — Write `CREATE POLICY` statements for each table operation. Test with `auth.uid()` simulation in the SQL Editor.
4. **Client SDK setup** — Install `supabase-py` or `@supabase/supabase-js`, create a client with project URL and anon key, wrap authenticated routes.
5. **Realtime configuration** — Enable replication on target tables via Dashboard → Database → Replication, subscribe with `channel.on('postgres_changes', ...)`.
6. **Storage and Edge Functions** — Create buckets with policy-protected access, deploy Deno functions with `supabase functions deploy`, wire to database triggers.
7. **Production hardening** — Enable point-in-time recovery, configure custom SMTP, set up Supavisor connection pooling, monitor with Dashboard analytics.


## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will just use curl" | MCP handles auth, retries, streaming, and type safety. Use the SDK. |
| "One mega-server is simpler" | Single-responsibility servers are easier to debug and maintain. |
| "MCP is just a wrapper" | MCP enables cross-platform tool sharing. It is infrastructure, not overhead. |
| "Postgres.js is enough, I don't need Supabase" | Supabase provides auth, real-time, storage, and edge functions — months of work if built on raw Postgres. |
| "RLS policies are optional for my MVP" | RLS is the security foundation. Skipping it creates data leakage that requires a full rewrite to add later. |
| "I can poll the database instead of real-time" | Supabase Realtime uses WebSocket subscriptions — lower latency, lower bandwidth, no polling interval to tune. |


## Code Examples

### Python (supabase-py)

```python
from supabase import create_client, Client

# Initialize client
url: str = "https://your-project.supabase.co"
key: str = "your-supabase-anon-key"
supabase: Client = create_client(url, key)

# Query rows with filters
response = supabase.table("profiles").select("*").eq("role", "admin").execute()
for row in response.data:
    print(row["full_name"])

# Insert a new row
data = {"full_name": "Alice", "role": "admin", "email": "alice@example.com"}
result = supabase.table("profiles").insert(data).execute()
print(f"Created: {result.data}")

# Auth — sign up a new user
auth_response = supabase.auth.sign_up(
    {"email": "alice@example.com", "password": "secure-password"}
)
print(f"User ID: {auth_response.user.id}")

# Storage — upload a file
with open("photo.jpg", "rb") as f:
    storage_resp = supabase.storage.from_("avatars").upload(
        "public/alice.jpg", f.read()
    )
```

### JavaScript (supabase-js)

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-supabase-anon-key'
)

// Query rows with filters
const { data, error } = await supabase
  .from('profiles')
  .select('*')
  .eq('role', 'admin')

if (error) throw error
console.log(data)

// Insert a new row
const { data: newProfile, error: insertError } = await supabase
  .from('profiles')
  .insert({ full_name: 'Alice', role: 'admin', email: 'alice@example.com' })
  .select()

// Real-time subscription
const channel = supabase
  .channel('profile-changes')
  .on('postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'profiles' },
    (payload) => console.log('New profile:', payload.new)
  )
  .subscribe()

// Storage download
const { data: fileData, error: dlError } = await supabase
  .storage
  .from('avatars')
  .download('public/alice.jpg')
```


## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| Row Level Security blocks all queries | Ensure the anon key JWT has the correct `role` claim. Use `service_role` key for server-side admin operations. |
| Real-time subscription receives no events | Enable Replication on the table via Dashboard → Database → Replication. Only tables with replication enabled broadcast changes. |
| Storage upload fails with 403 | Check the bucket's RLS policy — a common pattern is `bucket_id = 'your-bucket' AND auth.role() = 'authenticated'`. |
| supabase-py returns empty data | Add `.execute()` to the query chain. Supabase queries in Python are lazily evaluated until `.execute()` is called. |
| Edge Function times out connecting to DB | Set `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` as environment variables in the function config; never hardcode credentials. |
| TypeScript type errors on Supabase types | Use `@supabase/supabase-js` v2+ with generated types: run `supabase gen types typescript --linked > database.types.ts` and pass as generic. |


## Monetization

- **Supabase consulting** — Offer Supabase migration, schema design, and RLS policy auditing at $150–300/hr. Many teams migrating from Firebase or raw Postgres need expert guidance on RLS and real-time.
- **MCP server as a product** — Package and sell a hosted Supabase MCP gateway with team access controls, usage dashboards, and SLA guarantees for enterprises.
- **Template marketplace** — Create and sell full-stack starter kits (Next.js + Supabase, React Native + Supabase) with pre-configured RLS policies, auth flows, and MCP tooling.
- **Performance optimization** — Offer Supabase query tuning, indexing strategy, connection pooling configuration, and query plan analysis as a flat-fee or retainer service.
- **Custom RLS and Edge Function development** — Build and maintain custom RLS policies, database triggers, and Supabase Edge Functions for clients on monthly retainer.
- **Supabase course/platform** — Create a video course or written guide on building production apps with Supabase + MCP, monetized via one-time purchase or subscription.


## Process

1. **Project design** — Define tables, relationships, RLS policies, and storage buckets in the Supabase Dashboard before writing any client code.
2. **SQL schema migration** — Use Supabase migrations (local SQL files) or the Dashboard SQL editor for version-controlled schema changes with rollback plans.
3. **Client integration** — Install supabase-js or supabase-py, initialize the client with anon key, and verify basic CRUD against each table.
4. **Security hardening** — Write RLS policies for every table, enable MFA for production, set up email confirmation, and audit service_role key usage.
5. **Production deployment** — Enable point-in-time recovery, configure Supavisor connection pooling, deploy Edge Functions, set up custom SMTP, and monitor via Dashboard analytics.


## Verification

- [ ] Supabase project created and `service_role` key stored securely (never in client-side code)
- [ ] Client SDK (supabase-py or supabase-js) connects and authenticates successfully
- [ ] All table CRUD operations work with proper RLS enforcement for both authenticated and anonymous users
- [ ] Auth flows verified end-to-end: signup, login, password reset, and OAuth provider integration
- [ ] Storage upload and download succeed with correct bucket-level RLS policies
- [ ] Real-time subscriptions fire correctly on INSERT, UPDATE, and DELETE events
- [ ] Edge Functions deploy without errors and return expected responses
- [ ] Database backups enabled and point-in-time recovery time window confirmed
