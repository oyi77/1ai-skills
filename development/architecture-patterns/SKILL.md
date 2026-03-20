---
name: architecture-patterns
description: Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design. Use when architecting complex backend systems or refactoring existing applications for better maintainability.
source: https://github.com/LeoYeAI/openclaw-master-skills
---

# Architecture Patterns

Master proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design to build maintainable, testable, and scalable systems.

## When to Use This Skill

- Designing new backend systems from scratch
- Refactoring monolithic applications for better maintainability
- Establishing architecture standards for your team
- Migrating from tightly coupled to loosely coupled architectures
- Implementing domain-driven design principles
- Creating testable and mockable codebases
- Planning microservices decomposition

## Core Concepts

### 1. Clean Architecture (Uncle Bob)

**Layers (dependency flows inward):**

- **Entities**: Core business models
- **Use Cases**: Application business rules
- **Interface Adapters**: Controllers, presenters, gateways
- **Frameworks & Drivers**: UI, database, external services

**Key Principles:**

- Dependencies point inward
- Inner layers know nothing about outer layers
- Business logic independent of frameworks
- Testable without UI, database, or external services

### 2. Hexagonal Architecture (Ports and Adapters)

**Components:**

- **Domain Core**: Business logic
- **Ports**: Interfaces defining interactions
- **Adapters**: Implementations of ports (database, REST, message queue)

**Benefits:**

- Swap implementations easily (mock for testing)
- Technology-agnostic core
- Clear separation of concerns

### 3. Domain-Driven Design (DDD)

**Strategic Patterns:**

- **Bounded Contexts**: Separate models for different domains
- **Context Mapping**: How contexts relate
- **Ubiquitous Language**: Shared terminology

**Tactical Patterns:**

- **Entities**: Objects with identity
- **Value Objects**: Immutable objects defined by attributes
- **Aggregates**: Consistency boundaries
- **Repositories**: Data access abstraction
- **Domain Events**: Things that happened

## Clean Architecture Directory Structure

```
app/
├── domain/           # Entities & business rules
│   ├── entities/
│   ├── value_objects/
│   └── interfaces/   # Abstract interfaces (ports)
├── use_cases/        # Application business rules
├── adapters/         # Interface implementations
│   ├── repositories/
│   ├── controllers/
│   └── gateways/
└── infrastructure/   # Framework & external concerns
    ├── database.py
    ├── config.py
    └── logging.py
```

## Implementation Examples

### Clean Architecture: Use Case Pattern

```python
@dataclass
class CreateUserRequest:
    email: str
    name: str

class CreateUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        existing = await self.user_repository.find_by_email(request.email)
        if existing:
            return CreateUserResponse(success=False, error="Email exists")

        user = User(id=uuid4(), email=request.email, name=request.name)
        saved = await self.user_repository.save(user)
        return CreateUserResponse(user=saved, success=True)
```

### Hexagonal: Ports and Adapters

```python
# Port (interface)
class PaymentGatewayPort(ABC):
    @abstractmethod
    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        pass

# Production adapter
class StripePaymentAdapter(PaymentGatewayPort):
    async def charge(self, amount, customer):
        charge = stripe.Charge.create(amount=amount.cents, customer=customer)
        return PaymentResult(success=True, transaction_id=charge.id)

# Test adapter
class MockPaymentAdapter(PaymentGatewayPort):
    async def charge(self, amount, customer):
        return PaymentResult(success=True, transaction_id="mock-123")
```

### DDD: Value Objects and Aggregates

```python
# Value Object (immutable)
@dataclass(frozen=True)
class Money:
    amount: int  # cents
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)

# Aggregate Root
class Order:
    def __init__(self, id: str, customer: Customer):
        self.id = id
        self.items: List[OrderItem] = []
        self.status = OrderStatus.PENDING
        self._events: List[DomainEvent] = []

    def add_item(self, product, quantity):
        self.items.append(OrderItem(product, quantity))
        self._events.append(ItemAddedEvent(self.id))

    def submit(self):
        if not self.items:
            raise ValueError("Cannot submit empty order")
        self.status = OrderStatus.SUBMITTED
        self._events.append(OrderSubmittedEvent(self.id))
```

## Best Practices

1. **Dependency Rule**: Dependencies always point inward
2. **Interface Segregation**: Small, focused interfaces
3. **Business Logic in Domain**: Keep frameworks out of core
4. **Test Independence**: Core testable without infrastructure
5. **Bounded Contexts**: Clear domain boundaries
6. **Ubiquitous Language**: Consistent terminology
7. **Thin Controllers**: Delegate to use cases
8. **Rich Domain Models**: Behavior with data

## Common Pitfalls

- **Anemic Domain**: Entities with only data, no behavior
- **Framework Coupling**: Business logic depends on frameworks
- **Fat Controllers**: Business logic in controllers
- **Repository Leakage**: Exposing ORM objects
- **Missing Abstractions**: Concrete dependencies in core
- **Over-Engineering**: Clean architecture for simple CRUD
