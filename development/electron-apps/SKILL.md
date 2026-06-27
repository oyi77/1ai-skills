---
name: electron-apps
description: Electron desktop app development — main/renderer process, IPC, native menus, auto-update, packaging
domain: development
tags:
- apps
- coding
- electron
- software-engineering
- testing
---


## Overview

Electron enables building cross-platform desktop applications using web technologies (HTML, CSS, JavaScript). It powers apps like VS Code, Slack, Discord, and Figma Desktop. The main process handles native APIs while the renderer process runs the web UI.

## Capabilities

- Build desktop apps with any web framework (React, Vue, Svelte, vanilla)
- Native menus, system tray, notifications, dialog boxes
- IPC communication between main and renderer processes
- File system access, shell integration, clipboard
- Auto-update with electron-updater
- Deep linking and file associations
- Cross-platform packaging (Windows, macOS, Linux)
- Native Node.js modules support
- Crash reporting and telemetry

## When to Use

- Need desktop app with rich web UI
- Already have a web app to package as desktop
- Need deep OS integration (menus, tray, file associations)
- Building developer tools or productivity apps
- Team has strong web development skills
- Need to support Windows, macOS, and Linux

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The electron-apps workflow follows a standard pipeline pattern.

Core flow:
```
# electron-apps primary flow
input = prepare(raw_data)
result = process(input, config={apps, auto, desktop, development, electron})
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
# Using electron-vite (recommended)
npm create @quick-start/electron my-app
cd my-app
npm install

# Development
npm run dev

# Build
npm run build
```

### Main Process (main/index.ts)
```typescript
import { app, BrowserWindow, ipcMain, Menu, Tray, dialog, shell } from 'electron';
import path from 'path';

let mainWindow: BrowserWindow;
let tray: Tray;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, '../preload/index.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    titleBarStyle: 'hiddenInset', // macOS frameless
  });

  if (process.env.ELECTRON_DEV_URL) {
    mainWindow.loadURL(process.env.ELECTRON_DEV_URL);
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }
}

app.whenReady().then(() => {
  createWindow();
  createTray();
  createMenu();
});

// System Tray
function createTray() {
  tray = new Tray(path.join(__dirname, '../resources/icon.png'));
  const contextMenu = Menu.buildFromTemplate([
    { label: 'Show', click: () => mainWindow.show() },
    { label: 'Quit', click: () => app.quit() },
  ]);
  tray.setToolTip('My App');
  tray.setContextMenu(contextMenu);
  tray.on('click', () => mainWindow.show());
}

// Application Menu
function createMenu() {
  const template: Electron.MenuItemConstructorOptions[] = [
    {
      label: 'File',
      submenu: [
        { label: 'Open...', accelerator: 'CmdOrCtrl+O', click: openFileDialog },
        { label: 'Save', accelerator: 'CmdOrCtrl+S', click: saveFile },
        { type: 'separator' },
        { role: 'quit' },
      ],
    },
    {
      label: 'Edit',
      submenu: [{ role: 'undo' }, { role: 'redo' }, { role: 'cut' }, { role: 'copy' }, { role: 'paste' }],
    },
    {
      label: 'View',
      submenu: [{ role: 'reload' }, { role: 'toggleDevTools' }, { role: 'togglefullscreen' }],
    },
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}
```

### IPC Communication
```typescript
// main/index.ts — handle IPC
ipcMain.handle('dialog:open', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [{ name: 'Text', extensions: ['txt', 'md', 'json'] }],
  });
  if (result.canceled) return null;
  return fs.readFileSync(result.filePaths[0], 'utf-8');
});

ipcMain.handle('shell:openExternal', async (_, url: string) => {
  await shell.openExternal(url);
});

ipcMain.on('window:minimize', () => mainWindow.minimize());
ipcMain.on('window:maximize', () => {
  mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize();
});

// preload/index.ts — expose to renderer
import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  openFile: () => ipcRenderer.invoke('dialog:open'),
  openExternal: (url: string) => ipcRenderer.invoke('shell:openExternal', url),
  minimize: () => ipcRenderer.send('window:minimize'),
  maximize: () => ipcRenderer.send('window:maximize'),
  onProgress: (callback: (value: number) => void) => {
    ipcRenderer.on('progress-update', (_, value) => callback(value));
  },
});

// renderer (React) — use the API
const content = await window.electronAPI.openFile();
window.electronAPI.openExternal('https://example.com');
```

### Auto Update
```typescript
// main/index.ts
import { autoUpdater } from 'electron-updater';

autoUpdater.autoDownload = false;
autoUpdater.autoInstallOnAppQuit = true;

autoUpdater.on('update-available', async (info) => {
  const { response } = await dialog.showMessageBox({
    type: 'info',
    buttons: ['Download', 'Later'],
    title: 'Update Available',
    message: `Version ${info.version} is available. Download now?`,
  });
  if (response === 0) autoUpdater.downloadUpdate();
});

autoUpdater.on('update-downloaded', async () => {
  const { response } = await dialog.showMessageBox({
    type: 'info',
    buttons: ['Restart', 'Later'],
    title: 'Update Ready',
    message: 'Update downloaded. Restart to apply?',
  });
  if (response === 0) autoUpdater.quitAndInstall();
});

app.whenReady().then(() => {
  createWindow();
  autoUpdater.checkForUpdates();
});
```

### Packaging (electron-builder)
```json
// package.json
{
  "build": {
    "appId": "com.example.myapp",
    "productName": "My App",
    "mac": {
      "category": "public.app-category.developer-tools",
      "target": ["dmg", "zip"],
      "icon": "build/icon.icns"
    },
    "win": {
      "target": ["nsis", "portable"],
      "icon": "build/icon.ico"
    },
    "linux": {
      "target": ["AppImage", "deb"],
      "icon": "build/icon.png"
    },
    "publish": {
      "provider": "github",
      "owner": "your-username",
      "repo": "your-repo"
    }
  }
}
```

```bash
# Build for all platforms
npm run build

# Build for specific platform
npx electron-builder --mac
npx electron-builder --win
npx electron-builder --linux
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find module` | Native module not rebuilt | `npx electron-rebuild` |
| `SecurityError: blocked` | Context isolation blocking API | Use preload script with contextBridge |
| `GPU process error` | GPU rendering issue | Add `app.disableHardwareAcceleration()` |
| `Auto-update failed` | No publish config or signing | Check `build.publish` config |
| `Code signing failed` | Missing certificates | Set `CSC_LINK` and `CSC_KEY_PASSWORD` env vars |

## Common Patterns

Proven patterns for electron-apps usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Store (Persistent Settings)
```typescript
import Store from 'electron-store';

const store = new Store({
  defaults: { theme: 'dark', windowBounds: { width: 1200, height: 800 } },
});

// Save window bounds on resize
mainWindow.on('resize', () => {
  store.set('windowBounds', mainWindow.getBounds());
});

// Restore on startup
const bounds = store.get('windowBounds');
mainWindow.setBounds(bounds);
```

### Protocol Handler (Deep Links)
```typescript
app.setAsDefaultProtocolClient('myapp');

// macOS
app.on('open-url', (_, url) => {
  handleDeepLink(url);
});

// Windows/Linux
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', (_, argv) => {
    const url = argv.find(arg => arg.startsWith('myapp://'));
    if (url) handleDeepLink(url);
  });
}
```

### Crash Reporting
```typescript
import { crashReporter } from 'electron';

crashReporter.start({
  productName: 'My App',
  submitURL: 'https://your-crash-server.com/submit',
  uploadToServer: true,
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