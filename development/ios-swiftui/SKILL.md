---
name: ios-swiftui
description: SwiftUI development — declarative UI, state management, navigation, and Apple ecosystem integration. Use when working with ios swiftui.
domain: development
tags:
- coding
- ios
- software-engineering
- swiftui
- testing
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
**Trigger phrases:**
- "ios swiftui"
- "SwiftUI development — declarative UI, state management, navigation, and Apple ec"


- Building native iOS/macOS apps
- Need deep Apple ecosystem integration (HealthKit, CarPlay, widgets)
- Target iOS 16+ for modern SwiftUI features
- Team has Swift experience

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


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