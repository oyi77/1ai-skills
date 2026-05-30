---
name: nft-marketplace
description: NFT marketplace — ERC-721/1155, minting, auctions, royalties, metadata on IPFS

## Red Flags

- Metadata stored on HTTP URLs instead of IPFS/Arweave (mutable)
- Royalty enforcement bypassed in marketplace contract
- Lazy minting allows duplicate token IDs
- Auction end time manipulable by contract owner
- Escrow contract lacks timeout for stuck listings
- Token URI not set after mint (metadata inaccessible)

## Verification

After completing NFT marketplace implementation, confirm:

- [ ] ERC-721/1155 token standard compliance verified
- [ ] Lazy minting creates unique token IDs per creator
- [ ] EIP-2981 royaltyInfo returns correct recipient and amount
- [ ] IPFS CID used for metadata (not HTTP URLs)
- [ ] Escrow pattern handles buyer/seller disputes with timeout
- [ ] Auction logic enforces minimum bid increments and end times


## Red Flags

- Metadata stored on HTTP URLs instead of IPFS/Arweave (mutable)
- Royalty enforcement bypassed in marketplace contract
- Lazy minting allows duplicate token IDs
- Auction end time manipulable by contract owner
- Escrow contract lacks timeout for stuck listings

## Verification

After completing NFT marketplace implementation, confirm:

- [ ] ERC-721/1155 token standard compliance verified
- [ ] Lazy minting creates unique token IDs per creator
- [ ] EIP-2981 royaltyInfo returns correct recipient and amount
- [ ] IPFS CID used for metadata (not HTTP URLs)
- [ ] Escrow pattern handles buyer/seller disputes with timeout

---

## Overview

NFT marketplace development with ERC-721/1155, lazy minting, auction logic, royalty enforcement (EIP-2981), and metadata storage on IPFS/Arweave.

## Capabilities

- ERC-721/1155 token standards
- Lazy minting (gasless for creators)
- English/Dutch auctions
- Royalty enforcement (EIP-2981)
- Metadata on IPFS/Arweave
- Marketplace escrow

## When to Use

- NFT trading platforms
- Digital art/gaming marketplaces
- Creator royalty systems
- Auction platforms

## When NOT to Use

- Task is about portfolio management, not trading (use portfolio skills)
- Task is about financial analysis (use analysis skills)
- You need to analyze trade results (use analytics skills)
- Task is about risk management (use risk skills)
- You don't have trading capital
- Task requires financial advice (consult advisors)


## Pseudo Code

Reference implementations for lazy minting, marketplace escrow, and EIP-2981 royalty enforcement.


### Lazy Minting
```solidity
function mint(address to, uint tokenId, string memory uri) external {
    _safeMint(to, tokenId);
    _setTokenURI(tokenId, uri);
}

function buy(uint tokenId) external payable {
    require(msg.value >= price(tokenId));
    _transfer(creator(tokenId), msg.sender, tokenId);
    (bool ok, ) = creator(tokenId).call{value: msg.value - royalty(tokenId)}("");
}
```

### EIP-2981 Royalty
```solidity
function royaltyInfo(uint tokenId, uint salePrice) external view returns (address, uint) {
    return (creators[tokenId], salePrice * royaltyBps[tokenId] / 10000);
}
```

## Common Patterns

- IPFS CID for metadata (not HTTP URLs)
- Escrow pattern for safe trades
- Lazy mint to reduce creator gas costs
- EIP-2981 for on-chain royalties

## Red Flags

- Metadata stored on HTTP URLs instead of IPFS/Arweave (mutable)
- Royalty enforcement bypassed in marketplace contract
- Lazy minting allows duplicate token IDs
- Auction end time manipulable by contract owner
- Escrow contract lacks timeout for stuck listings

## Verification

After completing NFT marketplace implementation, confirm:

- [ ] ERC-721/1155 token standard compliance verified
- [ ] Lazy minting creates unique token IDs per creator
- [ ] EIP-2981 royaltyInfo returns correct recipient and amount
- [ ] IPFS CID used for metadata (not HTTP URLs)
- [ ] Escrow pattern handles buyer/seller disputes with timeout
