---
name: browser-extension-reverse
description: >-
  Reverse engineer browser extensions: unpack CRX/XPIs or load unpacked
  directories, audit manifest permissions for overreach, trace content and
  background script data flows, extract API endpoints and storage keys, and
  detect malicious or data-exfiltrating behavior. Use when analyzing extension
  security posture, suspicious extensions, or extension-based attack chains.
domain: cybersecurity
subdomain: web-application-security
tags:
  - browser-extension
  - reverse-engineering
  - malware-analysis
  - manifest
  - chrome
  - firefox
  - supply-chain
version: '1.0'
author: oyi77
license: Apache-2.0
nist_csf:
  - DE.AE-02
  - RS.AN-03
  - ID.RA-01
  - DE.CM-01
---

# Browser Extension Reverse Engineering

## Overview

Browser extensions (Chrome/Edge MV2/MV3, Firefox) run with privileges a web
page does not have: cross-origin requests, webRequest interception, storage
access, and native messaging. That elevated trust makes them a high-value
target for both attackers (malicious extensions, supply-chain poisoning of
popular extensions) and defenders (credential or traffic logic recovery).

This skill covers the full extension analysis workflow: package acquisition,
manifest permission audit, content/background script tracing, dynamic
loading in developer mode, and the data-flow reconstruction that ties it
together. Complex obfuscated inner logic routes into the general JavaScript
workflow (`js-reverse`); poisoning investigations route into supply-chain
and malware analysis.

Source: cherry-picked and translated from `zhaoxuya520/reverse-skill`
(`skills/browser-extension-reverse`, MIT license); reference notes
(`extension-analysis.md`) inlined.

## When to Use

**Trigger phrases:**
- "analyze this browser extension"
- "is this extension malicious"
- "what does this extension do with my data"
- "unpack a crx and trace its logic"
- "extension supply-chain investigation"
- "recover an extension's signing or proxy logic"

Use this skill when:

- The target is a browser extension (crx/xpi/unpacked directory), not a
  plain web page — plain page JS routes to `js-reverse`.
- You must assess an extension's permission surface, extract its endpoints,
  or determine whether it exfiltrates data.

## Prerequisites

- Chrome/Edge (MV2/MV3) or Firefox.
- An archive tool (unzip/7z) or `jq` for manifest parsing.
- Chrome DevTools for worker debugging; YARA for malicious-extension rules.

## Workflow

### Phase 1: Package

- Acquire the package: unpack the CRX/XPI archive, or copy the extension
  directory out of the browser profile.
- Read `manifest.json`: `permissions`, `host_permissions`,
  `background`/`service_worker`, `content_scripts`.
- Assess overreach before reading a single script (risk signals table
  below).

### Phase 2: Logic

- Locate the `service_worker` / `background` entry point and the
  `content_script` injection points and their worlds (isolated vs main).
- Hunt for keys: `chrome.storage`, IndexedDB, `localStorage`, and any
  encrypted configuration blobs.
- Observe network and message-passing flows (`runtime.sendMessage` /
  `chrome.runtime.onMessage`) exactly as in `js-reverse`: watch what the
  extension sends, when, and to where.

### Phase 3: Dynamic

- Load the unpacked directory via developer mode; check
  `chrome://extensions` for errors.
- Attach DevTools to the service worker.
- If the logic resists static reading, use Frida or a CDP-level hook to
  instrument the worker at runtime.

### Phase 4: Data Flow Reconstruction

- Trace each sensitive input (page DOM data, storage keys, webRequest
  bodies) to its sink (network call, native messaging port, storage write).
- Reconstruct the full flow: trigger → handler → transform → exfiltration or
  legitimate use.

## Manifest Risk Signals

| Field | Risk signal |
|---|---|
| `host_permissions` `<all_urls>` | Can read/write any site |
| `webRequestBlocking` | Man-in-the-middle style rewriting of traffic |
| `nativeMessaging` | Escapes the browser to the host machine |
| `externally_connectable` | Web pages can drive the extension |

MV3 specifics: audit the `service_worker` lifecycle and
`declarativeNetRequest` rules — static/dynamic rules are a common covert
traffic-modification surface.

## Verification

Run this self-check before claiming completion:

- [ ] The permission surface and entry scripts are listed in the report.
- [ ] The extension's data flow (input → transform → sink) is reconstructed
      with observed evidence for each hop.
- [ ] API endpoints and storage keys used by the extension are extracted.
- [ ] Every risk signal from the manifest table is either confirmed or
      explicitly ruled out with evidence.
- [ ] If a verdict (benign / malicious / suspicious) is given, it cites the
      artifacts that support it.

## When NOT to Use

- Plain web-page JavaScript — route to `js-reverse`.
- Server-side logic — protocol analysis is the right tool.
- A full malware-family deep dive — hand the samples to malware analysis.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "The manifest looks minimal, so it's safe." | Minimal permissions can still be abused; content scripts and DNR rules are invisible in the permission list. Read the code. |
| "I'll just read the background script." | The interesting flow usually lives across content script → messages → worker → network. Trace the whole path. |
| "Dynamic analysis is unnecessary." | Static reading misses runtime-injected URLs, dynamically constructed endpoints, and obfuscated handlers. Load it in developer mode. |
| "It's from the official store, so it's clean." | Store review has been bypassed repeatedly; supply-chain attacks land in stores. Treat the package as untrusted input. |