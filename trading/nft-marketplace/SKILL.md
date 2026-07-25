---
name: nft-marketplace
description: 'Skill: nft-marketplace. See SKILL.md body for details. Use when this domain is relevant.'
domain: trading
tags:
- algorithms
- marketplace
- markets
- nft
- trading
---
## Money-Making Overview

NFT marketplaces generate revenue through protocol fees (0.5-2.5% per trade), listing fees, and order-flow monetization. A marketplace doing $1M daily volume at 1% fee yields ~$3.6M/year gross. Liquidity bootstrapping through zero-fee periods, trader incentives, and EIP-2981 royalty enforcement drives volume.

## Revenue Streams

1. **Marketplace Fees** — Take rate on secondary trades (0.5-5%)
2. **Creator Royalties** — EIP-2981 enforcement (typically 2.5-10% per secondary sale)
3. **Lazy Minting Premium** — Per-mint fee on mint-on-sale fulfillment
4. **Aggregation Rebates** — Aggregators pay for order flow from the marketplace order book
5. **Trait/Collection Offer Spread** — Bid-ask capture on non-standard order types

## First Action in 60 Minutes

```bash
#!/usr/bin/env bash
mkdir -p ~/nft-marketplace/{contracts,test,scripts,subgraph}
echo "=== NFT Marketplace Architecture Check ==="
echo "1. Token standard: ERC-721 / ERC-1155 / both?"
echo "2. Order book: on-chain (escrow) / off-chain (signed orders)?"
echo "3. Royalty: EIP-2981 / Imanium basis points?"
echo "4. Metadata: IPFS CIDv1 / Arweave / on-chain?"
echo "5. Auction: English / Dutch / Sealed-bid?"
echo ""
echo "Gate: Pick ONE token standard and ONE order-book model"
echo "If <=$100K monthly volume -> on-chain escrow (simpler)"
echo "If >$100K monthly volume -> off-chain signed orders (cheaper)"
```

## Overview

NFT marketplace development spans token standards (ERC-721/1155/6551/4907), order matching, metadata permanence, royalty enforcement, and cross-market aggregation. Architecture choices determine gas costs, liquidity depth, and composability with aggregators like Reservoir and Seaport 1.6.

## When to Use

**Trigger phrases:**
- "nft marketplace"
- "NFT trading platforms"
- "Digital art/gaming marketplaces"
- "Creator royalty systems"

- Primary/secondary NFT trading platforms
- Auction platforms (English, Dutch, sealed-bid)
- Gaming/music/domain marketplaces
- Creator royalty enforcement (EIP-2981)
- Aggregator interfaces pulling from Reservoir, Seaport, Blur
- Collection offers, trait bidding, floor price tracking

## When NOT to Use

- Portfolio value tracking (use portfolio skills)
- DeFi LP/money market integration (use defi-protocols)
- Pure token minting without trading (use smart-contract-dev)
- On-chain analytics for existing marketplaces (use onchain-transaction-forensics)
- ERC-20 spot exchange (use liquidity pools, not NFTs)

## Token Standards

### ERC-721 (Ownership, Single Asset)

Each `tokenId` owned by exactly one address. Used for art, collectibles, domains.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ArtCollection is ERC721URIStorage, Ownable {
    uint public nextTokenId = 1;

    constructor() ERC721("ArtCollection", "ART") Ownable(msg.sender) {}

    function mint(string memory uri) external returns (uint tokenId) {
        tokenId = nextTokenId++;
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, uri);
    }
}
```

### ERC-1155 (Multi-Token, Batch Transfers)

Single contract for fungible and non-fungible token types. `balanceOf(address, id)` replaces per-token ownership. Gas-efficient for gaming assets where users hold many items.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";

contract GameItems is ERC1155 {
    mapping(uint => uint) public maxSupply;
    mapping(uint => uint) public minted;

    uint public constant SWORD = 1;
    uint public constant SHIELD = 2;

    constructor() ERC1155("https://api.game.io/metadata/{id}.json") {
        maxSupply[SWORD] = 100;
        maxSupply[SHIELD] = 50;
    }

    function mint(uint id, uint amount) external {
        require(maxSupply[id] == 0 || minted[id] + amount <= maxSupply[id], "supply exceeded");
        minted[id] += amount;
        _mint(msg.sender, id, amount, "");
    }
}
```

