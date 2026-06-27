---
name: esbuild-bundler
description: esbuild bundler configuration — blazing fast JS/TS bundling, plugins, watch mode, minification
domain: development
tags:
- bundler
- coding
- esbuild
- software-engineering
- testing
---


## Overview

esbuild is an extremely fast JavaScript/TypeScript bundler and minifier written in Go. It's 10-100x faster than Webpack/Rollup for most builds. This skill covers API usage, CLI configuration, plugin development, and integration patterns.

## Capabilities

- Bundle JS/TS/CSS in milliseconds (not seconds)
- Tree shaking and dead code elimination
- Minification (JS, CSS, HTML)
- Source maps (inline, external, linked)
- Code splitting with dynamic imports
- Plugin system for custom transformations
- Watch mode for development
- JSX/TSX support (React, Vue, Svelte)
- CSS bundling and minification
- Library building (ESM, CJS, IIFE)

## When to Use

- Need fastest possible build times
- Building npm libraries
- CLI tools and Node.js applications
- CI/CD pipelines where build speed matters
- Custom bundler with plugin pipeline
- Replacing Webpack for simple to medium projects
- Building multiple entry points

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The esbuild-bundler workflow follows a standard pipeline pattern.

Core flow:
```
# esbuild-bundler primary flow
input = prepare(raw_data)
result = process(input, config={blazing, bundler, bundling, configuration, esbuild})
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


### API Usage
```javascript
// build.mjs
import * as esbuild from 'esbuild';

await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  outdir: 'dist',
  format: 'esm',
  platform: 'node',
  target: 'node20',
  sourcemap: true,
  minify: true,
  splitting: true,
  external: ['express', 'pg'], // Don't bundle these
  define: {
    'process.env.NODE_ENV': '"production"',
  },
});
```

### CLI Usage
```bash
# Basic bundle
esbuild src/index.ts --bundle --outfile=dist/index.js

# Watch mode
esbuild src/index.ts --bundle --outfile=dist/index.js --watch

# Minified with source maps
esbuild src/index.ts --bundle --minify --sourcemap --outfile=dist/index.js

# Multiple formats
esbuild src/index.ts --bundle --format=esm --outdir=dist/esm
esbuild src/index.ts --bundle --format=cjs --outdir=dist/cjs

# CSS bundling
esbuild src/styles.css --bundle --minify --outfile=dist/styles.css

# Library mode
esbuild src/lib.ts --bundle --format=esm --outfile=dist/lib.mjs --external:react
```

### Package.json Scripts
```json
{
  "scripts": {
    "build": "node build.mjs",
    "dev": "node build.mjs --watch",
    "build:lib": "esbuild src/index.ts --bundle --format=esm,cjs --outdir=dist --external:react --external:react-dom"
  }
}
```

### Plugins
```javascript
// Custom loader plugin
const sassPlugin = {
  name: 'sass',
  setup(build) {
    build.onLoad({ filter: /\.scss$/ }, async (args) => {
      const { compile } = await import('sass');
      const result = compile(args.path, { style: 'compressed' });
      return { contents: result.css, loader: 'css' };
    });
  },
};

// Environment variable plugin
const envPlugin = {
  name: 'env',
  setup(build) {
    build.onResolve({ filter: /^env$/ }, (args) => ({
      path: args.path,
      namespace: 'env-ns',
    }));
    build.onLoad({ filter: /.*/, namespace: 'env-ns' }, () => ({
      contents: JSON.stringify(process.env),
      loader: 'json',
    }));
  },
};

await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  outdir: 'dist',
  plugins: [sassPlugin, envPlugin],
});
```

### Dev Server
```javascript
import * as esbuild from 'esbuild';
import http from 'http';

const ctx = await esbuild.context({
  entryPoints: ['src/index.ts'],
  bundle: true,
  outdir: 'dist',
  sourcemap: true,
});

// Watch for changes
await ctx.watch();

// Serve with esbuild
const { host, port } = await ctx.serve({ servedir: 'dist' });

console.log(`Dev server running at http://localhost:${port}`);
```

### Multi-Page App
```javascript
await esbuild.build({
  entryPoints: {
    main: 'src/pages/main.tsx',
    admin: 'src/pages/admin.tsx',
    login: 'src/pages/login.tsx',
  },
  bundle: true,
  outdir: 'dist',
  splitting: true,
  format: 'esm',
  metafile: true, // Generate build metadata
});

// Analyze bundle
const result = await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  metafile: true,
  write: false,
});
console.log(await esbuild.analyzeMetafile(result.metafile));
```

### TypeScript Config
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "outDir": "dist",
    "declaration": true
  },
  "include": ["src"]
}
```

### CSS with PostCSS
```javascript
import postcss from 'postcss';
import autoprefixer from 'autoprefixer';
import tailwindcss from 'tailwindcss';

const postcssPlugin = {
  name: 'postcss',
  setup(build) {
    build.onLoad({ filter: /\.css$/ }, async (args) => {
      const fs = await import('fs/promises');
      const css = await fs.readFile(args.path, 'utf8');
      const result = await postcss([tailwindcss, autoprefixer]).process(css, { from: args.path });
      return { contents: result.css, loader: 'css' };
    });
  },
};
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Could not resolve` | Missing import or typo | Check import paths, add to `external` if needed |
| `No matching export` | Wrong import syntax | Use named imports or check package exports |
| `Build failed` | Syntax error in source | Check error message for file and line |
| `Out of memory` | Huge project | Split into multiple builds or increase memory |
| `Plugin error` | Plugin bug | Check plugin return value format |

## Common Patterns

Proven patterns for esbuild-bundler usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Library with Types
```javascript
// build.mjs
await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  outdir: 'dist',
  format: 'esm',
  external: ['react'],
});

// Generate types separately
// tsconfig.json
{
  "compilerOptions": {
    "declaration": true,
    "declarationDir": "dist",
    "emitDeclarationOnly": true
  }
}
```

### Conditional Builds
```javascript
const isProd = process.env.NODE_ENV === 'production';

await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  outdir: 'dist',
  minify: isProd,
  sourcemap: !isProd,
  define: {
    'process.env.NODE_ENV': isProd ? '"production"' : '"development"',
  },
});
```

### HTML Entry
```javascript
import { htmlPlugin } from '@craftamap/esbuild-plugin-html';

await esbuild.build({
  entryPoints: ['src/index.tsx'],
  bundle: true,
  outdir: 'dist',
  plugins: [
    htmlPlugin({
      files: [{ entryPoints: ['src/index.tsx'], filename: 'index.html' }],
    }),
  ],
});
```

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