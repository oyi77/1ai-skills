---
name: accessibility-audit
description: WCAG compliance audit — semantic HTML, ARIA, keyboard navigation, color contrast, and screen reader testing
---



## Overview

Accessibility (a11y) audit framework for WCAG 2.1 compliance. Covers semantic HTML, ARIA attributes, keyboard navigation, color contrast, focus management, and screen reader testing.

## Capabilities

- Audit pages against WCAG 2.1 AA criteria
- Check semantic HTML structure and heading hierarchy
- Verify keyboard navigation and focus management
- Test color contrast ratios (4.5:1 normal, 3:1 large text)
- Validate ARIA attributes and screen reader experience

## When to Use

- Before launching any public-facing UI
- Legal compliance requirements (ADA, EAA)
- User complaints about accessibility
- Adding keyboard navigation support

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The accessibility-audit workflow follows a standard pipeline pattern.

Core flow:
```
# accessibility-audit primary flow
input = prepare(raw_data)
result = process(input, config={accessibility, aria, audit, color, compliance})
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


### Core Workflow
```
# accessibility-audit primary flow
input = prepare(raw_data)
result = process(input, config={accessibility, aria, audit, color, compliance})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Automated Audit
```python
def audit_accessibility(url):
    results = {
        "headings": check_heading_hierarchy(url),  # h1 > h2 > h3, no skips
        "images": check_alt_text(url),  # All images have alt
        "contrast": check_color_contrast(url),  # 4.5:1 minimum
        "keyboard": check_tab_order(url),  # All interactive elements reachable
        "aria": check_aria_labels(url),  # Buttons, links have accessible names
        "forms": check_form_labels(url),  # All inputs have labels
    }
    return generate_report(results, level="AA")
```

### Manual Checklist
```markdown
- [ ] Page has exactly one h1
- [ ] All images have descriptive alt text
- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicator is visible on all focusable elements
- [ ] Color is not the only way to convey information
- [ ] Form inputs have associated labels
- [ ] Error messages are announced to screen readers
```

## Common Patterns

- **Semantic first**: Use `<button>` not `<div onclick>`, `<nav>` not `<div class="nav">`
- **Skip links**: Add "Skip to content" link for keyboard users
- **Focus visible**: Never `outline: none` without replacement
- **ARIA sparingly**: Native HTML > ARIA. Only use ARIA when no semantic equivalent exists.

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing
