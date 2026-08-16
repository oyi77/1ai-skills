---
name: dsl-vm-reverse
description: Use when reverse JavaScript-based custom DSL/VM interpreters, non-standard
  WASM-like runtimes, and risk-control engines. Use when analyzing IIFE or switch-based
  opcode dispatchers, extracting instruction tables, recovering bytecode semantics,
  capturing VM state at runtime, or reconstructing execution flow.
domain: cybersecurity
subdomain: web-application-security
tags:
- javascript
- reverse-engineering
- dsl
- vm
- anti-bot
- obfuscation
- risk-control
- web-application-security
version: '1.0'
author: oyi77
license: Apache-2.0
nist_csf:
- DE.AE-02
- RS.AN-03
- ID.RA-01
- DE.CM-01
category: cybersecurity
---


# DSL VM Reverse Engineering

## Overview

Many hardened web applications do not run their anti-bot or risk-control logic
as plain JavaScript. Instead they compile it to a custom bytecode interpreted by
a hand-rolled virtual machine — an IIFE wrapping a `switch`-based opcode
dispatcher over a single-letter variable array (typically `d[]`), with a
constant table (typically `C[9]`). The dispatcher is usually named `DG()`,
`W()` or similar. Because the interpreter never appears in source maps and the
bytecode is stored as a numeric constant table, the logic is invisible to
standard static review and survives even after the surrounding JS is
beautified.

This skill is a repeatable, six-phase workflow for reversing such engines:
identify the VM, recover variable and opcode semantics, extract the constant
table, locate exported functions, and — when static analysis is not enough —
capture VM state at runtime. It targets the common `AWSCInner` family of
risk-control engines but generalizes to any IIFE/switch-based dispatcher.

Source: cherry-picked and translated from `zhaoxuya520/reverse-skill`
(`skills/reverse-engineering/dsl-vm-reverse`, MIT license).

## When to Use

**Trigger phrases:**
- "reverse a DSL VM"
- "analyze risk-control engine bytecode"
- "extract opcode table from obfuscated JS"
- "recover VM semantics from an IIFE dispatcher"
- "capture VM state at runtime"
- "reconstruct execution flow of an anti-bot interpreter"

Use this skill when:

- A page's behavior is driven by an interpreter whose `switch` dispatch handles
  numeric opcodes rather than readable statements.
- You need the meaning of opcodes, operands, or the constant table before you
  can reason about what the code does.
- Static beautified JS is not enough and you must capture interpreter state
  (variables, return values, module exports) at runtime.
- You are analyzing a WASM-like runtime that is not actual WebAssembly
  (`\x00asm` magic absent) but a JS bytecode VM.

## Prerequisites

- Node.js 18+ for running reconstructed VM code and scripts.
- A browser automation stack for runtime capture: Selenium with CDP access, or
  Playwright (`npm i playwright`).
- A JS beautifier (prettier, js-beautify) and a code editor with regex search.
- Optional: Chrome DevTools Protocol knowledge for `Input.dispatchMouseEvent`.

## Workflow

### Phase 1: VM Identification (10-30 min)

Confirm the target is a custom DSL VM and not plain JS:

1. Check for a WASM payload: scan for the `\x00asm` magic bytes and compute the
   zero-byte percentage of the script. A high zero-byte ratio with no `\x00asm`
   header points to a custom bytecode blob, not WASM.
2. Look for the IIFE pattern `var U=void 0;` or equivalent single-letter
   hoisting that precedes a `switch (d[7]&31)` style dispatcher.
3. Confirm the dispatcher signature: `function DG(){...}` reading and writing a
   shared array `d[]`, with a constant table `C[9]` referenced as `C[9][n]`.

If none of these match, the target is ordinary obfuscated JS — use
`js-reverse` instead.

### Phase 2: Variable Mapping (30-60 min)

Build a variable meaning table before touching opcodes:

1. Extract assignments: regex `var\s+(\w+)\s*=\s*(\d+)` over the first 2000
   characters of the VM body.
2. Record the numeric literal bound to each single-letter variable. These
   literals are array indices or opcode constants, not real values.
3. Map the dispatcher array: `d[7]` is typically the instruction pointer /
   current opcode slot, `d[4]`/`d[5]` arithmetic registers, `d[6]` the operand
   stack, `d[8]` a scratch register, `d[9]` a return/throw slot. Verify each
   role from its usage across the switch body.