### ERC-6551 (Token-Bound Accounts)

Each ERC-721 token controls its own smart contract account, enabling NFTs to hold assets and interact with protocols independently.

```solidity
contract TokenBoundAccount {
    address public implementation;
    address public registry;

    function execute(address to, uint value, bytes calldata data)
        external returns (bytes memory result)
    {
        require(msg.sender == owner(), "not token owner");
        (bool ok, bytes memory res) = to.call{value: value}(data);
        require(ok, "call failed");
        return res;
    }

    function owner() public view returns (address) {
        // Derive from ERC-6551 registry
        (,,,, address nft, uint tokenId) = IERC6551Registry(registry).token(address(this));
        return IERC721(nft).ownerOf(tokenId);
    }
}
```

### ERC-4907 (Rentable NFTs)

Adds `user` and `expires` to ERC-721. Owner retains title; user gets usage rights for a limited period.

```solidity
contract RentableNFT is ERC721, IERC4907 {
    struct UserInfo { address user; uint64 expires; }
    mapping(uint => UserInfo) private _users;

    function setUser(uint tokenId, address user, uint64 expires) external {
        require(_isApprovedOrOwner(tokenId), "unauthorized");
        _users[tokenId] = UserInfo(user, expires);
        emit UpdateUser(tokenId, user, expires);
    }

    function userOf(uint tokenId) external view returns (address) {
        if (_users[tokenId].expires >= block.timestamp) return _users[tokenId].user;
        return address(0);
    }
}
```

## Marketplace Architecture

### Order Book Models

| Model | Gas/Trade | Liquidity | Complexity | Use Case |
|---|---|---|---|---|
| On-chain escrow | ~150K | Low | Low | Small collections |
| Off-chain signed | ~80K | High | Medium | Blur, OpenSea |
| Hybrid (deposit+sign) | ~40K | High | Medium | Seaport 1.6 |

