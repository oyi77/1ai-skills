---
name: crypto-wallet
description: Crypto wallet development — HD wallets, key management, transaction signing, multi-chain, WalletConnect

## Red Flags

- Private keys stored in plaintext or logged to console output
- No mnemonic backup recovery flow implemented
- Gas estimation missing for transaction signing
- WalletConnect session not properly disconnected on app close
- Nonce management collisions causing stuck transactions
- Hardware wallet integration bypassing user confirmation prompts

## Verification

After completing wallet implementation, confirm:

- [ ] HD wallet derivation produces correct addresses for m/44'/60'/0'/0/0 path
- [ ] Transaction signing handles EIP-1559 gas parameters correctly
- [ ] Multi-chain support tested on at least 2 EVM networks
- [ ] WalletConnect v2 session lifecycle managed (connect, disconnect, restore)
- [ ] Private keys never logged or stored in plaintext
- [ ] Gas estimation returns reasonable values before transaction broadcast


## Red Flags

- Private keys stored in plaintext or logged to console output
- No mnemonic backup recovery flow implemented
- Gas estimation missing for transaction signing
- WalletConnect session not properly disconnected on app close
- Nonce management collisions causing stuck transactions

## Verification

After completing wallet implementation, confirm:

- [ ] HD wallet derivation produces correct addresses for m/44'/60'/0'/0/0 path
- [ ] Transaction signing handles EIP-1559 gas parameters correctly
- [ ] Multi-chain support tested on at least 2 EVM networks
- [ ] Private keys never logged or stored in plaintext
- [ ] Gas estimation returns reasonable values before transaction broadcast

---

## Overview

Crypto wallet development covering HD wallet derivation (BIP-32/39/44), transaction signing, EIP-1559 gas, multi-chain support, and WalletConnect v2 integration.

## Capabilities

- HD wallet derivation (BIP-32/39/44)
- Transaction signing (EIP-1559)
- Multi-chain support (EVM chains)
- WalletConnect v2 integration
- Hardware wallet integration
- Gas estimation

## When to Use

- Building wallet apps
- Multi-chain portfolio managers
- DeFi dashboard integrations
- Hardware wallet support

## When NOT to Use

- Task is about portfolio management, not trading (use portfolio skills)
- Task is about financial analysis (use analysis skills)
- You need to analyze trade results (use analytics skills)
- Task is about risk management (use risk skills)
- You don't have trading capital
- Task requires financial advice (consult advisors)


## Pseudo Code

Reference implementations for HD wallet derivation, transaction signing, and multi-chain integration.


### HD Wallet (ethers.js)
```javascript
const { ethers } = require("ethers");
const mnemonic = ethers.Wallet.createRandom().mnemonic.phrase;
const child = ethers.HDNodeWallet.fromMnemonic(mnemonic, "m/44'/60'/0'/0/0");
console.log(child.address, child.privateKey);
```

### Transaction Signing
```javascript
const tx = await wallet.sendTransaction({
  to: "0xRecipient",
  value: ethers.parseEther("0.1"),
  maxFeePerGas: ethers.parseGwei("20"),
  maxPriorityFeePerGas: ethers.parseGwei("2"),
});
await tx.wait();
```

## Common Patterns

- BIP-39 mnemonic (12/24 words)
- BIP-44 path: m/44'/60'/0'/0/0 (Ethereum)
- Nonce management for sequential txs
- EIP-1559: maxFeePerGas, maxPriorityFeePerGas

## Red Flags

- Private keys stored in plaintext or logged to console output
- No mnemonic backup recovery flow implemented
- Gas estimation missing for transaction signing
- WalletConnect session not properly disconnected on app close
- Nonce management collisions causing stuck transactions

## Verification

After completing wallet implementation, confirm:

- [ ] HD wallet derivation produces correct addresses for m/44'/60'/0'/0/0 path
- [ ] Transaction signing handles EIP-1559 gas parameters correctly
- [ ] Multi-chain support tested on at least 2 EVM networks
- [ ] Private keys never logged or stored in plaintext
- [ ] Gas estimation returns reasonable values before transaction broadcast
