---
name: vue-patterns
description: Vue.js 3 development patterns — Composition API, Pinia state management, Vue Router, Nuxt.js, component architecture. Use when working with vue patterns.
domain: development
tags:
- api
- coding
- patterns
- software-engineering
- testing
- vue
---


## Overview

Vue.js 3 patterns for building modern web applications. Covers Composition API, Pinia state management, Vue Router, Nuxt.js SSR/SSG, and component architecture best practices.

## Capabilities

- Composition API with composables for reusable logic
- Pinia store design (setup stores, options stores)
- Vue Router with nested routes, guards, and lazy loading
- Nuxt.js SSR/SSG with server routes and middleware
- Performance optimization (shallowRef, v-memo, lazy components)

## When to Use
**Trigger phrases:**
- "vue patterns"
- "Vue"


- Building Vue 3 applications or migrating from Vue 2
- Designing state management with Pinia
- Setting up Nuxt.js projects with SSR/SSG
- Creating reusable composables and component libraries

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The vue-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# vue-patterns primary flow
input = prepare(raw_data)
result = process(input, config={architecture, component, composition, development, management})
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


### Composition API composable
```typescript
// composables/useApi.ts
import { ref, watchEffect } from 'vue'

export function useApi<T>(url: Ref<string>) {
  const data = ref<T | null>(null)
  const error = ref<Error | null>(null)
  const loading = ref(false)

  watchEffect(async () => {
    loading.value = true
    try {
      const res = await fetch(url.value)
      data.value = await res.json()
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  })

  return { data, error, loading }
}
```

### Pinia store (setup syntax)
```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const users = ref<User[]>([])
  const currentUser = ref<User | null>(null)

  const activeUsers = computed(() => users.value.filter(u => u.active))

  async function fetchUsers() {
    users.value = await api.getUsers()
  }

  function setCurrentUser(user: User) {
    currentUser.value = user
  }

  return { users, currentUser, activeUsers, fetchUsers, setCurrentUser }
})
```

### Nuxt.js page with server route
```vue
<!-- pages/users/[id].vue -->
<script setup lang="ts">
const route = useRoute()
const { data: user } = await useFetch(`/api/users/${route.params.id}`)
</script>

<template>
  <div v-if="user">
    <h1>{{ user.name }}</h1>
    <p>{{ user.email }}</p>
  </div>
</template>
```

```typescript
// server/api/users/[id].ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')
  return await db.users.findById(id)
})
```

### Performance optimization
```vue
<script setup>
import { shallowRef, defineAsyncComponent } from 'vue'

// shallowRef for large objects (no deep reactivity)
const largeList = shallowRef(hugeArray)

// Lazy component loading
const HeavyComponent = defineAsyncComponent(() =>
  import('./HeavyComponent.vue')
)
</script>

<template>
  <!-- v-memo to skip re-renders -->
  <div v-for="item in largeList" :key="item.id" v-memo="[item.selected]">
    {{ item.name }}
  </div>
</template>
```

## Common Patterns

- **Composable extraction**: Extract reusable logic into `use*` composables
- **Provide/inject**: Share data across component tree without props drilling
- **Template refs**: Access DOM elements with `ref()` in setup
- **Suspense**: Handle async components with `<Suspense>` fallback
- **Route middleware**: Auth guards via `defineNuxtRouteMiddleware`

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