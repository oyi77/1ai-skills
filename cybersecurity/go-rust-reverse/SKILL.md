---
name: go-rust-reverse
description: 'Use when reverse engineer Go and Rust binaries: recognize the language
  runtime from go.buildid, runtime symbols, or panic strings, recover function tables
  and names from pclntab, and rebuild symbols with GoReSym or redress before Ghidra/IDA
  analysis. Use when analyzing stripped Go/Rust malware, ELF/PE binaries with non-standard
  symbol layouts, or runtime-library-heavy samples.'
domain: cybersecurity
subdomain: malware-analysis
tags:
- go
- rust
- reverse-engineering
- malware-analysis
- pclntab
- ghidra
- ida
- symbol-recovery
version: '1.0'
author: oyi77
license: Apache-2.0
nist_csf:
- DE.AE-02
- RS.AN-03
- ID.RA-01
category: cybersecurity
---


# Go / Rust Binary Reverse Engineering

## Overview

Go and Rust binaries break generic reverse-engineering assumptions. They are
statically linked, carry their own runtimes, and when stripped they leave
massive symbol tables behind (Go's pclntab, Rust's panic strings) that
generic disassemblers ignore. The language-specific shortcut is: recognize
the runtime, recover the metadata, then read the business logic — never wade
through runtime library code.

This skill covers runtime recognition, pclntab/function-name recovery with
GoReSym/redress, and idiomatic decompilation recovery for both languages,
plus a dynamic-analysis note for Go's unusual stack/scheduler behavior. It
complements (does not replace) the generic Ghidra/IDA workflow in
`analyzing-go-golang-with-ghidra` and similar skills.

Source: cherry-picked and translated from `zhaoxuya520/reverse-skill`
(`skills/go-rust-reverse`, MIT license); reference notes
(`go-rust-notes.md`) inlined.

## When to Use

**Trigger phrases:**
- "reverse this stripped Go binary"
- "recover function names from pclntab"
- "analyze Rust malware"
- "GoReSym on this ELF"
- "language-specific RE of a Go/Rust sample"
- "find the main entry of a Go binary"

Use this skill when:

- The sample is a Go or Rust compiled artifact (confirmed via `file`, string
  inspection, or runtime fingerprints).
- Symbols are stripped and you need function names or the `main` entry back.
- You want to skip runtime-library noise and go straight to business logic.

## Prerequisites

- `file`, `strings`/`rabin2` for triage.
- GoReSym (and/or redress, or a Go-aware IDA plugin) for Go metadata.
- Ghidra or IDA with Go/Rust plugins for decompilation; radare2 for quick
  string work.

## Workflow

### Phase 1: Triage — Identify the Runtime

- Confirm the language before anything else: `go.buildid` section,
  `runtime.` symbol residue, `main.main` references, or Rust `panic`
  strings / `rust_begin_unwind`.
- Record the language-runtime evidence explicitly — it drives every later
  step.

### Phase 2: Go — Recover Metadata

- Go: locate `go.buildid`, residual `runtime` symbols, and the pclntab
  (program counter line table).
- Run GoReSym / redress / an IDA Go plugin to restore function names from
  pclntab.
- Anchor on `runtime.main` and `main.main` first, then work outward.
- Decompilation notes: recognize how `interface`, `slice`, and `string`
  values render in the decompiler; follow `crypto/*` and `net/http` import
  paths to locate network or encryption logic.

### Phase 3: Rust — String-Drive the Analysis

- Rust: collect `src/` path strings, crate-path hints, and panic strings
  first — they are the best roadmap in a stripped Rust binary.
- Watch for generics instantiation bloat; locate string xrefs to jump from
  user-visible text to the code that renders it.
- Async/tokio state machines need cross-referencing of the state enum and
  poll loop — do not try to read them linearly.
- Look for `Option`/`Result` handling blocks as behavioral landmarks.

### Phase 4: Dynamic (Optional)

- Frida still works; account for Go's goroutine stacks and scheduler — break
  on log/config strings first rather than arbitrary addresses.
- Log- and configuration-string-driven breakpoints give the fastest
  orientation in both languages.

### Phase 5: Business Logic

- With names (Go) or string anchors (Rust) recovered, read the business
  logic: C2, persistence, exfiltration, or protocol handling.
- Record which function names are recovered vs inferred (equivalent mapping
  is an acceptable fallback when pclntab recovery is partial).

## Hands-On Example

Triage a stripped Go binary and confirm its runtime before metadata recovery
(Phase 1 — Triage). Ensure the toolchain exists with `apt install golang-go`
(Debian/Kali; go 1.24 verified here), then list symbols directly:

```bash
go tool nm ./sample | grep -E ' main\.main| runtime\.main'
# a35100 T main.main
# a361c0 T main.main.CountFlags.CountFlags.func1
```

`go tool nm` (output above verified against a real Go binary) gives an
instant stripped-vs-not read: a symbol-rich result means the binary was NOT
stripped and Go-aware tooling can recover full metadata without pclntab
parsing. Pair it with `file ./sample` for the runtime fingerprint.

## Verification

Run this self-check before claiming completion:

- [ ] Language runtime evidence is documented (go.buildid / runtime symbols /
      panic strings / crate paths).
- [ ] `runtime.main`/`main.main` (Go) or the primary string anchors (Rust)
      are located.
- [ ] Function names are recovered via GoReSym/redress, or an equivalent
      mapping is explicitly labeled as inferred.
- [ ] Network/encryption paths (`crypto/*`, `net/http`, TLS usage) are
      identified.
- [ ] The recovered business logic (C2, persistence, exfil, protocol) is
      cross-referenced to the decompiled evidence.

## When NOT to Use

- C/C++ binaries with normal symbols — generic RE is faster.
- Go binaries already handled by a dedicated Go workflow — use this skill as
  the additive pclntab/GoReSym layer, not a duplicate.
- Malware-family Go/Rust samples with a single-toolchain playbook — start
  from `reverse-engineering-rust-malware` (Rust malware, IDA/Ghidra +
  sandbox/IOCs) or `analyzing-golang-malware-with-ghidra` (Go + Ghidra
  scripts); this skill is the toolchain-agnostic, non-malware path.
- Fully dynamic-only tasks where no static recovery adds value.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just open it in Ghidra." | A stripped Go/Rust binary without pclntab recovery is a wall of runtime noise; you will burn hours in `runtime.*`. Recover metadata first. |
| "The Go toolchain names are useless anyway." | `main.main`, `crypto/*`, `net/http` and the pclntab function table are exactly the roadmap you need. |
| "I'll read the whole binary." | String-driven (Rust) and anchor-driven (Go) analysis covers the business logic with a fraction of the surface. |
| "Panic strings are just noise." | In stripped Rust binaries, panic strings and `src/` paths are frequently the only surviving source map. |
| "Dynamic analysis is the same as C." | Go's goroutine stacks and scheduler break naive Frida assumptions; break on strings, not addresses. |