### On-Chain Escrow

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract EscrowMarket is ERC721Holder, ReentrancyGuard {
    uint public protocolFeeBps = 100; // 1%
    uint public constant MAX_FEE = 500;

    struct Listing { address seller; address token; uint tokenId; uint price; bool active; }
    mapping(bytes32 => Listing) public listings;

    event Listed(bytes32 indexed listingId, address indexed seller, address indexed token, uint tokenId, uint price);
    event Sale(bytes32 indexed listingId, address indexed buyer, uint price);

    function list(address token, uint tokenId, uint price) external returns (bytes32 listingId) {
        IERC721(token).safeTransferFrom(msg.sender, address(this), tokenId);
        listingId = keccak256(abi.encode(token, tokenId, msg.sender, block.timestamp));
        listings[listingId] = Listing(msg.sender, token, tokenId, price, true);
        emit Listed(listingId, msg.sender, token, tokenId, price);
    }

    function buy(bytes32 listingId) external payable nonReentrant {
        Listing memory l = listings[listingId];
        require(l.active, "not active");
        require(msg.value >= l.price, "insufficient");
        listings[listingId].active = false;

        uint fee = msg.value * protocolFeeBps / 10000;
        (bool feeOk,) = owner().call{value: fee}(""); require(feeOk, "fee failed");
        IERC721(l.token).safeTransferFrom(address(this), msg.sender, l.tokenId);
        (bool payOk,) = l.seller.call{value: msg.value - fee}(""); require(payOk, "pay failed");
        emit Sale(listingId, msg.sender, msg.value);
    }

    function cancel(bytes32 listingId) external {
        Listing memory l = listings[listingId];
        require(msg.sender == l.seller && l.active, "cannot cancel");
        listings[listingId].active = false;
        IERC721(l.token).safeTransferFrom(address(this), l.seller, l.tokenId);
    }

    function owner() private view returns (address) { return tx.origin; } // simplified
}
```

### Off-Chain Signed Orders (EIP-712)

Orders signed off-chain — zero listing gas, submitted only on fill.

```solidity
contract SignedMarket is EIP712("SignedMarket", "1") {
    using ECDSA for bytes32;

    bytes32 constant ORDER_TYPE = keccak256(
        "Order(address maker,address token,uint256 tokenId,uint256 price,uint256 nonce,uint256 deadline)"
    );
    mapping(address => uint) public nonces;
    mapping(bytes32 => bool) public filled;

    /// @notice Taker fills a maker-signed order
    /// @param maker Address that signed the order — receives payment
    /// @param token NFT contract
    /// @param tokenId NFT token id
    /// @param price Sale price in wei
    /// @param deadline Block timestamp after which the order expires
    /// @param sig EIP-712 typed signature from maker
    function fill(
        address maker, address token, uint tokenId, uint price,
        uint deadline, bytes calldata sig
    ) external payable {
        bytes32 h = _hash(maker, token, tokenId, price, nonces[maker]++, deadline);
        require(!filled[h] && block.timestamp <= deadline, "invalid");
        require(h.recover(sig) == maker, "bad sig");
        require(msg.value >= price, "insufficient");
        filled[h] = true;

        // Transfer NFT maker -> taker (maker must approve this contract)
        IERC721(token).safeTransferFrom(maker, msg.sender, tokenId);
        // Pay maker
        (bool ok,) = maker.call{value: msg.value}(""); require(ok, "pay failed");
    }

    function _hash(address maker, address token, uint tokenId, uint price, uint nonce, uint deadline)
        internal view returns (bytes32)
    {
        return _hashTypedDataV4(keccak256(abi.encode(
            ORDER_TYPE, maker, token, tokenId, price, nonce, deadline
        )));
    }
}
```

## Lazy Minting

Creator signs an EIP-712 voucher off-chain. NFT minted on-chain only when a buyer fulfills — zero gas for the creator unless the item sells.

```solidity
contract LazyNFT is ERC721URIStorage, EIP712("LazyNFT", "1") {
    using ECDSA for bytes32;

    bytes32 constant VOUCHER_TYPE = keccak256(
        "NFTVoucher(uint256 tokenId,address creator,string uri,uint256 price,uint256 royaltyBps)"
    );
    mapping(bytes32 => bool) public redeemed;

    function redeem(address creator, string memory uri, uint price, uint royalty,
                    bytes calldata sig, address buyer) external payable returns (uint tokenId)
    {
        tokenId = uint(keccak256(abi.encodePacked(creator, block.timestamp)));
        bytes32 h = _hash(tokenId, creator, uri, price, royalty);
        require(!redeemed[h] && h.recover(sig) == creator && msg.value >= price, "invalid");
        redeemed[h] = true;
        _safeMint(buyer, tokenId);
        _setTokenURI(tokenId, uri);
        (bool ok,) = creator.call{value: msg.value}(""); require(ok, "pay failed");
    }

    function _hash(uint tokenId, address creator, string memory uri, uint price, uint royalty)
        internal view returns (bytes32)
    {
        return _hashTypedDataV4(keccak256(abi.encode(
            VOUCHER_TYPE, tokenId, creator, keccak256(bytes(uri)), price, royalty
        )));
    }
}
```

### Off-Chain Signing (TypeScript)

```typescript
import { ethers } from "ethers";

const VOUCHER_TYPE = {
  NFTVoucher: [
    { name: "tokenId", type: "uint256" }, { name: "creator", type: "address" },
    { name: "uri", type: "string" }, { name: "price", type: "uint256" },
    { name: "royaltyBps", type: "uint256" },
  ],
};

