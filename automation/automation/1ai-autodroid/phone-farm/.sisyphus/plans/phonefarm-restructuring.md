# Phonefarm Restructuring Plan

## TL;DR

> **Quick Summary**: Restructure phonefarm codebase from flat Python files to Clean Architecture with TDD + SOLID + KISS. Add FastAPI for HTTP layer, implement multi-tenant row-level security, preserve all existing features and API contracts.
> 
> **Deliverables**:
> - Clean Architecture with domain/infrastructure/api layers
> - FastAPI HTTP server with all existing endpoints
> - Multi-tenant data isolation with tenant_id
> - Comprehensive pytest test suite (TDD approach)
> - Dependency injection for testability
> - CLI backward compatibility
> 
> **Estimated Effort**: Large (XL)
> **Parallel Execution**: YES - 4 waves
> **Critical Path**: Setup → Domain Models → Infrastructure → API Layer → Tests → Integration

---

## Context

### Original Request
Restructure phonefarm codebase following:
- TDD (Test-Driven Development) + SSD (Structured System Design)
- SOLID + KISS principles
- Add FastAPI + httpx
- Preserve all current features + add multi-tenant SaaS
- Big bang approach

### Interview Summary

**Key Discussions**:
- Current: 17 flat Python files, no package structure
- Largest: farm_daemon.py (1651 lines), db.py (944 lines)
- Test: pytest exists but limited coverage
- User preference: TDD approach, FastAPI for HTTP, add multi-tenant

**Research Findings**:
- SQLite database with 15+ tables (tenants, devices, tasks, users, sessions, earnings)
- Standard library only (json, sqlite3, threading, dataclasses)
- Existing tests use httpx MockTransport
- No pyproject.toml or dependency management

### Metis Review

**Identified Gaps** (addressed):
- Clarified multi-tenant as row-level security with tenant_id
- Set explicit scope boundaries (no admin UI, billing, SSO)
- Added backward compatibility requirements for CLI and API
- Defined edge cases for migration (NULL tenant_id, corrupted DB, concurrent writes)
- Specified test execution criteria as executable commands

---

## Work Objectives

### Core Objective
Transform flat Python codebase into Clean Architecture with:
1. Proper layer separation (domain/infrastructure/api)
2. FastAPI HTTP layer replacing monolith
3. Multi-tenant data isolation
4. Comprehensive test coverage via TDD

### Concrete Deliverables
- `src/` directory with Clean Architecture structure
- `pyproject.toml` with FastAPI, httpx, pytest dependencies
- All existing API endpoints in FastAPI routes
- Multi-tenant middleware with tenant_id filtering
- CLI-compatible entry points (farm_daemon.py)
- pytest test suite with 80%+ coverage target

### Definition of Done
- [ ] `pytest --tb=short -v` passes with ZERO regressions
- [ ] All existing API endpoints respond with same JSON structure
- [ ] `python3 farm_daemon.py --help` outputs expected help
- [ ] Tenant A cannot read Tenant B's devices (isolation verified)
- [ ] No breaking changes to existing CLI commands

### Must Have
- FastAPI HTTP server with all endpoints
- Multi-tenant isolation via tenant_id
- Backward compatible CLI
- pytest test suite (TDD approach)
- Dependency injection for services

### Must NOT Have (Guardrails)
- Admin UI or billing features (scope creep)
- Redis, Celery, or external infrastructure
- Breaking changes to API contract
- Schema isolation or separate DBs per tenant (complexity)
- Over-abstracted repository patterns

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: YES
- **Automated tests**: TDD (test-first approach)
- **Framework**: pytest + pytest-asyncio
- **Test Workflow**: RED (failing test) → GREEN (minimal impl) → REFACTOR

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

**Test execution**:
- `pytest tests/unit/ -v` - Unit tests for domain services
- `pytest tests/integration/ -v` - API integration tests
- `pytest --tb=short -v` - Full test suite

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Setup + Foundation):
├── T1: Project scaffolding with pyproject.toml [quick]
├── T2: Create src/ directory structure [quick]
├── T3: Define domain entities (Device, Task, User, Tenant) [quick]
├── T4: Define Pydantic models for API [quick]
├── T5: Setup pytest configuration + conftest.py [quick]
└── T6: Install dependencies (FastAPI, httpx, pytest) [quick]

Wave 2 (Domain + Infrastructure - MAX PARALLEL):
├── T7: Database connection + repository base [deep]
├── T8: Device repository implementation [unspecified-high]
├── T9: Task repository implementation [unspecified-high]
├── T10: User repository implementation [unspecified-high]
├── T11: ADB pool wrapper (preserve existing logic) [unspecified-high]
├── T12: Auth implementation (JWT + password) [deep]
├── T13: Tenant isolation middleware [deep]
└── T14: Config management [quick]

