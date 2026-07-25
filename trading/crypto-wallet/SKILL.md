---
name: crypto-wallet
description: 'Skill: crypto-wallet. See SKILL.md body for details. Use when this domain is relevant.'
domain: trading
tags:
- algorithms
- crypto
- markets
- trading
- wallet
---

## Overview

Crypto wallet engineering spans key derivation, transaction construction, signing, and multi-chain broadcasting. This skill covers production-grade wallet implementation using HD derivation (BIP-32/39/44), EIP-1559 transaction building, WalletConnect v2 integration, hardware wallet support, and cross-chain RPC management.

## Core Concepts

A non-custodial wallet generates and stores private keys client-side. Three wallet tiers:

| Tier | Example | Key Storage | Use Case |
|------|---------|-------------|----------|
| Hot wallet | Browser extension, mobile app | Encrypted keystore / OS keychain | Daily trading, DeFi interactions |
| Warm wallet | Hardware wallet (Ledger/Trezor) | Secure element, never exposed | Medium-value holdings, frequent use |
| Cold wallet | Air-gapped machine, paper wallet | Offline, manual signing | Long-term storage, large holdings |

## When to Use

**Trigger phrases:**
- "crypto wallet", "Generate wallet from mnemonic"
- "Sign transaction / sign message", "WalletConnect integration"
- "Hardware wallet support", "Multi-chain portfolio manager"
- "DeFi dashboard integration"

**Situations:**
- Building a non-custodial wallet UI (browser extension, mobile, desktop)
- Integrating wallet connection into a dApp (RainbowKit, Web3Modal, ConnectKit)
- Implementing backend transaction broadcasting or fee estimation
- Supporting EIP-712 typed data signing for gasless permits or off-chain orders

## When NOT to Use

- Task is about portfolio management analytics (use portfolio-manager)
- Task is about trading strategy execution (use trading-strategist)
- Task is about DeFi protocol analysis (use defi-protocols)
- You need regulatory compliance or custody infrastructure — custodial wallet management requires separate security patterns
- You only need read-only balances or transaction history without signing (use block explorer APIs instead)

## HD Wallet Derivation (BIP-32 / BIP-39 / BIP-44)

### BIP-39: Mnemonic Generation

A mnemonic encodes 128-256 bits of entropy into 12-24 words from a 2048-word list. Each word represents 11 bits plus a 4-8 bit checksum.

```javascript
// ethers.js v6
import { entropyToMnemonic, mnemonicToEntropy, HDNodeWallet, randomBytes } from "ethers";

const entropy = randomBytes(16); // 128 bits → 12 words
const mnemonic = entropyToMnemonic(entropy);
console.log("Mnemonic:", mnemonic);

// Validate
const recovered = mnemonicToEntropy(mnemonic);
console.assert(recovered === entropy);
```

```python
# web3.py
from eth_account import Account
import os

entropy = os.urandom(16)
account = Account.create_with_mnemonic(extra_entropy=entropy)
mnemonic = account[0]

# Validate
from eth_account.mnemonic import Mnemonic
assert Mnemonic("english").check(mnemonic)
```

| Entropy (bits) | Checksum (bits) | Words |
|---------------|----------------|-------|
| 128 | 4 | 12 |
| 192 | 6 | 18 |
| 256 | 8 | 24 |

**Passphrase support**: An optional passphrase ("25th word") produces a completely different wallet from the same mnemonic.

```javascript
// Different passphrase = different wallet
const walletNoPass = HDNodeWallet.fromMnemonic(
  HDNodeWallet.mnemonicFrom(mnemonic), "m/44'/60'/0'/0/0"
);
const walletWithPass = HDNodeWallet.fromMnemonic(
  HDNodeWallet.mnemonicFrom(mnemonic, "my-passphrase"), "m/44'/60'/0'/0/0"
);
// walletNoPass.address !== walletWithPass.address
```

### BIP-32: Hierarchical Deterministic Derivation

A single master seed derives an unlimited tree of keypairs. Hardened paths (apostrophe `'`) require parent private key; non-hardened paths can derive children from extended public key (xpub).