async function signVoucher(
  wallet: ethers.Wallet, tokenId: number, uri: string, price: bigint,
  royaltyBps: number, contractAddr: string
): Promise<string> {
  return wallet.signTypedData(
    { name: "LazyNFT", version: "1", chainId: 1, verifyingContract: contractAddr },
    VOUCHER_TYPE,
    { tokenId, creator: wallet.address, uri, price, royaltyBps }
  );
}
```

## Auction Types

### English Ascending

```solidity
contract EnglishAuction is ReentrancyGuard {
    struct Auction { address seller; address token; uint tokenId; uint reservePrice;
        uint highestBid; address highestBidder; uint endTime; uint bidIncrementBps; bool settled; }
    mapping(bytes32 => Auction) public auctions;
    mapping(bytes32 => mapping(address => uint)) public pendingReturns;

    function create(address token, uint tokenId, uint reserve, uint duration, uint incBps)
        external returns (bytes32 id)
    {
        IERC721(token).safeTransferFrom(msg.sender, address(this), tokenId);
        id = keccak256(abi.encode(token, tokenId, msg.sender));
        auctions[id] = Auction(msg.sender, token, tokenId, reserve, 0, address(0), block.timestamp + duration, incBps, false);
    }

    function bid(bytes32 id) external payable nonReentrant {
        Auction storage a = auctions[id];
        require(block.timestamp < a.endTime && !a.settled, "ended");
        uint minBid = a.highestBid == 0 ? a.reservePrice : a.highestBid + (a.highestBid * a.bidIncrementBps / 10000);
        require(msg.value >= minBid, "too low");
        if (a.highestBidder != address(0)) pendingReturns[id][a.highestBidder] += a.highestBid;
        a.highestBid = msg.value; a.highestBidder = msg.sender;
    }

    function settle(bytes32 id) external nonReentrant {
        Auction storage a = auctions[id];
        require(block.timestamp >= a.endTime && !a.settled, "cannot settle"); a.settled = true;
        if (a.highestBidder != address(0)) {
            IERC721(a.token).safeTransferFrom(address(this), a.highestBidder, a.tokenId);
            (bool ok,) = a.seller.call{value: a.highestBid}(""); require(ok, "pay failed");
        } else { IERC721(a.token).safeTransferFrom(address(this), a.seller, a.tokenId); }
    }
}
```

### Dutch Descending (Price Decay)

```solidity
contract DutchAuction {
    struct Auction { address seller; address token; uint tokenId; uint startPrice; uint endPrice; uint startTime; uint duration; bool settled; }
    mapping(bytes32 => Auction) public auctions;

    function create(address token, uint tokenId, uint start, uint end, uint dur) external returns (bytes32 id) {
        IERC721(token).safeTransferFrom(msg.sender, address(this), tokenId);
        id = keccak256(abi.encode(token, tokenId, msg.sender, block.timestamp));
        auctions[id] = Auction(msg.sender, token, tokenId, start, end, block.timestamp, dur, false);
    }

    function currentPrice(bytes32 id) public view returns (uint) {
        Auction storage a = auctions[id];
        if (block.timestamp >= a.startTime + a.duration) return a.endPrice;
        uint elapsed = block.timestamp - a.startTime;
        return a.startPrice - ((a.startPrice - a.endPrice) * elapsed / a.duration);
    }

    function buy(bytes32 id) external payable {
        Auction storage a = auctions[id]; require(!a.settled, "done");
        uint price = currentPrice(id); require(msg.value >= price, "insufficient"); a.settled = true;
        IERC721(a.token).safeTransferFrom(address(this), msg.sender, a.tokenId);
        (bool ok,) = a.seller.call{value: msg.value}(""); require(ok, "pay failed");
    }
}
```

### Sealed-Bid (Commit-Reveal)

Bidder commits `keccak256(amount, secret)`, then reveals. Prevents front-running.

```solidity
contract SealedBid {
    struct Bid { bytes32 commitment; bool revealed; uint amount; }
    mapping(bytes32 => mapping(address => Bid)) public bids;
    bytes32 public auctionId; uint public revealDeadline;
    address public highestBidder; uint public highestBid;

    function commit(bytes32 commitment) external {
        require(block.timestamp < revealDeadline, "too late");
        bids[auctionId][msg.sender].commitment = commitment;
    }

    function reveal(uint amount, bytes32 secret) external {
        Bid storage b = bids[auctionId][msg.sender];
        require(!b.revealed && b.commitment == keccak256(abi.encode(amount, secret)), "invalid");
        b.revealed = true; b.amount = amount;
        if (amount > highestBid) { highestBid = amount; highestBidder = msg.sender; }
    }
}
```

## Royalty Standards

### EIP-2981 (On-Chain)

```solidity
contract RoyaltyNFT is IERC2981 {
    struct RoyaltyInfo { address receiver; uint96 royaltyFraction; }
    mapping(uint => RoyaltyInfo) private _royalties;
    uint96 public constant MAX_ROYALTY = 1000; // 10% cap

    function royaltyInfo(uint tokenId, uint salePrice)
        external view returns (address receiver, uint royaltyAmount)
    {
        RoyaltyInfo memory r = _royalties[tokenId];
        return (r.receiver, salePrice * r.royaltyFraction / 10000);
    }

    function _setRoyalty(uint tokenId, address receiver, uint96 bps) internal {
        require(bps <= MAX_ROYALTY, "too high");
        _royalties[tokenId] = RoyaltyInfo(receiver, bps);
    }

    function supportsInterface(bytes4 interfaceId) public view virtual returns (bool) {
        return interfaceId == type(IERC2981).interfaceId || super.supportsInterface(interfaceId);
    }
}
```

### Royalty Registry

A centralized registry maps NFT contracts to royalty receivers, consumed at settlement time:

```solidity
contract RoyaltyRegistry {
    mapping(address => address) public overrides;
    function getRoyaltyInfo(address nft, uint tokenId, uint salePrice)
        external view returns (address receiver, uint amount)
    {
        return IERC2981(nft).royaltyInfo(tokenId, salePrice);
    }
}
```

### Imanium Fee Model

Seller fee deducted from proceeds: `sellerProceeds = price * (10000 - feeBps) / 10000`. Used by OpenSea (2.5% flat).

## Metadata

### ERC-721 Metadata Schema

```json
{
  "name": "Artwork #42",
  "description": "Generative art minted on chain.",
  "image": "ipfs://bafybeigdyrzt5mkx3q6hxjlnlq6m5v3s7xjl6r4z6p5kq6hxjlnlq6m5v3s",
  "attributes": [
    { "trait_type": "Background", "value": "Deep Blue" },
    { "display_type": "boost_percentage", "trait_type": "Rarity Boost", "value": 15 }
  ]
}
```

### IPFS (CIDv1)

```typescript
import { create } from "ipfs-http-client";

