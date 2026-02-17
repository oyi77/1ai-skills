# Trading Skills System - Comprehensive Work Plan

## TL;DR

> **Quick Summary**: Create a comprehensive trading skills system for 1ai-skills repo with full trading team capabilities, autonomous operations, and multi-broker support. Includes XAUUSD 7-Candle Breakout strategy with backtest, paper trade, and real trade modes.

> **Deliverables**: 
> - Complete trading skills folder structure
> - Broker connectors (MT5, MT4, CCXT)
> - Strategy modules (crypto + tradfi)
> - Autonomous trading team skills
> - XAUUSD 7-Candle Breakout strategy implementation
> - Backtest, paper trade, and real trade modules
> - Risk management system
> - PR created to https://github.com/oyi77/1ai-skills

> **Estimated Effort**: XL (Large-scale system)
> **Parallel Execution**: YES - Multiple waves
> **Critical Path**: Foundation → Broker Connectors → Core Strategy → Autonomous Team → XAUUSD Implementation

---

## Context

### Original Request
User wants to create a trading skills system integrated into https://github.com/oyi77/1ai-skills with:
- Generic structure supporting multiple skills and autonomous system
- Support for OpenCrawl, research, fact collection, strategy improvement, strategy building, trade execution, MetaTrader connection, and risk management
- Folder structure: strategy/crypto and strategy/tradfi (forex, stocks, commodities)
- Full trading team with autonomous capabilities
- Broker connectors: MetaTrader (MT5, MT4) and CCXT

### Specific Implementation Request
XAUUSD Asia 7-Candle Breakout Strategy (H1) with:
- 7 candle window (3 before + COA + 3 after)
- HH/LL calculation with pending orders
- SL = 1R, TP = 2R risk/reward
- Backtest, paper trade, and real trade modes
- Complete UX commands

### Research Findings

#### Repository Structure (1ai-skills)
- 73 skills (42 local + 31 external)
- SKILL.md format with YAML header containing name, description, permissions
- SKILL_INDEX.json for skill registry
- Existing trading code in `research/polymarket-analyst/` (paper trading)

#### Broker Integration Research

