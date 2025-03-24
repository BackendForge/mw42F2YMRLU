from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

SPOTTER_ADDRESS = Web3.to_checksum_address("0x65C79fcB50Ca1594B025960e539eD7A9a6D434A3")  # mainnet
EXPECTED_OSM = Web3.to_checksum_address("0x81FE72B5A8d1A857d176C3E7d5Bd2679A9B85763")  # known OSM for ETH-A

ilk = Web3.to_bytes(text="ETH-A").ljust(32, b'\0')

spotter_abi = json.loads('''
[
  {
    "constant": true,
    "inputs": [{"name": "", "type": "bytes32"}],
    "name": "ilks",
    "outputs": [
      {"name": "pip", "type": "address"},
      {"name": "mat", "type": "uint256"}
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
''')

spotter = w3.eth.contract(address=SPOTTER_ADDRESS, abi=spotter_abi)
actual_pip, mat = spotter.functions.ilks(ilk).call()

print("Actual OSM address for ETH-A:", actual_pip)
print("Expected OSM address:", EXPECTED_OSM)

if actual_pip.lower() == EXPECTED_OSM.lower():
    print("✅ Spotter is configured with the correct OSM.")
else:
    print("❌ Spotter is NOT using the expected OSM.")
