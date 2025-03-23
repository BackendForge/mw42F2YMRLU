// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// import {Script} from "forge-std/Script.sol";
import "forge-std/Script.sol";
import {MakerVaultManager} from "../src/mkrVault.sol";

// forge script script/mkrVault.s.sol:DeployMakerVaultManager --broadcast --rpc-url https://rpc-pulsechain.g4mm4.io

contract DeployMakerVaultManager is Script {
    function setUp() public {}

    function run() public {
        // Hardcoded receiver addresses (update as needed)
       
        address vat = vm.envAddress("VAT_ADDRESS");
        address daiJoin = vm.envAddress("GEM_ADDRESS");
        address cdpManager = vm.envAddress("CDP_MANAGER_ADDRESS");
        bytes32 ilk = bytes32(bytes(vm.envString("ILK")));


        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);
        // Deploy the contract
        MakerVaultManager mkr = new MakerVaultManager(vat, daiJoin, cdpManager, ilk);

        console.log("MakerVaultManager deployed at:", address(mkr));

        vm.stopBroadcast();
    }
}
