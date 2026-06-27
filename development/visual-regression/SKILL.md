---
name: visual-regression
description: Visual regression testing — screenshot comparison, baseline management, and UI change detection
domain: development
tags:
- coding
- regression
- software-engineering
- testing
- visual
---


## Overview

Detect unintended visual changes by comparing screenshots against baselines. Uses Playwright, Percy, or Chromatic for automated visual regression testing.

## Capabilities

- Capture and compare screenshots against baselines
- Detect pixel-level visual regressions
- Manage baselines across branches and environments
- Test responsive layouts at multiple viewport sizes
- Ignore dynamic content (animations, timestamps)

## When to Use

- After UI changes — verify nothing broke visually
- CSS refactoring — ensure visual parity
- Cross-browser visual consistency checks
- Design system component library testing

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The visual-regression workflow follows a standard pipeline pattern.

Core flow:
```
# visual-regression primary flow
input = prepare(raw_data)
result = process(input, config={baseline, change, comparison, detection, management})
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


### Playwright Visual Test
```typescript
test('homepage matches baseline', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixelRatio: 0.01,
    animations: 'disabled'
  })
})
```

### Responsive Visual Test
```typescript
const viewports = [
  { width: 320, height: 568, name: 'mobile' },
  { width: 768, height: 1024, name: 'tablet' },
  { width: 1440, height: 900, name: 'desktop' }
]

for (const vp of viewports) {
  test(`responsive ${vp.name}`, async ({ page }) => {
    await page.setViewportSize({ width: vp.width, height: vp.height })
    await page.goto('/')
    await expect(page).toHaveScreenshot(`${vp.name}.png`)
  })
}
```

## Common Patterns

- **Baseline per branch**: Different baselines for different feature branches
- **Ignore regions**: Mask dynamic content (ads, timestamps, animations)
- **Threshold tuning**: 0.01% max diff for strict, 1% for lenient
- **Full-page screenshots**: Capture full scrollable area, not just viewport

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