Wave 3 (API Layer - MAX PARALLEL):
├── T15: FastAPI server setup + lifecycle [deep]
├── T16: Device CRUD routes [unspecified-high]
├── T17: Task management routes [unspecified-high]
├── T18: Auth routes (login/logout/register) [unspecified-high]
├── T19: Admin routes [unspecified-high]
├── T20: Screen streaming WebSocket [unspecified-high]
├── T21: CLI entry point (farm_daemon.py) [deep]
└── T22: Rate limiter middleware [quick]

Wave 4 (Testing + Integration):
├── T23: Write unit tests for domain services [deep]
├── T24: Write integration tests for API endpoints [deep]
├── T25: Write multi-tenant isolation tests [deep]
├── T26: CLI compatibility tests [unspecified-high]
└── T27: Run full test suite + fix failures [deep]

Wave FINAL (Verification):
├── F1: Plan compliance audit (oracle) [deep]
├── F2: Code quality review [unspecified-high]
├── F3: Real manual QA [unspecified-high]
└── F4: Scope fidelity check [deep]

Critical Path: T1 → T2 → T7 → T15 → T16-20 → T21 → T27 → F1-F4
```

### Dependency Matrix
- T1-T6: None (start immediately)
- T7-T14: Depend on T2, T4
- T15-T22: Depend on T7-T14, T5 (tests)
- T23-T27: Depend on T15-T22
- F1-F4: Depend on T27

---

## TODOs

- [x] 1. **Project scaffolding with pyproject.toml**
- [x] 2. **Create src/ directory structure**
- [x] 3. **Define domain entities**

  **What to do**:
  - Create domain entities in `src/domain/entities/`:
    - `device.py`: Device, DeviceStatus, DeviceInfo
    - `task.py`: Task, TaskStatus, TaskPriority
    - `user.py`: User, UserRole
    - `tenant.py`: Tenant
  - Use dataclasses with type hints
  - No external dependencies in domain layer

  **Must NOT do**:
  - Add Pydantic or database references in domain entities

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Pure data classes with type hints

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 1, with T2, T4-T6)

  **Acceptance Criteria**:
  - [ ] All 4 entity modules created
  - [ ] Type hints on all fields
  - [ ] No external imports (pure Python)

  **QA Scenarios**:
  ```
  Scenario: Domain entities import correctly
    Tool: Bash
    Preconditions: T2 complete
    Steps:
      1. python3 -c "from src.domain.entities import Device, Task, User, Tenant; print('OK')"
    Expected Result: OK printed
    Failure Indicators: ImportError
    Evidence: .sisyphus/evidence/task-3-entities.txt
  ```

- [x] 4. **Define Pydantic models for API**

  **What to do**:
  - Create request/response models in `src/api/models/`:
    - DeviceCreate, DeviceResponse, DeviceUpdate
    - TaskCreate, TaskResponse
    - UserCreate, UserResponse, LoginRequest
    - ErrorResponse
  - Extend Pydantic BaseModel
  - Add validation (field constraints)

  **Recommended Agent Profile**:
  - **Category**: `quick`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 1)

  **Acceptance Criteria**:
  - [ ] All Pydantic models created
  - [ ] Field validation working
  - [ ] Serialization/deserialization works

  **QA Scenarios**:
  ```
  Scenario: Pydantic models validate correctly
    Tool: Bash
    Preconditions: T1 dependencies installed
    Steps:
      1. python3 -c "from pydantic import BaseModel; class Test(BaseModel): name: str; m = Test(name='ok'); print(m.model_dump())"
    Expected Result: {'name': 'ok'}
    Failure Indicators: Validation error
  ```

- [x] 5. **Setup pytest configuration**

  **What to do**:
  - Create `tests/conftest.py` with:
    - pytest fixtures for test database
    - Mock objects for dependencies
    - Test client fixture for FastAPI
  - Create `tests/__init__.py`
  - Create `tests/unit/__init__.py`
  - Create `tests/integration/__init__.py`
  - Add pytest.ini or pyproject.toml pytest section

  **Recommended Agent Profile**:
  - **Category**: `quick`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 1)

  **Acceptance Criteria**:
  - [ ] pytest can be run and discovers tests
  - [ ] Fixtures work correctly

- [x] 6. **Install dependencies**

  **What to do**:
  - Run `uv sync` or `pip install -e .` to install dependencies
  - Verify all imports work

  **Recommended Agent Profile**:
  - **Category**: `quick`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 1)

  **Acceptance Criteria**:
  - [ ] fastapi imports work
  - [ ] httpx imports work
  - [ ] pytest discovers tests

- [x] 7. **Database connection + repository base**

  **What to do**:
  - Create `src/infrastructure/database/connection.py`:
    - Database connection management (SQLite with WAL mode)
    - Thread-local connections
    - Get connection function
  - Create repository base class:
    - CRUD operations interface
    - Generic repository implementation
  - Preserve existing db.py logic (15+ tables)

  **Must NOT do**:
  - Break existing database schema

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Complex database logic, thread safety

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on T2, T4)
  - **Blocks**: T8-T10
  - **Blocked By**: T2, T4

  **Acceptance Criteria**:
  - [ ] Database connection works
  - [ ] WAL mode enabled
  - [ ] Thread-safe connections
  - [ ] All 15 tables accessible

  **QA Scenarios**:
  ```
  Scenario: Database connection works
    Tool: Bash
    Preconditions: T7 complete
    Steps:
      1. python3 -c "from src.infrastructure.database.connection import get_conn; c = get_conn(); print(c.execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall())"
    Expected Result: List of tables
    Failure Indicators: Connection error
  ```

- [x] 8. **Device repository implementation**

  **What to do**:
  - Create `src/infrastructure/repositories/device_repo.py`:
    - CRUD for devices table
    - Methods: create, get_by_serial, list, update, delete
    - Filter by tenant_id for multi-tenant

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 2 with T9, T10)
  - **Blocks**: T16
  - **Blocked By**: T7

- [x] 9. **Task repository implementation**

  **What to do**:
  - Create `src/infrastructure/repositories/task_repo.py`:
    - CRUD for tasks table
    - Methods: create, get_by_id, list, update_status
    - Filter by tenant_id

- [x] 10. **User repository implementation**

  **What to do**:
  - Create `src/infrastructure/repositories/user_repo.py`:
    - CRUD for users, sessions tables
    - Methods: create, get_by_email, verify_password
    - Session management

- [x] 11. **ADB pool wrapper**

  **What to do**:
  - Copy and adapt existing adb_pool.py logic to `src/infrastructure/adb/pool.py`
  - Preserve all existing ADB operations
  - Add type hints and error handling
  - Add unit tests

  **Must NOT do**:
  - Change ADB behavior (must work exactly as before)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 2)

- [x] 12. **Auth implementation**

  **What to do**:
  - Create `src/infrastructure/auth/jwt.py`:
    - JWT token creation/verification
    - Token expiration
  - Create `src/infrastructure/auth/password.py`:
    - Password hashing (bcrypt via passlib)
    - Password verification
  - Preserve existing auth.py functionality

  **Recommended Agent Profile**:
  - **Category**: `deep`

- [x] 13. **Tenant isolation middleware**

  **What to do**:
  - Create `src/api/middleware/tenant.py`:
    - Extract tenant_id from JWT token
    - Add tenant_id to request state
    - Apply tenant filtering to all queries
  - Ensure Tenant A cannot see Tenant B's data

  **Recommended Agent Profile**:
  - **Category**: `deep`

  **Acceptance Criteria**:
  - [ ] Middleware extracts tenant_id from token
  - [ ] Queries are filtered by tenant_id
  - [ ] Cross-tenant data access blocked

- [x] 14. **Config management**

  **What to do**:
  - Create `src/config.py`:
    - Load from environment variables
    - Database path, JWT secret, server config
    - Provide config object to services

- [x] 15. **FastAPI server setup**

  **What to do**:
  - Create `src/api/server.py`:
    - FastAPI app creation
    - CORS middleware
    - Exception handlers
    - Startup/shutdown events
  - Create `src/main.py`:
    - Uvicorn entry point

  **Recommended Agent Profile**:
  - **Category**: `deep`

- [x] 16-20. **API routes (devices, tasks, auth, admin, WebSocket)**

  **What to do**:
  - Implement all existing endpoints in FastAPI routes
  - Preserve exact API contract (request/response formats)
  - Add proper error handling

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`