async function uploadMetadata(client: ReturnType<typeof create>, metadata: object): Promise<string> {
  const { cid } = await client.add(JSON.stringify(metadata), { pin: true, cidVersion: 1 });
  return `ipfs://${cid}`;
}
```

### Arweave (Permanent Storage)

```typescript
import Arweave from "arweave";
const arweave = Arweave.init({ host: "arweave.net", port: 443, protocol: "https" });

async function upload(data: object, key: any): Promise<string> {
  const tx = await arweave.createTransaction({ data: JSON.stringify(data) }, key);
  tx.addTag("Content-Type", "application/json");
  await arweave.transactions.sign(tx, key);
  const { status } = await arweave.transactions.post(tx);
  if (status !== 200 && status !== 208) throw new Error("upload failed");
  return `ar://${tx.id}`;
}
```

### On-Chain SVG/JSON

Fully on-chain: no external storage dependency.

```solidity
function tokenURI(uint tokenId) public view override returns (string memory) {
    string memory svg = '<svg ...><text x="10" y="20">Art</text></svg>';
    string memory json = string(abi.encodePacked(
        '{"name":"#', toString(tokenId), '","image":"data:image/svg+xml;base64,', base64Encode(bytes(svg)), '"}'
    ));
    return string(abi.encodePacked("data:application/json;base64,", base64Encode(bytes(json))));
}
```

## Aggregation and Advanced Trading

### Seaport 1.6 Integration

```typescript
import { Seaport } from "@opensea/seaport-js";

