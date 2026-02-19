# Trading Skill Enhancement

## TL;DR

> **Quick Summary**: Enhance the trading skill with new technical indicators, strategy templates, broker support, improved risk management, and comprehensive test suite for OpenClaw compatibility.
> 
> **Deliverables**:
> - Technical indicators library (RSI, MACD, Bollinger Bands, Moving Averages)
> - Strategy templates (Breakout, Trend Following, Mean Reversion, Scalping)
> - Enhanced broker connectors (stable connectivity)
> - More symbols (forex pairs: EURUSD, GBPUSD, USDJPY)
> - Improved risk management system
> - Better error handling
> - Comprehensive test suite (TDD + Backtest validation)
> 
> **Estimated Effort**: XL (20-30 tasks)
> **Parallel Execution**: YES - 6 waves with ~5-6 tasks each
> **Critical Path**: Infrastructure → Indicators → Strategies → Tests → Integration

---

## Context

### Original Request
Enhance the existing trading skill to be more powerful with:
1. New technical indicators (RSI, MACD, Bollinger Bands, Moving Averages)
2. New strategy templates (Breakout, Trend Following, Mean Reversion, Scalping)
3. More crypto exchanges support (via existing CCXT)
4. More forex pairs (EURUSD, GBPUSD, USDJPY)
5. Improved risk management
6. Better broker connectivity
7. Better error handling
8. Unit tests for OpenClaw testability
9. Backtest validation tests

### Current State
- Well-structured codebase with base classes
- Existing: MT5, MT4, CCXT connectors
- Existing: XAUUSD Asia 7C Breakout strategy
- Backtest engine with metrics
- Paper trade and real trade engines
- Team roles (orchestrator, strategist, researcher, executor, risk_manager)
- Yahoo Finance data provider
- Missing: unit tests, comprehensive error handling
- Missing: technical indicators library
- Missing: strategy templates

### Metis Review
**Identified Gaps** (to be addressed):
- No test infrastructure (pytest not set up)
- Missing technical indicators library
- Risk management needs parameter-based config
- Error handling is minimal (try/except only)
- No validation for OpenClaw integration
- Missing integration tests for broker connectors

---

## Work Objectives

### Core Objective
Create a production-ready, well-tested trading skill with comprehensive technical analysis capabilities, robust broker connectivity, and full OpenClaw compatibility.

### Concrete Deliverables
1. `trading/indicators/` - Technical indicators library
2. `trading/strategy/templates/` - Reusable strategy templates
3. `trading/risk/` - Enhanced risk management
4. Enhanced broker connectors with retry logic
5. Symbol configs for EURUSD, GBPUSD, USDJPY
6. `tests/` - Comprehensive test suite
7. `scripts/test_integration.py` - OpenClaw validation script

### Definition of Done
- [ ] All new indicators pass unit tests
- [ ] Strategy templates work with backtest engine
- [ ] Broker connectors have 99.9% uptime (retry logic)
- [ ] All forex pairs have symbol configs
- [ ] 80%+ test coverage
- [ ] OpenClaw can execute: `bun test` and `python scripts/test_integration.py`

### Must Have
- RSI, MACD, Bollinger Bands, Moving Averages
- At least 2 strategy templates (Breakout + one other)
- Symbol configs for EURUSD, GBPUSD, USDJPY
- Retry logic for broker connections
- pytest test infrastructure
- Backtest validation tests
- Error handling with proper logging

### Must NOT Have (Guardrails)
- No real money trading in tests (only paper/backtest)
- No hardcoded API keys
- No infinite retry loops (max 3 attempts)
- No blocking I/O in unit tests
- No modifications to existing strategy file (extend, don't modify)

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO (need to set up)
- **Automated tests**: TDD (RED-GREEN-REFACTOR)
- **Framework**: pytest for Python
- **TDD Workflow**: Each task includes failing test → implementation → passing test

### QA Policy
Every task MUST include agent-executed QA scenarios. Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Backend/Modules**: Use Bash (pytest) - Run tests, assert PASS
- **Backtest**: Use Bash (python) - Run backtest, assert metrics
- **Broker Connectivity**: Use Bash (curl/mock) - Test connections

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Foundation - Infrastructure):
├── Task 1: Setup pytest infrastructure and test structure
├── Task 2: Fix package imports and structure (resolve LSP errors)
├── Task 3: Create indicators base class and module structure
├── Task 4: Create symbol configs for EURUSD, GBPUSD, USDJPY
└── Task 5: Enhanced error handling base classes

Wave 2 (Core Components - MAX PARALLEL):
├── Task 6: Implement Moving Averages (SMA, EMA, WMA)
├── Task 7: Implement RSI indicator with tests
├── Task 8: Implement MACD indicator with tests
├── Task 9: Implement Bollinger Bands with tests
├── Task 10: Enhanced risk management system
└── Task 11: Broker connector retry logic

Wave 3 (Strategy Templates):
├── Task 12: Strategy template base class
├── Task 13: Breakout strategy template
├── Task 14: Trend Following strategy template
├── Task 15: Mean Reversion strategy template
└── Task 16: Scalping strategy template

Wave 4 (Tests & Integration):
├── Task 17: Unit tests for indicators (100% coverage)
├── Task 18: Unit tests for risk manager
├── Task 19: Unit tests for broker connectors (mock)
├── Task 20: Integration test script for OpenClaw
└── Task 21: Backtest validation test suite

Wave 5 (Polish & Validation):
├── Task 22: Error handling improvements throughout
├── Task 23: Performance optimization (if needed)
├── Task 24: Documentation updates
└── Task 25: End-to-end test: Run full pipeline

Wave FINAL (4 parallel reviews):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high)
└── Task F4: Scope fidelity check (deep)