- [x] 21. **CLI entry point**

  **What to do**:
  - Create backward-compatible `farm_daemon.py`:
    - Same CLI interface as before
    - Calls FastAPI server internally
  - Ensure `python3 farm_daemon.py --help` works

  **Recommended Agent Profile**:
  - **Category**: `deep`

- [ ] 22. **Rate limiter middleware**

  **What to do**:
  - Port existing rate_limiter.py to FastAPI middleware

- [ ] 23-26. **Testing (TDD approach)**

  **What to do**:
  - Write failing tests first (RED)
  - Implement to make tests pass (GREEN)
  - Refactor (REFACTOR)
  - Cover: unit, integration, isolation tests

  **Recommended Agent Profile**:
  - **Category**: `deep`

- [ ] 27. **Run full test suite**

  **What to do**:
  - Run `pytest --tb=short -v`
  - Fix any failing tests
  - Ensure zero regressions

- [ ] F1-F4. **Final verification**

  **What to do**:
  - Plan compliance audit
  - Code quality review
  - Manual QA
  - Scope fidelity check

---

## Final Verification Wave

- [ ] F1. **Plan Compliance Audit** — Read plan, verify each "Must Have" implemented
- [ ] F2. **Code Quality Review** — Run linter, type checker, tests
- [ ] F3. **Real Manual QA** — Test CLI, API endpoints manually
- [ ] F4. **Scope Fidelity Check** — Verify no scope creep

---

## Success Criteria

### Verification Commands
```bash
pytest --tb=short -v           # All tests pass
python3 farm_daemon.py --help  # CLI works
curl http://localhost:8889/health  # Server responds
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] All tests pass
- [ ] CLI backward compatible
- [ ] Multi-tenant isolation verified