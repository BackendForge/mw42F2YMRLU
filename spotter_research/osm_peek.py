from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# OSM contract address from Spotter.ilks("ETH-A")
OSM_ADDRESS = "0x81FE72B5A8d1A857d176C3E7d5Bd2679A9B85763"  # example for ETH-A
your_contracts = {
    "0x135954d155898D42C90D2a57824C690e0c7BEf1B": "dog",
    "0x65C79fcB50Ca1594B025960e539eD7A9a6D434A3": "spotter",
    "0x0e2e8F1D1326A4B9633D96222Ce399c708B19c28": "end",
    "0xc67963a226eddd77B91aD8c421630A1b0AdFF270": "clipper-eth-a",
    # more clippers . . .
}

osm_abi = json.loads(
    """
[
    {
        "constant": true,
        "inputs": [],
        "name": "peek",
        "outputs": [
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
            {"internalType": "bool", "name": "", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "read",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [{"name": "", "type": "address"}],
        "name": "bud",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }                                          
]
"""
)

osm = w3.eth.contract(address=Web3.to_checksum_address(OSM_ADDRESS), abi=osm_abi)

# Read the price from the OSM - will fail: OSM/contract-not-whitelisted

# NOT REVERTS IF:
# - The price is valid
# - The caller is whitelisted
try:
    price_bytes, valid = osm.functions.peek().call()
    if valid:
        price = int.from_bytes(price_bytes, byteorder="big")
        print(f"DAI price from OSM: {price} (usually scaled by 1e18)")
    else:
        print("Price not valid yet")
except Exception as e:
    print(f"OSM access failed: {e}")

for your_contract, name in your_contracts.items():
    osm_bud = w3.eth.contract(address=OSM_ADDRESS, abi=osm_abi)
    is_whitelisted = (
        osm_bud.functions.bud(Web3.to_checksum_address(your_contract)).call() > 0
    )
    print(f"Whitelisted for {name} @ {your_contract}:", is_whitelisted)
