---
name: visual-regression
description: Visual regression testing — screenshot comparison, baseline management, and UI change detection
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

## Pseudo Code

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