### Phase 3: Opcode Extraction and Classification (1-2 hours)

1. Extract every `case N:` label from the dispatcher switch. Each case is one
   opcode.
2. Classify each case by its statement shape (see the reference table below):

   | Statement shape | Classification |
   |---|---|
   | `d[7]=...` (no condition) | BRANCH |
   | `return ...` / `throw ...` | RETURN |
   | `W(C[` ... `,null,function(){...})` | CALL |
   | `new ...` | ALLOC |
   | `try{...}catch(...){...}` | EXCEPTION |
   | `d[x]=d[y][C[n]]` / `d[x]=d[y]<d[z]` | ARITH / STORE |
   | `P[d[9]]=...` | STORE (data handoff) |

3. Record, for each opcode number, the classification and a one-line comment
   describing its effect. Keep this table in your notes — it becomes the
   instruction set reference for Phase 5.

### Phase 4: Constant Table Analysis (30-60 min)

1. Grep the VM for references to the constant table: `C\[9\]\[(\d+)\]`.
2. Collect the full set of referenced indices — this bounds how much bytecode
   the interpreter can address.
3. For each referenced index, note the constant value and where it is consumed
   (opcode operand, function index, string pool offset).
4. The constant table is the bytecode store: exported functions whose bodies
   are not present as JS source are implemented as numeric sequences in
   `C[9]`.

### Phase 5: Exported Function Tracing (1-2 hours)

1. Find the registration call, e.g. `AWSCInner.register(name, moduleName,
   factory)` or an equivalent `register()` invocation.
2. Resolve `moduleName` → the factory function → the object it returns.
3. If a function name does not exist in the JS source, it is stored as
   bytecode in `C[9]` — note the index range.
4. Trace the call chain:

   ```javascript
   AWSCInner._modules['fy'].getToken()
   → W(C[<functionIndex>], null, ...)
   → DG()  // interpreter executes the encoded instruction sequence
   ```

5. Convert the traced bytecode range into the reconstructed semantics from
   Phase 3 so you can read what the exported function actually computes.

### Phase 6: Runtime Injection (when static analysis is insufficient)

If pure static reconstruction stalls (unresolved jumps, dynamic table writes,
state-dependent branches), inject a minimal compatible environment and run the
VM:

```javascript
// Minimal AWSC-compatible environment
const fakeEnv = {
    AWSCInner: {
        _modules: {},
        register(name, moduleName, factory) {
            this._modules[moduleName] = factory();
        }
    }
};

// Execute the DSL VM code in this sandbox
dslVmCode.call(fakeEnv);

// Read exports
const token = fakeEnv.AWSCInner._modules['fy'].getToken({});
```

Drive the real page when the VM needs live browser context (see Runtime
Capture below). In either case, log every `d[]` write at interesting opcodes to
produce a state trace for verification.

## Opcode Reference (observed on AWSC-family engines)

| Opcode | Type | Characteristic statement |
|---|---|---|
| 0 | BRANCH | `d[7]=xxx` unconditional jump |
| 1 | CALL | `W(C[Y],null,function(){...})` embedded call |
| 2 | ARITH | `d[4]=0`, `d[7]=72` register assignment |
| 3 | ARITH | `d[0]=d[1][C[x]]`, `d[5]=d[0]<d[3]` compare |
| 4 | STORE | `d[8]=d[5]in d[4]` property/in check |
| 5 | ARITH | `d[8]=d[4]-d[8]` arithmetic |
| 6 | RETURN | `return gV` / `throw` |
| 7 | ALLOC | `d[6]=[]`, `d[6][C[8]](...)` push |
| 8 | BRANCH | `d[7]=d[k]?512:425` conditional jump |
| 9 | STRING | `d[6][C[t]]=d[m]`, `new fh(...)` regex |
| 10 | ALLOC | argument prep, call-frame creation |
| 11 | STRING | `new fh("\\s",d[5])` regex match |
| 12 | STORE | `P[d[9]]=d[4][C[H]](d[3])` data handoff |
| 13 | CALL | `C[9][113]=d[9]` module init |
| 14 | STRING | `d[8]=d[9]+d[m]` string concat |
| 15 | RETURN | `return EL;` |
| 16 | ALLOC | `var r,P,Z,B...` local declarations |
| 17 | ALLOC | `(Z=[])[C[8]](69,T,445)` static array init |
| 18 | TABLE | function/type table init |
| 19 | EXCEPTION | `try{for(var RK=x;...` try-catch loop |
| 20 | DOM | `Is[d[o]]` DOM operation |
| 21 | STORE | safe global/object property fetch |
| 22 | STRING | `new fh(r,v)` string/regex handling |
| 23 | BRANCH | try-catch safe fetch + conditional jump |
| 24 | CALL | `W(C[2],null,8,z,FL)` multi-arg call |
| 25 | EXCEPTION | `try{...}catch(C){...}` catch + jump |