async function fulfillOrder(signer: ethers.Signer, order: any) {
  const seaport = new Seaport(signer);
  const { executeAllActions } = await seaport.fulfillOrder({ order, unitsToFill: 1 });
  const tx = await executeAllActions();
  return tx.hash;
}
```

### Reservoir Protocol (Aggregation)

```typescript
import { reservoirClient } from "@reservoir0x/reservoir-sdk";

const client = reservoirClient({ baseUrl: "https://api.reservoir.tools", apiKey: process.env.RESERVOIR_API_KEY! });

async function bestAsk(collection: string) {
  return (await client.orders.collectionsTopBid(collection)).data.topBid;
}

async function buyToken(contract: string, tokenId: string, taker: string) {
  return (await client.actions.buyToken({ items: [{ contract, tokenId, quantity: 1 }], taker, onlyQuote: false })).data;
}
```

### Blur Order Matching

Blur's off-chain engine aggregates bids across collections and traits. Orders are signed EIP-712 blobs submitted to a relayer for matching.

```typescript
interface BlurOrder {
  side: "buy" | "sell";
  collection: string;
  tokenId?: string; // null = collection offer
  price: string;    // wei
  expiration: number;
  nonce: number;
  signature: string;
}
```

### Collection Offers and Trait Bidding

```solidity
contract TraitBidding {
    struct TraitBid { address bidder; address token; string traitType; string traitValue; uint price; uint deadline; }
    mapping(bytes32 => TraitBid) public traitBids;

    function placeTraitBid(address token, string calldata traitType, string calldata traitValue, uint price, uint deadline)
        external payable returns (bytes32 bidId)
    {
        bidId = keccak256(abi.encode(msg.sender, token, traitType, traitValue, block.timestamp));
        traitBids[bidId] = TraitBid(msg.sender, token, traitType, traitValue, price, deadline);
    }

    // Seller fills trait bid by proving trait via merkle proof or on-chain query
    function fillTraitBid(bytes32 bidId, uint tokenId) external {
        TraitBid storage tb = traitBids[bidId];
        require(block.timestamp < tb.deadline, "expired");
        // Verify trait, transfer token, pay seller
        emit TraitBidFilled(bidId, tokenId, msg.sender, tb.price);
    }
}
```

### Floor Price Tracking

```typescript
async function getFloorPrice(collectionAddress: string): Promise<bigint> {
  const resp = await fetch(
    `https://api.reservoir.tools/collections/v7?id=${collectionAddress}`,
    { headers: { "x-api-key": process.env.RESERVOIR_API_KEY! } }
  );
  const { collections } = await resp.json();
  return BigInt(collections[0]?.floorAsk?.price?.amount?.native ?? "0");
}
```

### TheGraph Subgraph

```graphql
type Listing @entity {
  id: ID!
  seller: Bytes!
  token: Bytes!
  tokenId: BigInt!
  price: BigInt!
  active: Boolean!
  buyer: Bytes
  filledAt: BigInt
}

type Collection @entity {
  id: ID!
  name: String
  floorPrice: BigInt
  totalVolume: BigInt!
  tradeCount: BigInt!
}
```

```typescript
// mapping.ts
export function handleSale(event: SaleEvent): void {
  let listing = Listing.load(event.params.listingId.toHex());
  if (listing) { listing.active = false; listing.buyer = event.params.buyer; listing.filledAt = event.block.timestamp; listing.save(); }
  let c = Collection.load(event.params.token.toHex());
  if (!c) { c = new Collection(event.params.token.toHex()); c.totalVolume = BigInt.zero(); c.tradeCount = BigInt.zero(); }
  c.totalVolume = c.totalVolume.plus(event.params.price);
  c.tradeCount = c.tradeCount.plus(BigInt.fromU32(1));
  c.save();
}
```

## Python / web3.py Query

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"))
ERC721_ABI = [...]  # balanceOf, ownerOf, tokenURI, royaltyInfo

def inspect_nft(contract_address: str, token_id: int) -> dict:
    c = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=ERC721_ABI)
    owner = c.functions.ownerOf(token_id).call()
    uri = c.functions.tokenURI(token_id).call()
    receiver, amount = c.functions.royaltyInfo(token_id, 1_000_000).call()
    return {"token_id": token_id, "owner": owner, "uri": uri, "royalty_bps": amount * 10000 // 1_000_000}
```