**MetaTrader5 Python Library** (https://www.mql5.com/en/docs/python_metatrader5):
- Connection: `mt5.initialize()`, `mt5.login()`, `mt5.shutdown()`
- OHLCV: `mt5.copy_rates_from()`, `mt5.copy_rates_range()`, `mt5.copy_rates_from_pos()`
- Trading: `mt5.order_send()`, `mt5.order_check()`
- Positions/Orders: `mt5.positions_get()`, `mt5.orders_get()`, `mt5.history_deals_get()`
- Account: `mt5.account_info()`
- Error handling: `mt5.last_error()`

**CCXT Library** (https://github.com/ccxt/ccxt):
- Crypto-only (107 exchanges supported)
- DOES NOT support MT5/MT4
- For cryptocurrency strategies only
- OHLCV: `exchange.fetch_ohlcv(symbol, timeframe)`
- Trading: `exchange.createOrder()`, `exchange.cancelOrder()`

---

## Work Objectives

### Core Objective
Build a comprehensive trading skills system that enables:
1. Autonomous trading operations with full team capabilities
2. Multi-broker connectivity (MT5, MT4 for TradFi; CCXT for crypto)
3. Strategy development, testing, and execution
4. Risk management integration

### Concrete Deliverables
1. **Trading Skills Root**: `trading/SKILL.md` - Main trading skills entry point
2. **Broker Connectors**:
   - `trading/brokers/mt5/connector.py` - MetaTrader 5 Python integration
   - `trading/brokers/mt4/connector.py` - MetaTrader 4 Python integration
   - `trading/brokers/ccxt/connector.py` - CCXT crypto integration
3. **Strategy Modules**:
   - `trading/strategy/crypto/` - Cryptocurrency strategies
   - `trading/strategy/tradfi/forex/` - Forex strategies
   - `trading/strategy/tradfi/stocks/` - Stock strategies
   - `trading/strategy/tradfi/commodities/` - Commodity strategies
4. **Trading Team Skills**:
   - `trading/team/researcher/SKILL.md` - Market research automation
   - `trading/team/strategist/SKILL.md` - Strategy building
   - `trading/team/risk-manager/SKILL.md` - Risk management
   - `trading/team/executor/SKILL.md` - Trade execution
5. **XAUUSD 7-Candle Strategy**:
   - `trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout.py` - Core strategy logic
   - `trading/strategy/tradfi/commodities/backtest.py` - Backtest module
   - `trading/strategy/tradfi/commodities/paper_trade.py` - Paper trading module
   - `trading/strategy/tradfi/commodities/real_trade.py` - Real trading module
6. **Data Modules**:
   - `trading/data/collector.py` - Data collection
   - `trading/data/storage.py` - Data storage
7. **Risk Management**:
   - `trading/risk/manager.py` - Risk management system
8. **SKILL_INDEX.json Update** - Add all new skills

### Definition of Done
- [ ] All skills follow SKILL.md format
- [ ] Broker connectors can fetch OHLCV data
- [ ] Broker connectors can execute trades
- [ ] XAUUSD strategy calculates HH/LL correctly
- [ ] Backtest produces metrics and trade logs
- [ ] Paper trade tracks virtual positions
- [ ] Real trade shows guardrail summary before execution
- [ ] All configurations can be changed without modifying core code

### Must Have
- Broker connection for MT5, MT4, CCXT
- Backtest, paper trade, real trade modes
- Risk management with SL/TP calculation
- Asia session timing for XAUUSD strategy
- Trade log export (CSV/JSON)

### Must NOT Have
- Real money execution without user confirmation
- Hard-coded credentials in source files
- Execution without guardrail checks

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: NO - Creating new test infrastructure
- **Automated tests**: YES (TDD - Tests First)
- **Framework**: pytest
- **TDD Approach**: Each task includes test file creation BEFORE implementation
- **Agent-Executed QA**: Mandatory for all tasks (TDD doesn't replace QA scenarios)

### QA Policy
Every task includes agent-executed QA scenarios verifying:
- Broker connection establishment
- OHLCV data retrieval accuracy
- Strategy signal generation
- Backtest metrics calculation
- Paper trade position tracking
- Guardrail warnings

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Foundation - Start Immediately):
├── Task 1: Create trading/ folder structure [quick]
├── Task 2: Create SKILL_INDEX.json entries for all trading skills [quick]
├── Task 3: Create broker connector base classes [quick]
├── Task 4: Create MT5 connector implementation [quick]
├── Task 5: Create data storage module [quick]
├── Task 6: Create risk management base [quick]
└── Task 7: Create main trading SKILL.md [quick]

Wave 2 (Broker Connectors - MAX PARALLEL):
├── Task 8: CCXT connector (crypto) [quick]
├── Task 9: MT4 connector [quick]
├── Task 10: Data collector module [quick]
├── Task 11: Unified broker interface [quick]
└── Task 12: Connection pool/manager [quick]

Wave 3 (Strategy Foundation):
├── Task 13: Strategy base class [quick]
├── Task 14: XAUUSD 7-Candle strategy core logic [deep]
├── Task 15: Signal generator module [quick]
└── Task 16: Strategy config loader [quick]

Wave 4 (Trading Modes):
├── Task 17: Backtest engine [deep]
├── Task 18: Paper trade engine [deep]
├── Task 19: Real trade engine with guardrails [deep]
└── Task 20: Trade logger & exporter [quick]

Wave 5 (Trading Team Skills):
├── Task 21: Researcher skill [quick]
├── Task 22: Strategist skill [quick]
├── Task 23: Risk Manager skill [quick]
├── Task 24: Executor skill [quick]
└── Task 25: Team orchestrator skill [quick]

Wave 6 (Integration & Documentation):
├── Task 26: XAUUSD strategy SKILL.md [quick]
├── Task 27: Complete all strategy SKILL.md files [quick]
├── Task 28: Update main SKILL_INDEX.json [quick]
└── Task 29: Create README and examples [quick]

Wave 7 (Final Integration):
├── Task 30: Integration testing [deep]
├── Task 31: Code quality review [quick]
└── Task 32: Git PR creation [quick]
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|------------|--------|------|
| 1-7 | — | 8-16 | 1 |
| 8-12 | 1-7 | 13-16 | 2 |
| 13-16 | 8-12 | 17-20 | 3 |
| 17-20 | 13-16 | 21-25 | 4 |
| 21-25 | 17-20 | 26-29 | 5 |
| 26-29 | 21-25 | 30-31 | 6 |
| 30-32 | 26-29 | — | 7 |

---

## TODOs

### Wave 1: Foundation

- [ ] 1. Create trading/ folder structure

  **What to do**:
  - Create directories: trading/, trading/strategy/, trading/strategy/crypto/, trading/strategy/tradfi/, trading/strategy/tradfi/forex/, trading/strategy/tradfi/stocks/, trading/strategy/tradfi/commodities/, trading/team/, trading/brokers/, trading/brokers/mt5/, trading/brokers/mt4/, trading/brokers/ccxt/, trading/data/, trading/risk/, trading/backtest/, trading/paper_trade/, trading/real_trade/
  - Create __init__.py files for Python packages

  **Must NOT do**:
  - No actual implementation code yet

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Directory creation is trivial file system work
  - **Skills**: None required
  - **Skills Evaluated but Omitted**: N/A

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-7)
  - **Blocks**: Tasks 8-32
  - **Blocked By**: None

  **References**:
  - /Users/paijo/1ai-skills/research/polymarket-analyst/ - Existing trading code structure
  - /Users/paijo/1ai-skills/SKILL_INDEX.json - Skill registry format

  **Acceptance Criteria**:
  - [ ] All directories created under trading/
  - [ ] __init__.py files present in each Python package

  **Commit**: YES
  - Message: `feat(trading): create folder structure`
  - Files: trading/**/

---

- [ ] 2. Create SKILL_INDEX.json entries for trading skills

  **What to do**:
  - Add entries for: trading, trading-researcher, trading-strategist, trading-risk-manager, trading-executor, trading-team, xauusd-asia-7c-breakout
  - Follow existing SKILL_INDEX.json format with name, description, keywords, domains, source

  **Must NOT do**:
  - Don't create actual skill implementations

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: JSON entry creation is straightforward
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-7)

  **References**:
  - /Users/paijo/1ai-skills/SKILL_INDEX.json - Format reference

  **Acceptance Criteria**:
  - [ ] 7+ skill entries added to SKILL_INDEX.json

  **Commit**: YES
  - Message: `feat(trading): add skill index entries`
  - Files: SKILL_INDEX.json

---

- [ ] 3. Create broker connector base classes

  **What to do**:
  - Create base class `BrokerConnector` in trading/brokers/base.py
  - Define abstract methods: connect(), disconnect(), get_ohlcv(), place_order(), get_positions(), get_account_info()
  - Create enum for broker types: BROKER_TYPE_MT5, BROKER_TYPE_MT4, BROKER_TYPE_CCXT
  - Define data classes for OHLCV, Order, Position, AccountInfo

  **Must NOT do**:
  - Don't implement concrete broker connections

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Interface definitions are straightforward
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-7)

  **References**:
  - MT5 docs: https://www.mql5.com/en/docs/python_metatrader5
  - CCXT docs: https://docs.ccxt.com

  **Acceptance Criteria**:
  - [ ] BaseBroker class with all abstract methods defined
  - [ ] Data classes for OHLCV, Order, Position, AccountInfo
  - [ ] BrokerType enum defined

  **QA Scenarios**:

  ```
  Scenario: Import broker base module
    Tool: Bash
    Preconditions: Python environment available
    Steps:
      1. python -c "from trading.brokers.base import BaseBroker, BrokerType, OHLCV, Order, Position, AccountInfo; print('OK')"
    Expected Result: Module imports without errors
    Evidence: .sisyphus/evidence/task-3-import.txt

  **Commit**: YES
  - Message: `feat(trading): add broker base classes`
  - Files: trading/brokers/base.py
  - Pre-commit: python -c "from trading.brokers.base import BaseBroker"

---

- [ ] 4. Create MT5 connector implementation

  **What to do**:
  - Implement MT5Connector class inheriting from BaseBroker
  - Implement connect() using mt5.initialize()
  - Implement get_ohlcv() using mt5.copy_rates_from() and mt5.copy_rates_range()
  - Implement place_order() using mt5.order_send()
  - Implement get_positions() using mt5.positions_get()
  - Implement get_account_info() using mt5.account_info()
  - Implement error handling with mt5.last_error()

  **Must NOT do**:
  - Don't hardcode credentials

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Following MT5 documentation pattern
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-7)

  **References**:
  - Official MT5 Python docs: https://www.mql5.com/en/docs/python_metatrader5
  - Key functions: mt5.initialize(), mt5.copy_rates_from(), mt5.order_send(), mt5.positions_get(), mt5.account_info()

  **Acceptance Criteria**:
  - [ ] MT5Connector class implemented
  - [ ] All BaseBroker abstract methods implemented
  - [ ] Proper error handling

  **QA Scenarios**:

  ```
  Scenario: Import MT5 connector
    Tool: Bash
    Preconditions: pip install MetaTrader5
    Steps:
      1. python -c "from trading.brokers.mt5 import MT5Connector; print('OK')"
    Expected Result: Module imports without errors
    Evidence: .sisyphus/evidence/task-4-import.txt

  **Commit**: YES
  - Message: `feat(trading): implement MT5 connector`
  - Files: trading/brokers/mt5/__init__.py, trading/brokers/mt5/connector.py

---

- [ ] 5. Create data storage module

  **What to do**:
  - Create DataStorage class in trading/data/storage.py
  - Support CSV and JSON storage for OHLCV data
  - Support trade log storage (CSV/JSON)
  - Create methods: save_ohlcv(), load_ohlcv(), save_trade(), load_trades(), export_trades()

  **Must NOT do**:
  - Don't implement database connections yet

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: File I/O operations are straightforward
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-7)

  **References**:
  - /Users/paijo/1ai-skills/research/polymarket-analyst/paper_trading_data.json - Existing data format

  **Acceptance Criteria**:
  - [ ] DataStorage class with all methods
  - [ ] CSV and JSON support
  - [ ] Trade log export

  **QA Scenarios**:

  ```
  Scenario: DataStorage basic operations
    Tool: Bash
    Preconditions: Python with json, csv
    Steps:
      1. python -c "from trading.data.storage import DataStorage; ds = DataStorage('./data'); print('OK')"
    Expected Result: Storage initialized
    Evidence: .sisyphus/evidence/task-5-test.txt

  **Commit**: YES
  - Message: `feat(trading): add data storage module`
  - Files: trading/data/storage.py
  - Pre-commit: python -c "from trading.data.storage import DataStorage"

---

- [ ] 6. Create risk management base

  **What to do**:
  - Create RiskManager class in trading/risk/manager.py
  - Calculate position size based on risk percent
  - Calculate SL/TP in points and price
  - Validate trade parameters (max spread, max drawdown)
  - Support fixed lot and fixed risk percent modes

  **Must NOT do**:
  - Don't connect to live accounts

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Risk calculations are mathematical
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-7)

  **References**:
  - User requirements: risk_mode (fixed_lot/fixed_risk_percent), risk_percent, rr_ratio

  **Acceptance Criteria**:
  - [ ] RiskManager class with calculate_position_size()
  - [ ] SL/TP calculation methods
  - [ ] Parameter validation methods

  **QA Scenarios**:

  ```
  Scenario: RiskManager calculations
    Tool: Bash
    Preconditions: Python environment
    Steps:
      1. python -c "from trading.risk.manager import RiskManager; rm = RiskManager(); size = rm.calculate_position_size(1000, 2.0, 2034.50, 2033.30); print(f'Position size: {size}')"
    Expected Result: Calculated position size output
    Evidence: .sisyphus/evidence/task-6-test.txt

  **Commit**: YES
  - Message: `feat(trading): add risk management module`
  - Files: trading/risk/manager.py

---

- [ ] 7. Create main trading SKILL.md

  **What to do**:
  - Create trading/SKILL.md following existing SKILL.md format
  - Include YAML header with name, description, permissions
  - Document capabilities: broker connection, strategy execution, backtest, paper trade, real trade
  - Document commands: setup, connect, signal, backtest, paper, real

  **Must NOT do**:
  - Don't include credentials in skill file

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation creation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-7)

  **References**:
  - /Users/paijo/1ai-skills/core/self-improving-agent/SKILL.md - Format reference
  - /Users/paijo/1ai-skills/automation/job-hunter/SKILL.md - Format reference

  **Acceptance Criteria**:
  - [ ] trading/SKILL.md created
  - [ ] YAML header with name, description, permissions
  - [ ] Capabilities section
  - [ ] Commands documentation

  **Commit**: YES
  - Message: `docs(trading): add main trading skill`
  - Files: trading/SKILL.md

---

### Wave 2: Broker Connectors

- [ ] 8. CCXT connector (crypto)

  **What to do**:
  - Implement CCXTConnector class in trading/brokers/ccxt/connector.py
  - Support major exchanges: Binance, OKX, Bybit, KuCoin
  - Implement get_ohlcv() using exchange.fetch_ohlcv()
  - Implement place_order() using exchange.createOrder()
  - Implement get_positions() using exchange.fetch_positions()
  - Implement get_account_info() using exchange.fetch_balance()

  **Must NOT do**:
  - Don't hardcode API keys

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Following CCXT documentation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 8-12)
  - **Blocks**: Task 13
  - **Blocked By**: Task 3, 5

  **References**:
  - CCXT GitHub: https://github.com/ccxt/ccxt
  - CCXT Docs: https://docs.ccxt.com

  **Acceptance Criteria**:
  - [ ] CCXTConnector implemented
  - [ ] Supports Binance, OKX, Bybit, KuCoin
  - [ ] All BaseBroker methods implemented

  **Commit**: YES
  - Message: `feat(trading): add CCXT connector`
  - Files: trading/brokers/ccxt/connector.py

---

- [ ] 9. MT4 connector

  **What to do**:
  - Implement MT4Connector class in trading/brokers/mt4/connector.py
  - Note: MT4 Python library is limited compared to MT5
  - Create wrapper with available methods
  - Document limitations

  **Must NOT do**:
  - Don't implement features not supported by MT4 Python

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Wrapper implementation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 8-12)

  **References**:
  - MT4 Python resources: https://www.mql4.com/pen/python

  **Acceptance Criteria**:
  - [ ] MT4Connector implemented (or documented limitation)
  - [ ] Base methods available

  **Commit**: YES
  - Message: `feat(trading): add MT4 connector`
  - Files: trading/brokers/mt4/connector.py

---

- [ ] 10. Data collector module

  **What to do**:
  - Create DataCollector class in trading/data/collector.py
  - Collect OHLCV from broker connectors
  - Support historical data collection for backtesting
  - Support live data subscription for paper/real trading
  - Store collected data using DataStorage

  **Must NOT do**:
  - Don't implement data sources beyond brokers

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Data aggregation logic
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 8-12)

  **References**:
  - Task 5 (DataStorage)
  - Task 4, 8, 9 (Broker connectors)

  **Acceptance Criteria**:
  - [ ] DataCollector class implemented
  - [ ] Historical data collection
  - [ ] Live data support (optional)

  **Commit**: YES
  - Message: `feat(trading): add data collector`
  - Files: trading/data/collector.py

---

- [ ] 11. Unified broker interface

  **What to do**:
  - Create BrokerFactory in trading/brokers/factory.py
  - Create unified interface for switching between brokers
  - Implement broker selection by type
  - Add connection pooling for multiple brokers

  **Must NOT do**:
  - Don't implement complex connection management yet

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Factory pattern implementation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 8-12)

  **References**:
  - Task 3 (Base classes)
  - Task 4, 8, 9 (Connectors)

  **Acceptance Criteria**:
  - [ ] BrokerFactory implemented
  - [ ] Can create MT5, MT4, CCXT connectors

  **Commit**: YES
  - Message: `feat(trading): add broker factory`
  - Files: trading/brokers/factory.py

---

- [ ] 12. Connection pool/manager

  **What to do**:
  - Create BrokerManager class for managing multiple broker connections
  - Implement connection health checks
  - Add reconnection logic
  - Support broker failover

  **Must NOT do**:
  - Don't implement complex failover yet

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Connection management
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 8-12)

  **References**:
  - Task 11 (BrokerFactory)

  **Acceptance Criteria**:
  - [ ] BrokerManager class
  - [ ] Health check methods

  **Commit**: YES
  - Message: `feat(trading): add broker manager`
  - Files: trading/brokers/manager.py

---

### Wave 3: Strategy Foundation

- [ ] 13. Strategy base class

  **What to do**:
  - Create Strategy base class in trading/strategy/base.py
  - Define abstract methods: get_signals(), calculate_hh_ll(), calculate_sl_tp()
  - Add configuration handling
  - Add logging capabilities

  **Must NOT do**:
  - Don't implement specific strategies

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Base class definition
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 13-16)
  - **Blocks**: Tasks 17-20
  - **Blocked By**: Tasks 8-12

  **References**:
  - User requirements: 7 candle window, HH/LL, SL/TP calculation

  **Acceptance Criteria**:
  - [ ] Strategy base class
  - [ ] Abstract methods defined

  **Commit**: YES
  - Message: `feat(trading): add strategy base class`
  - Files: trading/strategy/base.py

---