```javascript
// ethers.js v6 — derive addresses at any depth
const mnemonic = HDNodeWallet.createRandom().mnemonic;
const derive = (path) => HDNodeWallet.fromMnemonic(mnemonic, path);
const path = "m/44'/60'/0'/0/0";  // Ethereum first address
const wallet = derive(path);
console.log("Address:", wallet.address);

// Iterate addresses
for (let i = 0; i < 5; i++) {
  console.log(`Address ${i}:`, derive(`m/44'/60'/0'/0/${i}`).address);
}
```

```rust
// ethers-rs
use ethers::signers::{MnemonicBuilder, coins_bip39::English};
let wallet = MnemonicBuilder::<English>::default()
    .phrase(phrase)
    .derivation_path("m/44'/60'/0'/0/0")?
    .build()?;
println!("{:?}", wallet.address());
```

### BIP-44: Multi-Account Hierarchy

Standardized path: `m / purpose' / coin_type' / account' / change / address_index`

| Coin | coin_type' | Path Example |
|------|-----------|-------------|
| Bitcoin | 0' | m/44'/0'/0'/0/0 |
| Ethereum | 60' | m/44'/60'/0'/0/0 |
| Solana | 501' | m/44'/501'/0'/0' |
| Binance Chain | 714' | m/44'/714'/0'/0/0 |
| Cosmos | 118' | m/44'/118'/0'/0/0 |
| Polkadot | 354' | m/44'/354'/0'/0/0 |
| Litecoin | 2' | m/44'/2'/0'/0/0 |

## Address Derivation

### Ethereum (EIP-55 Checksummed)

Derivation: `keccak256(publicKey)` last 20 bytes, with mixed-case checksum.

```javascript
import { Wallet, getAddress } from "ethers";
const wallet = new Wallet(privateKey);
console.log("Address:", wallet.address); // EIP-55 checksummed

// Validate
console.assert(getAddress(rawAddr) === rawAddr); // throws if invalid checksum
```

### Bitcoin Addresses (P2PKH, P2SH, Bech32)

```javascript
import * as bitcoin from "bitcoinjs-lib";
import { BIP32Factory } from "bip32";
import * as ecc from "tiny-secp256k1";

const bip32 = BIP32Factory(ecc);
const seed = bip32.fromSeed(Buffer.from(mnemonicToSeed(mnemonic), "hex"));

// P2PKH (legacy, starts with 1)
const p2pkh = bitcoin.payments.p2pkh({
  pubkey: seed.derivePath("m/44'/0'/0'/0/0").publicKey,
  network: bitcoin.networks.bitcoin,
});
// P2SH-P2WPKH (nested SegWit, starts with 3)
const p2sh = bitcoin.payments.p2sh({
  redeem: bitcoin.payments.p2wpkh({
    pubkey: seed.derivePath("m/49'/0'/0'/0/0").publicKey,
    network: bitcoin.networks.bitcoin,
  }),
});
// Bech32 (native SegWit, starts with bc1)
const bech32 = bitcoin.payments.p2wpkh({
  pubkey: seed.derivePath("m/84'/0'/0'/0/0").publicKey,
  network: bitcoin.networks.bitcoin,
});
```

### EVM Chains

All EVM chains use the same address format — `keccak256(pubkey)[12..32]` with EIP-55. One address works on Polygon, Arbitrum, Optimism, BSC, Avalanche, Base, and every EVM L2.

```javascript
import { isAddress } from "viem";
if (!isAddress(input)) throw new Error("Invalid address");
```

## Transaction Building

### EIP-1559 (Type 2)

Post-London fork. Uses base fee (burned) + priority fee (tip to validator).

```javascript
// ethers.js v6
const tx = await wallet.sendTransaction({
  to: "0xRecipient",
  value: ethers.parseEther("0.1"),
  maxFeePerGas: ethers.parseGwei("50"),
  maxPriorityFeePerGas: ethers.parseGwei("2"),
  gasLimit: 21000n,
  chainId: 1,
  nonce: await wallet.getNonce(),
  type: 2,
});
await tx.wait();
```

```typescript
// viem
import { createWalletClient, http, parseEther, parseGwei } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet } from "viem/chains";

const account = privateKeyToAccount("0x...");
const client = createWalletClient({ account, chain: mainnet, transport: http() });
const hash = await client.sendTransaction({
  to: "0xRecipient", value: parseEther("0.1"),
  maxFeePerGas: parseGwei("50"), maxPriorityFeePerGas: parseGwei("2"),
});
await client.waitForTransactionReceipt({ hash });
```

```python
# web3.py
from web3 import Web3
w3 = Web3(Web3.HTTPProvider("https://eth-mainnet.g.alchemy.com/v2/KEY"))
signed = account.sign_transaction({
    "to": "0xRecipient", "value": w3.to_wei(0.1, "ether"),
    "gas": 21000, "chainId": 1,
    "maxFeePerGas": w3.to_wei(50, "gwei"),
    "maxPriorityFeePerGas": w3.to_wei(2, "gwei"),
    "nonce": w3.eth.get_transaction_count(account.address),
})
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
```

### Legacy (Type 0) — Pre-EIP-1559

```javascript
const tx = await wallet.sendTransaction({
  to: "0xRecipient", value: ethers.parseEther("0.1"),
  gasPrice: ethers.parseGwei("10"),
  gasLimit: 21000n, chainId: 1, nonce: nonce, type: 0,
});
```

### EIP-2930 (Type 1) — Access Lists

Pre-declare contract storage slots to reduce gas costs in multi-contract interactions.

```javascript
const tx = {
  to: "0xContract", data: "0x...",
  accessList: [{
    address: "0xContractAddress",
    storageKeys: ["0x00...01", "0x00...02"],
  }],
  maxFeePerGas: ethers.parseGwei("50"),
  maxPriorityFeePerGas: ethers.parseGwei("2"),
  chainId: 1, type: 1,
};
```

### EIP-4844 (Type 3) — Blob Transactions

Used for L2 data availability. Requires blob-carrying transaction support.

```typescript
// viem
const txHash = await walletClient.sendTransaction({
  blobs: toBlobSidecar({ data: "0x..." }).blobs,
  maxFeePerBlobGas: parseGwei("1"),
  account: wallet.account, chain: mainnet,
});
```

## Signing

### ECDSA (secp256k1)

Every private key is a random 256-bit scalar on secp256k1.

```javascript
const wallet = new Wallet(privateKey);
const sig = await wallet.signMessage("Hello");
// 0x... (65 bytes: r,s,v)
```

### personal_sign

Prepends `\x19Ethereum Signed Message:\n<len>` before hashing.

```typescript
// viem — verify
import { verifyMessage } from "viem";
const valid = await verifyMessage({
  address: userAddress, message: "Login to ExampleApp", signature: sig,
});
```

### EIP-712 (Typed Structured Data)

Used for gasless permits, Uniswap orders, ERC-2612, and typed auth.

```javascript
// ethers.js v6
const domain = { name: "Uniswap V2", version: "1", chainId: 1, verifyingContract: "0x..." };
const types = {
  Permit: [
    { name: "owner", type: "address" },
    { name: "spender", type: "address" },
    { name: "value", type: "uint256" },
    { name: "nonce", type: "uint256" },
    { name: "deadline", type: "uint256" },
  ],
};
const value = { owner: "0xOwner", spender: "0xSpender", value: ethers.parseUnits("1000", 18) };
const sig = await wallet.signTypedData(domain, types, value);
```

```python
# web3.py
from eth_account.messages import encode_typed_data
encoded = encode_typed_data(domain, types, value)
signed = account.sign_message(encoded)
```

### ERC-1271 (Contract Signature Validation)

Smart contract wallets need on-chain validation for off-chain signatures.

```solidity
function verify(address signer, bytes32 hash, bytes calldata sig) internal view returns (bool) {
    if (signer.code.length > 0) {
        try IERC1271(signer).isValidSignature(hash, sig) returns (bytes4 result) {
            return result == 0x1626ba7e;
        } catch { return false; }
    } else {
        return ecrecover(hash, ...) == signer;
    }
}
```

## WalletConnect v2

Symmetric key exchange over a relay network for chain-agnostic, session-based communication.

