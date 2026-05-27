---
name: android-jetpack
description: Android Jetpack Compose — declarative UI, state management, Material Design, and Play Store deployment
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

- Building native Android apps
- Need Material Design 3 components
- Want declarative UI over XML layouts
- Team has Kotlin experience

## Pseudo Code

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
