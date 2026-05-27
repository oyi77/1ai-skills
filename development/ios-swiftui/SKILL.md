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
