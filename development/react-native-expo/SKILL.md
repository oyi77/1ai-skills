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

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The react-native-expo workflow follows a standard pipeline pattern.

Core flow:
```
# react-native-expo primary flow
input = prepare(raw_data)
result = process(input, config={deployment, expo, managed, modules, native})
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
