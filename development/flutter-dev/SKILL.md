---
name: flutter-dev
description: Flutter cross-platform development — Dart, widgets, state management, platform channels, Firebase integration. Use when working with flutter dev.
domain: development
tags:
- coding
- dev
- flutter
- software-engineering
- testing
---


## Overview

Flutter is Google's UI toolkit for building natively compiled applications for mobile, web, and desktop from a single codebase. This skill covers Dart fundamentals, widget architecture, state management with Riverpod/Bloc, platform channels for native features, Firebase integration, and deployment to App Store and Google Play.

## Capabilities

- Build cross-platform apps from a single Dart codebase
- Compose UIs with Flutter's rich widget library (Material, Cupertino)
- Manage state with Riverpod, Bloc, or Provider
- Access native APIs via platform channels (MethodChannel)
- Integrate Firebase for auth, Firestore, storage, messaging
- Implement responsive layouts for phones, tablets, web
- Optimize performance with const widgets, lazy loading, profiling
- Build and deploy to iOS, Android, Web, macOS, Windows, Linux

## When to Use
**Trigger phrases:**
- "flutter dev"
- "Flutter cross-platform development — Dart, widgets, state management, platform c"


- Building mobile apps that target both iOS and Android
- Need native performance with cross-platform code sharing
- Prototyping MVPs quickly with hot reload
- Building apps that need custom UI/animations beyond standard components
- Integrating with Firebase or Google Cloud services

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The flutter-dev workflow follows a standard pipeline pattern.

Core flow:
```
# flutter-dev primary flow
input = prepare(raw_data)
result = process(input, config={channels, cross, dart, dev, development})
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
# Create new Flutter project
flutter create my_app --org com.example
cd my_app

# Add dependencies
flutter pub add flutter_riverpod firebase_core firebase_auth cloud_firestore
flutter pub add go_router flutter_screenutil

# Run on device/emulator
flutter run
```

### State Management with Riverpod
```dart
// Define a provider
final counterProvider = StateNotifierProvider<CounterNotifier, int>((ref) {
  return CounterNotifier();
});

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);
  void increment() => state++;
  void decrement() => state--;
}

// Use in widget
class CounterPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Scaffold(
      body: Center(child: Text('$count', style: TextStyle(fontSize: 48))),
      floatingActionButton: FloatingActionButton(
        onPressed: () => ref.read(counterProvider.notifier).increment(),
        child: Icon(Icons.add),
      ),
    );
  }
}
```

### Platform Channel (Native API)
```dart
// Dart side
class BatteryLevel {
  static const _channel = MethodChannel('com.example/battery');
  
  static Future<int> getBatteryLevel() async {
    final level = await _channel.invokeMethod<int>('getBatteryLevel');
    return level ?? -1;
  }
}

// Kotlin side (android/app/src/main/...)
class MainActivity: FlutterActivity() {
  override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
    super.configureFlutterEngine(flutterEngine)
    MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.example/battery")
      .setMethodCallHandler { call, result ->
        if (call.method == "getBatteryLevel") {
          result.success(85) // Get actual battery level
        } else {
          result.notImplemented()
        }
      }
  }
}
```

### Firebase Integration
```dart
// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(const ProviderScope(child: MyApp()));
}

// Auth service
class AuthService {
  final _auth = FirebaseAuth.instance;
  
  Future<User?> signIn(String email, String password) async {
    final cred = await _auth.signInWithEmailAndPassword(
      email: email, password: password,
    );
    return cred.user;
  }
  
  Future<User?> signUp(String email, String password) async {
    final cred = await _auth.createUserWithEmailAndPassword(
      email: email, password: password,
    );
    return cred.user;
  }
  
  Stream<User?> get authStateChanges => _auth.authStateChanges();
}
```

### Responsive Layout
```dart
class ResponsiveLayout extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth < 600) {
          return MobileLayout();
        } else if (constraints.maxWidth < 1200) {
          return TabletLayout();
        } else {
          return DesktopLayout();
        }
      },
    );
  }
}
```

