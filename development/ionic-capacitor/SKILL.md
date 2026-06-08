---
name: ionic-capacitor
description: Ionic + Capacitor hybrid mobile apps — Angular/React/Vue, native plugins,
  PWA, App Store deployment
domain: development
---


## Overview

Ionic Framework combined with Capacitor enables building cross-platform mobile apps using web technologies (Angular, React, or Vue). Capacitor provides access to native device APIs while Ionic handles UI components that look and feel native on every platform.

## Capabilities

- Build mobile apps with Angular, React, or Vue
- Access native device APIs (camera, GPS, filesystem, notifications)
- Deploy as PWA, iOS app, and Android app from single codebase
- Use Ionic's pre-built UI components (modals, tabs, lists, gestures)
- Live reload during development on device
- App Store and Play Store deployment
- Offline storage with SQLite or IndexedDB
- Push notifications via Firebase Cloud Messaging

## When to Use

- Team has strong web development skills
- Need to ship to iOS + Android + Web quickly
- Building content-heavy or form-based apps
- Want PWA capabilities alongside native apps
- Migrating existing web app to mobile

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The ionic-capacitor workflow follows a standard pipeline pattern.

Core flow:
```
# ionic-capacitor primary flow
input = prepare(raw_data)
result = process(input, config={angular, apps, capacitor, deployment, hybrid})
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
# Create Ionic app (choose Angular, React, or Vue)
npm create ionic@latest my-app -- --type react
cd my-app

# Add Capacitor
npx cap init my-app com.example.myapp
npx cap add ios
npx cap add android

# Install native plugins
npm install @capacitor/camera @capacitor/geolocation @capacitor/push-notifications
npm install @capacitor/filesystem @capacitor/haptics @capacitor/share

# Run in browser
ionic serve

# Sync to native
npx cap sync
```

### Native Plugin Usage
```typescript
import { Camera, CameraResultType } from '@capacitor/camera';
import { Geolocation } from '@capacitor/geolocation';
import { PushNotifications } from '@capacitor/push-notifications';

// Camera
async takePicture() {
  const image = await Camera.getPhoto({
    quality: 90,
    resultType: CameraResultType.Base64,
    source: CameraSource.Camera,
  });
  return `data:image/jpeg;base64,${image.base64String}`;
}

// Geolocation
async getCurrentPosition() {
  const coords = await Geolocation.getCurrentPosition();
  return { lat: coords.coords.latitude, lng: coords.coords.longitude };
}

// Push Notifications
async initPush() {
  await PushNotifications.requestPermissions();
  await PushNotifications.register();
  PushNotifications.addListener('registration', (token) => {
    console.log('Push token:', token.value);
  });
  PushNotifications.addListener('pushNotificationReceived', (notification) => {
    console.log('Push received:', notification);
  });
}
```

### Ionic UI Components (React)
```tsx
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
         IonList, IonItem, IonLabel, IonButton, IonModal } from '@ionic/react';

const HomePage: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Home</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent>
        <IonList>
          {items.map(item => (
            <IonItem key={item.id} button onClick={() => selectItem(item)}>
              <IonLabel>
                <h2>{item.title}</h2>
                <p>{item.description}</p>
              </IonLabel>
            </IonItem>
          ))}
        </IonList>
        <IonButton expand="block" onClick={() => setShowModal(true)}>
          Open Modal
        </IonButton>
        <IonModal isOpen={showModal}>
          <ModalContent onDismiss={() => setShowModal(false)} />
        </IonModal>
      </IonContent>
    </IonPage>
  );
};
```

### Offline Storage
```typescript
import { Storage } from '@ionic/storage-angular';

class OfflineStorage {
  private storage: Storage;

  async init() {
    this.storage = await Storage.create();
  }

  async save(key: string, value: any) {
    await this.storage.set(key, JSON.stringify(value));
  }

  async load<T>(key: string): Promise<T | null> {
    const data = await this.storage.get(key);
    return data ? JSON.parse(data) : null;
  }

  async remove(key: string) {
    await this.storage.remove(key);
  }
}
```

### Build & Deploy
```bash
# Build web assets
ionic build

# Sync to native projects
npx cap sync

# Open in Xcode (iOS)
npx cap open ios

# Open in Android Studio
npx cap open android

# Live reload on device
ionic cap run ios --livereload --external
ionic cap run android --livereload --external
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Plugin not registered` | Plugin not synced to native | `npx cap sync` after installing plugin |
| `CORS error` | API blocked in WebView | Configure proxy or allow CORS on server |
| `White screen` | JS error in production | Check Safari/Chrome remote debugging |
| `Build failed: iOS` | CocoaPods or signing issue | `cd ios/App && pod install`, check signing |
| `Build failed: Android` | Gradle or SDK issue | Check `android/gradle.properties` |

## Common Patterns

Proven patterns for ionic-capacitor usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Route Guard (React)
```tsx
const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <IonSpinner />;
  return isAuthenticated ? <>{children}</> : <Redirect to="/login" />;
};
```

### Pull to Refresh
```tsx
<IonRefresher slot="fixed" onIonRefresh={async (e) => {
  await refreshData();
  e.detail.complete();
}}>
  <IonRefresherContent />
</IonRefresher>
```

### Infinite Scroll
```tsx
<IonInfiniteScroll onIonInfinite={async (e) => {
  await loadMore();
  e.target.complete();
}}>
  <IonInfiniteScrollContent />
</IonInfiniteScroll>
```

### App Lifecycle
```typescript
import { App } from '@capacitor/app';

App.addListener('appStateChange', ({ isActive }) => {
  console.log('App active:', isActive);
});

App.addListener('backButton', ({ canGoBack }) => {
  if (!canGoBack) App.exitApp();
  else window.history.back();
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
