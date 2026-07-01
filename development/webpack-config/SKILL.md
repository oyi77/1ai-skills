---
name: webpack-config
description: Webpack 5 configuration — loaders, plugins, code splitting, tree shaking, module federation, dev server. Use when working with webpack config.
domain: development
tags:
- coding
- config
- software-engineering
- testing
- webpack
---


## Overview

Webpack 5 is a static module bundler for modern JavaScript applications. It processes every module in your project, applies loaders and plugins, and outputs optimized bundles. This skill covers configuration patterns for production-grade builds.

## Capabilities

- Bundle JS/TS/CSS/assets into optimized output files
- Code splitting with dynamic imports and splitChunks
- Tree shaking to eliminate dead code
- Module Federation for micro-frontends
- Hot Module Replacement (HMR) for development
- Asset processing with loaders (images, fonts, CSS, etc.)
- Environment-specific configuration (dev/prod)
- Source maps for debugging
- Bundle analysis and optimization

## When to Use
**Trigger phrases:**
- "webpack config"
- "Webpack 5 configuration — loaders, plugins, code splitting, tree shaking, module"


- Building complex web applications with many dependencies
- Need fine-grained control over bundling
- Implementing micro-frontends with Module Federation
- Migrating legacy projects to modern bundling
- Need custom loader/plugin pipeline
- Building library packages

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The webpack-config workflow follows a standard pipeline pattern.

Core flow:
```
# webpack-config primary flow
input = prepare(raw_data)
result = process(input, config={code, config, configuration, federation, loaders})
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
```javascript
// webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = (env, argv) => {
  const isProd = argv.mode === 'production';

  return {
    entry: './src/index.tsx',
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: isProd ? '[name].[contenthash:8].js' : '[name].js',
      clean: true,
      publicPath: '/',
    },
    resolve: {
      extensions: ['.tsx', '.ts', '.js', '.jsx'],
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    module: {
      rules: [
        {
          test: /\.[jt]sx?$/,
          exclude: /node_modules/,
          use: 'babel-loader',
        },
        {
          test: /\.css$/,
          use: [
            isProd ? MiniCssExtractPlugin.loader : 'style-loader',
            'css-loader',
            'postcss-loader',
          ],
        },
        {
          test: /\.(png|jpe?g|gif|svg)$/,
          type: 'asset',
          parser: { dataUrlCondition: { maxSize: 8 * 1024 } },
        },
        {
          test: /\.(woff2?|eot|ttf|otf)$/,
          type: 'asset/resource',
        },
      ],
    },
    plugins: [
      new HtmlWebpackPlugin({ template: './public/index.html' }),
      isProd && new MiniCssExtractPlugin({ filename: '[name].[contenthash:8].css' }),
    ].filter(Boolean),
    optimization: {
      minimizer: ['...', new CssMinimizerPlugin()],
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          vendor: { test: /[\\/]node_modules[\\/]/, name: 'vendors', chunks: 'all' },
        },
      },
    },
    devServer: {
      port: 3000,
      hot: true,
      historyApiFallback: true,
      proxy: { '/api': 'http://localhost:8080' },
    },
    devtool: isProd ? 'source-map' : 'eval-cheap-module-source-map',
  };
};
```

### Code Splitting (Dynamic Imports)
```typescript
// Lazy-loaded routes
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const Settings = React.lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### Module Federation
```javascript
// Host app webpack.config.js
const { ModuleFederationPlugin } = require('webpack').container;

new ModuleFederationPlugin({
  name: 'host',
  remotes: {
    remoteApp: 'remoteApp@http://localhost:3001/remoteEntry.js',
  },
  shared: { react: { singleton: true }, 'react-dom': { singleton: true } },
});

// Remote app webpack.config.js
new ModuleFederationPlugin({
  name: 'remoteApp',
  filename: 'remoteEntry.js',
  exposes: { './Widget': './src/Widget' },
  shared: { react: { singleton: true }, 'react-dom': { singleton: true } },
});

// Host app usage
const RemoteWidget = React.lazy(() => import('remoteApp/Widget'));
```

### Bundle Analysis
```bash
# Install analyzer
npm install --save-dev webpack-bundle-analyzer

# Add to config
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
plugins: [new BundleAnalyzerPlugin()]

# Run analysis
npx webpack --mode production --stats-error-details
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Module not found` | Missing import or alias | Check `resolve.extensions` and `resolve.alias` |
| `Out of memory` | Bundle too large | Increase `NODE_OPTIONS=--max-old-space-size=4096` |
| `HMR not working` | Dev server misconfig | Check `devServer.hot: true` and entry point |
| `CSS not loading` | Missing loader | Add `style-loader` + `css-loader` |
| `Tree shaking not working` | CommonJS modules | Use ESM (import/export syntax), check sideEffects |

## Common Patterns

Proven patterns for webpack-config usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Environment Config
```javascript
// webpack.config.js
const Dotenv = require('dotenv-webpack');

module.exports = (env) => ({
  plugins: [
    new Dotenv({ path: env.production ? '.env.production' : '.env.development' }),
  ],
});
```

### TypeScript Config
```javascript
module.exports = {
  module: {
    rules: [{ test: /\.tsx?$/, use: 'ts-loader', exclude: /node_modules/ }],
  },
};
```

### SVG as React Components
```javascript
module.exports = {
  module: {
    rules: [
      {
        test: /\.svg$/,
        use: ['@svgr/webpack', 'url-loader'],
      },
    ],
  },
};
```

### Performance Budgets
```javascript
module.exports = {
  performance: {
    maxAssetSize: 250000,
    maxEntrypointSize: 250000,
    hints: 'warning',
  },
};
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