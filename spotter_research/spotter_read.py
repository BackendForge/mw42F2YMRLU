from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
# Connect to Ethereum
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Addresses (mainnet)
SPOTTER_ADDR = Web3.to_checksum_address("0x65C79fcB50Ca1594B025960e539eD7A9a6D434A3")
VAT_ADDR = Web3.to_checksum_address("0x35d1b3f3d7966a1dfe207aa4514c12a259a0492b")

# Ilk to query
ILK = Web3.to_bytes(text="ETH-A").ljust(32, b'\0')
RAY = 10 ** 27

# Minimal ABIs
spotter_abi = json.loads('''
[
  {
    "constant": true,
    "inputs": [],
    "name": "par",
    "outputs": [{"name": "", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
  }
]
''')

vat_abi = json.loads('''
[
  {
    "constant": true,
    "inputs": [{"name": "", "type": "bytes32"}],
    "name": "ilks",
    "outputs": [
      {"name": "Art", "type": "uint256"},
      {"name": "rate", "type": "uint256"},
      {"name": "spot", "type": "uint256"},
      {"name": "line", "type": "uint256"},
      {"name": "dust", "type": "uint256"}
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
''')

# Load contracts
spotter = w3.eth.contract(address=SPOTTER_ADDR, abi=spotter_abi)
vat = w3.eth.contract(address=VAT_ADDR, abi=vat_abi)

# Read par from Spotter (DAI/USD peg, usually 1e27)
par = spotter.functions.par().call()

# Read `spot` from Vat.ilks — this is the collateral's price in internal units
ilk_data = vat.functions.ilks(ILK).call()
raw_spot = ilk_data[2]  # spot

# Calculate price
price = (raw_spot * par) / RAY**2  # because spot and par are both RAY-scaled (1e27)

print(f"ETH-A price: {price:.18f} DAI")
