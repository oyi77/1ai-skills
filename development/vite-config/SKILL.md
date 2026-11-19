---
name: vite-config
description: Use when vite build tool configuration — plugins, SSR, library mode,
  environment variables, dev server proxy. Use when working with vite config.
domain: development
author: oyi77
license: Apache-2.0
subdomain: software-development
tags:
- coding
- config
- software-engineering
- testing
- vite
version: 1.0.0
category: development
---



## Overview

Vite is a next-generation frontend build tool that leverages native ES modules for instant dev server start and Rollup-based builds for production. This skill covers configuration patterns for React, Vue, Svelte, library mode, and SSR.

## Capabilities

- Instant dev server start with native ESM
- Lightning-fast HMR (Hot Module Replacement)
- Optimized production builds with Rollup
- Plugin system compatible with Rollup plugins
- Library mode for building npm packages
- SSR support for frameworks like Next.js/Nuxt
- Environment variables with `import.meta.env`
- CSS preprocessing (Sass, Less, PostCSS, Tailwind)
- Asset handling (images, fonts, JSON)
- Dev server proxy for API requests

## When to Use
**Trigger phrases:**
- "vite config"
- "Vite build tool configuration — plugins, SSR, library mode, environment variable"


- Starting new frontend projects (React, Vue, Svelte, Solid)
- Building npm libraries for distribution
- Migrating from Webpack (faster builds)
- Need fast dev server with HMR
- Building SSR applications
- Monorepo setups with shared config

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The vite-config workflow follows a standard pipeline pattern.

Core flow:
```
# vite-config primary flow
input = prepare(raw_data)
result = process(input, config={build, config, configuration, environment, library})
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


### Basic Configuration
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, 'src') },
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
        },
      },
    },
  },
});
```

### Environment Variables
```bash
# .env
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My App

# .env.production
VITE_API_URL=https://api.production.com

# .env.local (gitignored)
VITE_API_KEY=secret
```

```typescript
// Usage in code
const apiUrl = import.meta.env.VITE_API_URL;
const title = import.meta.env.VITE_APP_TITLE;
const isDev = import.meta.env.DEV;
const isProd = import.meta.env.PROD;
```

### Library Mode
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import dts from 'vite-plugin-dts';

export default defineConfig({
  build: {
    lib: {
      entry: 'src/index.ts',
      name: 'MyLib',
      formats: ['es', 'cjs', 'umd'],
      fileName: (format) => `my-lib.${format}.js`,
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: { globals: { react: 'React', 'react-dom': 'ReactDOM' } },
    },
  },
  plugins: [dts()], // Generate .d.ts files
});
```

### Tailwind CSS Integration
```typescript
// vite.config.ts
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [tailwindcss()],
});

// src/index.css
@import "tailwindcss";
```

### SSR Configuration
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      input: {
        client: 'src/entry-client.tsx',
        server: 'src/entry-server.tsx',
      },
    },
  },
});

// server.ts (Node.js SSR)
import express from 'express';
import { createServer as createViteServer } from 'vite';

async function createServer() {
  const app = express();
  const vite = await createViteServer({ server: { middlewareMode: true } });
  app.use(vite.middlewares);
  
  app.use('*', async (req, res) => {
    const template = fs.readFileSync('index.html', 'utf-8');
    const { render } = await vite.ssrLoadModule('/src/entry-server.tsx');
    const html = await render(req.originalUrl);
    res.status(200).set({ 'Content-Type': 'text/html' }).end(
      template.replace('<!--app-html-->', html)
    );
  });
  
  app.listen(3000);
}
createServer();
```

### Plugin Configuration
```typescript
// vite.config.ts
import react from '@vitejs/plugin-react';
import legacy from '@vitejs/plugin-legacy';
import { VitePWA } from 'vite-plugin-pwa';
import checker from 'vite-plugin-checker';

export default defineConfig({
  plugins: [
    react(),
    legacy({ targets: ['defaults', 'not IE 11'] }),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: { globPatterns: ['**/*.{js,css,html,ico,png,svg}'] },
    }),
    checker({ typescript: true, eslint: { lintCommand: 'eslint src' } }),
  ],
});
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Pre-transform error` | Invalid import or syntax | Check import paths and syntax |
| `CSS not loading` | Missing PostCSS/Sass | `npm install -D sass` or `postcss` |
| `HMR not working` | File outside root | Move files into project root |
| `Build failed: chunk size` | Large bundle | Use `manualChunks` or dynamic imports |
| `env not defined` | Missing `VITE_` prefix | All env vars must start with `VITE_` |

## Production Configuration Checklist

- **Environment:** every `VITE_*` variable is public in the client bundle. Never put secrets, private API keys, or server credentials behind a `VITE_` prefix; keep them server-side.
- **Source maps:** publish them only where access is controlled; do not expose source maps containing secrets or private source.
- **Bundle:** inspect the production bundle; use dynamic imports for routes/heavy features and avoid manual chunks until measured.
- **Dependencies:** audit plugin compatibility with the installed Vite major; pin/lock versions in CI.
- **SSR:** keep browser-only globals (`window`, `document`, `localStorage`) behind client boundaries; test direct requests and hydration for mismatch.
- **Assets:** reserve image dimensions, use hashed assets, and verify base paths when deployed under a subpath.
- **Dev server:** bind to localhost by default; only expose the network host intentionally, with auth or trusted-network controls.
- **Proxy:** dev proxy is not a production API security boundary. Configure CORS, auth, timeouts, and rate limits at the real server.
- **Build proof:** run `vite build`, serve the generated `dist/` with a static server, direct-load nested routes, and inspect console/network errors.

### Environment safety

```bash
# Safe: public client configuration only
VITE_PUBLIC_API_ORIGIN=https://api.example.com

# Unsafe: this value is bundled into client JavaScript
VITE_SECRET_KEY=do-not-do-this

# Keep private values in the server/runtime environment instead
API_SECRET_KEY=server-only
```



### Multi-Page App
```typescript
export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: 'index.html',
        admin: 'admin/index.html',
      },
    },
  },
});
```

### CSS Modules
```typescript
// Component.module.css
.button { background: blue; color: white; }

// Component.tsx
import styles from './Component.module.css';
function Component() {
  return <button className={styles.button}>Click</button>;
}
```

### Global CSS Variables
```css
:root {
  --color-primary: #3b82f6;
  --color-surface: #ffffff;
  --font-sans: 'Inter', sans-serif;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-surface: #1a1a1a;
  }
}
```

### Dev Server HTTPS
```typescript
import basicSsl from '@vitejs/plugin-basic-ssl';

export default defineConfig({
  plugins: [basicSsl()],
  server: { https: true },
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

- [ ] `vite build` passes in a clean install
- [ ] No private secret uses a `VITE_` prefix or appears in built assets
- [ ] Production bundle inspected; heavy features are split only where measured
- [ ] SSR/direct-load routes render without hydration mismatch
- [ ] `dist/` served by a static server; nested route refresh works
- [ ] Base path, asset URLs, image dimensions, and source-map policy verified
- [ ] Dev proxy is not mistaken for production auth/CORS/rate limiting
- [ ] Dev server exposure is intentional and bounded to a trusted network

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |