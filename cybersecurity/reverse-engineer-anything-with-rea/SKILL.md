---
name: reverse-engineer-anything-with-rea
description: Use when reverse engineering a shipped native binary, Go or Rust executable, Android application, Electron or JavaScript package, firmware image, browser target, or other artifact where behavior must be established from the artifact or observed runtime. Routes supported investigations through REA while preserving evidence, limitations, and unknowns; skip it for ordinary source-repository analysis.
domain: cybersecurity
author: oyi77
license: Apache-2.0
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - REA
  - binaries
  - malware-analysis
  - runtime-observation
  - artifact-analysis
version: 1.0.0
category: cybersecurity
---

# Reverse Engineer Anything with REA

## Overview

REA is the artifact- and runtime-evidence workflow for questions that cannot be answered reliably from available source alone. Use it for shipped binaries and packages, decompilation, passive application runtime evidence, firmware, Android applications, Electron/JavaScript bundles, browser behavior, and version comparisons. It is an evidence collection and reasoning workflow, not a replacement for ordinary repository tools or a license to execute an untrusted target without authorization.

## When to Use

**Trigger phrases:**
- "reverse engineer this binary/package with REA"
- "what does this shipped artifact do?"
- "compare these versions"
- "decompile this application"
- "observe the application's requests without replaying them"
- "inspect this Go/Rust/Android/Electron artifact"

Use REA when the claim depends on an artifact, decompiled code, passive runtime observation, or behavior comparison that is not established by available source. Route to the more specific workflow after triage when the task is malware, ELF, Go/Rust, Android, JavaScript, or exploitation focused.

## When NOT to Use

- The complete source repository already establishes the answer; use normal search, tests, and repository tools.
- The task is ordinary implementation or architecture review rather than artifact behavior.
- You do not have authorization to inspect, execute, instrument, or collect evidence from the target.
- The request requires active exploitation, persistence, credential theft, or endpoint interaction outside an approved test environment.

## Safety and Authorization

- Work on a copy and record the artifact SHA-256 before analysis.
- Treat samples as hostile: use an isolated VM/container, least privilege, no production credentials, and controlled networking.
- Prefer static inspection and passive observation. Do not replay captured requests or execute unknown code merely to fill an evidence gap.
- State scope and approval before instrumenting a target. Redact secrets and personal data from reports.
- Separate observed behavior, tool-derived interpretation, and analyst inference; never present an inference as direct observation.

## Workflow

### Phase 1: Route and scope

1. Write the concrete question and the smallest artifact/runtime evidence needed to answer it.
2. Decide whether source analysis is sufficient. If yes, skip REA.
3. Confirm authorization, target identity, version, architecture, environment, and allowed network/runtime actions.
4. Hash and preserve the original artifact. Work from a copy and record tool versions.
5. Choose the focused path: native/package inspection, Go/Rust metadata, Android, JavaScript/Electron/browser, firmware, malware, or vulnerability analysis.

### Phase 2: Connect only when required

Use the installed REA CLI/MCP integration when available and follow its live schema/help rather than assuming a particular release. If REA is unavailable, use the approved package invocation documented by the installation; do not invent tool names or arguments. A connection failure is a blocker to the REA path, not evidence about the target.

For a native artifact, open only the required local file and retain its returned session/reference. For package, Android, JavaScript, or runtime work, use the corresponding artifact inspection or passive observation operation. Keep all analysis actions tied to a scoped question.

### Phase 3: Collect evidence

- Start with artifact identity, format, architecture, hashes, entry points, imports/exports, strings, resources, and metadata.
- For Go, inspect embedded build/module metadata before treating generic decompilation as complete. For Rust, use panic strings, crate paths, and symbol/string anchors as leads.
- For Android, inspect manifest/components/resources and then trace only the relevant code or behavior.
- For JavaScript/Electron/browser targets, capture the request/function path and observed values; do not invent browser globals or replay requests.
- For runtime questions, prefer passive observation and record environment, timing, selected scope, coverage, and exclusions.
- Read normalized tool results and preserve evidence IDs, artifact ranges, SHA-256 values, and pagination/coverage information.

### Phase 4: Reason and verify

1. Maintain a question ledger with `answered`, `partially answered`, or `unresolved` for every requested question.
2. Tie each claim to an evidence record, artifact range, observed value, or clearly labeled inference.
3. Cross-check important conclusions with an independent signal: decompilation plus strings/xrefs, metadata plus symbols, or runtime behavior plus a local reproduction.
4. Treat missing records, unsupported formats, truncated output, and bounded negative searches as unknowns—not proof of absence.
5. Re-run only the smallest necessary observation after a hypothesis changes. Do not broaden collection without a reason.

### Phase 5: Report and close

Report the target identity, scope, tools/versions, evidence references, findings, confidence, limitations, residual unknowns, and safe next steps. Mark what was observed versus inferred. Export or copy portable evidence before closing an opened native session, then close the session according to the installed REA integration. Do not claim completeness while required questions remain unresolved.

## Focused Routing

| Task | Start here |
|---|---|
| Malware behavior, C2, persistence, or unpacking | Malware-specific skill, with this workflow for artifact evidence |
| Linux ELF or native binary | `analyzing-linux-elf-malware` or `reverse-engineering-malware-with-ghidra` |
| Go or Rust executable | `go-rust-reverse` |
| Android application | `reverse-engineering-android-malware-with-jadx` or `analyzing-android-malware-with-apktool` |
| JavaScript, Electron, or browser logic | `js-reverse` or `deobfuscating-javascript-malware` |
| Memory corruption or exploitability | `binary-breaker`, only in an authorized lab |
| Source-only code understanding | Do not use REA; use repository tools |

## Evidence Record

For each meaningful operation, preserve:

```text
Question:
Target and version:
Artifact SHA-256 / runtime scope:
Operation and tool version:
Evidence ID or artifact range:
Observed result:
Interpretation:
Confidence:
Coverage and limitations:
Residual unknowns:
```

## Verification

- [ ] Authorization, isolation, target identity, and allowed actions are documented.
- [ ] Original artifact is preserved and its SHA-256 is recorded.
- [ ] REA was used only because artifact/runtime evidence was required.
- [ ] Every material claim maps to evidence or is labeled as inference.
- [ ] Unsupported, missing, truncated, and unobserved behavior remains explicitly unknown.
- [ ] Focused route and independent cross-check are documented.
- [ ] Evidence was exported before native sessions were closed.
- [ ] Final report includes scope, findings, confidence, limitations, and unresolved questions.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "The decompiler output is the truth." | Decompilation is an interpretation; preserve addresses, ranges, tool version, and corroborating evidence. |
| "No result means it is absent." | Unsupported or incomplete coverage is an unknown, not a negative finding. |
| "I can just run the sample." | Execution requires authorization, isolation, least privilege, and a question that static evidence cannot answer. |
| "The request capture can be replayed." | REA observation is passive; replay changes behavior and can affect real systems. |
| "I will report the whole application." | Scope the question and disclose coverage; bounded analysis is stronger than an unsupported completeness claim. |