Critical Path: Task 1 → Task 6-9 → Task 12-16 → Task 17-21 → Task 25 → F1-F4
```

### Dependency Matrix

| Task | Depends On | Blocks |
|------|-----------|--------|
| 1 | — | 6-9, 17 |
| 2 | — | 3, 6-9 |
| 3 | 2 | 6-9 |
| 4 | — | 13-16 |
| 5 | — | 22 |
| 6 | 1, 2, 3 | 17 |
| 7 | 1, 2, 3 | 17 |
| 8 | 1, 2, 3 | 17 |
| 9 | 1, 2, 3 | 17 |
| 10 | — | 19 |
| 11 | — | 19 |
| 12 | 6-9 | 13-16 |
| 13 | 4, 12 | 21 |
| 14 | 4, 12 | 21 |
| 15 | 4, 12 | 21 |
| 16 | 4, 12 | 21 |
| 17 | 6-9 | 25 |
| 18 | 10 | 25 |
| 19 | 11 | 25 |
| 20 | 1-21 | 25 |
| 21 | 13-16 | 25 |
| 22 | 5 | 25 |
| 23 | 6-22 | 25 |
| 24 | — | 25 |
| 25 | 17-24 | F1-F4 |

### Agent Dispatch Summary

- **Wave 1 (5 tasks)**: T1 → `quick`, T2 → `quick`, T3 → `quick`, T4 → `quick`, T5 → `quick`
- **Wave 2 (6 tasks)**: T6-T9 → `unspecified-high`, T10-T11 → `unspecified-high`
- **Wave 3 (5 tasks)**: T12-T16 → `unspecified-high`
- **Wave 4 (5 tasks)**: T17-T21 → `quick` + `unspecified-high`
- **Wave 5 (5 tasks)**: T22-T25 → `unspecified-high` + `writing`
- **Wave FINAL (4 tasks)**: F1 → `oracle`, F2-F4 → `unspecified-high`

---

## TODOs

### Wave 1: Foundation (Infrastructure)

- [x] 1. Setup pytest infrastructure and test structure

  **What to do**:
  - Create `tests/` directory structure
  - Create `pytest.ini` with test discovery config
  - Create `tests/conftest.py` with fixtures (broker mock, strategy mock)
  - Add pytest-cov to dev dependencies
  - Create first passing test to verify setup: `tests/test_setup.py`

  **Must NOT do**:
  - Don't install unnecessary packages
  - Don't modify existing source code yet

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []
  - Reason: Simple infrastructure setup task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Task 6-9, 17
  - **Blocked By**: None

  **References**:
  - Pattern: Check existing `trading/` structure for test placement
  - External: https://docs.pytest.org/en/stable/

  **Acceptance Criteria**:
  - [ ] `tests/` directory created
  - [ ] `pytest.ini` created with proper config
  - [ ] `tests/conftest.py` created with basic fixtures
  - [ ] Running `pytest tests/test_setup.py` passes

  **QA Scenarios**:
  ```
  Scenario: Verify pytest setup works
    Tool: Bash
    Preconditions: None
    Steps:
      1. cd C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading
      2. pytest tests/test_setup.py -v
    Expected Result: Output shows 1 passed test
    Evidence: .sisyphus/evidence/task-1-pytest-setup.txt
  ```

  **Commit**: YES
  - Message: `test: setup pytest infrastructure`
  - Files: tests/, pytest.ini

- [x] 2. Fix package imports and structure

  **What to do**:
  - Fix LSP errors in trading/strategy/ files (relative imports → absolute)
  - Fix LSP errors in trading/brokers/ files
  - Fix LSP errors in trading/data/yahoo.py
  - Add `__init__.py` files where missing
  - Verify `import trading` works from root directory

  **Must NOT do**:
  - Don't change any logic, only imports
  - Don't break existing functionality

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []
  - Reason: Import fixes are straightforward

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1)
  - **Parallel Group**: Wave 1
  - **Blocks**: Task 3, 6-9
  - **Blocked By**: None

  **References**:
  - Fix: `trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/strategy.py` line 20-21
  - Fix: `trading/brokers/ccxt/connector.py` line 11
  - Fix: `trading/data/yahoo.py` line 9

  **Acceptance Criteria**:
  - [ ] LSP errors resolved in all identified files
  - [ ] Can import modules without errors: `python -c "from trading.strategy.base import Strategy; print('OK')"`
  - [ ] Backtest script still works: `python scripts/xauusd_backtest.py --initial-balance 100`

  **QA Scenarios**:
  ```
  Scenario: Verify imports work
    Tool: Bash
    Preconditions: Task 1 completed
    Steps:
      1. cd C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading
      2. python -c "from trading.strategy.base import Strategy; from trading.brokers.base import OHLCV; print('All imports OK')"
    Expected Result: Output shows "All imports OK"
    Evidence: .sisyphus/evidence/task-2-imports.txt
  ```

  **Commit**: YES
  - Message: `fix: resolve package import issues`
  - Files: trading/__init__.py, trading/strategy/ files, trading/brokers/ files

- [x] 3. Create indicators base class and module structure

  **What to do**:
  - Create `trading/indicators/` directory
  - Create `trading/indicators/__init__.py`
  - Create `trading/indicators/base.py` with Indicator base class
  - Base class should have: `calculate(self, data: List[OHLCV]) -> Any`, `validate_input()`
  - Create `trading/indicators/utils.py` for helper functions

  **Must NOT do**:
  - Don't implement actual indicators yet (that's Tasks 6-9)
  - Don't modify existing strategy files

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []
  - Reason: Structure creation

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1-2)
  - **Parallel Group**: Wave 1
  - **Blocks**: Task 6-9
  - **Blocked By**: Task 2

  **References**:
  - Pattern: `trading/strategy/base.py` for abstract class pattern
  - Pattern: `trading/brokers/base.py` for dataclass pattern

  **Acceptance Criteria**:
  - [ ] `trading/indicators/` directory exists
  - [ ] `trading/indicators/base.py` has Indicator abstract class
  - [ ] Can import: `from trading.indicators.base import Indicator`

  **QA Scenarios**:
  ```
  Scenario: Verify indicators module structure
    Tool: Bash
    Steps:
      1. cd C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading
      2. python -c "from trading.indicators.base import Indicator; print('Indicator base OK')"
    Expected Result: Output shows "Indicator base OK"
    Evidence: .sisyphus/evidence/task-3-indicators-structure.txt
  ```

  **Commit**: YES
  - Message: `feat(indicators): create base module structure`
  - Files: trading/indicators/

- [x] 4. Create symbol configs for EURUSD, GBPUSD, USDJPY

  **What to do**:
  - Create `trading/data/symbols.py` for symbol configuration
  - Add SymbolConfig dataclass with: symbol, yahoo_ticker, point_value, pip_digits, contract_size
  - Add EURUSD config: "EURUSD" → "EURUSD=X"
  - Add GBPUSD config: "GBPUSD" → "GBPUSD=X"
  - Add USDJPY config: "USDJPY" → "JPY=X"
  - Update `trading/data/yahoo.py` to use symbol configs

  **Must NOT do**:
  - Don't remove existing XAUUSD mapping
  - Don't change YahooFinanceProvider API (extend it)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []
  - Reason: Configuration data

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1-3)
  - **Parallel Group**: Wave 1
  - **Blocks**: Task 13-16
  - **Blocked By**: Task 2

  **References**:
  - Pattern: `trading/brokers/base.py` dataclass pattern
  - Existing: `trading/data/yahoo.py` line 17-27 for symbol mapping

  **Acceptance Criteria**:
  - [ ] `trading/data/symbols.py` created
  - [ ] Can access: `get_symbol_config("EURUSD")`
  - [ ] YahooFinanceProvider can fetch EURUSD data

  **QA Scenarios**:
  ```
  Scenario: Verify symbol configs work
    Tool: Bash
    Steps:
      1. cd C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading
      2. python -c "from trading.data.symbols import get_symbol_config; c = get_symbol_config('EURUSD'); print(f'{c.symbol}: {c.yahoo_ticker}')"
    Expected Result: Output shows "EURUSD: EURUSD=X"
    Evidence: .sisyphus/evidence/task-4-symbol-configs.txt
  ```

  **Commit**: YES
  - Message: `feat(data): add forex symbol configurations`
  - Files: trading/data/symbols.py, trading/data/yahoo.py

- [x] 5. Create enhanced error handling base classes

  **What to do**:
  - Create `trading/exceptions.py` for custom exceptions
  - Add: BrokerConnectionError, IndicatorCalculationError, StrategyValidationError, RiskManagerError
  - Create `trading/utils/error_handler.py` with retry decorator
  - Retry decorator: max_attempts, backoff, exponential_jitter

  **Must NOT do**:
  - Don't apply error handling yet (that's Task 22)
  - Don't modify existing code

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []
  - Reason: Base classes creation

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1-4)
  - **Parallel Group**: Wave 1
  - **Blocks**: Task 22
  - **Blocked By**: None

  **References**:
  - External: https://docs.python.org/3/library/typing.html for type hints
  - Pattern: Standard Python exception hierarchy

  **Acceptance Criteria**:
  - [ ] `trading/exceptions.py` with 4+ custom exceptions
  - [ ] `trading/utils/error_handler.py` with retry decorator
  - [ ] Decorator works: `@retry(max_attempts=3)`

  **QA Scenarios**:
  ```
  Scenario: Verify retry decorator works
    Tool: Bash
    Steps:
      1. cd C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading
      2. python -c "
        from trading.utils.error_handler import retry
        @retry(max_attempts=2)
        def flaky_func():
          print('called')
          raise ValueError('fail')
        try:
          flaky_func()
        except:
          pass
      "
    Expected Result: "called" prints twice (2 attempts)
    Evidence: .sisyphus/evidence/task-5-error-handling.txt
  ```

  **Commit**: YES
  - Message: `feat(core): add error handling infrastructure`
  - Files: trading/exceptions.py, trading/utils/

### Wave 2: Core Components (Indicators & Infrastructure)

- [x] 6. Implement Moving Averages (SMA, EMA, WMA)

  **What to do**:
  - Create `trading/indicators/moving_averages.py`
  - Implement SMA (Simple Moving Average)
  - Implement EMA (Exponential Moving Average)
  - Implement WMA (Weighted Moving Average)
  - Each class extends `Indicator` base class
  - Add unit tests: `tests/test_indicators/test_moving_averages.py`
  - Tests should verify calculations against known values

  **Must NOT do**:
  - Don't optimize for performance yet (keep it readable)
  - Don't handle edge cases beyond empty data

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Mathematical calculations need accuracy

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 7-9)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 17
  - **Blocked By**: Task 1, 2, 3

  **References**:
  - Pattern: `trading/indicators/base.py` (from Task 3)
  - Formula: SMA = sum(period) / period
  - Formula: EMA = (Price * k) + (Previous EMA * (1-k)), k=2/(period+1)
  - Formula: WMA = sum(weight * price) / sum(weights)

  **Acceptance Criteria**:
  - [ ] SMA implemented and tested
  - [ ] EMA implemented and tested
  - [ ] WMA implemented and tested
  - [ ] All tests pass: `pytest tests/test_indicators/test_moving_averages.py -v`

  **QA Scenarios**:
  ```
  Scenario: Test SMA calculation
    Tool: Bash
    Steps:
      1. cd C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading
      2. pytest tests/test_indicators/test_moving_averages.py::test_sma -v
    Expected Result: Test passes with known values verified
    Evidence: .sisyphus/evidence/task-6-moving-averages.txt
  ```

  **Commit**: YES (can group with 7-9)
  - Message: `feat(indicators): add moving averages (SMA, EMA, WMA)`
  - Files: trading/indicators/moving_averages.py, tests/test_indicators/test_moving_averages.py

- [x] 7. Implement RSI indicator

  **What to do**:
  - Create `trading/indicators/rsi.py`
  - Implement RSI (Relative Strength Index)
  - Period: configurable (default 14)
  - Overbought level: 70, Oversold level: 30
  - Add unit tests: `tests/test_indicators/test_rsi.py`
  - Verify with known test data (e.g., TradingView values)

  **Must NOT do**:
  - Don't implement divergences yet (keep it basic)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Calculation accuracy critical

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 6, 8-9)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 17
  - **Blocked By**: Task 1, 2, 3

  **References**:
  - Formula: RSI = 100 - (100 / (1 + RS))
  - RS = Average Gain / Average Loss
  - Standard: 14 periods

  **Acceptance Criteria**:
  - [ ] RSI implemented
  - [ ] Returns values 0-100
  - [ ] Tests pass with known values
  - [ ] pytest tests/test_indicators/test_rsi.py -v

  **QA Scenarios**:
  ```
  Scenario: Test RSI calculation
    Tool: Bash
    Steps:
      1. cd C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading
      2. pytest tests/test_indicators/test_rsi.py -v
    Expected Result: All tests pass
    Evidence: .sisyphus/evidence/task-7-rsi.txt
  ```

  **Commit**: YES (group with 6, 8-9)
  - Message: `feat(indicators): add RSI indicator`
  - Files: trading/indicators/rsi.py, tests/test_indicators/test_rsi.py

- [x] 8. Implement MACD indicator

  **What to do**:
  - Create `trading/indicators/macd.py`
  - Implement MACD with: Fast EMA (12), Slow EMA (26), Signal (9)
  - Calculate: MACD Line, Signal Line, Histogram
  - Add unit tests: `tests/test_indicators/test_macd.py`

  **Must NOT do**:
  - Don't implement histogram divergences

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Multi-component calculation

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 6-7, 9)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 17
  - **Blocked By**: Task 1, 2, 3

  **References**:
  - Formula: MACD = EMA(12) - EMA(26)
  - Signal = EMA(9) of MACD
  - Histogram = MACD - Signal

  **Acceptance Criteria**:
  - [ ] MACD Line calculated
  - [ ] Signal Line calculated
  - [ ] Histogram calculated
  - [ ] Tests pass

  **QA Scenarios**:
  ```
  Scenario: Test MACD components
    Tool: Bash
    Steps:
      1. pytest tests/test_indicators/test_macd.py -v
    Expected Result: All components tested and passing
    Evidence: .sisyphus/evidence/task-8-macd.txt
  ```

  **Commit**: YES (group with 6-7, 9)
  - Message: `feat(indicators): add MACD indicator`
  - Files: trading/indicators/macd.py, tests/test_indicators/test_macd.py

- [x] 9. Implement Bollinger Bands indicator

  **What to do**:
  - Create `trading/indicators/bollinger_bands.py`
  - Implement: Middle Band (SMA 20), Upper Band (+2 std dev), Lower Band (-2 std dev)
  - Add Bollinger Band Width and %B calculations
  - Add unit tests: `tests/test_indicators/test_bollinger_bands.py`

  **Must NOT do**:
  - Don't implement squeeze detection yet

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Statistical calculation

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 6-8)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 17
  - **Blocked By**: Task 1, 2, 3

  **References**:
  - Formula: Middle = SMA(20)
  - Upper = Middle + (2 * StdDev)
  - Lower = Middle - (2 * StdDev)
  - %B = (Price - Lower) / (Upper - Lower)

  **Acceptance Criteria**:
  - [ ] All 3 bands calculated
  - [ ] Width and %B calculated
  - [ ] Tests pass

  **QA Scenarios**:
  ```
  Scenario: Test Bollinger Bands
    Tool: Bash
    Steps:
      1. pytest tests/test_indicators/test_bollinger_bands.py -v
    Expected Result: All calculations verified
    Evidence: .sisyphus/evidence/task-9-bollinger.txt
  ```

  **Commit**: YES (group with 6-8)
  - Message: `feat(indicators): add Bollinger Bands`
  - Files: trading/indicators/bollinger_bands.py, tests/test_indicators/test_bollinger_bands.py

- [ ] 10. Enhanced risk management system

  **What to do**:
  - Enhance `trading/risk/manager.py`
  - Add position sizing methods: Fixed Lot, Fixed Risk %, Kelly Criterion
  - Add max drawdown protection (halt trading if DD > threshold)
  - Add correlation check (don't add correlated positions)
  - Add portfolio heat (total risk exposure)
  - Add unit tests: `tests/test_risk.py`

  **Must NOT do**:
  - Don't change existing RiskManager API (extend/add methods)
  - Don't remove existing lot_size calculation

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Complex risk calculations

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 6-9, 11)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 18
  - **Blocked By**: Task 2

  **References**:
  - Existing: `trading/risk/manager.py`
  - Pattern: Add new methods, keep existing calculate_lot_size

  **Acceptance Criteria**:
  - [ ] Fixed Lot sizing
  - [ ] Fixed Risk % sizing
  - [ ] Kelly Criterion sizing
  - [ ] Max drawdown protection
  - [ ] Portfolio heat calculation
  - [ ] All tests pass

  **QA Scenarios**:
  ```
  Scenario: Test risk manager methods
    Tool: Bash
    Steps:
      1. pytest tests/test_risk.py -v
    Expected Result: All risk calculations verified
    Evidence: .sisyphus/evidence/task-10-risk-manager.txt
  ```

  **Commit**: YES
  - Message: `feat(risk): enhanced risk management system`
  - Files: trading/risk/manager.py, tests/test_risk.py

- [ ] 11. Broker connector retry logic

  **What to do**:
  - Enhance `trading/brokers/ccxt/connector.py`
  - Add retry logic with exponential backoff for:
    - get_ohlcv()
    - place_order()
    - get_positions()
    - get_account_info()
  - Add connection health check
  - Add automatic reconnection on failure
  - Add unit tests with mocked broker: `tests/test_brokers/test_ccxt.py`

  **Must NOT do**:
  - Don't change BrokerConnector base class API
  - Don't modify MT5/MT4 connectors (only CCXT)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Network resilience logic

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 6-10)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 19
  - **Blocked By**: Task 2

  **References**:
  - Existing: `trading/brokers/ccxt/connector.py`
  - Use: `trading/utils/error_handler.py` retry decorator (Task 5)

  **Acceptance Criteria**:
  - [ ] Retry logic on all API calls (max 3 attempts)
  - [ ] Exponential backoff
  - [ ] Connection health check method
  - [ ] Mock tests verify retry behavior
  - [ ] Tests pass

  **QA Scenarios**:
  ```
  Scenario: Test broker retry logic
    Tool: Bash
    Steps:
      1. pytest tests/test_brokers/test_ccxt.py::test_retry_logic -v
    Expected Result: Retry on failure verified
    Evidence: .sisyphus/evidence/task-11-broker-retry.txt
  ```

  **Commit**: YES
  - Message: `feat(brokers): add retry logic to CCXT connector`
  - Files: trading/brokers/ccxt/connector.py, tests/test_brokers/test_ccxt.py

### Wave 3: Strategy Templates

- [ ] 12. Create strategy template base class

  **What to do**:
  - Create `trading/strategy/templates/` directory
  - Create `trading/strategy/templates/__init__.py`
  - Create `trading/strategy/templates/base.py`
  - Define StrategyTemplate base class that extends Strategy
  - Add hooks for: entry_conditions(), exit_conditions(), position_sizing()
  - Include validation and parameter management

  **Must NOT do**:
  - Don't modify existing `trading/strategy/base.py`
  - Don't create actual strategy yet (Tasks 13-16)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Template pattern design

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 6-9)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 13-16
  - **Blocked By**: Task 6-9

  **References**:
  - Pattern: `trading/strategy/base.py` Strategy class
  - Pattern: Template method pattern

  **Acceptance Criteria**:
  - [ ] `trading/strategy/templates/base.py` created
  - [ ] StrategyTemplate class extends Strategy
  - [ ] Hooks defined: entry_conditions, exit_conditions, position_sizing

  **QA Scenarios**:
  ```
  Scenario: Verify template base class
    Tool: Bash
    Steps:
      1. python -c "from trading.strategy.templates.base import StrategyTemplate; print('Template base OK')"
    Expected Result: Output shows "Template base OK"
    Evidence: .sisyphus/evidence/task-12-template-base.txt
  ```

  **Commit**: YES
  - Message: `feat(strategies): create strategy template base`
  - Files: trading/strategy/templates/

- [ ] 13. Breakout strategy template

  **What to do**:
  - Create `trading/strategy/templates/breakout.py`
  - Implement BreakoutTemplate class
  - Uses HH/LL breakout logic (similar to XAUUSD strategy)
  - Configurable lookback period for breakout detection
  - Add tests: `tests/test_strategies/test_breakout.py`

  **Must NOT do**:
  - Don't hardcode symbol-specific logic
  - Don't use fixed session times (make configurable)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Strategy logic

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 14-16)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 21
  - **Blocked By**: Task 4, 12

  **References**:
  - Pattern: `trading/strategy/templates/base.py` (Task 12)
  - Reference: `trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/strategy.py`

  **Acceptance Criteria**:
  - [ ] BreakoutTemplate class created
  - [ ] Configurable lookback period
  - [ ] Works with any symbol (uses symbol config)
  - [ ] Tests pass

  **QA Scenarios**:
  ```
  Scenario: Test breakout strategy
    Tool: Bash
    Steps:
      1. pytest tests/test_strategies/test_breakout.py -v
    Expected Result: Strategy generates correct signals
    Evidence: .sisyphus/evidence/task-13-breakout.txt
  ```

  **Commit**: YES (can group with 14-16)
  - Message: `feat(strategies): add breakout strategy template`
  - Files: trading/strategy/templates/breakout.py, tests/test_strategies/test_breakout.py

- [ ] 14. Trend Following strategy template

  **What to do**:
  - Create `trading/strategy/templates/trend_following.py`
  - Implement TrendFollowingTemplate class
  - Uses Moving Averages for trend detection
  - Entry: Fast MA crosses above Slow MA (bullish) / below (bearish)
  - Uses indicators from Task 6
  - Add tests

  **Must NOT do**:
  - Don't use fixed periods (make configurable)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Strategy with indicators

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 13, 15-16)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 21
  - **Blocked By**: Task 4, 6, 12

  **References**:
  - Pattern: Task 12 template base
  - Indicators: `trading/indicators/moving_averages.py` (Task 6)

  **Acceptance Criteria**:
  - [ ] TrendFollowingTemplate created
  - [ ] Uses SMA/EMA from indicators
  - [ ] Configurable periods
  - [ ] Tests pass

  **QA Scenarios**:
  ```
  Scenario: Test trend following strategy
    Tool: Bash
    Steps:
      1. pytest tests/test_strategies/test_trend_following.py -v
    Expected Result: MA crossovers detected correctly
    Evidence: .sisyphus/evidence/task-14-trend-following.txt
  ```

  **Commit**: YES (group with 13, 15-16)
  - Message: `feat(strategies): add trend following template`
  - Files: trading/strategy/templates/trend_following.py, tests/test_strategies/test_trend_following.py

- [ ] 15. Mean Reversion strategy template

  **What to do**:
  - Create `trading/strategy/templates/mean_reversion.py`
  - Implement MeanReversionTemplate class
  - Uses RSI or Bollinger Bands for overbought/oversold
  - Entry: RSI < 30 (buy) / RSI > 70 (sell)
  - Uses indicators from Task 7, 9
  - Add tests

  **Must NOT do**:
  - Don't use fixed RSI levels (make configurable)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Mean reversion logic

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 13-14, 16)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 21
  - **Blocked By**: Task 4, 7, 9, 12

  **References**:
  - Indicators: RSI (Task 7), Bollinger (Task 9)
  - Pattern: Task 12 template base

  **Acceptance Criteria**:
  - [ ] MeanReversionTemplate created
  - [ ] Uses RSI and/or Bollinger Bands
  - [ ] Configurable levels
  - [ ] Tests pass

  **QA Scenarios**:
  ```
  Scenario: Test mean reversion
    Tool: Bash
    Steps:
      1. pytest tests/test_strategies/test_mean_reversion.py -v
    Expected Result: Oversold/overbought signals correct
    Evidence: .sisyphus/evidence/task-15-mean-reversion.txt
  ```

  **Commit**: YES (group with 13-14, 16)
  - Message: `feat(strategies): add mean reversion template`
  - Files: trading/strategy/templates/mean_reversion.py, tests/test_strategies/test_mean_reversion.py

- [ ] 16. Scalping strategy template

  **What to do**:
  - Create `trading/strategy/templates/scalping.py`
  - Implement ScalpingTemplate class
  - Short-term strategy (5-15 min timeframe)
  - Uses Bollinger Bands + MACD
  - Tight SL/TP (1:1 or 1:1.5 R:R)
  - Uses indicators from Task 8, 9
  - Add tests

  **Must NOT do**:
  - Don't use hardcoded SL/TP (make configurable)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Short-term strategy

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 13-15)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 21
  - **Blocked By**: Task 4, 8, 9, 12

  **References**:
  - Indicators: MACD (Task 8), Bollinger (Task 9)
  - Pattern: Task 12 template base

  **Acceptance Criteria**:
  - [ ] ScalpingTemplate created
  - [ ] Uses MACD + Bollinger Bands
  - [ ] Configurable timeframe
  - [ ] Tests pass

  **QA Scenarios**:
  ```
  Scenario: Test scalping strategy
    Tool: Bash
    Steps:
      1. pytest tests/test_strategies/test_scalping.py -v
    Expected Result: Short-term signals generated
    Evidence: .sisyphus/evidence/task-16-scalping.txt
  ```

  **Commit**: YES (group with 13-15)
  - Message: `feat(strategies): add scalping strategy template`
  - Files: trading/strategy/templates/scalping.py, tests/test_strategies/test_scalping.py

### Wave 4: Tests & Integration

- [ ] 17. Unit tests for indicators (100% coverage)

  **What to do**:
  - Create `tests/test_indicators/` test suite
  - Test all 4 indicators: Moving Averages, RSI, MACD, Bollinger Bands
  - Test edge cases: empty data, single candle, minimum period
  - Test with known values from TradingView or other source
  - Achieve 100% coverage: `pytest --cov=trading/indicators`
  - Create `tests/test_indicators/__init__.py`

  **Must NOT do**:
  - Don't test implementation details, test behavior
  - Don't use live data in tests (use fixtures)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []
  - Reason: Comprehensive test writing

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 18-21)
  - **Parallel Group**: Wave 4
  - **Blocks**: Task 25
  - **Blocked By**: Task 6-9

  **References**:
  - Indicators: Tasks 6-9
  - Fixtures: `tests/conftest.py` (Task 1)

  **Acceptance Criteria**:
  - [ ] 100% coverage for `trading/indicators/`
  - [ ] All edge cases tested
  - [ ] Known values verified
  - [ ] `pytest tests/test_indicators/ -v` passes
  - [ ] `pytest --cov=trading/indicators` shows 100%

  **QA Scenarios**:
  ```
  Scenario: Test indicators coverage
    Tool: Bash
    Steps:
      1. pytest tests/test_indicators/ -v --cov=trading/indicators --cov-report=term-missing
    Expected Result: 100% coverage, all tests pass
    Evidence: .sisyphus/evidence/task-17-indicators-coverage.txt
  ```

  **Commit**: YES
  - Message: `test: add comprehensive indicator tests (100% coverage)`
  - Files: tests/test_indicators/

- [ ] 18. Unit tests for risk manager

  **What to do**:
  - Create `tests/test_risk.py`
  - Test all risk manager methods:
    - Fixed lot sizing
    - Fixed risk % sizing
    - Kelly Criterion
    - Max drawdown protection
    - Portfolio heat
  - Test edge cases: zero balance, extreme drawdown

  **Must NOT do**:
  - Don't test with real broker connections (mock)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []
  - Reason: Risk calculations test

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 17, 19-21)
  - **Parallel Group**: Wave 4
  - **Blocks**: Task 25
  - **Blocked By**: Task 10

  **References**:
  - Risk manager: `trading/risk/manager.py` (Task 10)

  **Acceptance Criteria**:
  - [ ] All risk methods tested
  - [ ] Edge cases covered
  - [ ] Tests pass

  **QA Scenarios**:
  ```
  Scenario: Test risk manager
    Tool: Bash
    Steps:
      1. pytest tests/test_risk.py -v
    Expected Result: All risk tests pass
    Evidence: .sisyphus/evidence/task-18-risk-tests.txt
  ```

  **Commit**: YES (can group with 17, 19-21)
  - Message: `test: add risk manager unit tests`
  - Files: tests/test_risk.py

- [ ] 19. Unit tests for broker connectors (mock)

  **What to do**:
  - Create `tests/test_brokers/` directory
  - Create `tests/test_brokers/test_ccxt.py`
  - Mock CCXT exchange for testing
  - Test: connect, disconnect, get_ohlcv, place_order, get_positions, get_account_info
  - Test retry logic: verify 3 attempts on failure
  - Test connection health check

  **Must NOT do**:
  - Don't make real API calls in tests
  - Don't test with real credentials

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Mock testing

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 17-18, 20-21)
  - **Parallel Group**: Wave 4
  - **Blocks**: Task 25
  - **Blocked By**: Task 11

  **References**:
  - Broker: `trading/brokers/ccxt/connector.py` (Task 11)
  - Python unittest.mock for mocking

  **Acceptance Criteria**:
  - [ ] All broker methods mocked and tested
  - [ ] Retry logic verified
  - [ ] Connection health check tested
  - [ ] Tests pass

  **QA Scenarios**:
  ```
  Scenario: Test broker with mocks
    Tool: Bash
    Steps:
      1. pytest tests/test_brokers/test_ccxt.py -v
    Expected Result: All broker tests pass
    Evidence: .sisyphus/evidence/task-19-broker-tests.txt
  ```

  **Commit**: YES (group with 17-18, 20-21)
  - Message: `test: add broker connector unit tests with mocks`
  - Files: tests/test_brokers/

- [ ] 20. Integration test script for OpenClaw

  **What to do**:
  - Create `scripts/test_integration.py`
  - Script tests full OpenClaw integration:
    1. Import all modules
    2. Create strategy instance
    3. Run backtest with mock data
    4. Verify metrics calculated
    5. Test CLI commands (simulate)
  - Output: JSON with test results
  - Exit code 0 if all pass, 1 if any fail

  **Must NOT do**:
  - Don't require broker connection
  - Don't use real API keys

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []
  - Reason: Integration script

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 17-19, 21)
  - **Parallel Group**: Wave 4
  - **Blocks**: Task 25
  - **Blocked By**: Task 1-21

  **References**:
  - Pattern: `scripts/xauusd_backtest.py`
  - Backtest: `trading/backtest/engine.py`

  **Acceptance Criteria**:
  - [ ] `scripts/test_integration.py` created
  - [ ] Tests all major components
  - [ ] Returns JSON results
  - [ ] Exit code based on results
  - [ ] Can run: `python scripts/test_integration.py`

  **QA Scenarios**:
  ```
  Scenario: Run integration test
    Tool: Bash
    Steps:
      1. cd C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading
      2. python scripts/test_integration.py
    Expected Result: Output shows JSON with all tests passed
    Evidence: .sisyphus/evidence/task-20-integration.json
  ```

  **Commit**: YES
  - Message: `test: add OpenClaw integration test script`
  - Files: scripts/test_integration.py

- [ ] 21. Backtest validation test suite

  **What to do**:
  - Create `tests/test_backtest.py`
  - Test backtest engine with strategy templates
  - Test each strategy template:
    - Breakout (Task 13)
    - Trend Following (Task 14)
    - Mean Reversion (Task 15)
    - Scalping (Task 16)
  - Verify metrics: win rate, profit factor, max drawdown
  - Test with EURUSD, GBPUSD, USDJPY configs

  **Must NOT do**:
  - Don't use large dataset (keep tests fast)
  - Don't test with real broker

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Backtest validation

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 17-20)
  - **Parallel Group**: Wave 4
  - **Blocks**: Task 25
  - **Blocked By**: Task 13-16

  **References**:
  - Backtest: `trading/backtest/engine.py`
  - Strategies: Tasks 13-16

  **Acceptance Criteria**:
  - [ ] All 4 strategy templates tested
  - [ ] All 3 forex pairs tested
  - [ ] Metrics validated
  - [ ] Tests pass

  **QA Scenarios**:
  ```
  Scenario: Test backtest validation
    Tool: Bash
    Steps:
      1. pytest tests/test_backtest.py -v
    Expected Result: All backtest tests pass
    Evidence: .sisyphus/evidence/task-21-backtest-validation.txt
  ```

  **Commit**: YES (group with 17-20)
  - Message: `test: add backtest validation test suite`
  - Files: tests/test_backtest.py

### Wave 5: Polish & Validation

- [ ] 22. Error handling improvements throughout

  **What to do**:
  - Apply error handling from Task 5 across codebase:
    - Add try/except in backtest engine
    - Add try/except in paper trade engine
    - Add try/except in real trade engine
    - Add try/except in broker connectors
    - Add try/except in data providers
  - Use custom exceptions from `trading/exceptions.py`
  - Add proper logging for all errors
  - Don't crash on non-critical errors (log and continue where appropriate)

  **Must NOT do**:
  - Don't change logic, only error handling
  - Don't swallow errors silently

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Error handling patterns

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 23-25)
  - **Parallel Group**: Wave 5
  - **Blocks**: Task 25
  - **Blocked By**: Task 5

  **References**:
  - Exceptions: `trading/exceptions.py` (Task 5)
  - Pattern: Proper logging levels

  **Acceptance Criteria**:
  - [ ] All engines have error handling
  - [ ] All brokers have error handling
  - [ ] All data providers have error handling
  - [ ] Custom exceptions used
  - [ ] Tests still pass

  **QA Scenarios**:
  ```
  Scenario: Verify error handling
    Tool: Bash
    Steps:
      1. grep -r "try:" trading/backtest/ trading/brokers/ trading/data/
      2. pytest tests/ -v
    Expected Result: Try blocks present, all tests pass
    Evidence: .sisyphus/evidence/task-22-error-handling.txt
  ```

  **Commit**: YES
  - Message: `fix: add comprehensive error handling throughout`
  - Files: trading/backtest/, trading/brokers/, trading/data/, trading/paper_trade/, trading/real_trade/

- [ ] 23. Performance optimization (if needed)

  **What to do**:
  - Profile indicators calculation with large datasets
  - Optimize if slow:
    - Use vectorized operations where possible
    - Cache intermediate calculations
    - Avoid unnecessary loops
  - Focus on: SMA, EMA, RSI (most used)

  **Must NOT do**:
  - Don't optimize prematurely
  - Don't break existing tests

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: Performance profiling

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 22, 24-25)
  - **Parallel Group**: Wave 5
  - **Blocks**: Task 25
  - **Blocked By**: Task 6-9

  **References**:
  - Indicators: Tasks 6-9
  - Python profiling tools

  **Acceptance Criteria**:
  - [ ] Performance acceptable (no test > 1s)
  - [ ] All tests pass
  - [ ] No regressions

  **QA Scenarios**:
  ```
  Scenario: Check performance
    Tool: Bash
    Steps:
      1. pytest tests/test_indicators/ -v --durations=10
    Expected Result: All tests < 1s
    Evidence: .sisyphus/evidence/task-23-performance.txt
  ```

  **Commit**: YES (only if changes made)
  - Message: `perf: optimize indicator calculations`
  - Files: trading/indicators/ (if modified)

- [ ] 24. Documentation updates

  **What to do**:
  - Update `SKILL.md` with new features:
    - Document new indicators
    - Document new strategy templates
    - Document new symbol configs
    - Document test commands
  - Update `README.md` with quickstart
  - Add docstrings to all new classes/methods
  - Create `docs/API.md` with API reference

  **Must NOT do**:
  - Don't duplicate existing docs
  - Don't remove existing content

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []
  - Reason: Documentation

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 22-23, 25)
  - **Parallel Group**: Wave 5
  - **Blocks**: Task 25
  - **Blocked By**: Task 1-23

  **References**:
  - Existing: `SKILL.md`, `README.md`

  **Acceptance Criteria**:
  - [ ] SKILL.md updated
  - [ ] README.md updated
  - [ ] Docstrings added
  - [ ] API.md created (optional)

  **QA Scenarios**:
  ```
  Scenario: Verify documentation
    Tool: Bash
    Steps:
      1. grep "RSI\|MACD\|Bollinger" SKILL.md
      2. grep "strategy template" README.md
    Expected Result: New features documented
    Evidence: .sisyphus/evidence/task-24-docs.txt
  ```

  **Commit**: YES
  - Message: `docs: update documentation for new features`
  - Files: SKILL.md, README.md, docs/API.md

- [ ] 25. End-to-end test: Run full pipeline

  **What to do**:
  - Create comprehensive end-to-end test
  - Test flow:
    1. Fetch data (mock or small real dataset)
    2. Run indicators on data
    3. Generate signals with strategy template
    4. Run backtest
    5. Verify metrics
  - Test with EURUSD and one strategy template
  - Save results to `.sisyphus/evidence/e2e/`

  **Must NOT do**:
  - Don't require real broker connection
  - Don't use large dataset

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []
  - Reason: End-to-end testing

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 22-24)
  - **Parallel Group**: Wave 5
  - **Blocks**: F1-F4
  - **Blocked By**: Task 1-24

  **References**:
  - Integration test: Task 20
  - Backtest: Task 21

  **Acceptance Criteria**:
  - [ ] End-to-end test passes
  - [ ] Results saved to `.sisyphus/evidence/e2e/`
  - [ ] No manual intervention needed

  **QA Scenarios**:
  ```
  Scenario: Run end-to-end test
    Tool: Bash
    Steps:
      1. cd C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading
      2. python scripts/test_e2e.py
    Expected Result: E2E test passes with metrics output
    Evidence: .sisyphus/evidence/e2e/e2e-results.json
  ```

  **Commit**: YES
  - Message: `test: add end-to-end test suite`
  - Files: scripts/test_e2e.py

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Rejection → fix → re-run.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, curl endpoint, run command). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `pytest` + linter. Review all changed files for: `as any`/`@ts-ignore`, empty catches, unused imports. Check AI slop: excessive comments, over-abstraction, generic names.
  Output: `Build [PASS/FAIL] | Lint [PASS/FAIL] | Tests [N pass/N fail] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high`
  Start from clean state. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test cross-task integration (features working together, not isolation). Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff (git log/diff). Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check "Must NOT do" compliance. Detect cross-task contamination.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- Wave 1: `feat(tests): setup pytest infrastructure` — tests/, pyproject.toml
- Wave 2: `feat(indicators): add technical indicators library` — trading/indicators/
- Wave 3: `feat(strategies): add strategy templates` — trading/strategy/templates/
- Wave 4: `test: add comprehensive test suite` — tests/
- Wave 5: `feat(core): improve risk, brokers, error handling` — trading/risk/, trading/brokers/
- Wave FINAL: `chore: final review and polish`

---

## Success Criteria

### Verification Commands
```bash
# Test suite
pytest tests/ -v

# Integration test
python scripts/test_integration.py

# Backtest validation
python scripts/backtest_validation_test.py

# Indicator tests
pytest tests/test_indicators.py -v

# All tests
pytest --cov=trading --cov-report=term-missing
```

### Final Checklist
- [ ] All 4 indicators implemented with tests (100% coverage)
- [ ] 4 strategy templates implemented
- [ ] EURUSD, GBPUSD, USDJPY symbol configs
- [ ] Risk manager enhanced with new features
- [ ] Broker connectors have retry logic
- [ ] Error handling improved throughout
- [ ] pytest runs all tests: PASS
- [ ] Integration test for OpenClaw: PASS
- [ ] Evidence files exist in .sisyphus/evidence/

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Technical indicator calculations wrong | Low | High | Use known test data, compare with TradingView |
| Broker API changes during development | Low | Medium | Mock in tests, document API version |
| Tests fail on CI but pass locally | Medium | Medium | Use Docker for consistent environment |
| OpenClaw integration issues | Medium | High | Create integration test script early |

---

*Plan generated by Prometheus*  
*Last updated: 2026-02-19*
