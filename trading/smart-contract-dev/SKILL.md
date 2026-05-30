---
name: smart-contract-dev
description: Smart contract development — Solidity, Hardhat, Foundry. DeFi, NFTs, upgradeable contracts, security patterns

## Red Flags

- Missing ReentrancyGuard on external state-changing functions
- Ownable contract uses deprecated Ownable instead of Ownable2Step
- No access control on critical admin functions (mint, pause, upgrade)
- Upgradeable proxy missing _authorizeUpgrade override
- Constructor sets state that initializer should set (bypassed in proxy)
- Hardcoded gas limits that may break on network upgrades

## Verification

After completing smart contract development, confirm:

- [ ] All external state changes follow Checks-Effects-Interactions pattern
- [ ] ReentrancyGuard applied to withdrawal and transfer functions
- [ ] AccessControl or Ownable2Step used for admin functions
- [ ] Unit tests cover happy path, revert conditions, and edge cases
- [ ] Fork tests validate behavior against mainnet state
- [ ] Upgradeable contracts tested with proxy deployment and upgrade flow


## Red Flags

- Missing ReentrancyGuard on external state-changing functions
- Ownable contract uses deprecated Ownable instead of Ownable2Step
- No access control on critical admin functions (mint, pause, upgrade)
- Upgradeable proxy missing _authorizeUpgrade override
- Hardcoded gas limits that may break on network upgrades

## Verification

After completing smart contract development, confirm:

- [ ] All external state changes follow Checks-Effects-Interactions pattern
- [ ] ReentrancyGuard applied to withdrawal and transfer functions
- [ ] AccessControl or Ownable2Step used for admin functions
- [ ] Unit tests cover happy path, revert conditions, and edge cases
- [ ] Fork tests validate behavior against mainnet state

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

## When NOT to Use

- Task is about portfolio management, not trading (use portfolio skills)
- Task is about financial analysis (use analysis skills)
- You need to analyze trade results (use analytics skills)
- Task is about risk management (use risk skills)
- You don't have trading capital
- Task requires financial advice (consult advisors)


## Pseudo Code

Reference implementations for ERC-20 tokens, Hardhat/Foundry tests, and UUPS upgradeable proxies.


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

## Red Flags

- Missing ReentrancyGuard on external state-changing functions
- Ownable contract uses deprecated Ownable instead of Ownable2Step
- No access control on critical admin functions (mint, pause, upgrade)
- Upgradeable proxy missing _authorizeUpgrade override
- Hardcoded gas limits that may break on network upgrades

## Verification

After completing smart contract development, confirm:

- [ ] All external state changes follow Checks-Effects-Interactions pattern
- [ ] ReentrancyGuard applied to withdrawal and transfer functions
- [ ] AccessControl or Ownable2Step used for admin functions
- [ ] Unit tests cover happy path, revert conditions, and edge cases
- [ ] Fork tests validate behavior against mainnet state