Opcode bit layout (observed): 5-bit opcode | 5-bit sub-opcode | operand.
Decoded in JS as `d[7]&31` (opcode), `d[7]>>5&31` (sub-opcode). Verify the
layout per sample before relying on it.

## Runtime Capture

### Option A: Selenium + CDP native events (recommended, highest success)

```python
from selenium import webdriver

driver = webdriver.Chrome()

# Inject anti-detection before any script runs
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": r"""
        Object.defineProperty(navigator, 'webdriver', {get: () => false});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN','zh','en']});
    """
})

# Send trusted CDP mouse events
driver.execute_cdp_cmd("Input.dispatchMouseEvent", {
    "type": "mousePressed",
    "x": 549.5, "y": 441.2,
    "button": "left", "buttons": 1,
    "clickCount": 1, "pointerType": "mouse"
})
```

### Option B: Playwright headless browser

```javascript
const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    // Observe API traffic while the VM runs
    await page.route('**/api/**', async route => { await route.continue_(); });

    await page.goto('https://target-page.com');

    // Wait until the DSL VM finished initializing
    await page.waitForFunction(() => {
        return window.AWSCInner &&
               window.AWSCInner._modules &&
               window.AWSCInner._modules['fy'];
    });

    // Trigger the flow that runs the bytecode
    await page.mouse.move(500, 400);
    await page.mouse.down();
    // ... interaction sequence ...
    await page.mouse.up();
    await browser.close();
})();
```

### Option C: Pure protocol replay (very low success — avoid)

DSL VM tokens are usually bound to the browser context (TLS JA3 fingerprint,
IP, cookies, request headers). Replaying the captured token outside the browser
lets the server detect the context mismatch. **Do not default to a pure
protocol approach.**

## Common Status Codes (AWSC-family)

| Code | Meaning | Handling |
|---|---|---|
| 0 | Verification passed | Extract `sessionId` + `sig` |
| 300 | Risk-control blocked | Blocked; cannot pass |
| 8778 | Verification failed, retry | Retry the operation |
| 8776 | Action too fast, retry | Add delay, then retry |
| 69634 | Generic failure | Check request parameters |

## Verification

Run this self-check before claiming the reversal is complete:

- [ ] Confirmed VM identification (IIFE + single-letter vars + `DG()`-style
      dispatcher, no `\x00asm` magic).
- [ ] Extracted the variable mapping table (`var X=<number>` literals decoded).
- [ ] Extracted and classified the full opcode list from `case N:` labels.
- [ ] Analyzed the `C[9]` constant table reference range.
- [ ] Located the exported-function registration point and traced at least one
      export to its bytecode range.
- [ ] When static analysis was insufficient, attempted runtime injection and
      recorded a state trace.
- [ ] Reproduced one real output (token, signature, or computed value) and
      compared it against a live page capture — the outputs must match.
- [ ] Documented the opcode table and VM layout in the case notes for reuse.

## When NOT to Use

- The code is ordinary obfuscated JavaScript with no interpreter — use
  `js-reverse` instead.
- The target is real WebAssembly (has `\x00asm` magic) — WASM tooling applies.
- You only need the request/response contract, not the VM semantics — protocol
  analysis is faster and sufficient.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "The switch is too long; I'll only read the opcodes I hit first." | An incomplete opcode table misreads later bytecode. Classify all `case N:` labels before concluding semantics. |
| "I beautified the JS, so the logic is now readable." | Beautifying does not decode bytecode. The logic lives in the `C[9]` table + dispatcher, not the source formatting. |
| "I'll just replay the captured token with curl." | Tokens are context-bound (JA3, IP, cookies). Server-side context mismatch detection defeats pure protocol replay. |
| "The variable names are meaningless, so I can skip mapping them." | The numeric literals bound to those variables are the indices and constants the VM needs — skipping the map guarantees misreads. |
| "One captured output is enough evidence." | A single match can be luck. Verify against at least two independent captures before claiming correctness. |
