---
name: vue-framework
description: Vue.js 3 development — Composition API, Pinia, Vue Router, Nuxt, SSR/SSG patterns. Use when working with vue framework.
domain: development
tags:
- api
- coding
- framework
- software-engineering
- testing
- vue
---


## Overview

Build modern web applications with Vue.js 3 — Composition API reactivity, Pinia state management, Vue Router, and Nuxt 3 for SSR/SSG.

## Capabilities

- Composition API (ref, reactive, computed, watch)
- Pinia stores with TypeScript
- Vue Router with nested routes and guards
- Nuxt 3 SSR/SSG with auto-imports
- Component patterns (slots, provide/inject, composables)
- Form handling and validation
- Testing with Vitest + Vue Test Utils

## When to Use
**Trigger phrases:**
- "vue framework"
- "Vue"


- Building single-page applications (SPAs)
- Server-side rendered apps (Nuxt 3)
- Static site generation (Nuxt SSG)
- Admin dashboards and internal tools
- Progressive web apps

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The vue-framework workflow follows a standard pipeline pattern.

Core flow:
```
# vue-framework primary flow
input = prepare(raw_data)
result = process(input, config={composition, development, framework, nuxt, patterns})
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


### Composition API Component

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'

const items = ref([])
const filter = ref('')
const loading = ref(false)

const filteredItems = computed(() =>
  items.value.filter(i => i.name.includes(filter.value))
)

onMounted(async () => {
  loading.value = true
  items.value = await fetch('/api/items').then(r => r.json())
  loading.value = false
})
</script>

<template>
  <input v-model="filter" placeholder="Search..." />
  <div v-if="loading">Loading...</div>
  <ul v-else>
    <li v-for="item in filteredItems" :key="item.id">{{ item.name }}</li>
  </ul>
</template>
```

### Pinia Store

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const double = computed(() => count.value * 2)
  function increment() { count.value++ }
  return { count, double, increment }
})
```

### Vue Router

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('@/pages/Home.vue') },
    { path: '/user/:id', component: () => import('@/pages/User.vue'), props: true },
    {
      path: '/admin',
      component: () => import('@/pages/Admin.vue'),
      beforeEnter: (to, from) => {
        if (!useAuth().isAdmin) return '/login'
      },
    },
  ],
})
```

### Nuxt 3 Page with SSR

```vue
<!-- pages/users/[id].vue -->
<script setup>
const route = useRoute()
const { data: user } = await useFetch(`/api/users/${route.params.id}`)
</script>

<template>
  <div>
    <h1>{{ user.name }}</h1>
    <p>{{ user.email }}</p>
  </div>
</template>
```

## Common Patterns

- **Composables**: Extract reusable logic into `use*` functions
- **Auto-imports**: Nuxt 3 auto-imports Vue APIs and components
- **Dynamic imports**: Lazy-load routes with `() => import()`
- **Provide/Inject**: Share data across component trees
- **Suspense**: Handle async components with loading states

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