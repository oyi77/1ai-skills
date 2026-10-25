---
name: type-narrowing-audit
description: Auditing and replacing unsafe any types, untyped catch blocks, unvalidated external payloads, and blind type assertions with strict type narrowing. Use when upgrading TypeScript or Python strictness, eliminating runtime type crashes, or securing data boundaries.
domain: development
subdomain: software-development
author: oyi77
license: Apache-2.0
version: 1.0.0
category: development
tags:
  - typescript
  - python
  - type-safety
  - runtime-validation
  - type-narrowing
  - defensive-programming
---

## Overview

Static type systems provide compile-time guarantees, but runtime crashes frequently occur at trust boundaries where data enters via JSON parsers, HTTP payloads, database queries, or catch clauses. The Type Narrowing Audit playbook establishes a zero-blind-assertion engineering standard, ensuring dynamic inputs are validated and safely narrowed before consumption.

## Anti-Rationalization Table

| Rationalization | Engineering Reality | Strict Protocol |
|---|---|---|
| "Using `as unknown as Type` is quick and gets past the compiler." | Double assertions lie to the compiler, suppressing typechecker warnings and deferring crashes to production runtime. | Never use blind type assertions. Parse external payloads at runtime using Zod, Valibot, or Pydantic schemas. |
| "`any` is fine for internal glue code or quick prototypes." | Unchecked `any` is infectious: it disables type safety for all downstream callers and spreads untyped holes across the repo. | Ban `any` via linter (`@typescript-eslint/no-explicit-any: error`). Use `unknown` for unverified data and narrow before use. |
| "Remote APIs always match our TypeScript interface definition." | Upstream services drift, rename fields, omit optional values, or return error envelopes instead of expected schemas. | Validate every inbound HTTP and webhook payload at runtime before accessing properties. |
| "TypeScript type annotations run at runtime and validate inputs." | TypeScript types are completely erased at compile time; an unvalidated type annotation provides zero runtime defense. | Pair compile-time types with runtime schema validators or user-defined type guards (`is` operator). |
| "A generic `catch (err)` block does not need type narrowing." | Caught errors in TypeScript are typed as `unknown` because JavaScript can throw non-Error objects (strings, numbers, null). | Always narrow caught errors using `err instanceof Error ? err.message : String(err)` before reading properties. |
| "Type guards are too verbose for simple property checks." | Incomplete property checks (`obj.foo`) trigger `TypeError: Cannot read properties of undefined` when `obj` is nullish. | Use discriminated unions with exhaustive `never` switches or validated schema parsers for complex variants. |

## When to Use

- Migrating codebases to strict typechecking (`"strict": true`, `"noImplicitAny": true`, `mypy --strict`).
- Hardening API endpoints, webhook receivers, and event consumers against malformed input payloads.
- Diagnosing and eliminating recurring `TypeError: Cannot read properties of undefined` in production logs.
- Upgrading legacy JavaScript codebases to modern type-safe TypeScript or Python typed architectures.

## When NOT to Use

- High-performance binary stream processing or WebAssembly interop where schema parsing overhead is prohibitive.
- Quick single-run scratchpad scripts where type safety provides no long-term maintenance benefit.
- Static internal code paths where data has already passed through validated ingress gates and remained immutable.

## Workflow

```
┌────────────────────────────────────────────────────────┐
│             Type Narrowing Audit Workflow              │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 1. Ingress Boundary & Any-Leak Identification          │
│    - Scan for `any`, `as`, untyped catches, raw JSON   │
│    - Inventory all unvalidated external data sources   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 2. Runtime Schema Validation at Trust Boundaries       │
│    - Define Zod / Valibot / Pydantic schemas for I/O   │
│    - Replace blind type casts with `schema.safeParse`  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 3. Discriminated Unions & Exhaustive Matching          │
│    - Tag polymorphic payloads with a literal `type` tag│
│    - Use `never` check to ensure all variants handled  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 4. Defensive Catch Block & Error Narrowing             │
│    - Guard caught exceptions with `instanceof Error`   │
│    - Extract error messages and stack traces safely    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 5. Compiler Strict Mode Verification                   │
│    - Enable strict compiler flags across all modules   │
│    - Prove 100% clean typecheck without assertions     │
└───────────────────────────┘
```

### Step 1: Ingress Boundary & Any-Leak Identification
Run automated scans to locate unvalidated inputs and unsafe assertions:
- Search for explicit `any`: `git grep -E ":\s*any\b" "src/"`
- Search for double-casting: `git grep "as unknown as"`
- Search for raw JSON parsing without validation: `JSON.parse(` without subsequent schema parsing.

