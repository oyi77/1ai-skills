---
name: gate-dex-wallet
description: "Use when managing Gate DEX wallets or signing EVM/GateChain transactions. Triggers on address/balance checks on-chain, EVM/EIP-3009 gasless x402 resource payments, DApp connection requests, and wallet-cli operations."
domain: trading
author: oyi77
license: Apache-2.0
subdomain: trading
tags:
  - gate
  - dex
  - wallet
  - payment
  - on-chain
version: 1.0.0
category: trading
---

## Overview

Gate DEX Wallet covers decentralized wallet operations for GateChain, EVM networks (Ethereum, Base, BSC), and Solana. It outlines multi-chain wallet management, transaction signing, WalletConnect integrations, and EIP-3009 gasless transaction execution for x402 resource retrieval.

## When to Use

**Trigger phrases:**
- "gate-dex-wallet", "show my Gate DEX address"
- "gasless x402 payment base", "sign EVM transaction"
- "connect dApp with gate-wallet", "on-chain audit balance"

**Situations:**
- Interacting with DApps, approving tokens, and signing off-chain EIP-712 structured data via wallet providers.
- Direct CLI-based transaction dispatching using `gate-wallet-cli` or similar tools.
- Automating HTTP 402 payment loops using gasless EIP-3009 signature schemas.

## When NOT to Use

- Task belongs to centralized Gate.io exchange operations (use `gate-exchange-trading`).
- Task only checks market prices or token listings without wallet connectivity (use `polymarket` or standard token checkers).
- Bypassing transaction verification or signing messages containing unvetted destination payloads.

## Operational Workflow

### Step 1: Initialize Wallet/Connection
Obtain account lists and chain configuration:
```javascript
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const account = privateKeyToAccount(process.env.WALLET_PRIVATE_KEY);
const client = createWalletClient({ account, chain: base, transport: http() });
```

### Step 2: Sign and Execute Transactions
Before broadcasting arbitrary payloads, run strict check-ins with Gate Verify.
```bash
gate-wallet-cli transfer --to 0xRecipientAddress --amount 0.01 --chain base
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll copy the raw private key into my application files" | Exposed keys lead to instant wallet drain. Use OS keychain or load encrypted private keys via env variables. |
| "I don't need to verify txBundle details before signing" | Unverified transaction bundles can execute malicious smart contract calls. Verify destination first. |
| "A fallback RPC is unnecessary for simple balance reads" | Primary RPC nodes can go down. Implement fallback arrays to prevent balance reading failure. |

## Verification

### Verification Checklist
- [ ] Wallet client initialization resolves to correct EIP-55 address format
- [ ] EVM chain ID registry routes to correct RPC network endpoint
- [ ] Check-in tokens sign EIP-712 typed structured data successfully
- [ ] CLI command `gate-wallet-cli --version` operates on local PATH

## Process

1. **Verify wallet credentials** - ensure PRIVATE_KEY/mnemonic is securely retrieved.
2. **Execute connection probe** - confirm RPC liveness and get current block number.
3. **Draft tx payload** - estimate gas limits and verify destination addresses.
4. **Trigger validation checkin** - verify against the Gate Verify server.
5. **Sign and broadcast** - dispatch transaction, await receipt, and return txHash.