```javascript
// Wallet-side (in-webapp wallet, @walletconnect/web3wallet)
import { Web3Wallet } from "@walletconnect/web3wallet";

const web3wallet = await Web3Wallet.init({
  projectId: "YOUR_PROJECT_ID",
  metadata: { name: "MyWallet", description: "...", url: "...", icons: ["..."] },
});

// Handle session proposals
web3wallet.on("session_proposal", async (proposal) => {
  const { id, params } = proposal;
  // Approve with namespace-scoped methods
  await web3wallet.approveSession({
    id,
    namespaces: {
      eip155: {
        accounts: [`eip155:1:${address}`, `eip155:137:${address}`],
        methods: ["eth_sendTransaction", "personal_sign", "eth_signTypedData"],
        events: ["chainChanged", "accountsChanged"],
      },
    },
  });
});

// Handle signing requests
web3wallet.on("session_request", async (event) => {
  const { request } = event.params;
  if (request.method === "eth_sendTransaction") {
    const [tx] = request.params;
    const signedTx = await wallet.signTransaction(tx);
    await web3wallet.respondSessionRequest({
      topic: event.topic,
      response: { id: event.id, jsonrpc: "2.0", result: signedTx },
    });
  }
});
```

**Required namespaces** define mandatory chains, methods, and events. **Optional namespaces** let the wallet add chains without re-approval:

```javascript
const requiredNamespaces = {
  eip155: {
    chains: ["eip155:1"],  // Ethereum mainnet
    methods: ["eth_sendTransaction", "personal_sign"],
    events: ["chainChanged", "accountsChanged"],
  },
};
const optionalNamespaces = {
  eip155: {
    chains: ["eip155:137", "eip155:10"],  // Polygon, Optimism
    methods: ["eth_sendTransaction"],
    events: ["chainChanged"],
  },
};
```

## Hardware Wallet Integration

### Ledger

```javascript
// @ethers-ext/signer-ledger
import { LedgerSigner } from "@ethers-ext/signer-ledger";
const signer = new LedgerSigner(provider, "44'/60'/0'/0/0");
const addr = await signer.getAddress();
const tx = await signer.sendTransaction({ to: "...", value: ethers.parseEther("0.01") });
await tx.wait();
```

```typescript
// viem + @shutter-network/viem-account-ledger
const client = createWalletClient({
  account: await ledgerWallet({ path: "m/44'/60'/0'/0/0" }),
  chain: mainnet, transport: http(),
});
const hash = await client.sendTransaction({ to: "0x...", value: parseEther("0.01") });
```

### Trezor

```javascript
import TrezorConnect from "@trezor/connect";
TrezorConnect.init({ manifest: { email: "dev@example.com", appUrl: "https://app.com" } });

const result = await TrezorConnect.ethereumSignTransaction({
  path: "m/44'/60'/0'/0/0",
  transaction: {
    to: "0xRecipient", value: "0x2386f26fc10000",
    gasLimit: "0x5208", nonce: "0x0", chainId: 1,
    maxFeePerGas: "0xBA43B7400", maxPriorityFeePerGas: "0x77359400",
  },
});
```

## Multi-Chain Management

### Chain ID Registry

```javascript
const CHAINS = {
  1:    { name: "Ethereum",   rpc: "https://eth-mainnet.g.alchemy.com/v2/KEY" },
  137:  { name: "Polygon",    rpc: "https://polygon-mainnet.g.alchemy.com/v2/KEY" },
  10:   { name: "Optimism",   rpc: "https://opt-mainnet.g.alchemy.com/v2/KEY" },
  42161:{ name: "Arbitrum",   rpc: "https://arb-mainnet.g.alchemy.com/v2/KEY" },
  8453: { name: "Base",       rpc: "https://base-mainnet.g.alchemy.com/v2/KEY" },
};
function getProvider(chainId) {
  return new ethers.JsonRpcProvider(CHAINS[chainId].rpc, chainId, { staticNetwork: true });
}
```

### RPC Failover Pattern

```javascript
// viem fallback transport
import { fallback, http } from "viem";
const transport = fallback([
  http("https://eth-mainnet.g.alchemy.com/v2/KEY1"),
  http("https://mainnet.infura.io/v3/KEY2"),
  http("https://rpc.ankr.com/eth"),
]);

// Manual failover
async function failoverSend(method, params) {
  for (const rpc of ["https://.../v2/KEY1", "https://.../v3/KEY2"]) {
    try {
      const resp = await fetch(rpc, { method: "POST", body: JSON.stringify({ method, params }) });
      const json = await resp.json();
      if (json.error) throw new Error(json.error.message);
      return json.result;
    } catch (e) { console.warn("RPC failed:", e.message); }
  }
  throw new Error("All RPCs failed");
}
```

