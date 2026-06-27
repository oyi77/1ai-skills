---
name: svelte-framework
description: Svelte and SvelteKit development — runes, stores, server-side rendering, form actions, streaming
domain: development
tags:
- coding
- framework
- software-engineering
- svelte
- testing
---


## Overview

Build high-performance web apps with Svelte 5 (runes reactivity) and SvelteKit (SSR, routing, form actions, streaming).

## Capabilities

- Svelte 5 runes ($state, $derived, $effect)
- Stores and reactive state
- SvelteKit file-based routing
- Server-side rendering and streaming
- Form actions for mutations
- Load functions for data fetching
- Adapter-based deployment (Vercel, Node, Cloudflare)

## When to Use

- Building fast, lightweight web applications
- SSR/SSG with minimal JavaScript
- Form-heavy applications with progressive enhancement
- Real-time apps with efficient reactivity
- Edge-deployed applications

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The svelte-framework workflow follows a standard pipeline pattern.

Core flow:
```
# svelte-framework primary flow
input = prepare(raw_data)
result = process(input, config={actions, development, form, framework, rendering})
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


### Svelte 5 Component with Runes

```svelte
<script>
  let count = $state(0)
  let doubled = $derived(count * 2)

  $effect(() => {
    console.log(`Count changed to ${count}`)
  })

  function increment() {
    count++
  }
</script>

<button onclick={increment}>{count} (doubled: {doubled})</button>
```

### SvelteKit Load Function

```typescript
// src/routes/users/[id]/+page.server.ts
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ params, fetch }) => {
  const response = await fetch(`/api/users/${params.id}`)
  const user = await response.json()
  return { user }
}
```

### SvelteKit Form Action

```typescript
// src/routes/todos/+page.server.ts
import type { Actions } from './$types'

export const actions: Actions = {
  create: async ({ request, locals }) => {
    const data = await request.formData()
    const title = data.get('title') as string

    await locals.db.todos.create({ data: { title, userId: locals.user.id } })
    return { success: true }
  },

  delete: async ({ request, locals }) => {
    const data = await request.formData()
    await locals.db.todos.delete({ where: { id: data.get('id') } })
  },
}
```

```svelte
<!-- src/routes/todos/+page.svelte -->
<script>
  let { data } = $props()
</script>

{#each data.todos as todo}
  <form method="POST" action="?/delete">
    <span>{todo.title}</span>
    <input type="hidden" name="id" value={todo.id} />
    <button>Delete</button>
  </form>
{/each}

<form method="POST" action="?/create">
  <input name="title" required />
  <button>Add</button>
</form>
```

### Streaming

```typescript
// Slow data streams to client as it resolves
export const load = async ({ fetch }) => {
  return {
    streamed: {
      analytics: fetch('/api/analytics').then(r => r.json()),
    },
  }
}
```

```svelte
{#await data.streamed.analytics}
  <p>Loading analytics...</p>
{:then analytics}
  <Dashboard data={analytics} />
{/await}
```

## Common Patterns

- **Form actions**: Progressive enhancement, works without JS
- **Streaming**: Stream slow data to avoid blocking page load
- **Runes**: Fine-grained reactivity without virtual DOM overhead
- **Adapter deployment**: Swap adapters for different hosts
- **Layout groups**: Shared layouts with `(group)` directories

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