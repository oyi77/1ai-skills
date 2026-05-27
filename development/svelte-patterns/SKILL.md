---
name: svelte-patterns
description: Svelte 5 and SvelteKit development patterns — runes, stores, server-side rendering, form actions, edge deployment
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

- Building reactive UIs with minimal boilerplate
- Need SSR/SSG with SvelteKit
- Building forms that work without JavaScript
- Deploying to edge runtimes

## Pseudo Code

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