### Non-EVM Chains

```javascript
// Solana — Ed25519 (not secp256k1)
import { Keypair, SystemProgram, Transaction, LAMPORTS_PER_SOL, Connection } from "@solana/web3.js";
import { derivePath } from "ed25519-hd-key";

const seed = ethers.utils.mnemonicToSeed(mnemonic);
const derived = derivePath("m/44'/501'/0'/0'", seed.toString("hex"));
const keypair = Keypair.fromSeed(derived.key);

const tx = new Transaction().add(SystemProgram.transfer({
  fromPubkey: keypair.publicKey, toPubkey: new PublicKey("recipient"),
  lamports: 0.01 * LAMPORTS_PER_SOL,
}));
await connection.sendTransaction(tx, [keypair]);
```

```javascript
// Bitcoin — PSBT with bitcoinjs-lib
import * as bitcoin from "bitcoinjs-lib";
import { ECPairFactory } from "ecpair";
const ECPair = ECPairFactory(ecc);
const psbt = new bitcoin.Psbt({ network: bitcoin.networks.bitcoin });
psbt.addInput({ hash: "prevTxId", index: 0 });
psbt.addOutput({ address: "bc1q...", value: 100000 });
psbt.signInput(0, ECPair.fromWIF("..."));
psbt.finalizeInput(0);
const txHex = psbt.extractTransaction().toHex();
await fetch("https://mempool.space/api/tx", { method: "POST", body: txHex });
```

## Gas Estimation

### eth_estimateGas vs Simulation

```javascript
// Estimate with 20% buffer
const estimate = await provider.estimateGas({ from, to, data });
const safeGas = estimate * 120n / 100n;

// Simulate first (catches reverts)
try {
  await provider.call({ from, to, data });
} catch (err) {
  console.error("Would revert:", err.reason); // Don't send this tx
}
```

### Fee Oracle (EIP-1559)

```javascript
// ethers.js
const feeData = await provider.getFeeData();
console.log({
  maxFee: ethers.formatUnits(feeData.maxFeePerGas, "gwei"),
  priority: ethers.formatUnits(feeData.maxPriorityFeePerGas, "gwei"),
});

// Custom: median base fee of last N blocks
async function customOracle(provider, n = 10) {
  const fees = [];
  for (let i = 0; i < n; i++) {
    const block = await provider.getBlock(await provider.getBlockNumber() - i);
    if (block.baseFeePerGas) fees.push(Number(block.baseFeePerGas));
  }
  fees.sort((a, b) => a - b);
  const median = fees[Math.floor(fees.length / 2)];
  return {
    maxFeePerGas: BigInt(Math.floor(median * 2)),
    maxPriorityFeePerGas: ethers.parseGwei("2"),
  };
}
```

### Per-Chain Gas Profile

| Chain | Gas Model | Block Time | Priority Fee |
|-------|-----------|-----------|-------------|
| Ethereum | EIP-1559 | 12s | 1-2 gwei |
| Polygon | EIP-1559 | 2s | 30-50 gwei |
| Arbitrum | L2 rollup | 0.25s | 0.1 gwei |
| Optimism | L2 rollup | 2s | 0.001 gwei |
| BNB Chain | Legacy | 3s | 3 gwei (gasPrice) |
| Avanlanche | EIP-1559 | 2s | 25 nAVAX |

## Security

### Never Log Private Keys

```javascript
// WRONG
console.log("Private key:", privateKey);   // DANGER
// CORRECT
console.log("Wallet address:", wallet.address);
// For debugging: one-way hash
console.log("PK hash:", ethers.keccak256(privateKey));
```

### Encrypted Storage