- [ ] 14. XAUUSD 7-Candle strategy core logic

  **What to do**:
  - Implement XAUUSDAsia7CBreakout class in trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout.py
  - Implement 7-candle window identification (COA-3 to COA+3)
  - Implement HH/LL calculation from 7-candle window
  - Implement R (range) calculation from last candle
  - Implement pending order level calculation
  - Implement SL/TP calculation based on R and RR ratio
  - Implement Asia session time filtering

  **Must NOT do**:
  - Don't implement execution logic

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Core trading logic with precise calculations
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 13-16)

  **References**:
  - User requirements: 7 candle window, HH = max(high), LL = min(low), R = range of candle 7, SL = 1R, TP = 2R, Asia session

  **Acceptance Criteria**:
  - [ ] XAUUSDAsia7CBreakout class implemented
  - [ ] COA identification correct
  - [ ] HH/LL calculation correct
  - [ ] R calculation correct
  - [ ] SL/TP calculation correct
  - [ ] Asia session filtering correct

  **QA Scenarios**:

  ```
  Scenario: XAUUSD strategy signal generation
    Tool: Bash
    Preconditions: Python environment
    Steps:
      1. Create test OHLCV data with known values
      2. Run strategy.get_signals()
      3. Verify HH/LL/R calculation
    Expected Result: Correct signal with HH, LL, R, SL, TP
    Evidence: .sisyphus/evidence/task-14-test.txt

  **Commit**: YES
  - Message: `feat(trading): implement XAUUSD 7-candle strategy`
  - Files: trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout.py

---

- [ ] 15. Signal generator module

  **What to do**:
  - Create SignalGenerator class in trading/strategy/signal_generator.py
  - Generate structured signal output
  - Include all required levels: HH, LL, R, buy_stop, sell_stop, sl, tp
  - Add signal validation

  **Must NOT do**:
  - Don't implement strategy-specific logic

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Data formatting
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 13-16)

  **References**:
  - Task 14 (Strategy logic)

  **Acceptance Criteria**:
  - [ ] SignalGenerator class
  - [ ] Signal output format matches user requirements

  **Commit**: YES
  - Message: `feat(trading): add signal generator`
  - Files: trading/strategy/signal_generator.py

---

- [ ] 16. Strategy config loader

  **What to do**:
  - Create ConfigLoader in trading/strategy/config.py
  - Load strategy parameters from YAML/JSON
  - Support default values
  - Validate configuration

  **Must NOT do**:
  - Don't hardcode configuration

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Configuration handling
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 13-16)

  **References**:
  - User requirements: All configurable parameters

  **Acceptance Criteria**:
  - [ ] ConfigLoader class
  - [ ] All user parameters configurable

  **Commit**: YES
  - Message: `feat(trading): add strategy config loader`
  - Files: trading/strategy/config.py

---

### Wave 4: Trading Modes

- [ ] 17. Backtest engine

  **What to do**:
  - Create BacktestEngine in trading/backtest/engine.py
  - Implement historical data simulation
  - Implement pending order trigger simulation
  - Implement SL/TP hit detection
  - Implement cancel logic (opposite trigger, session end)
  - Calculate metrics: total trades, win rate, profit factor, max drawdown, expectancy
  - Generate trade log with CSV/JSON export
  - Support slippage, spread, commission modeling

  **Must NOT do**:
  - Don't execute real trades

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Complex simulation logic
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 17-20)
  - **Blocks**: Task 21
  - **Blocked By**: Tasks 13-16

  **References**:
  - User requirements: Backtest section with all metrics

  **Acceptance Criteria**:
  - [ ] BacktestEngine class implemented
  - [ ] Historical simulation works
  - [ ] All metrics calculated
  - [ ] Trade log exportable

  **QA Scenarios**:

  ```
  Scenario: Backtest execution
    Tool: Bash
    Preconditions: Python with test data
    Steps:
      1. Load historical OHLCV data
      2. Run backtest for date range
      3. Verify metrics output
    Expected Result: Complete backtest with metrics
    Evidence: .sisyphus/evidence/task-17-test.txt

  **Commit**: YES
  - Message: `feat(trading): add backtest engine`
  - Files: trading/backtest/engine.py

---

- [ ] 18. Paper trade engine

  **What to do**:
  - Create PaperTradeEngine in trading/paper_trade/engine.py
  - Subscribe to live OHLCV updates
  - Track virtual positions
  - Calculate virtual P&L
  - Implement daily briefing output
  - Persist state for restart

  **Must NOT do**:
  - Don't connect to real broker for execution

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: State management and live updates
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 17-20)

  **References**:
  - /Users/paijo/1ai-skills/research/polymarket-analyst/paper_trader_v2.py - Reference implementation

  **Acceptance Criteria**:
  - [ ] PaperTradeEngine class
  - [ ] Virtual position tracking
  - [ ] Daily briefing output
  - [ ] State persistence

  **Commit**: YES
  - Message: `feat(trading): add paper trade engine`
  - Files: trading/paper_trade/engine.py

---

