# fin-crypto-forensic: Blockchain Forensics & OSINT

## Use Cases
- Hack tracing and fund movement tracking
- Wallet clustering and entity identification
- Exchange drain monitoring (pre-hack signal)
- Sanctions compliance (OFAC SDN wallet screening)
- Smart contract exploit analysis

---

## Transaction Tracing Framework

### Step 1: Seed Address Identification
- Start with known address (hack victim, suspicious wallet, entity of interest)
- Tools: Etherscan, Solscan, Blockchain.com, Mempool.space

### Step 2: Clustering Analysis
- Common-input ownership heuristic: inputs spent together = likely same entity
- Exchange deposit reuse: same deposit address = same user
- Tools: Chainalysis Reactor, Arkham Intelligence, TRM Labs

### Step 3: Taint Analysis
- Track "tainted" funds through mixing services, bridges, and DEXes
- Heuristics: FIFO, LIFO, haircut method
- Note: Legal taint vs. technical taint distinction

### Step 4: Exchange Flow Monitoring
- Sudden large inflows to exchanges before protocol exploits = insider signal
- Monitor top 10 exchange hot wallets for anomalous inflows

### Step 5: OSINT Layer
- Link wallet to social identity (ENS names, on-chain attestations, Twitter/X)
- Polymarket / Manifold resolution addresses
- Governance voting history (on-chain governance)

---

## Red Flags for Portfolio Risk
- Project multisig signers dumping tokens pre-announcement
- Treasury wallet moving funds to non-disclosed addresses
- Large unlabeled wallet accumulating before major catalyst
- Bridge contracts receiving unusual inflows (bridge exploit pattern)

---

## Forensic Tools Reference
| Tool | Use Case | Access |
|------|----------|--------|
| Etherscan / Solscan | Transaction lookup, contract interaction | Free |
| Arkham Intelligence | Wallet labeling, entity graphs | Free/Pro |
| Dune Analytics | Custom on-chain queries | Free/Pro |
| Chainalysis Reactor | Professional taint analysis | Enterprise |
| TRM Labs | Compliance screening | Enterprise |
| Breadcrumbs | Visual wallet tracing | Free/Pro |
