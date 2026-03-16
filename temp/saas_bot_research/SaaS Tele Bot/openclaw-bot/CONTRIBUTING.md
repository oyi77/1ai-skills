# Contributing to OpenClaw Bot

Terima kasih atas minat Anda untuk berkontribusi pada OpenClaw Bot! Dokumen ini berisi panduan untuk kontribusi yang efektif.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)
- [Release Process](#release-process)

---

## 📜 Code of Conduct

### Our Standards

- **Respectful**: Hormati pendapat dan pengalaman orang lain
- **Constructive**: Berikan feedback yang membangun
- **Professional**: Jaga profesionalisme dalam komunikasi
- **Inclusive**: Sambut kontributor dari berbagai latar belakang

### Unacceptable Behavior

- Diskriminasi atau pelecehan
- Trolling atau komentar tidak pantas
- Pelanggaran privasi
- Perilaku tidak profesional lainnya

---

## 🚀 Getting Started

### Prerequisites

```bash
# Node.js 20+
node --version  # v20.x.x

# npm 10+
npm --version   # 10.x.x

# Git
git --version   # 2.x.x

# Docker (optional)
docker --version
```

### Setup Development Environment

```bash
# 1. Fork repository
# Click "Fork" button on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/openclaw-bot.git
cd openclaw-bot

# 3. Add upstream remote
git remote add upstream https://github.com/openclaw/bot.git

# 4. Install dependencies
npm install

# 5. Setup environment
cp .env.example .env
# Edit .env dengan konfigurasi lokal Anda

# 6. Run database migrations
npm run migrate:dev

# 7. Start development server
npm run dev
```

### Verify Setup

```bash
# Run tests
npm test

# Run linter
npm run lint

# Check types
npm run typecheck
```

---

## 🔄 Development Workflow

### Branch Naming Convention

```
feature/short-description     # New features
bugfix/issue-number           # Bug fixes
hotfix/critical-issue         # Critical production fixes
docs/description              # Documentation updates
refactor/description          # Code refactoring
test/description              # Test additions/updates
chore/description             # Maintenance tasks
```

### Workflow Steps

```bash
# 1. Sync dengan upstream
git checkout main
git pull upstream main
git push origin main

# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make changes
# ... edit files ...

# 4. Commit changes
git add .
git commit -m "feat: add amazing feature"

# 5. Push to your fork
git push origin feature/amazing-feature

# 6. Create Pull Request
# Via GitHub UI
```

---

## 💻 Coding Standards

### TypeScript/JavaScript

```typescript
// ✅ Good
interface UserConfig {
  id: string;
  name: string;
  isActive: boolean;
}

function processUser(config: UserConfig): void {
  if (!config.isActive) {
    return;
  }
  
  console.log(`Processing ${config.name}`);
}

// ❌ Bad
function processuser(cfg) {
  if(cfg.isactive==false)return
  console.log("Processing "+cfg.name)
}
```

### Code Style Rules

| Rule | Config |
|------|--------|
| Indentation | 2 spaces |
| Quotes | Single |
| Semicolons | Required |
| Line length | 100 chars |
| Trailing commas | Required |

### ESLint + Prettier

```bash
# Run linter
npm run lint

# Fix auto-fixable issues
npm run lint:fix

# Format code
npm run format
```

### File Organization

```
src/
├── commands/           # Telegram bot commands
│   ├── start.ts
│   ├── create.ts
│   ├── topup.ts
│   └── ...
├── handlers/           # Event handlers
│   ├── message.ts
│   ├── callback.ts
│   └── error.ts
├── services/           # Business logic
│   ├── video/
│   ├── payment/
│   ├── user/
│   └── ...
├── models/             # Database models
│   ├── user.ts
│   ├── transaction.ts
│   └── ...
├── utils/              # Utilities
│   ├── logger.ts
│   ├── validator.ts
│   └── ...
├── middleware/         # Express/Telegraf middleware
│   ├── auth.ts
│   ├── rateLimit.ts
│   └── ...
├── config/             # Configuration
│   ├── database.ts
│   ├── redis.ts
│   └── ...
└── types/              # TypeScript types
    ├── index.ts
    └── telegram.ts
```

---

## 🧪 Testing

### Test Structure

```
tests/
├── unit/               # Unit tests
│   ├── commands/
│   ├── services/
│   └── utils/
├── integration/        # Integration tests
│   ├── database/
│   ├── payment/
│   └── queue/
├── e2e/                # End-to-end tests
│   └── telegram/
└── fixtures/           # Test data
```

### Writing Tests

```typescript
// Example unit test
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

### Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- src/services/credit.test.ts

# Run in watch mode
npm run test:watch

# Run E2E tests
npm run test:e2e
```

### Coverage Requirements

| Type | Minimum Coverage |
|------|------------------|
| Statements | 80% |
| Branches | 75% |
| Functions | 80% |
| Lines | 80% |

---

## 📝 Documentation

### Code Documentation

```typescript
/**
 * Calculates credit cost for video generation
 * @param params - Video parameters
 * @param params.duration - Video duration in seconds
 * @param params.scenes - Number of scenes
 * @returns Credit cost (0.5 - 4.0)
 * @throws {ValidationError} If parameters are invalid
 * 
 * @example
 * ```typescript
 * const cost = calculateCredits({ duration: 30, scenes: 5 });
 * console.log(cost); // 1
 * ```
 */
function calculateCredits(params: {
  duration: number;
  scenes: number;
}): number {
  // Implementation
}
```

### README Updates

Update README.md jika Anda menambahkan:
- Fitur baru yang signifikan
- Breaking changes
- Dependencies baru
- Environment variables baru

### Changelog

Tambahkan entry ke CHANGELOG.md mengikuti format:

```markdown
### Added
- Description of new feature (#PR_NUMBER)

### Fixed
- Description of bug fix (#PR_NUMBER)
```

---

## 💬 Commit Messages

### Conventional Commits

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Code style (no logic change) |
| `refactor` | Code refactoring |
| `test` | Tests |
| `chore` | Maintenance |
| `perf` | Performance |
| `security` | Security |

### Examples

```bash
# Feature
feat(payment): add Tripay gateway integration

# Bug fix
fix(queue): handle job timeout gracefully

# Documentation
docs(api): update webhook documentation

# Refactoring
refactor(database): optimize user queries

# Test
test(video): add generation pipeline tests

# Security
security(auth): implement rate limiting
```

### Scopes

- `bot` - Telegram bot core
- `payment` - Payment system
- `video` - Video generation
- `user` - User management
- `queue` - Job queue
- `db` - Database
- `api` - API endpoints
- `auth` - Authentication
- `config` - Configuration
- `docs` - Documentation

---

## 🔀 Pull Requests

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] No breaking changes (or documented)