- [ ] 19. Real trade engine with guardrails

  **What to do**:
  - Create RealTradeEngine in trading/real_trade/engine.py
  - Implement guardrail checks before execution
  - Show parameter summary before trade
  - Implement spread check
  - Implement SL/TP placement
  - Implement cancel opposite pending
  - Implement cancel all at session end
  - Implement one trade per day limit
  - Support execution plan generation (if no API access)

  **Must NOT do**:
  - Don't auto-execute without confirmation

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Safety-critical trading logic
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 17-20)

  **References**:
  - User requirements: Real Money mode with guardrails section

  **Acceptance Criteria**:
  - [ ] RealTradeEngine class
  - [ ] Guardrail checks implemented
  - [ ] Parameter summary before execution
  - [ ] Execution plan generation (fallback)

  **QA Scenarios**:

  ```
  Scenario: Guardrail check
    Tool: Bash
    Preconditions: Python environment
    Steps:
      1. Create RealTradeEngine
      2. Call guardrail_check() with high spread
      3. Verify trade blocked
    Expected Result: Trade blocked due to high spread
    Evidence: .sisyphus/evidence/task-19-test.txt

  **Commit**: YES
  - Message: `feat(trading): add real trade engine with guardrails`
  - Files: trading/real_trade/engine.py

---

- [ ] 20. Trade logger & exporter

  **What to do**:
  - Create TradeLogger in trading/data/trade_logger.py
  - Log all trades with full details
  - Export to CSV and JSON
  - Support trade history queries

  **Must NOT do**:
  - Don't implement duplicate logging

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Logging utilities
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 17-20)

  **References**:
  - Task 5 (DataStorage)
  - User requirements: Export trades command

  **Acceptance Criteria**:
  - [ ] TradeLogger class
  - [ ] CSV export
  - [ ] JSON export

  **Commit**: YES
  - Message: `feat(trading): add trade logger`
  - Files: trading/data/trade_logger.py

---

### Wave 5: Trading Team Skills

- [ ] 21. Researcher skill

  **What to do**:
  - Create trading/team/researcher/SKILL.md
  - Document research automation capabilities
  - Include commands: analyze_market, collect_data, scan_opportunities
  - Follow SKILL.md format

  **Must NOT do**:
  - Don't implement actual research algorithms

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 5 (with Tasks 21-25)
  - **Blocked By**: Task 17

  **References**:
  - /Users/paijo/1ai-skills/research/polymarket-analyst/SKILL.md - Reference

  **Acceptance Criteria**:
  - [ ] Researcher SKILL.md created
  - [ ] Commands documented

  **Commit**: YES
  - Message: `docs(trading): add researcher skill`
  - Files: trading/team/researcher/SKILL.md

---

- [ ] 22. Strategist skill

  **What to do**:
  - Create trading/team/strategist/SKILL.md
  - Document strategy building capabilities
  - Include commands: build_strategy, test_strategy, optimize_parameters

  **Must NOT do**:
  - Don't implement strategy generation

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 5 (with Tasks 21-25)

  **Acceptance Criteria**:
  - [ ] Strategist SKILL.md created

  **Commit**: YES
  - Message: `docs(trading): add strategist skill`
  - Files: trading/team/strategist/SKILL.md

---

- [ ] 23. Risk Manager skill

  **What to do**:
  - Create trading/team/risk-manager/SKILL.md
  - Document risk management capabilities
  - Include commands: assess_risk, calculate_position, validate_trade

  **Must NOT do**:
  - Don't implement live risk monitoring

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 5 (with Tasks 21-25)

  **References**:
  - Task 6 (Risk management module)

  **Acceptance Criteria**:
  - [ ] Risk Manager SKILL.md created

  **Commit**: YES
  - Message: `docs(trading): add risk manager skill`
  - Files: trading/team/risk-manager/SKILL.md

---

- [ ] 24. Executor skill

  **What to do**:
  - Create trading/team/executor/SKILL.md
  - Document trade execution capabilities
  - Include commands: execute_signal, monitor_positions, close_trade

  **Must NOT do** - Don't implement execution without guardrails

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 5 (with Tasks 21-25)

  **References**:
  - Task 19 (Real trade engine)

  **Acceptance Criteria**:
  - [ ] Executor SKILL.md created

  **Commit**: YES
  - Message: `docs(trading): add executor skill`
  - Files: trading/team/executor/SKILL.md

---

- [ ] 25. Team orchestrator skill

  **What to do**:
  - Create trading/team/orchestrator/SKILL.md
  - Document team coordination capabilities
  - Include autonomous workflow commands

  **Must NOT do**:
  - Don't implement complex orchestration

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 5 (with Tasks 21-25)

  **Acceptance Criteria**:
  - [ ] Team orchestrator SKILL.md created

  **Commit**: YES
  - Message: `docs(trading): add team orchestrator skill`
  - Files: trading/team/orchestrator/SKILL.md

---

### Wave 6: Integration & Documentation

- [ ] 26. XAUUSD strategy SKILL.md

  **What to do**:
  - Create trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/SKILL.md
  - Document full XAUUSD strategy
  - Include setup, signal today, backtest, paper, real commands
  - Document all configuration parameters
  - Follow SKILL.md format

  **Must NOT do**:
  - Don't duplicate code documentation

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 6 (with Tasks 26-29)
  - **Blocked By**: Tasks 21-25

  **References**:
  - User requirements: UX Skill section with all commands

  **Acceptance Criteria**:
  - [ ] XAUUSD strategy SKILL.md created
  - [ ] All commands documented

  **Commit**: YES
  - Message: `docs(trading): add XAUUSD strategy skill`
  - Files: trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/SKILL.md

---

- [ ] 27. Complete all strategy SKILL.md files

  **What to do**:
  - Create SKILL.md for each strategy folder
  - trading/strategy/crypto/SKILL.md
  - trading/strategy/tradfi/SKILL.md
  - trading/strategy/tradfi/forex/SKILL.md
  - trading/strategy/tradfi/stocks/SKILL.md
  - trading/strategy/tradfi/commodities/SKILL.md
  - trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/SKILL.md (from Task 26)

  **Must NOT do**:
  - Don't create implementation documentation

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 6 (with Tasks 26-29)

  **Acceptance Criteria**:
  - [ ] All strategy SKILL.md files created

  **Commit**: YES
  - Message: `docs(trading): add strategy skill docs`
  - Files: trading/strategy/**/SKILL.md

---

- [ ] 28. Update main SKILL_INDEX.json

  **What to do**:
  - Add all new skills to SKILL_INDEX.json
  - Include paths and categories
  - Ensure proper format

  **Must NOT do**:
  - Don't miss any skill entries

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: JSON update
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 6 (with Tasks 26-29)

  **References**:
  - Task 2 (Initial entries)
  - Task 21-26 (Additional skills)

  **Acceptance Criteria**:
  - [ ] All trading skills in SKILL_INDEX.json

  **Commit**: YES
  - Message: `feat(trading): update skill index`
  - Files: SKILL_INDEX.json

---

- [ ] 29. Create README and examples

  **What to do**:
  - Create trading/README.md
  - Include getting started guide
  - Include configuration examples
  - Include command reference

  **Must NOT do**:
  - Don't include credentials

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 6 (with Tasks 26-29)

  **Acceptance Criteria**:
  - [ ] trading/README.md created

  **Commit**: YES
  - Message: `docs(trading): add trading README`
  - Files: trading/README.md

---

### Wave 7: Final Integration

- [ ] 30. Integration testing

  **What to do**:
  - Test broker connections (mock if no live account)
  - Test backtest with sample data
  - Test strategy calculations with known inputs
  - Verify all modules work together

  **Must NOT do**:
  - Don't test with real money

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Integration verification
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 7 (with Tasks 30-32)
  - **Blocked By**: Tasks 26-29

  **References**:
  - All previous tasks

  **Acceptance Criteria**:
  - [ ] All modules import correctly
  - [ ] Backtest runs without errors
  - [ ] Strategy calculations verified

  **Commit**: NO

---

- [ ] 31. Code quality review

  **What to do**:
  - Run Python linter (flake8/ruff)
  - Check for common issues
  - Verify documentation completeness

  **Must NOT do**:
  - Don't skip critical issues

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Code review
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 7 (with Tasks 30-32)

  **Acceptance Criteria**:
  - [ ] No critical lint errors
  - [ ] All files have documentation

  **Commit**: NO

---

- [ ] 32. Git PR creation

  **What to do**:
  - Create new branch: feature/trading-skills-system
  - Commit all changes
  - Push to remote
  - Create PR to https://github.com/oyi77/1ai-skills

  **Must NOT do**:
  - Don't push to main branch

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Git operations
  - **Skills**: None required

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 7 (with Tasks 30-32)
  - **Blocked By**: Task 30, 31

  **Acceptance Criteria**:
  - [ ] Branch created
  - [ ] PR created
  - [ ] All files committed

  **Commit**: YES (automatic with PR)

---

## Success Criteria

### Verification Commands
```bash
# Import all modules
python -c "from trading.brokers import MT5Connector, CCXTConnector; from trading.strategy import XAUUSDAsia7CBreakout; from trading.backtest import BacktestEngine; from trading.paper_trade import PaperTradeEngine; from trading.real_trade import RealTradeEngine; print('All imports OK')"

# Run tests
pytest trading/ -v
```

### Final Checklist
- [ ] All 32 tasks completed
- [ ] PR created to https://github.com/oyi77/1ai-skills
- [ ] All skills follow SKILL.md format
- [ ] XAUUSD strategy implements all user requirements
- [ ] Backtest, paper trade, real trade modes working
- [ ] Risk management integrated
- [ ] Documentation complete