### Step 2: Runtime Schema Validation at Trust Boundaries
Wrap every inbound data source in a runtime parser:
- API endpoints: Validate `req.body`, `req.query`, `req.params`.
- External HTTP responses: Parse `res.data` before passing into application layers.
- Database outputs: Validate untyped JSON columns.

### Step 3: Discriminated Unions & Exhaustive Matching
Model multi-state domain entities with discriminated unions:
- Assign a constant discriminator field (e.g. `status: 'idle' | 'loading' | 'success' | 'error'`).
- Use switch statements with an `assertNever` helper to guarantee exhaustive compilation checks.

### Step 4: Defensive Catch Block & Error Narrowing
Audit all error handlers:
- Replace `catch (err: any)` with standard `catch (err: unknown)`.
- Use helper functions like `toError(err)` or `getErrorMessage(err)` to safely unpack errors.

### Step 5: Compiler Strict Mode Verification
Lock in type safety configuration:
- In TypeScript: Enable `"strict": true`, `"noUncheckedIndexedAccess": true`.
- In Python: Run `mypy --strict` or `pyright`.

## Code Examples

### TypeScript Runtime Validation & Boundary Narrowing (Zod)

```typescript
import { z } from 'zod';

export const UserProfileSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  role: z.enum(['admin', 'member', 'guest']),
  metadata: z.record(z.string(), z.unknown()).default({}),
  createdAt: z.string().datetime().transform((val) => new Date(val)),
});

export type UserProfile = z.infer<typeof UserProfileSchema>;

// Ingress handler: Safe parsing without throwing
export function parseInboundUser(rawPayload: unknown): UserProfile {
  const result = UserProfileSchema.safeParse(rawPayload);

  if (!result.success) {
    const errorDetails = result.error.errors
      .map((e) => `${e.path.join('.')}: ${e.message}`)
      .join(', ');
    throw new Error(`Invalid user payload boundary violation: ${errorDetails}`);
  }

  // Compiler now strictly knows result.data is UserProfile
  return result.data;
}
```

### Discriminated Union with Exhaustive Compile-Time Check

```typescript
export type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'pending' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

export function assertNever(value: never): never {
  throw new Error(`Unhandled discriminated union variant: ${JSON.stringify(value)}`);
}

export function renderAsyncState<T>(state: AsyncState<T>): string {
  switch (state.status) {
    case 'idle':
      return 'Waiting to start';
    case 'pending':
      return 'Loading...';
    case 'success':
      return `Loaded data successfully`;
    case 'error':
      return `Error: ${state.error.message}`;
    default:
      // If a new status is added to AsyncState, this line fails to compile!
      return assertNever(state);
  }
}
```

### Safe Catch-Block Error Narrowing Helper

```typescript
export function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  if (typeof error === 'string') {
    return error;
  }
  if (error !== null && typeof error === 'object' && 'message' in error) {
    return String((error as { message: unknown }).message);
  }
  try {
    return JSON.stringify(error);
  } catch {
    return String(error);
  }
}

// Usage in async service
try {
  await performCriticalNetworkRequest();
} catch (error: unknown) {
  const message = getErrorMessage(error);
  logger.error({ error, message }, 'Network request failed');
}
```

### Python TypeGuard and Pydantic Runtime Narrowing

```python
from typing import Any, Dict, TypeGuard, Union
from pydantic import BaseModel, EmailStr, ValidationError

class UserPayload(BaseModel):
    id: str
    email: EmailStr
    is_active: bool

def is_dict_payload(val: Any) -> TypeGuard[Dict[str, Any]]:
    return isinstance(val, dict)

def validate_inbound_data(raw_input: Union[Dict[str, Any], Any]) -> UserPayload:
    if not is_dict_payload(raw_input):
        raise ValueError("Expected dictionary payload")

    try:
        return UserPayload.model_validate(raw_input)
    except ValidationError as err:
        raise ValueError(f"Schema mismatch: {err.errors()}") from err
```

## Verification Checklist

- [ ] All `any` types replaced with `unknown` or specific domain interfaces.
- [ ] No double type assertions (`as unknown as Target`) present in production code.
- [ ] External HTTP, webhook, and database JSON inputs validated with runtime schemas (Zod, Pydantic).
- [ ] Caught errors typed as `unknown` and safely narrowed with `instanceof Error`.
- [ ] Discriminated unions verified with exhaustive compile-time `never` checks.
- [ ] `tsc --noEmit` and `mypy` pass with strict checking enabled.