```javascript
// Browser — AES-GCM with PBKDF2
async function encryptAndStore(pk, password) {
  const salt = crypto.getRandomValues(new Uint8Array(32));
  const key = await crypto.subtle.importKey("raw",
    await deriveKey(password, salt), { name: "AES-GCM" }, false, ["encrypt"]);
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encrypted = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, new TextEncoder().encode(pk));
  localStorage.setItem("wallet", JSON.stringify({
    encrypted: btoa(String.fromCharCode(...new Uint8Array(encrypted))),
    iv: btoa(String.fromCharCode(...iv)), salt: btoa(String.fromCharCode(...salt)),
  }));
}

// Node.js — OS keychain
import keytar from "keytar";
await keytar.setPassword("MyApp", `wallet-${address}`, privateKey);
```

### Mnemonic Backup Verification

```javascript
function verifyMnemonic(mnemonic) {
  const words = mnemonic.split(" ");
  if (![12, 15, 18, 21, 24].includes(words.length)) return false;
  // Accept check: user re-enters words at positions 2, 5, 8
  const confirmWords = {}; // { 2: "word", 5: "word", 8: "word" }
  for (const [idx, word] of Object.entries(confirmWords)) {
    if (word !== words[idx]) return false;
  }
  return Mnemonic("english").check(mnemonic);
}
```

### WalletConnect Session Cleanup

```javascript
window.addEventListener("beforeunload", () => {
  Object.values(web3wallet?.getActiveSessions() || {}).forEach(s =>
    web3wallet.disconnectSession({ topic: s.topic }));
});
```

## Rate Limits

RPC providers enforce strict limits. Exceeding them causes 429s or dropped connections.

```javascript
// Token bucket limiter
class RpcLimiter {
  constructor(rps = 10) {
    this.tokens = rps; this.max = rps;
    this.interval = 1000 / rps; this.lastRefill = Date.now();
  }
  async acquire() {
    this.refill();
    if (this.tokens < 1) {
      await new Promise(r => setTimeout(r, this.interval));
      this.refill();
    }
    this.tokens--;
  }
  refill() {
    const now = Date.now();
    this.tokens = Math.min(this.max, this.tokens + (now - this.lastRefill) / this.interval);
    this.lastRefill = now;
  }
}

// Batch requests
const batch = new ethers.BatchProvider(provider);
const [b1, b2, b3] = await Promise.all([
  batch.getBalance(a1), batch.getBalance(a2), batch.getBalance(a3),
]);
```

| Provider | Free Tier | Rate Limit |
|----------|-----------|-----------|
| Alchemy | 300M CU/mo | 330 CU/s |
| Infura | 100K req/day | 100 req/s |
| QuickNode | 250K req/mo | 25 req/s |
| Ankr | 1M req/day | 100 req/s |
| Self-hosted | Unlimited | hardware |

## Common Patterns

### Nonce Management

```javascript
class NonceManager {
  constructor(address, provider) {
    this.address = address; this.provider = provider; this.pending = null;
  }
  async nextNonce() {
    const chain = await this.provider.getTransactionCount(this.address);
    if (this.pending === null || chain > this.pending) this.pending = chain;
    return this.pending++;
  }
  async send(tx) { return this.provider.getSigner().sendTransaction({ ...tx, nonce: await this.nextNonce() }); }
}
```

### Fee Bumping (Replace stuck tx)

```javascript
async function bumpFee(txHash, wallet, increasePct = 20n) {
  const tx = await provider.getTransaction(txHash);
  if (!tx || tx.confirmations > 0) throw new Error("Already confirmed");
  const increase = (100n + increasePct) * tx.maxFeePerGas / 100n;
  return wallet.sendTransaction({
    to: tx.to, value: tx.value, data: tx.data, nonce: tx.nonce,
    maxFeePerGas: increase,
    maxPriorityFeePerGas: (100n + increasePct) * tx.maxPriorityFeePerGas / 100n,
    gasLimit: tx.gasLimit, chainId: tx.chainId,
  });
}
```

### Address Confirmation

```javascript
function formatAddress(addr) { return `${addr.slice(0, 6)}...${addr.slice(-4)}`; }
// Always display recipient on screen before signing
```

## Red Flags

