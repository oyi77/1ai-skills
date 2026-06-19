# Ponytail Skills — Lazy Senior Dev Mode

**Source**: [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT License)  
**Integrated**: 2026-06-18  
**Maintainer**: @oyi77 (BerkahKarya)

---

## Overview

Ponytail enforces a "lazy senior dev" mindset: YAGNI, stdlib-first, no unrequested abstractions. The best code is the code never written.

**Benefits for OmniRoute**:
- Reduces over-engineering in multi-provider routing logic
- Prevents premature abstraction in adapter patterns
- Enforces deletion over addition when refactoring
- Cuts boilerplate in SSE streaming and fallback chains

**Metrics** (from upstream benchmarks):
- 80-94% less code per task
- 3-6× faster implementation
- 42-75% cheaper token usage

---

## Available Skills

### Core

| Skill | Path | Use When |
|-------|------|----------|
| **ponytail** | `skill://ponytail` | Default mode for all implementation tasks |

**Modes**: `/ponytail lite\|full\|ultra`  
**Persistence**: Active every response unless explicitly disabled with "stop ponytail" or "normal mode"

### Specialized

| Skill | Path | Use When |
|-------|------|----------|
| **ponytail-review** | `skill://ponytail-review` | Reviewing diffs for unnecessary complexity |
| **ponytail-audit** | `skill://ponytail-audit` | Auditing existing codebases for deletion candidates |
| **ponytail-debt** | `skill://ponytail-debt` | Quantifying and prioritizing tech debt removal |
| **ponytail-help** | `skill://ponytail-help` | Quick reference for Ponytail rules and ladder |

---

## The Ladder

Stop at the first rung that holds:

1. **Does this need to exist at all?** → YAGNI. Skip it.
2. **Stdlib does it?** → Use it.
3. **Native platform feature?** → `<input type="date">` over a picker lib.
4. **Already-installed dependency?** → Use it. Never add new deps for what a few lines can do.
5. **Can it be one line?** → One line.
6. **Only then**: Minimum code that works.

---

## Integration with OmniRoute

### High-Value Targets

1. **Provider Adapters** (`omniroute-provider/`)
   - 40+ chat providers with repetitive error handling
   - Opportunity: Extract common patterns to stdlib utils, delete per-provider boilerplate

2. **SSE Streaming** (`open-sse/services/`)
   - Complex keepalive and fallback logic
   - Opportunity: Simplify state machines, remove speculative retry paths

3. **Routing Logic** (`omniroute-gate/`)
   - Multi-tier fallback chains with nested config
   - Opportunity: Flatten decision trees, delete unused routing strategies

4. **Type Definitions** (all `src/types/`)
   - Overlapping interfaces and wrapper types
   - Opportunity: Consolidate to minimal shared types, delete one-use interfaces

### Recommended Workflow

1. **New Features**: Activate `skill://ponytail` by default
2. **Refactoring**: Run `skill://ponytail-audit` first to identify deletion targets
3. **PR Reviews**: Use `skill://ponytail-review` to catch over-engineering
4. **Tech Debt**: Use `skill://ponytail-debt` to prioritize cleanup

---

## Examples

### Before (Typical AI Agent Output)
```typescript
// 50 lines: custom date validator, timezone handling, format config
class DateValidator {
  private formats: string[];
  private timezone: string;
  constructor(config: DateValidatorConfig) { /* ... */ }
  validate(date: string): ValidationResult { /* ... */ }
}
```

### After (Ponytail Mode)
```typescript
// 1 line: Date.parse() handles it, real validation is user confirmation
const isValid = !isNaN(Date.parse(dateStr));
```

---

## Rules (Enforced by Skills)

- **No unrequested abstractions**: No interface with one implementation, no factory for one product
- **No boilerplate**: No scaffolding "for later"
- **Deletion over addition**: Remove > refactor > add
- **Boring over clever**: Cleverness is decoded at 3am
- **Fewest files possible**: Shortest working diff wins
- **Ship lazy version first**: Optimize only when measured need exists

---

## Deactivation

Skills persist across responses. To disable:
- `"stop ponytail"` or `"normal mode"` in user message
- Agent will acknowledge and return to default behavior

---

## Upstream

**Repository**: https://github.com/DietrichGebert/ponytail  
**Stars**: 34,502  
**Compatible With**: Claude, Cursor, Windsurf, OpenClaw, GitHub Copilot, and 8 other agents

---

## Local Modifications

None yet. Using upstream skills verbatim. Any future customizations for OmniRoute-specific patterns will be documented here.

---

**Last Updated**: 2026-06-18  
**Next Review**: When we accumulate OmniRoute-specific deletion patterns worth codifying
