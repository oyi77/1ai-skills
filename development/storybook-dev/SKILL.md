---
name: storybook-dev
description: Storybook component development — stories, addons, controls, accessibility testing, visual regression
---

## Overview

Storybook is a frontend workshop for building UI components in isolation. It provides an interactive environment to develop, test, and document components independently from your application. This skill covers story authoring, addon configuration, accessibility testing, and visual regression.

## Capabilities

- Develop UI components in isolation from the app
- Interactive component playground with controls
- Auto-generated documentation from component props
- Accessibility testing with a11y addon
- Visual regression testing with Chromatic
- Interaction testing with play functions
- Design system documentation
- Theme switching (light/dark)
- Responsive viewport testing
- Mock providers for context/state

## When to Use

- Building a component library or design system
- Developing components before the app is ready
- Documenting UI components for team reference
- Visual regression testing for UI changes
- Accessibility testing components in isolation
- Onboarding new developers to the UI codebase

## Pseudo Code

### Setup
```bash
# Add to existing project
npx storybook@latest init

# Start Storybook
npm run storybook

# Build static Storybook
npm run build-storybook
```

### Configuration
```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: ['../src/**/*.stories.@(ts|tsx)'],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-a11y',
    '@storybook/addon-interactions',
    '@storybook/addon-themes',
  ],
  framework: { name: '@storybook/react-vite', options: {} },
};

export default config;

// .storybook/preview.ts
import type { Preview } from '@storybook/react';
import { ThemeProvider } from '../src/theme';
import '../src/index.css';

const preview: Preview = {
  decorators: [
    (Story) => (
      <ThemeProvider>
        <Story />
      </ThemeProvider>
    ),
  ],
  parameters: {
    layout: 'centered',
    backgrounds: {
      values: [
        { name: 'Light', value: '#ffffff' },
        { name: 'Dark', value: '#1a1a1a' },
      ],
    },
  },
};

export default preview;
```

### Story Authoring (CSF3)
```typescript
// src/components/Button/Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: { control: 'select', options: ['primary', 'secondary', 'danger'] },
    size: { control: 'select', options: ['sm', 'md', 'lg'] },
    disabled: { control: 'boolean' },
    onClick: { action: 'clicked' },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: { variant: 'primary', children: 'Primary Button' },
};

export const Secondary: Story = {
  args: { variant: 'secondary', children: 'Secondary Button' },
};

export const Disabled: Story = {
  args: { disabled: true, children: 'Disabled' },
};

export const AllSizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
};
```

### Interaction Testing
```typescript
// src/components/LoginForm/LoginForm.stories.tsx
import { expect, userEvent, within } from '@storybook/test';
import { LoginForm } from './LoginForm';

export const SuccessfulLogin: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    await userEvent.type(canvas.getByLabelText('Email'), 'user@example.com');
    await userEvent.type(canvas.getByLabelText('Password'), 'password123');
    await userEvent.click(canvas.getByRole('button', { name: 'Sign In' }));
    
    await expect(canvas.getByText('Welcome!')).toBeInTheDocument();
  },
};

export const ValidationErrors: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    await userEvent.click(canvas.getByRole('button', { name: 'Sign In' }));
    
    await expect(canvas.getByText('Email is required')).toBeInTheDocument();
    await expect(canvas.getByText('Password is required')).toBeInTheDocument();
  },
};
```

### Mock Providers
```typescript
// src/components/UserMenu/UserMenu.stories.tsx
import { UserMenu } from './UserMenu';
import { AuthProvider } from '../../contexts/AuthContext';

const meta: Meta<typeof UserMenu> = {
  title: 'Components/UserMenu',
  component: UserMenu,
  decorators: [
    (Story) => (
      <AuthProvider value={{ user: { name: 'John', email: 'john@example.com' }, isAuthenticated: true }}>
        <Story />
      </AuthProvider>
    ),
  ],
};
```

### Theme Switching
```typescript
// .storybook/preview.ts
import { withThemeByClassName } from '@storybook/addon-themes';

export const decorators = [
  withThemeByClassName({
    themes: { Light: '', Dark: 'dark' },
    defaultTheme: 'Light',
  }),
];
```

### Accessibility Testing
```typescript
// .storybook/main.ts
addons: ['@storybook/addon-a11y']

// In stories, a11y violations will show in the panel
// Or test programmatically:
import { expect } from '@storybook/test';
import { axe } from 'axe-playwright';

export const Accessible: Story = {
  play: async ({ canvasElement }) => {
    const results = await axe(canvasElement);
    expect(results.violations).toHaveLength(0);
  },
};
```

### Responsive Viewports
```typescript
export const Mobile: Story = {
  parameters: { viewport: { defaultViewport: 'mobile1' } },
};

export const Tablet: Story = {
  parameters: { viewport: { defaultViewport: 'tablet' } },
};
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Module not found` | Missing dependency | Run `npx storybook@latest init` again |
| `Stories not loading` | Wrong path in `stories` | Check glob pattern in main.ts |
| `Styles not applied` | CSS not imported | Import CSS in preview.ts |
| `Addon not working` | Not in addons array | Add to addons in main.ts |
| `Build failed` | Config syntax error | Check main.ts and preview.ts |

## Common Patterns

### Documentation Page
```typescript
// src/components/Card/Card.stories.tsx
const meta: Meta<typeof Card> = {
  title: 'Components/Card',
  component: Card,
  tags: ['autodocs'], // Auto-generates docs page
  parameters: {
    docs: {
      description: {
        component: 'A versatile card component for displaying content in a contained format.',
      },
    },
  },
};
```

### Args Table (Controls)
```typescript
argTypes: {
  variant: {
    control: 'select',
    options: ['primary', 'secondary', 'ghost'],
    description: 'The visual style of the button',
    table: {
      type: { summary: 'string' },
      defaultValue: { summary: 'primary' },
      category: 'Appearance',
    },
  },
},
```

### Composition (Nested Stories)
```typescript
export const WithHeader: Story = {
  render: () => (
    <Card>
      <Card.Header title="Title" subtitle="Subtitle" />
      <Card.Body>Content here</Card.Body>
      <Card.Footer>
        <Button>Action</Button>
      </Card.Footer>
    </Card>
  ),
};
```

### Visual Regression (Chromatic)
```bash
# Install
npm install -D chromatic

# Run
npx chromatic --project-token=<token>

# In CI
npx chromatic --project-token=${{ secrets.CHROMATIC_TOKEN }}
```
