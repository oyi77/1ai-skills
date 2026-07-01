---
name: svelte-patterns
description: Svelte 5 and SvelteKit development patterns — runes, stores, server-side rendering, form actions, edge deployment. Use when working with svelte patterns.
domain: development
tags:
- coding
- patterns
- software-engineering
- svelte
- testing
---


## Overview

Svelte 5 introduces runes (`$state`, `$derived`, `$effect`) replacing the old reactive syntax. SvelteKit provides SSR/SSG with file-based routing, form actions, and server-side load functions.

## Capabilities

- Svelte 5 runes for fine-grained reactivity
- SvelteKit file-based routing with layouts and groups
- Form actions for progressive enhancement
- Server-side load functions and streaming
- Edge deployment with adapters (Vercel, Cloudflare, Node)

## When to Use
**Trigger phrases:**
- "svelte patterns"
- "Svelte 5 and SvelteKit development patterns — runes, stores, server-side renderi"


- Building reactive UIs with minimal boilerplate
- Need SSR/SSG with SvelteKit
- Building forms that work without JavaScript
- Deploying to edge runtimes

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The svelte-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# svelte-patterns primary flow
input = prepare(raw_data)
result = process(input, config={actions, deployment, development, edge, form})
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


### Svelte 5 runes
```svelte
<script>
  // State
  let count = $state(0);
  let name = $state('world');

  // Derived
  let greeting = $derived(`Hello ${name}! Count: ${count}`);

  // Effect
  $effect(() => {
    console.log(`Count changed to ${count}`);
    localStorage.setItem('count', String(count));
  });

  // Props (runes syntax)
  let { title, items = [] } = $props();
</script>

<h1>{title}</h1>
<p>{greeting}</p>
<button onclick={() => count++}>Increment</button>
```

### SvelteKit form action
```typescript
// src/routes/login/+page.server.ts
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const email = data.get('email') as string;
    const password = data.get('password') as string;

    const user = await authenticate(email, password);
    if (!user) return fail(400, { error: 'Invalid credentials' });

    cookies.set('session', user.token, { path: '/', httpOnly: true });
    redirect(303, '/dashboard');
  }
};
```

### SvelteKit load function
```typescript
// src/routes/products/+page.server.ts
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ url, fetch }) => {
  const page = Number(url.searchParams.get('page') ?? 1);
  const res = await fetch(`/api/products?page=${page}`);
  const { products, total } = await res.json();
  return { products, total, page };
};
```

### Component with slots and events
```svelte
<!-- Card.svelte -->
<script>
  let { title, children } = $props();
</script>

<div class="card">
  <h2>{title}</h2>
  <div class="content">
    {@render children()}
  </div>
</div>
```

## Common Patterns

- **$state.raw**: Non-deep-reactive state for large arrays/objects
- **$effect.cleanup**: Cleanup side effects when component unmounts
- **Layout groups**: `(app)` and `(auth)` route groups for different layouts
- **Streaming**: Return promises from load functions for progressive loading
- **Hooks**: `handle` for middleware, `handleError` for error reporting

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