## Hardhat Tests

```typescript
import { expect } from "chai";
import { ethers } from "hardhat";

describe("EscrowMarket", function () {
  it("should list and buy an NFT", async () => {
    const [seller, buyer] = await ethers.getSigners();
    const NFT = await (await ethers.getContractFactory("TestNFT")).deploy();
    const Market = await (await ethers.getContractFactory("EscrowMarket")).deploy();
    await NFT.mint(seller.address, 1);
    await NFT.connect(seller).setApprovalForAll(await Market.getAddress(), true);
    const tx = await Market.connect(seller).list(await NFT.getAddress(), 1, ethers.parseEther("1"));
    const listingId = (await tx.wait())!.logs[2].topics[1];
    await Market.connect(buyer).buy(listingId, { value: ethers.parseEther("1") });
    expect(await NFT.ownerOf(1)).to.equal(buyer.address);
  });

  it("should deduct protocol fee", async () => {
    const [seller, buyer] = await ethers.getSigners();
    const NFT = await (await ethers.getContractFactory("TestNFT")).deploy();
    const Market = await (await ethers.getContractFactory("EscrowMarket")).deploy();
    await NFT.mint(seller.address, 1);
    await NFT.connect(seller).setApprovalForAll(await Market.getAddress(), true);
    const price = ethers.parseEther("1");
    const tx = await Market.connect(seller).list(await NFT.getAddress(), 1, price);
    const listingId = (await tx.wait())!.logs[2].topics[1];
    const before = await ethers.provider.getBalance(seller.address);
    await Market.connect(buyer).buy(listingId, { value: price });
    const after = await ethers.provider.getBalance(seller.address);
    const fee = price * (await Market.protocolFeeBps()) / 10000n;
    expect(after - before).to.equal(price - fee);
  });
});
```

## Common Patterns

1. **On-Chain Settlement** — Single contract validates payment, royalty, and ownership atomically. Prevents partial-fill race conditions.

2. **Signature-Based Approvals** — Off-chain signed orders (EIP-712) avoid per-listing gas. Schema includes `nonce` (replay protection), `deadline` (expiry), and maker/taker addresses.

3. **Cancel-All with Nonce Invalidation** — Increment a global nonce to cancel all outstanding orders:
```solidity
mapping(address => uint) public nonces;
function cancelAll() external { nonces[msg.sender]++; }
```

4. **Merkle Tree for Allowlist / Trait Bids** — Root stored on-chain; sellers prove inclusion via proof:
```solidity
function buyWithAllowlist(bytes32[] calldata proof) external payable {
    require(MerkleProof.verify(proof, merkleRoot, keccak256(abi.encodePacked(msg.sender))), "not allowed");
}
```

5. **Conduit Pattern (Seaport)** — Single conduit holds all approvals. Users approve once; marketplace contracts execute transfers through it, saving per-marketplace approval gas.

6. **Merkle Tree for Trait Verification** — Root stores allowed trait values. Seller proves token has the trait via leaf = `keccak256(tokenId, traitValue)`.

7. **Dutch Auction with Reserve** — If no one buys before price hits `endPrice`, the auction expires with no sale. Buyer can trigger `buy()` at any intermediate price.

## Red Flags