## Testing
How to test these changes

## Screenshots (if applicable)
```

### PR Process

1. **Create PR** dari feature branch ke `main`
2. **Fill template** dengan lengkap
3. **Link issues** (Fixes #123)
4. **Request review** dari minimal 2 reviewers
5. **Address feedback**
6. **CI checks pass**
7. **Merge** (squash and merge)

### Review Criteria

- [ ] Code quality
- [ ] Test coverage
- [ ] Documentation
- [ ] Performance impact
- [ ] Security implications
- [ ] Breaking changes

---

## 🏷️ Release Process

### Version Bumping

```bash
# Patch (bug fixes)
npm version patch  # 3.0.0 -> 3.0.1

# Minor (features)
npm version minor  # 3.0.0 -> 3.1.0

# Major (breaking)
npm version major  # 3.0.0 -> 4.0.0
```

### Release Checklist

- [ ] All tests pass
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Tag created
- [ ] Release notes drafted
- [ ] Deployed to staging
- [ ] Smoke tests passed
- [ ] Deployed to production
- [ ] Monitoring confirmed

---

## 🆘 Getting Help

### Resources

- [Documentation](https://docs.openclaw.ai)
- [Discord](https://discord.gg/openclaw)
- [GitHub Discussions](https://github.com/openclaw/bot/discussions)

### Questions?

- General: [GitHub Discussions](https://github.com/openclaw/bot/discussions)
- Bugs: [GitHub Issues](https://github.com/openclaw/bot/issues)
- Security: `security@openclaw.ai`

---

## 🙏 Recognition

Kontributor akan diakui di:
- README.md Contributors section
- Release notes
- Hall of Fame (significant contributions)

---

**Terima kasih telah berkontribusi!** 🎉