### Navigation with GoRouter
```dart
final router = GoRouter(
  routes: [
    GoRoute(path: '/', builder: (c, s) => HomeScreen()),
    GoRoute(path: '/profile/:id', builder: (c, s) {
      final id = s.pathParameters['id']!;
      return ProfileScreen(userId: id);
    }),
    ShellRoute(builder: (c, s, child) => ScaffoldWithNav(child: child),
      routes: [
        GoRoute(path: '/home', builder: (c, s) => HomePage()),
        GoRoute(path: '/settings', builder: (c, s) => SettingsPage()),
      ],
    ),
  ],
  redirect: (context, state) {
    final isLoggedIn = ref.read(authProvider) != null;
    if (!isLoggedIn && state.matchedLocation != '/login') return '/login';
    return null;
  },
);
```

### Build & Deploy
```bash
# Android
flutter build apk --release
flutter build appbundle --release  # For Play Store

# iOS
flutter build ios --release
# Then archive in Xcode

# Web
flutter build web --release

# Desktop
flutter build macos --release
flutter build windows --release
flutter build linux --release
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Gradle build failed` | Android SDK/Java mismatch | Check `flutter doctor`, update Java/Gradle |
| `CocoaPods error` | iOS dependency conflict | `cd ios && pod install --repo-update` |
| `RenderFlex overflowed` | Widget exceeds bounds | Use `Expanded`, `Flexible`, or `SingleChildScrollView` |
| `setState called after dispose` | Widget disposed while async pending | Check `mounted` before `setState` |
| `Plugin not registered` | Platform plugin missing | Run `flutter clean && flutter pub get` |

## Common Patterns

Proven patterns for flutter-dev usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Clean Architecture
```
lib/
  core/           # Constants, themes, utils
  features/       # Feature modules
    auth/
      data/       # Repositories, data sources, models
      domain/     # Entities, use cases
      presentation/  # Pages, widgets, providers
    home/
      data/
      domain/
      presentation/
  shared/         # Shared widgets, services
```

### Error Handling with AsyncValue
```dart
final dataProvider = FutureProvider<List<Item>>((ref) async {
  return ref.read(apiClientProvider).fetchItems();
});

class ItemsPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final itemsAsync = ref.watch(dataProvider);
    return itemsAsync.when(
      loading: () => CircularProgressIndicator(),
      error: (err, stack) => ErrorWidget(err),
      data: (items) => ListView.builder(
        itemCount: items.length,
        itemBuilder: (c, i) => ItemTile(item: items[i]),
      ),
    );
  }
}
```

### Form Validation
```dart
class LoginForm extends StatefulWidget {
  @override
  _LoginFormState createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailCtrl = TextEditingController();
  final _passCtrl = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(children: [
        TextFormField(
          controller: _emailCtrl,
          validator: (v) => v!.contains('@') ? null : 'Invalid email',
          decoration: InputDecoration(labelText: 'Email'),
        ),
        TextFormField(
          controller: _passCtrl,
          obscureText: true,
          validator: (v) => v!.length >= 6 ? null : 'Min 6 characters',
          decoration: InputDecoration(labelText: 'Password'),
        ),
        ElevatedButton(
          onPressed: () {
            if (_formKey.currentState!.validate()) {
              // Submit
            }
          },
          child: Text('Login'),
        ),
      ]),
    );
  }
}
```

### Custom Theme
```dart
class AppTheme {
  static ThemeData light = ThemeData(
    useMaterial3: true,
    colorSchemeSeed: Colors.blue,
    brightness: Brightness.light,
    fontFamily: 'Inter',
    textTheme: TextTheme(
      headlineLarge: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
      bodyLarge: TextStyle(fontSize: 16, height: 1.5),
    ),
  );

  static ThemeData dark = ThemeData(
    useMaterial3: true,
    colorSchemeSeed: Colors.blue,
    brightness: Brightness.dark,
  );
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