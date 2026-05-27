---
name: react-native-expo
description: React Native with Expo — managed workflow, native modules, navigation, and app store deployment
---

## Overview

React Native development with Expo for cross-platform mobile apps. Covers managed vs bare workflow, navigation, native modules, EAS Build, OTA updates, and app store submission.

## Capabilities

- Build cross-platform apps with Expo managed workflow
- Implement navigation with React Navigation
- Use native modules and Expo SDK APIs
- Configure EAS Build for iOS and Android
- Deploy OTA updates without app store review

## When to Use

- Building a mobile app for both iOS and Android
- Need fast development with hot reload
- Want OTA updates without app store review delays
- Team has React/web experience

## Pseudo Code

### Navigation Setup
```typescript
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### EAS Build
```bash
# Configure
eas build:configure

# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android

# OTA update
eas update --channel production
```

## Common Patterns

- **Expo managed first**: Only eject to bare if you need native modules Expo doesn't support
- **EAS Build**: Use EAS for cloud builds — faster than local Xcode/Gradle
- **OTA updates**: Push JS bundle updates without app store review
- **Platform-specific code**: Use Platform.OS for iOS/Android differences
