// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface MakerVat {
    function frob(bytes32 ilk, int256 dink, int256 dart) external;
    function move(address src, address dst, uint256 rad) external;
    function hope(address usr) external;
}

interface DaiJoin {
    function exit(address guy, uint256 wad) external;
}

interface CDPManager {
    function frob(uint cdp, int dink, int dart) external;
    function move(uint cdp, address dst, uint rad) external;
    function urns(uint cdp) external view returns (address);
    function ilks(uint cdp) external view returns (bytes32);
}

contract MakerVaultManager {
    address public owner;
    MakerVat public vat;
    DaiJoin public daiJoin;
    CDPManager public cdpManager;
    bytes32 public ilk;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _;
    }

    constructor(address _vat, address _daiJoin, address _cdpManager, bytes32 _ilk) {
        owner = msg.sender;
        vat = MakerVat(_vat);
        daiJoin = DaiJoin(_daiJoin);
        cdpManager = CDPManager(_cdpManager);
        ilk = _ilk;
        vat.hope(_daiJoin);
    }

    function justBorrowAndExit(uint cdpId, int256 dink, uint256 daiAmount) external onlyOwner {
        int256 dart = int256(daiAmount * 1 ether ); // Convert to 18 decimals
        
        // 1. Borrow DAI (increase debt in vault)
        // dink = how many tokens to lock, can be 0
        cdpManager.frob(cdpId, dink, dart);

        // 2. Move DAI from the vault to user's internal balance
        cdpManager.move(cdpId, address(this), uint256(dart));

        // 3. Exit DAI from Maker's system to the owner’s wallet
        daiJoin.exit(owner, daiAmount);
    }
}
