---
name: ui-critique
description: Structured UI review — visual hierarchy, consistency, accessibility, and actionable improvement feedback
---

## Overview

Structured framework for reviewing UI designs. Evaluates visual hierarchy, consistency, accessibility, spacing, typography, color usage, and provides actionable improvement recommendations.

## Capabilities

- Analyze visual hierarchy and information architecture
- Check consistency across components and pages
- Evaluate accessibility (contrast, focus states, semantic HTML)
- Review responsive behavior across breakpoints
- Provide specific, actionable improvement recommendations

## When to Use

- Before launching a new UI or redesign
- Onboarding a new team member to design standards
- User complaints about usability or confusion
- Pre-launch design review checklist

## Pseudo Code

### Critique Framework
```python
def critique_ui(screenshot, url):
    checks = {
        "visual_hierarchy": check_hierarchy(screenshot),  # Can user find CTA in 3s?
        "consistency": check_spacing_and_colors(screenshot),  # Same patterns everywhere?
        "contrast": check_color_contrast(screenshot),  # WCAG AA compliant?
        "responsive": check_mobile_view(url),  # Works on 320px?
        "loading": check_performance(url),  # LCP < 2.5s?
        "accessibility": check_aria_and_semantics(url)  # Screen reader friendly?
    }
    return generate_report(checks)
```

## Common Patterns

- **3-second test**: Can user identify the primary action in 3 seconds?
- **Squint test**: Blur the UI — does the hierarchy still work?
- **Contrast check**: All text meets WCAG AA (4.5:1 for normal text)
- **Spacing audit**: Consistent spacing between similar elements