| Red Flag | Risk | Mitigation |
|----------|------|-----------|
| Private key logged to console | Complete loss of funds | Use structured logging with address only |
| Mnemonic stored in plaintext | Theft on disk compromise | Encrypt with AES-GCM + OS keychain |
| No backup verification | User locks themselves out | Require 3-word confirmation during setup |
| Hardcoded gas prices | Failed or overpriced txns | Use fee oracle + configurable multiplier |
| No nonce tracking | Stuck/collided txns | Use NonceManager pattern |
| Single RPC endpoint | Downtime on provider outage | Use fallback transport |
| Missing chain ID | Replay across chains | Always set chainId in every tx |
| No gas estimation | Wasted gas on revert | Simulate via eth_call first |
| HW path hardcoded | Wrong derivation | Make derivation path configurable |
| Session persists after logout | Session hijacking | Disconnect all sessions on logout |

## Verification Checklist

**Wallet Setup**
- [ ] Mnemonic generates valid entropy (12/15/18/21/24 words)
- [ ] BIP-44 derivation produces correct address for 3+ coin types
- [ ] Passphrase changes produce different wallet addresses
- [ ] EIP-55 checksum verification passes on all EVM chains

**Transaction Signing**
- [ ] EIP-1559 transaction sends with maxFeePerGas and maxPriorityFeePerGas
- [ ] Legacy transaction sends with gasPrice
- [ ] EIP-712 typed data signature verifies correctly with ecrecover
- [ ] personal_sign produces recoverable signature
- [ ] ERC-1271 contract validation returns correct magic value
- [ ] Insufficient balance fails gracefully with error message
- [ ] Fee bumping replaces unconfirmed tx within 6 blocks

**Multi-Chain**
- [ ] Same address works on 3+ EVM chains
- [ ] Chain ID validation prevents cross-chain replay
- [ ] RPC failover switches provider within 5 seconds on timeout
- [ ] Gas estimation returns values within 20% of actual cost

**Hardware Wallet**
- [ ] Ledger/Trezor path produces correct address (compare with vendor app)
- [ ] Transaction signing works with device
- [ ] Device disconnect/reconnect returns correct address

**Security**
- [ ] Private keys never logged, stored, or exposed in error messages
- [ ] Encrypted storage uses AES-256-GCM with PBKDF2
- [ ] WalletConnect sessions disconnect on app close
- [ ] Mnemonic backup requires re-entry of 3+ random words

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll store the mnemonic in app config, it's private" | Configs end up in git, CI logs, or cloud backups. Mnemonics belong on paper or in a hardware wallet. |
| "Custodial is fine for small balances — I'll self-custody later" | Later never comes. Self-custody from the first sat. |
| "Hot wallet is convenient, cold storage is too slow" | A hardware wallet adds 5 seconds per tx for 100x better protection. |
| "I only need one RPC — redundancy is overkill" | One provider downtime during a trade costs more than 3 API keys. |
| "EIP-1559 is complicated, I'll use legacy gasPrice" | Legacy overpays in quiet blocks and fails in congested ones. EIP-1559 saves 10-30%. |
| "I don't need nonce management for simple code" | One double-send or stuck tx from parallel calls wipes months of fee savings. |
| "Hardware wallet support is a future feature" | Adding it post-launch means re-architecting the signing layer. Add the interface day 1. |
| "Backup verification is unnecessary — users will test" | Users who write down the wrong word lose everything. Verify or ship a support nightmare. |
| "My private key is safe in an env file" | process.env leaks through error handlers, logging, and child processes. Encrypt with a password. |

## Process

1. **Determine wallet scope** — hot/cold/custodial, single-chain vs multi-chain, hardware support needed
2. **Select derivation scheme** — BIP-44 path per coin type, passphrase policy, account iteration range
3. **Generate mnemonic** — cryptographically secure entropy, 12 or 24 words depending on security requirements
4. **Implement address derivation** — EIP-55 for EVM, Bech32/P2PKH for Bitcoin, Ed25519 for Solana
5. **Build transaction signing** — EIP-1559 with fee estimation, legacy fallback, EIP-712 typed data
6. **Add multi-chain support** — chain ID registry, RPC failover, gas estimation per chain
7. **Integrate WalletConnect** — session proposals, namespace scoping, request handling
8. **Add hardware wallet** — Ledger/Trezor derivation path config, device disconnect handling
9. **Apply security hardening** — encrypted storage, mnemonic backup verification, session cleanup
10. **Test end-to-end** — derive addresses, sign transactions, broadcast on testnet, verify receipts