- **Unsafe `safeTransferFrom` ordering** — Calling `safeTransferFrom(token, buyer, tokenId)` before verifying payment enables reentrancy. Transfer after payment, or use pull-payment.
- **Royalty bypass via low-level call** — `call{value: price}` without EIP-2981 deduction lets buyers bypass creator fees. Always call `royaltyInfo` before payout.
- **Cross-chain bridge without burn verification** — Minting target-side NFT without verifying the source burn enables inflation (wormhole-style).
- **Auction end time manipulable** — `block.timestamp` allows ~15s miner manipulation. Use block numbers for time-sensitive auctions, or commit-reveal.
- **Lazy minting duplicate token IDs** — `keccak256(abi.encode(creator, block.timestamp))` is collision-safe, but using `msg.sender` as creator allows fulfilling someone else's voucher.
- **No cancel timeout on escrow** — NFTs locked forever without a seller cancel path. Always provide `cancel()` for active listings.
- **Fee-on-transfer NFT tokens** — If token contract charges a transfer fee, `msg.value == price` underpays seller. Track actual received balance.
- **Off-chain order replay across chains** — Signature lacks `chainId` in EIP-712 domain. Anyone can replay an Ethereum order on Polygon without binding `chainId`.

## Verification Checklist

### Token Standard
- [ ] ERC-721 metadata conforms to OpenSea/enum schema
- [ ] ERC-1155 `uri()` returns per-token-type metadata
- [ ] ERC-6551 account executes only from the token owner
- [ ] ERC-4907 `userOf()` respects `expires` timestamp

### Marketplace Contracts
- [ ] Protocol fee capped (<= 5%)
- [ ] ReentrancyGuard on all payable entry points
- [ ] Escrow has seller cancel/withdraw path
- [ ] Off-chain orders use EIP-712 + nonce + deadline
- [ ] Cancel-all atomically increments nonce

### Auction
- [ ] English auction enforces minimum bid increment
- [ ] Dutch auction `price()` is monotonic decreasing
- [ ] Sealed-bid commitment includes salt (prevent rainbow table)
- [ ] Anyone can trigger settlement (not only seller/buyer)

### Royalty
- [ ] EIP-2981 `royaltyInfo` called before every payout
- [ ] Royalty cap enforced (<= 1000 bps / 10%)
- [ ] Registry supports override per collection

### Metadata
- [ ] Token URI returns valid JSON
- [ ] IPFS CIDs use CIDv1 (not CIDv0 or HTTP gateway)
- [ ] Arweave transaction confirmed (status 200/208)

## Anti-Rationalization

| Excuse | Truth |
|---|---|
| "An aggregator is the same as a marketplace" | Aggregators route to external markets. A marketplace owns the order book; aggregators earn rebates but don't control liquidity. |
| "On-chain order book is always better" | On-chain costs gas per listing and locks tokens. Off-chain signed orders scale to millions of listings with zero listing gas. Choose by expected volume. |
| "IPFS is better than Arweave for all metadata" | IPFS needs pinning services for persistence; Arweave is permanent with upfront cost. Hybrid: Arweave for immutable artwork, IPFS for updatable descriptions. |
| "Royalty enforcement is mandatory for growth" | Markets enforcing EIP-2981 (OpenSea legacy) lost volume to optional-royalty markets (Blur). The trade-off between creator alignment and liquidity capture is real. |
| "Event logs are sufficient — I don't need a subgraph" | Ethereum prunes event logs after ~128 blocks. Without an indexer, floor price trends and historical trade data are inaccessible. |
| "ERC-1155 is always cheaper than ERC-721" | Batch mints are cheaper, but single transfers cost more due to the `amount` parameter. Profile your use case before choosing. |

## Workflow

1. Choose token standard (ERC-721 / 1155 / both) based on asset type and batch requirements
2. Select order book model: on-chain escrow for <$100K volume, off-chain signed orders for scale
3. Implement settlement contracts with reentrancy guards and fee enforcement
4. Integrate EIP-2981 royalty with on-chain deduction before seller payout
5. Add lazy minting if creators should avoid upfront mint gas
6. Deploy a subgraph (TheGraph) for event indexing, floor price tracking, and historical queries
7. Integrate aggregation APIs (Reservoir, Seaport 1.6) for cross-marketplace liquidity
8. Test with Hardhat/Foundry: list/buy/cancel cycle, auction edge cases, royalty math
9. Verify metadata on IPFS/Arweave with correct CID and schema
10. Monitor collection-level and trait-level bid activity; emit on-chain events for oracle updates
