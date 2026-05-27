---
name: nft-marketplace
description: NFT marketplace — ERC-721/1155, minting, auctions, royalties, metadata on IPFS
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

## Pseudo Code

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
