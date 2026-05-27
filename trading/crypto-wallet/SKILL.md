---
name: crypto-wallet
description: Crypto wallet development — HD wallets, key management, transaction signing, multi-chain, WalletConnect
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

## Pseudo Code

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
