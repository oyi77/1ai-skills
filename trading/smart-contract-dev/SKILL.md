---
name: smart-contract-dev
description: Smart contract development — Solidity, Hardhat, Foundry. DeFi, NFTs, upgradeable contracts, security patterns
---

## Overview

Smart contract development for EVM chains using Solidity. Hardhat and Foundry toolchains, testing, deployment, upgradeable proxies, and security patterns.

## Capabilities

- Solidity contracts (ERC-20, ERC-721, ERC-1155)
- Hardhat and Foundry development
- Unit/integration/fork testing
- Upgradeable contracts (UUPS, Transparent Proxy)
- Security patterns (reentrancy, access control)

## When to Use

- DeFi protocols (DEX, lending, staking)
- NFT collections and marketplaces
- DAOs and governance
- Token-based applications

## Pseudo Code

### ERC-20 (OpenZeppelin)
```solidity
contract MyToken is ERC20, Ownable {
    constructor() ERC20("MyToken", "MTK") Ownable(msg.sender) {
        _mint(msg.sender, 1_000_000 * 10**decimals());
    }
}
```

### Hardhat Test
```javascript
it("should mint", async () => {
    const token = await (await ethers.getContractFactory("MyToken")).deploy();
    expect(await token.balanceOf(owner.address)).to.equal(ethers.parseEther("1000000"));
});
```

### Foundry Test
```solidity
function testMint() public {
    token.mint(address(1), 1000);
    assertEq(token.balanceOf(address(1)), 1000);
}
```

### UUPS Upgradeable
```solidity
contract MyV1 is UUPSUpgradeable, OwnableUpgradeable {
    function initialize(address _owner) public initializer {
        __Ownable_init(_owner); __UUPSUpgradeable_init();
    }
    function _authorizeUpgrade(address) internal override onlyOwner {}
}
```

## Common Patterns

- ReentrancyGuard on all external state changes
- AccessControl for role-based permissions
- Pull over push for payments
- Checks-Effects-Interactions pattern
