---
name: swiftui-patterns
description: SwiftUI native iOS/macOS development — declarative UI, Combine, Core Data, widgets, App Clips
---


## Overview

SwiftUI is Apple's declarative UI framework for building apps across all Apple platforms (iOS, macOS, watchOS, tvOS, visionOS). It uses a syntax-driven approach where you describe what the UI should look like, and SwiftUI handles the rendering.

## Capabilities

- Declarative UI with automatic state-driven updates
- Single codebase for iOS, macOS, watchOS, tvOS, visionOS
- Native integration with UIKit/AppKit via UIViewRepresentable
- Core Data and SwiftData integration
- WidgetKit for home screen widgets
- App Clips for lightweight app experiences
- NavigationStack and NavigationSplitView
- Animations and gestures built-in
- Combine framework for reactive data flow

## When to Use

- Building native Apple platform apps
- Targeting iOS 16+ / macOS 13+ (mature SwiftUI)
- Want declarative UI over UIKit storyboards
- Building widgets or App Clips
- Prototyping iOS apps quickly
- Building apps for Apple Vision Pro

## Pseudo Code

The swiftui-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# swiftui-patterns primary flow
input = prepare(raw_data)
result = process(input, config={clips, combine, core, data, declarative})
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


### Views and Modifiers
```swift
struct ContentView: View {
    @State private var isOn = false
    @State private var name = ""
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Hello, \(name)")
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundStyle(.blue)
            
            TextField("Enter name", text: $name)
                .textFieldStyle(.roundedBorder)
                .padding(.horizontal)
            
            Toggle("Enable Feature", isOn: $isOn)
                .padding()
            
            Button("Tap Me") {
                print("Tapped!")
            }
            .buttonStyle(.borderedProminent)
            .disabled(name.isEmpty)
            
            List(1...10, id: \.self) { number in
                Text("Item \(number)")
            }
        }
        .padding()
        .navigationTitle("Home")
    }
}
```

### State Management
```swift
// Observable model
@Observable
class TaskStore {
    var tasks: [Task] = []
    
    func add(_ task: Task) {
        tasks.append(task)
    }
    
    func toggle(_ task: Task) {
        if let index = tasks.firstIndex(where: { $0.id == task.id }) {
            tasks[index].completed.toggle()
        }
    }
}

// Using in view
struct TaskListView: View {
    @State private var store = TaskStore()
    
    var body: some View {
        NavigationStack {
            List {
                ForEach(store.tasks) { task in
                    TaskRow(task: task) {
                        store.toggle(task)
                    }
                }
                .onDelete { indexSet in
                    store.tasks.remove(atOffsets: indexSet)
                }
            }
            .navigationTitle("Tasks")
            .toolbar {
                Button("Add") {
                    store.add(Task(title: "New Task"))
                }
            }
        }
    }
}
```

### Navigation
```swift
// NavigationStack (push-based)
struct AppView: View {
    @State private var path = NavigationPath()
    
    var body: some View {
        NavigationStack(path: $path) {
            List(items) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                }
            }
            .navigationDestination(for: Item.self) { item in
                DetailView(item: item)
            }
        }
    }
}

// NavigationSplitView (sidebar)
struct SidebarApp: View {
    @State private var selection: Section?
    
    var body: some View {
        NavigationSplitView {
            List(sections, selection: $selection) { section in
                Label(section.name, systemImage: section.icon)
            }
        } detail: {
            if let selection {
                SectionView(section: selection)
            } else {
                Text("Select a section")
            }
        }
    }
}
```

### Core Data Integration
```swift
// Data model
@ManagedObject
class CDTask: Identifiable {
    @NSManaged var id: UUID
    @NSManaged var title: String
    @NSManaged var completed: Bool
    @NSManaged var createdAt: Date
}

// View with Core Data
struct TaskView: View {
    @Environment(\.managedObjectContext) private var context
    @FetchRequest(
        entity: CDTask.entity(),
        sortDescriptors: [NSSortDescriptor(keyPath: \CDTask.createdAt, ascending: false)]
    ) private var tasks: FetchedResults<CDTask>
    
    var body: some View {
        List {
            ForEach(tasks) { task in
                Text(task.title)
            }
            .onDelete { offsets in
                offsets.map { tasks[$0] }.forEach(context.delete)
                try? context.save()
            }
        }
    }
}
```

