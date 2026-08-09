---
name: js-reverse
description: >-
  Front-end JavaScript reverse engineering for web apps and anti-bot engines:
  observe request flows, capture logic via hooks or breakpoints, rebuild in a
  local Node environment, apply minimal patches, and decode obfuscated signing
  algorithms. Use when analyzing request signing chains, obfuscated SDKs, or
  client-side protection logic.
domain: cybersecurity
subdomain: web-application-security
tags:
  - javascript
  - reverse-engineering
  - deobfuscation
  - anti-bot
  - web-application-security
  - devtools
  - signing-algorithm
version: '1.0'
author: oyi77
license: Apache-2.0
nist_csf:
  - DE.AE-02
  - RS.AN-03
  - ID.RA-01
---

# Front-End JavaScript Reverse Engineering

## Overview

Modern web applications move security logic (request signing, anti-bot
tokens, risk scoring) into the browser. Reversing that logic is a discipline
with its own order of operations: observing traffic first, capturing the
relevant code path, rebuilding the logic in a controlled local environment,
and only then patching or decoding. Jumping straight to breakpoints or
deobfuscation is how reversers burn hours on the wrong code.

This skill provides a five-phase workflow — Observe → Capture → Rebuild →
Patch → Decode — plus the execution discipline (evidence-first, artifact
per task, minimal patches) that keeps the process reproducible. It is
tool-agnostic: the same workflow runs on Chrome DevTools, Playwright,
puppeteer, or any CDP-capable driver, and on any runtime rebuilt in Node.js.

Source: cherry-picked and translated from `zhaoxuya520/reverse-skill`
(`skills/js-reverse`, MIT license). MCP-specific tool bindings were
generalized to standard browser/CDP tooling.

## When to Use

**Trigger phrases:**
- "reverse the signing logic of this request"
- "how is this frontend token generated"
- "analyze obfuscated JS behavior"
- "rebuild a client-side algorithm in Node"
- "patch a JS function to verify a hypothesis"
- "deobfuscate control flow of a web SDK"

Use this skill when:

- A request carries a signature, token, or header you must reproduce or
  understand (for security review, testing, or interoperability).
- Obfuscated or minified client code hides the algorithm.
- You need to confirm behavior before writing a rewrite (verify the real
  runtime, never assume from source shape).

## Prerequisites

- Chrome (or Chromium) with DevTools; Playwright/puppeteer if scripting.
- Node.js 18+ for local rebuilds.
- A beautifier (prettier or js-beautify) and a proficient code editor.

## Workflow

### Phase 1: Observe

- Open DevTools → Network, filter by the target request type; identify the
  target request URL.
- Open the initiator chain / call stack of that request to find the entry
  function.
- Locate the script that issues the request: find the JS file URL, then the
  function name and approximate line in the Sources panel.
- Take notes on the request header names you must reproduce and their current
  values.

### Phase 2: Capture

- **Break-on-XHR first**: enable XHR breakpoints on the target URL so the
  stack lands at the exact call site — the most direct capture point.
- Use light runtime observation: console-log the arguments each step of the
  chain receives, not the whole call graph.
- Capture: the function name, the values in scope at the call site,
  and when the computed value is added to the request.

### Phase 3: Rebuild

- Rebuild the captured call chain as a local Node.js script.
- Evidence-based only: never invent `window`, `document`, `crypto`, or
  `localStorage` behavior — introduce browser globals you actually saw being
  read (via the DevTools console or a strace of properties accessed).
- If the code needs a browser environment, run Playwright and evaluate the
  rebuilt logic inside the page context for parity.
- Structure the script so each step prints its output: this exposes the first
  divergence immediately.

### Phase 4: Patch

- Apply **one minimal patch per failure**: on the first error or first
  divergence, patch the smallest thing that resolves it, retest, log.
- Never mass-edit the target logic before it runs locally.
- Patches are for verification (fix an undefined var, seed a needed value),
  not for finishing a half-rebuild.

### Phase 5: Decode / DeepDive

- Only after the rebuild runs end-to-end does deobfuscation make sense:
  beautify the captured scope of the algorithm and restore control flow
  (switch dispatch → if/else) guided by the observed behavior.
- Extract the business logic: key derivation, signing steps, or token field
  semantics.
- **Downgradeable**: if the task only needs the signing result (not long-term
  reuse of the algorithm chain), phase 5 can stop at "locally reproduced the
  value" without full control-flow recovery.

## Execution Rules

- Every task produces artifacts — the script, the capture log, the patch
  list. A task with no artifacts is not done.
- Final state per artifact: the runnable rebuilt script with the minimal
  patches and a list of every divergence observed and its resolution.
- No unexplained tool calls: every automation action must map to a step in
  this workflow.
- Fallbacks: when a capability has no implementation (e.g. deserializer
  missing), fall back to the documented generic mechanism instead of
  stopping.
- Evidence-first: any claim about what the code does requires a recorded
  run or a captured value.

## Verification

Run this self-check before claiming completion:

- [ ] Target request URL and initiator chain are documented.
- [ ] Break-on-XHR or equivalent capture produced the full function chain
      with observed values.
- [ ] The rebuilt Node/Playwright script reproduces the target value without
      invented browser behavior.
- [ ] Each patch is minimal, logged, and justified (one error → one patch).
- [ ] The final value is compared live against a real page capture and
      matches.
- [ ] If the task needed control-flow recovery: the deobfuscated version
      recompiles/reruns and produces the same output.

## When NOT to Use

- The logic is server-side only (no browser involvement) — protocol analysis
  is the right tool.
- The target is real WebAssembly — use WASM tooling and `dsl-vm-reverse` for
  JS VM targets separately.
- You only need to call the endpoint, not reproduce its algorithm — a
  recorded replay may be sufficient, though context-bound tokens will break.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll go straight to the deobfuscator." | Deobfuscating before you have a local, running rebuild tells you nothing about what to look at. Rebuild first. |
| "I'll read the whole obfuscated file before patching." | You only need the captured execution path. Mass-reading is slower and wrong-reasoning fodder. |
| "I invented a window object to make it run." | Invented environment masks the real divergence and can produce a value that only appears right. |
| "The value looks plausible, so it's correct." | Middle values are invisible; only a compared output proves correctness. |
| "One patch fixed everything." | One error, one patch — a giant patch hides multiple divergences you will not understand later. |