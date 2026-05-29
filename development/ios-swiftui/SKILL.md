---
name: ios-swiftui
description: SwiftUI development — declarative UI, state management, navigation, and Apple ecosystem integration
---


## Overview

SwiftUI for building native iOS, macOS, watchOS, and tvOS apps. Covers declarative UI, state management, navigation, Core Data, and Apple ecosystem integration.

## Capabilities

- Build declarative UIs with SwiftUI views and modifiers
- Implement state management (@State, @Binding, @Observable)
- Design navigation with NavigationStack and NavigationLink
- Integrate with Core Data, HealthKit, and Apple services
- Submit to App Store via TestFlight

## When to Use

- Building native iOS/macOS apps
- Need deep Apple ecosystem integration (HealthKit, CarPlay, widgets)
- Target iOS 16+ for modern SwiftUI features
- Team has Swift experience

## Pseudo Code

The ios-swiftui workflow follows a standard pipeline pattern.

Core flow:
```
# ios-swiftui primary flow
input = prepare(raw_data)
result = process(input, config={apple, declarative, development, ecosystem, integration})
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


### SwiftUI View
```swift
struct ContentView: View {
    @State private var items: [Item] = []
    
    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink(item.name) {
                    DetailView(item: item)
                }
            }
            .navigationTitle("Items")
            .task { await loadItems() }
        }
    }
    
    func loadItems() async {
        items = try? await APIService.fetchItems()
    }
}
```

### Observable Pattern
```swift
@Observable
class ItemStore {
    var items: [Item] = []
    
    func fetch() async throws {
        items = try await APIService.fetchItems()
    }
}
```

## Common Patterns

- **@Observable**: Use the new @Observable macro (iOS 17+) over ObservableObject
- **NavigationStack**: Use NavigationStack over NavigationView (deprecated)
- **Task modifier**: Use .task {} for async loading instead of .onAppear
- **PreviewProvider**: Always include previews for rapid development

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