### WidgetKit
```swift
@main
struct MyWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "com.example.widget", provider: Provider()) { entry in
            WidgetView(entry: entry)
        }
        .configurationDisplayName("My Widget")
        .description("Shows quick info")
        .supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
    }
}

struct WidgetView: View {
    let entry: Provider.Entry
    
    var body: some View {
        VStack {
            Text(entry.title)
                .font(.headline)
            Text(entry.value)
                .font(.largeTitle)
                .fontWeight(.bold)
        }
        .containerBackground(.fill.tertiary, for: .widget)
    }
}
```

### Animations
```swift
struct AnimatedView: View {
    @State private var isExpanded = false
    
    var body: some View {
        VStack {
            RoundedRectangle(cornerRadius: isExpanded ? 20 : 0)
                .fill(.blue)
                .frame(
                    width: isExpanded ? 300 : 100,
                    height: isExpanded ? 300 : 100
                )
                .animation(.spring(response: 0.5, dampingFraction: 0.6), value: isExpanded)
                .onTapGesture {
                    isExpanded.toggle()
                }
        }
    }
}
```

### Network Layer
```swift
@Observable
class APIClient {
    var items: [Item] = []
    var isLoading = false
    var error: String?
    
    func fetchItems() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            let url = URL(string: "https://api.example.com/items")!
            let (data, _) = try await URLSession.shared.data(from: url)
            items = try JSONDecoder().decode([Item].self, from: data)
        } catch {
            self.error = error.localizedDescription
        }
    }
}
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Thread warning` | UI update from background thread | Use `@MainActor` or `await MainActor.run` |
| `Navigation not working` | Missing NavigationStack | Wrap in `NavigationStack` |
| `Core Data crash` | Context not injected | Add `.environment(\.managedObjectContext, context)` |
| `Widget not updating` | Timeline not refreshing | Call `WidgetCenter.shared.reloadTimelines` |
| `Preview crash` | Missing `#Preview` macro | Use `#Preview { ContentView() }` |

## Common Patterns

Proven patterns for swiftui-patterns usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Form Validation
```swift
struct FormView: View {
    @State private var email = ""
    @State private var password = ""
    
    private var isValid: Bool {
        email.contains("@") && password.count >= 8
    }
    
    var body: some View {
        Form {
            Section("Credentials") {
                TextField("Email", text: $email)
                    .textContentType(.emailAddress)
                    .keyboardType(.emailAddress)
                    .autocapitalization(.none)
                
                SecureField("Password", text: $password)
                    .textContentType(.newPassword)
            }
            
            Section {
                Button("Sign Up") { submit() }
                    .disabled(!isValid)
            }
        }
    }
}
```

### Async Image Loading
```swift
struct RemoteImage: View {
    let url: URL
    
    var body: some View {
        AsyncImage(url: url) { phase in
            switch phase {
            case .success(let image):
                image.resizable().aspectRatio(contentMode: .fit)
            case .failure:
                Image(systemName: "photo").foregroundColor(.gray)
            case .empty:
                ProgressView()
            @unknown default:
                EmptyView()
            }
        }
    }
}
```

### App Storage (UserDefaults)
```swift
struct SettingsView: View {
    @AppStorage("theme") private var theme = "system"
    @AppStorage("notifications") private var notifications = true
    
    var body: some View {
        Form {
            Picker("Theme", selection: $theme) {
                Text("System").tag("system")
                Text("Light").tag("light")
                Text("Dark").tag("dark")
            }
            Toggle("Notifications", isOn: $notifications)
        }
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
