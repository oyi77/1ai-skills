---
name: postcss-plugins
description: PostCSS plugin ecosystem — Autoprefixer, cssnano, nesting, custom plugins, preset configuration
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

## Pseudo Code

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
