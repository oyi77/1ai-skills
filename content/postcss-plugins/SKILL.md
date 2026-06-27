---
name: postcss-plugins
description: PostCSS plugin ecosystem — Autoprefixer, cssnano, nesting, custom plugins, preset configuration
domain: content
tags:
- content-creation
- digital-content
- media
- plugins
- postcss
---



## Overview

PostCSS is a CSS transformation tool with a rich plugin ecosystem. Autoprefixer adds vendor prefixes, cssnano minifies, nesting enables CSS nesting, and custom plugins can transform CSS in any way.

## Capabilities

- Autoprefixer for vendor prefix management
- cssnano for CSS minification and optimization
- CSS nesting support (native and polyfill)
- Custom PostCSS plugin development
- Preset-env for modern CSS features
- Source map support and watch mode

## When to Use

- Need vendor prefix automation
- Want CSS minification as part of build pipeline
- Using CSS nesting before browser support is universal
- Building custom CSS transformation tools
- Using modern CSS features with fallbacks

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The postcss-plugins workflow follows a standard pipeline pattern.

Core flow:
```
# postcss-plugins primary flow
input = prepare(raw_data)
result = process(input, config={autoprefixer, configuration, cssnano, custom, ecosystem})
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
# postcss-plugins primary flow
input = prepare(raw_data)
result = process(input, config={autoprefixer, configuration, cssnano, custom, ecosystem})
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


### Configuration
```js
// postcss.config.js
module.exports = {
  plugins: {
    "postcss-import": {},
    "postcss-nesting": {},
    "postcss-preset-env": {
      stage: 2,
      features: {
        "nesting-rules": false, // using postcss-nesting instead
      },
    },
    autoprefixer: {},
    cssnano: process.env.NODE_ENV === "production" ? {} : false,
  },
}
```

### Autoprefixer Config
```js
// .browserslistrc
> 0.5%
last 2 versions
not dead
not ie 11
```

### Custom Plugin
```js
// postcss-plugin-example.js
module.exports = (opts = {}) => {
  return {
    postcssPlugin: "postcss-add-prefix",
    Declaration(decl) {
      if (decl.prop.startsWith("my-")) {
        decl.prop = `--custom-${decl.prop.slice(3)}`
      }
    },
  }
}
module.exports.postcss = true
```

### CSS Nesting
```css
/* Input */
.card {
  background: white;
  & .title {
    font-size: 1.5rem;
    &:hover {
      color: blue;
    }
  }
  @media (max-width: 768px) {
    padding: 1rem;
  }
}

/* Output (after postcss-nesting) */
.card { background: white; }
.card .title { font-size: 1.5rem; }
.card .title:hover { color: blue; }
@media (max-width: 768px) { .card { padding: 1rem; } }
```

### preset-env Features
```css
/* Modern CSS with fallbacks */
.card {
  color: oklch(60% 0.2 250);           /* oklch color */
  container-type: inline-size;           /* container queries */
  text-wrap: balance;                    /* text balancing */
  &:has(> img) { grid-template-columns: 1fr 2fr; }  /* :has() selector */
}
```

## Common Patterns

- **Preset-env stages**: Stage 0 (experimental) → Stage 3 (nearly stable)
- **Plugin order**: import → nesting → preset-env → autoprefixer → cssnano
- **Conditional plugins**: `cssnano: production ? {} : false` to skip in dev
- **Source maps**: `map: { inline: false }` in config
- **Watch mode**: `postcss src/**/*.css -o dist/ --watch --map`

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

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Good enough content works" | Quality content drives engagement. Mediocre content gets ignored. |
| "I will optimize later" | SEO and distribution need optimization from the start. |
| "Templates are good enough" | Templates are a starting point. Custom content outperforms generic. |