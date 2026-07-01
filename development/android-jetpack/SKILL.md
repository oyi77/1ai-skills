---
name: android-jetpack
description: Android Jetpack Compose — declarative UI, state management, Material Design, and Play Store deployment
domain: development
tags:
- android
- coding
- jetpack
- software-engineering
- testing
---


## Overview

Jetpack Compose for building native Android apps. Covers declarative UI, state management, Material Design 3, Room database, navigation, and Play Store submission.

## Capabilities

- Build declarative UIs with Composable functions
- Implement state management (State, ViewModel, StateFlow)
- Apply Material Design 3 theming and components
- Use Room for local database persistence
- Navigate with Compose Navigation

## When to Use
**Trigger phrases:**
- "android jetpack"
- "Android Jetpack Compose — declarative UI, state management, Material Design, and"


- Building native Android apps
- Need Material Design 3 components
- Want declarative UI over XML layouts
- Team has Kotlin experience

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The android-jetpack workflow follows a standard pipeline pattern.

Core flow:
```
# android-jetpack primary flow
input = prepare(raw_data)
result = process(input, config={android, compose, declarative, deployment, design})
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


### Composable Function
```kotlin
@Composable
fun ItemList(items: List<Item>, onItemClick: (Item) -> Unit) {
    LazyColumn {
        items(items) { item ->
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { onItemClick(item) }
                    .padding(8.dp)
            ) {
                Text(item.name, style = MaterialTheme.typography.titleMedium)
            }
        }
    }
}
```

### ViewModel
```kotlin
class ItemViewModel : ViewModel() {
    private val _items = MutableStateFlow<List<Item>>(emptyList())
    val items: StateFlow<List<Item>> = _items.asStateFlow()
    
    fun loadItems() {
        viewModelScope.launch {
            _items.value = repository.getItems()
        }
    }
}
```

## Common Patterns

- **Single source of truth**: ViewModel holds state, Composables observe
- **Material 3**: Use MaterialTheme for consistent design
- **Navigation Compose**: Type-safe navigation with routes
- **Room + Flow**: Reactive queries with Flow return types

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