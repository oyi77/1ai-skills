# Testing Guide

This directory contains all tests for the OpenClaw Bot project.

## 📁 Test Structure

```
tests/
├── unit/           # Unit tests for individual functions/modules
├── integration/    # Integration tests for component interactions
├── e2e/           # End-to-end tests for complete workflows
└── fixtures/      # Test data and mock objects
```

## 🧪 Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- tests/unit/example.test.ts

# Run in watch mode
npm run test:watch

# Run E2E tests
npm run test:e2e
```

## 📊 Coverage Requirements

| Type | Minimum Coverage |
|------|------------------|
| Statements | 80% |
| Branches | 75% |
| Functions | 80% |
| Lines | 80% |

## 📝 Writing Tests

### Unit Test Example

```typescript
import { describe, it, expect, jest } from '@jest/globals';
import { calculateCredits } from '@/services/credit';

describe('Credit Service', () => {
  describe('calculateCredits', () => {
    it('should calculate credits for 30s video', () => {
      const result = calculateCredits({ duration: 30, scenes: 5 });
      expect(result).toBe(1);
    });

    it('should throw error for invalid duration', () => {
      expect(() => calculateCredits({ duration: -1, scenes: 5 }))
        .toThrow('Invalid duration');
    });
  });
});
```

### Integration Test Example

```typescript
import { describe, it, expect, beforeAll, afterAll } from '@jest/globals';
import { initializeDatabase, disconnectDatabase } from '@/config/database';

describe('Database Integration', () => {
  beforeAll(async () => {
    await initializeDatabase();
  });

  afterAll(async () => {
    await disconnectDatabase();
  });

  it('should connect to database', async () => {
    // Test database connection
  });
});
```

## 🔧 Test Configuration

Test configuration is in `package.json` under the `jest` section.

---

*For more information, see [CONTRIBUTING.md](../CONTRIBUTING.md)*
