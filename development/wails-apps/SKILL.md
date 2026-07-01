---
name: wails-apps
description: Wails desktop app development — Go backend, web frontend, native bindings, small binary, cross-platform. Use when working with wails apps.
domain: development
tags:
- apps
- coding
- software-engineering
- testing
- wails
---


## Overview

Wails is a Go framework for building desktop applications with web frontends. It compiles to a single native binary with no runtime dependencies, using the OS's native WebView. Go handles the backend logic while any web framework (React, Vue, Svelte, vanilla) provides the UI.

## Capabilities

- Build desktop apps with Go backend + web frontend
- Native Go functions callable directly from JavaScript
- Single binary output (~10MB), no runtime dependencies
- Cross-platform: Windows, macOS, Linux
- Built-in dev server with hot reload
- System tray, menus, dialogs, notifications
- File drag-and-drop support
- Custom asset embedding
- Auto-update support

## When to Use
**Trigger phrases:**
- "wails apps"
- "Wails desktop app development — Go backend, web frontend, native bindings, small"


- Want Go's performance and ecosystem for backend logic
- Need single-binary distribution (no installer required)
- Building CLI tools with optional GUI
- Prefer Go over Rust (vs Tauri) or Node.js (vs Electron)
- System tray utilities and menu bar apps
- Internal tools and admin panels

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The wails-apps workflow follows a standard pipeline pattern.

Core flow:
```
# wails-apps primary flow
input = prepare(raw_data)
result = process(input, config={apps, backend, binary, bindings, cross})
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


### Project Setup
```bash
# Install Wails CLI
go install github.com/wailsapp/wails/v2/cmd/wails@latest

# Create project
wails init -n my-app -t react-ts
cd my-app

# Development
wails dev

# Build
wails build
```

### Go Backend (app.go)
```go
package main

import (
    "context"
    "fmt"
    "os"
    "path/filepath"
)

type App struct {
    ctx context.Context
}

func NewApp() *App {
    return &App{}
}

func (a *App) startup(ctx context.Context) {
    a.ctx = ctx
}

// Called from JavaScript
func (a *App) Greet(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}

func (a *App) ReadFile(path string) (string, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return "", err
    }
    return string(data), nil
}

func (a *App) SaveFile(path string, content string) error {
    dir := filepath.Dir(path)
    os.MkdirAll(dir, 0755)
    return os.WriteFile(path, []byte(content), 0644)
}

func (a *App) GetAppDir() string {
    dir, _ := os.UserHomeDir()
    return filepath.Join(dir, ".myapp")
}

// Structured data example
type Task struct {
    ID        int    `json:"id"`
    Title     string `json:"title"`
    Completed bool   `json:"completed"`
}

var tasks []Task

func (a *App) GetTasks() []Task {
    return tasks
}

func (a *App) AddTask(title string) Task {
    task := Task{ID: len(tasks) + 1, Title: title, Completed: false}
    tasks = append(tasks, task)
    return task
}
```

### Frontend Invocation (TypeScript/React)
```typescript
// Import Go bindings (auto-generated)
import { Greet, ReadFile, SaveFile, GetTasks, AddTask } from '../wailsjs/go/main/App';
import { WindowSetText } from '../wailsjs/runtime/runtime';

// Call Go function
const message = await Greet('World');
console.log(message); // "Hello, World!"

// File operations
const content = await ReadFile('/path/to/file.txt');
await SaveFile('/path/to/output.txt', 'Hello from Go!');

// Task management
const tasks = await GetTasks();
const newTask = await AddTask('Build desktop app');

// Window title
WindowSetText('My App - v1.0');
```

### Dialogs (from Go)
```go
import "github.com/wailsapp/wails/v2/pkg/runtime"

func (a *App) OpenFileDialog() string {
    path, _ := runtime.OpenFileDialog(a.ctx, runtime.OpenDialogOptions{
        Title: "Select File",
        Filters: []runtime.FileFilter{
            {DisplayName: "Text Files", Pattern: "*.txt;*.md"},
            {DisplayName: "All Files", Pattern: "*.*"},
        },
    })
    return path
}

func (a *App) ShowNotification(title, message string) {
    runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
        Type:    runtime.InfoDialogType,
        Title:   title,
        Message: message,
    })
}
```

### System Tray
```go
func (a *App) setupTray() {
    runtime.SystemTraySetIcon(a.ctx, iconBytes)
    runtime.SystemTraySetTooltip(a.ctx, "My App")
    
    menu := runtime.NewMenu()
    menu.Add("Show Window").OnClick(func(ctx context.Context) {
        runtime.WindowShow(ctx)
    })
    menu.AddSeparator()
    menu.Add("Quit").OnClick(func(ctx context.Context) {
        runtime.Quit(ctx)
    })
    runtime.SystemTraySetMenu(a.ctx, menu)
}
```

### wails.json Configuration
```json
{
  "name": "my-app",
  "outputfilename": "my-app",
  "frontend:install": "npm install",
  "frontend:build": "npm run build",
  "frontend:dev:watcher": "npm run dev",
  "frontend:dev:serverUrl": "auto",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "info": {
    "companyName": "My Company",
    "productName": "My App",
    "productVersion": "1.0.0"
  }
}
```

### Build
```bash
# Build for current platform
wails build

# Build with UPX compression
wails build -upx

# Build for specific platform
wails build -platform windows/amd64
wails build -platform darwin/universal
wails build -platform linux/amd64

# Build with installer (NSIS for Windows)
wails build -nsis
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `WebView not found` | Missing system WebView (Linux) | Install `libwebkit2gtk-4.0-dev` |
| `Go build failed` | Go module issue | `go mod tidy`, check Go version |
| `Frontend build failed` | Node/npm issue | `cd frontend && npm install` |
| `Method not exported` | Go function not capitalized | Export functions start with uppercase |
| `Hot reload not working` | Dev server URL mismatch | Check `wails.json` dev server config |

## Common Patterns

Proven patterns for wails-apps usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Event System
```go
// Emit event from Go
runtime.EventsEmit(a.ctx, "progress", 75)

// Listen in frontend
import { EventsOn } from '../wailsjs/runtime/runtime';
EventsOn('progress', (value) => {
  console.log('Progress:', value);
});
```

### Persistent Config
```go
import "encoding/json"

type Config struct {
    Theme    string `json:"theme"`
    Language string `json:"language"`
}

func (a *App) LoadConfig() Config {
    path := filepath.Join(a.GetAppDir(), "config.json")
    data, err := os.ReadFile(path)
    if err != nil {
        return Config{Theme: "dark", Language: "en"}
    }
    var config Config
    json.Unmarshal(data, &config)
    return config
}

func (a *App) SaveConfig(config Config) error {
    path := filepath.Join(a.GetAppDir(), "config.json")
    data, _ := json.MarshalIndent(config, "", "  ")
    return os.WriteFile(path, data, 0644)
}
```

### Background Jobs
```go
func (a *App) StartLongTask() {
    go func() {
        for i := 0; i <= 100; i++ {
            runtime.EventsEmit(a.ctx, "task-progress", i)
            time.Sleep(50 * time.Millisecond)
        }
        runtime.EventsEmit(a.ctx, "task-complete", "Done!")
    }()
}
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