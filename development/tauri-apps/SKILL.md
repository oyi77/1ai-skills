---
name: tauri-apps
description: Tauri desktop app development — Rust backend, web frontend, native APIs, small binary size, cross-platform
---


## Overview

Tauri is a framework for building lightweight, secure desktop applications with a web-based frontend and a Rust backend. Unlike Electron, Tauri uses the OS's native WebView, resulting in significantly smaller binaries (typically <10MB) and lower memory usage.

## Capabilities

- Build desktop apps with React/Vue/Svelte/Solid frontend + Rust backend
- Native OS API access (filesystem, shell, notifications, system tray)
- Tiny binary size (~3-10MB vs Electron's ~150MB+)
- Low memory usage (~30MB vs Electron's ~100MB+)
- Cross-platform: Windows, macOS, Linux
- Auto-update mechanism built in
- Secure IPC between frontend and Rust commands
- Custom protocols, file associations, deep links
- Sidecar and shell command execution

## When to Use

- Need desktop app with small footprint
- Want native performance without bundling Chromium
- Security-sensitive applications (Rust backend)
- System tray apps, menu bar utilities
- Replacing Electron for resource-constrained environments
- Need native filesystem/shell access from web UI

## Pseudo Code

The tauri-apps workflow follows a standard pipeline pattern.

Core flow:
```
# tauri-apps primary flow
input = prepare(raw_data)
result = process(input, config={apis, apps, backend, binary, cross})
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
# Prerequisites: Rust + system dependencies
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Create Tauri app (with any frontend framework)
npm create tauri-app@latest my-app
cd my-app

# Development
npm run tauri dev

# Build
npm run tauri build
```

### Tauri Commands (Rust ↔ Frontend IPC)
```rust
// src-tauri/src/main.rs
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[tauri::command]
async fn read_file(path: String) -> Result<String, String> {
    std::fs::read_to_string(&path).map_err(|e| e.to_string())
}

#[tauri::command]
async fn save_data(key: String, value: String, app: tauri::AppHandle) -> Result<(), String> {
    let app_dir = app.path_resolver().app_data_dir().unwrap();
    let file_path = app_dir.join(format!("{}.json", key));
    std::fs::write(file_path, value).map_err(|e| e.to_string())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, read_file, save_data])
        .run(tauri::generate_context!())
        .expect("error running tauri app");
}
```

### Frontend Invocation
```typescript
import { invoke } from '@tauri-apps/api/tauri';
import { open, save } from '@tauri-apps/api/dialog';
import { readTextFile, writeTextFile } from '@tauri-apps/api/fs';
import { appDataDir, join } from '@tauri-apps/api/path';

// Call Rust command
const greeting = await invoke<string>('greet', { name: 'World' });

// File dialog
const filePath = await open({
  multiple: false,
  filters: [{ name: 'Text', extensions: ['txt', 'md'] }],
});

if (filePath) {
  const content = await readTextFile(filePath as string);
  console.log(content);
}

// Save file
const savePath = await save({ filters: [{ name: 'JSON', extensions: ['json'] }] });
if (savePath) {
  await writeTextFile(savePath, JSON.stringify(data, null, 2));
}
```

### System Tray
```rust
use tauri::{SystemTray, SystemTrayMenu, SystemTrayMenuItem, CustomMenuItem};

fn main() {
    let tray_menu = SystemTrayMenu::new()
        .add_item(CustomMenuItem::new("show", "Show Window"))
        .add_item(CustomMenuItem::new("hide", "Hide Window"))
        .add_native_item(SystemTrayMenuItem::Separator)
        .add_item(CustomMenuItem::new("quit", "Quit"));

    let system_tray = SystemTray::new().with_menu(tray_menu);

    tauri::Builder::default()
        .system_tray(system_tray)
        .on_system_tray_event(|app, event| {
            match event {
                tauri::SystemTrayEvent::MenuItemClick { id, .. } => {
                    match id.as_str() {
                        "show" => {
                            let window = app.get_window("main").unwrap();
                            window.show().unwrap();
                        }
                        "hide" => {
                            let window = app.get_window("main").unwrap();
                            window.hide().unwrap();
                        }
                        "quit" => std::process::exit(0),
                        _ => {}
                    }
                }
                _ => {}
            }
        })
        .run(tauri::generate_context!())
        .expect("error running tauri app");
}
```

### Auto Update
```rust
// Cargo.toml
[dependencies]
tauri = { version = "1", features = ["updater"] }

// main.rs
fn main() {
    tauri::Builder::default()
        .setup(|app| {
            // Auto-update check on startup
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error running tauri app");
}

// Frontend
import { checkUpdate, installUpdate } from '@tauri-apps/api/updater';

const update = await checkUpdate();
if (update.shouldUpdate) {
  await installUpdate();
}
```

### Tauri Events
```rust
// Emit event from Rust
app.emit_all("progress-update", 75).unwrap();

// Listen on frontend
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen<number>('progress-update', (event) => {
  console.log('Progress:', event.payload);
});
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Cargo build failed` | Missing Rust dependencies | Check `rustup update`, install system deps |
| `WebView not found` | Missing system WebView (Linux) | Install `libwebkit2gtk-4.0-dev` |
| `Permission denied` | Tauri allowlist not configured | Add command to `tauri.conf.json` allowlist |
| `Command not found` | Rust command not registered | Add to `invoke_handler` in main.rs |
| `Build failed: code signing` | macOS signing issue | Set signing identity in Xcode or env var |

## Common Patterns

Proven patterns for tauri-apps usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Window Management
```rust
use tauri::Manager;

// Create window from Rust
let window = tauri::WindowBuilder::new(
    &app, "settings", tauri::WindowUrl::App("/settings".into())
).title("Settings").inner_size(600.0, 400.0).build()?;
```

### Persistent Store
```typescript
import Store from 'tauri-plugin-store-api';

const store = new Store('.settings.dat');
await store.set('theme', 'dark');
await store.save();

const theme = await store.get<string>('theme');
```

### Shell Commands
```rust
use tauri::api::process::{Command, CommandEvent};

#[tauri::command]
async fn run_script(script: String) -> Result<String, String> {
    let (mut rx, _child) = Command::new("sh")
        .args(["-c", &script])
        .spawn()
        .map_err(|e| e.to_string())?;
    
    let mut output = String::new();
    while let Some(event) = rx.recv().await {
        match event {
            CommandEvent::Stdout(line) => output.push_str(&line),
            CommandEvent::Stderr(line) => output.push_str(&format!("ERR: {}", line)),
            _ => {}
        }
    }
    Ok(output)
}
```

### Custom Protocol
```json
// tauri.conf.json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devPath": "http://localhost:5173",
    "distDir": "../dist"
  },
  "tauri": {
    "bundle": {
      "identifier": "com.example.myapp",
      "icon": ["icons/icon.png"]
    },
    "windows": [{
      "title": "My App",
      "width": 1024,
      "height": 768
    }]
  }
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
